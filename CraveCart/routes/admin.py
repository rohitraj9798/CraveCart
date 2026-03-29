from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from extensions import db
from models import User, Restaurant, Order, FoodItem

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.filter_by(role='customer').count()
    total_restaurants = Restaurant.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter_by(status='Delivered').scalar() or 0
    pending_restaurants = Restaurant.query.filter_by(is_approved=False).all()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html',
                           total_users=total_users, total_restaurants=total_restaurants,
                           total_orders=total_orders, total_revenue=total_revenue,
                           pending_restaurants=pending_restaurants, recent_orders=recent_orders)

@admin.route('/restaurants')
@login_required
@admin_required
def restaurants():
    rests = Restaurant.query.all()
    return render_template('admin/restaurants.html', restaurants=rests)

@admin.route('/restaurant/<int:rid>/approve', methods=['POST'])
@login_required
@admin_required
def approve_restaurant(rid):
    rest = Restaurant.query.get_or_404(rid)
    rest.is_approved = True
    db.session.commit()
    flash(f'{rest.name} approved!', 'success')
    return redirect(url_for('admin.restaurants'))

@admin.route('/restaurant/<int:rid>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_restaurant(rid):
    rest = Restaurant.query.get_or_404(rid)
    rest.is_active = not rest.is_active
    db.session.commit()
    return jsonify({'active': rest.is_active})

@admin.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.all()
    return render_template('admin/users.html', users=all_users)

@admin.route('/orders')
@login_required
@admin_required
def orders():
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=all_orders)
