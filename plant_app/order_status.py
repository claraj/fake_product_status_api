from flask import Flask, jsonify, request, abort, Blueprint
import random 
import json 
from datetime import date, timedelta 

# Fake order tracking API. Generates random plant data, but should be the same for any given order number  

bp = Blueprint('orders', __name__, url_prefix='/orders')

# app = Flask(__name__)


statuses = ['processing', 'shipped', 'delivered', 'returned']

json_file = 'data.json'
plant_data = json.load(open(json_file))

@bp.route('/status')
def tracking_no_id():
    return jsonify( {'Error': 'Missing order number'}), 400


@bp.route('/status/<order_id>')
def tracking_invalid_id(order_id):
    return jsonify( {'Error': f'Invalid order number "{order_id}". Order numbers are 10 digits long'}), 400


@bp.route('/status/<int:order_id>')
def tracking(order_id):

    # Order IDs should be 10 numbers long
    if len(str(order_id)) != 10:
        return jsonify( {'Error': f'Invalid order number "{order_id}". Order numbers are 10 digits long'}), 400
    
    random.seed(order_id)

    # Generate 
    #    'order_date': order_date.isoformat(),
    #    'delivery_date': delivery_date,
    #    'status': status,
    #    'items': plant_order

    # order date must be today, or earlier   # TODO these dates will move as today changes, fix them relative to when generated
    today = date.today()
    days_ago_order = random.randint(0, 40) 
    order_date = today - timedelta(days=days_ago_order)

    status = random.choice(statuses)

    # Delivery date - only if order status is 'delivered', 'returned'
    delivery_date = None
    if status in ['delivered', 'returned']:
        delivery_date = (order_date + timedelta(days=3)).isoformat()

    # Items ordered
    plants = random.sample(plant_data, random.randint(1, 3))
    plant_order = [ { 'product': plant['name'], 'price': plant['price'], 'quantity': random.randint(1, 2)} for plant in plants ]

    return jsonify( {
        'order_number': order_id,
        'order_date': order_date.isoformat(),
        'delivery_date': delivery_date,
        'status': status,
        'items': plant_order
    })


@bp.errorhandler(404)
def page_not_found(error):
    return jsonify ({'Error': 'This page does not exist'} ), 404


# if __name__ == '__main__':
#     app.run(debug=True)

