from extensions import db
from datetime import datetime

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    cuisine_type = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    image_url = db.Column(db.String(300), nullable=True)
    rating = db.Column(db.Float, default=0.0)
    total_ratings = db.Column(db.Integer, default=0)
    delivery_time = db.Column(db.Integer, default=30)  # minutes
    min_order = db.Column(db.Float, default=0)
    delivery_fee = db.Column(db.Float, default=30)
    is_approved = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    opening_time = db.Column(db.String(10), default='09:00')
    closing_time = db.Column(db.String(10), default='22:00')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    food_items = db.relationship('FoodItem', backref='restaurant', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='restaurant', lazy=True)
    reviews = db.relationship('Review', backref='restaurant', lazy=True)

    def avg_rating(self):
        if self.reviews:
            return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)
        return self.rating

    def __repr__(self):
        return f'<Restaurant {self.name}>'
