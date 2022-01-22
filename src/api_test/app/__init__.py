from flask import Flask
from app.config import config_options
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_options[os.environ.get('FLASK_ENV')])

    from app.routes.routes import routes
    app.register_blueprint(routes)

    return app


app = create_app()
