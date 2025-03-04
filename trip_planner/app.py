from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use environment variable for security
DATABASE_URL = "postgresql://trip_planner_db_e5dt_user:Eff1WCXnhXz1EkzpWpjfPYmSIVlHXQtF@dpg-cv3bs83tq21c73biscc0-a/trip_planner_db_e5dt"

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a database model
class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return "Trip Planner is Live with Database!"

if __name__ == "__main__":
    app.run(debug=True)
