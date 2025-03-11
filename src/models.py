from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Artifact(db.Model):
    __tablename__ = 'artifacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    historical_context = db.Column(db.Text, nullable=True)
    year_of_looting = db.Column(db.Integer, nullable=True)
    origin = db.Column(db.String(255), nullable=True)
    current_location = db.Column(db.String(255), nullable=True)
    repatriation_status = db.Column(db.String(255), nullable=True)

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