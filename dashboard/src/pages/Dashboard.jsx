import { useState, useEffect, useMemo } from "react";
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

function DORAGauge({ label, value, unit, score, color }) {
  const pct = Math.min(Math.max((score ?? 0) * 100, 0), 100);
  return (
    <div className="flex flex-col items-center">
      <div className="relative w-16 h-16 mb-1">
        <svg className="w-16 h-16 -rotate-90" viewBox="0 0 64 64">
          <circle cx="32" cy="32" r="28" fill="none" stroke="#e5e7eb" strokeWidth="6" />
          <circle cx="32" cy="32" r="28" fill="none" stroke={color || "#3b82f6"} strokeWidth="6"
            strokeDasharray={`${(pct / 100) * 176} 176`} strokeLinecap="round" />
        </svg>
        <span className="absolute inset-0 flex items-center justify-center text-sm font-bold">
          {value ?? "--"}
        </span>
      </div>
      <span className="text-xs text-gray-500 text-center">{label}</span>
      {unit && <span className="text-[10px] text-gray-400">{unit}</span>}
    </div>
  );
}

function SummaryCard({ summary, onToggleReview }) {
  const [copied, setCopied] = useState(false);

  if (!summary) {
    return (
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <h3 className="text-sm font-semibold text-gray-700 mb-2">AI Summary</h3>
        <p className="text-sm text-gray-400">Run poller to generate.</p>
      </div>
    );
  }

  const bullets = summary.summary ? summary.summary.split("\n").filter(Boolean) : [];

  const handleCopy = () => {
    navigator.clipboard.writeText(summary.summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 mb-6">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-semibold text-gray-700">AI Summary</h3>
        <div className="flex items-center gap-2">
          <label className="flex items-center gap-1 text-xs text-gray-400">
            <input type="checkbox" checked={summary.reviewed} onChange={onToggleReview} />
            Reviewed
          </label>
          <button onClick={handleCopy}
            className="text-xs px-2 py-1 rounded bg-gray-100 hover:bg-gray-200 text-gray-600">
            {copied ? "Copied!" : "Copy"}
          </button>
        </div>
      </div>
      <ul className="space-y-1">
        {bullets.map((b, i) => (
          <li key={i} className="text-sm text-gray-700 flex gap-2">
            <span className="text-blue-500 shrink-0">→</span>
            <span>{b}</span>
          </li>
        ))}
        {bullets.length === 0 && (
          <li className="text-sm text-gray-400">{summary.summary}</li>
        )}
      </ul>
      <p className="text-[10px] text-gray-400 mt-2">
        Generated with {summary.model_used} &middot; {summary.generated_at ? new Date(summary.generated_at).toLocaleString() : ""}
      </p>
    </div>
  );
}

export default function Dashboard() {
  const [sprints, setSprints] = useState([]);
  const [selectedSprint, setSelectedSprint] = useState(null);
  const [persona, setPersona] = useState(() => sessionStorage.getItem("sprintsense_persona") || "sdm");
  const [metrics, setMetrics] = useState(null);
  const [trends, setTrends] = useState([]);
  const [engineers, setEngineers] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [summary, setSummary] = useState(null);

  const handlePersonaChange = (e) => {
    const p = e.target.value;
    setPersona(p);
    sessionStorage.setItem("sprintsense_persona", p);
  };

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
    fetch(`${API}/metrics/${selectedSprint}/summary`)
      .then((r) => r.json())
      .then(setSummary);
  }, [selectedSprint]);

  const fmtHours = (h) => {
    if (!h && h !== 0) return "--";
    if (h < 24) return `${h.toFixed(1)}h`;
    return `${(h / 24).toFixed(1)}d`;
  };

  const doraScore = (val, type) => {
    if (val == null) return null;
    if (type === "deploy_freq") return Math.min(val / 10, 1);
    if (type === "lead_time") return Math.max(1 - val / 168, 0);
    if (type === "mttr") return Math.max(1 - val / 24, 0);
    if (type === "cfr") return 1 - val;
    return null;
  };

  const doraColor = (score) => {
    if (score == null) return "#d1d5db";
    if (score >= 0.8) return "#22c55e";
    if (score >= 0.5) return "#eab308";
    return "#ef4444";
  };

  const currentEngineer = useMemo(() => engineers.length > 0 ? engineers[0] : null, [engineers]);

  const renderJuniorView = () => (
    <>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <MetricCard title="My Cycle Time"
          value={fmtHours(currentEngineer?.cycle_time_mean_hours)}
          subtitle="Avg time from commit to merge" />
        <MetricCard title="My Points"
          value={currentEngineer?.completed_points ?? 0}
          subtitle={`${currentEngineer?.story_count ?? 0} stories`} />
        <MetricCard title="My WIP"
          value={currentEngineer?.max_concurrent_issues ?? 0}
          subtitle={currentEngineer?.max_concurrent_issues > 4 ? "High — flag your lead" : "On track"}
          color={currentEngineer?.max_concurrent_issues > 4 ? "text-red-500" : "text-green-600"} />
      </div>
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <h3 className="text-sm font-semibold text-gray-700 mb-2">Coach Tip</h3>
        <p className="text-sm text-gray-600">
          {currentEngineer?.cycle_time_mean_hours && currentEngineer.cycle_time_mean_hours > 40
            ? "Your cycle time is above average. Try breaking stories into smaller chunks and requesting early review."
            : "You're on a good track! Keep committing regularly and updating your tasks."}
        </p>
      </div>
    </>
  );

  const renderSeniorView = () => (
    <>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <MetricCard title="My Velocity"
          value={currentEngineer?.completed_points ?? 0}
          subtitle="This sprint" />
        <MetricCard title="My Cycle Time"
          value={fmtHours(currentEngineer?.cycle_time_mean_hours)}
          subtitle="Personal avg" />
        <MetricCard title="Reviews Done"
          value={currentEngineer?.prs_reviewed ?? 0}
          subtitle="PRs reviewed" />
        <MetricCard title="Team Velocity"
          value={metrics ? `${metrics.completed_points ?? 0} / ${metrics.planned_points ?? 0}` : "--"}
          subtitle={`Ratio: ${metrics?.velocity_ratio != null ? (metrics.velocity_ratio * 100).toFixed(0) + "%" : "--"}`} />
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
    </>
  );

  const renderStaffView = () => (
    <>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <MetricCard title="My Velocity"
          value={currentEngineer?.completed_points ?? 0}
          subtitle="This sprint" />
        <MetricCard title="My Cycle Time"
          value={fmtHours(currentEngineer?.cycle_time_mean_hours)}
          subtitle="Personal avg" />
        <MetricCard title="Blocked Issues"
          value={currentEngineer?.blocked_count ?? 0}
          color={currentEngineer?.blocked_count > 0 ? "text-red-500" : "text-green-600"} />
      </div>
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <h3 className="text-sm font-semibold text-gray-700 mb-2">Unblocking Requests</h3>
        {currentEngineer?.blocked_count > 0 ? (
          <p className="text-sm text-gray-600">You have {currentEngineer.blocked_count} blocked item(s). Review with your EM to unblock.</p>
        ) : (
          <p className="text-sm text-gray-400">No blockers. Your team is flowing well.</p>
        )}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Team Velocity</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="sprint" tick={{ fontSize: 10 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="completed_points" fill="#3b82f6" name="Completed" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Cycle Time Trend</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="sprint" tick={{ fontSize: 10 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line dataKey="cycle_time_mean_hours" stroke="#3b82f6" name="Team Mean" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </>
  );

  return (
    <div>
      <div className="mb-4 flex items-center gap-4">
        <select className="border rounded px-3 py-1.5 text-sm bg-white shadow-sm"
          value={persona} onChange={handlePersonaChange}>
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
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>
      </div>

      {persona === "junior" && renderJuniorView()}
      {persona === "senior" && renderSeniorView()}
      {persona === "staff" && renderStaffView()}
      {persona !== "junior" && persona !== "senior" && persona !== "staff" && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <MetricCard title="Velocity"
              value={metrics ? `${metrics.completed_points ?? 0} / ${metrics.planned_points ?? 0}` : "--"}
              subtitle={`Ratio: ${metrics?.velocity_ratio != null ? (metrics.velocity_ratio * 100).toFixed(0) + "%" : "--"}`}
              color={metrics?.velocity_ratio >= 0.8 ? "text-green-600" : "text-yellow-600"} />
            <MetricCard title="PR Cycle Time"
              value={fmtHours(metrics?.cycle_time_mean_hours)}
              subtitle={`P90: ${fmtHours(metrics?.cycle_time_p90_hours)}`} />
            <MetricCard title="Bug Rate"
              value={metrics?.bugs_introduced != null ? `${metrics.bugs_introduced} / ${metrics.bugs_closed}` : "--"}
              subtitle={`Rate: ${metrics?.bug_regression_rate != null ? (metrics.bug_regression_rate * 100).toFixed(1) + "%" : "--"}`} />
            <MetricCard title="Capacity"
              value={metrics?.capacity_ratio != null ? `${(metrics.capacity_ratio * 100).toFixed(0)}%` : "--"}
              subtitle={`${metrics?.actual_capacity ?? 0} / ${metrics?.planned_capacity ?? 0} pts`} />
          </div>

          <SummaryCard summary={summary} onToggleReview={() => {}} />

          {metrics && (
            <div className="bg-white rounded-lg shadow p-4 mb-6">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">DORA Pulse</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <DORAGauge label="Deploy Freq" value={metrics.deploy_frequency?.toFixed(1)} unit="/wk"
                  score={doraScore(metrics.deploy_frequency, "deploy_freq")}
                  color={doraColor(doraScore(metrics.deploy_frequency, "deploy_freq"))} />
                <DORAGauge label="Lead Time" value={metrics.lead_time_hours?.toFixed(0)} unit="hrs"
                  score={doraScore(metrics.lead_time_hours, "lead_time")}
                  color={doraColor(doraScore(metrics.lead_time_hours, "lead_time"))} />
                <DORAGauge label="MTTR" value={metrics.mttr_hours?.toFixed(1)} unit="hrs"
                  score={doraScore(metrics.mttr_hours, "mttr")}
                  color={doraColor(doraScore(metrics.mttr_hours, "mttr"))} />
                <DORAGauge label="Change Fail" value={metrics.change_failure_rate != null ? `${(metrics.change_failure_rate * 100).toFixed(0)}%` : "--"}
                  score={doraScore(metrics.change_failure_rate, "cfr")}
                  color={doraColor(doraScore(metrics.change_failure_rate, "cfr"))} />
              </div>
            </div>
          )}

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
                      {a.severity === "critical" ? "\u{1F534}" : a.severity === "warning" ? "\u26A0\uFE0F" : "\u2139\uFE0F"}
                    </span>
                    <div>
                      <p className="font-medium">{a.title}</p>
                      {a.description && <p className="text-xs text-gray-400">{a.description}</p>}
                      {a.engineer_login && (
                        <p className="text-xs text-orange-500 mt-0.5">Engineer: {a.engineer_login}</p>
                      )}
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
        </>
      )}
    </div>
  );
}
