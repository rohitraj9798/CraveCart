from flask import Blueprint, jsonify, request
from models import Restaurant, FoodItem, Order

api = Blueprint('api', __name__)

@api.route('/restaurants/search')
def search_restaurants():
    q = request.args.get('q', '')
    rests = Restaurant.query.filter(
        Restaurant.name.ilike(f'%{q}%'),
        Restaurant.is_approved == True
    ).limit(10).all()
    return jsonify([{
        'id': r.id, 'name': r.name, 'cuisine': r.cuisine_type,
        'rating': r.rating, 'delivery_time': r.delivery_time
    } for r in rests])

@api.route('/order/<int:order_id>/status')
def order_status(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({'status': order.status, 'updated_at': order.updated_at.isoformat()})

@api.route('/cart/count')
def cart_count():
    from flask import session
    cart = session.get('cart', {})
    return jsonify({'count': sum(cart.values())})
