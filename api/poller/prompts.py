"""Prompt templates for AI summaries per persona."""

SDM_SUMMARY_SYSTEM = """You are a sprint analytics assistant for an Engineering SDM.
Summarize the sprint data into exactly 5 bullet points only (no thinking, no explanations, no greetings).
Each bullet: "metric → consequence".

Rules:
- Only output the 5 bullet points, nothing else before or after
- Start with the most impactful metric first
- State the metric value, then its consequence for the team
- Use numbers where available (%, hours, points)
- If data is missing, say "Data unavailable"
- Keep each bullet under 120 characters
- Do NOT include any thinking process"""


def sdm_summary_prompt(metrics):
    v = metrics.get("velocity_ratio")
    ct = metrics.get("cycle_time_mean_hours")
    ct_p50 = metrics.get("cycle_time_median_hours")
    bugs = metrics.get("bugs_introduced")
    capacity = metrics.get("capacity_ratio")
    planned = metrics.get("planned_points")
    completed = metrics.get("completed_points")
    carry = metrics.get("carry_over_points")

    lines = [
        "Sprint data for SDM summary:",
        f"- Velocity: {v*100:.0f}% ({completed}/{planned} pts)" if planned else "- Velocity: unknown",
        f"- Cycle time (mean): {ct}h" if ct else "- Cycle time: unknown",
        f"- Cycle time (median): {ct_p50}h" if ct_p50 else "",
        f"- Bugs introduced: {bugs}" if bugs is not None and bugs > 0 else "- No new bugs",
        f"- Capacity utilization: {capacity*100:.0f}%" if capacity else "- Capacity: unknown",
        f"- Carry-over: {carry} pts" if carry else "",
    ]
    return "\n".join(line for line in lines if line)


SRSDM_SUMMARY_SYSTEM = """You are a sprint analytics assistant for a Senior SDM overseeing multiple teams.
Summarize the multi-team sprint data into exactly 5 bullet points only (no thinking, no explanations, no greetings).
Each bullet: "team metric → systemic pattern".

Rules:
- Only output the 5 bullet points, nothing else before or after
- Focus on cross-team patterns and systemic issues
- Reference specific team names where patterns differ
- Use numbers where available (%, hours, points)
- Keep each bullet under 120 characters
- Do NOT include any thinking process"""


def srsdm_summary_prompt(team_metrics_list):
    lines = ["Multi-team sprint data for SrSDM summary:"]
    for tm in team_metrics_list:
        team = tm.get("team", "?")
        v = tm.get("velocity_ratio")
        ct = tm.get("cycle_time_mean_hours")
        bugs = tm.get("bugs_introduced")
        lines.append(
            f"- {team}: velocity {v*100:.0f}%"
            if v else f"- {team}: velocity unknown"
        )
        if ct:
            lines[-1] += f", cycle time {ct}h"
        if bugs:
            lines[-1] += f", bugs {bugs}"
    return "\n".join(lines)


DIRECTOR_SUMMARY_SYSTEM = """You are a strategic analytics assistant for an Engineering Director.
Summarize the org-level quarterly data into exactly 4 bullet points only (no thinking, no explanations, no greetings).
The last bullet must be a specific, actionable recommendation.

Rules:
- Only output the 4 bullet points, nothing else before or after
- Focus on org-wide trends, not per-team details
- Compare current quarter to previous quarter using QoQ deltas
- Use numbers where available (%, hours, points)
- Keep each bullet under 140 characters
- Do NOT include any thinking process"""


def director_summary_prompt(quarterly_data):
    lines = ["Org-level quarterly data for Director summary:"]
    for team_data in quarterly_data:
        team = team_data.get("team", "?")
        avg = team_data.get("averages", {})
        delta = team_data.get("qoq_delta", {})
        vel = avg.get("velocity_ratio")
        vel_str = f"{vel*100:.0f}%" if vel is not None else "unknown"
        vel_delta = delta.get("velocity_ratio")
        vel_delta_str = f"{vel_delta:+.1f}%" if vel_delta is not None else "N/A"
        ct = avg.get("cycle_time_mean_hours")
        ct_str = f"{ct:.0f}h" if ct is not None else "unknown"
        ct_delta = delta.get("cycle_time_mean_hours")
        ct_delta_str = f"{ct_delta:+.1f}%" if ct_delta is not None else "N/A"
        lines.append(
            f"- {team}: velocity {vel_str} (QoQ: {vel_delta_str}), "
            f"cycle time {ct_str} (QoQ: {ct_delta_str})"
        )
    return "\n".join(lines)
