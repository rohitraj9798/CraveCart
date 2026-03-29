# 🍔 CraveCart — Food Delivery Web Application

A full-stack food delivery platform built with **Flask** (Python) + modern HTML/CSS/JS frontend.

---

## 🚀 Quick Setup

### Prerequisites
- Python 3.9+
- pip

### 1. Install dependencies
```bash
cd cravecart
pip install -r requirements.txt
```

### 2. Run the application
```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 🔑 Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@cravecart.com | admin123 |
| Restaurant Owner | raj@spicehut.com | owner123 |
| Customer | Register a new account | — |

---

## 📁 Project Structure

```
cravecart/
├── app.py                    # App factory, seed data
├── requirements.txt
├── models/
│   ├── user.py               # User model (Customer/Admin/Owner)
│   ├── restaurant.py         # Restaurant model
│   ├── food_item.py          # FoodItem model
│   ├── order.py              # Order + OrderItem models
│   └── review.py             # Review model
├── routes/
│   ├── auth.py               # Login, Register, Logout
│   ├── customer.py           # Home, Menu, Cart, Checkout, Orders
│   ├── restaurant.py         # Owner Dashboard, Menu Mgmt, Orders
│   ├── admin.py              # Admin Dashboard, Approvals
│   └── api.py                # REST API endpoints
└── templates/
    ├── base.html             # Shared layout
    ├── auth/                 # Login + Register pages
    ├── customer/             # Home, Menu, Cart, Checkout, Orders
    ├── restaurant/           # Owner Dashboard, Menu, Orders
    └── admin/                # Admin Dashboard, Users, Restaurants, Orders
```

---

## 🗄️ Database Schema

**User** — id, name, email, phone, password(hashed), role, address, city, is_active  
**Restaurant** — id, owner_id, name, description, address, city, cuisine_type, rating, delivery_time, min_order, delivery_fee, is_approved, is_active  
**FoodItem** — id, restaurant_id, name, description, price, category, image_url, is_veg, is_available, rating  
**Order** — id, customer_id, restaurant_id, status, total_amount, delivery_fee, delivery_address, payment_method, special_instructions  
**OrderItem** — id, order_id, food_item_id, quantity, unit_price, subtotal  
**Review** — id, user_id, restaurant_id, order_id, rating, comment

---

## ✨ Features

### Customer
- Browse restaurants with search & filters
- View menus by category (Veg/Non-Veg)
- Real-time cart with quantity controls
- Checkout with address & payment selection
- Live order tracking with status updates
- Order history & review submission

### Restaurant Owner
- Register restaurant (admin-reviewed)
- Add/edit/delete menu items with images
- Toggle item availability
- Accept/update order status
- Revenue & analytics dashboard

### Admin
- Approve new restaurant registrations
- Monitor all users, restaurants & orders
- Platform-wide analytics
- Toggle restaurant active status

---

## 🔧 Configuration

Set environment variables:
```bash
export SECRET_KEY="your-secure-secret-key"
export DATABASE_URL="sqlite:///cravecart.db"  # or PostgreSQL URL
```

For PostgreSQL:
```bash
pip install psycopg2-binary
export DATABASE_URL="postgresql://user:pass@localhost/cravecart"
```

---

## 📱 Optional Enhancements

- **Razorpay/Stripe** — Add `razorpay` to requirements.txt and integrate in checkout route
- **Real-time tracking** — Use Flask-SocketIO for live order status push
- **Image uploads** — Use Flask-Uploads or store to S3/Cloudinary
- **SMS OTP** — Integrate Twilio for phone verification
- **Maps** — Add Google Maps API for location-based filtering

---

## 🏗️ Production Deployment

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

Use with Nginx as reverse proxy. Deploy to Railway, Render, or any VPS.

---

Made with ❤️ by CraveCart
