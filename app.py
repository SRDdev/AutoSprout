from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new.db'
db = SQLAlchemy(app)

class CounterLog(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    value = db.Column(db.Integer)

# Create the database tables
with app.app_context():
    db.create_all()

# Internal counter variable
internal_counter = 0

def get_table_names():
    table_names = []
    # Check if the database file exists
    if not os.path.exists('instance/new.db'):
        print("Error: Database file 'data.db' not found.")
        return table_names

    try:
        # Connect to the database
        conn = sqlite3.connect('instance/new.db')
        cursor = conn.cursor()

        # Execute a query to get the names of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Extract table names
        for row in rows:
            table_names.append(row[0])  # Table names are in the first column

    except sqlite3.OperationalError as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    return table_names

@app.route('/tables')
def display_tables():
    logs = CounterLog.query.all()
    tables = get_table_names()
    # Render the template with table names
    return render_template('database.html', logs=logs)

@app.route('/', methods=['POST'])
def update_counter():
    global internal_counter  # Accessing the global counter variable
    data = request.json
    if 'value' in data:
        sensor_value = data['value']
        # Log data into the database
        log = CounterLog(value=sensor_value)
        db.session.add(log)
        db.session.commit()
        internal_counter += 1  # Increment the internal counter
        return "Counter and sensor value updated successfully", 200
    else:
        return 'Invalid data format', 400

@app.route('/get_counter', methods=['GET'])
def get_counter():
    global internal_counter  # Accessing the global counter variable
    return jsonify({'internal_counter': internal_counter})

@app.route('/get_sensor_value', methods=['GET'])
def get_sensor_value():
    latest_log = CounterLog.query.order_by(CounterLog.id.desc()).first()
    if latest_log:
        sensor_value = latest_log.value
    else:
        sensor_value = 0
    return str(sensor_value)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
