from fastapi import FastAPI, HTTPException, Query, Depends, Request, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

from database import get_connection, run_migrations
import crud
import auth_service
from schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectStatusUpdate,
    TaskCreate,
    StatsResponse,
    LoginRequest,
)

app = FastAPI(title="Kira Mission Tracker API", version="1.0.0")


# ─── CORS ────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Startup ─────────────────────────────────────────────────────────────────

@app.on_event("startup")
def startup_event():
    run_migrations()


# ─── Dependency ──────────────────────────────────────────────────────────────

def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


# ─── Auth ────────────────────────────────────────────────────────────────────

@app.post("/api/auth/login", tags=["Auth"])
def login(body: LoginRequest, response: Response, conn=Depends(get_db)):
    user = auth_service.get_user_by_username(conn, body.username)
    if not user or not auth_service.verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    session = auth_service.create_session(conn, user["id"])
    response.set_cookie(
        key="session_id",
        value=session["token"],
        httponly=True,
        samesite="lax",
        max_age=7*24*60*60
    )
    return {"message": "Login successful"}

@app.post("/api/auth/logout", tags=["Auth"])
def logout(response: Response, session_id: Optional[str] = Cookie(None), conn=Depends(get_db)):
    if session_id:
        auth_service.delete_session(conn, session_id)
    response.delete_cookie("session_id")
    return {"message": "Logged out"}

def get_current_user(session_id: Optional[str] = Cookie(None), conn=Depends(get_db)):
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    session = auth_service.get_session(conn, session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Session invalid or expired")
    user = auth_service.get_user_by_id(conn, session["user_id"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/api/auth/me", tags=["Auth"])
def get_me(user=Depends(get_current_user)):
    return {"id": str(user["id"]), "username": user["username"]}


# ─── Stats ───────────────────────────────────────────────────────────────────

@app.get("/api/stats", response_model=StatsResponse, tags=["Stats"])
def get_stats(conn=Depends(get_db), user=Depends(get_current_user)):
    try:
        return crud.get_stats(conn)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Projects ────────────────────────────────────────────────────────────────

@app.get("/api/projects", tags=["Projects"])
def list_projects(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    conn=Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        projects = crud.get_all_projects(conn, status=status, priority=priority)
        # Serialize UUIDs and dates for JSON
        return _serialize_list(projects)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects", status_code=201, tags=["Projects"])
def create_project(body: ProjectCreate, conn=Depends(get_db), user=Depends(get_current_user)):
    try:
        project = crud.create_project(conn, body.model_dump())
        return _serialize(project)
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}", tags=["Projects"])
def get_project(project_id: str, conn=Depends(get_db), user=Depends(get_current_user)):
    try:
        project = crud.get_project_with_tasks(conn, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return _serialize(project)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/projects/{project_id}", tags=["Projects"])
def update_project(project_id: str, body: ProjectUpdate, conn=Depends(get_db), user=Depends(get_current_user)):
    try:
        existing = crud.get_project_by_id(conn, project_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Project not found")

        data = body.model_dump(exclude_unset=True)
        # Convert date to string for psycopg2
        if "deadline" in data and data["deadline"] is not None:
            data["deadline"] = str(data["deadline"])

        project = crud.update_project(conn, project_id, data)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return _serialize(project)
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/projects/{project_id}", status_code=204, tags=["Projects"])
def delete_project(project_id: str, conn=Depends(get_db), user=Depends(get_current_user)):
    try:
        deleted = crud.delete_project(conn, project_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Project not found")
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/projects/{project_id}/status", tags=["Projects"])
def update_project_status(project_id: str, body: ProjectStatusUpdate, conn=Depends(get_db), user=Depends(get_current_user)):
    try:
        project = crud.update_project_status(conn, project_id, body.status.value)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return _serialize(project)
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ─── Tasks ───────────────────────────────────────────────────────────────────

@app.post("/api/projects/{project_id}/tasks", status_code=201, tags=["Tasks"])
def add_task(project_id: str, body: TaskCreate, conn=Depends(get_db), user=Depends(get_current_user)):
    try:
        existing = crud.get_project_by_id(conn, project_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Project not found")

        task = crud.create_task(conn, project_id, body.title)
        return _serialize(task)
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/tasks/{task_id}/toggle", tags=["Tasks"])
def toggle_task(task_id: str, conn=Depends(get_db), user=Depends(get_current_user)):
    try:
        task = crud.toggle_task(conn, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return _serialize(task)
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: str, conn=Depends(get_db), user=Depends(get_current_user)):
    try:
        deleted = crud.delete_task(conn, task_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ─── Serialization Helpers ───────────────────────────────────────────────────

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
