SUCCESS = 'success'
MISSING_PARAMS = 'missing params'
UNKNOWN_ERROR = 'unknown error'
EXIST_ERROR = 'already exist'
INVALID_ERROR = 'invalid data'
FORBIDDEN_ERROR = 'not permission'
NOT_FOUND_ERROR = 'server can not find the requested resource'


def response(status, message=None, data=None):
    """
    function for return requets
    """
    if data is None:
        data = None

    if not message:
        if status == 200:
            message = SUCCESS
        elif status == 400:
            message = MISSING_PARAMS
        elif status == 403:
            message = FORBIDDEN_ERROR
        elif status == 404:
            message = NOT_FOUND_ERROR
        elif status == 409:
            message = EXIST_ERROR
        elif status == 500:
            message = UNKNOWN_ERROR

    res = {
        'status': status,
        'message': message,
        'data': data
    }

    return res
