from flask import Flask, request, jsonify, render_template  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yourpassword@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

# Create the database and the database table
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # return "Hello"
    return render_template('todoweb.html')

@app.route('/tasks', methods=['GET'])   
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'name': task.name} for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    task_data = request.json
    new_task = Task(name=task_data['name'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'name': new_task.name}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task_data = request.json
    task = Task.query.get(id)
    if task:
        task.name = task_data['name']
        db.session.commit()
        return jsonify({'id': task.id, 'name': task.name})
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'})
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
