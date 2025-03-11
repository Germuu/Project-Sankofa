from flask import Blueprint, render_template, request, redirect, url_for
from models import Artifact, db

app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_artifact', methods=['POST'])
def add_artifact():
    name = request.form['name']
    description = request.form['description']
    historical_context = request.form.get('historical_context')
    year_of_looting = request.form.get('year_of_looting')
    origin = request.form.get('origin')
    current_location = request.form.get('current_location')
    repatriation_status = request.form.get('repatriation_status')

    new_artifact = Artifact(
        name=name,
        description=description,
        historical_context=historical_context,
        year_of_looting=year_of_looting,
        origin=origin,
        current_location=current_location,
        repatriation_status=repatriation_status
    )
    db.session.add(new_artifact)
    db.session.commit()
    return redirect(url_for('app.artifact_database'))

@app.route('/artifacts')
def artifact_database():
    artifacts = Artifact.query.all()
    return render_template('artifact_database.html', artifacts=artifacts)

@app.route('/artifact/<int:id>')
def artifact_detail(id):
    artifact = Artifact.query.get_or_404(id)
    return render_template('artifact.html', artifact=artifact)

@app.route('/map')
def interactive_map():
    return render_template('map.html')