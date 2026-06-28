# SprintSense — Technical Spec v1

**Status:** APPROVED
**Derived from:** `docs/prd.md` (APPROVED)
**Date:** June 2026

---

## 1. Overview & Architecture

### 1.1 System Context

SprintSense is a prototype AI sprint intelligence tool with three services, one shared PostgreSQL database, and a React SPA dashboard.

```
┌─────────────────────────────────────────────────────────────┐
│                     External APIs                            │
│  GitHub (Issues, Projects, Milestones, PRs, Actions)        │
│  PagerDuty (Incidents)                                      │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Poller Service       │  Python
│  • Reads config from GitHub  │
│  • Syncs config → DB         │
│  • Reads config from DB      │
│  • Fetches from GH/PD APIs   │
│  • Writes raw data → DB      │
│  • Computes metrics → DB     │
│  • Triggers LLM summaries    │
│  • Runs on-demand (manual)   │
└──────────────┬───────────────┘
               │ writes
               ▼
┌──────────────────────────────┐
│         PostgreSQL           │
│  • config tables             │
│  • raw data (issues, PRs…)   │
│  • computed metrics          │
│  • AI summaries              │
└──────────────┬───────────────┘
               │ reads
               ▼
┌──────────────────────────────┐
│        API Server            │  Python
│  • REST endpoints            │
│  • Reads from DB             │
│  • Serves JSON to dashboard  │
│  • Triggers poller on-demand │
└──────────────┬───────────────┘
               │ JSON
               ▼
┌──────────────────────────────┐
│     React SPA Dashboard      │
│  • Calls API for all data    │
│  • Persona-tuned views       │
│  • AI summary display        │
└──────────────────────────────┘
```

### 1.2 Component Architecture

| Component | Language | Role |
|---|---|---|
| **Poller** | Python | Fetches data from GitHub + PagerDuty APIs. Syncs config from GitHub → DB. Computes metrics. Triggers LLM summaries. |
| **API Server** | Python | REST API. Reads from PostgreSQL. Serves dashboard. Exposes `/trigger-poll` endpoint. |
| **Dashboard** | React (SPA) | Calls API. Renders persona-tuned dashboards, charts, AI summaries, risk alerts. |
| **Database** | PostgreSQL | Single shared database. All inter-service communication through DB reads/writes. |

### 1.3 Data Flow

```
1. Config lives in GitHub: sprintsense-config.yaml
2. User triggers poll: API Server → Poller starts
3. Poller reads sprintsense-config.yaml from GitHub → syncs to DB config tables
4. Poller reads config from DB (repos, labels, milestones, thresholds)
5. Poller calls GitHub API → writes raw data to DB
6. Poller calls PagerDuty API → writes incident data to DB
7. Poller computes metrics from raw data → writes to metrics tables
8. Poller calls LLM → writes AI summaries to DB
9. Dashboard calls API → API reads DB → returns JSON → Dashboard renders
```

### 1.4 Design Principles

- **DB as integration point.** No direct service-to-service calls (except Poller trigger). All data flows through PostgreSQL.
- **Config in GitHub, synced to DB.** `sprintsense-config.yaml` in a GitHub repo is the source of truth. Poller syncs it to DB on each run.
- **On-demand polling.** No cron, no job scheduler. Poller is triggered via API or CLI. Runs once per invocation.
- **Prototype-first.** No scaling concerns. Single instance of each service. Local development with Docker Compose.
- **Stateless services.** Poller and API Server are stateless. All state in PostgreSQL.

---

## 2. Technology Stack

### 2.1 Language & Runtime

- **Language:** Python 3.11+
- **Package manager:** pip + `requirements.txt` (or `pyproject.toml`)
- **Async/sync:** Flask is synchronous. Poller uses `requests` or `urllib` for GitHub API calls. No async needed for prototype.

### 2.2 Backend Framework

- **API Server:** Flask
- **Poller:** Flask CLI command or plain Python script (no web server needed — runs via `flask poll` or `python -m poller`)
- **Shared library:** `common/` package with DB models, config parser, metric computation logic — used by both Poller and API Server.

### 2.3 Frontend / Dashboard

- **Framework:** React (SPA)
- **Bundler:** Vite (or Create React App)
- **Charts:** Recharts or Chart.js via `react-chartjs-2`
- **Routing:** React Router (for persona views)
- **State:** React hooks + `fetch` to API. No Redux needed for prototype.
- **Styling:** Tailwind CSS or plain CSS modules.

### 2.4 Database & Storage

- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (with Flask-SQLAlchemy for API Server)
- **Migrations:** Alembic
- **Config file:** `sprintsense-config.json` — stored in a GitHub repo. Poller clones/fetches it, syncs to `config` tables in DB.
- **No caching layer** in prototype. API reads directly from PostgreSQL.

### 2.5 LLM Provider & Model

- **Provider:** Ollama with MLX backend (Apple Silicon)
- **Model:** `qwen3:9b` (Qwen 3.5 9B, MLX 4-bit quantized)
- **Hosting:** Runs locally on developer machine. No cloud LLM costs.
- **Integration:** Poller calls Ollama REST API (`http://localhost:11434/api/generate`) to generate executive summaries after metrics are computed.
- **Fallback:** None in prototype. If Ollama is offline, summaries are skipped with a logged warning.

### 2.6 External APIs

| API | Purpose | Auth |
|---|---|---|
| GitHub REST API | Issues, Projects, Milestones, PRs, Actions | Personal access token (fine-grained) |
| PagerDuty REST API | Incident events | API token |
| Ollama API | LLM summary generation | None (localhost) |

### 2.7 Hosting & Infrastructure

- **Prototype:** All services run locally on developer macOS machine.
- **Database:** Local PostgreSQL instance (installed via Homebrew or Docker).
- **Containerization:** Docker Compose for PostgreSQL + services (optional — can run directly too).
- **No cloud infrastructure.** No CI/CD pipeline for prototype.
- **No monitoring/alerting** beyond console logs.

---

## 3. Data Model

### 3.1 Sprint Naming Convention

All sprints use the format: **`TEAM-YY.START_WEEK.END_WEEK`**

- `team1-26.02.03` = Team 1, 2026 weeks 2-3 (Jan 5 – Jan 18, 2026)
- `team1-26.24.25` = Team 1, 2026 weeks 24-25 (Jun 8 – Jun 21, 2026)
- `team2-26.24.25` = Team 2, same date range, different team
- `team3-26.48.49` = Team 3, 2026 weeks 48-49 (Nov 23 – Dec 6, 2026)

**Properties:**
- 2-week sprints (ISO week numbering)
- Team-scoped: different teams can have sprints in the same week range
- Supports modeling 4-5 teams with independent sprint cadences
- Sortable as strings: `team1-26.02.03` < `team1-26.24.25`
- Machine-parsable: team name, year, start week, end week
- Crossing year boundaries: e.g., `team1-25.52.01` for 2025 week 52 → 2026 week 1

### 3.2 Core Entities

```
┌──────────┐     ┌───────────────┐     ┌──────────┐
│   Repo   │────→│     Issue     │────→│  Sprint  │
└──────────┘     └───────┬───────┘     └──────────┘
                         │
                    ┌────┴────┐
                    │  Label  │ (points:3, bug, feature, sprint:26.X.Y)
                    └─────────┘

┌──────────┐     ┌───────────────┐
│   Repo   │────→│  PullRequest  │
└──────────┘     └───────┬───────┘
                         │
                    ┌────┴────┐
                    │ Commits │
                    └─────────┘

┌──────────┐     ┌──────────────┐
│   Repo   │────→│ DeployEvent  │ (from GitHub Actions)
└──────────┘     └──────────────┘

                 ┌──────────┐
                 │ Incident │ (from PagerDuty)
                 └──────────┘

┌──────────────┐     ┌───────────────┐
│ SprintMetrics│────→│    Sprint     │
└──────────────┘     └───────────────┘

┌──────────────────────┐     ┌───────────────┐
│ EngineerSprintMetrics│────→│    Sprint     │
└──────────────────────┘     └───────────────┘

┌────────────┐     ┌───────────────┐
│ AISummary  │────→│    Sprint     │
└────────────┘     └───────────────┘

┌───────┐     ┌───────────────┐
│ Alert │────→│    Sprint     │
└───────┘     └───────────────┘
```

### 3.3 Engineer Identity

- **No separate `engineers` table.** GitHub usernames (`issue.assignee.login`, `pr.user.login`) are used directly as engineer identifiers.
- All engineer-specific tables (`engineer_sprint_metrics`, `issues.assignee`) reference the raw GitHub username string.
- Team mapping: if teams are needed, a config mapping `username → team_name` lives in `sprintsense-config.json` and is synced to a config table.

### 3.4 Sprint Detection & Reconciliation

The poller maps three GitHub sprint mechanisms into a unified `sprints` table:

| Mechanism | Detection | Priority |
|---|---|---|
| GitHub Milestones | Milestone with due date. If milestone spans ~2 weeks, treat as a sprint. | 1 (highest) |
| GitHub Project Iterations | ProjectV2 iteration field with start/end dates. | 2 |
| Issue Labels | `sprint:26.X.Y` label on issues. | 3 (fallback) |

**Reconciliation logic:**
1. Poller collects all Milestones, Project iterations, and sprint labels.
2. Maps each to a `26.X.Y` sprint name based on date range.
3. Merges overlapping sprints from different mechanisms (e.g., Milestone "Sprint 12" and `sprint:26.24.25` label both map to `26.24.25`).
4. Issues are assigned to a sprint if they have: a milestone, a project iteration, OR a `sprint:` label.
5. If an issue has multiple sprint signals that conflict, milestone wins.

### 3.5 Database Schema

#### Config Tables

