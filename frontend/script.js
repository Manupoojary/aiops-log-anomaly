const API_BASE = "http://localhost:5000";

async function loadModels() {
    const res = await fetch(`${API_BASE}/models`);
    const models = await res.json();

    const select = document.getElementById("modelSelect");
    select.innerHTML = "";

    models.forEach(model => {
        const opt = document.createElement("option");
        opt.value = model;
        opt.textContent = model;
        select.appendChild(opt);
    });
}

async function startPipeline() {
    const model = document.getElementById("modelSelect").value;

    await fetch(`${API_BASE}/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model })
    });

    updateStatus();
}

async function stopPipeline() {
    await fetch(`${API_BASE}/stop`, { method: "POST" });
    updateStatus();
}

async function updateStatus() {
    const res = await fetch(`${API_BASE}/status`);
    const data = await res.json();

    const statusEl = document.getElementById("status");

    if (data.pipeline_running) {
        statusEl.textContent = "Status: Running";
        statusEl.className = "status running";
    } else {
        statusEl.textContent = "Status: Stopped";
        statusEl.className = "status stopped";
    }
}

async function updateMetrics() {
    const res = await fetch(`${API_BASE}/metrics`);
    const data = await res.json();

    document.getElementById("anomalyCount").textContent =
        data.anomaly_count ?? 0;
}

// ---------- AUTO REFRESH ----------
setInterval(updateStatus, 3000);
setInterval(updateMetrics, 3000);

// ---------- INIT ----------
loadModels();
updateStatus();
updateMetrics();
