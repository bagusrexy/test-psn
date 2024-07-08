from marshmallow import fields, Schema, validates, ValidationError, validate
from models.customers import Customer

class RequestCustomerSchema(Schema):
    title = fields.Str(required=True)
    name = fields.Str(required=True)
    gender = fields.Str(required=True, validate=validate.OneOf(["M", "F"]))
    phone_number = fields.Str(required=True)
    image = fields.Str(required=True)
    email = fields.Email(required=True)
    
    @validates("phone_number")
    def validate_phone_number(self, value):
        existing_customer = Customer.query.filter(Customer.phone_number == value).first()
        if existing_customer:
            raise ValidationError('phone_number already exists.')
        
class RequestAddressSchema(Schema):
    address = fields.Str(required=True)
    district = fields.Str(required=True)
    city = fields.Str(required=True)
    province = fields.Str(required=True)
    postal_code = fields.Int(required=True)
  