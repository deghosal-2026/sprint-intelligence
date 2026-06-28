import { useState, useEffect } from "react";

const API = "/api";

export default function Dashboard() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetch(`${API}/health`)
      .then((r) => r.json())
      .then(setHealth)
      .catch(() => setHealth({ status: "error" }));
  }, []);

  return (
    <div>
      <div className="mb-4 flex items-center gap-4">
        <select className="border rounded px-3 py-1 text-sm">
          <option>SDM</option>
        </select>
        <select className="border rounded px-3 py-1 text-sm">
          <option>Most recent sprint</option>
        </select>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm text-gray-500">Velocity</h3>
          <p className="text-2xl font-bold">--</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm text-gray-500">PR Cycle Time</h3>
          <p className="text-2xl font-bold">--</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm text-gray-500">Bug Rate</h3>
          <p className="text-2xl font-bold">--</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm text-gray-500">Capacity</h3>
          <p className="text-2xl font-bold">--</p>
        </div>
      </div>
      {health && (
        <div className="mt-4 text-xs text-gray-400">
          API: {health.status}
        </div>
      )}
    </div>
  );
}
