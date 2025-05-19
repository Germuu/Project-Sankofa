from flask import Flask
from models import db
from sqlalchemy import text  # Import text for raw SQL queries

# Create a temporary Flask app for seeding
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artifacts.db'  # Use artifacts.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    # Manually insert data into the 'users' table
    db.session.execute(
        text("INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)"),
        {"username": "admin", "password": "password", "is_admin": True}
    )
    db.session.execute(
        text("INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)"),
        {"username": "user", "password": "password", "is_admin": False}
    )
    db.session.commit()

    print("Users seeded successfully!")