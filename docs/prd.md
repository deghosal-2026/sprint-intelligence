# SprintSense — PRD v1

**Status:** APPROVED
**Type:** Individual learning project — building AI-native sprint intelligence from scratch
**Scope:** 1 engineering org — up to 25 ICs, 5 SDMs, 5 Directors, 6 GitHub repos (Issues + PRs)
**Data sources:** GitHub Issues (Projects, Milestones, labels for sprint tracking + story points + issue types), GitHub PRs (cycle time, reviews), GitHub Actions (deploy events), PagerDuty (incidents)
**Date:** June 2026

---

## 1. Executive Summary

### The Problem (WHY)

Everyone in an engineering org — from a junior IC trying to understand their own velocity to a Director justifying headcount — relies on gut feel, fragmented dashboards, and manually compiled reports. There is no single source of truth for sprint execution. No measurement baseline. No trends. No automated risk signals.

An SDM spends 4 hours every Monday compiling sprint reports. A Director can't quote their org's DORA numbers. A junior engineer has no visibility into their own delivery patterns. A staff engineer can't see cross-team bottlenecks. The org ships, but nobody knows — with data — whether it's getting better or worse.

### The Solution (WHAT)

SprintSense is an AI sprint intelligence layer for the entire engineering org. It pulls data from GitHub Issues, Projects, Milestones, and PRs, computes sprint velocity, PR cycle time, bug regression, capacity vs. actual, and DORA metrics. It generates consequence-first AI summaries tuned to each persona's level. It detects risks — stale PRs, overloaded engineers, scope creep — and surfaces them to the right people.

Every persona sees what they need, and nothing they don't. A junior engineer sees their own growth — not their peers' velocity. A Director sees org-level trends — not individual engineer data. The tool scales coaching upward and self-awareness downward.

### The Pitch (10 seconds)

> "Junior engineers track their own growth. SDMs get their Monday mornings back. Directors have org-level DORA at their fingertips. One tool. Every level. No gut feelings."

---

## 2. Problem Deep-Dive

### 2.1 Current State (Without SprintSense)

| Task | Today | With SprintSense |
|---|---|---|
| SDM compiles sprint velocity + quality data | 4 hours/manual | <15 min automated |
| Director asks for DORA metrics | Weeks to compile, if at all | Dashboard, always current |
| Junior engineer understands own delivery patterns | Nothing — no feedback loop | Personal trend dashboard |
| Staff engineer identifies cross-team bottlenecks | Anecdotal, slow to surface | Cross-team cycle time + blocker patterns |
| Senior SDM compares health across teams | Spreadsheets, inconsistent | Per-team dashboards, no side-by-side ranking |
| Org proves delivery improvement | Can't — no baseline | 12+ weeks of trended DORA |

### 2.2 The "So What"

- **No measurement baseline** → cannot prove improvement, justify investment, or benchmark.
- **Gut-feel management doesn't scale** → an SDM managing 5 engineers can feel the pulse. An SDM managing 15+ or a Director overseeing 5 SDMs cannot.
- **Engineers have zero self-service delivery visibility** → junior ICs don't know if they're improving. Seniors don't see their bottlenecks. Staff don't see cross-team friction.
- **Reactive, not proactive** → risks surface at retro or postmortem, not mid-sprint when they're fixable.
- **Builder time lost** → 4 hours/week of report compilation per SDM is time not spent coaching, designing, or building.

### 2.3 Why This Matters to the Organization

- **DORA visibility** → most Directors can't quote their org's DORA numbers. SprintSense makes this baseline trivial.
- **AI-native management proof point** → SprintSense demonstrates that AI + structured data materially improves engineering leadership — not a slide deck, a working system.
- **Roadmap dependency** → SprintSense is a prerequisite for DeliveryOS (Stage 3 unified platform) and a required proof point for the AI-Powered Director career roadmap.
- **Engineer retention through growth visibility** → engineers who can see their own improvement stay longer.

---

## 3. User Personas

### 3.1 Junior Engineer (IC1-IC2)

**Name:** Priya
**Experience:** 0-3 years
**Context:** Completing well-scoped tickets. Learning the codebase, the team's pace, and what "good" looks like.

**Pain points:**
- No feedback loop on delivery speed — am I getting faster?
- Doesn't know if her PR cycle time is normal or slow
- No visibility into her own WIP patterns (is she context-switching too much?)
- Relies on manager's 1:1 feedback for all delivery signals (slow, sparse)

**What SprintSense gives her:**
- Her own PR cycle time trend (last 3 sprints) — "you're getting 15% faster"
- Her completed story points per sprint — trended, not compared to peers
- Her WIP count — with a gentle nudge if she's juggling too many tickets
- No access to anyone else's data. Period.

**Behaviors:**
- Checks personal dashboard once per sprint (~5 min)
- Reviews before 1:1 with SDM — comes prepared with her own data
- Uses PR cycle time trend as a personal growth metric

---

### 3.2 Senior Engineer (IC3-IC4)

**Name:** Marcus
**Experience:** 4-8 years
**Context:** Leading features. Mentoring juniors. Owns service areas. Expected to unblock himself and others.

**Pain points:**
- Can't quantify his impact — "I know I delivered a lot, but what does the data say?"
- PRs he reviews sometimes sit — is he a review bottleneck?
- Wants to mentor juniors with data, not just opinions
- Needs to see team-level patterns to understand where to focus his effort

