from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration (Using SQLite for local testing)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///places.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model for Places
class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    visit_count = db.Column(db.Integer, default=0)

# Create database tables
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def index():
    places = Place.query.order_by(Place.visit_count.desc()).all()
    return render_template('index.html', places=places)

# Add a Place
@app.route('/add', methods=['POST'])
def add_place():
    name = request.form['name']
    location = request.form['location']
    new_place = Place(name=name, location=location)
    db.session.add(new_place)
    db.session.commit()
    return redirect(url_for('index'))

# Increase Visit Count
@app.route('/visit/<int:place_id>')
def visit_place(place_id):
    place = Place.query.get_or_404(place_id)
    place.visit_count += 1
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
