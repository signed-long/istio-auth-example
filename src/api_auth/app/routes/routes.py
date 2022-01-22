from flask import Blueprint, request, abort, make_response
from flask_expects_json import expects_json
from os import environ
from app import db
from app.models import User
from app.utils.helpers import (
    make_json_response,
    create_jwt_for_user
)

routes = Blueprint("routes", __name__)

login_schema = {
    "email": {
        "type": "string",
        "minLength": 5,
        "maxLength": 254},
    "password": {
        "type": "string",
        "minLength": 8},
    "required": ["email", "password"]
}


@routes.route("/auth/register", methods=["POST"])
@expects_json(login_schema)
def register():
    '''
    Creates a new user in the db.
    '''
    request_data = request.get_json()

    email = request_data["email"]
    user = User.query.filter_by(email=request_data["email"]).first()
    if user is not None:
        abort(409)

    user = User(email=email, password=request_data["password"])
    db.session.add(user)
    db.session.commit()

    msg = "OK 201: Registration successful"
    return make_json_response(status=201, msg=msg)


@routes.route("/auth/login", methods=["POST"])
@expects_json(login_schema)
def login():
    '''
    Authenticates a client and responds with access token.
    '''
    # pull user from db
    request_data = request.get_json()
    user = User.query.filter_by(email=request_data["email"]).first()

    # authenticate user and return access token
    if user and user.check_pw_hash(request_data["password"]):

        exp = int(environ.get("ACCESS_TOKEN_EXP_SEC"))
        access_token = create_jwt_for_user(user_id=str(user.id), sec=exp)

        tokens = {"access_token": access_token}
        msg = "OK 200: Authentication successful"
        return make_json_response(status=200, msg=msg, response_dict=tokens)

    # user does not exist or entered bad credentials
    abort(401)


@routes.route("/readiness", methods=["POST"])
def readiness_probe():
    '''

    '''
    try:
        db.engine.execute('SELECT 1')
        return make_response("ready :D", 200)
    except Exception as e:
        return make_response("not ready x_x", 500)


@routes.route("/liveness", methods=["POST"])
def liveness_probe():
    '''

    '''
    return make_response("live :D", 200)
