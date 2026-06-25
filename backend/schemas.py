from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID
from enum import Enum


class ProjectStatus(str, Enum):
    active = "active"
    paused = "paused"
    completed = "completed"
    dropped = "dropped"


class ProjectPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


# ─── Task Schemas ────────────────────────────────────────────────────────────

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class TaskResponse(BaseModel):
    id: UUID
    project_id: UUID
    title: str
    is_done: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Project Schemas ──────────────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.active
    priority: ProjectPriority = ProjectPriority.medium
    deadline: Optional[date] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    priority: Optional[ProjectPriority] = None
    deadline: Optional[date] = None


class ProjectStatusUpdate(BaseModel):
    status: ProjectStatus


class ProjectResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    status: ProjectStatus
    priority: ProjectPriority
    deadline: Optional[date]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectDetailResponse(ProjectResponse):
    tasks: List[TaskResponse] = []


# ─── Stats Schema ─────────────────────────────────────────────────────────────

class StatsResponse(BaseModel):
    total_projects: int
    by_status: dict
    by_priority: dict
    overdue_count: int

# ─── Auth Schema ──────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str
