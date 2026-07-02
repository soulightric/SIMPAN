from flask import Flask
from .config import Config
from .database.db import db

def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        from .database.models import History
        db.create_all()
    from .routes import main
    app.register_blueprint(main)
    return app