import os
import logging
from functools import wraps

from flask import Flask, send_from_directory, request, jsonify, g, make_response
from flask_cors import CORS
from pydantic import ValidationError

from database import get_connection, run_migrations
import crud
import auth_service
from schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectStatusUpdate,
    TaskCreate,
    LoginRequest,
)

# ─── Initialization ────────────────────────────────────────────────────────────

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder=None)
CORS(app, supports_credentials=True)

# Resolve directories relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Startup: run migrations once
try:
    logger.info("Running database migrations...")
    run_migrations()
    logger.info("Database migrations completed.")
except Exception as e:
    logger.error(f"Failed to run database migrations: {e}")


# ─── DB & Lifecycle ──────────────────────────────────────────────────────────

def get_db():
    if 'conn' not in g:
        g.conn = get_connection()
    return g.conn

@app.teardown_request
def teardown_db(exception):
    conn = g.pop('conn', None)
    if conn is not None:
        if exception:
            conn.rollback()
        conn.close()


# ─── Helpers ─────────────────────────────────────────────────────────────────

def json_error(status_code, detail):
    return jsonify({"detail": detail}), status_code

def _serialize(obj):
    """Recursively convert UUIDs, dates, datetimes to JSON-safe types."""
    from uuid import UUID
    from datetime import date, datetime

    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_serialize(i) for i in obj]
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return obj.isoformat()
    else:
        return obj

def _serialize_list(lst):
    return [_serialize(item) for item in lst]


# ─── Auth ────────────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = request.cookies.get("session_id")
        if not session_id:
            return json_error(401, "Not authenticated")
        
        conn = get_db()
        session = auth_service.get_session(conn, session_id)
        if not session:
            return json_error(401, "Session invalid or expired")
            
        user = auth_service.get_user_by_id(conn, session["user_id"])
        if not user:
            return json_error(401, "User not found")
            
        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function

@app.route("/api/auth/login", methods=["POST"])
def login_api():
    try:
        data = request.get_json() or {}
        body = LoginRequest(**data)
        conn = get_db()
        user = auth_service.get_user_by_username(conn, body.username)
        if not user or not auth_service.verify_password(body.password, user["password_hash"]):
            return json_error(401, "Invalid username or password")
        
        session = auth_service.create_session(conn, user["id"])
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie(
            key="session_id",
            value=session["token"],
            httponly=True,
            samesite="Lax",
            max_age=7*24*60*60
        )
        return response
    except ValidationError as e:
        return json_error(422, e.errors())
    except Exception as e:
        if 'conn' in g: g.conn.rollback()
        logger.error(f"Login error: {e}")
        return json_error(500, str(e))

@app.route("/api/auth/logout", methods=["POST"])
def logout_api():
    session_id = request.cookies.get("session_id")
    if session_id:
        conn = get_db()
        auth_service.delete_session(conn, session_id)
    response = make_response(jsonify({"message": "Logged out"}))
    response.delete_cookie("session_id")
    return response

@app.route("/api/auth/me", methods=["GET"])
@login_required
def get_me():
    user = g.current_user
    return jsonify({"id": str(user["id"]), "username": user["username"]})


# ─── Stats ───────────────────────────────────────────────────────────────────

@app.route("/api/stats", methods=["GET"])
@login_required
def get_stats():
    try:
        conn = get_db()
        return jsonify(_serialize(crud.get_stats(conn)))
    except Exception as e:
        logger.error(f"Get stats error: {e}")
        return json_error(500, str(e))


# ─── Projects ────────────────────────────────────────────────────────────────

@app.route("/api/projects", methods=["GET"])
@login_required
def list_projects():
    try:
        status = request.args.get("status")
        priority = request.args.get("priority")
        conn = get_db()
        projects = crud.get_all_projects(conn, status=status, priority=priority)
        return jsonify(_serialize_list(projects))
    except Exception as e:
        logger.error(f"List projects error: {e}")
        return json_error(500, str(e))

@app.route("/api/projects", methods=["POST"])
@login_required
def create_project():
    try:
        data = request.get_json() or {}
        body = ProjectCreate(**data)
        conn = get_db()
        project = crud.create_project(conn, body.model_dump())
        return jsonify(_serialize(project)), 201
    except ValidationError as e:
        return json_error(422, e.errors())
    except Exception as e:
        if 'conn' in g: g.conn.rollback()
        logger.error(f"Create project error: {e}")
        return json_error(500, str(e))

