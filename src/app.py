import os
from flask import Flask
from flask_migrate import Migrate
from routes import app as routes_blueprint
from models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artifacts.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set a secret key for session management
    app.secret_key = os.urandom(24)  # Generates a random secret key

    db.init_app(app)
    app.register_blueprint(routes_blueprint)

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)