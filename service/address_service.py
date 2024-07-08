from models.address import Address, db_address_query
from models.customers import db_customer_query
from models.db import db
from utils.response import create_response, Response
from validation.schemas import RequestCustomerSchema
from datetime import datetime

class AddressService(object):
    def __init__(self, params='', headers='', payload=''):
        self.params = params
        self.headers = headers
        self.payload = payload
    
    def add_address(self):
        try:
            validated_payload = RequestCustomerSchema()
            validated_payload.load(self.payload)
            customer_id = self.params.get('customer_id')
            customer = db_customer_query.get_customer_by_id(customer_id)
            if not customer:
                response_template = Response.ERROR_PROCESS.copy()
                response_template['response_message'] = f"Customer with ID {customer_id} not found"
                return create_response(response_template), 404
            new_address = Address(
                address=self.payload.get('address'),
                district=self.payload.get('district'),
                city=self.payload.get('city'),
                province=self.payload.get('province'),
                postal_code=self.payload.get('postal_code'),
                customer_id=int(customer_id)
            )
            
            db.session.add(new_address)
            db.session.commit()
            
            return create_response(Response.SUCCESS_PROCESS), 200
        except Exception as e:
            db.session.rollback()
            response_template = Response.ERROR_PROCESS.copy()
            response_template['response_message'] = f"Error occurred: {str(e)}"
            return create_response(response_template), 500
        
    def update_address_by_id(self, id):
        try:
            address = db_address_query.get_address_by_id(id)
            if not address:
                response_template = Response.ERROR_PROCESS.copy()
                response_template['response_message'] = f"Customer with ID {address} not found"
                return create_response(response_template), 404

            for key, value in self.payload.items():
                if hasattr(address, key):
                    setattr(address, key, value)
            
            address.updated_at = datetime.utcnow()
            db.session.commit()
            return create_response(Response.SUCCESS_PROCESS), 200

        except Exception as e:
            db.session.rollback()
            response_template = Response.ERROR_PROCESS.copy()
            response_template['response_message'] = f"Error occurred: {str(e)}"
            return create_response(response_template), 500
        
    def delete_address_by_id(self, id):
        try:
            address = db_address_query.get_address_by_id(id)
            if not address:
                response_template = Response.ERROR_PROCESS.copy()
                response_template['response_message'] = f"Customer with ID {id} not found"
                return create_response(response_template), 404
            
            db.session.delete(address)
            db.session.commit()
            return create_response(Response.SUCCESS_PROCESS), 200

        except Exception as e:
            db.session.rollback()
            response_template = Response.ERROR_PROCESS.copy()
            response_template['response_message'] = f"Error occurred: {str(e)}"
            return create_response(response_template), 500