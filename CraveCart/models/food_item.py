from extensions import db
from datetime import datetime

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=True)  # Veg, Non-Veg, Fast Food, Desserts
    image_url = db.Column(db.String(300), nullable=True)
    is_veg = db.Column(db.Boolean, default=True)
    is_available = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    is_featured = db.Column(db.Boolean, default=False)
    preparation_time = db.Column(db.Integer, default=15)  # minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = db.relationship('OrderItem', backref='food_item', lazy=True)

    def __repr__(self):
        return f'<FoodItem {self.name}>'

# Not a DB model - just a helper for categories
FOOD_CATEGORIES = ['Veg', 'Non-Veg', 'Fast Food', 'Desserts', 'Beverages', 'Starters', 'Breakfast']

class Category:
    pass