```sql
-- Repos to poll
CREATE TABLE repos (
    id SERIAL PRIMARY KEY,
    owner VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    UNIQUE(owner, name)
);

-- Label conventions per repo
CREATE TABLE label_config (
    id SERIAL PRIMARY KEY,
    repo_id INTEGER REFERENCES repos(id),
    points_prefix VARCHAR(50) DEFAULT 'points:',     -- e.g., "points:" → points:3
    bug_label VARCHAR(100) DEFAULT 'bug',
    feature_label VARCHAR(100) DEFAULT 'feature',
    techdebt_label VARCHAR(100) DEFAULT 'tech-debt',
    task_label VARCHAR(100) DEFAULT 'task',
    sprint_prefix VARCHAR(50) DEFAULT 'sprint:',      -- e.g., "sprint:" → sprint:26.24.25
    UNIQUE(repo_id)
);

-- Global thresholds
CREATE TABLE thresholds (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,   -- e.g., 'stale_pr_days', 'max_wip'
    value VARCHAR(255) NOT NULL         -- e.g., '3', '4'
);
```

#### Raw Data Tables

```sql
-- Raw GitHub issues
CREATE TABLE issues (
    id SERIAL PRIMARY KEY,
    github_id BIGINT NOT NULL,
    repo_id INTEGER REFERENCES repos(id),
    number INTEGER NOT NULL,
    title TEXT,
    state VARCHAR(20),                -- open, closed
    created_at TIMESTAMP,
    closed_at TIMESTAMP,
    updated_at TIMESTAMP,
    assignee_login VARCHAR(255),      -- GitHub username
    story_points DECIMAL,             -- parsed from points:N label
    is_bug BOOLEAN DEFAULT FALSE,
    is_feature BOOLEAN DEFAULT FALSE,
    is_techdebt BOOLEAN DEFAULT FALSE,
    milestone_title VARCHAR(255),     -- raw milestone name
    raw_json JSONB,                   -- full API response for future recomputation
    fetched_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(github_id, repo_id)
);

-- Raw GitHub PRs
CREATE TABLE pull_requests (
    id SERIAL PRIMARY KEY,
    github_id BIGINT NOT NULL,
    repo_id INTEGER REFERENCES repos(id),
    number INTEGER NOT NULL,
    title TEXT,
    state VARCHAR(20),                -- open, closed, merged
    author_login VARCHAR(255),
    created_at TIMESTAMP,
    merged_at TIMESTAMP,
    closed_at TIMESTAMP,
    first_commit_at TIMESTAMP,        -- earliest commit on branch
    cycle_time_hours DECIMAL,         -- first_commit_at → merged_at
    review_count INTEGER DEFAULT 0,
    reviewers TEXT[],                  -- array of reviewer logins
    raw_json JSONB,
    fetched_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(github_id, repo_id)
);

-- Deploy events (from GitHub Actions workflow runs)
CREATE TABLE deploy_events (
    id SERIAL PRIMARY KEY,
    repo_id INTEGER REFERENCES repos(id),
    workflow_run_id BIGINT NOT NULL,
    deployed_at TIMESTAMP NOT NULL,
    status VARCHAR(50),               -- success, failure
    environment VARCHAR(100),         -- production, staging
    UNIQUE(workflow_run_id, repo_id)
);

-- Incident events (from PagerDuty)
CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    pagerduty_id VARCHAR(255) UNIQUE NOT NULL,
    title TEXT,
    status VARCHAR(50),               -- triggered, acknowledged, resolved
    created_at TIMESTAMP,
    resolved_at TIMESTAMP,
    mttr_hours DECIMAL,               -- created_at → resolved_at
    is_change_failure BOOLEAN,         -- linked to a deploy event?
    linked_deploy_id INTEGER REFERENCES deploy_events(id)
);
```

#### Unified Sprint Table

```sql
-- Unified sprint — mapped from Milestones, Project iterations, and labels
CREATE TABLE sprints (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,  -- e.g., '26.24.25'
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    source_type VARCHAR(50),           -- 'milestone', 'project_iteration', 'label'
    source_id VARCHAR(255),            -- raw milestone title or iteration ID
    repo_id INTEGER REFERENCES repos(id)
);

-- Issue-to-sprint mapping (resolved by poller)
CREATE TABLE issue_sprint_map (
    id SERIAL PRIMARY KEY,
    issue_id INTEGER REFERENCES issues(id),
    sprint_id INTEGER REFERENCES sprints(id),
    UNIQUE(issue_id, sprint_id)
);
```

#### Computed Metrics Tables

```sql
-- Per-sprint aggregate metrics (one row per sprint)
CREATE TABLE sprint_metrics (
    id SERIAL PRIMARY KEY,
    sprint_id INTEGER REFERENCES sprints(id) UNIQUE,
    -- Velocity
    planned_points DECIMAL,
    completed_points DECIMAL,
    velocity_ratio DECIMAL,            -- completed / planned
    carry_over_points DECIMAL,         -- points not completed
    -- PR Cycle Time (first commit → merge, all PRs in sprint)
    cycle_time_mean_hours DECIMAL,
    cycle_time_median_hours DECIMAL,
    cycle_time_p90_hours DECIMAL,
    total_prs_merged INTEGER,
    -- Bugs
    bugs_introduced INTEGER,
    bugs_closed INTEGER,
    bug_regression_rate DECIMAL,       -- introduced / total completed
    -- Capacity
    planned_capacity DECIMAL,          -- sum of story points planned
    actual_capacity DECIMAL,           -- sum of story points completed
    capacity_ratio DECIMAL,            -- actual / planned
    -- DORA
    deploy_frequency DECIMAL,          -- deploys per week
    lead_time_hours DECIMAL,           -- commit → deploy (mean)
    mttr_hours DECIMAL,                -- mean time to recovery
    change_failure_rate DECIMAL,       -- failed deploys / total deploys
    -- Meta
    computed_at TIMESTAMP DEFAULT NOW()
);

-- Per-engineer per-sprint metrics (one row per engineer per sprint)
CREATE TABLE engineer_sprint_metrics (
    id SERIAL PRIMARY KEY,
    sprint_id INTEGER REFERENCES sprints(id),
    engineer_login VARCHAR(255) NOT NULL,
    -- Velocity contribution
    completed_points DECIMAL,
    story_count INTEGER,
    -- PR metrics
    prs_merged INTEGER,
    cycle_time_mean_hours DECIMAL,
    -- Reviews
    prs_reviewed INTEGER,
    avg_review_turnaround_hours DECIMAL,
    -- WIP
    max_concurrent_issues INTEGER,     -- peak WIP during sprint
    avg_wip DECIMAL,                   -- average WIP during sprint
    blocked_count INTEGER,             -- issues in blocked/impeded state
    -- Meta
    computed_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(sprint_id, engineer_login)
);
```

#### AI Summaries Table

```sql
CREATE TABLE ai_summaries (
    id SERIAL PRIMARY KEY,
    sprint_id INTEGER REFERENCES sprints(id),
    persona_level VARCHAR(50) NOT NULL, -- 'sdm', 'senior_sdm', 'director', 'junior_eng', 'senior_eng', 'staff_eng'
    summary_text TEXT NOT NULL,         -- the 5-bullet (or persona-appropriate) summary
    model_used VARCHAR(100),            -- e.g., 'qwen3:9b'
    generated_at TIMESTAMP DEFAULT NOW(),
    reviewed BOOLEAN DEFAULT FALSE,     -- human review toggle
    UNIQUE(sprint_id, persona_level)
);
```

#### Risk Alerts Table

```sql
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    sprint_id INTEGER REFERENCES sprints(id),
    alert_type VARCHAR(50) NOT NULL,    -- 'stale_pr', 'overloaded_engineer', 'scope_creep'
    severity VARCHAR(20) DEFAULT 'warning', -- 'info', 'warning', 'critical'
    title TEXT NOT NULL,
    description TEXT,
    engineer_login VARCHAR(255),        -- for overloaded alerts
    pr_id INTEGER REFERENCES pull_requests(id),  -- for stale PR alerts
    issue_count INTEGER,                -- for scope creep (unplanned issues added)
    points_added DECIMAL,               -- for scope creep
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);
```

### 3.6 Index Strategy

```sql
-- Hot paths
CREATE INDEX idx_issues_repo_state ON issues(repo_id, state);
CREATE INDEX idx_issues_assignee ON issues(assignee_login);
CREATE INDEX idx_pull_requests_repo ON pull_requests(repo_id);
CREATE INDEX idx_pull_requests_author ON pull_requests(author_login);
CREATE INDEX idx_issue_sprint_map_sprint ON issue_sprint_map(sprint_id);
CREATE INDEX idx_sprint_metrics_sprint ON sprint_metrics(sprint_id);
CREATE INDEX idx_engineer_sprint_metrics_sprint_eng ON engineer_sprint_metrics(sprint_id, engineer_login);
CREATE INDEX idx_alerts_sprint ON alerts(sprint_id);
CREATE INDEX idx_deploy_events_repo_ts ON deploy_events(repo_id, deployed_at);
CREATE INDEX idx_incidents_ts ON incidents(created_at);
```

### 3.7 Data Freshness

- Poller is on-demand. No automatic refresh. User triggers via API or CLI.
- Each poll run is a full sync: fetches all data since last poll, updates existing records, inserts new ones.
- Metrics are recomputed on every poll run for all affected sprints.
- No data archival or S3 out-of-band storage in prototype scope. `raw_json` column preserves original API response for future reprocessing.

---

## 4. Data Pipeline (GitHub API Integration)

### 4.1 Overview: Two-Phase Poller

The poller is split into two independent phases. This allows expensive data fetching (GitHub API, rate-limited) to happen once, while cheap computation runs repeatedly for testing and iteration.

