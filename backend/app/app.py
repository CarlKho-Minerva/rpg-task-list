from flask import Flask, request, jsonify, session
from flask_cors import CORS
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

DATABASE_URL = "sqlite:///tasks.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    tasks = relationship('Task', back_populates='user')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(String, primary_key=True)
    description = Column(String)
    status = Column(String)
    user_id = Column(String, ForeignKey('users.id'))
    user = relationship('User', back_populates='tasks')

Base.metadata.create_all(engine)

@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.json
        if not data or "username" not in data or "password" not in data:
            raise BadRequest("Invalid registration data. 'username' and 'password' are required.")

        username = data["username"]
        password = data["password"]
        if db_session.query(User).filter_by(username=username).first():
            raise BadRequest("Username already exists.")

        user_id = str(uuid.uuid4())
        password_hash = generate_password_hash(password)
        user = User(id=user_id, username=username, password_hash=password_hash)
        db_session.add(user)
        db_session.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data or "username" not in data or "password" not in data:
            raise BadRequest("Invalid login data. 'username' and 'password' are required.")

        username = data["username"]
        password = data["password"]
        user = db_session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return jsonify({"message": "Login successful."}), 200
        raise BadRequest("Invalid username or password.")
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful."}), 200

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    tasks = db_session.query(Task).filter_by(user_id=user_id).all()
    return jsonify([{"id": task.id, "description": task.description, "status": task.status} for task in tasks])

@app.route("/api/tasks", methods=["POST"])
def add_task():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        new_task = request.json
        if not new_task or "description" not in new_task or "status" not in new_task:
            raise BadRequest("Invalid task data. 'description' and 'status' are required.")

        task_id = str(uuid.uuid4())
        task = Task(id=task_id, description=new_task["description"], status=new_task["status"], user_id=user_id)
        db_session.add(task)
        db_session.commit()
        return jsonify({"id": task_id, **new_task}), 201
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route("/api/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        update_data = request.json
        if not update_data or "status" not in update_data:
            raise BadRequest("Invalid update data. 'status' is required.")

        task = db_session.query(Task).filter_by(id=task_id, user_id=user_id).first()
        if task:
            task.status = update_data["status"]
            db_session.commit()
            return jsonify({"id": task.id, "description": task.description, "status": task.status})
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
