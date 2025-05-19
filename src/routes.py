from flask import Blueprint, render_template, request, redirect, url_for
from models import Artifact, db
from sqlalchemy import text

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

@app.route('/search', methods=['GET'])
def search_artifacts():
    query = request.args.get('q', '')

    # Vulnerable: Direct string concatenation in SQL query
    raw_sql = f"SELECT * FROM artifacts WHERE name LIKE '%{query}%' OR description LIKE '%{query}%'"
    
    with db.engine.connect() as connection:
        result = connection.execute(text(raw_sql))  # Direct execution of raw SQL
        artifacts = [dict(row._mapping) for row in result]
    
    return render_template('search_results.html', artifacts=artifacts, query=query)

# Fix (commented out):
# @app.route('/search', methods=['GET'])
# def search_artifacts():
#     query = request.args.get('q', '')
#     
#     # Safe: Using parameterized queries with SQLAlchemy ORM
#     artifacts = Artifact.query.filter(
#         (Artifact.name.ilike(f'%{query}%')) | 
#         (Artifact.description.ilike(f'%{query}%'))
#     ).all()
#     
#     return render_template('search_results.html', artifacts=artifacts, query=query)