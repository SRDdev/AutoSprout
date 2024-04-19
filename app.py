from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database
db = SQLAlchemy(app)

class CounterLog(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    value = db.Column(db.Integer)

# Create the database tables
with app.app_context():
    db.create_all()

# Internal counter variable
internal_counter = 0

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
