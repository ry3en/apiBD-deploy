from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
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

# Crea la base de datos se comenta despues
db.create_all()


class TaskSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "check")


taskSchema = TaskSchema()

taskSchema = TaskSchema(many=True)

tasks = [{}]

tareas = Task.query.all()
print(tareas)


@app.route("/")
def hello_world():
    return "Hola Mundo"


@app.route("/api/tasks/", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tareas})


@app.route("/api/tasks/" + "<int:id>", methods=["GET"])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({"task": task})


@app.route("/api/tasks/", methods=["POST"])
def create_task():
    if not request.json:
        abort(404)
    new_task = Task(name=request.json["name"], check=request.json["check"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task": new_task}), 201


@app.route("/api/tasks/" + "<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if not request.json:
        abort(400)

    task = Task.query.get_or_404(task_id)

    task.name = request.json["name"]
    task.check = request.json["check"]
    db.session.commit()

    return jsonify({"task": Task.as_dict(task)}), 201


@app.route("/api/tasks/" + "<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"result": True})


if __name__ == "__main__":
    app.run(debug=True)