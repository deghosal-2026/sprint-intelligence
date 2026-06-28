# SprintSense — TODO

**Status:** SPEC APPROVED — June 27, 2026
**Data source:** GitHub Issues, Projects, Milestones, PRs (10 repos, 10 teams, 120 sprints)
**Spec:** `docs/spec.md`
**GH Issues:** `#1`–`#12` on GitHub

---

## M1: Data Foundation + SDM Core (1 Team)
**Scope:** 1 repo, SDM only. Prove the pipeline.
**Spec:** Sections 3, 4, 11
**Issues:** `#1`–`#6`, `#12`

- [ ] `#1` Project scaffolding (Docker, PostgreSQL, Flask, React, Alembic)
- [ ] `#12` Test data generation tools (download, transform, seed scripts)
- [ ] `#3` GitHub API client + config sync
- [ ] `#2` Data pipeline — Phase 1 fetch (issues, PRs, milestones)
- [ ] `#4` Sprint resolution + Phase 2 compute (metrics)
- [ ] `#5` SDM Dashboard — 4 metric cards + Recharts + engineer table
- [ ] `#6` Admin page — poller controls + system status

**Gate:** SDM dashboard loads 12 sprints of data. All 4 metric cards render. → M2

---

## M2: AI Summaries + Risk Alerts + DORA (1 Team)
**Scope:** Same 1 repo. Layer intelligence on proven data.
**Spec:** Sections 5, 7
**Issues:** `#7`, `#8`

- [ ] `#7` AI executive summary — 5-bullet consequence-first
- [ ] `#7` Risk alerts: stale PRs, overloaded engineers, scope creep
- [ ] `#7` DORA: deploy frequency, lead time, MTTR, change failure rate
- [ ] `#7` Sprint planning capacity estimate
- [ ] `#7` Deploy events (GitHub Actions) + incidents (PagerDuty) ingestion
- [ ] `#8` Bug fixes from M1

**Gate:** AI summary rendered for all sprints. 3 alert types firing. 4 DORA gauges. → M3

---

## M3: Engineer Self-Service Dashboards (1 Team)
**Scope:** Add IC personas (Junior, Senior, Staff) to pilot team.
**Spec:** Sections 6.2-6.3
**Issue:** `#9`

- [ ] `#9` Persona selector dropdown in top bar
- [ ] `#9` Junior engineer view: personal cycle time, story points, WIP, AI nudge
- [ ] `#9` Senior engineer view: personal + review metrics + team aggregate
- [ ] `#9` Staff engineer view: personal + cross-team cycle time + blockers
- [ ] `#9` Bug fixes from M1/M2

**Gate:** All 4 persona views render correctly. ≥80% adoption on pilot team. → M4

---

## M4: Multi-Team + Senior SDM + Director
**Scope:** Add 2 more repos. SrSDM and Director personas.
**Spec:** Sections 6.2-6.3
**Issue:** `#10`

- [ ] `#10` Multi-repo data pipeline (3 repos, 3 teams)
- [ ] `#10` Senior SDM view: per-team tabs, cross-team patterns, multi-team summary
- [ ] `#10` Director view: org-level DORA + quality + velocity + quarterly view
- [ ] `#10` Bug fixes from M1-M3

**Gate:** SrSDM sees 3 team tabs. Director sees org DORA. Cross-team pattern detected. → M5

---

## M5: Full Org Rollout + Sprint Q&A
**Scope:** All 10 repos, all 10 teams. All personas. Sprint Q&A.
**Spec:** Sections 5.3, 6.6, 8
**Issue:** `#11`

- [ ] `#11` Sprint Q&A text box in dashboard (POST /api/ask → Ollama)
- [ ] `#11` Full 10-team, 120-sprint data pipeline
- [ ] `#11` Anomaly detection: velocity drop >25% vs baseline
- [ ] `#11` Delivery Health Score (composite)
- [ ] `#11` Custom metric thresholds per team
- [ ] `#11` Onboarding wizard on admin page (6-step modal)
- [ ] `#11` User guide (4 tabs)
- [ ] `#11` Bug fixes from M4

**Gate:** Q&A works for 5 test questions. Health score renders. >80% teams valid. → M6

---

## M6: Polish, Ecosystem, Self-Serve
**Scope:** Harden, document, integrate stubs.
**Spec:** Section 10, 11, 12.6
**Issue:** `#11` (tracked within same epic)

- [ ] Export-to-slide: DORA + velocity charts as PNG/PDF
- [ ] Trend forecasting stub
- [ ] DeliveryOS integration stub (metric format standardization)
- [ ] Self-service onboarding: config → auto-detect repos + labels
- [ ] All edge cases handled from 10-team data run
- [ ] Dashboard load < 3s with 120 sprints
- [ ] README with full setup instructions
- [ ] API documentation
- [ ] Code cleanup, linting, docstrings

**Gate:** All 10 acceptance criteria from spec Section 8.4 pass. README clear.

---

*Derived from `docs/spec.md`. GitHub issues `#1`–`#12` track this work. Update checkboxes as milestones complete.*
