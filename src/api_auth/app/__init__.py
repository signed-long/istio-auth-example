from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import config_options
import os
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():

    app = Flask(__name__)
    app.config.from_object(config_options[os.environ.get('FLASK_ENV')])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from app.routes.routes import routes
    from app.errors.handlers import errors

    app.register_blueprint(routes)
    app.register_blueprint(errors)

    return app


app = create_app()
