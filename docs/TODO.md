# SprintSense — TODO

**Status:** IMPLEMENTATION STARTED — June 27, 2026
**Spec:** `docs/spec.md`
**All issues:** `#13`–`#140` on GitHub

**Workflow:** Complete each issue's feature + tests + bugfixes before moving to the next within the milestone.

---

## M1: Data Foundation + SDM Core (1 Team)
**Issues: #13–#46** (34 issues: 10 chores, 19 features, 5 tests)

### Scaffolding ✅
- [x] [#13](https://github.com/deghosal-2026/sprint-intelligence/issues/13) C1.1 PostgreSQL schema + Alembic migrations
- [x] [#14](https://github.com/deghosal-2026/sprint-intelligence/issues/14) C1.2 Flask app skeleton + Dockerfile
- [x] [#15](https://github.com/deghosal-2026/sprint-intelligence/issues/15) C1.3 React app skeleton + Vite + Dockerfile
- [x] [#16](https://github.com/deghosal-2026/sprint-intelligence/issues/16) C1.4 Docker Compose setup (db + api + dashboard)
- [x] [#17](https://github.com/deghosal-2026/sprint-intelligence/issues/17) C1.5 .env template + gitignore
- [x] [#18](https://github.com/deghosal-2026/sprint-intelligence/issues/18) C1.6 tools/download_public_data.py
- [x] [#19](https://github.com/deghosal-2026/sprint-intelligence/issues/19) C1.7 tools/transform_test_data.py
- [x] [#20](https://github.com/deghosal-2026/sprint-intelligence/issues/20) C1.8 tools/seed_database.py
- [x] [#21](https://github.com/deghosal-2026/sprint-intelligence/issues/21) C1.9 Seed 2 test users (alex/sdm, priya/junior)
- [x] [#22](https://github.com/deghosal-2026/sprint-intelligence/issues/22) C1.10 Admin page UI + routing

### Features ✅
- [x] [#23](https://github.com/deghosal-2026/sprint-intelligence/issues/23) F1.1 sprintsense-config.json
- [x] [#24](https://github.com/deghosal-2026/sprint-intelligence/issues/24) F1.2 Config sync (GH → DB)
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

### Tests (pending)
- [ ] [#42](https://github.com/deghosal-2026/sprint-intelligence/issues/42) T1.1 Issues ingestion test
- [ ] [#43](https://github.com/deghosal-2026/sprint-intelligence/issues/43) T1.2 PR cycle time test
- [ ] [#44](https://github.com/deghosal-2026/sprint-intelligence/issues/44) T1.3 Sprint resolution test
- [ ] [#45](https://github.com/deghosal-2026/sprint-intelligence/issues/45) T1.4 Velocity test
- [ ] [#46](https://github.com/deghosal-2026/sprint-intelligence/issues/46) T1.5 Rate limiting test

**Gate:** All tests pass. → M2

---

## M2: AI Summaries + Risk Alerts + DORA
**Issues: #47–#75** (29 issues)

- [ ] [#47](https://github.com/deghosal-2026/sprint-intelligence/issues/47) F2.1 Ollama client
- [ ] [#48](https://github.com/deghosal-2026/sprint-intelligence/issues/48) F2.2 SDM summary prompt
- [ ] [#49](https://github.com/deghosal-2026/sprint-intelligence/issues/49) F2.3 AI summary generation
- [ ] [#50](https://github.com/deghosal-2026/sprint-intelligence/issues/50) F2.4 Summary card
- [ ] [#51](https://github.com/deghosal-2026/sprint-intelligence/issues/51) F2.5 Copy to clipboard
- [ ] [#52](https://github.com/deghosal-2026/sprint-intelligence/issues/52) F2.6 Stale PR alert
- [ ] [#53](https://github.com/deghosal-2026/sprint-intelligence/issues/53) F2.7 Overloaded engineer
- [ ] [#54](https://github.com/deghosal-2026/sprint-intelligence/issues/54) F2.8 Scope creep alert
- [ ] [#55](https://github.com/deghosal-2026/sprint-intelligence/issues/55) F2.9 Risk alerts card
- [ ] [#56](https://github.com/deghosal-2026/sprint-intelligence/issues/56) F2.10 Alert drill-down
- [ ] [#57](https://github.com/deghosal-2026/sprint-intelligence/issues/57) F2.11 Deploy events
- [ ] [#58](https://github.com/deghosal-2026/sprint-intelligence/issues/58) F2.12 PagerDuty incidents
- [ ] [#59](https://github.com/deghosal-2026/sprint-intelligence/issues/59) F2.13 DORA: deploy frequency
- [ ] [#60](https://github.com/deghosal-2026/sprint-intelligence/issues/60) F2.14 DORA: lead time
- [ ] [#61](https://github.com/deghosal-2026/sprint-intelligence/issues/61) F2.15 DORA: MTTR
- [ ] [#62](https://github.com/deghosal-2026/sprint-intelligence/issues/62) F2.16 DORA: change failure rate
- [ ] [#63](https://github.com/deghosal-2026/sprint-intelligence/issues/63) F2.17 DORA pulse card
- [ ] [#64](https://github.com/deghosal-2026/sprint-intelligence/issues/64) F2.18 Sprint planning capacity
- [ ] [#65](https://github.com/deghosal-2026/sprint-intelligence/issues/65) F2.19 Admin AI summary status
- [ ] [#66](https://github.com/deghosal-2026/sprint-intelligence/issues/66) B2.1 Empty repos
- [ ] [#67](https://github.com/deghosal-2026/sprint-intelligence/issues/67) B2.2 Orphaned PRs
- [ ] [#68](https://github.com/deghosal-2026/sprint-intelligence/issues/68) B2.3 Sprint selector order
- [ ] [#69](https://github.com/deghosal-2026/sprint-intelligence/issues/69) T2.1 AI summary data points
- [ ] [#70](https://github.com/deghosal-2026/sprint-intelligence/issues/70) T2.2 AI summary missing data
- [ ] [#71](https://github.com/deghosal-2026/sprint-intelligence/issues/71) T2.3 AI summary offline skip
- [ ] [#72](https://github.com/deghosal-2026/sprint-intelligence/issues/72) T2.4 Stale PR alert fires
- [ ] [#73](https://github.com/deghosal-2026/sprint-intelligence/issues/73) T2.5 Overloaded alert fires
- [ ] [#74](https://github.com/deghosal-2026/sprint-intelligence/issues/74) T2.6 Scope creep alert fires
- [ ] [#75](https://github.com/deghosal-2026/sprint-intelligence/issues/75) T2.7 DORA CFR correct

---

## M3–M6 (same format, pending)

**Summary:** Scaffolding + all M1 features complete. 30 issues closed (#13–#41). Tests + M2 remaining.
