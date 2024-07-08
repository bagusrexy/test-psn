from flask import Blueprint, request
from utils.response import create_response, log_request_start, log_request_end, Response

check_health_bp = Blueprint('check_health', __name__)

@check_health_bp.route('/', methods=['GET'])
def check_health():
    log_request_start('/health')
    
    data = {"status": "healthy"}
    
    response = create_response(Response.SUCCESS_PROCESS, data)
    
    log_request_end('/health', Response.SUCCESS_PROCESS["response_message"])
    return response
