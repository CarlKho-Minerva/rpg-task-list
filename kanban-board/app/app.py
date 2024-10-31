from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import uuid
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
CORS(app)

DATABASE = "tasks.db"


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    with app.app_context():
        db = get_db()
        db.execute(
            """CREATE TABLE IF NOT EXISTS tasks
                      (id TEXT PRIMARY KEY, description TEXT, status TEXT)"""
        )
        db.commit()


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    db = get_db()
    tasks = db.execute("SELECT * FROM tasks").fetchall()
    return jsonify([dict(task) for task in tasks])


@app.route("/api/tasks", methods=["POST"])
def add_task():
    try:
        new_task = request.json
        if not new_task or "description" not in new_task or "status" not in new_task:
            raise BadRequest(
                "Invalid task data. 'description' and 'status' are required."
            )

        task_id = str(uuid.uuid4())
        db = get_db()
        db.execute(
            "INSERT INTO tasks (id, description, status) VALUES (?, ?, ?)",
            (task_id, new_task["description"], new_task["status"]),
        )
        db.commit()
        return jsonify({"id": task_id, **new_task}), 201
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route("/api/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        update_data = request.json
        if not update_data or "status" not in update_data:
            raise BadRequest("Invalid update data. 'status' is required.")

        db = get_db()
        db.execute(
            "UPDATE tasks SET status = ? WHERE id = ?", (update_data["status"], task_id)
        )
        db.commit()
        updated_task = db.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if updated_task:
            return jsonify(dict(updated_task))
        raise NotFound("Task not found")
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "An unexpected server error occurred"}), 500


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
