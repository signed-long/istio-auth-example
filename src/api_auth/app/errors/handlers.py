from flask import Blueprint
from app.utils.helpers import make_json_response

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(400)
def error_400(error):
    '''
    Handels 400 error Bad Request.
    '''
    msg = ("ERROR 400: Bad Request.")
    return make_json_response(status=400, msg=msg)


@errors.app_errorhandler(401)
def error_401(error):
    '''
    Handels 401 error Unauthorized.
    '''
    msg = ("ERROR 401: Unauthorized.")
    return make_json_response(status=401, msg=msg)


@errors.app_errorhandler(404)
def error_404(error):
    '''
    Handels 404 error Page not found.
    '''
    msg = ("ERROR 404: Page not found.")
    return make_json_response(status=404, msg=msg)


@errors.app_errorhandler(405)
def error_405(error):
    '''
    Handels 405 error Method not allowed.
    '''
    msg = ("ERROR 405: Method not allowed.")
    return make_json_response(status=405, msg=msg)


@errors.app_errorhandler(409)
def error_409(error):
    '''
    Handels 409 error User already exisits.
    '''
    msg = ("ERROR 409: User already exisits")
    return make_json_response(status=409, msg=msg)


@errors.app_errorhandler(500)
def error_500(error):
    '''
    Handels 500 error Internal Error.
    '''
    msg = ("ERROR 500: An error occured on the server.")
    return make_json_response(status=500, msg=msg)