**What SprintSense gives him:**
- His own metrics (same as Priya's view, plus review metrics: PRs reviewed, review turnaround time)
- Team-level aggregated metrics (velocity trend, bug rate, cycle time) — for context, not comparison
- His review impact: "You reviewed 8 PRs this sprint, avg turnaround 4 hours"
- No access to other engineers' individual data

**Behaviors:**
- Checks personal dashboard before sprint planning (~10 min)
- Uses team-level metrics to flag delivery risks during standup
- References his review metrics in promo packet / performance conversations

---

### 3.3 Staff Engineer (IC5+)

**Name:** Jordan
**Experience:** 8+ years
**Context:** Cross-team architecture. Unblocking teams. Setting technical direction. Expected to see patterns others miss.

**Pain points:**
- Cross-team delivery friction is invisible until it becomes a crisis
- Can't quantify "organizational drag" — where does work stall between teams?
- Needs data to justify architectural investment ("this service is the bottleneck — here's the data")
- Spends time in too many repos/boards with no unified view

**What SprintSense gives him:**
- His own metrics (same as senior view)
- Cross-team PR cycle time patterns — which repos are slowest? Which inter-team dependencies stall?
- Blocker patterns across teams — what's getting stuck, where, and for how long?
- No access to other individuals' data. Sees repo-level and team-level aggregates only.

**Behaviors:**
- Checks cross-team view weekly (~15 min)
- Uses blocker data to prioritize technical debt and architectural improvements
- Presents cycle-time trends to justify infra/platform investments

---

### 3.4 Software Development Manager (SDM)

**Name:** Alex
**Context:** Manages 4-6 engineers. Accountable for team delivery, quality, and engineer growth. Reports upward to Senior SDM or Director.

**Pain points:**
- Spends 4 hours every Monday compiling sprint reports from GitHub Issues, Projects, and PRs
- Can't quantify team improvement over time — "I feel like we're getting faster, but I can't prove it"
- Relies on standup + 1:1 signals for risk detection (slow, inconsistent, misses things)
- Needs to present sprint health to leadership with data, not anecdotes
- Wants to coach engineers with data, not just memory

**What SprintSense gives him:**
- Full team dashboard: velocity trend, PR cycle time (mean/median/P90), bug regression, capacity vs. actual
- 5-bullet AI executive summary — consequence-first, paste-ready for weekly report
- Risk alerts: stale PRs, overloaded engineers, scope creep
- Per-engineer drill-down (for his team only): WIP, blocked tickets, PR cycle time, velocity contribution
- Sprint planning input: capacity estimate based on historical velocity + team composition
- DORA metrics trended across sprints

**Behaviors:**
- Primary dashboard: Monday morning review (~15 min)
- Mid-sprint pulse check: 2-3x per sprint (~5 min each)
- Uses engineer drill-downs to prepare for 1:1s
- Copies AI executive summary into weekly leadership report (after human review)
- Uses data in sprint planning and retro to ground conversations

---

### 3.5 Senior Software Development Manager (Senior SDM)

**Name:** Sarah
**Context:** Manages 2-4 SDMs (each with their own team). Accountable for multi-team delivery, resource allocation, and cross-team coordination. Reports to Director.

**Pain points:**
- Manages through SDM reports — secondhand information, inconsistent formats
- Each SDM reports differently: different metrics, different narratives, different levels of detail
- Can't see cross-team patterns: which team is struggling, where are the systemic bottlenecks?
- Needs to allocate resources (people, focus) across teams with data, not politics
- Needs to present consolidated multi-team health to Director

**What SprintSense gives her:**
- Per-team dashboards — separate views for each SDM's team (no side-by-side ranking)
- Cross-team pattern detection: "Teams A and C both saw PR cycle time increases this sprint — correlated with shared dependency on Repo X"
- Aggregate org-level metrics (not per-individual, not per-team comparisons)
- AI executive summary at her level: multi-team trends, systemic risks, resource allocation signals
- No access to individual engineer data outside her direct span

**Behaviors:**
- Checks per-team dashboards weekly (~20 min)
- Uses cross-team patterns in SDM 1:1s — "I noticed your team's cycle time trended up. What's going on?"
- Uses aggregate data for Director-level reporting
- Uses resource signals to make staffing and allocation decisions

---

### 3.6 Director of Engineering

**Name:** David
**Context:** Oversees 3-5 SDMs/Senior SDMs (~20-25 engineers). Accountable for org-level delivery, quality, budget, hiring, and strategy. Reports to VP.

**Pain points:**
- Can't quote his org's DORA metrics — no measurement infrastructure exists
- Receives inconsistent, narrative-heavy reports from SDMs — no apples-to-apples view
- Can't answer "are we getting better?" with data
- Needs to justify headcount, tooling budget, and platform investments with delivery data
- Wants to identify systemic issues (not individual or team-level) to address at org level

**What SprintSense gives him:**
- Org-level aggregate dashboard: DORA metrics, velocity trends, quality trends — all aggregated across teams
- No per-team comparisons. No per-individual data. Aggregate only.
- AI executive summary at Director level: "Org DORA: deploy frequency up 12%. MTTR flat. Change failure rate down 8%. Lead time improving. Risk: 2 teams showed scope creep >20% this quarter."
- Trend data over quarters, not just sprints

**Behaviors:**
- Checks org dashboard bi-weekly or monthly (~10 min)
- Uses DORA trends in VP/stakeholder presentations
- Uses quality trend data to justify platform/infra investment
- Uses delivery trends for hiring and budget decisions
- Never sees individual engineer data — this is a hard constraint

---

### 3.7 Anti-Personas (Who SprintSense is NOT for)

- **HR / Performance Review committees** → SprintSense is a coaching tool, not an evaluation tool. Metrics never feed into HR systems.
- **Team-vs-team comparators** → SprintSense never displays side-by-side velocity comparisons. Aggregate = yes. Ranking = no.
- **Project managers tracking individual ticket completion** → That's what GitHub Issues/Projects is for. SprintSense analyzes sprint-level patterns.
- **External stakeholders** → Sprint data stays inside the engineering org. No customer-facing dashboards. No public benchmarks.

---

## 4. User Journeys

### 4.1 Junior Engineer: Understanding My Own Growth

**Actor:** Priya (Junior Engineer)
**Frequency:** Once per sprint, before 1:1
**Goal:** See her delivery trends and come to 1:1s prepared with data

| Step | Action | SprintSense Behavior |
|---|---|---|
| 1 | Priya opens SprintSense | Authenticated. Sees ONLY her personal dashboard. |
| 2 | Sees "Your Sprint Summary" | Completed 8 story points. PR cycle time: 2.1 days avg (↓11% vs last sprint). WIP count: 2 (healthy). |
| 3 | Sees "Your Trends" | PR cycle time trending down over 3 sprints (3.1 → 2.6 → 2.1 days). Story points trending up (5 → 6 → 8). |
| 4 | Reads AI insight card | "You're getting faster: PR cycle time improved 11% this sprint. Your WIP is steady at 1-2 tickets — no context-switching detected. One nudge: your PRs get first review after 8 hours on average. Consider pinging reviewers sooner." |
| 5 | Comes to 1:1 with SDM | "My PR cycle time improved again — down to 2.1 days. But I noticed first reviews take 8 hours. Any tips on getting faster reviews?" |

**Success:** Priya has data-driven self-awareness. The SDM spends 1:1 time on coaching, not data gathering.

---

### 4.2 Senior Engineer: Quantifying My Impact

**Actor:** Marcus (Senior Engineer)
**Frequency:** Once per sprint + before promo conversations
**Goal:** See his delivery and mentoring impact with data

| Step | Action | SprintSense Behavior |
|---|---|---|
| 1 | Marcus opens SprintSense | Sees personal dashboard + team aggregate (no individual peer data). |
| 2 | Sees his delivery metrics | Completed 13 story points. PR cycle time: 1.4 days. Bugs introduced: 1. |
| 3 | Sees his review/mentoring metrics | Reviewed 11 PRs this sprint. Avg review turnaround: 3.2 hours (top quartile). PRs from juniors he mentored: cycle time improved 18%. |
| 4 | Sees team aggregate for context | Team velocity: 42 pts. Bug rate: 3 introduced, 4 closed (net +1, watchful). |
| 5 | Uses data in performance conversation | "I delivered 13 pts with 1.4 day cycle time. Reviewed 11 PRs with 3.2 hour turnaround. Junior engineers I mentor have 18% faster cycle times." |

**Success:** Marcus has quantified impact. Mentoring contributions are visible. Promo packet gets harder data.

**The core insight:** Senior engineers are expected to lead features, mentor juniors, and unblock teams — but they have no way to quantify any of it. Their promo packet relies on anecdotes and LinkedIn-style bullet points ("Led the migration to..."). A senior who reviews 11 PRs with 3-hour turnaround is invisible to the system. A senior whose mentoring makes juniors 18% faster has no data to show for it. Their value is felt, not measured.

**What SprintSense changes:** It surfaces the invisible work. Review turnaround time. Number of PRs reviewed. The downstream impact of their mentoring (junior cycle time improvement). Bug count — not to penalize, but to show: "I shipped 13 points with 1 bug, and my code is clean." These are evidence points for promo committees that have never existed before. The team aggregate view gives context without comparison — "my 13 points means something because the team delivered 42."

**The behavioral shift:** The senior comes to performance conversations with a portfolio, not a list of projects. "Here's what I built, here's my quality, here's my mentoring impact — with data." The SDM doesn't need to reconstruct the senior's impact from memory. The senior advocates for themselves with evidence.

**The constraint:** Seniors see team aggregate but never individual peer data. They can't rank themselves against teammates. The tool coaches, it doesn't compete.

---

### 4.3 Staff Engineer: Finding Cross-Team Bottlenecks

**Actor:** Jordan (Staff Engineer)
**Frequency:** Weekly
**Goal:** Identify systemic delivery friction across teams and repos

| Step | Action | SprintSense Behavior |
|---|---|---|
| 1 | Jordan opens SprintSense | Sees personal dashboard + cross-team view. |
| 2 | Reviews "Cross-Team Cycle Time" | Repo A: PR cycle time 1.2 days. Repo B: 3.8 days (↑22%). Repo C: 1.5 days. |
| 3 | Drills into Repo B | Sees: avg time-to-first-review on Repo B is 18 hours (vs. 4 hours on other repos). Reviewers on Repo B are overloaded. |
| 4 | Reviews "Blocker Patterns" | 4 tickets blocked this sprint, all blocked on Repo B's service. Blocked tickets average 5.2 days in blocked state. |
| 5 | Takes action | Jordan raises in architecture sync: "Repo B is the bottleneck. PR reviews take 18 hours, 4 tickets blocked on that service. I'm proposing we split that service or add reviewers." |

**Success:** Jordan found a systemic bottleneck with data, not anecdotes. Architectural investment is justified with delivery metrics.

**The core insight:** A staff engineer's job is to see patterns others miss. But today, cross-team delivery friction is invisible. They know Repo B "feels slow" but can't prove it. They suspect a service is a bottleneck but can't quantify how many tickets are blocked on it, or for how long. Without data, architectural investment proposals are opinion contests — "I think we should split this service" vs. "I think it's fine." The staff engineer loses.

**What SprintSense changes:** It makes organizational drag visible. Cross-team PR cycle time by repo — which repos are slowest? Blocker patterns — how many tickets are stuck, on what, for how long? Time-to-first-review by repo — is the bottleneck review capacity or code complexity? The staff engineer can say: "Repo B PR reviews take 18 hours vs. 4 hours elsewhere. Four tickets are blocked on that service, averaging 5 days stuck. This is a measurable bottleneck. Here's the data. Here's the proposal."

**The behavioral shift:** The staff engineer shifts from "I have a hunch" to "here's the evidence." Their architectural influence increases because their arguments are grounded. They spend less time building consensus through persuasion and more time letting data do the convincing. Their weekly review of SprintSense becomes a proactive scan for systemic friction — not a fire drill when something breaks.

**The constraint:** Staff engineers see repo-level and team-level aggregates, never individual engineer data outside their own. They identify systemic patterns, not individual blame. The question is always "what's slow?" not "who's slow?"

---

### 4.4 SDM: Monday Morning Sprint Review

**Actor:** Alex (SDM)
**Frequency:** Every Monday, start of sprint
**Goal:** Understand team sprint health in <15 min, get exec summary ready

| Step | Action | SprintSense Behavior |
|---|---|---|
| 1 | Alex opens SprintSense | Authenticated. Team dashboard loaded with last 3 sprints. |
| 2 | Dashboard renders | Velocity trend (planned vs actual, 3-sprint), PR cycle time (mean/median/P90), bug regression, capacity vs. actual, DORA pulse. |
| 3 | Alex reads "Executive Summary" | 5-bullet AI summary: "1. Velocity up 8% vs 3-sprint avg. 2. PR cycle time flat — no improvement. 3. Bug regression rate up — 5 bugs introduced vs 3 avg. 4. Engineer X overloaded — 5 concurrent tickets, 2 stale PRs. 5. Action: discuss quality in retro, rebalance Engineer X's load." |
| 4 | Alex scans "Risk Alerts" | Stale PRs: 3 (2 from Engineer X). Overloaded: Engineer X (WIP 5). Scope creep: 2 unplanned tickets (+6 pts). |
| 5 | Alex drills into Engineer X | Sees WIP trend: was 2-3 last 3 sprints, now 5. PR cycle time spiked from 2.1 to 4.8 days. Context: Engineer X is covering on-call + mentoring. |
| 6 | Alex copies exec summary | Adds 1 line of human context: "Engineer X's WIP spike is temporary — returning from on-call rotation next sprint." Pastes into weekly report. |

**Success:** Alex spent 12 minutes. Exec summary is paste-ready. Risks are surfaced. 1:1 prep is data-informed.

**The core insight:** The SDM's Monday morning is currently a 4-hour data compilation ritual. Open GitHub Issues/Projects, count story points. Scan PRs across 6 repos. Check who's overloaded. Write a narrative for leadership. This is non-leadership work — it's data entry and pattern matching. The SDM is acting as a human ETL pipeline between GitHub and their weekly report. That's 4 hours/week the SDM is not coaching engineers, not designing architecture, not building leverage tools. 200+ hours/year lost to report compilation.

**What SprintSense changes:** It automates the ETL. The dashboard loads with 3 sprints of trend data. The AI summary is pre-written — 5 bullets, consequence-first, paste-ready. The SDM's job shifts from *compiling* data to *interpreting* it. The 15 minutes are spent reading the summary, scanning for nuance the AI missed, adding 1-2 lines of human context, and moving on. Risk alerts surface automatically: stale PRs, overloaded engineers, scope creep. The SDM doesn't hunt for problems — they're flagged.

**The behavioral shift:** The SDM becomes a coach who uses data, not a reporter who gathers it. Monday mornings are for insight, not compilation. The executive summary is always consistent — same format, same depth, every sprint. Leadership gets a reliable signal. The SDM gets 3.75 hours of their Monday back, every week.

**The constraint:** The AI summary must be human-reviewed before sharing. The tool generates; the SDM curates. AI can miss context ("Engineer X's WIP spike is temporary — returning from on-call"). The SDM adds that human layer. The summary is a draft, not a final product.

---

### 4.5 SDM: Mid-Sprint Risk Check

**Actor:** Alex (SDM)
**Frequency:** 2-3x per sprint, mid-week
**Goal:** Quick pulse — anything on fire?

| Step | Action | SprintSense Behavior |
|---|---|---|
| 1 | Alex opens SprintSense mid-sprint | "Current Sprint" view. |
| 2 | Glances at Risk Alerts | New: "Scope creep: 3 unplanned tickets (+8 pts) added since sprint start." |
| 3 | Clicks alert | Sees: tickets added by Product Manager on day 3. Impact: planned capacity was 42 pts, now 50 pts committed. 3 engineers' WIP bumped. |
| 4 | Alex addresses in standup | "We've added 8 unplanned points. Let's triage: defer, split, or accept the scope change." |

**Success:** Risk caught mid-sprint. Fixable. Not discovered at retro.

**The core insight:** Today, risks surface at standup — or worse, at retro. By the time an SDM realizes an engineer is overloaded, they've already been context-switching for a week. By the time scope creep is visible, 3 unplanned tickets are already in progress and the sprint commitment is blown. The SDM's risk detection is gated on human attention — someone has to notice, remember, and speak up. In a busy sprint, that fails regularly.

**What SprintSense changes:** It decouples risk detection from human attention. The system polls every 4 hours and checks conditions: WIP > threshold? PR stale > 3 days? Unplanned tickets added mid-sprint? Alerts fire automatically and surface as soon as the SDM opens the dashboard. Mid-sprint pulse check takes 5 minutes: open, glance at alerts, decide. No hunting. No forgetting. The SDM catches scope creep on day 3, not at retro when it's a postmortem item.

**The behavioral shift:** The SDM shifts from "I hope nothing's on fire" to "let me check if anything needs attention." It becomes a proactive habit — 5 minutes, 2-3 times per sprint. The standup and retro become venues for discussion and decision, not discovery. Risks are addressed when they're small — 3 unplanned tickets can be deferred or split. At retro, 8 unplanned points are a negotiation crisis.

**The constraint:** SprintSense surfaces risks — it doesn't resolve them. The SDM still decides: address in standup, escalate to Senior SDM, or let it ride. The tool is an early warning system, not an autopilot.

---

### 4.6 SDM: Sprint Planning with Data

**Actor:** Alex (SDM)
**Frequency:** Sprint boundary
**Goal:** Use historical data to inform capacity plan

| Step | Action | SprintSense Behavior |
|---|---|---|
| 1 | Alex opens "Planning View" | Historical capacity data loaded. |
| 2 | Reviews "Capacity Estimate" | "Based on last 3 sprints (avg 42 pts, team of 5, 1 PTO), estimated capacity: 36-40 pts. Watch: Engineer X returning from on-call — historically 20% lower post-oncall." |
| 3 | Reviews "Carry-over Risk" | 2 tickets incomplete from last sprint. Estimated remaining effort: 5 pts. |
| 4 | Reviews team composition | "Engineer Y PTO days 3-7. Historical velocity impact when they're out: -6 pts." |
| 5 | Alex brings data to planning | SprintSense informs. Alex decides. |

**Success:** Planning is data-grounded, not gut-feel.

**The core insight:** Sprint planning today is a negotiation between the SDM's intuition and the team's optimism. "We can do 45 points this sprint." "How do you know?" "We did 42 last sprint, and we feel good." There's no systematic accounting for PTO, on-call rotation, carry-over, or individual engineer capacity patterns. The result is consistently over-committed sprints and consistently under-delivered results — not because the team is slow, but because planning has no data.

**What SprintSense changes:** It gives planning a historical baseline. The planning view shows: average velocity over 3 sprints, adjusted for team composition (PTO, on-call), carry-over risk from incomplete tickets, and historical impact patterns ("Engineer Y's PTO historically costs -6 points"). The AI suggests a capacity range. The SDM brings that number to planning. The conversation shifts from "how much can we do?" to "here's the data — let's decide what to commit to."

**The behavioral shift:** Planning becomes a calibration exercise, not a guessing game. The team debates priorities within a data-informed capacity envelope. Over-commitment declines because the baseline is visible to everyone. The SDM doesn't have to be the "bad guy" saying no — the data does it. Sprint commitments become more predictable, which builds trust with product and leadership.

**The constraint:** SprintSense estimates capacity — it doesn't allocate it. The SDM and team still decide which tickets to pull in. The tool provides the container; humans fill it. Predictions will be wrong sometimes — the key is that they're consistently wrong by a known margin, not randomly.

---

### 4.7 Senior SDM: Multi-Team Health

**Actor:** Sarah (Senior SDM)
**Frequency:** Weekly
**Goal:** Understand delivery health across 3+ teams, surface systemic issues

| Step | Action | SprintSense Behavior |
|---|---|---|
| 1 | Sarah opens SprintSense | Sees per-team dashboards (Team Alpha, Team Beta, Team Gamma). No side-by-side ranking. |
| 2 | Reviews Team Alpha dashboard | Velocity steady. PR cycle time flat. 1 risk alert: scope creep. |
| 3 | Reviews Team Beta dashboard | Velocity ↑12%. PR cycle time improving. No alerts. |
| 4 | Reviews Team Gamma dashboard | Velocity ↓18%. PR cycle time ↑30%. 3 risk alerts: 2 overloaded engineers, 4 stale PRs. |
| 5 | Reviews "Cross-Team Patterns" | "Team Gamma's cycle time increase correlates with Repo D slowdown (time-to-review on Repo D up 40%). Repo D is shared by Teams Alpha and Gamma — but only Gamma is affected. Likely a skills-gap issue, not infra." |
| 6 | Reads executive summary | AI summary: "Team Gamma is the watch item — velocity down 18%, cycle time up 30%. Root cause likely skills-gap on Repo D, not infra. Team Alpha/Beta healthy. Action: discuss with Team Gamma SDM, consider pairing or knowledge-sharing session on Repo D." |
| 7 | Sarah uses insights in 1:1 with Team Gamma SDM | "I see cycle time trending up on your team. Patterns suggest Repo D is the friction point. What's your read? How can I help?" |

**Success:** Sarah has consistent data across all teams. Cross-team patterns are detected. 1:1s are inquiry-driven, not status-driven.

**The core insight:** A Senior SDM today manages through secondhand information. Each SDM reports differently — different metrics, different narratives, different levels of detail. One SDM sends a detailed spreadsheet. Another sends a 3-line Slack message. The Senior SDM spends 1:1 time gathering status that should be visible, and has no way to spot patterns across teams. Is Team Gamma's velocity decline a one-off or a trend? Is it specific to that team or correlated with something systemic? These questions are unanswerable without consistent data across teams.

**What SprintSense changes:** It gives the Senior SDM consistent per-team dashboards — same format, same metrics, same depth, every team. No more inconsistent reporting. Cross-team pattern detection surfaces correlations a human would miss: "Team Gamma's slowdown correlates with Repo D — but only Gamma is affected, so it's likely a skills gap, not infra." The Senior SDM's 1:1s shift from "tell me what happened" to "here's what I see — what's your read?" They become inquiry-driven, coaching conversations.

**The behavioral shift:** The Senior SDM moves from status-gathering to pattern-recognition and resource allocation. They spend 1:1 time on the "why" and "what now," not the "what happened." When presenting to the Director, they have consistent, comparable data across all teams. They can answer the Director's questions without asking each SDM to compile a report.

**The constraint:** SprintSense never displays team-vs-team rankings. The Senior SDM sees per-team dashboards separately, not side-by-side comparison tables. Aggregate metrics are just that — aggregate, not ranked. The tool coaches; it doesn't create a leaderboard.

---

### 4.8 Director: Org-Level DORA + Trends

**Actor:** David (Director)
**Frequency:** Bi-weekly or monthly
**Goal:** Know if the org is getting better, identify systemic issues, have data for VP conversations

| Step | Action | SprintSense Behavior |
|---|---|---|
| 1 | David opens SprintSense | Org aggregate dashboard. No per-team drill-down. No per-individual data. |
| 2 | Reviews DORA metrics | Deploy frequency: 12/week (↑8% QoQ). Lead time: 2.1 days (↓15% QoQ). MTTR: 4.2 hours (flat). Change failure rate: 4.1% (↓12% QoQ). |
| 3 | Reviews quality trends | Bug regression rate trending down over 6 months. PR cycle time stable at 2.3 days org average. |
| 4 | Reviews velocity trend | Org delivering ~180 pts/sprint across all teams. Stable trend. |
| 5 | Reads "Org Health Summary" | AI summary at Director level: "Org DORA is improving: lead time and change failure rate declining, deploy frequency increasing. MTTR is flat — incident response hasn't improved despite delivery gains. Watch: 2 teams had >20% scope creep this quarter — investigate systemic causes (product intake? estimation?). Recommendation: focus next quarter on MTTR improvement and scope-creep governance." |
| 6 | David uses in VP presentation | "Here's our DORA baseline. We're improving on 3 of 4 metrics. MTTR is our Q3 focus. We have data now — we can track whether our interventions work." |

**Success:** David has org-level DORA at his fingertips. Can prove improvement. Can identify systemic issues. Data for VP conversations is always current.

**The core insight:** Most engineering Directors cannot quote their org's DORA metrics. Not because they don't care — because no measurement infrastructure exists. When the VP asks "are we getting better?" the answer is a narrative: "I think so, we shipped the migration, velocity feels up." That's not an answer a Director should have to give. Without DORA, the Director cannot justify headcount ("we need 3 more engineers" — based on what?), cannot benchmark against industry standards, and cannot prove that platform investments are working. The Director is flying blind at the org level.

**What SprintSense changes:** It gives the Director an org-level aggregate dashboard. Four DORA metrics, trended over quarters, with QoQ deltas. Quality and velocity trends aggregated across all teams. The dashboard answers the VP's question in 30 seconds: "Lead time down 15%, deploy frequency up 8%, change failure rate down 12%. MTTR is flat — that's our Q3 focus." The Director no longer needs to ask SDMs to compile data. It's always current. It's always consistent.

**The behavioral shift:** The Director shifts from narrative-based leadership to data-informed leadership. VP presentations are grounded. QBR prep that used to take days now takes 10 minutes. The Director can make resource decisions with evidence: "We need to invest in observability because MTTR hasn't improved in 2 quarters." They can track whether their interventions work: "We hired 2 SREs in Q2 — did MTTR improve in Q3?" The data closes the loop.

**The constraint:** The Director sees org-level aggregates only. No per-team drill-down. No per-individual data. This is non-negotiable — it preserves trust at every level below. If a Director wants to understand a team-specific issue, they talk to the Senior SDM. SprintSense surfaces systemic patterns; humans handle specifics. The Director cannot use this tool to bypass their management chain.

---

### 4.9 Director: Quarterly Business Review Prep

**Actor:** David (Director)
**Frequency:** Quarterly
**Goal:** Present engineering delivery health to VP and stakeholders

| Step | Action | SprintSense Behavior |
|---|---|---|
| 1 | David opens "Quarterly View" | 3 months of trend data aggregated. |
| 2 | Sees DORA trends QoQ | All 4 metrics trended with deltas. |
| 3 | Sees "Delivery Health Score" | Composite score from DORA + velocity stability + quality. |
| 4 | Reads AI narrative | "This quarter: delivery speed ↑, quality ↑, stability flat. The org delivered 15% more story points with 12% fewer bugs than Q1. MTTR is the outlier — unchanged for 2 quarters. Recommendation: invest in observability + runbook automation for Q3." |
| 5 | Exports for presentation | Data + narrative. David adds strategic context. Presents. |

**Success:** QBR prep that used to take days now takes 10 minutes. Data is consistent. Narrative is grounded.

**The core insight:** Quarterly Business Reviews are the highest-stakes presentation a Director gives. The VP and stakeholders are in the room. The questions are sharp: "Did we get better? Where? Prove it. What's the plan for next quarter?" Today, QBR prep is a multi-day fire drill. The Director asks each SDM for data — each responds in a different format. The Director compiles, normalizes, writes narrative, builds slides. By the time the QBR happens, the data is already stale. And next quarter, the same fire drill repeats — from scratch.

**What SprintSense changes:** It makes QBR prep a retrieval exercise, not a compilation exercise. The Quarterly View loads 3 months of trended DORA, quality, and velocity data — always current, always consistent. The AI generates a narrative: what improved, what didn't, what to focus on next quarter. A "Delivery Health Score" — a composite from DORA + velocity stability + quality — gives a single number that tells the story. The Director exports data + narrative, adds strategic context, and presents. 10 minutes, not 3 days.

**The behavioral shift:** QBR becomes a strategic conversation, not a data-gathering exercise. The Director spends their prep time thinking about "what does this mean?" and "what's the plan?" — not "where do I find MTTR data?" The presentation is grounded in consistent metrics quarter after quarter, so trends are comparable. Stakeholders trust the data because it's the same source, same format, every time. The Director looks prepared not because they worked harder, but because the system works.

**The constraint:** SprintSense provides data and narrative — it doesn't set strategy. The Director still decides: what's the Q3 focus? What's the hiring plan? What's the budget ask? The tool removes the data-gathering tax so the Director can spend their cognitive load on decisions. The AI narrative is a draft — the Director adds organizational context, political nuance, and forward-looking strategy that no tool can infer.

---

## 5. Feature Scope

### 5.1 Data Visibility Matrix (What Each Persona Sees)

| | Personal Metrics | Team Aggregate | Cross-Team Patterns | Individual Peer Data | Org Aggregate | AI Exec Summary |
|---|---|---|---|---|---|---|
| **Junior Eng** | ✅ Own only | ❌ | ❌ | ❌ | ❌ | Personal insights only |
| **Senior Eng** | ✅ Own only | ✅ Own team | ❌ | ❌ | ❌ | Personal + team context |
| **Staff Eng** | ✅ Own only | ✅ Own team | ✅ Repo/team patterns | ❌ | ❌ | Personal + cross-team |
| **SDM** | ❌ | ✅ Own team | ❌ | ✅ Own team only | ❌ | Team-level, 5-bullet |
| **Senior SDM** | ❌ | ✅ Per-team (separate) | ✅ Cross-team patterns | ❌ | ✅ Aggregate | Multi-team, systemic |
| **Director** | ❌ | ❌ | ❌ | ❌ | ✅ Org only | Org-level, quarterly |

Key rule: **the dashboard emphasizes what's relevant to your role. Data is technically visible to all, but views are persona-tuned.** No exceptions on emphasis — but v1 does not enforce hard data isolation at the access-control layer.

---

### 5.2 v1 — Must Have

**Data Pipeline:**
- Pull sprint data from GitHub Issues, Milestones, and Projects across all repos (last 3 sprints)
- Sprint model: GitHub Projects with iteration fields + GitHub Milestones (1 milestone = 1 sprint)
- Story points: issue labels (`points:1`, `points:3`, etc.)
- Issue types: issue labels (`bug`, `feature`, `tech-debt`, `task`)
- Pull PR data from all repos (cycle time, merge frequency, review patterns)
- Poll on schedule (default: every 4 hours)

**Personal Dashboards (Junior, Senior, Staff):**
- PR cycle time trend (own PRs only)
- Completed story points per sprint (trended)
- WIP count (current + trend)
- Senior+: review metrics (PRs reviewed, review turnaround time)
- Staff+: cross-team cycle time and blocker patterns

**Team Dashboard (SDM):**
- Velocity trend: planned vs. completed per sprint, 3-sprint trend
- PR cycle time: mean/median/P90, team aggregate, trended
- Bug regression rate: introduced vs. closed per sprint
- Capacity vs. actual: planned vs. delivered, with variance
- DORA metrics: deploy frequency, lead time, MTTR, change failure rate
- Engineer drill-down: per-engineer WIP, blocked tickets, PR cycle time, velocity contribution (own team only)

**AI Executive Summary (SDM):**
- 5-bullet consequence-first summary per completed sprint
- Structured: what matters → what's trending → what's at risk → what to do
- Copy-paste ready
- Human review required before sharing

**Risk Alerts (SDM):**
- Stale PRs (>3 days since activity)
- Overloaded engineers (WIP > configurable threshold)
- Scope creep (unplanned tickets mid-sprint exceeding threshold)

**Multi-Team View (Senior SDM):**
- Per-team dashboards (separate tabs/cards, no ranking)
- Cross-team pattern detection (e.g., "Teams A and C both slowed on Repo X")
- Aggregate metrics across teams
- AI summary at multi-team level

**Org Dashboard (Director):**
- Org-level aggregate DORA metrics, trended
- Org-level quality + velocity trends (quarterly views)
- AI executive summary at Director level (systemic issues, QoQ trends)
- No per-team drill-down. No per-individual data.

---

### 5.3 v2 — Should Have

- Predictive capacity estimates (per-sprint, per-team)
- Sprint planning assistant view
- Custom metric thresholds per team
- Slack notifications for risk alerts (SDM level)
- Engineer-level AI nudges: "Your PR cycle time improved 3 sprints in a row — nice trend"
- Historical sprint comparison (pick any two sprints, view deltas)

---

### 5.4 v3 — Could Have

- Anomaly detection ("Velocity dropped 25% — unusual vs. 12-sprint baseline")
- Sprint retro data integration (RetroMaster tie-in)
- DeliveryOS unified dashboard integration
- Export-to-slide for QBR
- Trend forecasting ("if current trajectory holds, expect X by Q4")

---

## 6. Launch Phasing

SprintSense ships in 6 milestones, starting with 1 team and expanding to the full org. Each milestone builds on the previous — no milestone ships features that require data or infrastructure not yet proven.

### M1: Data Foundation + SDM Core (1 Team)

**Scope:** 1 GitHub repo (Issues + Projects + Milestones + PRs), 1 SDM (Alex's team). No ICs. No Directors.

**What ships:**
- Data pipeline: poll GitHub Issues, Milestones, Projects, and PRs every 4 hours. Compute 3 core metrics: velocity (planned vs. completed), PR cycle time (mean/median), bug regression rate.
- SDM dashboard: velocity trend, PR cycle time trend, bug regression trend, capacity vs. actual. 3-sprint history.
- Engineer drill-down: per-engineer WIP count, blocked tickets, PR cycle time, velocity contribution.
- Data validation: flag missing story points, inconsistent labels, API failures.

**What does NOT ship yet:** AI summaries, risk alerts, DORA, any persona view besides SDM, any other teams.

**Success gate:** SDM uses M1 dashboard for 2 consecutive Mondays. Data pipeline is stable. Time-to-insight < 20 min (self-reported). Only then does M2 begin.

**Why this first:** The vault's guidance: "Get the data pipeline working before building any dashboard or AI analysis." M1 proves the hardest part — reliable data ingestion — before anything else.

---

### M2: AI Summaries + Risk Alerts (1 Team)

**Scope:** Same 1 team. SDM only. Still no ICs or Directors.

**What ships:**
- AI executive summary: 5-bullet consequence-first summary per completed sprint. Human review step enforced in UI (summary shown with "reviewed" toggle before copy enabled).
- Risk alerts: stale PRs (>3 days), overloaded engineers (WIP > threshold), scope creep (unplanned tickets added mid-sprint).
- Capacity estimate for sprint planning.
- DORA metrics (4 metrics trended). First SprintSense feature to aggregate DORA from raw deployment + incident sources.

**What does NOT ship yet:** IC dashboards, Director views, cross-team patterns, multi-team support.

**Success gate:** AI summary is used by SDM in 2 consecutive weekly reports. Risk alerts fire with <20% false positive rate. DORA metrics are computing and trending. Only then does M3 begin.

**Why this second:** AI summaries and DORA are the core differentiators. But they're useless without M1's reliable data pipeline. M2 layers intelligence on a proven foundation.

---

### M3: Engineer Self-Service Dashboards (1 Team)

**Scope:** Same 1 team. Now includes all ICs on that team (Junior, Senior, Staff).

**What ships:**
- Junior engineer dashboard: personal PR cycle time, story points trend, WIP count, AI nudge card.
- Senior engineer dashboard: personal metrics + review/mentoring metrics + team aggregate for context.
- Staff engineer dashboard: personal metrics + cross-team cycle time + blocker patterns.
- All IC dashboards are persona-tuned — default view matches persona, but data is technically open (per D4).

**What does NOT ship yet:** Director views, Senior SDM multi-team view, additional teams.

**Success gate:** ≥80% of ICs on the pilot team check their dashboard at least once per sprint for 2 sprints. Zero "this feels like surveillance" complaints (qualitative — SDM checks in with each IC directly). Only then does M4 begin.

**Why this third:** Engineer adoption is the trust test. If ICs reject the tool, the rest doesn't matter. M3 validates that SprintSense is perceived as a growth tool, not surveillance.

---

### M4: Multi-Team + Senior SDM + Director Views

**Scope:** Add 2 more teams (teams 2 and 3). Senior SDM and Director personas.

**What ships:**
- Multi-team data pipeline: additional repos (Issues + Projects + Milestones + PRs) connected.
- Senior SDM view: per-team dashboards (separate, no ranking), cross-team pattern detection, multi-team AI executive summary.
- Director view: org-level aggregate DORA + quality + velocity trends. Director-level AI executive summary. Quarterly view for QBR prep.
- No per-individual data for Director. No per-team ranking views anywhere.

**What does NOT ship yet:** Remaining teams (4 and 5), polish, integrations.

**Success gate:** Senior SDM uses SprintSense in 2 consecutive 1:1s with SDMs. Director uses data in 1 VP/stakeholder presentation. Only then does M5 begin.

**Why this fourth:** Director and Senior SDM are the highest-leverage users, but they need multi-team data that only exists after M1-M3 prove the model with 1 team. Launching to them with partial data would erode trust.

---

### M5: Full Org Rollout (All Teams)

**Scope:** All 5 teams, all 6 repos. All personas active.

**What ships:**
- Remaining teams (4 and 5) onboarded.
- Slack notifications for risk alerts (SDM level) — Monday morning summary, mid-sprint alerts.
- Anomaly detection: "Velocity dropped 25% — unusual vs. 12-sprint baseline."
- Custom metric thresholds per team.
- Delivery Health Score (composite) for Director QBR view.

**What does NOT ship yet:** DeliveryOS integration, RetroMaster tie-in, trend forecasting.

**Success gate:** ≥80% of org (ICs + SDMs + Directors) actively using SprintSense. DORA metrics tracked continuously for 3+ months. Director can answer "are we getting better?" in under 2 minutes.

---

### M6: Polish, Ecosystem, Handoff

**Scope:** Full org. Focus shifts from building new features to hardening, integrating, and enabling self-service.

**What ships:**
- DeliveryOS unified dashboard integration (SprintSense data feeds into the platform).
- RetroMaster integration (sprint retro data enriches SprintSense patterns).
- Export-to-slide for QBR.
- Trend forecasting ("if current trajectory holds, expect X by Q4").
- Self-service onboarding for new teams: connect repo (Issues + Projects + Milestones) via config, get dashboard. Target: <1 hour.
- Performance optimization: dashboard load < 3 seconds with 12+ sprints of data.
- Documentation: how to read each metric, how to use data in 1:1s/planning/retros, what SprintSense is and isn't.

**Success gate:** SprintSense is the default sprint health tool for the org. New teams onboard without the SprintSense team's involvement. Data feeds into DeliveryOS. The tool is mature enough to be handed off to a sustaining team.

---

### Milestone Summary

| Milestone | Scope | New Personas | Ships | Gates on |
|---|---|---|---|---|
| M1 | 1 team | SDM | Vel, cycle time, bugs, cap vs actual, eng drill-down | Data pipeline stable, SDM uses for 2 weeks |
| M2 | 1 team | SDM | AI summaries, risk alerts, DORA, capacity estimate | AI summary used in 2 reports, alerts <20% FP |
| M3 | 1 team | ICs (Jr, Sr, Staff) | Personal dashboards per persona | ≥80% IC adoption, zero surveillance complaints |
| M4 | 3 teams | Sr SDM, Director | Multi-team dashboards, cross-team patterns, org DORA, QBR view | Sr SDM uses in 1:1s, Dir presents to VP |
| M5 | 5 teams | All | Full org, Slack alerts, anomalies, health score | ≥80% org adoption, 3+ months DORA data |
| M6 | 5 teams | All | Polish, DeliveryOS integration, self-serve onboarding, forecasting | Default tool, self-serve onboarding, platform-ready |

### Onboarding & First-Time Setup

A new user — whether SDM, IC, or Director — must be able to go from zero to their first dashboard in under 30 minutes. This is a hard success criterion.

**Setup steps:**

| Step | Action | Time |
|---|---|---|
| 1 | Authenticate via GitHub OAuth | <1 min |
| 2 | Select repos to connect (Issues + Projects + Milestones + PRs) | <2 min |
| 3 | Verify label conventions: SprintSense auto-detects `points:N`, `bug`, `feature`, `tech-debt`, `sprint:YYYY-MM-DD` labels. User confirms or maps custom labels. | <5 min |
| 4 | Connect data sources: GitHub Actions (deploy events) via repo settings, PagerDuty API token (incident events) | <5 min |
| 5 | Initial data pull: SprintSense fetches last 3 sprints of data. Progress indicator shown. | <10 min |
| 6 | Dashboard renders: user lands on their persona-tuned default view | <2 min |
| 7 | User guide walkthrough: 5-minute guided tour overlaying the dashboard, explaining each metric, where data comes from, and how to use it | <5 min |
| **Total** | | **<30 min** |

**Post-setup user guide (always accessible):**
- "Reading your dashboard" — explains each metric, what the trend line means, what "green/yellow/red" thresholds indicate.
- "What SprintSense is and isn't" — transparent disclosure of what's measured, what's never measured, and who can see what.
- "Using SprintSense in 1:1s" — how SDMs and ICs can use data together in coaching conversations.
- "Using SprintSense in sprint planning" — how to interpret capacity estimates and carry-over risk.
- "Using SprintSense for leadership reporting" — how SDMs, Sr SDMs, and Directors use exec summaries for upward communication.

**Success criteria:**
- New user completes setup in <30 minutes (measured end-to-end for 3 test users).
- User guide is self-contained — no external documentation needed to understand the dashboard.
- "What SprintSense is and isn't" disclosure is shown during setup, not buried in docs. User must acknowledge before dashboard renders.

---

## 7. Testing Strategy

Testing uses synthetic GitHub Issues across dedicated test repos to validate the data pipeline and all persona views without depending on real sprint data.

### 7.1 Test Data Generation

- Dedicated test repos with controlled issue history, PRs, Milestones, and Project iterations.
- Synthetic issues generated with known labels: `points:1` through `points:13`, `bug`, `feature`, `tech-debt`, `task`, `sprint:YYYY-MM-DD`.
- PRs with controlled open/merge timestamps to produce known cycle times for validation.
- Multiple sprints of history (3-6) generated with predetermined velocity, bug counts, and cycle times so expected outputs are known in advance.

### 7.2 Test Suite Categories

| Category | What it validates | How |
|---|---|---|
| **Data pipeline** | Correct counts of issues, PRs, story points, bugs per sprint | Compare pipeline output to known test data |
| **Metric computation** | Velocity, cycle time, bug regression, capacity vs. actual match expected values | Assert computed metrics against pre-calculated baselines |
| **Persona data scope** | Each persona sees correct data set | Junior sees only own data. Director sees only aggregates. Run as persona-specific test suites. |
| **Risk alerts** | Stale PRs (>3 days), overloaded engineers (WIP > 4), scope creep fire correctly | Inject test data with known risk conditions; assert alerts fire |
| **AI summary accuracy** | Executive summary mentions correct metrics, trends, risk signals | Evaluate against golden summaries for known test data |
| **Edge cases** | Empty sprint, zero bugs, all-stale PRs, max WIP, single engineer | Inject edge-case data; assert graceful handling |

### 7.3 Test Data: Sample Scenario

A single controlled test sprint contains:

- **10 issues:** 8 `feature` (total 40 pts), 2 `bug` (6 pts). 7 features closed (35 pts), 2 bugs closed (6 pts). 1 feature carried over.
- **Velocity:** 41 pts completed vs. 46 pts planned = 89% delivery.
- **PRs:** 10 created → merge. Cycle times (first commit → merge): 0.5d, 0.8d, 1.2d, 1.5d, 2.1d, 2.3d, 2.8d, 3.5d, 4.2d, 7.1d. Mean: 2.6d, P90: 5.7d.
- **Stale PR:** The 7.1d PR triggers the stale alert.
- **WIP:** One engineer assigned 5 concurrent issues — triggers overload alert.
- **Scope creep:** 2 issues added mid-sprint with `sprint:YYYY-MM-DD` labels dated after sprint start — triggers scope creep alert.

This scenario validates the full pipeline: data ingestion, metric computation, risk alerts, and all persona dashboards against known expected outputs.

---

## 8. Non-Functional Expectations

| Requirement | Target | Rationale |
|---|---|---|
| **Dashboard load time** | < 3 seconds (cold), < 1 second (warm) | Monday morning ritual. Slow dashboards = abandoned dashboards. |
| **Data freshness** | ≤ 4 hours (poll interval) | Sprint-level analysis doesn't need real-time. 4 hours catches mid-sprint risks same-day. |
| **Availability** | Nice-to-have, not critical | If SprintSense is down, SDM can manually compile. No on-call rotation for SprintSense itself. Target: 95% uptime during business hours. |
| **Data retention** | 12 sprints (6 months) of sprint-level metrics; unlimited for trend aggregates | Enough for meaningful trend analysis. Raw issue/PR data pruned after 6 months. |
| **API rate limits** | Stay under GitHub's secondary rate limits (5,000 requests/hour for authenticated users) | 6 repos × 4 polls/day is well within limits. Monitor and throttle if needed. |
| **AI summary generation** | < 30 seconds per sprint summary (SDM level); < 60 seconds for Director-level | Background job, not blocking page load. Summaries are pre-computed, not generated on-demand. |
| **Concurrent users** | Up to 35 (all personas) | Web dashboard should handle simultaneous loads from all users. |

---

## 9. Success Criteria

### 9.1 v1 Success (Ship Criteria)

| # | Criterion | Measurement |
|---|---|---|
| SC1 | Data pipeline pulls all repos (GitHub Issues, Projects, Milestones, PRs) without manual intervention | Automated poll succeeds for 2 consecutive weeks |
| SC2 | Every persona sees their correct data scope — no leaks | Penetration test: Junior Eng cannot see peer data. Director cannot see individual data. Senior SDM cannot rank teams. |
| SC3 | SDM dashboard shows: velocity trend, PR cycle time, bug regression, capacity vs. actual | All 4 metrics render with trend lines on first load |
| SC4 | AI generates 5-bullet executive summary per completed sprint (SDM level) | Summary renders for every sprint; manual review confirms factual accuracy |
| SC5 | Risk alerts fire for stale PRs, overloaded engineers, scope creep | Alerts fire within 1 poll cycle of condition; false positive rate < 20% |
| SC6 | Junior engineers can see their own PR cycle time and story point trends | Personal dashboard renders for all 25 ICs |
| SC7 | Director can see org-level DORA aggregated across all teams | 4 DORA metrics visible, trended, with QoQ deltas |
| SC8 | At least 1 SDM uses SprintSense every Monday and reports time savings | Time-to-insight < 15 min (self-reported, 4 consecutive weeks) |
| SC9 | New user completes first-time setup in under 30 minutes | Measured end-to-end for 3 test users (fresh setup, no prior config) |

### 9.2 v2 Success (Adoption + Impact)

| # | Criterion | Measurement |
|---|---|---|
| SC9 | DORA metrics tracked continuously for 3+ months | 4 DORA metrics have 12+ weeks of trend data |
| SC10 | ≥80% of engineers (20/25) check their personal dashboard at least once per sprint | Usage analytics |
| SC11 | ≥3 SDMs use SprintSense weekly as their primary sprint health tool | Self-reported + usage data |
| SC12 | Director uses SprintSense data in at least 2 VP/stakeholder presentations | Self-reported |

### 9.3 v3 Success (Org Impact)

| # | Criterion | Measurement |
|---|---|---|
| SC13 | DORA metrics show measurable improvement over 6-month baseline | ≥15% improvement in ≥2 of 4 DORA metrics |
| SC14 | SprintSense data feeds into DeliveryOS unified dashboard | Integration verified |
| SC15 | Director can answer "are we getting better?" with data in under 2 minutes | Timed |

---

## 10. Anti-Goals

1. **NOT a team ranking tool.** No side-by-side velocity or quality comparisons. Aggregate = yes (Director sees org total). Ranking = never.

2. **NOT a performance evaluation tool.** Metrics never feed into HR systems, performance reviews, or calibration sessions. Coaching data ≠ evaluation data.

3. **NOT a GitHub replacement.** Read-only. No issue creation, editing, or workflow transitions.

4. **NOT a real-time ops dashboard.** 4-hour poll interval. SprintSense does not replace PagerDuty, Datadog, or Grafana.

5. **NOT a fully autonomous narrator.** All AI summaries require human review before sharing. The tool generates; the person curates.

6. **NOT over-instrumented.** v1 ships with 5 core metrics. New metrics are added only when existing set has 4+ weeks of reliable data and active use.

7. **NOT a public benchmark.** No external sharing. No "industry comparison." Sprint data stays in the org.

8. **NOT a surveillance tool.** Engineers are informed about what's measured and why. Transparency is non-negotiable.

---

## 11. Constraints & Scale Boundaries

| Constraint | Limit | Rationale |
|---|---|---|
| Max repos (Issues + Projects + PRs) | 6 | Current scope. Same scaling philosophy. |
| Max engineers (ICs) | 25 | Junior through Staff. |
| Max SDMs | 5 | Each managing 4-6 engineers. |
| Max Senior SDMs | 2-3 | Each overseeing 2-3 SDMs. |
| Max Directors | 5 | Org-level consumers. |
| Total users | ~35-40 | All personas combined. |
| Data freshness | 4-hour poll | Sufficient for sprint-level analysis. |
| Sprint history depth | 3 sprints (v1), 6 sprints (v2) | 3 is minimum for a trend line. |
| AI summary length (SDM) | 5 bullets max | Hard constraint. Enforced in prompt. |

---

## 12. Open Decisions

| # | Decision | Options | Impact |
|---|---|---|---|
| ~~D1~~ | **GitHub Issues labeling conventions?** | ✅ **Decided: A** — Enforced across all repos. `points:N` labels for story points. `bug`, `feature`, `tech-debt`, `task` labels for issue types. `sprint:YYYY-MM-DD` labels for sprint tracking. Milestones map 1:1 to sprints. Projects provide board visualization. | Metrics reliable from day 1. |
| ~~D2~~ | **DORA data sources available?** | ✅ **Decided: A.** Deployment events (GitHub Actions/Jenkins) and incident signals (PagerDuty) exist individually. No DORA aggregation exists today — SprintSense will be the first to compute and trend it. DORA is v1. | v1 scope includes all 4 DORA metrics from day 1 |
| ~~D3~~ | **Delivery format?** | ✅ **Decided: A.** Web dashboard. Easier to visualize trends, drill-down, and share across persona levels. | UX investment worth it for trend visualization |
| ~~D4~~ | **Access control mechanism?** | ✅ **Decided: B — Open access.** All data visible to all authenticated users. No persona-based data scoping enforced technically. Data isolation is a social/cultural contract, not a code constraint. RBAC exists only for config changes (who can modify thresholds, data sources, settings). | Significantly simpler to build. Anti-goal of "no team ranking" is upheld culturally — the tool won't display ranking views, but won't technically prevent someone from inferring comparisons. |
| ~~D5~~ | **Repo-to-team mapping?** | ✅ **Decided: 1:1.** Each repo maps to exactly one team. Issues, Projects, and Milestones are scoped per repo. No cross-repo ownership resolution in v1. | Simplest data model. |

---

## 13. User Stories (v1)

### Junior Engineer
| ID | I want to... | So that... |
|---|---|---|
| US-J1 | See my PR cycle time trend across the last 3 sprints | I know if I'm getting faster |
| US-J2 | See my completed story points per sprint | I can track my output over time |
| US-J3 | See my current WIP count | I know if I'm juggling too much |
| US-J4 | Get a personal AI insight about my delivery patterns | I get coaching nudges between 1:1s |

### Senior Engineer
| ID | I want to... | So that... |
|---|---|---|
| US-S1 | See my PR review metrics (count, turnaround time) | I can quantify my mentoring impact |
| US-S2 | See team-level aggregate metrics (velocity, quality) | I have context for my own numbers |
| US-S3 | Know if I'm a review bottleneck | I can adjust my review habits |

### Staff Engineer
| ID | I want to... | So that... |
|---|---|---|
| US-ST1 | See PR cycle time by repo across all teams | I can identify which repos/services are bottlenecks |
| US-ST2 | See cross-team blocker patterns | I can quantify organizational drag |
| US-ST3 | Justify architectural investment with delivery data | My proposals have data, not just opinions |

### SDM
| ID | I want to... | So that... |
|---|---|---|
| US-M1 | See a team dashboard with velocity, PR cycle time, bug rate, and capacity vs. actual | I can understand sprint health without manual compilation |
| US-M2 | Get a 5-bullet AI executive summary every sprint | I can paste it into my weekly report after review |
| US-M3 | See risk alerts for stale PRs, overloaded engineers, and scope creep | I can address issues mid-sprint |
| US-M4 | Drill into each engineer's WIP, blocked tickets, and PR cycle time | I can coach with data, not memory |
| US-M5 | See velocity and quality trends across 3+ sprints | I can distinguish a bad sprint from a declining trend |
| US-M6 | See DORA metrics for my team | I can track delivery excellence over time |
| US-M7 | Get a capacity estimate before sprint planning | My planning is grounded in data |

### Senior SDM
| ID | I want to... | So that... |
|---|---|---|
| US-SM1 | See per-team dashboards for each SDM's team | I have consistent data across all teams |
| US-SM2 | See cross-team patterns and correlations | I can identify systemic issues vs. team-specific ones |
| US-SM3 | Get a multi-team executive summary | I can report upward with consistency |
| US-SM4 | Never see team-vs-team rankings | The tool stays a coaching tool, not a competition |

### Director
| ID | I want to... | So that... |
|---|---|---|
| US-D1 | See org-level aggregate DORA metrics trended over quarters | I can answer "are we getting better?" with data |
| US-D2 | See org-level quality and velocity trends | I have a delivery health baseline |
| US-D3 | Get an org-level AI executive summary | I can present engineering health to VP/stakeholders |
| US-D4 | Never see individual engineer data or per-team comparisons | Trust in the tool is maintained |
| US-D5 | Use SprintSense data for QBR and VP presentations | My presentations are data-driven, not anecdotal |

---

## 14. Assumptions & Risks

### 14.1 Assumptions

1. GitHub API access is available (read-only) for Issues, Projects, Milestones, and PRs across all repos.
2. GitHub Projects have iteration fields configured for sprint tracking.
3. ✅ GitHub Issues use `points:N` labels consistently — confirmed.
4. ✅ Issue types are distinguishable via labels (`bug`, `feature`, `tech-debt`, `task`) — confirmed.
5. At least 3 completed sprints of history exist at launch.
6. ✅ Deployment events (GitHub Actions/Jenkins) and incident signals (PagerDuty) confirmed available. SprintSense will be the first tool to aggregate into DORA. v1 scope.
7. The org trusts SprintSense as a coaching tool — not a surveillance or evaluation tool.
8. Persona-to-data-scope mapping is enforceable (role-based access).
9. Engineers are informed about what's measured and why before launch.

### 14.2 Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| ~~Issue labeling inconsistent~~ | Low (standards enforced) | — | Risk mitigated — D1 confirmed consistent labels |
| GitHub rate limiting | Low | Medium | Caching layer; configurable poll frequency |
| AI summaries hallucinate or miss context | Medium | Medium | Always require human review; summaries cite data sources |
| Perceived as surveillance by engineers | High | **Critical** | Transparent comms pre-launch; never feed HR systems; strict data visibility rules; engineers see their own data first |
| Scope creep — too many metrics before core 5 are stable | High | Medium | Enforce metric gating rule |
| ~~DORA data sources don't exist~~ | Low (confirmed available) | — | Risk mitigated — D2 confirmed; SprintSense is first DORA aggregator |
| ~~Data scope leak~~ | N/A (open access by design) | — | v1 does not enforce data isolation. Risk shifts to cultural: ensure "no ranking" views are not built and no comparison dashboards exist |
| Adoption failure — nobody uses it | Medium | High | Start with SDM persona (highest pain); expand to ICs and Directors after proving value |

---

## 15. Ecosystem Dependencies

SprintSense is part of a broader AI-native SDLC platform (DeliveryOS, Stage 3). It integrates with other tools in the portfolio. While each tool is independently useful, designing with integration in mind avoids rework later.

| Tool | Relationship to SprintSense | Integration point |
|---|---|---|
| **Guardian** | AI code review and governance | When Guardian detects an AI-code incident pattern, it feeds into SprintSense's risk detection (bug regression rate spike). SprintSense quality data feeds back into Guardian's review thresholds. |
| **CI-Agent** | Autonomous CI/CD triage | SprintSense consumes deployment events from CI-Agent for DORA metrics (deploy frequency, lead time). CI-Agent consumes SprintSense risk alerts to auto-prioritize CI failures. |
| **DocPulse** | Documentation health scoring | SprintSense velocity/quality data enriches DocPulse's repo health scores. DocPulse's "stale runbook" alerts correlate with SprintSense's MTTR signals. |
| **RAGoncall** | Runbook retrieval for on-call | SprintSense MTTR data feeds RAGoncall's retrieval quality scoring. RAGoncall usage patterns indicate incident frequency — a spike correlates with SprintSense's change failure rate. |
| **RetroMaster** | Sprint retro facilitation | SprintSense sprint data feeds RetroMaster's retro agenda. RetroMaster's action items and sentiment data feed back into SprintSense's sprint health trending. |
| **DeliveryOS** | Unified AI-native SDLC platform | SprintSense is one of 5 services in the DeliveryOS unified dashboard. Standardize on shared metrics format and event schema from day 1 to avoid rework at integration time. |

**Integration principle:** Each tool remains independently useful. SprintSense does not require any other tool to function. But when other tools exist, the integration points above make the whole greater than the sum.

---

## 16. Glossary

| Term | Definition |
|---|---|
| **Velocity** | Sum of story points completed in a sprint. Trended, not absolute. |
| **PR Cycle Time** | Time from first commit on branch → PR merge. Measured as mean, median, P90. Excludes time before first push. |
| **Bug Regression Rate** | Bugs introduced in a sprint vs. total work completed. Increasing = quality problem. |
| **Capacity vs. Actual** | Planned story points vs. delivered. Variance = estimation accuracy or unplanned work. |
| **DORA Metrics** | Deployment Frequency, Lead Time for Changes, MTTR, Change Failure Rate. |
| **WIP** | Concurrent issues assigned. High WIP = context switching = slower delivery. |
| **Stale PR** | PR with no activity for >3 days. |
| **Scope Creep** | Issues added to a sprint after sprint start. |
| **Consequence-First Summary** | Lead with "so what," then context. |
| **MTTR** | Mean Time to Recovery — how long to restore service after an incident. |
| **GitHub Project** | Kanban-style board with iteration fields. Sprint board equivalent. |
| **GitHub Milestone** | Group of issues with a due date. One milestone = one sprint. |
| **Story Points** | Issue labels: `points:1`, `points:3`, `points:5`, `points:8`, `points:13`. |
| **Issue Type** | Issue labels: `bug`, `feature`, `tech-debt`, `task`. |
| **Sprint Label** | Issue label: `sprint:YYYY-MM-DD` for sprint assignment. |
| **DeliveryOS** | Stage 3 platform integrating Guardian, SprintSense, CI-Agent, RAGoncall, and DocPulse. |

---

*This PRD is a living document. Assumptions should be revisited every 2 sprints. Persona journeys should be validated with actual users before design begins.*
