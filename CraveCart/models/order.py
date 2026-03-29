from extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    status = db.Column(db.String(30), default='Pending')
    # Status: Pending, Accepted, Preparing, Out for Delivery, Delivered, Cancelled, Rejected
    total_amount = db.Column(db.Float, nullable=False)
    delivery_fee = db.Column(db.Float, default=30)
    delivery_address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50), default='COD')
    payment_status = db.Column(db.String(20), default='Pending')
    special_instructions = db.Column(db.Text, nullable=True)
    estimated_delivery = db.Column(db.Integer, default=45)  # minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    STATUS_FLOW = ['Pending', 'Accepted', 'Preparing', 'Out for Delivery', 'Delivered']
    STATUS_COLORS = {
        'Pending': 'warning',
        'Accepted': 'info',
        'Preparing': 'primary',
        'Out for Delivery': 'secondary',
        'Delivered': 'success',
        'Cancelled': 'danger',
        'Rejected': 'danger',
    }

    def next_status(self):
        if self.status in self.STATUS_FLOW:
            idx = self.STATUS_FLOW.index(self.status)
            if idx < len(self.STATUS_FLOW) - 1:
                return self.STATUS_FLOW[idx + 1]
        return None

    def __repr__(self):
        return f'<Order #{self.id} - {self.status}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.food_item_id} x{self.quantity}>'