```
Phase 1: FETCH                    Phase 2: COMPUTE
───────────────                    ─────────────────
Config sync from GitHub            Read raw data from DB
   ↓                               Resolve sprints (milestones → iterations → labels)
Fetch Issues (GitHub API)          Map issues to sprints
   ↓                               Compute sprint metrics
Fetch PRs + commits (GitHub API)   Compute engineer metrics
   ↓                               Compute DORA metrics
Fetch Projects + Milestones        Detect risk alerts
   ↓                               Generate AI summaries (Ollama)
Fetch Deploy Events (GH Actions)   Write all metrics → DB
   ↓
Fetch Incidents (PagerDuty)
   ↓
Write raw data → DB

Phase 1 runs ONCE per test cycle (downloads 6 months of data).
Phase 2 runs MANY times (recomputes from cached raw data).
```

### 4.2 Trigger Mechanism

| Trigger | Method | Description |
|---|---|---|
| API Endpoint | `POST /api/poller/fetch` | Runs Phase 1 only |
| API Endpoint | `POST /api/poller/compute` | Runs Phase 2 only |
| API Endpoint | `POST /api/poller/full` | Runs Phase 1 + Phase 2 sequentially |
| CLI Command | `python -m poller --fetch` | Phase 1 from terminal |
| CLI Command | `python -m poller --compute` | Phase 2 from terminal |
| CLI Command | `python -m poller --full` | Both phases from terminal |
| Dashboard | "Run Poller" button | Triggers `POST /api/poller/full` |

### 4.3 Config Sync

`sprintsense-config.json` lives in the sprint-intelligence GitHub repo. The poller fetches it on startup.

```json
{
  "repos": [
    {"owner": "org", "name": "repo-name", "team": "team1"},
    {"owner": "org", "name": "another-repo", "team": "team2"}
  ],
  "labels": {
    "points_prefix": "points:",
    "bug": "bug",
    "feature": "feature",
    "tech_debt": "tech-debt",
    "task": "task",
    "sprint_prefix": "sprint:"
  },
  "thresholds": {
    "stale_pr_days": 3,
    "max_wip": 4,
    "scope_creep_points": 6
  },
  "sprint": {
    "duration_weeks": 2,
    "history_months": 6
  },
  "pagerduty": {
    "api_token_env": "PAGERDUTY_API_TOKEN"
  }
}
```

Config is synced to the `repos`, `label_config`, and `thresholds` tables on every poller run. Repo-to-team mapping is in the config.

### 4.4 Phase 1: Data Fetching

#### GitHub REST API v3

**Authentication:** Fine-grained personal access token in `GITHUB_TOKEN` env var.
**Base URL:** `https://api.github.com`

#### 4.4.1 Issues Fetch

```
Endpoint: GET /repos/{owner}/{repo}/issues
Parameters:
  - state: all
  - since: {6_months_ago_iso8601}
  - per_page: 100
  - page: 1..N
  - filter: all  (includes PRs — we filter by presence of pull_request key)
```

**Pagination:** Follow `Link` header for `rel="next"`. Stop when no more pages or `since` boundary is passed.

**Label parsing:** For each issue, parse labels:
- `points:1` → `story_points = 1`
- `points:3` → `story_points = 3`
- `points:5`, `points:8`, `points:13` similarly
- `bug` → `is_bug = true`
- `feature` → `is_feature = true`
- `tech-debt` → `is_techdebt = true`
- `sprint:team1-26.24.25` → sprint label for later reconciliation

**Deduplication:** `INSERT ... ON CONFLICT (github_id, repo_id) DO UPDATE` to handle re-fetches.

#### 4.4.2 Pull Requests Fetch

```
Endpoint: GET /repos/{owner}/{repo}/pulls
Parameters:
  - state: all
  - sort: updated
  - direction: desc
  - per_page: 100
```

For each PR, fetch commits to determine `first_commit_at`:
```
Endpoint: GET /repos/{owner}/{repo}/pulls/{pr_number}/commits
Parameters: per_page: 1 (only need the first commit)
```
Take `commits[0].commit.author.date` as `first_commit_at`.

**PR cycle time:** `first_commit_at → merged_at` in hours. If not merged, `cycle_time_hours = NULL`.

**Reviews:** Count reviews from PR details (`/pulls/{pr_number}/reviews`).

#### 4.4.3 Milestones Fetch

```
Endpoint: GET /repos/{owner}/{repo}/milestones
Parameters:
  - state: all
  - per_page: 100
```

Milestones with non-null `due_on` within the last 6 months are candidates for sprint mapping.

#### 4.4.4 Projects & Iterations Fetch

GitHub ProjectsV2 requires GraphQL API. Since we're using REST, Projects will be approximated:

**Approach:** Use Milestones as primary sprint mechanism. If `sprint:` labels exist on issues, use those as secondary. Project iterations are supported in the schema but fetched minimally.

```
Endpoint: POST /graphql
Query: organization(login: "{org}") { projectV2(number: N) { ... } }
```
Only if Projects are configured in `sprintsense-config.json`. Default: skip.

#### 4.4.5 Deploy Events (GitHub Actions)

```
Endpoint: GET /repos/{owner}/{repo}/actions/workflows
→ GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs
Parameters:
  - status: completed
  - created: >={6_months_ago}
  - per_page: 100
```

Filter for workflow names containing `deploy`, `release`, `production`. Mark successful runs as deploy events.

#### 4.4.6 Incident Events (PagerDuty)

```
Endpoint: GET /incidents
Headers: Authorization: Token token={PAGERDUTY_API_TOKEN}
Parameters:
  - since: {6_months_ago_iso8601}
  - until: {now}
  - limit: 100
  - offset: 0..N
```

Extract: `id`, `title`, `status`, `created_at`, `resolved_at`. Compute `mttr_hours` = `resolved_at - created_at`.

#### 4.4.7 Rate Limiting

| Limit | Value | Strategy |
|---|---|---|
| GitHub REST | 5,000 req/hr (authenticated) | Check `X-RateLimit-Remaining` header after each request. If < 50, sleep until `X-RateLimit-Reset`. |
| GitHub Search | 30 req/min | Not used — we query per-repo, not search API. |
| PagerDuty | 960 req/min | Far above our needs. Pagination with `offset` ≤ 10 pages. |
| Ollama | Local — no rate limit | Sequential calls only — one summary at a time to avoid OOM. |

**Conservative estimate for Phase 1 (10 repos, 6 months of data):**
- Issues: ~50 pages × 10 repos = 500 requests
- PRs + commits: ~100 pages × 10 repos × 2 (PRs + commits) = 2,000 requests
- Milestones: ~1 request × 10 repos = 10 requests
- Workflow runs: ~5 requests × 10 repos = 50 requests
- **Total: ~2,560 requests** — well under 5,000/hr limit for a single run.
- With sleep-on-limit, worst case: ~40 minutes for initial fetch. Typical: ~15-20 minutes.

### 4.5 Phase 2: Metric Computation

Runs entirely from the database. No API calls except LLM.

#### 4.5.1 Sprint Resolution

```
1. Query all milestones with due_on in last 6 months
2. For each milestone, map date range → team-YY.START_WEEK.END_WEEK
3. Query all distinct sprint: labels from issues
4. Merge overlapping sprints (milestone wins on conflict)
5. INSERT INTO sprints (name, start_date, end_date, ...)
6. For each issue, determine sprint membership:
   - If issue has a milestone → map to that sprint
   - If issue has sprint: label → map to that sprint
   - If issue has project iteration → map to that sprint
   - INSERT INTO issue_sprint_map
```

#### 4.5.2 Sprint Metrics Computation

```python
for sprint in sprints:
    issues = query_issues_in_sprint(sprint.id)
    prs = query_prs_merged_between(sprint.start_date, sprint.end_date)
    
    # Velocity
    metrics.planned_points = sum(i.story_points for i in issues)
    metrics.completed_points = sum(i.story_points for i in issues if i.state == 'closed')
    metrics.carry_over_points = sum(i.story_points for i in issues if i.state == 'open')
    
    # PR Cycle Time
    cycle_times = [pr.cycle_time_hours for pr in prs if pr.cycle_time_hours]
    metrics.cycle_time_mean = mean(cycle_times)
    metrics.cycle_time_median = median(cycle_times)
    metrics.cycle_time_p90 = percentile(cycle_times, 90)
    metrics.total_prs_merged = len(prs)
    
    # Bugs
    bugs_introduced = count(i for i in issues if i.is_bug and i.created_at in sprint)
    bugs_closed = count(i for i in issues if i.is_bug and i.closed_at in sprint)
    metrics.bug_regression_rate = bugs_introduced / metrics.completed_points if metrics.completed_points else 0
    
    # DORA
    deploys = query_deploys_between(sprint.start_date, sprint.end_date)
    metrics.deploy_frequency = len(deploys) / 2  # per week (2-week sprint)
    metrics.lead_time_hours = compute_lead_time(prs, deploys)
    metrics.mttr_hours = compute_mttr(incidents, sprint)
    metrics.change_failure_rate = compute_cfr(deploys, incidents)
```

#### 4.5.3 Engineer Metrics Computation

```python
engineers = distinct_assignees_in_sprint(sprint.id)
for eng in engineers:
    # Velocity contribution
    em.completed_points = sum(i.story_points for i in issues if i.assignee == eng and i.state == 'closed')
    
    # PR metrics
    eng_prs = [pr for pr in prs if pr.author == eng]
    em.prs_merged = len([p for p in eng_prs if p.merged_at])
    em.cycle_time_mean = mean(p.cycle_time_hours for p in eng_prs if p.cycle_time_hours)
    
    # Reviews (PRs reviewed, not authored)
    reviewed = [pr for pr in prs if eng in pr.reviewers]
    em.prs_reviewed = len(reviewed)
    
    # WIP
    em.max_concurrent_issues = max_concurrent_assigned(eng, sprint)
```

#### 4.5.4 LLM Summary Generation

