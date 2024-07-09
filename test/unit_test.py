import pytest
import datetime
import random
import time
from app import app, db
from models.customers import Customer
from models.address import db_address_query

@pytest.fixture(scope='module')
def app_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_customer(app_client):
    # Create a Customer 1
    customer_1 = {
        "title": "Mr",
        "name": "John Wick",
        "gender": "M",
        "phone_number": "08532222222255",
        "image": "https://img.freepik.com/free-photo/man-avatar-profile_24640-14044.jpg",
        "email": "john.doe@example.com"
    }
    response = app_client.post('/customer', json=customer_1)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    # Create a Customer 2
    customer_2 = {
        "title": "Mr",
        "name": "John Doe",
        "gender": "M",
        "phone_number": "08525252552",
        "image": "https://img.freepik.com/free-photo/man-avatar-profile_24640-14044.jpg",
        "email": "john.doe@example.com"
    }
    response = app_client.post('/customer', json=customer_2)   
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    # Get Customer List
    response = app_client.get('/customer')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    assert len(response_data['data']) == 2
    for customer in response_data['data']:
        assert 'customer_id' in customer
        assert 'title' in customer
        assert 'name' in customer
        assert 'gender' in customer
        assert 'phone_number' in customer
        assert 'image' in customer
        assert 'email' in customer
        assert 'created_at' in customer
        assert 'updated_at' in customer

    # Update Customer 1 data
    updated_customer = {
        "title": "Mr",
        "name": "Thomas Shelby",
        "gender": "M",
        "phone_number": str(generte_random_number()),
        "image": "https://img.freepik.com/premium-vector/man-avatar-profile-round-icon_24640-14044.jpg",
        "email": "adrien.philippe@gmail.com"
    }

    customer_1_obj = Customer.query.filter(Customer.name == customer_1.get("name")).first()
    response = app_client.patch(f'/customer/{str(customer_1_obj.customer_id)}', json=updated_customer)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    # Delete Customer 1
    response = app_client.delete(f'/customer/{str(customer_1_obj.customer_id)}')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    # Delete Customer 2
    customer_2_obj = Customer.query.filter(Customer.name == customer_2.get("name")).first()
    assert customer_2_obj is not None  # Ensure customer object is retrieved successfully
    response = app_client.delete(f'/customer/{str(customer_2_obj.customer_id)}')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'


def test_address(app_client):
    # Create a Customer 1
    customer_1 = {
        "title": "Mr",
        "name": "John Wick",
        "gender": "M",
        "phone_number": "08532222222255",
        "image": "https://img.freepik.com/free-photo/man-avatar-profile_24640-14044.jpg",
        "email": "john.doe@example.com"
    }
    response = app_client.post('/customer', json=customer_1)
    
    # Add new address for Customer 1  
    new_address = {
        "address" : "Kawasan Karyadeka Pancamurni Blok A Kav. 3",
        "district" : "Cikarang Selatan",
        "city" : "Jakarta Selatan",
        "province" : "DKI Jakarta",
        "postal_code" : 17530
        }

    response = app_client.post(f'/address?customer_id={1}', json=new_address)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    # Update Customer Data
    updated_customer = {
        "address" : "Kawasan Karyadeka Pancamurni Blok A Kav. 3",
        "district" : "Cikarang Selatan",
        "city" : "Bekasi",
        "province" : "Jawa Barat",
        "postal_code" : 17530
    }
    get_address_id = db_address_query.get_one_address_by_customer_id(1)
    response = app_client.patch(f'/address/{get_address_id.id}', json=updated_customer)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    # Delete Address Data
    response = app_client.delete(f'/address/{get_address_id.id}')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    # Delete Customer 1
    customer_1_obj = Customer.query.filter(Customer.name == customer_1.get("name")).first()
    response = app_client.delete(f'/customer/{str(customer_1_obj.customer_id)}')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
def generte_random_number():
    """
    Generate unique api call id
    """
    now_time = int(time.time())
    current_date = datetime.datetime.now()

    hour_tm = current_date.hour
    minute_tm = current_date.minute
    second_tm = current_date.second

    start_id = str(now_time) + str(hour_tm) + str(minute_tm) + str(second_tm)
    invoice_code = '{}'.format(str(start_id))
    return invoice_code


def test_customers_detail(app_client):
    # Create a Customer 1
    customer_1 = {
        "title": "Mr",
        "name": "John Wick",
        "gender": "M",
        "phone_number": "08532222222255",
        "image": "https://img.freepik.com/free-photo/man-avatar-profile_24640-14044.jpg",
        "email": "john.doe@example.com"
    }
    response = app_client.post('/customer', json=customer_1)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    # Add new address for Customer 1  
    new_address = {
        "address" : "Kawasan Karyadeka Pancamurni Blok A Kav. 3",
        "district" : "Cikarang Selatan",
        "city" : "Jakarta Selatan",
        "province" : "DKI Jakarta",
        "postal_code" : 17530
        }

    response = app_client.post(f'/address?customer_id={1}', json=new_address)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    # Get Customer Detail
    response = app_client.get('/customer/1')
    assert response.status_code == 200
    response_data = response.get_json()

    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'

    customer_1_obj = Customer.query.filter(Customer.name == customer_1.get("name")).first()
    get_address_id = db_address_query.get_one_address_by_customer_id(1)

    expected_data = {
        "data": {
            "address": [
                {
                    "address": "Kawasan Karyadeka Pancamurni Blok A Kav. 3",
                    "city": "Jakarta Selatan",
                    "district": "Cikarang Selatan",
                    "id": str(customer_1_obj.id),
                    "postal_code": 17530,
                    "province": "DKI Jakarta",
                }
            ],
            "title": "Mr",
            "name": "John Wick",
            "gender": "M",
            "phone_number": "08532222222255",
            "image": "https://img.freepik.com/free-photo/man-avatar-profile_24640-14044.jpg",
            "email": "john.doe@example.com"
    },
        "response_code": "SUCCESS",
        "response_message": "Success",
    }

    assert response_data['data']['name'] == expected_data['data']['name']
    assert response_data['data']['phone_number'] == expected_data['data']['phone_number']
    assert response_data['data']['email'] == expected_data['data']['email']
    assert response_data['data']['title'] == expected_data['data']['title']
    assert response_data['data']['gender'] == expected_data['data']['gender']
    assert response_data['data']['image'] == expected_data['data']['image']

    assert len(response_data['data']['address']) == 1
    assert response_data['data']['address'][0]['address'] == expected_data['data']['address'][0]['address']
    assert response_data['data']['address'][0]['city'] == expected_data['data']['address'][0]['city']
    assert response_data['data']['address'][0]['district'] == expected_data['data']['address'][0]['district']
    assert response_data['data']['address'][0]['postal_code'] == expected_data['data']['address'][0]['postal_code']
    assert response_data['data']['address'][0]['province'] == expected_data['data']['address'][0]['province']
    
    # Delete Address Data
    response = app_client.delete(f'/address/{get_address_id.id}')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    # Delete Customer 1
    customer_1_obj = Customer.query.filter(Customer.name == customer_1.get("name")).first()
    response = app_client.delete(f'/customer/{str(customer_1_obj.customer_id)}')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'