from flask import Flask
from extensions import db, login_manager, bcrypt
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cravecart-secret-key-2024')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///cravecart.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from routes.auth import auth
    from routes.customer import customer
    from routes.restaurant import restaurant
    from routes.admin import admin
    from routes.api import api

    app.register_blueprint(auth)
    app.register_blueprint(customer)
    app.register_blueprint(restaurant, url_prefix='/restaurant')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(api, url_prefix='/api')

    with app.app_context():
        db.create_all()
        seed_data()

    return app

def seed_data():
    from models.user import User
    from models.restaurant import Restaurant
    from models.food_item import FoodItem
    from models.order import Order

    from app import bcrypt
    
    # Ensure Admin exists
    admin_user = db.session.query(User).filter_by(role='admin').first()
    if not admin_user:
        admin_user = User(name='Admin', email='admin@cravecart.com',
                     password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                     role='admin', phone='9999999999')
        db.session.add(admin_user)
        db.session.commit()

    # Global Restaurants Data
    global_restaurants = [
        {
            "name": "Spice Hut", "city": "Mumbai", "cuisine": "Indian",
            "desc": "Authentic Indian cuisine with bold flavors",
            "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400",
            "items": [
                {"name": "Butter Chicken", "price": 320, "veg": False, "cat": "Main Course", "img": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?w=300"},
                {"name": "Paneer Tikka", "price": 250, "veg": True, "cat": "Starters", "img": "https://images.unsplash.com/photo-1567158406597-9e487fb07222?w=300"}
            ]
        },
        {
            "name": "Sushi Zen", "city": "Tokyo", "cuisine": "Japanese",
            "desc": "Fresh, artistic sushi and sashimi",
            "img": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400",
            "items": [
                {"name": "Salmon Nigiri", "price": 450, "veg": False, "cat": "Sushi", "img": "https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=300"},
                {"name": "Miso Soup", "price": 120, "veg": True, "cat": "Soup", "img": "https://images.unsplash.com/photo-1548943487-a2e4142f1a30?w=300"}
            ]
        },
        {
            "name": "Le Central", "city": "Paris", "cuisine": "French",
            "desc": "Classic Parisian bistro experience",
            "img": "https://images.unsplash.com/photo-1550966841-3ee7adac1623?w=400",
            "items": [
                {"name": "Escargot", "price": 600, "veg": False, "cat": "Appetizer", "img": "https://images.unsplash.com/photo-1626082929543-5a41ebd48ebc?w=300"},
                {"name": "Ratatouille", "price": 480, "veg": True, "cat": "Main", "img": "https://images.unsplash.com/photo-1572453800999-e8d2d1589b7c?w=300"}
            ]
        },
        {
            "name": "The Burger Joint", "city": "New York", "cuisine": "American",
            "desc": "Best burgers in the heart of NYC",
            "img": "https://images.unsplash.com/photo-1586816001966-79b8367c4c87?w=400",
            "items": [
                {"name": "Classic Cheeseburger", "price": 350, "veg": False, "cat": "Burgers", "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300"},
                {"name": "Truffle Fries", "price": 180, "veg": True, "cat": "Sides", "img": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=300"}
            ]
        },
        {
            "name": "Pasta Bella", "city": "Rome", "cuisine": "Italian",
            "desc": "Hand-made pasta following nonna's recipes",
            "img": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=400",
            "items": [
                {"name": "Carbonara", "price": 420, "veg": False, "cat": "Pasta", "img": "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=300"},
                {"name": "Margherita Pizza", "price": 380, "veg": True, "cat": "Pizza", "img": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=300"}
            ]
        },
        {
            "name": "London Fish & Chips", "city": "London", "cuisine": "British",
            "desc": "A British staple since 1860",
            "img": "https://images.unsplash.com/photo-1524339322300-84a867702f25?w=400",
            "items": [
                {"name": "Cod & Chips", "price": 550, "veg": False, "cat": "Seafood", "img": "https://images.unsplash.com/photo-1596701550974-bc55848e4ff8?w=300"},
                {"name": "Mushy Peas", "price": 80, "veg": True, "cat": "Sides", "img": "https://plus.unsplash.com/premium_photo-1675271816005-4c07d3b51900?w=300"}
            ]
        },
        {
            "name": "Desert Oasis", "city": "Dubai", "cuisine": "Middle Eastern",
            "desc": "Luxurious dining with traditional Arabic flavors",
            "img": "https://images.unsplash.com/photo-1541544741938-0af808b77e40?w=400",
            "items": [
                {"name": "Lamb Mansaf", "price": 750, "veg": False, "cat": "Signature", "img": "https://images.unsplash.com/photo-1649980695039-3d1f1f9a110a?w=300"},
                {"name": "Hummus Platter", "price": 240, "veg": True, "cat": "Starters", "img": "https://images.unsplash.com/photo-1577906096429-f73c2c312435?w=300"}
            ]
        },
        {
            "name": "Beijing Duck House", "city": "Beijing", "cuisine": "Chinese",
            "desc": "Traditional Peking Duck carved table-side",
            "img": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400",
            "items": [
                {"name": "Peking Duck", "price": 850, "veg": False, "cat": "Specialty", "img": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=300"},
                {"name": "Vegetable Dumplings", "price": 220, "veg": True, "cat": "Dim Sum", "img": "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?w=300"}
            ]
        },
        {
            "name": "Sydney Harbour Grill", "city": "Sydney", "cuisine": "Australian",
            "desc": "Fresh seafood with a view of the Opera House",
            "img": "https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=400",
            "items": [
                {"name": "Grilled Barramundi", "price": 650, "veg": False, "cat": "Seafood", "img": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=300"},
                {"name": "Pavlova", "price": 280, "veg": True, "cat": "Dessert", "img": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=300"}
            ]
        },
        {
            "name": "Coyoacan Tacos", "city": "Mexico City", "cuisine": "Mexican",
            "desc": "Vibrant street food flavors from the heart of Mexico",
            "img": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400",
            "items": [
                {"name": "Tacos al Pastor", "price": 280, "veg": False, "cat": "Tacos", "img": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=300"},
                {"name": "Guacamole & Chips", "price": 150, "veg": True, "cat": "Appetizer", "img": "https://images.unsplash.com/photo-1522008342704-6b2db5cbabcc?w=300"}
            ]
        },
        {
            "name": "Siam Soul", "city": "Bangkok", "cuisine": "Thai",
            "desc": "Aromatic Thai spices and street food favorites",
            "img": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=400",
            "items": [
                {"name": "Pad Thai", "price": 300, "veg": False, "cat": "Noodles", "img": "https://images.unsplash.com/photo-1559314809-0d155014e29e?w=300"},
                {"name": "Mango Sticky Rice", "price": 180, "veg": True, "cat": "Dessert", "img": "https://images.unsplash.com/photo-1601000938259-9e41608eff78?w=300"}
            ]
        },
        {
            "name": "Bosphorus Bites", "city": "Istanbul", "cuisine": "Turkish",
            "desc": "Turkish delights and charcoal-grilled kebabs",
            "img": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400",
            "items": [
                {"name": "Adana Kebab", "price": 450, "veg": False, "cat": "Grill", "img": "https://images.unsplash.com/photo-1633365922097-9e79e6027a05?w=300"},
                {"name": "Baklava", "price": 220, "veg": True, "cat": "Dessert", "img": "https://images.unsplash.com/photo-1599813295831-7e39efd1c1bd?w=300"}
            ]
        },
        {
            "name": "Karim's", "city": "Delhi", "cuisine": "Mughlai",
            "desc": "Historic Mughlai flavors since 1913",
            "img": "https://images.unsplash.com/photo-1589135303429-23cf0a701918?w=400",
            "items": [
                {"name": "Mutton Korma", "price": 450, "veg": False, "cat": "Main Course", "img": "https://images.unsplash.com/photo-1582570089855-408a2ff5fb60?w=300"},
                {"name": "Khamiri Roti", "price": 40, "veg": True, "cat": "Bread", "img": "https://images.unsplash.com/photo-1626074353765-517a681e40be?w=300"}
            ]
        },
        {
            "name": "MTR (Mavalli Tiffin Rooms)", "city": "Bangalore", "cuisine": "South Indian",
            "desc": "Traditional Karnataka heritage restaurant",
            "img": "https://images.unsplash.com/photo-1626074353765-517a681e40be?w=400",
            "items": [
                {"name": "Rava Idli", "price": 120, "veg": True, "cat": "Breakfast", "img": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=300"},
                {"name": "Masala Dosa", "price": 150, "veg": True, "cat": "Mains", "img": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=300"}
            ]
        },
        {
            "name": "Saravana Bhavan", "city": "Chennai", "cuisine": "South Indian",
            "desc": "World-famous South Indian vegetarian meals",
            "img": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400",
            "items": [
                {"name": "Mini Tiffin", "price": 180, "veg": True, "cat": "Breakfast", "img": "https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?w=300"},
                {"name": "Parotta Kurma", "price": 140, "veg": True, "cat": "Mains", "img": "https://images.unsplash.com/photo-1625943555419-56a2cb596640?w=300"}
            ]
        },
        {
            "name": "Peter Cat", "city": "Kolkata", "cuisine": "Continental",
            "desc": "Legendary Park Street destination known for Chelo Kebab",
            "img": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=400",
            "items": [
                {"name": "Chelo Kebab", "price": 520, "veg": False, "cat": "Specialty", "img": "https://images.unsplash.com/photo-1603513689456-91e8ded0a38c?w=300"},
                {"name": "Chicken Steak", "price": 480, "veg": False, "cat": "Conti", "img": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=300"}
            ]
        },
        {
            "name": "Paradise Biryani", "city": "Hyderabad", "cuisine": "Hyderabadi",
            "desc": "The quintessential Hyderabadi Dum Biryani experience",
            "img": "https://images.unsplash.com/photo-1563379091339-0bfb16267714?w=400",
            "items": [
                {"name": "Special Mutton Biryani", "price": 420, "veg": False, "cat": "Biryani", "img": "https://images.unsplash.com/photo-1589302168068-964664d93cb0?w=300"},
                {"name": "Mirchi ka Salan", "price": 80, "veg": True, "cat": "Sides", "img": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=300"}
            ]
        },
        {
            "name": "German Bakery", "city": "Pune", "cuisine": "Cafe",
            "desc": "A vibrant cafe with exotic breads and pastries",
            "img": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400",
            "items": [
                {"name": "Red Velvet Cake", "price": 180, "veg": True, "cat": "Bakery", "img": "https://images.unsplash.com/photo-1586788224331-947f68671caf?w=300"},
                {"name": "Iced Peach Tea", "price": 120, "veg": True, "cat": "Beverages", "img": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=300"}
            ]
        },
        {
            "name": "Rawat Mishthan Bhandar", "city": "Jaipur", "cuisine": "Street Food",
            "desc": "Famous for the original Pyaaz Kachori",
            "img": "https://images.unsplash.com/photo-1601050638917-2708316df633?w=400",
            "items": [
                {"name": "Pyaaz Kachori", "price": 60, "veg": True, "cat": "Snacks", "img": "https://images.unsplash.com/photo-1626804475297-41609ea004eb?w=300"},
                {"name": "Ghevar", "price": 550, "veg": True, "cat": "Sweets", "img": "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=300"}
            ]
        },
        {
            "name": "Agashiye", "city": "Ahmedabad", "cuisine": "Gujarati",
            "desc": "Traditional Gujarati Thali on a terrace setting",
            "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400",
            "items": [
                {"name": "Full Gujarati Thali", "price": 950, "veg": True, "cat": "Thali", "img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=300"},
                {"name": "Dhokla Platter", "price": 250, "veg": True, "cat": "Snacks", "img": "https://images.unsplash.com/photo-1626159620586-b41300898be2?w=300"}
            ]
        }
    ]

    for r_data in global_restaurants:
        owner_email = f"owner_{r_data['name'].lower().replace(' ', '_')}@test.com"
        owner = db.session.query(User).filter_by(email=owner_email).first()
        if not owner:
            owner = User(name=f"{r_data['name']} Owner", email=owner_email,
                         password=bcrypt.generate_password_hash('owner123').decode('utf-8'),
                         role='restaurant_owner', phone='9876543210')
            db.session.add(owner)
            db.session.flush()

        rest = db.session.query(Restaurant).filter_by(name=r_data['name']).first()
        if not rest:
            rest = Restaurant(name=r_data['name'], owner_id=owner.id,
                              description=r_data['desc'],
                              address=f"Famous Street, {r_data['city']}", city=r_data['city'],
                              cuisine_type=r_data['cuisine'], rating=4.5 + (len(r_data['name']) % 5) * 0.1,
                              delivery_time=25 + (len(r_data['city']) % 10), min_order=150,
                              is_approved=True, is_active=True,
                              image_url=r_data['img'])
            db.session.add(rest)
            db.session.flush()

            for i_data in r_data['items']:
                item = FoodItem(name=i_data['name'], restaurant_id=rest.id, price=i_data['price'],
                               category=i_data['cat'], description=f"The best {i_data['name']} in {r_data['city']}",
                               is_veg=i_data['veg'], is_available=True, rating=4.7, image_url=i_data.get('img'))
                db.session.add(item)
    
    # Add a test order for Admin to track easily
    if admin_user and not db.session.query(Order).filter_by(customer_id=admin_user.id).first():
        test_rest = db.session.query(Restaurant).filter_by(name='Spice Hut').first()
        if test_rest:
            new_order = Order(customer_id=admin_user.id, restaurant_id=test_rest.id,
                             total_amount=500, delivery_fee=30, status='Preparing',
                             delivery_address='123 Admin Lane, Mumbai',
                             payment_method='COD')
            db.session.add(new_order)

    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
