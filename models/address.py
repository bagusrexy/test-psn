from datetime import datetime
from .db import db

class Address(db.Model):
    __tablename__ = 'address'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id', ondelete="CASCADE"), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class db_address_query(object):
    
    @staticmethod
    def get_address_by_id(value):
        address = Address.query.filter(Address.id == value).first()
        return address
    
    @staticmethod
    def get_address_by_customer_id(customer_id):
        address = Address.query.filter(Address.customer_id == customer_id).all()
        return address