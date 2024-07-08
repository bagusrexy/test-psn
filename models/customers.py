from datetime import datetime
from .db import db

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, autoincrement=True, nullable=False, unique=True)
    title = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    addresses = db.relationship('Address', backref='customer', lazy=True)

class db_customer_query(object):
    @staticmethod
    def get_last_customer_id():
        last_customer = Customer.query.order_by(Customer.customer_id.desc()).first()
        if last_customer:
            return last_customer.customer_id
        else:
            return None
        
    @staticmethod
    def get_list_customers(limit):
        customers = Customer.query.order_by(Customer.name.desc()).limit(limit).all()
        return customers
    
    @staticmethod
    def get_customer_by_id(customer_id):
        customer = Customer.query.filter(Customer.customer_id == customer_id).first()
        return customer
    
    @staticmethod
    def get_customer_by_name(customer_name):
        customer = Customer.query.filter(Customer.name == customer_name).first()
        return customer