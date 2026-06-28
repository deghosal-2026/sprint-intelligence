from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

db = SQLAlchemy()


class Repo(db.Model):
    __tablename__ = "repos"
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    team = db.Column(db.String(100))
    __table_args__ = (db.UniqueConstraint("owner", "name"),)


class LabelConfig(db.Model):
    __tablename__ = "label_config"
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey("repos.id"))
    points_prefix = db.Column(db.String(50), default="points:")
    bug_label = db.Column(db.String(100), default="bug")
    feature_label = db.Column(db.String(100), default="feature")
    techdebt_label = db.Column(db.String(100), default="tech-debt")
    task_label = db.Column(db.String(100), default="task")
    sprint_prefix = db.Column(db.String(50), default="sprint:")
    __table_args__ = (db.UniqueConstraint("repo_id"),)

    repo = db.relationship("Repo", backref=db.backref("label_config", uselist=False))


class Threshold(db.Model):
    __tablename__ = "thresholds"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(255))
    default_persona = db.Column(db.String(50), nullable=False)
    team_name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Issue(db.Model):
    __tablename__ = "issues"
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.BigInteger, nullable=False)
    repo_id = db.Column(db.Integer, db.ForeignKey("repos.id"))
    number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text)
    state = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)
    closed_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    assignee_login = db.Column(db.String(255))
    story_points = db.Column(db.Numeric)
    is_bug = db.Column(db.Boolean, default=False)
    is_feature = db.Column(db.Boolean, default=False)
    is_techdebt = db.Column(db.Boolean, default=False)
    is_task = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    milestone_title = db.Column(db.String(255))
    raw_json = db.Column(postgresql.JSONB)
    fetched_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint("github_id", "repo_id"),)

    repo = db.relationship("Repo", backref=db.backref("issues", lazy="dynamic"))


class PullRequest(db.Model):
    __tablename__ = "pull_requests"
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.BigInteger, nullable=False)
    repo_id = db.Column(db.Integer, db.ForeignKey("repos.id"))
    number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text)
    state = db.Column(db.String(20))
    author_login = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    merged_at = db.Column(db.DateTime)
    closed_at = db.Column(db.DateTime)
    first_commit_at = db.Column(db.DateTime)
    cycle_time_hours = db.Column(db.Numeric)
    review_count = db.Column(db.Integer, default=0)
    reviewers = db.Column(postgresql.ARRAY(db.String))
    raw_json = db.Column(postgresql.JSONB)
    fetched_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint("github_id", "repo_id"),)

    repo = db.relationship("Repo", backref=db.backref("pull_requests", lazy="dynamic"))


class DeployEvent(db.Model):
    __tablename__ = "deploy_events"
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey("repos.id"))
    workflow_run_id = db.Column(db.BigInteger, nullable=False)
    deployed_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50))
    environment = db.Column(db.String(100))
    __table_args__ = (db.UniqueConstraint("workflow_run_id", "repo_id"),)

    repo = db.relationship("Repo", backref=db.backref("deploy_events", lazy="dynamic"))


class Incident(db.Model):
    __tablename__ = "incidents"
    id = db.Column(db.Integer, primary_key=True)
    pagerduty_id = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.Text)
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
    resolved_at = db.Column(db.DateTime)
    mttr_hours = db.Column(db.Numeric)
    is_change_failure = db.Column(db.Boolean, default=False)
    linked_deploy_id = db.Column(db.Integer, db.ForeignKey("deploy_events.id"))


class Sprint(db.Model):
    __tablename__ = "sprints"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    source_type = db.Column(db.String(50))
    source_id = db.Column(db.String(255))
    repo_id = db.Column(db.Integer, db.ForeignKey("repos.id"))

    repo = db.relationship("Repo", backref=db.backref("sprints", lazy="dynamic"))


class IssueSprintMap(db.Model):
    __tablename__ = "issue_sprint_map"
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey("issues.id"))
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"))
    __table_args__ = (db.UniqueConstraint("issue_id", "sprint_id"),)

    issue = db.relationship("Issue", backref=db.backref("sprint_maps", lazy="dynamic"))
    sprint = db.relationship("Sprint", backref=db.backref("issue_maps", lazy="dynamic"))


class SprintMetric(db.Model):
    __tablename__ = "sprint_metrics"
    id = db.Column(db.Integer, primary_key=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"), unique=True)
    planned_points = db.Column(db.Numeric)
    completed_points = db.Column(db.Numeric)
    velocity_ratio = db.Column(db.Numeric)
    carry_over_points = db.Column(db.Numeric)
    cycle_time_mean_hours = db.Column(db.Numeric)
    cycle_time_median_hours = db.Column(db.Numeric)
    cycle_time_p90_hours = db.Column(db.Numeric)
    total_prs_merged = db.Column(db.Integer)
    bugs_introduced = db.Column(db.Integer)
    bugs_closed = db.Column(db.Integer)
    bug_regression_rate = db.Column(db.Numeric)
    planned_capacity = db.Column(db.Numeric)
    actual_capacity = db.Column(db.Numeric)
    capacity_ratio = db.Column(db.Numeric)
    deploy_frequency = db.Column(db.Numeric)
    lead_time_hours = db.Column(db.Numeric)
    mttr_hours = db.Column(db.Numeric)
    change_failure_rate = db.Column(db.Numeric)
    delivery_health_score = db.Column(db.Numeric)
    computed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    sprint = db.relationship("Sprint", backref=db.backref("metrics", uselist=False))


class EngineerSprintMetric(db.Model):
    __tablename__ = "engineer_sprint_metrics"
    id = db.Column(db.Integer, primary_key=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"))
    engineer_login = db.Column(db.String(255), nullable=False)
    completed_points = db.Column(db.Numeric)
    story_count = db.Column(db.Integer)
    prs_merged = db.Column(db.Integer)
    cycle_time_mean_hours = db.Column(db.Numeric)
    prs_reviewed = db.Column(db.Integer)
    avg_review_turnaround_hours = db.Column(db.Numeric)
    max_concurrent_issues = db.Column(db.Integer)
    avg_wip = db.Column(db.Numeric)
    blocked_count = db.Column(db.Integer)
    computed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    __table_args__ = (db.UniqueConstraint("sprint_id", "engineer_login"),)

    sprint = db.relationship("Sprint", backref=db.backref("engineer_metrics", lazy="dynamic"))


class AISummary(db.Model):
    __tablename__ = "ai_summaries"
    id = db.Column(db.Integer, primary_key=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"))
    persona_level = db.Column(db.String(50), nullable=False)
    summary_text = db.Column(db.Text, nullable=False)
    model_used = db.Column(db.String(100))
    generated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    reviewed = db.Column(db.Boolean, default=False)
    __table_args__ = (db.UniqueConstraint("sprint_id", "persona_level"),)

    sprint = db.relationship("Sprint", backref=db.backref("ai_summaries", lazy="dynamic"))


class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    sprint_id = db.Column(db.Integer, db.ForeignKey("sprints.id"))
    alert_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), default="warning")
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    engineer_login = db.Column(db.String(255))
    pr_id = db.Column(db.Integer, db.ForeignKey("pull_requests.id"))
    issue_count = db.Column(db.Integer)
    points_added = db.Column(db.Numeric)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    resolved_at = db.Column(db.DateTime)

    sprint = db.relationship("Sprint", backref=db.backref("alerts", lazy="dynamic"))
    pull_request = db.relationship("PullRequest", backref=db.backref("alerts", lazy="dynamic"))
