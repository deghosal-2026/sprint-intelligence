# SprintSense — TODO

**Status:** M3 COMPLETE — June 28, 2026 (95 tests, all 47 issues closed across M1-M3)
**Spec:** `docs/spec.md`
**All issues:** `#13`–`#140` on GitHub

**Workflow:** Complete each issue's feature + tests + bugfixes before moving to the next within the milestone.

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

## M4: Multi-Team + Senior SDM + Director
**Issues: #93–#111** (19 issues)

### Features
- [ ] [#93](https://github.com/deghosal-2026/sprint-intelligence/issues/93) F4.1 Multi-repo pipeline — Phase 1 for 2 more repos
- [ ] [#94](https://github.com/deghosal-2026/sprint-intelligence/issues/94) F4.2 Multi-repo Phase 1 + 2 — config-driven iteration
- [ ] [#95](https://github.com/deghosal-2026/sprint-intelligence/issues/95) F4.3 Senior SDM view — per-team tabs (3 teams)
- [ ] [#96](https://github.com/deghosal-2026/sprint-intelligence/issues/96) F4.4 Cross-team pattern detection — shared slowdown, correlated cycle time
- [ ] [#97](https://github.com/deghosal-2026/sprint-intelligence/issues/97) F4.5 SrSDM AI summary — multi-team, systemic prompt
- [ ] [#98](https://github.com/deghosal-2026/sprint-intelligence/issues/98) F4.6 Director view — org DORA + velocity + quality
- [ ] [#99](https://github.com/deghosal-2026/sprint-intelligence/issues/99) F4.7 Director AI summary — strategic, QoQ trends, 3-4 bullets
- [ ] [#100](https://github.com/deghosal-2026/sprint-intelligence/issues/100) F4.8 Quarterly view — 12-sprint aggregation
- [ ] [#101](https://github.com/deghosal-2026/sprint-intelligence/issues/101) F4.9 Director summary card — 3-4 bullet strategic
- [ ] [#102](https://github.com/deghosal-2026/sprint-intelligence/issues/102) F4.10 No team ranking — tabs only, no comparison table
- [ ] [#103](https://github.com/deghosal-2026/sprint-intelligence/issues/103) F4.11 No per-engineer for Director — org aggregate only

### Bug Fixes
- [ ] [#104](https://github.com/deghosal-2026/sprint-intelligence/issues/104) B4.1 Engineer metrics computed for correct team
- [ ] [#105](https://github.com/deghosal-2026/sprint-intelligence/issues/105) B4.2 Cross-team cycle time respects boundaries
- [ ] [#106](https://github.com/deghosal-2026/sprint-intelligence/issues/106) B4.3 DORA metrics scoped per team (not global)

### Tests
- [ ] [#107](https://github.com/deghosal-2026/sprint-intelligence/issues/107) T4.1 SrSDM: per-team tabs, no ranking table
- [ ] [#108](https://github.com/deghosal-2026/sprint-intelligence/issues/108) T4.2 Cross-team pattern detects repo slowdown
- [ ] [#109](https://github.com/deghosal-2026/sprint-intelligence/issues/109) T4.3 Director: org aggregate, no per-team data
- [ ] [#110](https://github.com/deghosal-2026/sprint-intelligence/issues/110) T4.4 Quarterly view spans 12 sprints
- [ ] [#111](https://github.com/deghosal-2026/sprint-intelligence/issues/111) T4.5 Director summary references QoQ deltas

**Gate:** SrSDM sees 3 team tabs. Director sees org DORA. → M5

---

## M5: Full Org Rollout + Sprint Q&A
**Issues: #112–#129** (18 issues)

### Features
- [ ] [#112](https://github.com/deghosal-2026/sprint-intelligence/issues/112) F5.1 Full 10-team data pipeline
- [ ] [#113](https://github.com/deghosal-2026/sprint-intelligence/issues/113) F5.2 120 sprints computed across all teams
- [ ] [#114](https://github.com/deghosal-2026/sprint-intelligence/issues/114) F5.3 Sprint Q&A text box — text input + chat bubbles
- [ ] [#115](https://github.com/deghosal-2026/sprint-intelligence/issues/115) F5.4 Sprint Q&A API — POST /api/ask
- [ ] [#116](https://github.com/deghosal-2026/sprint-intelligence/issues/116) F5.5 Sprint Q&A Ollama integration — context + history
- [ ] [#117](https://github.com/deghosal-2026/sprint-intelligence/issues/117) F5.6 Anomaly detection — velocity drop >25% vs 12-sprint baseline
- [ ] [#118](https://github.com/deghosal-2026/sprint-intelligence/issues/118) F5.7 Delivery Health Score — DORA + velocity + quality composite
- [ ] [#119](https://github.com/deghosal-2026/sprint-intelligence/issues/119) F5.8 Custom metric thresholds per team (admin page)
- [ ] [#120](https://github.com/deghosal-2026/sprint-intelligence/issues/120) F5.9 Onboarding wizard — 6-step modal
- [ ] [#121](https://github.com/deghosal-2026/sprint-intelligence/issues/121) F5.10 User guide — 4 tabs on admin page

### Bug Fixes
- [ ] [#122](https://github.com/deghosal-2026/sprint-intelligence/issues/122) B5.1 10-team data renders without performance degradation
- [ ] [#123](https://github.com/deghosal-2026/sprint-intelligence/issues/123) B5.2 10 team tabs: scrollable or dropdown

### Tests
- [ ] [#124](https://github.com/deghosal-2026/sprint-intelligence/issues/124) T5.1 Q&A: velocity question → data-backed answer
- [ ] [#125](https://github.com/deghosal-2026/sprint-intelligence/issues/125) T5.2 Q&A: overloaded engineer → correct name
- [ ] [#126](https://github.com/deghosal-2026/sprint-intelligence/issues/126) T5.3 Q&A: offline LLM → error message
- [ ] [#127](https://github.com/deghosal-2026/sprint-intelligence/issues/127) T5.4 Anomaly: >25% drop → alert fires
- [ ] [#128](https://github.com/deghosal-2026/sprint-intelligence/issues/128) T5.5 Health Score: known metrics → expected composite
- [ ] [#129](https://github.com/deghosal-2026/sprint-intelligence/issues/129) T5.6 Onboarding wizard completes in <30 mins

**Gate:** Q&A works for 5 test questions. Health score renders. ≥80% teams valid. → M6

---

## M6: Polish, Ecosystem, Self-Serve
**Issues: #130–#140** (11 issues)

### Features
- [ ] [#130](https://github.com/deghosal-2026/sprint-intelligence/issues/130) F6.1 Export-to-slide — download DORA + velocity charts as PNG/PDF
- [ ] [#131](https://github.com/deghosal-2026/sprint-intelligence/issues/131) F6.2 Trend forecasting stub — linear projection from 12-sprint trend
- [ ] [#132](https://github.com/deghosal-2026/sprint-intelligence/issues/132) F6.3 DeliveryOS integration stub — standardized metric JSON schema
- [ ] [#133](https://github.com/deghosal-2026/sprint-intelligence/issues/133) F6.4 Self-service onboarding — auto-detect repos + labels from config

### Bug Fixes
- [ ] [#134](https://github.com/deghosal-2026/sprint-intelligence/issues/134) B6.1 All edge cases from 10-team data run (nulls, missings, types)
- [ ] [#135](https://github.com/deghosal-2026/sprint-intelligence/issues/135) B6.2 Dashboard load ≤ 3s with 120 sprints of data

### Chores
- [ ] [#136](https://github.com/deghosal-2026/sprint-intelligence/issues/136) C6.1 README — setup, architecture, running guide
- [ ] [#137](https://github.com/deghosal-2026/sprint-intelligence/issues/137) C6.2 API documentation — all endpoints with request/response
- [ ] [#138](https://github.com/deghosal-2026/sprint-intelligence/issues/138) C6.3 User guide — 4 tabs complete with content
- [ ] [#139](https://github.com/deghosal-2026/sprint-intelligence/issues/139) C6.4 Code cleanup — linting, docstrings, dead code removal
- [ ] [#140](https://github.com/deghosal-2026/sprint-intelligence/issues/140) C6.5 Final test run — full seed → compute → validate all 10 ACs

**Gate:** All 10 ACs from spec Section 8.4 pass. Dashboard load < 3s.
