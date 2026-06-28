# SprintSense API Documentation

Base URL: `http://localhost:5001/api`

## Health

### `GET /api/health`
Returns DB connection status.

**Response:**
```json
{ "status": "ok", "db": "connected" }
```

---

## Sprints

### `GET /api/sprints`
List all sprints ordered by start date (newest first).

**Response:**
```json
[
  { "id": 12, "name": "team1-2026.24.25", "start_date": "2026-06-15", "end_date": "2026-06-28" }
]
```

---

## Teams

### `GET /api/teams`
List all teams with their latest sprint.

**Response:**
```json
[
  { "team": "team1", "owner": "microsoft", "repo": "vscode", "latest_sprint_id": 12, "latest_sprint_name": "team1-2026.24.25" }
]
```

---

## Sprint Metrics

### `GET /api/metrics/{sprint_id}`
Returns all computed metrics for a sprint.

**Response:**
```json
{
  "sprint_id": 12,
  "planned_points": 1987.0,
  "completed_points": 1029.0,
  "velocity_ratio": 0.5179,
  "carry_over_points": 958.0,
  "cycle_time_mean_hours": 24.5,
  "cycle_time_median_hours": 18.0,
  "cycle_time_p90_hours": 65.0,
  "total_prs_merged": 48,
  "bugs_introduced": 139,
  "bugs_closed": 120,
  "bug_regression_rate": 0.1351,
  "planned_capacity": 1987.0,
  "actual_capacity": 1029.0,
  "capacity_ratio": 0.5179,
  "deploy_frequency": 2.15,
  "lead_time_hours": 48.0,
  "mttr_hours": 4.2,
  "change_failure_rate": 0.5
}
```

### `GET /api/metrics/{sprint_id}/engineers`
Per-engineer metrics for a sprint.

**Response:**
```json
[
  {
    "engineer": "octocat",
    "completed_points": 34.0,
    "story_count": 8,
    "prs_merged": 5,
    "cycle_time_mean_hours": 18.5,
    "prs_reviewed": 3,
    "max_concurrent_issues": 4,
    "avg_wip": 4.0,
    "avg_review_turnaround_hours": null,
    "blocked_count": 0
  }
]
```

### `GET /api/metrics/{sprint_id}/trend`
Last 6 sprints of trend data for the same team.

**Response:**
```json
[
  {
    "sprint": "team1-2026.24.25",
    "start_date": "2026-06-15",
    "planned_points": 1987.0,
    "completed_points": 1029.0,
    "velocity_ratio": 0.5179,
    "cycle_time_mean_hours": 24.5,
    "bugs_introduced": 139,
    "bugs_closed": 120
  }
]
```

### `GET /api/metrics/{sprint_id}/summary?persona={persona}`
AI summary for a sprint. Persona: `sdm`, `srsdm`, `director`.

**Response:**
```json
{
  "summary": "• Velocity: 52% → Significantly delayed...\n• Bugs: 139 → ...",
  "model_used": "Llama-3.2-3B-Instruct-4bit",
  "generated_at": "2026-06-28T00:50:00",
  "reviewed": false
}
```

---

## Quarterly

### `GET /api/quarterly`
Per-team quarterly aggregates (12 sprints) with QoQ deltas.

**Response:**
```json
[
  {
    "team": "team1",
    "quarter_sprints": 12,
    "sprint_ids": [1, 2, 3, ...],
    "quarter_start": "2026-01-12",
    "quarter_end": "2026-06-28",
    "averages": {
      "velocity_ratio": 0.52,
      "cycle_time_mean_hours": 24.5,
      "total_prs_merged": 48.0,
      "bugs_introduced": 38,
      "capacity_ratio": 0.52,
      "deploy_frequency": 2.15,
      "lead_time_hours": 48.0,
      "change_failure_rate": 0.43
    },
    "qoq_delta": {
      "velocity_ratio": -5.2,
      "cycle_time_mean_hours": 12.3
    }
  }
]
```

### `GET /api/quarterly/org`
Org-level aggregate across all teams (12 sprints).

