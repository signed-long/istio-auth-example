from app.utils.helpers import create_jwt_for_user
import json
import jwt
import time
from os import environ


def test_jwt_create():
    token = create_jwt_for_user(user_id="123", sec=5)
    public_key = environ.get("ACCESS_TOKEN_PUBLIC_KEY")
    decoded = json.loads(json.dumps(jwt.decode(token, public_key, 'RS256')))
    assert decoded["sub"] == "123"
    assert decoded["iss"] == environ.get("ACCESS_TOKEN_ISS")


def jwt_expire():
    token = create_jwt_for_user(user_id="123", sec=5)
    public_key = environ.get("ACCESS_TOKEN_PUBLIC_KEY")
    time.sleep(6)
    try:
        json.loads(json.dumps(jwt.decode(token, public_key, 'RS256')))
        assert False
    except jwt.InvalidTokenError:
        assert True


def jwt_bad_pub_key():
    token = create_jwt_for_user(user_id="123", sec=5)
    public_key = environ.get("ACCESS_TOKEN_PUBLIC_KEY")
    try:
        json.loads(json.dumps(jwt.decode(token, public_key, 'RS256')))
        assert False
    except jwt.InvalidTokenError:
        assert True