```
For each sprint and persona level:
  1. Build prompt from sprint_metrics + engineer_metrics + alerts
  2. Call Ollama API: POST http://localhost:11434/api/generate
     { "model": "qwen3:9b", "prompt": "{system_prompt}\n{data_context}", "stream": false }
  3. Parse response → INSERT INTO ai_summaries (summary_text)
  4. Set reviewed = FALSE
  5. If Ollama unavailable → log warning, skip, continue
```

#### 4.5.5 Risk Alert Detection

```
Stale PRs:
  SELECT * FROM pull_requests
  WHERE state = 'open'
    AND EXTRACT(EPOCH FROM (NOW() - updated_at)) / 3600 > (stale_pr_days * 24)

Overloaded Engineers:
  SELECT assignee_login, COUNT(*) as wip
  FROM issues WHERE state = 'open'
  GROUP BY assignee_login HAVING COUNT(*) > max_wip

Scope Creep:
  Issues added to sprint AFTER sprint.start_date
  WHERE created_at > sprint.start_date AND points > scope_creep_threshold
```

### 4.6 Data Validation

| Check | How | Action |
|---|---|---|
| Missing story points | `story_points IS NULL` for closed issues | Log warning, exclude from velocity |
| Inconsistent labels | Issue has both `bug` and `feature` | Priority: `bug` wins |
| Orphaned issues | Issue has sprint label but no matching milestone | Create sprint from label |
| Rate limit hit | `X-RateLimit-Remaining < 50` | Sleep, log, resume |
| API errors | HTTP 4xx/5xx | Retry 3x with exponential backoff, then skip repo |

### 4.7 Error Handling

```
Phase 1 (Fetch):
  - Per-repo isolation: if one repo fails, continue with others
  - Retry logic: 3 attempts, exponential backoff (1s, 2s, 4s)
  - Log all errors to console + write to `fetch_errors` log table
  - On GitHub 403 (rate limit): sleep until reset, continue
  - On GitHub 404 (repo not found): skip repo, log warning
  - On PagerDuty 401: skip incidents, log error

Phase 2 (Compute):
  - Sprint resolution failure: skip malformed sprints, log
  - Metric computation failure: null-safe — no story points = 0, no PRs = skip cycle time
  - LLM unavailable: skip AI summaries for this sprint, log
  - LLM timeout (>120s): cancel, skip, log
```

---

## 5. Metric Computation

All metric computation logic is implemented in Phase 2 of the poller (see Section 4.5). Formulas are in `4.5.2` (sprint metrics), `4.5.3` (engineer metrics), `4.5.5` (risk alerts).

### 5.1 Metric Reference

| Metric | Formula | Source Tables |
|---|---|---|
| **Velocity** | `SUM(story_points) WHERE state='closed'` per sprint | `issues`, `issue_sprint_map` |
| **PR Cycle Time** | `first_commit_at → merged_at` in hours | `pull_requests` |
| **Bug Regression** | `bugs_introduced / total_completed_points` | `issues` |
| **Capacity vs Actual** | `actual_completed / planned` | `issues` |
| **Deploy Frequency** | `COUNT(deploy_events) / sprint_duration_weeks` | `deploy_events` |
| **Lead Time** | `AVG(merged_at - first_commit_at)` for all PRs merged in sprint | `pull_requests` |
| **MTTR** | `AVG(resolved_at - created_at)` for incidents in sprint | `incidents` |
| **Change Failure Rate** | `COUNT(incidents linked to deploys) / COUNT(deploys)` | `incidents`, `deploy_events` |

### 5.2 Null Handling

- Missing story points → exclude from velocity, log warning
- Unmerged PRs → skip cycle time computation
- No incidents in sprint → MTTR = NULL, display as "N/A"
- Zero deploys → change failure rate = NULL

### 5.3 Trends

Trends are computed at query time by the API server:
```sql
SELECT sprint_id, metric_value FROM sprint_metrics
WHERE sprint_id IN (last 3 sprints for this team)
ORDER BY sprint.start_date
```
The API returns the raw 3-sprint array. The dashboard renders the trend line client-side.

---

## 6. Dashboard & UI

### 6.1 Framework & Structure

- **Framework:** React (SPA) with Vite
- **Charts:** Recharts (composable React chart library)
- **Styling:** Tailwind CSS
- **Routing:** React Router — `/` is the main dashboard
- **API:** `fetch()` calls to Flask API server (`/api/*`)

**Page structure:** One dashboard page with persona toggle. No separate routes per persona.

```
┌──────────────────────────────────────────────────────────────┐
│  SprintSense             [Persona: SDM ▾]  [Admin]  [Sprint ▾] │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Velocity    │  │  PR Cycle    │  │  Bug Rate    │       │
│  │  ↑ 8%        │  │  Time 2.3d   │  │  ↓ 12%       │       │
│  │  [chart]     │  │  [chart]     │  │  [chart]     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Capacity vs │  │  DORA        │  │  Exec        │       │
│  │  Actual      │  │  Pulse       │  │  Summary     │       │
│  │  [chart]     │  │  [4 gauges]  │  │  5 bullets   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Risk Alerts                                         │   │
│  │  ⚠ Engineer X: WIP 5 (threshold: 4)    [Drill down]  │   │
│  │  ⚠ 3 stale PRs >3 days                  [Drill down]  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  🤖 Ask SprintSense a question...                    │   │
│  │  [                                            ] [Ask] │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│                                               Sprint 26.24.25 │
└──────────────────────────────────────────────────────────────┘
```

### 6.2 Layout Regions

| Region | Content | Persona-dependent? |
|---|---|---|
| **Top bar** | Persona selector dropdown, "Admin" link, sprint selector (prev/next dropdown) | No |
| **Metric cards** | 6 metric cards (SDM): velocity, PR cycle time, bug rate, capacity, DORA pulse, exec summary. Fewer for IC personas. | Yes — cards shown depend on persona selected |
| **Risk alerts** | Scrollable list of active alerts. Click to drill into engineer/PR detail. | Yes — SDM and SrSDM only |
| **Engineer drill-down** | Table: engineer name, WIP, cycle time, blocked tickets, velocity contribution. Sortable. | Yes — SDM and SrSDM only |
| **Sprint Q&A** | Text input + response area. User types question about sprint data → API calls Ollama → renders answer. | No — always visible |
| **Sprint selector** | Dropdown or navigation arrows to switch between sprints. Default: most recent. | No |

### 6.3 Persona Views

Since data is open to all users (D4 decision), persona views are UI presets, not permission gates.

| Persona | Default view | Cards shown | Extra |
|---|---|---|---|
| **Junior Engineer** | Personal metrics only | PR cycle time (personal), story points (personal), WIP, AI insight card | No team data, no peer data |
| **Senior Engineer** | Personal + team context | Personal cycle time, review count, story points, team velocity aggregate | Review turnaround |
| **Staff Engineer** | Personal + cross-team | Personal metrics, repo cycle time comparison table, blocker patterns | Cross-team view |
| **SDM** | Full team dashboard | All 6 metric cards, risk alerts, engineer table, exec summary (5 bullets) | Full access |
| **Senior SDM** | Multi-team | Per-team tabs + cross-team patterns + multi-team summary | No ranking view |
| **Director** | Org aggregate | 4 DORA gauges, org velocity, quality trends, Director-level summary | No per-team or per-person |

### 6.4 Charts & Visualizations

| Metric | Chart Type | Notes |
|---|---|---|
| Velocity | Bar chart (3 sprints) + trend line | Planned vs. completed side-by-side bars |
| PR Cycle Time | Line chart (3 sprints) | Mean, median, P90 as separate lines |
| Bug Regression | Bar chart (3 sprints) | Introduced vs. closed, net delta |
| Capacity vs. Actual | Gauge chart or progress bar | Percentage complete per sprint |
| DORA Pulse | 4 mini gauge cards | Deploy freq, lead time, MTTR, change failure rate |
| Engineer table | Sortable HTML table | WIP, cycle time, blocked, velocity columns |
| Cross-team cycle time | Horizontal bar chart | One bar per repo/team |

### 6.5 Executive Summary UI

- Renders pre-computed AI summary from `ai_summaries` table.
- 5 bullets in a card. Consequence-first styling: bold lead-in per bullet.
- "Reviewed" toggle (checkbox) — SDM checks after reading. Toggles `reviewed = TRUE` in DB.
- "Copy to clipboard" button — copies summary as plain text with bullet markers.
- If no summary exists (LLM was down): card shows "Summary not available. Run poller to regenerate."

### 6.6 Sprint Q&A Text Box

**Purpose:** Freeform natural language questions about sprint data, answered by Ollama on the same machine.

**UI:**
- Text input at bottom of dashboard: `🤖 Ask SprintSense a question...`
- "Ask" button or Enter to submit
- Response appears in a chat-bubble style area above the input
- Conversation history within the session (scrollable, not persisted)
- "Clear" button to reset conversation

**Flow:**
```
User types: "Which engineer had the most stale PRs last sprint?"
  → Dashboard: POST /api/ask { question, sprint_id, persona }
  → API Server:
      1. Reads sprint metrics + engineer metrics + alerts from DB
      2. Builds context: JSON dump of relevant data
      3. Constructs prompt: system_prompt + sprint_context + user_question
      4. Calls Ollama: POST http://localhost:11434/api/generate
      5. Returns { answer, model_used }
  → Dashboard: Renders answer below input
```

**Prompt template for Q&A:**
```
You are SprintSense, an AI sprint coach. You have access to sprint data below.
Answer concisely and data-forward. If you can't answer from the data, say so.

Sprint: {sprint_name} ({start_date} to {end_date})
Team velocity: {velocity} points (planned {planned}, completed {completed})
PR cycle time: mean {mean}h, P90 {p90}h
Bug regression: {bugs_introduced} introduced, {bugs_closed} closed
Engineers:
{engineer_table_json}
Alerts:
{alerts_json}

User question: {question}
```

