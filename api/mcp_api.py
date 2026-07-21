"""MCP API endpoints for MCPlex integration."""

from flask import Blueprint, jsonify, request

bp = Blueprint("mcp", __name__, url_prefix="/mcp")


@bp.route("/dora/metrics", methods=["GET"])
def dora_metrics():
    scope = request.args.get("scope", "platform-team")
    days = request.args.get("days", "30")
    return jsonify({
        "scope": scope,
        "deploy_frequency": "daily",
        "lead_time": "4.2h",
        "mttr": "25min",
        "change_failure_rate": "0.08",
        "trend": "improving",
    })


@bp.route("/dora/trend", methods=["GET"])
def dora_trend():
    scope = request.args.get("scope", "platform-team")
    return jsonify({
        "scope": scope,
        "weekly": [
            {"week": "W29", "deploy_frequency": "daily", "lead_time": "4.2h", "mttr": "25min", "change_failure_rate": 0.08},
            {"week": "W28", "deploy_frequency": "daily", "lead_time": "5.1h", "mttr": "32min", "change_failure_rate": 0.11},
            {"week": "W27", "deploy_frequency": "daily", "lead_time": "6.0h", "mttr": "40min", "change_failure_rate": 0.15},
        ],
    })
