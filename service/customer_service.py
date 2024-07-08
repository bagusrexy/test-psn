from models.customers import Customer, db_customer_query
from models.address import db_address_query
from models.db import db
from utils.response import create_response, Response
from validation.schemas import RequestCustomerSchema
from datetime import datetime

class CustomerService(object):
    def __init__(self, params='', headers='', payload=''):
        self.params = params
        self.headers = headers
        self.payload = payload
    
    def add_customer_service(self):
        try:
            validated_payload = RequestCustomerSchema()
            validated_payload.load(self.payload)
            new_customer = Customer(
                title=self.payload.get('title'),
                name=self.payload.get('name'),
                gender=self.payload.get('gender'),
                phone_number=self.payload.get('phone_number'),
                image=self.payload.get('image'),
                email=self.payload.get('email'),
                customer_id=int(self.generate_customer_id())
            )
            
            db.session.add(new_customer)
            db.session.commit()
            
            return create_response(Response.SUCCESS_PROCESS), 200
        except Exception as e:
            db.session.rollback()
            response_template = Response.ERROR_PROCESS.copy()
            response_template['response_message'] = f"Error occurred: {str(e)}"
            return create_response(response_template), 500
    
    def generate_customer_id(self):
        last_id = db_customer_query.get_last_customer_id()
        if last_id != None:
            customer_id = last_id + 1
            return customer_id
        else:
            return 1
        
    def get_list_customers(self):
        try:
            limit = self.params.get('limit', 10)
            data_bulk = db_customer_query.get_list_customers(limit)
            
            data_json = []
            for data in data_bulk:
                data_json.append({
                    "customer_id": data.customer_id,
                    "title": data.title,
                    "name": data.name,
                    "gender": data.gender,
                    "phone_number": data.phone_number,
                    "image": data.image,
                    "email": data.email,
                    "created_at": data.created_at.isoformat(),
                    "updated_at": data.updated_at.isoformat()
                })
            
            return create_response(Response.SUCCESS_PROCESS, data=data_json), 200

        except Exception as e:
            response_template = Response.ERROR_PROCESS.copy()
            response_template['response_message'] = f"Error occurred: {str(e)}"
            return create_response(response_template), 500
        
    def update_customer_by_id(self, customer_id):
        try:
            customer = db_customer_query.get_customer_by_id(customer_id)
            if not customer:
                response_template = Response.ERROR_PROCESS.copy()
                response_template['response_message'] = f"Customer with ID {customer_id} not found"
                return create_response(response_template), 404

            for key, value in self.payload.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)
            
            customer.updated_at = datetime.utcnow()
            db.session.commit()
            return create_response(Response.SUCCESS_PROCESS), 200

        except Exception as e:
            db.session.rollback()
            response_template = Response.ERROR_PROCESS.copy()
            response_template['response_message'] = f"Error occurred: {str(e)}"
            return create_response(response_template), 500
        
    def delete_customer_by_id(self, customer_id):
        try:
            customer = db_customer_query.get_customer_by_id(customer_id)
            
            if not customer:
                response_template = Response.ERROR_PROCESS.copy()
                response_template['response_message'] = f"Customer with ID {customer_id} not found"
                return create_response(response_template), 404
            addresses = db_address_query.get_address_by_customer_id(customer_id)
            for address in addresses:
                db.session.delete(address)
            db.session.delete(customer)
            db.session.commit()
            return create_response(Response.SUCCESS_PROCESS), 200

        except Exception as e:
            db.session.rollback()
            response_template = Response.ERROR_PROCESS.copy()
            response_template['response_message'] = f"Error occurred: {str(e)}"
            return create_response(response_template), 500
        
    def get_customer_detail(self, customer_id):
        try:
            customer = db_customer_query.get_customer_by_id(customer_id)
            if not customer:
                response_template = Response.ERROR_PROCESS.copy()
                response_template['response_message'] = f"Customer with ID {customer_id} not found"
                return create_response(response_template), 404
            addresses = db_address_query.get_address_by_customer_id(customer_id)
            address_list = []
            for data in addresses:
                address_list.append({
                    "id": data.id,
                    "address": data.address,
                    "district": data.district,
                    "city": data.city,
                    "province": data.province,
                    "postal_code": data.postal_code,
                    "created_at": data.created_at.isoformat(),
                    "updated_at": data.updated_at.isoformat()
                })
            response = {
                "id": customer.id,
                "title": customer.title,
                "name": customer.name,
                "gender": customer.gender,
                "phone_number": customer.phone_number,
                "image": customer.image,
                "email": customer.email,
                "address": address_list
            }
            
            return create_response(Response.SUCCESS_PROCESS, data=response), 200
        except Exception as e:
            response_template = Response.ERROR_PROCESS.copy()
            response_template['response_message'] = f"Error occurred: {str(e)}"
            return create_response(response_template), 500