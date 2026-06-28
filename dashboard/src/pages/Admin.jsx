import { useState, useEffect } from "react";

const API = "/api";

export default function Admin() {
  const [system, setSystem] = useState(null);
  const [pollerStatus, setPollerStatus] = useState("idle");
  const [log, setLog] = useState([]);

  const fetchSystem = () => {
    fetch(`${API}/admin/system`)
      .then((r) => r.json())
      .then(setSystem);
  };

  useEffect(() => {
    fetchSystem();
    const interval = setInterval(fetchSystem, 30000);
    return () => clearInterval(interval);
  }, []);

  const runPoll = async (mode) => {
    setPollerStatus("running");
    addLog(`Starting ${mode}...`);
    try {
      const r = await fetch(`${API}/poller/${mode}`, { method: "POST" });
      const data = await r.json();
      addLog(`${mode} completed: ${JSON.stringify(data)}`);
    } catch (e) {
      addLog(`${mode} failed: ${e.message}`);
    }
    setPollerStatus("idle");
    fetchSystem();
  };

  const addLog = (msg) => {
    const ts = new Date().toLocaleTimeString();
    setLog((prev) => [`${ts} - ${msg}`, ...prev].slice(0, 50));
  };

  const statusDot = (ok) =>
    ok === "connected" ? (
      <span className="text-green-500">●</span>
    ) : (
      <span className="text-red-500">●</span>
    );

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Admin</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="font-semibold mb-3">Poller Controls</h2>
          <div className="flex flex-wrap gap-2 mb-3">
            <button
              onClick={() => runPoll("fetch")}
              disabled={pollerStatus === "running"}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white px-4 py-1.5 rounded text-sm"
            >
              Fetch Data
            </button>
            <button
              onClick={() => runPoll("compute")}
              disabled={pollerStatus === "running"}
              className="bg-green-500 hover:bg-green-600 disabled:bg-gray-300 text-white px-4 py-1.5 rounded text-sm"
            >
              Compute Metrics
            </button>
            <button
              onClick={() => runPoll("full")}
              disabled={pollerStatus === "running"}
              className="bg-purple-500 hover:bg-purple-600 disabled:bg-gray-300 text-white px-4 py-1.5 rounded text-sm"
            >
              Run Full Poll
            </button>
          </div>
          <p className="text-xs text-gray-400">
            Status: {statusDot(pollerStatus === "idle" ? "connected" : "disconnected")}{" "}
            {pollerStatus}
          </p>
          {system?.poller?.last_fetch && (
            <p className="text-xs text-gray-400 mt-1">
              Last fetch: {system.poller.last_fetch}
            </p>
          )}
          {system?.poller?.last_compute && (
            <p className="text-xs text-gray-400">
              Last compute: {system.poller.last_compute}
            </p>
          )}

          {log.length > 0 && (
            <div className="mt-3">
              <h3 className="text-xs font-semibold text-gray-500 mb-1">Log</h3>
              <div className="bg-gray-50 rounded p-2 max-h-32 overflow-y-auto text-xs font-mono">
                {log.map((entry, i) => (
                  <div key={i} className="text-gray-600">{entry}</div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="font-semibold mb-3">System Status</h2>
          <div className="space-y-2 text-sm">
            <p>
              DB: {statusDot(system?.db)} {system?.db ?? "Checking..."}
            </p>
            <p>
              Ollama: {statusDot(system?.ollama)} {system?.ollama ?? "Checking..."}
            </p>
            <p>
              GitHub API:{" "}
              {system?.github_remaining != null
                ? `${system.github_remaining} remaining`
                : "Checking..."}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