**Error handling:**
- Ollama unavailable → "SprintSense AI is currently unavailable. Please try again."
- Timeout (>60s) → "Response timed out. Try a more specific question."
- Empty question → disabled submit button

### 6.7 Admin Page

**Route:** `/admin`

Accessed via the "Admin" link in the top bar. Contains poller controls, onboarding wizard, and configuration.

**Layout:**
```
┌──────────────────────────────────────────────┐
│  Admin                              [← Back] │
│                                              │
│  ┌─ Poller ─────────────────────────────────┐│
│  │                                         ││
│  │  [Fetch Data]   [Compute Metrics]        ││
│  │  [Run Full Poll (Fetch + Compute)]       ││
│  │                                         ││
│  │  Last fetch: 2026-06-27 14:32 UTC       ││
│  │  Last compute: 2026-06-27 14:38 UTC     ││
│  │  Status: ● Idle                         ││
│  │                                         ││
│  │  ┌─ Fetch Log ──────────────────────┐   ││
│  │  │ 14:32 - Fetching issues...       │   ││
│  │  │ 14:34 - repo/alpha: 234 issues   │   ││
│  │  │ 14:35 - repo/beta: 189 issues    │   ││
│  │  │ 14:38 - Compute complete         │   ││
│  │  └──────────────────────────────────┘   ││
│  └─────────────────────────────────────────┘│
│                                              │
│  ┌─ Onboarding Wizard ──────────────────────┐│
│  │  [Start Setup]  or [Re-run Setup]       ││
│  └─────────────────────────────────────────┘│
│                                              │
│  ┌─ Configuration ──────────────────────────┐│
│  │  Repos: team1/repo-a, team1/repo-b...    ││
│  │  Labels: points:, bug, feature...        ││
│  │  Thresholds: stale=3d, WIP=4, scope=6   ││
│  │  [Edit Config]                           ││
│  └─────────────────────────────────────────┘│
│                                              │
│  ┌─ System ─────────────────────────────────┐│
│  │  DB: PostgreSQL (connected)              ││
│  │  Ollama: ● Connected (qwen3:9b)          ││
│  │  GitHub API: 4,823 requests remaining    ││
│  └─────────────────────────────────────────┘│
└──────────────────────────────────────────────┘
```

### 6.8 Onboarding Flow

First-time setup wizard runs from the Admin page. Step-by-step modal overlay.

```
Step 1: "Welcome to SprintSense" — what it is, what it isn't (disclosure)
        ⬜ I understand SprintSense is a coaching tool, not surveillance
        [Next →]

Step 2: Connect repos — select repos from sprintsense-config.json
        ☑ team1/repo-a  ☑ team1/repo-b  ☑ team2/repo-c  ...
        [Next →]

Step 3: Verify labels — auto-detected from config
        Points prefix: [points:________]
        Bug label:     [bug___________]
        Feature label: [feature_______]
        Sprint prefix: [sprint:_______]
        [Next →]

Step 4: Thresholds — confirm defaults
        Stale PR days: [3_]
        Max WIP:       [4_]
        Scope creep:   [6_] points
        [Next →]

Step 5: Run first poll
        [Fetch Data] — progress bar shows real-time status
        Once complete: ✓ 1,247 issues fetched, ✓ 856 PRs fetched, ✓ 3 sprints detected
        [Go to Dashboard →]
```

Must complete in <30 minutes (SC9). Disclosure acknowledgment (Step 1 checkbox) is mandatory.

### 6.9 User Guide

Accessible via the Admin page under a "User Guide" tab or link. Four tabs:
1. **Reading your dashboard** — metric definitions, trend interpretation, thresholds
2. **What SprintSense is and isn't** — transparency disclosure (always available)
3. **Using in 1:1s / planning / retros** — coaching guides per persona
4. **Sprint Q&A tips** — example questions, what the AI can/can't answer

---

## 7. AI / LLM Integration

### 7.1 Model Configuration

| Parameter | Value |
|---|---|
| Provider | Ollama (MLX backend, Apple Silicon) |
| Model | `qwen3:9b` (Qwen 3.5, 9B params, 4-bit quantized) |
| Endpoint | `http://localhost:11434/api/generate` |
| Context window | ~32K tokens — well above our prompt + data size |
| Temperature | 0.3 (low — factual, consistent, low creativity) |
| Max tokens | 512 for summaries, 1024 for Q&A |
| Timeout | 60s (summaries), 120s (Q&A) |
| Fallback | None. If Ollama is offline, skip AI generation, log warning. |

### 7.2 Prompt Architecture

Three categories of LLM calls:

| Category | Trigger | Frequency | Prompt style |
|---|---|---|---|
| **Pre-computed summaries** | Poller Phase 2 | Once per sprint | Persona-tuned, data-heavy, structured output |
| **Sprint Q&A** | User-initiated via dashboard | On-demand | Conversational, context-heavy, freeform output |
| **Engineer AI nudges** | Poller Phase 2 | Once per sprint per engineer | Personal, coaching tone, 2-3 sentences |

All prompts follow the same structure:
```
[SYSTEM PROMPT — role, tone, constraints]
[DATA CONTEXT — structured JSON of metrics]
[USER INSTRUCTION — what to generate, format, length]
```

### 7.3 Persona-Tuned Summary Prompts

#### SDM Summary (5-bullet, consequence-first)

```
System: You are an AI sprint coach for an engineering manager. 
You analyze sprint data and produce a 5-bullet consequence-first summary.
Rules:
- Lead with the "so what" — impact before context
- Exactly 5 bullets, no more, no less
- Each bullet must reference specific data (numbers, trends, names)
- Flag risks with recommended actions
- Be direct. No fluff. No hedging.
- If data is missing, say "Data unavailable" — don't invent.

Data Context:
Sprint: {sprint_name} ({start_date} to {end_date})
Velocity: {completed_points} / {planned_points} pts ({velocity_ratio:.0%})
  3-sprint trend: {trend_json}
PR Cycle Time: mean {mean}h, median {median}h, P90 {p90}h ({total_prs} PRs)
  3-sprint trend: {trend_json}
Bug Regression: {bugs_introduced} introduced, {bugs_closed} closed (rate: {bug_rate:.2f})
Capacity: {actual_capacity} / {planned_capacity} pts ({capacity_ratio:.0%})
DORA: deploy freq {deploy_freq}/wk, lead time {lead_time}h, MTTR {mttr}h, CFR {cfr:.1%}
Engineers:
{engineer_table_json}
Alerts:
{alerts_json}

Generate a 5-bullet consequence-first sprint summary. Format:
1. [Bold lead-in]: context
2. [Bold lead-in]: context
...
```

#### Director Summary (strategic, quarterly, systemic)

```
System: You are an AI engineering advisor for a Director of Engineering.
You analyze org-level DORA metrics and delivery trends.
Rules:
- Focus on systemic patterns, not individual teams or engineers
- Quarter-over-quarter trends, not sprint-level details
- Flag one strategic recommendation
- 3-4 bullets max
- Data-forward, no fluff

Data Context:
Quarter: Q{quarter} {year}
Org DORA: deploy freq {qty}/wk (QoQ: {delta}), lead time {h}h (QoQ: {delta}), 
  MTTR {h}h (QoQ: {delta}), CFR {cfr}% (QoQ: {delta})
Org velocity: {total_pts} pts/sprint across {team_count} teams (QoQ: {delta}%)
Org quality: bug regression rate {rate} (QoQ: {delta})
Scope creep: {teams_with_creep} of {team_count} teams >20% scope creep

Generate a Director-level org health summary. Include one strategic recommendation for next quarter.
```

#### Junior Engineer Nudge (coaching, personal)

```
System: You are a supportive AI coach for a junior engineer.
You help them see their growth with data.
Rules:
- Positive, encouraging tone
- Reference specific improvements (trend data)
- One gentle nudge or tip
- 2-3 sentences max
- Never compare to other engineers

Data Context:
Engineer: {name}
PR cycle time: {current}h (trend: {trend})
Story points: {completed} pts this sprint (trend: {trend})
WIP: {current_wip} concurrent issues
Reviews received: {review_count}, avg turnaround {turnaround}h

Generate a personal growth insight. Celebrate improvements. Suggest one small tip.
```

### 7.4 Sprint Q&A Prompt

```
System: You are SprintSense AI, an assistant that answers questions about sprint data.
You have access to the current sprint's data below.
Rules:
- Answer concisely in 2-4 sentences
- Reference specific numbers from the data
- If you can't answer from the data, say so honestly
- If the question spans multiple sprints, note what you can/can't see
- Never invent data

Sprint Data:
{same data context as SDM summary — sprint_metrics + engineer_metrics + alerts + DORA}

Previous conversation:
{conversation_history_as_text}

User: {question}
```

### 7.5 Human Review Flow

- All pre-computed summaries are stored with `reviewed = FALSE`.
- Dashboard shows a "Reviewed" toggle next to the summary card.
- SDM checks the toggle after reading → sets `reviewed = TRUE` via API.
- "Copy to clipboard" button is always enabled (review not required to copy).
- The review toggle is a signal, not a gate. It tracks whether the SDM has read it.

### 7.6 Cost Estimation

- Ollama runs locally on macOS with MLX. **Zero API cost.**
- Model is 4-bit quantized (~5.5 GB VRAM for 9B params).
- Apple Silicon M-series handles inference efficiently.
- No cloud LLM spend. No rate limit costs.
- Only cost: electricity + machine time during Phase 2 compute.

---

## 8. Testing Strategy

### 8.1 Testing Constraints
- No access to internal team data
- Must validate against real-world public data
- Need realistic PR volume, issue counts, and activity patterns
- Last 6 months of history for meaningful trend analysis

