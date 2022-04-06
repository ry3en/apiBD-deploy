import os
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# BD config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    check = db.Column(db.Boolean)

    def __init__(self, name, check):
        self.name = name
        self.check = check

    def __repr__(self):
        return '<Task %s>' % self.name


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'check')


tasksSchema = TaskSchema()  # Una sola tarea
tasks_Schema = TaskSchema(many=True)  # todas las tareas

@app.route('/api/tasks', methods=['Post'])
def create_task():
  title = request.json['title']
  check = request.json['description']

  new_task= Task(title, check)

  db.session.add(new_task)
  db.session.commit()

  return tasks_Schema.jsonify(new_task)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
  all_tasks = Task.query.all()
  result = tasks_Schema.dump(all_tasks)
  return jsonify(result)

@app.route('/api/tasks/<id>', methods=['GET'])
def get_task(id):
  task = Task.query.get(id)
  return tasksSchema.jsonify(task)

@app.route('/api/tasks/<id>', methods=['PUT'])
def update_task(id):
  task = Task.query.get(id)

  title = request.json['title']
  check = request.json['check']

  task.title = title
  task.check = check

  db.session.commit()

  return tasks_Schema.jsonify(task)

@app.route('/api/tasks/<id>', methods=['DELETE'])
def delete_task(id):
  task = Task.query.get(id)
  db.session.delete(task)
  db.session.commit()
  return tasksSchema.jsonify(task)


@app.route('/', methods=['GET'])
def index():
    return '<h1>Hola, bienvenido a mi API ToDO List<h1/>'

if __name__ == '__main__':
    app.run(debug=True)
