from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Artifact(db.Model):
    __tablename__ = 'artifacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    historical_context = db.Column(db.Text)
    year_of_looting = db.Column(db.String(4))
    origin = db.Column(db.String(100))
    current_location = db.Column(db.String(100))
    repatriation_status = db.Column(db.String(100))
    photographs = db.Column(db.PickleType)  # Assuming photographs are stored as a list of dictionaries

    def __repr__(self):
        return f'<Artifact {self.name}>'

class RepatriationEffort(db.Model):
    __tablename__ = 'repatriation_efforts'

    id = db.Column(db.Integer, primary_key=True)
    artifact_id = db.Column(db.Integer, db.ForeignKey('artifacts.id'), nullable=False)
    negotiation_status = db.Column(db.String(255), nullable=True)
    date_initiated = db.Column(db.Date, nullable=True)
    date_completed = db.Column(db.Date, nullable=True)

    artifact = db.relationship('Artifact', backref='repatriation_efforts')

    def __repr__(self):
        return f'<RepatriationEffort for Artifact ID {self.artifact_id}>'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    is_admin = db.Column(db.Boolean, default=False)  # True for admin users

    def __repr__(self):
        return f'<User {self.username}>'