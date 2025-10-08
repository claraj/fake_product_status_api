from flask import Flask, jsonify, request, abort
import random 

# Fake order tracking API. Generates random data.  

app = Flask(__name__)

@app.route('/orders/status')
def tracking_no_id():
    return jsonify( {'Error': 'Missing order number'}), 400


@app.route('/orders/status/<int:order_id>')
def tracking(order_id):

    key = request.args.get('API_KEY')

    if not key:
        return jsonify( { 'Error': 'Missing API key'}), 403

    # any palindrome over 10 letters will work. TOP SECRET obviously. 
    if len(key) < 10 or len(key) % 2 != 0:
        return jsonify( { 'Error': 'Invalid API key'}), 403

    for x, y in zip( key, reversed(key)):
        print(x, y)
        if x != y:
            return jsonify( { 'Error': 'Invalid API key'}), 403

    statuses = ['processing', 'preparing', 'shipped', 'delivered', 'returned']
    items = ['Running Shoes', 'Jogging Pants', 'Athletic Socks', 'Baseball Cap', 'Print Hoodie', 'Logo T-Shirt']

    status = random.choice(statuses)
    order = random.sample(items, random.randint(1, len(items)-1))

    return jsonify( {
        'order_number': order_id,
        'status': status,
        'items': order
    })


@app.errorhandler(404)
def page_not_found(error):
    return jsonify ({'Error': 'This page does not exist'} ), 404


if __name__ == '__main__':
    app.run(debug=True)

