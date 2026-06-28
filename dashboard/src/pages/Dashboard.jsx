import { useState, useEffect } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  LineChart, Line, ResponsiveContainer,
} from "recharts";

const API = "/api";

function MetricCard({ title, value, subtitle, color }) {
  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h3 className="text-sm text-gray-500 font-medium">{title}</h3>
      <p className={`text-2xl font-bold ${color || "text-gray-900"}`}>
        {value ?? "--"}
      </p>
      {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
    </div>
  );
}

export default function Dashboard() {
  const [sprints, setSprints] = useState([]);
  const [selectedSprint, setSelectedSprint] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [trends, setTrends] = useState([]);
  const [engineers, setEngineers] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch(`${API}/sprints`)
      .then((r) => r.json())
      .then((list) => {
        setSprints(list);
        if (list.length > 0) setSelectedSprint(list[0].id);
      });
  }, []);

  useEffect(() => {
    if (!selectedSprint) return;
    fetch(`${API}/metrics/${selectedSprint}`)
      .then((r) => r.json())
      .then(setMetrics);
    fetch(`${API}/metrics/${selectedSprint}/trend`)
      .then((r) => r.json())
      .then(setTrends);
    fetch(`${API}/metrics/${selectedSprint}/engineers`)
      .then((r) => r.json())
      .then(setEngineers);
    fetch(`${API}/alerts?sprint_id=${selectedSprint}`)
      .then((r) => r.json())
      .then(setAlerts);
  }, [selectedSprint]);

  const fmtHours = (h) => {
    if (!h && h !== 0) return "--";
    if (h < 24) return `${h.toFixed(1)}h`;
    return `${(h / 24).toFixed(1)}d`;
  };

  return (
    <div>
      <div className="mb-4 flex items-center gap-4">
        <select
          className="border rounded px-3 py-1.5 text-sm bg-white shadow-sm"
          value="sdm"
        >
          <option value="sdm">SDM</option>
          <option value="junior">Junior Engineer</option>
          <option value="senior">Senior Engineer</option>
          <option value="staff">Staff Engineer</option>
        </select>
        <select
          className="border rounded px-3 py-1.5 text-sm bg-white shadow-sm"
          value={selectedSprint ?? ""}
          onChange={(e) => setSelectedSprint(Number(e.target.value))}
        >
          {sprints.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <MetricCard
          title="Velocity"
          value={metrics ? `${metrics.completed_points ?? 0} / ${metrics.planned_points ?? 0}` : "--"}
          subtitle={`Ratio: ${metrics?.velocity_ratio != null ? (metrics.velocity_ratio * 100).toFixed(0) + "%" : "--"}`}
          color={metrics?.velocity_ratio >= 0.8 ? "text-green-600" : "text-yellow-600"}
        />
        <MetricCard
          title="PR Cycle Time"
          value={fmtHours(metrics?.cycle_time_mean_hours)}
          subtitle={`P90: ${fmtHours(metrics?.cycle_time_p90_hours)}`}
        />
        <MetricCard
          title="Bug Rate"
          value={metrics?.bugs_introduced != null ? `${metrics.bugs_introduced} / ${metrics.bugs_closed}` : "--"}
          subtitle={`Rate: ${metrics?.bug_regression_rate != null ? (metrics.bug_regression_rate * 100).toFixed(1) + "%" : "--"}`}
        />
        <MetricCard
          title="Capacity"
          value={metrics?.capacity_ratio != null ? `${(metrics.capacity_ratio * 100).toFixed(0)}%` : "--"}
          subtitle={`${metrics?.actual_capacity ?? 0} / ${metrics?.planned_capacity ?? 0} pts`}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Velocity Trend</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="sprint" tick={{ fontSize: 10 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="planned_points" fill="#94a3b8" name="Planned" />
              <Bar dataKey="completed_points" fill="#3b82f6" name="Completed" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">PR Cycle Time Trend</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="sprint" tick={{ fontSize: 10 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line dataKey="cycle_time_mean_hours" stroke="#3b82f6" name="Mean" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {alerts.length > 0 && (
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Risk Alerts</h3>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {alerts.map((a) => (
              <div key={a.id} className="flex items-start gap-2 text-sm">
                <span className={
                  a.severity === "critical" ? "text-red-500" :
                  a.severity === "warning" ? "text-yellow-500" : "text-blue-500"
                }>
                  {a.severity === "critical" ? "🔴" : a.severity === "warning" ? "⚠️" : "ℹ️"}
                </span>
                <div>
                  <p className="font-medium">{a.title}</p>
                  {a.description && <p className="text-xs text-gray-400">{a.description}</p>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-2">Engineers</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-gray-500">
                <th className="pb-2 pr-4">Engineer</th>
                <th className="pb-2 pr-4">Velocity</th>
                <th className="pb-2 pr-4">Stories</th>
                <th className="pb-2 pr-4">PRs Merged</th>
                <th className="pb-2 pr-4">Cycle Time</th>
                <th className="pb-2 pr-4">WIP</th>
                <th className="pb-2 pr-4">Blocked</th>
              </tr>
            </thead>
            <tbody>
              {engineers.map((e) => (
                <tr key={e.engineer} className="border-b last:border-0">
                  <td className="py-2 pr-4 font-medium">{e.engineer}</td>
                  <td className="py-2 pr-4">{e.completed_points}</td>
                  <td className="py-2 pr-4">{e.story_count}</td>
                  <td className="py-2 pr-4">{e.prs_merged}</td>
                  <td className="py-2 pr-4">{fmtHours(e.cycle_time_mean_hours)}</td>
                  <td className="py-2 pr-4">{e.max_concurrent_issues}</td>
                  <td className="py-2 pr-4">{e.blocked_count}</td>
                </tr>
              ))}
              {engineers.length === 0 && (
                <tr><td colSpan={7} className="py-4 text-center text-gray-400">No data. Run poller first.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
