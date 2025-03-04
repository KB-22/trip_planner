from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    visits = db.Column(db.Integer, default=0)

@app.route('/')
def home():
    places = Place.query.order_by(Place.visits.desc()).all()
    return render_template('home.html', places=places)

@app.route('/add', methods=['POST'])
def add_place():
    place_name = request.form.get('place')
    if place_name:
        new_place = Place(name=place_name, visits=0)
        db.session.add(new_place)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/visit/<int:place_id>')
def visit_place(place_id):
    place = Place.query.get(place_id)
    if place:
        place.visits += 1
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
