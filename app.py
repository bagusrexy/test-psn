from flask import Flask
from flask_migrate import Migrate
from models.db import db
from utils.logs import log_request_response

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)

    log_request_response(app)
    
    with app.app_context():
        db.create_all()

    from blueprint import check_health, customer, address
    app.register_blueprint(check_health.check_health_bp, url_prefix='/health')
    app.register_blueprint(customer.customer_bp)
    app.register_blueprint(address.address_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
