from typing import Union
import requests as rq
from jsonschema.exceptions import ValidationError
import jsonschema
# from urllib.parse import urlparse


def validate_json(data, scheme: Union[dict, str, None] = None) -> None:
    """validate dict

    Args:
        data --- dict of data to validate
        scheme --- scheme dict, follows json http://json-schema.org/
        accept_nan --- bool, if true, will assept nan as float
    """
    if scheme is None:
        scheme = data["$schema"]
    if isinstance(scheme, str):
        scheme = rq.get(scheme).json()

    try:
        jsonschema.validate(data, scheme)
    except ValidationError as e:
        raise Exception(
            e.message, e.validator, e.validator_value, e.absolute_schema_path
        )
