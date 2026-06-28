# SprintSense — TODO

**Status:** IMPLEMENTATION STARTED — June 27, 2026
**Spec:** `docs/spec.md`
**All issues:** `#13`–`#140` on GitHub (granular per spec feature/chore/test/bugfix)

**Workflow:** Complete each issue's feature + tests + bugfixes before moving to the next within the milestone.

---

## M1: Data Foundation + SDM Core (1 Team)
**Issues: #13–#46** (34 issues: 10 chores, 19 features, 5 tests)

### Scaffolding (Chores)
- [ ] [#13](https://github.com/deghosal-2026/sprint-intelligence/issues/13) C1.1 PostgreSQL schema + Alembic migrations
- [ ] [#14](https://github.com/deghosal-2026/sprint-intelligence/issues/14) C1.2 Flask app skeleton + Dockerfile
- [ ] [#15](https://github.com/deghosal-2026/sprint-intelligence/issues/15) C1.3 React app skeleton + Vite + Dockerfile
- [ ] [#16](https://github.com/deghosal-2026/sprint-intelligence/issues/16) C1.4 Docker Compose setup (db + api + dashboard)
- [ ] [#17](https://github.com/deghosal-2026/sprint-intelligence/issues/17) C1.5 .env template + gitignore
- [ ] [#18](https://github.com/deghosal-2026/sprint-intelligence/issues/18) C1.6 tools/download_public_data.py
- [ ] [#19](https://github.com/deghosal-2026/sprint-intelligence/issues/19) C1.7 tools/transform_test_data.py
- [ ] [#20](https://github.com/deghosal-2026/sprint-intelligence/issues/20) C1.8 tools/seed_database.py
- [ ] [#21](https://github.com/deghosal-2026/sprint-intelligence/issues/21) C1.9 Seed 2 test users (alex/sdm, priya/junior)
- [ ] [#22](https://github.com/deghosal-2026/sprint-intelligence/issues/22) C1.10 Admin page UI + routing

### Features → Tests → Bug Fixes
- [ ] [#23](https://github.com/deghosal-2026/sprint-intelligence/issues/23) F1.1 sprintsense-config.json
- [ ] [#24](https://github.com/deghosal-2026/sprint-intelligence/issues/24) F1.2 Config sync (GH → DB)
- [ ] [#25](https://github.com/deghosal-2026/sprint-intelligence/issues/25) F1.3 GitHub Issues ingestion → [#42](https://github.com/deghosal-2026/sprint-intelligence/issues/42) T1.1
- [ ] [#26](https://github.com/deghosal-2026/sprint-intelligence/issues/26) F1.4 GitHub PRs + commits → [#43](https://github.com/deghosal-2026/sprint-intelligence/issues/43) T1.2
- [ ] [#27](https://github.com/deghosal-2026/sprint-intelligence/issues/27) F1.5 Milestones ingestion
- [ ] [#28](https://github.com/deghosal-2026/sprint-intelligence/issues/28) F1.6 Rate limiting
- [ ] [#29](https://github.com/deghosal-2026/sprint-intelligence/issues/29) F1.7 Phase 1 Fetch endpoint
- [ ] [#30](https://github.com/deghosal-2026/sprint-intelligence/issues/30) F1.8 Sprint resolution → [#44](https://github.com/deghosal-2026/sprint-intelligence/issues/44) T1.3
- [ ] [#31](https://github.com/deghosal-2026/sprint-intelligence/issues/31) F1.9 Velocity computation → [#45](https://github.com/deghosal-2026/sprint-intelligence/issues/45) T1.4
- [ ] [#32](https://github.com/deghosal-2026/sprint-intelligence/issues/32) F1.10 PR cycle time computation
- [ ] [#33](https://github.com/deghosal-2026/sprint-intelligence/issues/33) F1.11 Bug regression computation
- [ ] [#34](https://github.com/deghosal-2026/sprint-intelligence/issues/34) F1.12 Capacity vs actual computation
- [ ] [#35](https://github.com/deghosal-2026/sprint-intelligence/issues/35) F1.13 SDM dashboard (4 metric cards + Recharts)
- [ ] [#36](https://github.com/deghosal-2026/sprint-intelligence/issues/36) F1.14 Sprint selector dropdown
- [ ] [#37](https://github.com/deghosal-2026/sprint-intelligence/issues/37) F1.15 Engineer drill-down table
- [ ] [#38](https://github.com/deghosal-2026/sprint-intelligence/issues/38) F1.16 Phase 2 Compute endpoint
- [ ] [#39](https://github.com/deghosal-2026/sprint-intelligence/issues/39) F1.17 Full poll endpoint
- [ ] [#40](https://github.com/deghosal-2026/sprint-intelligence/issues/40) F1.18 Admin poller controls
- [ ] [#41](https://github.com/deghosal-2026/sprint-intelligence/issues/41) F1.19 Admin system status
- [ ] [#42](https://github.com/deghosal-2026/sprint-intelligence/issues/42) T1.1 Issues ingestion test
- [ ] [#43](https://github.com/deghosal-2026/sprint-intelligence/issues/43) T1.2 PR cycle time test
- [ ] [#44](https://github.com/deghosal-2026/sprint-intelligence/issues/44) T1.3 Sprint resolution test
- [ ] [#45](https://github.com/deghosal-2026/sprint-intelligence/issues/45) T1.4 Velocity test
- [ ] [#46](https://github.com/deghosal-2026/sprint-intelligence/issues/46) T1.5 Rate limiting test

---

## M2: AI Summaries + Risk Alerts + DORA
**Issues: #47–#75** (29 issues: 19 features, 3 bugs, 7 tests)

- [ ] [#47](https://github.com/deghosal-2026/sprint-intelligence/issues/47) F2.1 Ollama client
- [ ] [#48](https://github.com/deghosal-2026/sprint-intelligence/issues/48) F2.2 SDM summary prompt template
- [ ] [#49](https://github.com/deghosal-2026/sprint-intelligence/issues/49) F2.3 AI summary generation (Phase 2)
- [ ] [#50](https://github.com/deghosal-2026/sprint-intelligence/issues/50) F2.4 Summary card in dashboard
- [ ] [#51](https://github.com/deghosal-2026/sprint-intelligence/issues/51) F2.5 Copy to clipboard button
- [ ] [#52](https://github.com/deghosal-2026/sprint-intelligence/issues/52) F2.6 Stale PR alert
- [ ] [#53](https://github.com/deghosal-2026/sprint-intelligence/issues/53) F2.7 Overloaded engineer alert
- [ ] [#54](https://github.com/deghosal-2026/sprint-intelligence/issues/54) F2.8 Scope creep alert
- [ ] [#55](https://github.com/deghosal-2026/sprint-intelligence/issues/55) F2.9 Risk alerts card
- [ ] [#56](https://github.com/deghosal-2026/sprint-intelligence/issues/56) F2.10 Alert drill-down
- [ ] [#57](https://github.com/deghosal-2026/sprint-intelligence/issues/57) F2.11 Deploy events ingestion (GH Actions)
- [ ] [#58](https://github.com/deghosal-2026/sprint-intelligence/issues/58) F2.12 PagerDuty incidents ingestion
- [ ] [#59](https://github.com/deghosal-2026/sprint-intelligence/issues/59) F2.13 DORA: deploy frequency
- [ ] [#60](https://github.com/deghosal-2026/sprint-intelligence/issues/60) F2.14 DORA: lead time
- [ ] [#61](https://github.com/deghosal-2026/sprint-intelligence/issues/61) F2.15 DORA: MTTR
- [ ] [#62](https://github.com/deghosal-2026/sprint-intelligence/issues/62) F2.16 DORA: change failure rate
- [ ] [#63](https://github.com/deghosal-2026/sprint-intelligence/issues/63) F2.17 DORA pulse card (4 mini gauges)
- [ ] [#64](https://github.com/deghosal-2026/sprint-intelligence/issues/64) F2.18 Sprint planning capacity view
- [ ] [#65](https://github.com/deghosal-2026/sprint-intelligence/issues/65) F2.19 Admin AI summary status
- [ ] [#66](https://github.com/deghosal-2026/sprint-intelligence/issues/66) B2.1 Handle empty repos gracefully
- [ ] [#67](https://github.com/deghosal-2026/sprint-intelligence/issues/67) B2.2 Handle orphaned PRs
- [ ] [#68](https://github.com/deghosal-2026/sprint-intelligence/issues/68) B2.3 Sprint selector chronological ordering
- [ ] [#69](https://github.com/deghosal-2026/sprint-intelligence/issues/69) T2.1 AI summary data points
- [ ] [#70](https://github.com/deghosal-2026/sprint-intelligence/issues/70) T2.2 AI summary missing data
- [ ] [#71](https://github.com/deghosal-2026/sprint-intelligence/issues/71) T2.3 AI summary offline skip
- [ ] [#72](https://github.com/deghosal-2026/sprint-intelligence/issues/72) T2.4 Stale PR alert fires
- [ ] [#73](https://github.com/deghosal-2026/sprint-intelligence/issues/73) T2.5 Overloaded alert fires
- [ ] [#74](https://github.com/deghosal-2026/sprint-intelligence/issues/74) T2.6 Scope creep alert fires
- [ ] [#75](https://github.com/deghosal-2026/sprint-intelligence/issues/75) T2.7 DORA CFR correct

---

## M3: Engineer Self-Service Dashboards
**Issues: #76–#92** (17 issues: 10 features, 3 bugs, 4 tests)

- [ ] [#76](https://github.com/deghosal-2026/sprint-intelligence/issues/76) F3.1 Persona selector dropdown
- [ ] [#77](https://github.com/deghosal-2026/sprint-intelligence/issues/77) F3.2 Junior engineer view
- [ ] [#78](https://github.com/deghosal-2026/sprint-intelligence/issues/78) F3.3 Junior engineer AI nudge
- [ ] [#79](https://github.com/deghosal-2026/sprint-intelligence/issues/79) F3.4 Senior engineer view
- [ ] [#80](https://github.com/deghosal-2026/sprint-intelligence/issues/80) F3.5 Staff engineer view
- [ ] [#81](https://github.com/deghosal-2026/sprint-intelligence/issues/81) F3.6 Engineer sprint metrics
- [ ] [#82](https://github.com/deghosal-2026/sprint-intelligence/issues/82) F3.7 Review metrics
- [ ] [#83](https://github.com/deghosal-2026/sprint-intelligence/issues/83) F3.8 Blocked issue detection
- [ ] [#84](https://github.com/deghosal-2026/sprint-intelligence/issues/84) F3.9 Persona-tuned card visibility
- [ ] [#85](https://github.com/deghosal-2026/sprint-intelligence/issues/85) F3.10 Adaptive metric cards
- [ ] [#86](https://github.com/deghosal-2026/sprint-intelligence/issues/86) B3.1 Correct team metrics
- [ ] [#87](https://github.com/deghosal-2026/sprint-intelligence/issues/87) B3.2 Engineer table sprint filter
- [ ] [#88](https://github.com/deghosal-2026/sprint-intelligence/issues/88) B3.3 Alerts scoped to sprint
- [ ] [#89](https://github.com/deghosal-2026/sprint-intelligence/issues/89) T3.1 Junior personal cards only
- [ ] [#90](https://github.com/deghosal-2026/sprint-intelligence/issues/90) T3.2 Senior team aggregate
- [ ] [#91](https://github.com/deghosal-2026/sprint-intelligence/issues/91) T3.3 Staff cycle time comparison
- [ ] [#92](https://github.com/deghosal-2026/sprint-intelligence/issues/92) T3.4 Persona toggle switches cards

---

## M4: Multi-Team + Senior SDM + Director
**Issues: #93–#111** (19 issues: 11 features, 3 bugs, 5 tests)

- [ ] [#93](https://github.com/deghosal-2026/sprint-intelligence/issues/93) F4.1 Multi-repo pipeline
- [ ] [#94](https://github.com/deghosal-2026/sprint-intelligence/issues/94) F4.2 Multi-repo Phase 1 + 2
- [ ] [#95](https://github.com/deghosal-2026/sprint-intelligence/issues/95) F4.3 Senior SDM per-team tabs
- [ ] [#96](https://github.com/deghosal-2026/sprint-intelligence/issues/96) F4.4 Cross-team pattern detection
- [ ] [#97](https://github.com/deghosal-2026/sprint-intelligence/issues/97) F4.5 SrSDM AI summary
- [ ] [#98](https://github.com/deghosal-2026/sprint-intelligence/issues/98) F4.6 Director view
- [ ] [#99](https://github.com/deghosal-2026/sprint-intelligence/issues/99) F4.7 Director AI summary
- [ ] [#100](https://github.com/deghosal-2026/sprint-intelligence/issues/100) F4.8 Quarterly view
- [ ] [#101](https://github.com/deghosal-2026/sprint-intelligence/issues/101) F4.9 Director summary card
- [ ] [#102](https://github.com/deghosal-2026/sprint-intelligence/issues/102) F4.10 No team ranking
- [ ] [#103](https://github.com/deghosal-2026/sprint-intelligence/issues/103) F4.11 No per-engineer for Director
- [ ] [#104](https://github.com/deghosal-2026/sprint-intelligence/issues/104) B4.1 Engineer metrics per team
- [ ] [#105](https://github.com/deghosal-2026/sprint-intelligence/issues/105) B4.2 Cross-team cycle time
- [ ] [#106](https://github.com/deghosal-2026/sprint-intelligence/issues/106) B4.3 DORA per team
- [ ] [#107](https://github.com/deghosal-2026/sprint-intelligence/issues/107) T4.1 SrSDM tabs no ranking
- [ ] [#108](https://github.com/deghosal-2026/sprint-intelligence/issues/108) T4.2 Cross-team slowdown
- [ ] [#109](https://github.com/deghosal-2026/sprint-intelligence/issues/109) T4.3 Director aggregate only
- [ ] [#110](https://github.com/deghosal-2026/sprint-intelligence/issues/110) T4.4 Quarterly 12 sprints
- [ ] [#111](https://github.com/deghosal-2026/sprint-intelligence/issues/111) T4.5 Director QoQ summary

---

## M5: Full Org Rollout + Sprint Q&A
**Issues: #112–#129** (18 issues: 10 features, 2 bugs, 6 tests)

- [ ] [#112](https://github.com/deghosal-2026/sprint-intelligence/issues/112) F5.1 Full 10-team pipeline
- [ ] [#113](https://github.com/deghosal-2026/sprint-intelligence/issues/113) F5.2 120 sprints computed
- [ ] [#114](https://github.com/deghosal-2026/sprint-intelligence/issues/114) F5.3 Sprint Q&A text box
- [ ] [#115](https://github.com/deghosal-2026/sprint-intelligence/issues/115) F5.4 Sprint Q&A API endpoint
- [ ] [#116](https://github.com/deghosal-2026/sprint-intelligence/issues/116) F5.5 Sprint Q&A Ollama integration
- [ ] [#117](https://github.com/deghosal-2026/sprint-intelligence/issues/117) F5.6 Anomaly detection
- [ ] [#118](https://github.com/deghosal-2026/sprint-intelligence/issues/118) F5.7 Delivery Health Score
- [ ] [#119](https://github.com/deghosal-2026/sprint-intelligence/issues/119) F5.8 Custom metric thresholds
- [ ] [#120](https://github.com/deghosal-2026/sprint-intelligence/issues/120) F5.9 Onboarding wizard (6-step)
- [ ] [#121](https://github.com/deghosal-2026/sprint-intelligence/issues/121) F5.10 User guide (4 tabs)
- [ ] [#122](https://github.com/deghosal-2026/sprint-intelligence/issues/122) B5.1 10-team performance
- [ ] [#123](https://github.com/deghosal-2026/sprint-intelligence/issues/123) B5.2 10 team tabs UI
- [ ] [#124](https://github.com/deghosal-2026/sprint-intelligence/issues/124) T5.1 Q&A velocity answer
- [ ] [#125](https://github.com/deghosal-2026/sprint-intelligence/issues/125) T5.2 Q&A overloaded engineer
- [ ] [#126](https://github.com/deghosal-2026/sprint-intelligence/issues/126) T5.3 Q&A offline LLM
- [ ] [#127](https://github.com/deghosal-2026/sprint-intelligence/issues/127) T5.4 Anomaly alert fires
- [ ] [#128](https://github.com/deghosal-2026/sprint-intelligence/issues/128) T5.5 Health Score correct
- [ ] [#129](https://github.com/deghosal-2026/sprint-intelligence/issues/129) T5.6 Onboarding <30 min

---

## M6: Polish, Ecosystem, Self-Serve
**Issues: #130–#140** (11 issues: 4 features, 2 bugs, 5 chores)

- [ ] [#130](https://github.com/deghosal-2026/sprint-intelligence/issues/130) F6.1 Export-to-slide
- [ ] [#131](https://github.com/deghosal-2026/sprint-intelligence/issues/131) F6.2 Trend forecasting stub
- [ ] [#132](https://github.com/deghosal-2026/sprint-intelligence/issues/132) F6.3 DeliveryOS integration stub
- [ ] [#133](https://github.com/deghosal-2026/sprint-intelligence/issues/133) F6.4 Self-service onboarding
- [ ] [#134](https://github.com/deghosal-2026/sprint-intelligence/issues/134) B6.1 All edge cases
- [ ] [#135](https://github.com/deghosal-2026/sprint-intelligence/issues/135) B6.2 Dashboard load ≤3s
- [ ] [#136](https://github.com/deghosal-2026/sprint-intelligence/issues/136) C6.1 README
- [ ] [#137](https://github.com/deghosal-2026/sprint-intelligence/issues/137) C6.2 API documentation
- [ ] [#138](https://github.com/deghosal-2026/sprint-intelligence/issues/138) C6.3 User guide complete
- [ ] [#139](https://github.com/deghosal-2026/sprint-intelligence/issues/139) C6.4 Code cleanup
- [ ] [#140](https://github.com/deghosal-2026/sprint-intelligence/issues/140) C6.5 Final test run

---

**Summary:** 128 total issues (#13–#140) across 6 milestones. Each issue maps to a spec Section. Features link to their corresponding tests and bug fixes.