### 8.2 Approach: Public Repos → Fabricated Sprint Structure

**Strategy:** Download real data from 10 high-activity public repos. Anonymize contributors and dates. Fabricate sprint assignments, labels, story points, deploy events, and incidents. The data volume and PR/issue complexity are real — the sprint structure is synthetic.

**Step 1: Select 10 Target Repos**

| # | Repo | Rationale |
|---|---|---|
| 1 | `microsoft/vscode` | Very high issue/PR volume, active community |
| 2 | `facebook/react` | High PR volume, good review patterns |
| 3 | `nodejs/node` | Mature project, diverse issue types |
| 4 | `kubernetes/kubernetes` | Massive volume, many contributors |
| 5 | `rust-lang/rust` | Structured labeling, RFC process |
| 6 | `vercel/next.js` | Active development, frequent releases |
| 7 | `grafana/grafana` | Good mix of features + bugs |
| 8 | `angular/angular` | Structured PR process, labels |
| 9 | `python/cpython` | Diverse contributor base |
| 10 | `tensorflow/tensorflow` | Large volume, varied issue types |

**Step 2: Download Raw Data**

Using GitHub REST API (same as Phase 1 poller):
- Issues: last 6 months, all states, per repo
- PRs: last 6 months, all states, per repo + first commit timestamps
- Milestones: all, per repo
- Workflow runs: last 6 months, deploy-related only

Estimated data volume: ~15,000 issues + ~20,000 PRs across 10 repos.

**Step 3: Anonymize & Transform**

`tools/transform_test_data.py` — a standalone script that reads raw JSON dumps and produces a seeded, transformed SQL dump.

**Anonymization:**
```
Real contributor → Fake engineer (1 repo = 1 team)
  microsoft/vscode  → team1-engineer1 through team1-engineer5
  facebook/react     → team2-engineer1 through team2-engineer5
  nodejs/node        → team3-engineer1 through team3-engineer5
  kubernetes/k8s     → team4-engineer1 through team4-engineer8 (large team)
  rust-lang/rust     → team5-engineer1 through team5-engineer5
  vercel/next.js     → team6-engineer1 through team6-engineer4
  grafana/grafana    → team7-engineer1 through team7-engineer5
  angular/angular    → team8-engineer1 through team8-engineer4
  python/cpython     → team9-engineer1 through team9-engineer5
  tensorflow/tf      → team10-engineer1 through team10-engineer4
  
  (10 teams, 50 total engineers)
```

**Team assignment:** 1 repo → 1 team. 10 repos → 10 teams.

| Team | Repo | Engineers |
|---|---|---|
| team1 | `microsoft/vscode` | 5 engineers |
| team2 | `facebook/react` | 5 engineers |
| team3 | `nodejs/node` | 5 engineers |
| team4 | `kubernetes/kubernetes` | 8 engineers (large team) |
| team5 | `rust-lang/rust` | 5 engineers |
| team6 | `vercel/next.js` | 4 engineers |
| team7 | `grafana/grafana` | 5 engineers |
| team8 | `angular/angular` | 4 engineers |
| team9 | `python/cpython` | 5 engineers |
| team10 | `tensorflow/tensorflow` | 4 engineers |

**Date shifting:** Optionally shift all dates to create a clean 6-month window ending "now." This ensures sprint boundaries align cleanly with ISO weeks.

**Sprint assignment:**
```
For each team, map issues/PRs to 2-week sprints based on their created/updated dates:
  team1-26.02.03, team1-26.04.05, ..., team1-26.24.25
  team2-26.02.03, team2-26.04.05, ..., team2-26.24.25
  ...
  (12 sprints per team = 120 sprints total)
```

**Step 4: Fabricate Labels & Metrics**

Since public repos don't use `points:N` or `sprint:` labels, we add them:

**Issue type and story point assignment (random):**

Both issue type (`bug`/`feature`/`tech-debt`/`task`) and story points (`1,2,3,5,8,13`) are assigned randomly using a seeded random generator. The seed ensures reproducibility across runs — same issue always gets same type + points.

```python
import random, hashlib

def assign_properties(github_issue_id):
    seed = int(hashlib.md5(str(github_issue_id).encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    issue_type = rng.choice(['feature', 'feature', 'feature', 'bug', 'bug', 'tech-debt', 'task'])
    story_points = rng.choice([1, 2, 2, 3, 3, 3, 5, 5, 8, 13])
    return issue_type, story_points
```

No weighted distribution — natural randomness from seed-based assignment produces a workable mix.

**Bug detection:**
- Issues labeled `bug` created during a sprint = `bugs_introduced`.
- Issues labeled `bug` closed during a sprint = `bugs_closed`.

**Scope creep simulation:**
- 15% of issues have `created_at` after their sprint `start_date` → triggers scope creep alerts.

**Step 5: Generate Deploy Events**

Synthetic deploy events per team per sprint:
- 3-7 deploys per sprint (random, seeded)
- 10% failure rate (deploy `status = 'failure'`)
- Timestamps distributed across the sprint's 2-week window
- Linked to specific repos

**Step 6: Generate Incidents**

Synthetic PagerDuty incidents:
- 0-3 incidents per team per sprint (random, seeded)
- 30% linked to a failed deploy (`is_change_failure = TRUE`)
- MTTR: random between 0.5h and 8h (log-normal distribution — most resolved fast, a few take hours)
- Timestamps within the sprint window

**Step 7: Load into DB**

Transformed data is loaded directly into PostgreSQL tables (bypasses Phase 1 poller). This is a one-time seed operation.

```bash
# Full test data setup flow
python tools/download_public_data.py --repos repos.json --since 2025-12-27 --output data/raw/
python tools/transform_test_data.py --input data/raw/ --output data/transformed/
python tools/seed_database.py --input data/transformed/ --db postgresql://...
python -m poller --compute   # Run Phase 2 on the seeded data
```

### 8.3 Test Data Validation

After seeding + computing, validate against known expectations:

| Check | Expected | How to verify |
|---|---|---|
| Issue count | ~15,000 issues across 10 repos | `SELECT COUNT(*) FROM issues` |
| PR count | ~20,000 PRs | `SELECT COUNT(*) FROM pull_requests` |
| Sprint count | 120 sprints (12 × 10 teams) | `SELECT COUNT(*) FROM sprints` |
| Feature/bug/techdebt/task | All present (no empty type column) | `SELECT is_feature, is_bug, is_techdebt, is_task, COUNT(*) FROM issues` |
| Engineers | 50 (across 10 teams) | `SELECT COUNT(DISTINCT assignee_login) FROM issues` |
| Deploy events | ≥ 360 (3 × 12 × 10 teams minimum) | `SELECT COUNT(*) FROM deploy_events` |
| Incidents | ≥ 0, ≤ 360 (3 × 12 × 10 teams maximum) | `SELECT COUNT(*) FROM incidents` |
| DORA metrics populated | 4 metrics × 120 sprints | `SELECT COUNT(*) FROM sprint_metrics WHERE deploy_frequency IS NOT NULL` |
| AI summaries | 120 SDM summaries + 120 Dir summaries | `SELECT COUNT(*) FROM ai_summaries` |
| Risk alerts | Some stale PRs, some overloaded engineers | `SELECT COUNT(*) FROM alerts WHERE alert_type = 'stale_pr'` |

### 8.4 Acceptance Criteria

| # | Criterion | How to verify |
|---|---|---|
| AC1 | Data pipeline downloads 10 public repos without errors | Phase 1 completes. All 10 repos have issues + PRs in DB. |
| AC2 | Data transformation produces 5 teams with 28 engineers | `tools/transform_test_data.py` output validates. |
| AC3 | Issues have assigned types + story points | No NULL values in `is_bug`/`is_feature`/`story_points` for closed issues. |
| AC4 | 120 sprints detected across 10 teams | `SELECT COUNT(*) FROM sprints` = 120. |
| AC5 | All metrics compute without errors | Phase 2 completes. No NULL sprints in sprint_metrics. |
| AC6 | AI summaries generated for all sprints (SDM level) | `SELECT COUNT(*) FROM ai_summaries WHERE persona_level = 'sdm'` = 120. |
| AC7 | Risk alerts fire for known conditions | At least 1 stale PR alert, 1 overloaded engineer alert, 1 scope creep alert. |
| AC8 | Dashboard renders all 6 metric cards with charts | Visual inspection. No blank cards. |
| AC9 | Sprint Q&A returns a valid answer to "What was team1's velocity last sprint?" | API returns non-empty answer. Answer references data. |
| AC10 | Persona toggle switches dashboard views correctly | Each persona sees different card sets as per visibility matrix. |

### 8.5 Test Environment

- Local PostgreSQL instance
- Ollama running locally (`qwen3:9b` model pulled and verified)
- Python virtual environment with Flask + SQLAlchemy + requests
- React dev server (Vite) for dashboard
- Test data generation is offline — no GitHub API calls needed after initial download
- Re-seedable: `tools/seed_database.py` can be re-run to start fresh

---

## 9. Security & Auth

### 9.1 Authentication

- **No OAuth or external auth provider.** Prototype uses manual user setup via backend.
- Users are defined in the database. Flask API checks a simple session or header-based user identity.
- Dashboard sends `X-User` header or session cookie. API resolves user from DB.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    default_persona VARCHAR(50) NOT NULL,   -- 'sdm', 'junior_eng', 'senior_eng', 'staff_eng', 'senior_sdm', 'director'
    team_name VARCHAR(100),                 -- NULL for Director, SrSDM
    is_admin BOOLEAN DEFAULT FALSE,         -- access to /admin page
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Test users (seeded manually):**

| Username | Persona | Team | Admin |
|---|---|---|---|
| `alex` | `sdm` | `team1` | Yes |
| `priya` | `junior_eng` | `team1` | No |

