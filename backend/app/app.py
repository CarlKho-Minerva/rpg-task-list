from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
CORS(app)

DATABASE_URL = "sqlite:///tasks.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True)
    description = Column(String)
    status = Column(String)


Base.metadata.create_all(engine)


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = session.query(Task).all()
    return jsonify(
        [
            {"id": task.id, "description": task.description, "status": task.status}
            for task in tasks
        ]
    )


@app.route("/api/tasks", methods=["POST"])
def add_task():
    try:
        new_task = request.json
        if not new_task or "description" not in new_task or "status" not in new_task:
            raise BadRequest(
                "Invalid task data. 'description' and 'status' are required."
            )

        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id, description=new_task["description"], status=new_task["status"]
        )
        session.add(task)
        session.commit()
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

        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            task.status = update_data["status"]
            session.commit()
            return jsonify(
                {"id": task.id, "description": task.description, "status": task.status}
            )
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
    Base.metadata.create_all(engine)
    app.run(debug=True, port=5000)