@app.route("/api/projects/<project_id>", methods=["GET"])
@login_required
def get_project(project_id):
    try:
        conn = get_db()
        project = crud.get_project_with_tasks(conn, project_id)
        if not project:
            return json_error(404, "Project not found")
        return jsonify(_serialize(project))
    except Exception as e:
        logger.error(f"Get project error: {e}")
        return json_error(500, str(e))

@app.route("/api/projects/<project_id>", methods=["PUT"])
@login_required
def update_project(project_id):
    try:
        data = request.get_json() or {}
        body = ProjectUpdate(**data)
        conn = get_db()
        
        existing = crud.get_project_by_id(conn, project_id)
        if not existing:
            return json_error(404, "Project not found")

        dumped = body.model_dump(exclude_unset=True)
        if "deadline" in dumped and dumped["deadline"] is not None:
            dumped["deadline"] = str(dumped["deadline"])

        project = crud.update_project(conn, project_id, dumped)
        if not project:
            return json_error(404, "Project not found")
        return jsonify(_serialize(project))
    except ValidationError as e:
        return json_error(422, e.errors())
    except Exception as e:
        if 'conn' in g: g.conn.rollback()
        logger.error(f"Update project error: {e}")
        return json_error(500, str(e))

@app.route("/api/projects/<project_id>", methods=["DELETE"])
@login_required
def delete_project(project_id):
    try:
        conn = get_db()
        deleted = crud.delete_project(conn, project_id)
        if not deleted:
            return json_error(404, "Project not found")
        return "", 204
    except Exception as e:
        if 'conn' in g: g.conn.rollback()
        logger.error(f"Delete project error: {e}")
        return json_error(500, str(e))

@app.route("/api/projects/<project_id>/status", methods=["PATCH"])
@login_required
def update_project_status(project_id):
    try:
        data = request.get_json() or {}
        body = ProjectStatusUpdate(**data)
        conn = get_db()
        
        project = crud.update_project_status(conn, project_id, body.status.value)
        if not project:
            return json_error(404, "Project not found")
        return jsonify(_serialize(project))
    except ValidationError as e:
        return json_error(422, e.errors())
    except Exception as e:
        if 'conn' in g: g.conn.rollback()
        logger.error(f"Update project status error: {e}")
        return json_error(500, str(e))


# ─── Tasks ───────────────────────────────────────────────────────────────────

@app.route("/api/projects/<project_id>/tasks", methods=["POST"])
@login_required
def add_task(project_id):
    try:
        data = request.get_json() or {}
        body = TaskCreate(**data)
        conn = get_db()
        
        existing = crud.get_project_by_id(conn, project_id)
        if not existing:
            return json_error(404, "Project not found")

        task = crud.create_task(conn, project_id, body.title)
        return jsonify(_serialize(task)), 201
    except ValidationError as e:
        return json_error(422, e.errors())
    except Exception as e:
        if 'conn' in g: g.conn.rollback()
        logger.error(f"Add task error: {e}")
        return json_error(500, str(e))

@app.route("/api/tasks/<task_id>/toggle", methods=["PATCH"])
@login_required
def toggle_task(task_id):
    try:
        conn = get_db()
        task = crud.toggle_task(conn, task_id)
        if not task:
            return json_error(404, "Task not found")
        return jsonify(_serialize(task))
    except Exception as e:
        if 'conn' in g: g.conn.rollback()
        logger.error(f"Toggle task error: {e}")
        return json_error(500, str(e))

@app.route("/api/tasks/<task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    try:
        conn = get_db()
        deleted = crud.delete_task(conn, task_id)
        if not deleted:
            return json_error(404, "Task not found")
        return "", 204
    except Exception as e:
        if 'conn' in g: g.conn.rollback()
        logger.error(f"Delete task error: {e}")
        return json_error(500, str(e))


# ─── Frontend & Static ───────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main dashboard HTML."""
    return send_from_directory(TEMPLATES_DIR, "index.html")

@app.route("/login")
def login_page():
    """Serve the login page."""
    return send_from_directory(TEMPLATES_DIR, "login.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    """Serve static frontend assets (CSS, JS, images)."""
    return send_from_directory(STATIC_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
