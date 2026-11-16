from flask import Flask, jsonify, request, abort, Blueprint
import random 
import json 
import math

bp = Blueprint('search', __name__, url_prefix='/search')

json_file = 'data.json'
plant_data = json.load(open(json_file))

@bp.route('/name')
def search_by_name():
    params = request.args
    name = params.get('name')
    if not name:
        return jsonify( {'Error': 'Missing search text'}), 400

    plants = [ plant for plant in plant_data if name.lower() in plant['name'].lower() ]
    return jsonify(plants)


# Searches by price, care level 
@bp.route('/search')
def general_search():
    params = request.args

    print(params)

    # TODO Set at least one of min and max or will return everything 
    # TODO check for negative numbers? 
    try:
        min_price = int(params.get('min_price')) or 0
        max_price = int(params.get('max_price')) or math.inf
    except ValueError:
        return jsonify( {'Error': 'Prices must be integers'}), 400
    if min_price < 0 or max_price < 0:
        return jsonify( {'Error': 'Prices must be positive integers'}), 400

    care_level = params.get('care_level')  # May be None
    if care_level:
        care_level = care_level.lower() 
    if care_level not in ['easy', 'medium', 'difficult']:
        return jsonify( {'Error': 'Invalid care level "care_level"'}), 400

    plants = [ plant for plant in plant_data if min_price < plant['price'] < max_price ]
    plants = [ plant for plant in plants if care_level == plant['care_level'] ]

    return jsonify(plants)
