import logging
from datetime import datetime
from flask import request
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])

def log_request_response(app):
    @app.before_request
    def log_request():
        logging.info(f"Request Start: {request.method} {request.path} | Params: {request.args}")

    @app.after_request
    def log_response(response):
        logging.info(f"Request End: {request.method} {request.path} | Response: {response.status} | Message: {response.get_data(as_text=True)}")
        return response
