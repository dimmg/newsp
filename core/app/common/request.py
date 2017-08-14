from tornado.escape import json_decode, to_unicode


def get_content_type(request):
    """
    Returns the Content-Type of current request.
    :param request: tornado request handler
    :return: value of Content-Type header
    :rtype: string
    """

    return request.headers.get('Content-Type')


def application_json(func):
    """
    Ensures that the subsequent request has the
    'Content-Type' header set to 'application/json'
    :param func: tornado request method handler 
    """

    def wrapper(self, *args, **kwargs):
        if get_content_type(self.request) != 'application/json':
            raise Exception('Content-Type is not application/json')

        return func(self, *args, **kwargs)

    return wrapper


def get_json(request):
    """
    Returns the request body as a dict.
    :param request: tornado request handler
    :return: posted request body 
    :rtype: dict
    """

    return json_decode(request.body)


def get_query_params(request):
    """
    Returns query params for a specific request object.
    :param request: request object
    :return: query params
    :rtype: dict
    """
    params = request.arguments

    result = {}
    for param, val in params.items():
        result[param] = serialize_number(to_unicode(val[0]))

    return result


def get_request_params(request):
    """
    Combines both URL and body parameters
    """
    query_params = get_query_params(request)
    body_params = get_json(request)

    return {**body_params, **query_params}


def get_request_payload(request):
    """
    Returns request payload: both query and body parameters,
    depending on the request method.
    :param method: request method (GET, PUT, POST, DELETE)
    :param request: request object
    """
    return {
        'GET': get_query_params,
        'POST': get_request_params
    }[request.method](request)


def serialize_number(value):
    """
    Tries to convert `string` to `int`, if it can't -
    tries to convert to `float`, if it fails again -
    the `string` itself is returned.
    """
    try:
        _val = int(value)
        return _val
    except ValueError:
        pass
    try:
        _val = float(value)
        return _val
    except ValueError:
        pass

    return value
