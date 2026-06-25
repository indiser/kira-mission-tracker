"""
CRUD operations using raw SQL with psycopg2.
All functions accept an open connection and return plain dicts / lists of dicts.
"""

from typing import Optional, List, Dict, Any


# ─── Projects ────────────────────────────────────────────────────────────────

def get_all_projects(
    conn,
    status: Optional[str] = None,
    priority: Optional[str] = None,
) -> List[Dict[str, Any]]:
    query = """
        SELECT
            p.id, p.title, p.description, p.status, p.priority,
            p.deadline, p.created_at, p.updated_at,
            COUNT(t.id) AS total_tasks,
            COUNT(t.id) FILTER (WHERE t.is_done = TRUE) AS done_tasks
        FROM projects p
        LEFT JOIN tasks t ON t.project_id = p.id
    """
    params = []
    conditions = []

    if status:
        conditions.append("p.status = %s")
        params.append(status)
    if priority:
        conditions.append("p.priority = %s")
        params.append(priority)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY p.id ORDER BY p.created_at DESC"

    with conn.cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()

    return [dict(r) for r in rows]


def get_project_by_id(conn, project_id: str) -> Optional[Dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM projects WHERE id = %s",
            (project_id,),
        )
        row = cur.fetchone()
    return dict(row) if row else None


def get_project_with_tasks(conn, project_id: str) -> Optional[Dict[str, Any]]:
    project = get_project_by_id(conn, project_id)
    if not project:
        return None

    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM tasks WHERE project_id = %s ORDER BY created_at ASC",
            (project_id,),
        )
        tasks = [dict(t) for t in cur.fetchall()]

    project["tasks"] = tasks
    return project


def create_project(conn, data: Dict[str, Any]) -> Dict[str, Any]:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO projects (title, description, status, priority, deadline)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
            """,
            (
                data["title"],
                data.get("description"),
                data.get("status", "active"),
                data.get("priority", "medium"),
                data.get("deadline"),
            ),
        )
        row = cur.fetchone()
    conn.commit()
    return dict(row)


def update_project(conn, project_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    # Build SET clause dynamically, tracking which keys are already queued
    fields = []
    params = []
    added_keys = set()

    for key in ("title", "description", "status", "priority", "deadline"):
        if key in data and data[key] is not None:
            fields.append(f"{key} = %s")
            params.append(data[key])
            added_keys.add(key)

    # Allow explicitly clearing nullable fields (description, deadline)
    for key in ("description", "deadline"):
        if key in data and data[key] is None and key not in added_keys:
            fields.append(f"{key} = %s")
            params.append(None)
            added_keys.add(key)

    if not fields:
        return get_project_by_id(conn, project_id)

    params.append(project_id)
    query = f"UPDATE projects SET {', '.join(fields)} WHERE id = %s RETURNING *"

    with conn.cursor() as cur:
        cur.execute(query, params)
        row = cur.fetchone()
    conn.commit()
    return dict(row) if row else None


def update_project_status(conn, project_id: str, status: str) -> Optional[Dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE projects SET status = %s WHERE id = %s RETURNING *",
            (status, project_id),
        )
        row = cur.fetchone()
    conn.commit()
    return dict(row) if row else None


def delete_project(conn, project_id: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM projects WHERE id = %s RETURNING id", (project_id,))
        row = cur.fetchone()
    conn.commit()
    return row is not None


# ─── Tasks ───────────────────────────────────────────────────────────────────

def create_task(conn, project_id: str, title: str) -> Dict[str, Any]:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO tasks (project_id, title)
            VALUES (%s, %s)
            RETURNING *
            """,
            (project_id, title),
        )
        row = cur.fetchone()
    conn.commit()
    return dict(row)


def toggle_task(conn, task_id: str) -> Optional[Dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE tasks SET is_done = NOT is_done WHERE id = %s RETURNING *",
            (task_id,),
        )
        row = cur.fetchone()
    conn.commit()
    return dict(row) if row else None


def delete_task(conn, task_id: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
        row = cur.fetchone()
    conn.commit()
    return row is not None


# ─── Stats ───────────────────────────────────────────────────────────────────

def get_stats(conn) -> Dict[str, Any]:
    with conn.cursor() as cur:
        # Total projects
        cur.execute("SELECT COUNT(*) AS total FROM projects")
        total = cur.fetchone()["total"]

        # Count by status
        cur.execute(
            "SELECT status, COUNT(*) AS cnt FROM projects GROUP BY status"
        )
        by_status_rows = cur.fetchall()
        by_status = {row["status"]: row["cnt"] for row in by_status_rows}

        # Count by priority
        cur.execute(
            "SELECT priority, COUNT(*) AS cnt FROM projects GROUP BY priority"
        )
        by_priority_rows = cur.fetchall()
        by_priority = {row["priority"]: row["cnt"] for row in by_priority_rows}

        # Overdue: deadline < today AND status != 'completed'
        cur.execute(
            """
            SELECT COUNT(*) AS cnt FROM projects
            WHERE deadline < CURRENT_DATE
              AND status != 'completed'
            """
        )
        overdue = cur.fetchone()["cnt"]

    return {
        "total_projects": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "overdue_count": overdue,
    }
