from flask import Blueprint, render_template, request, redirect, url_for, session
from models import Artifact, db, User
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # Replace with hashed password check in production
            session['user'] = user.username
            session['is_admin'] = user.is_admin
            return redirect(url_for('app.index'))
        else:
            return "Invalid credentials", 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('app.index'))

@app.route('/admin')
def admin_dashboard():
    # Check if the user is logged in and is an admin
    if not session.get('user') or not session.get('is_admin'):
        return "Access Denied", 403

    artifacts = Artifact.query.all()
    return render_template('admin_dashboard.html', artifacts=artifacts)