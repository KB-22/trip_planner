from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://trip_planner_db_e5dt_user:Eff1WCXnhXz1EkzpWpjfPYmSIVlHXQtF@dpg-cv3bs83tq21c73biscc0-a/trip_planner_db_e5dt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)  # Added missing column
    visit_count = db.Column(db.Integer, default=0)

# Ensure database tables are created
with app.app_context():
    db.create_all()

# Home Page - Show Places Ordered by Visit Count
@app.route('/')
def index():
    places = Place.query.order_by(Place.visit_count.desc()).all()
    return render_template('index.html', places=places)

# Add New Place (No Authentication, Open to Public)
@app.route('/add_place', methods=['POST'])
def add_place():
    name = request.form['name']
    location = request.form['location']

    if name and location:
        new_place = Place(name=name, location=location)
        db.session.add(new_place)
        db.session.commit()
    
    return redirect('/')

# Increase Visit Count
@app.route('/visit/<int:place_id>')
def visit_place(place_id):
    place = Place.query.get(place_id)
    if place:
        place.visit_count += 1
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
