# SprintSense — TODO

**Status:** PRD APPROVED — June 27, 2026
**Data source:** GitHub Issues, Projects, Milestones, PRs (6 repos)

---

## M1: Data Foundation + SDM Core (1 Team)
**Scope:** 1 repo, SDM only. Prove the data pipeline.

- [ ] GitHub API auth + polling setup (Issues, Projects, Milestones, PRs — 4-hour interval)
- [ ] Sprint detection: parse `sprint:YYYY-MM-DD` labels, Milestone 1:1 mapping, Project iterations
- [ ] Story point extraction: parse `points:1` through `points:13` labels
- [ ] Issue type extraction: parse `bug`, `feature`, `tech-debt`, `task` labels
- [ ] Compute velocity: planned vs. completed story points per sprint (3 sprints)
- [ ] Compute PR cycle time: first commit → merge (mean, median, P90)
- [ ] Compute bug regression: bugs introduced vs. bugs closed per sprint
- [ ] Compute capacity vs. actual: planned vs. delivered story points
- [ ] SDM dashboard: 4 metric cards + trend lines + 3-sprint history
- [ ] Engineer drill-down: per-engineer WIP, blocked issues, PR cycle time, velocity contribution
- [ ] Data validation: flag missing story points, inconsistent labels, API failures
- [ ] Synthetic test data pipeline (see testing strategy in PRD)

**Gate:** SDM uses dashboard for 2 consecutive Mondays. Pipeline stable. → M2

---

## M2: AI Summaries + Risk Alerts + DORA (1 Team)
**Scope:** Same 1 repo. Layer intelligence on proven data.

- [ ] AI executive summary: 5-bullet consequence-first, human review toggle in UI
- [ ] Risk alerts: stale PRs (>3 days), overloaded engineers (WIP >4), scope creep
- [ ] DORA metrics: deployment frequency, lead time, MTTR, change failure rate
- [ ] GitHub Actions deploy event ingestion
- [ ] PagerDuty incident event ingestion
- [ ] Sprint planning capacity estimate view

**Gate:** AI summary used in 2 weekly reports. Alerts <20% false positive. DORA trending. → M3

---

## M3: Engineer Self-Service Dashboards (1 Team)
**Scope:** Add ICs (Junior, Senior, Staff) to the pilot team.

- [ ] Junior engineer dashboard: personal PR cycle time, story points trend, WIP, AI nudge
- [ ] Senior engineer dashboard: personal + review/mentoring metrics + team aggregate
- [ ] Staff engineer dashboard: personal + cross-team cycle time + blocker patterns
- [ ] Persona-tuned default views (data open per D4, views role-aware)
- [ ] Onboarding flow: GitHub OAuth → repo selection → label mapping → first dashboard

**Gate:** ≥80% ICs check dashboard at least 1x/sprint. Zero surveillance complaints. → M4

---

## M4: Multi-Team + Senior SDM + Director Views
**Scope:** Add 2 more repos. Senior SDM and Director personas.

- [ ] Multi-repo data pipeline (3 repos, 3 teams)
- [ ] Senior SDM view: per-team dashboards, cross-team pattern detection, multi-team exec summary
- [ ] Director view: org-level DORA + quality + velocity, quarterly view, Director exec summary
- [ ] No team ranking views. No per-individual data for Director.

**Gate:** Senior SDM uses in 2 1:1s. Director presents to VP. → M5

---

## M5: Full Org Rollout
**Scope:** All 6 repos, all 5 teams. All personas.

- [ ] Remaining repos/teams onboarded
- [ ] Slack notifications: Monday morning summary, mid-sprint alerts
- [ ] Anomaly detection: "Velocity dropped 25% — unusual vs. 12-sprint baseline"
- [ ] Custom metric thresholds per team
- [ ] Delivery Health Score (composite for Director QBR)

**Gate:** ≥80% org adoption. 3+ months DORA data. → M6

---

## M6: Polish, Ecosystem, Self-Serve
**Scope:** Full org. Harden, integrate, hand off.

- [ ] DeliveryOS unified dashboard integration
- [ ] RetroMaster integration
- [ ] Export-to-slide for QBR
- [ ] Trend forecasting
- [ ] Self-service onboarding for new teams (<1 hour)
- [ ] Performance: dashboard load <3s with 12+ sprints of data
- [ ] Documentation: metric guides, 1:1/planning/retro usage guides, "what SprintSense is and isn't"

**Gate:** Default sprint health tool. Self-serve onboarding. Platform-ready.

---

*Derived from `docs/prd.md` Section 6 (Launch Phasing). Update checkboxes as milestones complete.*
