from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Restaurant, FoodItem, Order, OrderItem, Review

customer = Blueprint('customer', __name__)

@customer.route('/')
def home():
    restaurants = Restaurant.query.filter_by(is_approved=True, is_active=True).all()
    featured_items = FoodItem.query.filter_by(is_featured=True, is_available=True).limit(8).all()
    trending = FoodItem.query.filter_by(is_available=True).order_by(FoodItem.rating.desc()).limit(8).all()
    return render_template('customer/home.html', restaurants=restaurants,
                           featured_items=featured_items, trending=trending)

@customer.route('/restaurants')
def restaurants():
    search = request.args.get('search', '')
    city = request.args.get('city', '')
    cuisine = request.args.get('cuisine', '')
    query = Restaurant.query.filter_by(is_approved=True, is_active=True)
    if search:
        query = query.filter(Restaurant.name.ilike(f'%{search}%'))
    if city:
        query = query.filter(Restaurant.city.ilike(f'%{city}%'))
    if cuisine:
        query = query.filter(Restaurant.cuisine_type.ilike(f'%{cuisine}%'))
    rests = query.all()
    return render_template('customer/restaurants.html', restaurants=rests, search=search)

@customer.route('/restaurant/<int:rid>')
def restaurant_menu(rid):
    rest = Restaurant.query.get_or_404(rid)
    items = FoodItem.query.filter_by(restaurant_id=rid, is_available=True).all()
    categories = list(set(i.category for i in items))
    reviews = Review.query.filter_by(restaurant_id=rid).order_by(Review.created_at.desc()).limit(10).all()
    cart = session.get('cart', {})
    return render_template('customer/menu.html', restaurant=rest, items=items,
                           categories=categories, reviews=reviews, cart=cart)

@customer.route('/cart')
def cart():
    cart = session.get('cart', {})
    items_data = []
    total = 0
    for item_id, qty in cart.items():
        item = FoodItem.query.get(int(item_id))
        if item:
            subtotal = item.price * qty
            total += subtotal
            items_data.append({'item': item, 'qty': qty, 'subtotal': subtotal})
    delivery_fee = 30 if total > 0 else 0
    return render_template('customer/cart.html', items=items_data, total=total,
                           delivery_fee=delivery_fee, grand_total=total + delivery_fee)

@customer.route('/add-to-cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    cart = session.get('cart', {})
    key = str(item_id)
    cart[key] = cart.get(key, 0) + 1
    session['cart'] = cart
    return jsonify({'success': True, 'count': sum(cart.values())})

@customer.route('/update-cart', methods=['POST'])
def update_cart():
    data = request.get_json()
    cart = session.get('cart', {})
    item_id = str(data.get('item_id'))
    action = data.get('action')
    if action == 'increment':
        cart[item_id] = cart.get(item_id, 0) + 1
    elif action == 'decrement':
        if cart.get(item_id, 0) > 1:
            cart[item_id] -= 1
        else:
            cart.pop(item_id, None)
    elif action == 'remove':
        cart.pop(item_id, None)
    session['cart'] = cart
    return jsonify({'success': True, 'count': sum(cart.values())})

@customer.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('customer.home'))
    items_data = []
    total = 0
    restaurant_id = None
    for item_id, qty in cart.items():
        item = FoodItem.query.get(int(item_id))
        if item:
            subtotal = item.price * qty
            total += subtotal
            items_data.append({'item': item, 'qty': qty, 'subtotal': subtotal})
            restaurant_id = item.restaurant_id
    if request.method == 'POST':
        address = request.form.get('address')
        payment = request.form.get('payment', 'COD')
        instructions = request.form.get('instructions', '')
        delivery_fee = 30
        order = Order(customer_id=current_user.id, restaurant_id=restaurant_id,
                      total_amount=total, delivery_fee=delivery_fee,
                      delivery_address=address, payment_method=payment,
                      special_instructions=instructions)
        db.session.add(order)
        db.session.flush()
        for item_id, qty in cart.items():
            item = FoodItem.query.get(int(item_id))
            oi = OrderItem(order_id=order.id, food_item_id=item.id,
                           quantity=qty, unit_price=item.price,
                           subtotal=item.price * qty)
            db.session.add(oi)
        db.session.commit()
        session.pop('cart', None)
        flash(f'Order placed successfully! Order #{order.id}', 'success')
        return redirect(url_for('customer.order_tracking', order_id=order.id))
    delivery_fee = 30
    return render_template('customer/checkout.html', items=items_data, total=total,
                           delivery_fee=delivery_fee, grand_total=total + delivery_fee)

@customer.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(customer_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('customer/orders.html', orders=orders)

@customer.route('/order/<int:order_id>')
@login_required
def order_tracking(order_id):
    order = Order.query.get_or_404(order_id)
    if order.customer_id != current_user.id and current_user.role not in ['admin']:
        flash('Access denied.', 'danger')
        return redirect(url_for('customer.orders'))
    return render_template('customer/order_tracking.html', order=order)

@customer.route('/review/<int:order_id>', methods=['POST'])
@login_required
def submit_review(order_id):
    order = Order.query.get_or_404(order_id)
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '')
    existing = Review.query.filter_by(user_id=current_user.id, order_id=order_id).first()
    if not existing:
        review = Review(user_id=current_user.id, restaurant_id=order.restaurant_id,
                        order_id=order_id, rating=rating, comment=comment)
        db.session.add(review)
        db.session.commit()
        flash('Review submitted! Thank you.', 'success')
    return redirect(url_for('customer.order_tracking', order_id=order_id))
@customer.route('/profile')
@login_required
def profile():
    return render_template('customer/profile.html')
