import logging
from datetime import datetime
from flask import jsonify

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def create_response(response_template, data=None):
    response = response_template.copy()
    if data:
        response["data"] = data
    response["timestamp"] = datetime.utcnow().isoformat()
    return jsonify(response)

def log_request_start(endpoint, params=None):
    logger.info(f"Request Start: {endpoint} | Params: {params if params else '{}'}")

def log_request_end(endpoint, response_message):
    logger.info(f"Request End: {endpoint} | Message: {response_message}")

class Response:
    SUCCESS_PROCESS = {
        "response_code": "SUCCESS",
        "response_message": "Success",
        "data": {}
    }
    ERROR_PROCESS = {
        "response_code": "ERROR",
        "response_message": "Error occurred[error_message]",
        "data": {}
    }
