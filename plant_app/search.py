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


# Searches by price
@bp.route('/price')
def price_search():
    params = request.args

    print(params)

    # TODO Set at least one of min and max or will return everything 
    # TODO check for negative numbers? 
    try:
        min_price = float(params.get('min_price') or 0)
        max_price = float(params.get('max_price') or math.inf)
    except ValueError:
        return jsonify( {'Error': 'Prices must be numbers'}), 400
    if min_price < 0 or max_price < 0:
        return jsonify( {'Error': 'Prices must be positive numbers'}), 400
    if min_price > max_price:
        return jsonify( {'Error': 'Min price must be less than max price'}), 400

    plants = [ plant for plant in plant_data if min_price <= plant['price'] <= max_price ]

    return jsonify(plants)


# Searches by care level. Accepts multiple levels, separated by ; 
@bp.route('/care')
def care_search():
    params = request.args
    care_level = params.get('care_level')
    if not care_level:
        return jsonify( {'Error': 'Care level must be provided'}), 400

    care_levels = care_level.split(';')

    for level in care_levels:    
        if level not in ['easy', 'medium', 'difficult']:
            return jsonify( {'Error': 'Care level(s) must be one of "easy", "medium", "difficult"'}), 400

    matches = []
    for plant in plant_data:
        if plant['care']['care_level'] in care_levels:
            matches.append(plant)

    return jsonify(matches)
