import os

from dotenv import load_dotenv
from flask import Flask

from app.infrastructure.database import db
from app.presentation.routes import web_bp


def create_app(test_config=None):
    load_dotenv()

    app = Flask(
        __name__,
        template_folder="presentation/templates",
        static_folder="presentation/static",
    )

    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///n_layer_store.db",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    app.register_blueprint(web_bp)

    with app.app_context():
        db.create_all()

    return app