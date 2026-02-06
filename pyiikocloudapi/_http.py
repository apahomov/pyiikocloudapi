import json
import logging

from pyiikocloudapi.models import CustomErrorModel

logger = logging.getLogger(__name__)


def process_response(response_content: bytes, response_status_code: int,
                     return_dict: bool, model_response_data=None,
                     model_error=CustomErrorModel) -> dict:
    """
    Shared response processing logic for both sync and async clients.

    :param response_content: raw response bytes
    :param response_status_code: HTTP status code
    :param return_dict: if True, return raw dict instead of model
    :param model_response_data: pydantic model to parse success response
    :param model_error: pydantic model to parse error response
    :return: parsed response (model or dict)
    """
    try:
        response_data: dict = json.loads(response_content)
    except (json.JSONDecodeError, ValueError):
        error_model = model_error()
        error_model.status_code = response_status_code
        error_model.errorDescription = f"Non-JSON response: {response_content[:200]}"
        return error_model
    if response_data.get("errorDescription", None) is not None:
        error_model = model_error.model_validate(response_data)
        error_model.status_code = response_status_code
        return error_model
    if return_dict:
        return response_data
    if model_response_data is not None:
        return model_response_data.model_validate(response_data)
    return response_data
