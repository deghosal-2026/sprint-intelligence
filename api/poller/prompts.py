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
