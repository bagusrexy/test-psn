import pytest
import json
from app import app, db
from models.customers import db_customer_query
from datetime import datetime

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
    new_customer = {
        "title": "Mr",
        "name": "John Doe",
        "gender": "M",
        "phone_number": "1234567890",
        "image": "https://img.freepik.com/free-photo/man-avatar-profile_24640-14044.jpg",
        "email": "john.doe@example.com"
    }

    response = app_client.post('/customer', json=new_customer)
    new_customer = {
        "title": "Mr",
        "name": "John Doe",
        "gender": "M",
        "phone_number": "12345678901",
        "image": "https://img.freepik.com/free-photo/man-avatar-profile_24640-14044.jpg",
        "email": "john.doe@example.com"
    }

    response = app_client.post('/customer', json=new_customer)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    updated_customer = {
        "title": "Mr",
        "name": "Thomas Shelby",
        "gender": "M",
        "phone_number": "08522233422",
        "image": "https://img.freepik.com/premium-vector/man-avatar-profile-round-icon_24640-14044.jpg",
        "email": "adrien.philippe@gmail.com"
    }
    
    response = app_client.get('/customer', json=new_customer)
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

    response = app_client.patch('/customer/1', json=updated_customer)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    response = app_client.delete('/customer/1')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    response = app_client.delete('/customer/2')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
def test_get_customer_detail(app_client):
    new_customer = {
        "title": "Mr",
        "name": "Jokowi Dodol",
        "gender": "F",
        "phone_number": "08123451112",
        "image": "https://img.freepik.com/premium-vector/man-avatar-profile-round-icon_24640-14044.jpg",
        "email": "adrien.philippe@mail.com"
    }
    response = app_client.post('/customer', json=new_customer)
    assert response.status_code == 200
    customer_id = db_customer_query.get_customer_by_name(new_customer.get('name'))

    new_address = {
        "address": "Kawasan Karyadeka Pancamurni Blok A Kav. 3",
        "district": "Cikarang Selatan",
        "city": "Jakarta Selatan",
        "province": "DKI Jakarta",
        "postal_code": 17530
    }
    response = app_client.post(f'/address?customer_id={str(customer_id.customer_id)}', json=new_address)
    assert response.status_code == 200

    response = app_client.get(f'/customer/{customer_id.customer_id}')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'

    customer_data = response_data['data']
    assert customer_data['id'] == customer_id
    assert customer_data['title'] == new_customer['title']
    assert customer_data['name'] == new_customer['name']
    assert customer_data['gender'] == new_customer['gender']
    assert customer_data['phone_number'] == new_customer['phone_number']
    assert customer_data['image'] == new_customer['image']
    assert customer_data['email'] == new_customer['email']
    assert 'created_at' in customer_data
    assert 'updated_at' in customer_data
    

    addresses = customer_data['address']
    assert len(addresses) == 1 
    address = addresses[0]
    assert address['address'] == new_address['address']
    assert address['district'] == new_address['district']
    assert address['city'] == new_address['city']
    assert address['province'] == new_address['province']
    assert address['postal_code'] == new_address['postal_code']
    assert 'created_at' in address
    assert 'updated_at' in address

def test_address(app_client):
    new_address = {
        "address" : "Kawasan Karyadeka Pancamurni Blok A Kav. 3",
        "district" : "Cikarang Selatan",
        "city" : "Jakarta Selatan",
        "province" : "DKI Jakarta",
        "postal_code" : 17530
        }

    response = app_client.post('/address', json=new_address)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'
    
    updated_customer = {
        "address" : "Kawasan Karyadeka Pancamurni Blok A Kav. 3",
        "district" : "Cikarang Selatan",
        "city" : "Bekasi",
        "province" : "Jawa Barat",
        "postal_code" : 17530
    }
    
    response = app_client.patch('/address', json=updated_customer)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'

    response = app_client.delete('/customer/1')
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['response_code'] == 'SUCCESS'
    assert response_data['response_message'] == 'Success'