### 9.2 Authorization

| Page/API | Access |
|---|---|
| Dashboard `/` | Any authenticated user |
| Admin `/admin` | `is_admin = TRUE` only |
| `/api/poller/*` | `is_admin = TRUE` only |
| `/api/ask` | Any authenticated user |
| `/api/metrics/*` | Any authenticated user |

### 9.3 Data Visibility

All data is technically visible to all users (per PRD decision D4). Persona views are UI defaults, not permission gates. The API does not filter data by persona — the dashboard chooses which cards to render based on the user's `default_persona`.

### 9.4 Future: Workday/HR Integration

In production, user roles would sync from Workday or another HR system:
- Employee title/level → `default_persona` mapping
- Manager hierarchy → team assignment
- This is out of scope for prototype. Users are inserted manually via SQL or seed script.

### 9.5 Secrets Management

- `GITHUB_TOKEN` — environment variable in `docker-compose.yml`
- `PAGERDUTY_API_TOKEN` — environment variable in `docker-compose.yml`
- `ADMIN_PASSWORD` — optional, for extra admin page protection (not implemented in prototype)
- No secrets in code. All from env vars or `.env` file (gitignored).

---

## 10. Performance & Scaling

### 10.1 Performance Targets

| Metric | Target | Notes |
|---|---|---|
| Dashboard load (cold) | < 3 seconds | 6 metric cards + charts |
| Dashboard load (warm) | < 1 second | Subsequent loads |
| Phase 1: Fetch (10 repos) | < 30 minutes | Rate-limited. With sleep-on-limit, worst case ~40 min. |
| Phase 2: Compute (120 sprints) | < 5 minutes | Pure DB computation |
| LLM summary (per sprint) | < 10 seconds | Local Ollama, qwen3:9b |
| All 120 SDM summaries | < 20 minutes | Sequential (one at a time to avoid OOM) |
| Sprint Q&A response | < 15 seconds | User-facing, needs to feel fast |

### 10.2 Caching Strategy

- **No caching in prototype.** API reads directly from PostgreSQL.
- Metrics are pre-computed — queries are simple `SELECT` with no joins beyond 2 tables.
- If performance becomes an issue, add Flask-Caching with simple in-memory cache (TTL: 5 min).

### 10.3 API Optimization

- Pagination: all list endpoints support `?limit=50&offset=0`.
- Sprint data: single endpoint returns all metrics for a sprint in one response.
- Chart data: pre-aggregated arrays (3-sprint trend) returned by API — no client-side computation.
- No N+1 queries. All metric lookups use indexed columns.

### 10.4 Scaling Considerations

- **Out of scope for prototype.** Single instance, single DB, local machine.
- If scaling to production: read replicas for dashboard queries, separate poller worker, async LLM queue.
- PostgreSQL can handle 100+ concurrent dashboard users with simple indexed queries.

---

## 11. Deployment

### 11.1 Docker Compose

All services run in Docker Compose on local macOS machine.

```
docker-compose.yml
─────────────────
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: sprintsense
      POSTGRES_USER: sprintsense
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  api:
    build: ./api
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://sprintsense:${DB_PASSWORD}@db:5432/sprintsense
      GITHUB_TOKEN: ${GITHUB_TOKEN}
      PAGERDUTY_API_TOKEN: ${PAGERDUTY_API_TOKEN}
      OLLAMA_URL: http://host.docker.internal:11434
    depends_on:
      - db
    volumes:
      - ./api:/app

  dashboard:
    build: ./dashboard
    ports:
      - "3000:3000"
    environment:
      API_URL: http://localhost:5000
    depends_on:
      - api
    volumes:
      - ./dashboard:/app
      - /app/node_modules

volumes:
  pgdata:
```

### 11.2 Directory Structure

```
sprint-intelligence/
├── docker-compose.yml
├── .env                        # gitignored — GITHUB_TOKEN, DB_PASSWORD, etc.
├── sprintsense-config.json     # config — committed to repo
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py                  # Flask app entry point
│   ├── models.py               # SQLAlchemy models
│   ├── poller/
│   │   ├── __init__.py
│   │   ├── fetch.py            # Phase 1: data fetching
│   │   ├── compute.py          # Phase 2: metric computation
│   │   ├── github_client.py    # GitHub REST API wrapper
│   │   └── config.py           # Config sync from sprintsense-config.json
│   ├── routes/
│   │   ├── dashboard.py        # Metrics API endpoints
│   │   ├── poller.py           # Poller trigger endpoints
│   │   ├── ask.py              # Sprint Q&A endpoint
│   │   └── admin.py            # Admin endpoints
│   └── llm/
│       ├── __init__.py
│       ├── ollama_client.py    # Ollama API wrapper
│       └── prompts.py          # Prompt templates per persona
├── dashboard/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── components/
│       │   ├── MetricCard.jsx
│       │   ├── RiskAlerts.jsx
│       │   ├── EngineerTable.jsx
│       │   ├── SprintQA.jsx
│       │   ├── PersonaSelector.jsx
│       │   └── charts/
│       └── pages/
│           ├── Dashboard.jsx
│           └── Admin.jsx
├── tools/
│   ├── download_public_data.py  # Download from 10 public repos
│   ├── transform_test_data.py   # Anonymize + fabricate sprint structure
│   └── seed_database.py         # Load transformed data into DB
├── docs/
│   ├── prd.md
│   ├── spec.md
│   └── TODO.md
└── tests/
    ├── test_models.py
    ├── test_poller.py
    ├── test_metrics.py
    └── test_api.py
```

### 11.3 Environment Config

`.env` file (gitignored):
```
DB_PASSWORD=devpassword123
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
PAGERDUTY_API_TOKEN=optional_for_prototype
```

### 11.4 Running

```bash
# Build and start all services
docker compose up --build

# API at http://localhost:5000
# Dashboard at http://localhost:3000

# Run poller from within the api container
docker compose exec api python -m poller --full

# Seed test data
docker compose exec api python tools/seed_database.py

# Run tests
docker compose exec api pytest tests/
```

### 11.5 Ollama

Ollama runs on the host machine (not in Docker). The API container accesses it via `host.docker.internal:11434`. Model must be pulled before first use:

```bash
ollama pull qwen3:9b
```

### 11.6 CI/CD

- **No CI/CD pipeline for prototype.** Local development only.
- Database migrations: Alembic. Run manually: `docker compose exec api alembic upgrade head`.
- No automated tests in CI. Tests run locally.

---

## 12. Implementation Plan

### 12.1 M1: Data Foundation + SDM Core (1 Team)

**Scope:** 1 repo (team1), SDM dashboard. Prove the pipeline.

#### Features

| ID | Feature | Description |
|---|---|---|
| F1.1 | `sprintsense-config.json` | Config file with repos, labels, thresholds, sprint settings |
| F1.2 | Config sync | Poller reads config from GitHub repo, syncs to DB `repos`, `label_config`, `thresholds` tables |
| F1.3 | GitHub Issues ingestion | REST API: fetch issues with pagination, parse labels (`points:N`, `bug`, `feature`, `sprint:`) |
| F1.4 | GitHub PRs + commits ingestion | REST API: fetch PRs, first commit timestamps, compute `cycle_time_hours` |
| F1.5 | Milestones ingestion | REST API: fetch milestones with due dates for sprint detection |
| F1.6 | Rate limiting | Check `X-RateLimit-Remaining`, sleep on approaching limit |
| F1.7 | Phase 1: Fetch endpoint | `POST /api/poller/fetch` — triggers full data fetch |
| F1.8 | Sprint resolution | Map milestones → `team-YY.WW.WW` sprint names, assign issues to sprints |
| F1.9 | Velocity computation | Planned vs. completed story points per sprint |
| F1.10 | PR cycle time computation | Mean, median, P90 from `cycle_time_hours` |
| F1.11 | Bug regression computation | Bugs introduced vs. bugs closed per sprint |
| F1.12 | Capacity vs. actual computation | Planned vs. delivered story points |
| F1.13 | SDM dashboard page | React page with 4 metric cards + charts (Recharts) |
| F1.14 | Sprint selector | Dropdown to navigate between sprints |
| F1.15 | Engineer drill-down table | Sortable table: engineer name, WIP, cycle time, blocked, velocity |
| F1.16 | Phase 2: Compute endpoint | `POST /api/poller/compute` — computes all metrics |
| F1.17 | `POST /api/poller/full` | Combined Phase 1 + Phase 2 |
| F1.18 | Admin page — poller controls | Fetch/Compute/Full buttons with status display |
| F1.19 | Admin page — system status | DB connectivity, Ollama status, GitHub rate limit remaining |

#### Chores

| ID | Task |
|---|---|
| C1.1 | PostgreSQL schema + Alembic migrations |
| C1.2 | Flask app skeleton + Dockerfile |
| C1.3 | React app skeleton + Vite + Dockerfile |
| C1.4 | Docker Compose setup (db + api + dashboard) |
| C1.5 | `.env` template + gitignore |
| C1.6 | `tools/download_public_data.py` — download from 10 repos |
| C1.7 | `tools/transform_test_data.py` — anonymize + fabricate sprints |
| C1.8 | `tools/seed_database.py` — load test data |
| C1.9 | Seed 2 test users (alex/SDM, priya/junior_eng) |
| C1.10 | Admin page UI + routing |

#### Tests

| ID | Test |
|---|---|
| T1.1 | Issues ingestion: correct count, label parsing |
| T1.2 | PR cycle time: known timestamps → expected hours |
| T1.3 | Sprint resolution: milestone dates → correct `team1-26.XX.XX` name |
| T1.4 | Velocity: known points → expected completed/planned |
| T1.5 | Rate limiting: mock 403 → sleep + retry |

**Gate:** SDM dashboard loads with 12 sprints of data. All 4 metric cards render with charts. Engineer table shows correct data. → M2

