from flask import Flask, Blueprint
from . import order_status, search 

def create_app(test_config=None):
    app = Flask(__name__)

    app.json.sort_keys = False
    
    app.register_blueprint(order_status.bp)
    app.register_blueprint(search.bp)

    return app


