import os
from flask import Flask
from flask_cors import CORS
from api import models

db = models.db


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql://sprintsense:devpassword123@localhost:5432/sprintsense",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        from api.routes import dashboard, poller, admin, ask
        app.register_blueprint(dashboard.bp)
        app.register_blueprint(poller.bp)
        app.register_blueprint(admin.bp)
        app.register_blueprint(ask.bp)
    return app
