from flask import make_response, jsonify
import jwt
from datetime import datetime, timedelta, timezone
from os import environ


def make_json_response(status, msg, response_dict={}):
    '''
    Returns a JSON response given a response_dict. Required fields are passed as
    arguments, any other data is passed in as 'response_dict'.

    Parameters:
        - status (int) - Status code of the response.
        - msg (str) - Additional information for client.
        - response_dict (dict) - A dictionary that will be returned in the
          'data' field of the response.
    '''
    response = {
        "http_response": {
            "message": msg,
            "status": status
        },
        "data": {
            **response_dict
        }
    }
    status_code = response["http_response"]["status"]
    return make_response(jsonify(response), status_code)


def create_jwt_for_user(user_id, sec):
    '''
    Creates an access token.

    Parameters:
        - user (User) - A user to create the token for.
        - exp_sec (int) - number of second till expiration.
        - days (int) - number of days till expiration.

    '''
    private_key = environ.get("ACCESS_TOKEN_PRIVATE_KEY")
    payload = {"sub": user_id,
               "exp": datetime.now(timezone.utc) + timedelta(seconds=sec),
               "iss": environ.get("ACCESS_TOKEN_ISS")}

    return jwt.encode(payload, private_key, algorithm="RS256")
