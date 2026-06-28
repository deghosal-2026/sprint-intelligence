# SprintSense — TODO

**Status:** ALL MILESTONES COMPLETE — June 28, 2026 (10 teams, 120 sprints, 95 tests, trend forecasts, 3 persona AI summaries)
**Spec:** `docs/spec.md`
**All issues:** `#13`–`#140` on GitHub

**Workflow:** Complete each issue's feature + tests + bugfixes before moving to the next within the milestone.

## Known Issues

1. **Admin regenerate/fetch/compute background threads** — Operations now run in background threads (no more gunicorn hangs). However, `generate_all_summaries()` loops 120 sprints × ~2s LLM calls = ~4 min, and the thread may appear stuck. The admin UI shows "running" status with progress. Summaries do generate but `last_regenerate` status field may not always update. Workaround: run directly via `docker compose exec api python3 -c "from api.app import create_app; from api.poller.compute import generate_all_summaries; app=create_app(); app.app_context().push(); generate_all_summaries()"`.

2. **Poller fetch from admin UI** — Runs in background thread but makes live GitHub API calls for 11 repos. Data already seeded in DB. Use only for fresh data refresh.

3. **Poller compute from admin UI** — Runs in background thread with progress updates. Works for metrics/DORA/alerts/forecasts. AI summary portion is slow (see #1).

4. **PagerDuty token** — Placeholder in `.env`. No real PagerDuty integration; incidents are synthetic.

---

## M1: Data Foundation + SDM Core ✅
**Issues: #13–#46** (34 issues)

### Scaffolding ✅
- [x] [#13](https://github.com/deghosal-2026/sprint-intelligence/issues/13) C1.1 PostgreSQL schema + Alembic migrations
- [x] [#14](https://github.com/deghosal-2026/sprint-intelligence/issues/14) C1.2 Flask app skeleton + Dockerfile
- [x] [#15](https://github.com/deghosal-2026/sprint-intelligence/issues/15) C1.3 React app skeleton + Vite + Dockerfile
- [x] [#16](https://github.com/deghosal-2026/sprint-intelligence/issues/16) C1.4 Docker Compose setup
- [x] [#17](https://github.com/deghosal-2026/sprint-intelligence/issues/17) C1.5 .env template + gitignore
- [x] [#18](https://github.com/deghosal-2026/sprint-intelligence/issues/18) C1.6 tools/download_public_data.py
- [x] [#19](https://github.com/deghosal-2026/sprint-intelligence/issues/19) C1.7 tools/transform_test_data.py
- [x] [#20](https://github.com/deghosal-2026/sprint-intelligence/issues/20) C1.8 tools/seed_database.py
- [x] [#21](https://github.com/deghosal-2026/sprint-intelligence/issues/21) C1.9 Seed 2 test users
- [x] [#22](https://github.com/deghosal-2026/sprint-intelligence/issues/22) C1.10 Admin page UI + routing

### Features ✅
- [x] [#23](https://github.com/deghosal-2026/sprint-intelligence/issues/23) F1.1 sprintsense-config.json
- [x] [#24](https://github.com/deghosal-2026/sprint-intelligence/issues/24) F1.2 Config sync
- [x] [#25](https://github.com/deghosal-2026/sprint-intelligence/issues/25) F1.3 GitHub Issues ingestion
- [x] [#26](https://github.com/deghosal-2026/sprint-intelligence/issues/26) F1.4 GitHub PRs + commits
- [x] [#27](https://github.com/deghosal-2026/sprint-intelligence/issues/27) F1.5 Milestones ingestion
- [x] [#28](https://github.com/deghosal-2026/sprint-intelligence/issues/28) F1.6 Rate limiting
- [x] [#29](https://github.com/deghosal-2026/sprint-intelligence/issues/29) F1.7 Phase 1 Fetch endpoint
- [x] [#30](https://github.com/deghosal-2026/sprint-intelligence/issues/30) F1.8 Sprint resolution
- [x] [#31](https://github.com/deghosal-2026/sprint-intelligence/issues/31) F1.9 Velocity computation
- [x] [#32](https://github.com/deghosal-2026/sprint-intelligence/issues/32) F1.10 PR cycle time computation
- [x] [#33](https://github.com/deghosal-2026/sprint-intelligence/issues/33) F1.11 Bug regression computation
- [x] [#34](https://github.com/deghosal-2026/sprint-intelligence/issues/34) F1.12 Capacity vs actual computation
- [x] [#35](https://github.com/deghosal-2026/sprint-intelligence/issues/35) F1.13 SDM dashboard (4 metric cards + Recharts)
- [x] [#36](https://github.com/deghosal-2026/sprint-intelligence/issues/36) F1.14 Sprint selector dropdown
- [x] [#37](https://github.com/deghosal-2026/sprint-intelligence/issues/37) F1.15 Engineer drill-down table
- [x] [#38](https://github.com/deghosal-2026/sprint-intelligence/issues/38) F1.16 Phase 2 Compute endpoint
- [x] [#39](https://github.com/deghosal-2026/sprint-intelligence/issues/39) F1.17 Full poll endpoint
- [x] [#40](https://github.com/deghosal-2026/sprint-intelligence/issues/40) F1.18 Admin poller controls
- [x] [#41](https://github.com/deghosal-2026/sprint-intelligence/issues/41) F1.19 Admin system status

### Tests ✅
- [x] [#42](https://github.com/deghosal-2026/sprint-intelligence/issues/42) T1.1 Issues ingestion test
- [x] [#43](https://github.com/deghosal-2026/sprint-intelligence/issues/43) T1.2 PR cycle time test
- [x] [#44](https://github.com/deghosal-2026/sprint-intelligence/issues/44) T1.3 Sprint resolution test
- [x] [#45](https://github.com/deghosal-2026/sprint-intelligence/issues/45) T1.4 Velocity test
- [x] [#46](https://github.com/deghosal-2026/sprint-intelligence/issues/46) T1.5 Rate limiting test

---

## M2: AI Summaries + Risk Alerts + DORA ✅
**Issues: #47–#75** (29 issues)

### Features ✅
- [x] [#47](https://github.com/deghosal-2026/sprint-intelligence/issues/47) F2.1 Ollama client — connect to host.docker.internal:11434, POST /api/generate
- [x] [#48](https://github.com/deghosal-2026/sprint-intelligence/issues/48) F2.2 SDM summary prompt — 5-bullet, consequence-first template
- [x] [#49](https://github.com/deghosal-2026/sprint-intelligence/issues/49) F2.3 AI summary generation — Phase 2: per sprint + persona, call Ollama
- [x] [#50](https://github.com/deghosal-2026/sprint-intelligence/issues/50) F2.4 Summary card — 5 bullets, Reviewed toggle, Copy to clipboard
- [x] [#51](https://github.com/deghosal-2026/sprint-intelligence/issues/51) F2.5 Copy to clipboard button
- [x] [#52](https://github.com/deghosal-2026/sprint-intelligence/issues/52) F2.6 Stale PR alert — no activity >3d
- [x] [#53](https://github.com/deghosal-2026/sprint-intelligence/issues/53) F2.7 Overloaded engineer alert — WIP >4
- [x] [#54](https://github.com/deghosal-2026/sprint-intelligence/issues/54) F2.8 Scope creep alert — issues added after sprint start
- [x] [#55](https://github.com/deghosal-2026/sprint-intelligence/issues/55) F2.9 Risk alerts card — scrollable list in dashboard
- [x] [#56](https://github.com/deghosal-2026/sprint-intelligence/issues/56) F2.10 Alert drill-down — click stale PR → PR link, overloaded → WIP breakdown
- [x] [#57](https://github.com/deghosal-2026/sprint-intelligence/issues/57) F2.11 Deploy events ingestion — GH Actions workflow runs
- [x] ~~#58 F2.12 PagerDuty incidents ingestion~~ *(skipped per plan)*
- [x] [#59](https://github.com/deghosal-2026/sprint-intelligence/issues/59) F2.13 DORA: deploy frequency — deploys per week
- [x] [#60](https://github.com/deghosal-2026/sprint-intelligence/issues/60) F2.14 DORA: lead time — commit → deploy
- [x] [#61](https://github.com/deghosal-2026/sprint-intelligence/issues/61) F2.15 DORA: MTTR — incident resolution time
- [x] [#62](https://github.com/deghosal-2026/sprint-intelligence/issues/62) F2.16 DORA: change failure rate — failed deploys / total deploys
- [x] [#63](https://github.com/deghosal-2026/sprint-intelligence/issues/63) F2.17 DORA pulse card — 4 mini gauges on dashboard
- [x] [#64](https://github.com/deghosal-2026/sprint-intelligence/issues/64) F2.18 Sprint planning capacity view
- [x] [#65](https://github.com/deghosal-2026/sprint-intelligence/issues/65) F2.19 Admin AI summary status — per sprint, regenerate button

### Bug Fixes ✅
- [x] [#66](https://github.com/deghosal-2026/sprint-intelligence/issues/66) B2.1 Handle repos with zero issues gracefully
- [x] [#67](https://github.com/deghosal-2026/sprint-intelligence/issues/67) B2.2 Handle PRs with no commits (orphaned)
- [x] [#68](https://github.com/deghosal-2026/sprint-intelligence/issues/68) B2.3 Sprint selector in chronological order

### Tests ✅
- [x] [#69](https://github.com/deghosal-2026/sprint-intelligence/issues/69) T2.1 AI summary: known metrics → expected data points
- [x] [#70](https://github.com/deghosal-2026/sprint-intelligence/issues/70) T2.2 AI summary: missing data → "Data unavailable"
- [x] [#71](https://github.com/deghosal-2026/sprint-intelligence/issues/71) T2.3 AI summary: LLM offline → graceful skip
- [x] [#72](https://github.com/deghosal-2026/sprint-intelligence/issues/72) T2.4 Stale PR alert fires on 4d-old PR
- [x] [#73](https://github.com/deghosal-2026/sprint-intelligence/issues/73) T2.5 Overloaded alert fires on WIP 5
- [x] [#74](https://github.com/deghosal-2026/sprint-intelligence/issues/74) T2.6 Scope creep alert fires on post-start issue
- [x] [#75](https://github.com/deghosal-2026/sprint-intelligence/issues/75) T2.7 DORA CFR correct with known deploys + incidents

### Chores ✅
- [x] [#141](https://github.com/deghosal-2026/sprint-intelligence/issues/141) C2.1 Update transform/seed scripts for chunked raw data

**Status:** 60 AI summaries generated (Llama-3.2-3B-Instruct-4bit via omlx). 1228 alerts, 4 DORA gauges, 82/82 tests passing.

**Gate:** ✅ → M3

---

## M3: Engineer Self-Service Dashboards ✅
**Issues: #76–#92** (17 issues)

### Features ✅
- [x] [#76](https://github.com/deghosal-2026/sprint-intelligence/issues/76) F3.1 Persona selector dropdown — Junior/Senior/Staff/SDM
- [x] [#77](https://github.com/deghosal-2026/sprint-intelligence/issues/77) F3.2 Junior engineer view — personal cycle time, points, WIP, nudge
- [x] [#78](https://github.com/deghosal-2026/sprint-intelligence/issues/78) F3.3 Junior engineer AI nudge — coaching prompt, 2-3 sentences
- [x] [#79](https://github.com/deghosal-2026/sprint-intelligence/issues/79) F3.4 Senior engineer view — personal + review + team aggregate
- [x] [#80](https://github.com/deghosal-2026/sprint-intelligence/issues/80) F3.5 Staff engineer view — personal + cross-team + blockers
- [x] [#81](https://github.com/deghosal-2026/sprint-intelligence/issues/81) F3.6 Engineer sprint metrics — Phase 2 per-engineer computation
- [x] [#82](https://github.com/deghosal-2026/sprint-intelligence/issues/82) F3.7 Review metrics — PRs reviewed + avg turnaround
- [x] [#83](https://github.com/deghosal-2026/sprint-intelligence/issues/83) F3.8 Blocked issue detection — blocked label/state
- [x] [#84](https://github.com/deghosal-2026/sprint-intelligence/issues/84) F3.9 Persona-tuned card visibility
- [x] [#85](https://github.com/deghosal-2026/sprint-intelligence/issues/85) F3.10 Adaptive metric cards — fewer for junior, more for SDM

### Bug Fixes ✅
- [x] [#86](https://github.com/deghosal-2026/sprint-intelligence/issues/86) B3.1 SDM metrics show correct team (not all teams)
- [x] [#87](https://github.com/deghosal-2026/sprint-intelligence/issues/87) B3.2 Engineer table respects sprint filter
- [x] [#88](https://github.com/deghosal-2026/sprint-intelligence/issues/88) B3.3 Alerts scoped to sprint (don't persist across sprints)

### Tests ✅
- [x] [#89](https://github.com/deghosal-2026/sprint-intelligence/issues/89) T3.1 Junior view: only personal cards, no team data
- [x] [#90](https://github.com/deghosal-2026/sprint-intelligence/issues/90) T3.2 Senior view: team aggregate card renders
- [x] [#91](https://github.com/deghosal-2026/sprint-intelligence/issues/91) T3.3 Staff view: repo cycle time comparison renders
- [x] [#92](https://github.com/deghosal-2026/sprint-intelligence/issues/92) T3.4 Persona toggle switches visible cards correctly

**Status:** 82 Python tests + 13 frontend vitest tests = 95 total. All 4 persona views render.

**Gate:** ✅ → M4

---

## M4: Multi-Team + Senior SDM + Director ✅
**Issues: #93–#111** (19 issues)

### Features ✅
- [x] [#93](https://github.com/deghosal-2026/sprint-intelligence/issues/93) F4.1 Multi-repo pipeline — Phase 1 for 2 more repos
- [x] [#94](https://github.com/deghosal-2026/sprint-intelligence/issues/94) F4.2 Multi-repo Phase 1 + 2 — config-driven iteration
- [x] [#95](https://github.com/deghosal-2026/sprint-intelligence/issues/95) F4.3 Senior SDM view — per-team tabs (10 teams)
- [x] [#96](https://github.com/deghosal-2026/sprint-intelligence/issues/96) F4.4 Cross-team pattern detection — velocity decline, cycle time increase
- [x] [#97](https://github.com/deghosal-2026/sprint-intelligence/issues/97) F4.5 SrSDM AI summary — multi-team, systemic prompt
- [x] [#98](https://github.com/deghosal-2026/sprint-intelligence/issues/98) F4.6 Director view — org DORA + velocity + quality
- [x] [#99](https://github.com/deghosal-2026/sprint-intelligence/issues/99) F4.7 Director AI summary — strategic, QoQ trends, 3-4 bullets
- [x] [#100](https://github.com/deghosal-2026/sprint-intelligence/issues/100) F4.8 Quarterly view — 12-sprint aggregation + QoQ deltas
- [x] [#101](https://github.com/deghosal-2026/sprint-intelligence/issues/101) F4.9 Director summary card — strategic, different from SDM
- [x] [#102](https://github.com/deghosal-2026/sprint-intelligence/issues/102) F4.10 No team ranking — tabs only, no comparison table in SrSDM
- [x] [#103](https://github.com/deghosal-2026/sprint-intelligence/issues/103) F4.11 No per-engineer for Director — org aggregate only

### Bug Fixes ✅
- [x] [#104](https://github.com/deghosal-2026/sprint-intelligence/issues/104) B4.1 Engineer metrics computed for correct team
- [x] [#105](https://github.com/deghosal-2026/sprint-intelligence/issues/105) B4.2 Cross-team cycle time respects boundaries
- [x] [#106](https://github.com/deghosal-2026/sprint-intelligence/issues/106) B4.3 DORA metrics scoped per team (repo_id filter added)

### Tests ✅
- [x] [#107](https://github.com/deghosal-2026/sprint-intelligence/issues/107) T4.1 SrSDM: per-team tabs, no ranking table
- [x] [#108](https://github.com/deghosal-2026/sprint-intelligence/issues/108) T4.2 Cross-team pattern detects repo slowdown
- [x] [#109](https://github.com/deghosal-2026/sprint-intelligence/issues/109) T4.3 Director: org aggregate, no per-team data
- [x] [#110](https://github.com/deghosal-2026/sprint-intelligence/issues/110) T4.4 Quarterly view spans 12 sprints
- [x] [#111](https://github.com/deghosal-2026/sprint-intelligence/issues/111) T4.5 Director summary references QoQ deltas

**Status:** 10 teams, 120 sprints, 120 sprint metrics, 120 DORA metrics, 1362 alerts. SrSDM tabs + Director org view + quarterly comparison + cross-team patterns all working. 95 tests passing.

**Known Issues:** See top of file (#1-4: admin regenerate/fetch/compute hang on bulk operations).

**Gate:** ✅ → M5

---

## M5: Full Org Rollout + Sprint Q&A — DROPPED
**Issues: #112–#129** (18 issues)

*Dropped — no org rollout planned. Q&A, anomaly detection, health score, onboarding wizard not needed for prototype.*

---

## M6: Polish, Ecosystem, Self-Serve ✅
**Issues: #130–#140, #142** (12 issues, 5 skipped)

### Features ✅
- [x] [#131](https://github.com/deghosal-2026/sprint-intelligence/issues/131) F6.2 Trend forecasting — linear regression persisted in DB, shown in SrSDM + Director
- [x] ~~#130 F6.1 Export-to-slide~~ *(skipped — screenshots suffice)*
- [x] ~~#132 F6.3 DeliveryOS integration stub~~ *(skipped — not built)*
- [x] ~~#133 F6.4 Self-service onboarding~~ *(skipped)*

### Bug Fixes ✅
- [x] ~~#135 B6.2 Dashboard load ≤3s~~ *(skipped — performance fine)*

### Chores ✅
- [x] [#136](https://github.com/deghosal-2026/sprint-intelligence/issues/136) C6.1 README — setup, architecture, running guide
- [x] [#137](https://github.com/deghosal-2026/sprint-intelligence/issues/137) C6.2 API documentation — docs/API.md
- [x] [#138](https://github.com/deghosal-2026/sprint-intelligence/issues/138) C6.3 User guide — docs/USER_GUIDE.md
- [x] [#139](https://github.com/deghosal-2026/sprint-intelligence/issues/139) C6.4 Code cleanup — ruff clean (0 issues)
- [x] [#140](https://github.com/deghosal-2026/sprint-intelligence/issues/140) C6.5 Final test run — 95 tests passing
- [x] [#142](https://github.com/deghosal-2026/sprint-intelligence/issues/142) C6.6 Update screenshots with trend forecasts

**Status:** All milestones complete. 95 tests, 10 teams, 120 sprints, trend forecasts, 3 persona AI summaries.

**Gate:** ✅ Project complete.
