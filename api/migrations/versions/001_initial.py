"""Initial schema: all SprintSense tables

Revision ID: 001_initial
Revises:
Create Date: 2026-06-27
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "repos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("team", sa.String(100)),
        sa.UniqueConstraint("owner", "name"),
    )
    op.create_table(
        "label_config",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("repo_id", sa.Integer(), sa.ForeignKey("repos.id")),
        sa.Column("points_prefix", sa.String(50), server_default="points:"),
        sa.Column("bug_label", sa.String(100), server_default="bug"),
        sa.Column("feature_label", sa.String(100), server_default="feature"),
        sa.Column("techdebt_label", sa.String(100), server_default="tech-debt"),
        sa.Column("task_label", sa.String(100), server_default="task"),
        sa.Column("sprint_prefix", sa.String(50), server_default="sprint:"),
        sa.UniqueConstraint("repo_id"),
    )
    op.create_table(
        "thresholds",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(100), unique=True, nullable=False),
        sa.Column("value", sa.String(255), nullable=False),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(255), unique=True, nullable=False),
        sa.Column("display_name", sa.String(255)),
        sa.Column("default_persona", sa.String(50), nullable=False),
        sa.Column("team_name", sa.String(100)),
        sa.Column("is_admin", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "issues",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("github_id", sa.BigInteger(), nullable=False),
        sa.Column("repo_id", sa.Integer(), sa.ForeignKey("repos.id")),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text()),
        sa.Column("state", sa.String(20)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("closed_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
        sa.Column("assignee_login", sa.String(255)),
        sa.Column("story_points", sa.Numeric()),
        sa.Column("is_bug", sa.Boolean(), server_default="false"),
        sa.Column("is_feature", sa.Boolean(), server_default="false"),
        sa.Column("is_techdebt", sa.Boolean(), server_default="false"),
        sa.Column("is_task", sa.Boolean(), server_default="false"),
        sa.Column("is_blocked", sa.Boolean(), server_default="false"),
        sa.Column("milestone_title", sa.String(255)),
        sa.Column("raw_json", postgresql.JSONB()),
        sa.Column("fetched_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("github_id", "repo_id"),
    )
    op.create_index("idx_issues_repo_state", "issues", ["repo_id", "state"])
    op.create_index("idx_issues_assignee", "issues", ["assignee_login"])
    op.create_table(
        "pull_requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("github_id", sa.BigInteger(), nullable=False),
        sa.Column("repo_id", sa.Integer(), sa.ForeignKey("repos.id")),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text()),
        sa.Column("state", sa.String(20)),
        sa.Column("author_login", sa.String(255)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("merged_at", sa.DateTime()),
        sa.Column("closed_at", sa.DateTime()),
        sa.Column("first_commit_at", sa.DateTime()),
        sa.Column("cycle_time_hours", sa.Numeric()),
        sa.Column("review_count", sa.Integer(), server_default="0"),
        sa.Column("reviewers", sa.ARRAY(sa.String())),
        sa.Column("raw_json", postgresql.JSONB()),
        sa.Column("fetched_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("github_id", "repo_id"),
    )
    op.create_index("idx_prs_repo", "pull_requests", ["repo_id"])
    op.create_index("idx_prs_author", "pull_requests", ["author_login"])
    op.create_table(
        "deploy_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("repo_id", sa.Integer(), sa.ForeignKey("repos.id")),
        sa.Column("workflow_run_id", sa.BigInteger(), nullable=False),
        sa.Column("deployed_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(50)),
        sa.Column("environment", sa.String(100)),
        sa.UniqueConstraint("workflow_run_id", "repo_id"),
    )
    op.create_index("idx_deploy_repo_ts", "deploy_events", ["repo_id", "deployed_at"])
    op.create_table(
        "incidents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pagerduty_id", sa.String(255), unique=True, nullable=False),
        sa.Column("title", sa.Text()),
        sa.Column("status", sa.String(50)),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("resolved_at", sa.DateTime()),
        sa.Column("mttr_hours", sa.Numeric()),
        sa.Column("is_change_failure", sa.Boolean(), server_default="false"),
        sa.Column("linked_deploy_id", sa.Integer(), sa.ForeignKey("deploy_events.id")),
    )
    op.create_index("idx_incidents_ts", "incidents", ["created_at"])
    op.create_table(
        "sprints",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(20), unique=True, nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("source_type", sa.String(50)),
        sa.Column("source_id", sa.String(255)),
        sa.Column("repo_id", sa.Integer(), sa.ForeignKey("repos.id")),
    )
    op.create_table(
        "issue_sprint_map",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("issue_id", sa.Integer(), sa.ForeignKey("issues.id")),
        sa.Column("sprint_id", sa.Integer(), sa.ForeignKey("sprints.id")),
        sa.UniqueConstraint("issue_id", "sprint_id"),
    )
    op.create_index("idx_iss_map_sprint", "issue_sprint_map", ["sprint_id"])
    op.create_table(
        "sprint_metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sprint_id", sa.Integer(), sa.ForeignKey("sprints.id"), unique=True),
        sa.Column("planned_points", sa.Numeric()),
        sa.Column("completed_points", sa.Numeric()),
        sa.Column("velocity_ratio", sa.Numeric()),
        sa.Column("carry_over_points", sa.Numeric()),
        sa.Column("cycle_time_mean_hours", sa.Numeric()),
        sa.Column("cycle_time_median_hours", sa.Numeric()),
        sa.Column("cycle_time_p90_hours", sa.Numeric()),
        sa.Column("total_prs_merged", sa.Integer()),
        sa.Column("bugs_introduced", sa.Integer()),
        sa.Column("bugs_closed", sa.Integer()),
        sa.Column("bug_regression_rate", sa.Numeric()),
        sa.Column("planned_capacity", sa.Numeric()),
        sa.Column("actual_capacity", sa.Numeric()),
        sa.Column("capacity_ratio", sa.Numeric()),
        sa.Column("deploy_frequency", sa.Numeric()),
        sa.Column("lead_time_hours", sa.Numeric()),
        sa.Column("mttr_hours", sa.Numeric()),
        sa.Column("change_failure_rate", sa.Numeric()),
        sa.Column("delivery_health_score", sa.Numeric()),
        sa.Column("computed_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("idx_sm_sprint", "sprint_metrics", ["sprint_id"])
    op.create_table(
        "engineer_sprint_metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sprint_id", sa.Integer(), sa.ForeignKey("sprints.id")),
        sa.Column("engineer_login", sa.String(255), nullable=False),
        sa.Column("completed_points", sa.Numeric()),
        sa.Column("story_count", sa.Integer()),
        sa.Column("prs_merged", sa.Integer()),
        sa.Column("cycle_time_mean_hours", sa.Numeric()),
        sa.Column("prs_reviewed", sa.Integer()),
        sa.Column("avg_review_turnaround_hours", sa.Numeric()),
        sa.Column("max_concurrent_issues", sa.Integer()),
        sa.Column("avg_wip", sa.Numeric()),
        sa.Column("blocked_count", sa.Integer()),
        sa.Column("computed_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("sprint_id", "engineer_login"),
    )
    op.create_index("idx_esm_sprint_eng", "engineer_sprint_metrics", ["sprint_id", "engineer_login"])
    op.create_table(
        "ai_summaries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sprint_id", sa.Integer(), sa.ForeignKey("sprints.id")),
        sa.Column("persona_level", sa.String(50), nullable=False),
        sa.Column("summary_text", sa.Text(), nullable=False),
        sa.Column("model_used", sa.String(100)),
        sa.Column("generated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("reviewed", sa.Boolean(), server_default="false"),
        sa.UniqueConstraint("sprint_id", "persona_level"),
    )
    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sprint_id", sa.Integer(), sa.ForeignKey("sprints.id")),
        sa.Column("alert_type", sa.String(50), nullable=False),
        sa.Column("severity", sa.String(20), server_default="warning"),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("engineer_login", sa.String(255)),
        sa.Column("pr_id", sa.Integer(), sa.ForeignKey("pull_requests.id")),
        sa.Column("issue_count", sa.Integer()),
        sa.Column("points_added", sa.Numeric()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("resolved_at", sa.DateTime()),
    )
    op.create_index("idx_alerts_sprint", "alerts", ["sprint_id"])


def downgrade() -> None:
    op.drop_table("alerts")
    op.drop_table("ai_summaries")
    op.drop_table("engineer_sprint_metrics")
    op.drop_table("sprint_metrics")
    op.drop_table("issue_sprint_map")
    op.drop_table("sprints")
    op.drop_table("incidents")
    op.drop_table("deploy_events")
    op.drop_table("pull_requests")
    op.drop_table("issues")
    op.drop_table("users")
    op.drop_table("thresholds")
    op.drop_table("label_config")
    op.drop_table("repos")
