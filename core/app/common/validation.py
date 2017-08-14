import os
import json
from functools import wraps

import jsonschema

from .request import get_request_payload

SCHEMAS_DIR = 'app/specifications/schemas'
SCHEMAS_PATH = os.path.join(os.getcwd(), SCHEMAS_DIR)


def validate_schema(payload, schema):
    """
    Validates the payload against the defined json schema.
    
    :param payload: incoming request data
    :param schema: json schema, the payload should be validated against
    :return: errors if there are any, otherwise None
    """
    errors = []
    validator = jsonschema.Draft4Validator(schema, format_checker=jsonschema.FormatChecker())
    for error in sorted(validator.iter_errors(payload), key=str):
        errors.append(error.message)

    return errors


def get_schema(path):
    """
    Read the .json schema and returns its content
    :param path: path to schema
    :return: schema content
    :rtype: dict
    """
    with open(path, 'r') as f:
        return json.load(f)


def schema(path=None):
    """
    Validate request data against a json schema.
    
    This is a decorator that will be used to specify
    the path to the schema that the endpoint should be
    validated against.
    
    :param path: path to schema file
    """

    def decorator(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            _path = path.lstrip('/')

            payload = get_request_payload(self.request)
            schema_path = os.path.join(SCHEMAS_PATH, _path)

            errors = validate_schema(payload, get_schema(schema_path))
            if errors:
                raise Exception(str(errors))

            return func(self, *args, **kwargs)

        return wrapped

    return decorator
