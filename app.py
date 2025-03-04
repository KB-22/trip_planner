from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "trip_planner_db",
    "user": "your_username",
    "password": "your_password",
    "host": "your_host",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/', methods=['GET'])
def home():
    search_query = request.args.get('query', '')

    conn = get_db_connection()
    cur = conn.cursor()

    if search_query:
        cur.execute("SELECT * FROM places WHERE name ILIKE %s", ('%' + search_query + '%',))
    else:
        cur.execute("SELECT * FROM places ORDER BY id DESC")

    places = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('home.html', places=[{"name": p[1], "description": p[2]} for p in places])

@app.route('/add_place', methods=['POST'])
def add_place():
    place_name = request.form['place_name']
    district = request.form['district']
    description = request.form['description']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO places (name, district, description) VALUES (%s, %s, %s)", 
                (place_name, district, description))
    conn.commit()
    cur.close()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)