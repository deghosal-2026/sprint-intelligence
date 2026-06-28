# SprintSense User Guide

## Getting Started

### 1. Start the System
```bash
docker compose up -d --build
```
All three services start: PostgreSQL (db), Flask API (api), React dashboard (dashboard).

### 2. Access the Dashboard
Open http://localhost:3000 in your browser.

### 3. Access the Admin Panel
Open http://localhost:3000/admin for system health, poller controls, and AI summary management.

---

## Persona Views

Switch personas using the dropdown at the top of the dashboard. Your selection is saved in sessionStorage and persists across page refreshes.

### SDM (Sprint Delivery Manager)
**Who it's for:** Managers responsible for a single team's sprint delivery.

**What you see:**
- Velocity (completed/planned points + ratio)
- PR Cycle Time (mean, P90)
- Bug Rate (introduced/closed + regression rate)
- Capacity (actual/planned + ratio)
- DORA Pulse (4 gauges: deploy freq, lead time, MTTR, change failure rate)
- Velocity Trend chart (6 sprints)
- PR Cycle Time Trend chart
- Risk Alerts (stale PRs, overloaded engineers, scope creep)
- Engineer table (velocity, stories, PRs, cycle time, WIP, blocked)
- AI Summary (5 consequence-first bullets)

### Senior SDM
**Who it's for:** Managers overseeing multiple teams.

**What you see:**
- Per-team tab bar (click to switch teams)
- Cross-Team Patterns banner (velocity declines, cycle time increases)
- Trend Forecast card (next-sprint projection per metric)
- Full SDM dashboard for the selected team

**What you don't see:** No team ranking table — tabs only, to avoid unhealthy competition.

### Director
**Who it's for:** Engineering Directors overseeing the entire org.

**What you see:**
- Org-level DORA Pulse (aggregated across all teams)
- Org Velocity (quarterly average)
- Org Trend Forecasts (next-sprint projections for all teams)
- Team Quarterly Comparison table (velocity, cycle time, PRs, bugs, deploy freq, change fail, QoQ delta)
- Strategic AI Summary (4 bullets + one recommendation)

**What you don't see:** No per-engineer data. No per-team drill-down. Director sees org trends only.

### Junior Engineer
**Who it's for:** Individual contributors early in their career.

**What you see:**
- My Cycle Time (personal average)
- My Points (completed this sprint)
- My WIP (current work-in-progress)
- Coach Tip (automated guidance based on cycle time)

**What you don't see:** No team-level data, no other engineers' data. Designed for self-improvement without comparison anxiety.

### Senior Engineer
**Who it's for:** Experienced ICs who contribute individually and review others' work.

**What you see:**
- My Velocity, My Cycle Time, Reviews Done
- Team Velocity (aggregate)
- Velocity Trend chart
- PR Cycle Time Trend chart

### Staff Engineer
**Who it's for:** Senior ICs who unblock teams and drive cross-team initiatives.

**What you see:**
- My Velocity, My Cycle Time, Blocked Issues
- Unblocking Requests (blocked items needing attention)
- Team Velocity chart
- Cycle Time Trend chart

---

## Admin Panel

### System Status
- **DB**: Connected/disconnected
- **LLM**: omlx connection status
- **GitHub**: Remaining API rate limit
- **Poller**: Current status (idle/running) + last fetch/compute timestamps

### Poller Controls
- **Fetch**: Downloads raw data from GitHub API (Phase 1)
- **Compute**: Computes all metrics, DORA, alerts, forecasts, AI summaries (Phase 2)
- **Full**: Runs both phases sequentially

*Note: Fetch and Compute may take several minutes for 10+ teams. If they timeout, run directly via `docker compose exec api python3 -c "..."`.*

### AI Summary Management
- View all generated summaries (sprint, persona, model, timestamp, reviewed status)
- **Regenerate**: Regenerates all AI summaries (SDM + SrSDM + Director)
- **Reviewed toggle**: Mark summaries as reviewed

---

## Data Pipeline

### Phase 1: Fetch
Downloads from GitHub REST API:
- Issues (with labels, assignees, milestones)
- Pull Requests (with cycle time, reviewers)
- Deploy Events (GitHub Actions workflow runs)
- Milestones

### Phase 2: Compute
Computes and stores:
- Sprint metrics (velocity, cycle time, bugs, capacity, DORA)
- Engineer metrics (personal velocity, WIP, blocked, reviews)
- DORA metrics (deploy freq, lead time, MTTR, change failure rate) — scoped per team
- Risk alerts (stale PRs, overloaded engineers, scope creep)
- Trend forecasts (linear regression on 12-sprint history)
- AI summaries (per-persona, via Llama-3.2-3B-Instruct-4bit on omlx)

---

## Metrics Reference

| Metric | Description | Source |
|--------|-------------|--------|
| Velocity Ratio | Completed / planned points | Issues |
| Cycle Time (mean) | Avg hours from first commit to merge | PRs |
| Cycle Time (P90) | 90th percentile cycle time | PRs |
| Bug Regression Rate | Bugs introduced / completed points | Issues |
| Capacity Ratio | Actual / planned capacity | Issues |
| Deploy Frequency | Deploys per week | GitHub Actions |
| Lead Time | Hours from commit to deploy | PRs + Deploys |
| MTTR | Mean time to resolve incidents | Incidents |
| Change Failure Rate | Failed deploys / total deploys | Incidents + Deploys |
| WIP | Concurrent open issues per engineer | Issues |
| Blocked Count | Issues with "blocked" label | Issues |

---

## LLM Setup

SprintSense uses omlx (local LLM server) for AI summaries:

```bash
# Start omlx on host machine
omlx serve --port 8000 --api-key omlx-test

# Model: Llama-3.2-3B-Instruct-4bit
```

The Docker API container connects to `http://host.docker.internal:8000`.

---

## Troubleshooting

### Dashboard shows no data
1. Check API health: `curl http://localhost:5001/api/health`
2. Check DB has data: `docker compose exec db psql -U sprintsense -c "SELECT count(*) FROM sprints"`
3. If empty, run seed: `python3 tools/seed_database.py`

### AI summaries not generating
1. Check omlx is running: `curl http://localhost:8000/v1/models`
2. Check from container: `docker compose exec api python3 -c "from api.poller import ollama_client; print(ollama_client.is_available())"`
3. Generate directly: `docker compose exec api python3 -c "from api.app import create_app; from api.poller.compute import generate_all_summaries; app=create_app(); app.app_context().push(); generate_all_summaries()"`

### Port 5000 already in use
macOS uses port 5000 for AirPlay Receiver. The API maps to port 5001 instead.

### Poller fetch/compute hangs
Known issue — bulk operations block gunicorn workers. Run directly via `docker compose exec api python3 -c "..."` instead.
