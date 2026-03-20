import streamlit as st
import time
import os
import pandas as pd
import plotly.express as px
from database import init_db, insert_log, get_logs, get_anomaly_count, get_total_count
from file_watcher import get_new_logs
from detector import detect
import threading

def background_log_generator():
    from log_generator import start_generating
    thread = threading.Thread(
        target=start_generating,
        daemon=True
    )
    thread.start()

# Start generator automatically when app loads
if "generator_started" not in st.session_state:
    background_log_generator()
    st.session_state.generator_started = True

st.set_page_config(
    page_title="AIOps - Live Anomaly Detection",
    page_icon="🔍",
    layout="wide"
)

init_db()

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")
    
    algorithm = st.radio(
        "Select Algorithm",
        ["Isolation Forest", "LSTM"],
        index=0
    )
    
    st.markdown("---")
    
    if algorithm == "Isolation Forest":
        st.info("""
        **Isolation Forest**
        - Unsupervised ML
        - Trains on first 50 logs
        - Fast and lightweight
        - Industry standard baseline
        """)
    else:
        st.info("""
        **LSTM**
        - Sequence-based detection
        - Learns log patterns over time
        - Detects temporal anomalies
        - Better for sequential data
        """)
    
    st.markdown("---")
    st.caption("AIOps Log Anomaly Detection")
    st.caption("Built with Streamlit + Scikit-learn")

# Session state
if "running" not in st.session_state:
    st.session_state.running = False
if "file_position" not in st.session_state:
    st.session_state.file_position = 0
if "last_log" not in st.session_state:
    st.session_state.last_log = None

st.title("🔍 AIOps — Live Log Anomaly Detection")
st.markdown(f"Watching live log file · Detecting anomalies in real time · Algorithm: **{algorithm}**")

# Controls
col1, col2, col3 = st.columns(3)
with col1:
    start = st.button("▶ Start Watching", use_container_width=True)
with col2:
    stop = st.button("⏹ Stop Watching", use_container_width=True)
with col3:
    clear = st.button("🗑 Clear Data", use_container_width=True)

if start:
    st.session_state.running = True

if stop:
    st.session_state.running = False

if clear:
    if os.path.exists("data/logs.db"):
        os.remove("data/logs.db")
    init_db()
    st.session_state.file_position = 0
    st.session_state.last_log = None
    st.session_state.running = False
    st.success("Data cleared!")

# Status
if st.session_state.running:
    st.success("🟢 Watching live_logs.log — new logs detected every second")
else:
    st.warning("🔴 Stopped — click Start Watching to begin")

st.markdown("---")

# Metrics
m1, m2, m3, m4 = st.columns(4)
total = get_total_count()
anomalies = get_anomaly_count()
normal = total - anomalies
rate = round((anomalies / total * 100), 2) if total > 0 else 0

m1.metric("Total Logs", total)
m2.metric("Anomalies", anomalies)
m3.metric("Normal", normal)
m4.metric("Anomaly Rate", f"{rate}%")

st.markdown("---")

# Charts
df = get_logs(500)

if not df.empty:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Log Volume by Service")
        fig = px.bar(
            df.groupby('service').size().reset_index(name='count'),
            x='service', y='count', color='service'
        )
        st.plotly_chart(fig, use_container_width=True, key="chart1")

    with c2:
        st.subheader("Anomaly vs Normal")
        fig2 = px.pie(
            pd.DataFrame({
                'Type': ['Normal', 'Anomaly'],
                'Count': [normal, anomalies]
            }),
            names='Type', values='Count',
            color_discrete_map={
                'Normal': '#22c55e',
                'Anomaly': '#ef4444'
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Anomaly timeline
    st.subheader("Live Anomaly Timeline")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    timeline = df.groupby(
        pd.Grouper(key='timestamp', freq='10s')
    ).agg(
        total=('anomaly', 'count'),
        anomalies=('anomaly', 'sum')
    ).reset_index()
    fig3 = px.line(
        timeline, x='timestamp', y=['total', 'anomalies'],
        color_discrete_map={
            'total': '#3b82f6',
            'anomalies': '#ef4444'
        }
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Live log feed
    st.subheader("Live Log Feed")
    recent = df[['timestamp', 'level', 'service',
                 'message', 'anomaly']].head(20)
    st.dataframe(recent, use_container_width=True)

else:
    st.info("No logs yet — start log_generator.py then click Start Watching!")

# Show last processed log
if st.session_state.last_log:
    log = st.session_state.last_log
    st.markdown("---")
    st.caption(
        f"⚡ Last log: `{log['level']}` | `{log['service']}` | "
        f"`{log['message']}` | "
        f"{'🔴 ANOMALY' if log['anomaly'] == 1 else '🟢 Normal'}"
    )

# Continuous watcher
if st.session_state.running:
    new_logs, new_position = get_new_logs(st.session_state.file_position)
    st.session_state.file_position = new_position

    for log in new_logs:
        log['anomaly'] = detect(log)
        insert_log(log)
        st.session_state.last_log = log

    time.sleep(1)
    st.rerun()