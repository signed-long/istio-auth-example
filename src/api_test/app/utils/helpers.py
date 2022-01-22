from flask import make_response, jsonify


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