---

### 12.2 M2: AI Summaries + Risk Alerts + DORA

**Scope:** Same 1 team. Add intelligence layer.

#### Features

| ID | Feature |
|---|---|
| F2.1 | Ollama client — connect to `host.docker.internal:11434`, call `/api/generate` |
| F2.2 | SDM summary prompt — 5-bullet consequence-first |
| F2.3 | AI summary generation — runs in Phase 2 compute |
| F2.4 | Summary card in dashboard — renders 5 bullets with "Reviewed" toggle |
| F2.5 | "Copy to clipboard" button |
| F2.6 | Stale PR alert: PRs with no activity >3 days |
| F2.7 | Overloaded engineer alert: WIP > 4 concurrent issues |
| F2.8 | Scope creep alert: issues added after sprint start |
| F2.9 | Risk alerts card in dashboard — scrollable alert list |
| F2.10 | Alert drill-down: click stale PR → see PR link/age; click overloaded → see engineer WIP breakdown |
| F2.11 | Deploy events ingestion — GitHub Actions workflow runs |
| F2.12 | PagerDuty incidents ingestion |
| F2.13 | DORA: deploy frequency computation |
| F2.14 | DORA: lead time computation |
| F2.15 | DORA: MTTR computation |
| F2.16 | DORA: change failure rate computation |
| F2.17 | DORA pulse card — 4 mini gauges on dashboard |
| F2.18 | Sprint planning capacity estimate view |
| F2.19 | Admin page — AI summary status per sprint |

#### Bug Fixes

| ID | Bug |
|---|---|
| B2.1 | M1: Handle repos with zero issues gracefully (no crash) |
| B2.2 | M1: Handle PRs with no commits (orphaned PRs) |
| B2.3 | M1: Sprint selector shows sprints in chronological order |

#### Chores

| ID | Task |
|---|---|
| C2.1 | Pull `qwen3:9b` model: `ollama pull qwen3:9b` |
| C2.2 | Verify Ollama accessible from Docker container |
| C2.3 | Prompt template library (`prompts.py`) |

#### Tests

| ID | Test |
|---|---|
| T2.1 | AI summary: known metrics → summary contains expected data points |
| T2.2 | AI summary: missing data → "Data unavailable" in bullet |
| T2.3 | AI summary: LLM offline → graceful skip, logged warning |
| T2.4 | Stale PR alert: PR updated 4 days ago → alert fires |
| T2.5 | Overloaded alert: engineer with WIP 5 → alert fires |
| T2.6 | Scope creep: issue created after sprint start → alert fires |
| T2.7 | DORA: known deploy events + incidents → correct CFR |

**Gate:** AI summary rendered for 12 sprints. All 3 alert types firing. 4 DORA gauges populated. → M3

---

### 12.3 M3: Engineer Self-Service Dashboards

**Scope:** Add IC personas for the pilot team. Expand dashboard to 3 engineer views + SDM.

#### Features

| ID | Feature |
|---|---|
| F3.1 | Persona selector dropdown in top bar |
| F3.2 | Junior engineer view: personal PR cycle time, story points, WIP, AI nudge |
| F3.3 | Junior engineer AI nudge prompt (coaching tone, 2-3 sentences) |
| F3.4 | Senior engineer view: personal + review metrics + team aggregate |
| F3.5 | Staff engineer view: personal + cross-team cycle time + blocker patterns |
| F3.6 | Engineer sprint metrics table populated from Phase 2 compute |
| F3.7 | Review metrics: PRs reviewed count + avg turnaround time |
| F3.8 | Blocked issue detection: issues with `blocked` label or state |
| F3.9 | Persona-tuned card visibility: different cards show per persona selection |
| F3.10 | Metric cards adapt to persona: fewer cards for junior, more for SDM |

#### Bug Fixes

| ID | Bug |
|---|---|
| B3.1 | M1/M2: SDM metrics show correct team (not all teams) |
| B3.2 | M1/M2: Engineer table respects sprint filter |
| B3.3 | M2: Alerts don't persist across sprints (alert has sprint_id FK) |

#### Chores

| ID | Task |
|---|---|
| C3.1 | Write persona-specific CSS/theme for each view |
| C3.2 | Add persona data to user session/header |

#### Tests

| ID | Test |
|---|---|
| T3.1 | Junior view: renders only personal cards (no team data) |
| T3.2 | Senior view: renders team aggregate card |
| T3.3 | Staff view: renders repo cycle time comparison |
| T3.4 | Persona toggle: switching from SDM → Junior changes visible cards |

**Gate:** All 4 persona views render correctly. Junior AI nudge generates per engineer. ≥80% of test engineers see their data. → M4

---

### 12.4 M4: Multi-Team + Senior SDM + Director

**Scope:** Add 2 more teams (team2, team3). Senior SDM and Director views.

#### Features

| ID | Feature |
|---|---|
| F4.1 | Multi-repo data pipeline — fetch issues/PRs for 2 additional repos |
| F4.2 | Phase 1 + Phase 2 handle multiple repos cleanly |
| F4.3 | Senior SDM view: per-team tabs (Team Alpha, Beta, Gamma) |
| F4.4 | Cross-team pattern detection: shared repo slowdown, correlated cycle time |
| F4.5 | Senior SDM AI summary prompt (multi-team, systemic) |
| F4.6 | Director view: org-level aggregate DORA + velocity + quality |
| F4.7 | Director AI summary prompt (strategic, QoQ trends) |
| F4.8 | Quarterly view in Director dashboard (12-sprint aggregation) |
| F4.9 | Director summary card — 3-4 bullets, strategic tone |
| F4.10 | No team ranking in Senior SDM view: per-team tabs, no comparison table |
| F4.11 | No per-engineer data in Director view |

#### Bug Fixes

| ID | Bug |
|---|---|
| B4.1 | M3: Engineer metrics computed for correct team |
| B4.2 | M3: Cross-team cycle time respects team boundaries |
| B4.3 | M2: DORA metrics scoped per team, not globally |

#### Tests

| ID | Test |
|---|---|
| T4.1 | Senior SDM view: shows per-team tabs, no ranking table |
| T4.2 | Senior SDM view: cross-team pattern detects Repo D slowdown |
| T4.3 | Director view: shows org aggregate DORA, no per-team data |
| T4.4 | Director view: quarterly aggregation spans 12 sprints |
| T4.5 | Director summary: references QoQ deltas, not sprint-level details |

**Gate:** Senior SDM sees 3 team tabs. Director sees org aggregate DORA. Cross-team pattern detected. → M5

---

### 12.5 M5: Full Org Rollout

**Scope:** All 10 teams, all 10 repos. Slack alerts, anomalies, health score.

#### Features

| ID | Feature |
|---|---|
| F5.1 | Full 10-team data pipeline |
| F5.2 | 120 sprints computed across all teams |
| F5.3 | Sprint Q&A text box in dashboard |
| F5.4 | Sprint Q&A API endpoint (`POST /api/ask`) |
| F5.5 | Sprint Q&A Ollama integration with sprint data context |
| F5.6 | Anomaly detection: velocity drop >25% vs. 12-sprint baseline |
| F5.7 | Delivery Health Score: composite of DORA + velocity stability + quality |
| F5.8 | Custom metric thresholds per team (admin page) |
| F5.9 | Onboarding wizard on admin page (6-step modal) |
| F5.10 | User guide accessible from admin page |

#### Bug Fixes

| ID | Bug |
|---|---|
| B5.1 | M4: Cross-team data for 10 teams renders without performance degradation |
| B5.2 | M4: Senior SDM view handles 10 team tabs (scroll or dropdown) |

#### Chores

| ID | Task |
|---|---|
| C5.1 | Generate full 10-team test data set |
| C5.2 | Run full Phase 1 + Phase 2 on 10-team data |
| C5.3 | Performance test: 120-sprint dashboard load < 3s |

#### Tests

| ID | Test |
|---|---|
| T5.1 | Sprint Q&A: "What was team1's velocity?" → returns data-backed answer |
| T5.2 | Sprint Q&A: "Which engineer is overloaded?" → returns correct name |
| T5.3 | Sprint Q&A: offline LLM → error message in dashboard |
| T5.4 | Anomaly: velocity drop >25% → alert fires |
| T5.5 | Health Score: known metrics → expected composite value |
| T5.6 | Onboarding wizard: completes in <30 min (timed test) |

**Gate:** ≥80% of 10 teams have valid metrics. Q&A works for 5 test questions. Health score renders. → M6

---

### 12.6 M6: Polish, Ecosystem, Self-Serve

**Scope:** Harden, document, integrate stubs for future DeliveryOS.

#### Features

| ID | Feature |
|---|---|
| F6.1 | Export-to-slide: download DORA + velocity chart as PNG/PDF |
| F6.2 | Trend forecasting stub: "if trajectory holds, expect X by Q4" |
| F6.3 | DeliveryOS integration stub: standardize metric format for future platform |
| F6.4 | Self-service onboarding: config file → auto-detect repos + labels |

#### Bug Fixes

| ID | Bug |
|---|---|
| B6.1 | M1-M5: All edge cases from 10-team data (null handling, missing sprints) |
| B6.2 | Performance: dashboard load time with 120 sprints ≤ 3s |

#### Chores

| ID | Task |
|---|---|
| C6.1 | README with setup instructions |
| C6.2 | API documentation (endpoints, request/response examples) |
| C6.3 | User guide: 4 tabs completed |
| C6.4 | Code cleanup, linting, docstrings |
| C6.5 | Final test run: full 10-team seed → compute → dashboard validation |

**Gate:** All 10 acceptance criteria (Section 8.4) pass. Dashboard load < 3s. User guide complete. README clear.

---

*This spec is filled in section by section. Each section is discussed and decided before the next begins.*
