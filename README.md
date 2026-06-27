# sprint-intelligence

LLM-powered sprint analytics with DORA metrics — automated sprint health intelligence from structured engineering data.

## Problem

Sprints are run on gut feel — velocity, capacity, and risk are estimated without data. Reports take hours to compile from Jira, GitHub, and incident trackers. Engineers and EMs can't see real-time sprint health.

## What It Does

Every Monday, Sprint Intelligence generates:

- Current sprint velocity vs 3-sprint trend
- PRs stuck >3 days with blockers
- Bug regression rate
- Capacity vs actual output
- DORA metrics: deployment frequency, lead time, MTTR, change failure rate
- Executive summary — consequence-first, 5 bullet points — ready to paste into weekly reports

## Status

🔲 Seeding — project not started yet.

## Tech Stack (Planned)

- LLM: TBD (OMLX local or API)
- Data sources: Jira API, GitHub API, PagerDuty API
- Framework: Python
- Chunking/Retrieval: learnings from [oncall-rag](https://github.com/deghosal-2026/oncall-rag)

## License

MIT
