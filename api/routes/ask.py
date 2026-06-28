"""Sprint Q&A endpoint — chat with sprint data context."""

from flask import Blueprint, jsonify, request
from api.models import Sprint, SprintMetric, AISummary, Alert
from api.poller import ollama_client as llm

bp = Blueprint("ask", __name__, url_prefix="/api/ask")


@bp.route("", methods=["POST"])
def ask():
    data = request.get_json() or {}
    question = data.get("question", "").strip()
    sprint_id = data.get("sprint_id")

    if not question:
        return jsonify({"error": "Question required"}), 400

    sprint = Sprint.query.get(sprint_id) if sprint_id else Sprint.query.order_by(Sprint.start_date.desc()).first()
    if not sprint:
        return jsonify({"answer": "No sprint data available.", "model_used": None})

    metric = SprintMetric.query.filter_by(sprint_id=sprint.id).first()
    summary = AISummary.query.filter_by(sprint_id=sprint.id, persona_level="sdm").first()
    alerts = Alert.query.filter_by(sprint_id=sprint.id).order_by(Alert.created_at.desc()).limit(5).all()

    context_lines = [f"Sprint: {sprint.name} ({sprint.start_date} to {sprint.end_date})"]
    if metric:
        context_lines.append(f"Velocity: {metric.velocity_ratio}")
        context_lines.append(f"Cycle time (mean): {metric.cycle_time_mean_hours}h")
        context_lines.append(f"Bugs introduced: {metric.bugs_introduced}")
        context_lines.append(f"Deploy frequency: {metric.deploy_frequency}/week")
        context_lines.append(f"Change failure rate: {metric.change_failure_rate}")
    if summary:
        context_lines.append(f"AI summary: {summary.summary_text[:200]}")
    if alerts:
        context_lines.append(f"Active alerts: {len(alerts)}")
        for a in alerts[:3]:
            context_lines.append(f"  - {a.title}")

    context = "\n".join(context_lines)
    prompt = f"You are a sprint analytics assistant. Use the data below to answer the question.\n\n{context}\n\nQuestion: {question}\n\nAnswer concisely with data where possible."

    answer = llm.chat(prompt)
    if answer is None:
        return jsonify({"answer": "LLM unavailable. Try again later.", "model_used": None})

    return jsonify({"answer": answer, "model_used": llm.OMLX_MODEL})
