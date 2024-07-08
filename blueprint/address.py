from flask import Blueprint, request
from service.address_service import AddressService
from utils.response import log_request_start, log_request_end

address_bp = Blueprint('address', __name__)

@address_bp.route('/address', methods=['POST'])
def add_customer():
    endpoint = request.path
    params = request.args
    payload = request.json if request.json else {}
    log_request_start(endpoint, payload)

    service = AddressService(params=params, payload=payload)
    response, status_code = service.add_address()
    
    log_request_end(endpoint, response.json['response_message'])
    return response, status_code

@address_bp.route('/customer/<int:customer_id>', methods=['PATCH'])
def update_customer(customer_id):
    endpoint = request.path
    payload = request.json if request.json else {}
    log_request_start(endpoint, payload)
    
    service = AddressService(payload=payload)
    response, status_code = service.update_address_by_id(customer_id)

    response_json = response.get_json()
    log_request_end(endpoint, response_json['response_message'])
    
    return response, status_code

@address_bp.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    endpoint = request.path
    log_request_start(endpoint)
    
    service = AddressService()
    response, status_code = service.delete_address_by_id(customer_id)
    
    response_json = response.get_json()
    log_request_end(endpoint, response_json['response_message'])
    
    return response, status_code