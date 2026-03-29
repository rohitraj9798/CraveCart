🍔 CraveCart – Food Delivery Web Application

CraveCart is a full-stack food delivery web application that allows users to browse restaurants, explore menus, and place orders seamlessly. The project is designed with a focus on clean UI, responsiveness, and efficient backend processing using RESTful APIs.

---

## 🚀 Features

* Browse restaurants and menus
* Add to cart and manage orders
* Place orders smoothly
* Fully responsive design (mobile-friendly)
* REST API integration
* Fast and lightweight backend using Flask

---

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Responsive UI Design

### Backend

* Python (Flask)

### Database

* SQLite / MySQL

### Other Tools

* REST APIs

---

📂 Project Structure
CraveCart/
│
├── app/
│   ├── static/                # CSS, JS, Images
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── templates/            # HTML Templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── profile.html
│   │   ├── restaurants.html
│   │   └── orders.html
│   │
│   ├── routes/               # Application Routes
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── restaurant.py
│   │   └── order.py
│   │
│   ├── models/               # Database Models
│   │   ├── user_model.py
│   │   ├── restaurant_model.py
│   │   └── order_model.py
│   │
│   ├── utils/                # Helper Functions
│   │   └── helpers.py
│   │
│   └── _init_.py           # App Initialization
│
├── config.py                 # Configuration File
├── run.py                    # Entry Point
├── requirements.txt          # Dependencies
├── README.md                 # Project Documentation
└── database.db               # Database File


---

## ⚙️ Installation & Setup

1. Clone the repository

```
git clone https://github.com/rohitraj9798/CraveCart.git
```

2. Navigate to project folder

```
cd CraveCart
```

3. Create virtual environment

```
python -m venv venv
```

4. Activate virtual environment

* Windows:

```
venv\Scripts\activate
```

* Mac/Linux:

```
source venv/bin/activate
```

5. Install dependencies

```
pip install -r requirements.txt
```

6. Run the application

```
python app.py
```

7. Open in browser

```
http://127.0.0.1:5000/
```

---

## 🗄️ Database Setup

* Default: SQLite (no setup required)
* Optional: Configure MySQL in `app.py`

---

## 🎯 Future Improvements

* User authentication (Login/Signup)
* Payment gateway integration
* Live order tracking
* Ratings & reviews system

---

## 👨‍💻 Author

Developed by Rohit Raj

---
