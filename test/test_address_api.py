import pytest
import json
from app import app, db
from models.customers import Customer
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
    
