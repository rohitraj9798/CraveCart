from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer')  # customer, restaurant_owner, admin
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    profile_image = db.Column(db.String(300), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='customer', lazy=True, foreign_keys='Order.customer_id')
    restaurant = db.relationship('Restaurant', backref='owner', uselist=False, foreign_keys='Restaurant.owner_id')
    reviews = db.relationship('Review', backref='reviewer', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'
