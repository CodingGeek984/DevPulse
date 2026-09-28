from flask import Flask
from werkzeug.routing import IntegerConverter

from app.config import Config
from app.extensions import db
from app.routes.monitors import monitors_bp
from app.routes.webhooks import webhooks_bp


class MonitorIdConverter(IntegerConverter):
    regex = r"\d{1,9}"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.url_map.converters["monitor_id"] = MonitorIdConverter

    db.init_app(app)

    app.register_blueprint(monitors_bp)
    app.register_blueprint(webhooks_bp)

    @app.cli.command("init-db")
    def init_db_command():
        db.create_all()
        print("Tables created.")

    return app
