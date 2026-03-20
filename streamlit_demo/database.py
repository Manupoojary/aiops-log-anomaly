import sqlite3
import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "logs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            level TEXT,
            service TEXT,
            message TEXT,
            user_id INTEGER,
            anomaly INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_log(log):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        INSERT INTO logs (timestamp, level, service, message, user_id, anomaly)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (log['timestamp'], log['level'], log['service'],
          log['message'], log['user_id'], log['anomaly']))
    conn.commit()
    conn.close()

def get_logs(limit=200):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        f"SELECT * FROM logs ORDER BY id DESC LIMIT {limit}", conn)
    conn.close()
    return df

def get_anomaly_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT COUNT(*) FROM logs WHERE anomaly=1")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_total_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT COUNT(*) FROM logs")
    count = cursor.fetchone()[0]
    conn.close()
    return count