**Response:**
```json
{
  "quarter_sprints": 12,
  "quarter_start": "2026-01-12",
  "quarter_end": "2026-06-28",
  "averages": {
    "velocity_ratio": 0.23,
    "cycle_time_mean_hours": 16.4,
    "total_prs_merged": 48,
    "bugs_introduced": 38,
    "capacity_ratio": 0.23,
    "deploy_frequency": 3.7,
    "lead_time_hours": 2508.8,
    "change_failure_rate": 0.43
  }
}
```

---

## Patterns

### `GET /api/patterns`
Cross-team pattern detection — velocity declines and cycle time increases.

**Response:**
```json
{
  "slowdowns": [
    {
      "team": "team1",
      "decline_pct": 49.9,
      "early_avg": 0.66,
      "recent_avg": 0.331,
      "type": "velocity_decline"
    }
  ],
  "correlations": [
    {
      "team_a": "team1",
      "team_b": "team2",
      "type": "velocity_correlation",
      "avg_diff_pct": 8.2
    }
  ]
}
```

---

## Forecasts

### `GET /api/forecasts?team={team}`
Linear regression forecasts for next sprint. Optional team filter.

**Response:**
```json
[
  {
    "team": "team1",
    "metric": "velocity_ratio",
    "current_value": 0.5179,
    "forecast_value": 0.3183,
    "trend_direction": "decreasing",
    "slope": -0.031,
    "computed_at": "2026-06-28T01:10:00"
  }
]
```

Metrics forecasted: `velocity_ratio`, `cycle_time_mean_hours`, `bug_regression_rate`, `deploy_frequency`, `change_failure_rate`.

---

## Alerts

### `GET /api/alerts?sprint_id={sprint_id}`
Risk alerts, optionally filtered by sprint.

**Response:**
```json
[
  {
    "id": 1,
    "type": "stale_pr",
    "severity": "warning",
    "title": "Stale PR: Fix login bug",
    "description": "No activity in 3+ days",
    "engineer_login": "octocat",
    "created_at": "2026-06-28T00:00:00"
  }
]
```

Alert types: `stale_pr`, `overloaded_engineer`, `scope_creep`.

---

## Poller

### `POST /api/poller/fetch`
Phase 1: Fetch raw data from GitHub API for all configured repos.

**Response:**
```json
{ "status": "completed", "repos": 11, "issues": 3200, "prs": 800, "details": {...} }
```

### `POST /api/poller/compute`
Phase 2: Compute all metrics, DORA, alerts, forecasts, AI summaries.

**Response:**
```json
{ "status": "completed", "sprints": 120, "sprint_metrics": 120, "engineer_metrics": 920, "dora_metrics": 120, "alerts": 1362, "forecasts": 35, "ai_summaries": {...} }
```

### `POST /api/poller/full`
Run both Phase 1 and Phase 2 sequentially.

### `GET /api/poller/status`
Current poller status.

**Response:**
```json
{ "status": "idle", "last_fetch": null, "last_compute": null }
```

---

## Admin

### `GET /api/admin/system`
System health: DB, LLM, GitHub rate limit, poller status.

**Response:**
```json
{
  "db": "connected",
  "ollama": "connected",
  "github_remaining": 5000,
  "poller": { "status": "idle", "last_fetch": null, "last_compute": null }
}
```

### `GET /api/admin/summaries`
List recent AI summaries.

**Response:**
```json
[
  { "id": 1, "sprint_id": 12, "persona_level": "sdm", "model_used": "Llama-3.2-3B-Instruct-4bit", "generated_at": "...", "reviewed": false }
]
```

### `POST /api/admin/summaries/regenerate`
Regenerate all AI summaries (SDM + SrSDM + Director). Runs synchronously — may take several minutes.

**Response:**
```json
{ "status": "ok", "sdm": {"generated": 120, "skipped": 0, "errors": 0}, "srsdm": {...}, "director": {...} }
```

---

## Ask (Sprint Q&A)

### `POST /api/ask`
Ask a question about sprint data. *(Stub — not fully implemented)*

**Request:**
```json
{ "question": "What's our velocity trend?", "sprint_id": 12 }
```
