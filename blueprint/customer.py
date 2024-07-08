from flask import Blueprint, request
from service.customer_service import CustomerService
from utils.response import log_request_start, log_request_end

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customer', methods=['POST'])
def add_customer():
    endpoint = request.path
    payload = request.json if request.json else {}
    log_request_start(endpoint, payload)

    service = CustomerService(payload=payload)
    response, status_code = service.add_customer_service()
    
    log_request_end(endpoint, response.json['response_message'])
    return response, status_code

@customer_bp.route('/customer', methods=['GET'])
def get_customer():
    endpoint = request.path
    params = request.args
    log_request_start(endpoint, params)

    service = CustomerService(params=params)
    response, status_code = service.get_list_customers()

    log_request_end(endpoint, response.json['response_message'])
    return response, status_code

@customer_bp.route('/customer/<int:customer_id>', methods=['PATCH'])
def update_customer(customer_id):
    endpoint = request.path
    payload = request.json if request.json else {}
    log_request_start(endpoint, payload)
    
    service = CustomerService(payload=payload)
    response, status_code = service.update_customer_by_id(customer_id)

    response_json = response.get_json()
    log_request_end(endpoint, response_json['response_message'])
    
    return response, status_code

@customer_bp.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    endpoint = request.path
    log_request_start(endpoint)
    
    service = CustomerService()
    response, status_code = service.delete_customer_by_id(customer_id)
    
    response_json = response.get_json()
    log_request_end(endpoint, response_json['response_message'])
    
    return response, status_code

@customer_bp.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer_detail(customer_id):
    endpoint = request.path
    log_request_start(endpoint)
    
    service = CustomerService()
    response, status_code = service.get_customer_detail(customer_id)
    
    response_json = response.get_json()
    log_request_end(endpoint, response_json['response_message'])
    
    return response, status_code


