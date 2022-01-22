from flask import Flask
from app.config import config_options
import os
from app.utils.helpers import (
    make_json_response
)

app = Flask(__name__)
app.config.from_object(config_options[os.environ.get('FLASK_ENV')])


@app.route("/public/hello", methods=["GET"])
def public():
    '''
    Anyone can accesss this route.
    '''
    msg = "OK 200: Hello not authenticated"
    return make_json_response(status=200, msg=msg)


@app.route("/private/hello", methods=["GET"])
def private():
    '''
    Only an authorized user can accesss this route.
    '''
    msg = "OK 200: Hello authenticated"
    return make_json_response(status=200, msg=msg)


@routes.route("/readiness", methods=["POST"])
def readiness_probe():
    '''

    '''
    return make_response("ready :D", 200)


@routes.route("/liveness", methods=["POST"])
def liveness_probe():
    '''

    '''
    return make_response("live :D", 200)
