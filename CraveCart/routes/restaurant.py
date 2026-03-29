from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import Restaurant, FoodItem, Order, Review
from models.food_item import FOOD_CATEGORIES

restaurant = Blueprint('restaurant', __name__)

def owner_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'restaurant_owner':
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@restaurant.route('/dashboard')
@login_required
@owner_required
def dashboard():
    rest = Restaurant.query.filter_by(owner_id=current_user.id).first()
    if not rest:
        return redirect(url_for('restaurant.setup'))
    orders = Order.query.filter_by(restaurant_id=rest.id).order_by(Order.created_at.desc()).limit(20).all()
    total_revenue = sum(o.total_amount for o in Order.query.filter_by(restaurant_id=rest.id, status='Delivered').all())
    pending_count = Order.query.filter_by(restaurant_id=rest.id, status='Pending').count()
    return render_template('restaurant/dashboard.html', restaurant=rest, orders=orders,
                           total_revenue=total_revenue, pending_count=pending_count)

@restaurant.route('/setup', methods=['GET', 'POST'])
@login_required
@owner_required
def setup():
    if request.method == 'POST':
        rest = Restaurant(
            name=request.form['name'], owner_id=current_user.id,
            description=request.form.get('description'),
            address=request.form['address'], city=request.form['city'],
            cuisine_type=request.form.get('cuisine_type'),
            phone=request.form.get('phone'),
            image_url=request.form.get('image_url'),
            opening_time=request.form.get('opening_time', '09:00'),
            closing_time=request.form.get('closing_time', '22:00'),
            min_order=float(request.form.get('min_order', 0)),
            delivery_fee=float(request.form.get('delivery_fee', 30))
        )
        db.session.add(rest)
        db.session.commit()
        flash('Restaurant registered! Awaiting admin approval.', 'success')
        return redirect(url_for('restaurant.dashboard'))
    return render_template('restaurant/setup.html')

@restaurant.route('/menu')
@login_required
@owner_required
def menu():
    rest = Restaurant.query.filter_by(owner_id=current_user.id).first_or_404()
    items = FoodItem.query.filter_by(restaurant_id=rest.id).all()
    return render_template('restaurant/menu.html', restaurant=rest, items=items, categories=FOOD_CATEGORIES)

@restaurant.route('/menu/add', methods=['POST'])
@login_required
@owner_required
def add_item():
    rest = Restaurant.query.filter_by(owner_id=current_user.id).first_or_404()
    item = FoodItem(
        name=request.form['name'], restaurant_id=rest.id,
        description=request.form.get('description'),
        price=float(request.form['price']),
        category=request.form.get('category', 'Veg'),
        image_url=request.form.get('image_url'),
        is_veg=request.form.get('is_veg') == 'on',
        preparation_time=int(request.form.get('prep_time', 15))
    )
    db.session.add(item)
    db.session.commit()
    flash('Food item added!', 'success')
    return redirect(url_for('restaurant.menu'))

@restaurant.route('/menu/toggle/<int:item_id>', methods=['POST'])
@login_required
@owner_required
def toggle_item(item_id):
    item = FoodItem.query.get_or_404(item_id)
    item.is_available = not item.is_available
    db.session.commit()
    return jsonify({'available': item.is_available})

@restaurant.route('/menu/delete/<int:item_id>', methods=['POST'])
@login_required
@owner_required
def delete_item(item_id):
    item = FoodItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted.', 'info')
    return redirect(url_for('restaurant.menu'))

@restaurant.route('/orders')
@login_required
@owner_required
def orders():
    rest = Restaurant.query.filter_by(owner_id=current_user.id).first_or_404()
    status_filter = request.args.get('status', '')
    query = Order.query.filter_by(restaurant_id=rest.id)
    if status_filter:
        query = query.filter_by(status=status_filter)
    orders = query.order_by(Order.created_at.desc()).all()
    return render_template('restaurant/orders.html', orders=orders, status_filter=status_filter)

@restaurant.route('/order/<int:order_id>/update', methods=['POST'])
@login_required
@owner_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    order.status = new_status
    db.session.commit()
    flash(f'Order #{order.id} updated to {new_status}.', 'success')
    return redirect(url_for('restaurant.orders'))
