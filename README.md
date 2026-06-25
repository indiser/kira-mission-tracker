<div align="center">

# 🎯 Kira Mission Tracker

**A Full-Stack Personal Project Management System**

*Built with Flask · PostgreSQL · Vanilla JavaScript*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

*Mission Control Dashboard for Your Personal Projects*

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [Security Features](#-security-features)
- [UI/UX Design](#-uiux-design)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**Kira Mission Tracker** is a modern, full-stack personal project management application designed with a cinematic, anime-inspired UI aesthetic. Built on Flask with a unified architecture, it provides real-time project tracking, task management, and comprehensive analytics through an immersive "Mission Control" dashboard experience.

### Why This Project?

- **Unified Flask Architecture**: Single server handles both API and frontend (simplified deployment)
- **Mission Control Interface**: Dual-view system with read-only dashboard + edit override mode
- **Modern UI/UX**: Inspired by AAA game interfaces and anime aesthetics
- **Real-time Updates**: Optimistic UI updates for instant feedback
- **Secure Authentication**: Session-based authentication with HTTP-only cookies and automatic redirects
- **Production-Ready**: Built with PostgreSQL/NeonDB for scalability
- **Zero Framework Frontend**: Pure Vanilla JavaScript with no dependencies

---

## ✨ Key Features

### 🎯 Project Management
- **Create, Read, Update, Delete (CRUD)** operations for projects
- **Status Tracking**: Active, Paused, Completed, Dropped with color-coded badges
- **Priority Levels**: Low, Medium, High, Critical with visual indicators
- **Deadline Management**: Set and track project deadlines with overdue alerts
- **Filtering**: Real-time filtering by status and priority

### ✅ Task Management
- **Sub-task Creation**: Break down projects into manageable tasks
- **Progress Tracking**: Visual progress bars and circular SVG rings showing task completion
- **Toggle Completion**: Instant task status updates with optimistic UI
- **Task Deletion**: Remove tasks with smooth animations
- **Empty States**: Elegant "No tasks" state with Japanese kanji

### 📊 Analytics Dashboard (Mission Control)
- **Live Statistics**: Total projects, active, completed, and overdue counts with real-time updates
- **Mission Rank System**: Gamified ranking based on task completion (S, A, B, C ranks) with dynamic colors
- **Progress Visualization**: Circular SVG progress rings and horizontal bars
- **Achievement System**: Unlock achievements as you progress (Project Initiated, Milestone Alpha)
- **Dual View System**: 
  - **Read-Only Mission Control View**: Hero banner, 3-column dashboard layout, mission timeline
  - **Edit Override Mode**: Form-based editing with system override aesthetics and neon accents
- **AI Summary Section**: Placeholder for future AI-powered project insights

### 🔐 Authentication & Security
- **Session-based Authentication**: Secure HTTP-only cookies with 7-day expiration
- **Password Hashing**: PBKDF2-HMAC-SHA256 with 100,000 iterations and random salt
- **Protected Routes**: All API endpoints require authentication (except login)
- **Auto-redirect**: Instant redirect to login on authentication failure via global fetch interceptor
- **Remember Me**: Option to persist sessions
- **Profile Menu**: User profile dropdown with system preferences and logout

### 🎨 UI/UX Excellence
- **Cinematic Interface**: AAA game-inspired design language with sci-fi aesthetics
- **Anime Aesthetics**: Japanese typography (Noto Sans JP), neon accents, glass morphism
- **Smooth Animations**: Spring physics, parallax effects, 3D transforms, staggered card entrances
- **Responsive Design**: Fully responsive from mobile to desktop with Tailwind CSS
- **Dark Theme**: Eye-friendly dark mode with vibrant accent colors (Sakura pink, Kira blue)
- **Toast Notifications**: Slide-up notifications with auto-dismiss for all actions
- **Loading States**: Three-dot floating anime loaders for all async operations
- **Empty States**: Elegant empty state designs with Japanese kanji (無 - "nothing")
- **Password Toggle**: Eye icon to show/hide passwords on login
- **Floating Labels**: Material-design inspired input labels with smooth animations
- **Backdrop Blur**: Glassmorphism effects throughout the UI
- **Animated Particles**: Background particle system on login page
- **Confirm Dialogs**: Purge Protocol modal for destructive actions

---

## 🛠 Tech Stack

### Backend (Flask)

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Web Framework** | Flask | Lightweight WSGI web application framework |
| **CORS** | Flask-CORS | Cross-Origin Resource Sharing support |
| **Database** | PostgreSQL (NeonDB) | Serverless PostgreSQL database |
| **Database Driver** | psycopg2-binary | PostgreSQL adapter for Python with RealDictCursor |
| **Schema Validation** | Pydantic | Data validation and settings management |
| **Environment** | python-dotenv | Environment variable management |
| **HTTP Client** | httpx | Async HTTP client for testing |

### Frontend

| Component | Technology | Purpose |
|-----------|------------|---------|
| **UI Framework** | Vanilla JavaScript | Zero dependencies, pure JavaScript ES6+ |
| **Styling** | Custom CSS + Tailwind CDN | Utility-first CSS framework with custom design system |
| **Typography** | Google Fonts | Inter (body), Orbitron (display), Noto Sans JP (Japanese) |
| **Icons** | Unicode + Custom SVG | Lightweight icon system with emojis |

### Database

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Database** | PostgreSQL 12+ | Powerful, open-source relational database |
| **Hosting** | NeonDB | Serverless PostgreSQL with auto-scaling |
| **Queries** | Raw SQL | Direct SQL queries via psycopg2 for performance |

### Development Tools

- **Version Control**: Git
- **Environment**: Virtual environments (venv)
- **Code Style**: PEP 8, Black (Python formatter)

---

## 🏗 Architecture

### System Design

```
┌──────────────────────────────────┐
│         Browser                  │
│      (Port 5000)                 │
└─────────────┬────────────────────┘
              │
              │ HTTP Requests
              ▼
┌──────────────────────────────────┐
│      Flask Application           │
│        (Port 5000)               │
│  ┌────────────────────────────┐  │
│  │  Frontend Routes            │  │
│  │  - / → index.html           │  │
│  │  - /login → login.html      │  │
│  │  - /static/* → Assets       │  │
│  └────────────────────────────┘  │
│                                  │
│  ┌────────────────────────────┐  │
│  │  API Routes (/api/*)        │  │
│  │  - Auth, Projects, Tasks    │  │
│  │  - Stats, CRUD operations   │  │
│  └────────────────────────────┘  │
└─────────────┬────────────────────┘
              │
              │ SQL Queries (psycopg2)
              ▼
     ┌─────────────────┐
     │  PostgreSQL DB  │
     │   (NeonDB)      │
     └─────────────────┘
```

### Data Flow

1. **User Interaction** → Browser sends request to Flask server (port 5000)
2. **Static Assets** → Flask serves HTML templates via `send_from_directory`
3. **API Calls** → JavaScript makes async fetch calls to Flask API routes (/api/*)
4. **Authentication** → Session cookie validates user identity via `login_required` decorator
5. **Database Operations** → Flask executes raw SQL queries via psycopg2 with RealDictCursor
6. **Response** → JSON data returned to frontend, UI updates dynamically with optimistic updates
7. **Auto-redirect** → Global fetch interceptor catches 401 errors and redirects to /login

### Key Architectural Patterns

- **Unified Server**: Flask handles both API endpoints and frontend serving
- **Decorator-based Auth**: `@login_required` decorator protects all API routes
- **Per-Request DB Connection**: `get_db()` creates connection, `teardown_request` closes it
- **Optimistic UI**: Frontend updates immediately, reverts on error
- **Global Fetch Interceptor**: Automatic credential injection and 401 handling
- **Dual-View Modal**: Mission Control dashboard + Edit override form in single modal

---

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.9 or higher
- **pip**: Python package manager
- **PostgreSQL Database**: NeonDB account (or local PostgreSQL)
- **Git**: Version control system

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/indiser/kira-mission-tracker.git
cd kira-mission-tracker
```

2. **Create Virtual Environment**

```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# Admin User Credentials
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_secure_password
```

**Get your NeonDB connection string:**
1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string from **Connection Details**
4. Paste it into `.env` as `DATABASE_URL`

5. **Start the Application**

```bash
python app.py
```

The application will be available at `http://localhost:5000`

6. **Access the Application**

Open your browser and navigate to:
```
http://localhost:5000/login
```

**Default Credentials:**
- Username: `indiser`
- Password: `RANA`

> **Note**: These credentials are configured in your `.env` file and seeded automatically on first startup if no users exist in the database.

### Deployment Tips

**For production deployment:**
- Use a production WSGI server like Gunicorn or uWSGI
- Set `app.run(debug=False)` or use environment variables
- Enable HTTPS and secure cookie settings
- Configure proper CORS origins
- Set up database backups

**Example with Gunicorn:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📁 Project Structure

```
kira-mission-tracker/
│
├── app.py                       # Main Flask application (API + Frontend serving)
├── database.py                  # PostgreSQL connection, migrations, admin seeding
├── schemas.py                   # Pydantic models for validation
├── crud.py                      # Raw SQL queries for all database operations
├── auth_service.py              # Password hashing, session management
│
├── templates/                   # HTML Templates
│   ├── index.html              # Main dashboard (Mission Control)
│   └── login.html              # Authentication page
│
├── static/                      # Static Assets
│   ├── app.js                  # Main application logic
│   ├── auth.js                 # Global fetch interceptor for auth
│   ├── login.js                # Login page controller
│   ├── style.css               # Global styles & design system
│   ├── dashboard.css           # Mission Control dashboard styles
│   ├── login.css               # Login page styles
│   └── favicon/                # Application icons
│       ├── android-chrome-192x192.png
│       ├── android-chrome-512x512.png
│       ├── apple-touch-icon.png
│       ├── favicon-16x16.png
│       ├── favicon-32x32.png
│       ├── favicon.ico
│       └── site.webmanifest
│
├── .env                         # Environment variables (create this)
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── architecture.md              # Project architecture documentation
└── README.md                    # This file
```

### Key Files Explained

#### Backend Files

- **`app.py`**: Main Flask application with:
  - All API routes (`/api/auth/*`, `/api/projects/*`, `/api/tasks/*`, `/api/stats`)
  - Frontend routes (`/`, `/login`, `/static/*`)
  - Authentication decorator (`@login_required`)
  - Per-request database connection management
  - JSON serialization helpers for UUID, dates, datetimes
  - CORS configuration with credentials support

- **`database.py`**: Database setup:
  - Connection factory (`get_connection`)
  - Migration runner (`run_migrations`) - creates tables if not exist
  - Admin user seeding on first run
  - Trigger function for auto-updating `updated_at` column

- **`schemas.py`**: Pydantic models:
  - `ProjectCreate`, `ProjectUpdate`, `ProjectStatusUpdate`
  - `TaskCreate`, `TaskResponse`
  - `LoginRequest`
  - Enum definitions for `ProjectStatus` and `ProjectPriority`

- **`crud.py`**: Raw SQL operations:
  - Project CRUD: `get_all_projects`, `get_project_with_tasks`, `create_project`, `update_project`, `delete_project`
  - Task CRUD: `create_task`, `toggle_task`, `delete_task`
  - Stats aggregation: `get_stats` (counts by status, priority, overdue)

- **`auth_service.py`**: Authentication utilities:
  - Password hashing with PBKDF2-HMAC-SHA256 and random salt
  - Session token generation (64-byte URL-safe tokens)
  - User lookup by username/ID
  - Session CRUD operations

#### Frontend Files

- **`index.html`**: Main dashboard with:
  - Mission Control interface with hero banner
  - 3-column grid: Intel/AI Summary | Timeline | Analytics & Rank
  - Read-only view + edit override mode
  - Stats cards, filter bar, project grid
  - Add project modal, detail modal, confirm delete modal
  - Progress rings, achievement cards, mission rank display

- **`login.html`**: Authentication page with:
  - Floating label inputs
  - Password visibility toggle
  - Remember me checkbox
  - Animated particle background
  - Cinematic transitions

- **`app.js`**: Main application logic:
  - State management for projects and filters
  - API fetch helpers with error handling
  - Project card rendering with badges and progress bars
  - Modal management (add, detail, delete)
  - Task list rendering and interactions
  - Optimistic UI updates
  - Toast notifications

- **`auth.js`**: Global fetch interceptor:
  - Auto-injects `credentials: 'include'` for all `/api/` requests
  - Catches 401 responses and redirects to `/login`
  - Proactive auth check on dashboard load
  - Updates username in header
  - Global `logout()` function

- **`login.js`**: Login page controller:
  - Form submission handling
  - Password visibility toggle
  - Loading states and error handling
  - Cinematic exit animation on successful login

#### Styles

- **`style.css`**: Global design system:
  - CSS custom properties (colors, gradients, shadows)
  - Component library (buttons, inputs, modals, cards)
  - Animations (fade-in, slide-up, pulse)
  - Utilities and resets

- **`dashboard.css`**: Mission Control specific:
  - Hero banner with glass morphism
  - 3-column grid layout
  - Progress rings (SVG circles)
  - Mission rank cards
  - Achievement badges
  - Task timeline styles

- **`login.css`**: Login page specific:
  - Floating label animations
  - Glass panel effect
  - Particle system
  - Cinematic background

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000
```

### Frontend Routes

#### Serve Dashboard
```http
GET /

Response: 200 OK
Serves index.html (main dashboard)
```

#### Serve Login Page
```http
GET /login

Response: 200 OK
Serves login.html (authentication page)
```

#### Static Assets
```http
GET /static/<path:filename>

Examples:
- /static/app.js
- /static/style.css
- /static/favicon/favicon.ico
```

---

### API Endpoints

All API endpoints require authentication (except `/api/auth/login`). A valid session cookie must be present.

### Authentication Endpoints

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}

Response: 200 OK
{
  "message": "Login successful"
}
Sets HTTP-only cookie: session_id (7-day expiration)
```

#### Logout
```http
POST /api/auth/logout

Response: 200 OK
{
  "message": "Logged out"
}
Clears session_id cookie
```

#### Get Current User
```http
GET /api/auth/me

Response: 200 OK
{
  "id": "uuid",
  "username": "string"
}

Response: 401 Unauthorized (if not authenticated)
{
  "detail": "Not authenticated"
}
```

---

### Stats Endpoint

#### Get Statistics
```http
GET /api/stats

Response: 200 OK
{
  "total_projects": 0,
  "by_status": {
    "active": 0,
    "paused": 0,
    "completed": 0,
    "dropped": 0
  },
  "by_priority": {
    "low": 0,
    "medium": 0,
    "high": 0,
    "critical": 0
  },
  "overdue_count": 0
}
```

---

### Project Endpoints

#### List All Projects
```http
GET /api/projects?status={status}&priority={priority}

Query Parameters:
- status (optional): active|paused|completed|dropped
- priority (optional): low|medium|high|critical

Response: 200 OK
[
  {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "status": "active|paused|completed|dropped",
    "priority": "low|medium|high|critical",
    "deadline": "YYYY-MM-DD",
    "created_at": "ISO8601",
    "updated_at": "ISO8601",
    "total_tasks": 0,
    "done_tasks": 0
  }
]
```

#### Get Project Details
```http
GET /api/projects/{project_id}

Response: 200 OK
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "status": "string",
  "priority": "string",
  "deadline": "YYYY-MM-DD",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "tasks": [
    {
      "id": "uuid",
      "project_id": "uuid",
      "title": "string",
      "is_done": false,
      "created_at": "ISO8601"
    }
  ]
}

Response: 404 Not Found
{
  "detail": "Project not found"
}
```

#### Create Project
```http
POST /api/projects
Content-Type: application/json

{
  "title": "string",
  "description": "string?",
  "priority": "low|medium|high|critical",
  "deadline": "YYYY-MM-DD?"
}

Response: 201 Created
Returns created project object
```

#### Update Project
```http
PUT /api/projects/{project_id}
Content-Type: application/json

{
  "title": "string?",
  "description": "string?",
  "status": "string?",
  "priority": "string?",
  "deadline": "YYYY-MM-DD?"
}

Response: 200 OK
Returns updated project object

Response: 404 Not Found
{
  "detail": "Project not found"
}
```

#### Update Project Status
```http
PATCH /api/projects/{project_id}/status
Content-Type: application/json

{
  "status": "active|paused|completed|dropped"
}

Response: 200 OK
Returns updated project object
```

#### Delete Project
```http
DELETE /api/projects/{project_id}

Response: 204 No Content

Response: 404 Not Found
{
  "detail": "Project not found"
}
```

---

### Task Endpoints

#### Add Task to Project
```http
POST /api/projects/{project_id}/tasks
Content-Type: application/json

{
  "title": "string"
}

Response: 201 Created
Returns created task object

Response: 404 Not Found
{
  "detail": "Project not found"
}
```

#### Toggle Task Completion
```http
PATCH /api/tasks/{task_id}/toggle

Response: 200 OK
Returns updated task object (is_done flipped)

Response: 404 Not Found
{
  "detail": "Task not found"
}
```

#### Delete Task
```http
DELETE /api/tasks/{task_id}

Response: 204 No Content

Response: 404 Not Found
{
  "detail": "Task not found"
}
```

---

### Error Responses

All endpoints may return:

```http
400 Bad Request
{
  "detail": "Error message"
}

401 Unauthorized
{
  "detail": "Not authenticated"
}

422 Unprocessable Entity
{
  "detail": [
    {
      "loc": ["body", "field"],
      "msg": "Validation error message",
      "type": "value_error"
    }
  ]
}

500 Internal Server Error
{
  "detail": "Error message"
}
```

---

## 🗄 Database Schema

### Tables

#### `projects`
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'paused', 'completed', 'dropped')),
    priority VARCHAR(20) NOT NULL DEFAULT 'medium'
        CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    deadline DATE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### `tasks`
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    is_done BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### `users`
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### `sessions`
```sql
CREATE TABLE sessions (
    token VARCHAR(255) PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### Relationships

- **Projects → Tasks**: One-to-Many with CASCADE delete
- **Users → Sessions**: One-to-Many with CASCADE delete

### Triggers

- **`set_updated_at` on projects**: Automatically updates `updated_at` column on project modifications

### Indexes

PostgreSQL automatically creates indexes on:
- Primary keys (all `id` columns)
- Unique constraints (`users.username`, `sessions.token`)
- Foreign keys (`tasks.project_id`, `sessions.user_id`)

### Migrations

All migrations are handled automatically in `database.py` via `run_migrations()`. On application startup:
1. Tables are created if they don't exist
2. Admin user is seeded if no users exist
3. Trigger function and trigger are created

No migration framework is required.

---

## 🔒 Security Features

### Authentication
- **Password Hashing**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Random Salt**: 16 bytes of cryptographically secure random data per password
- **Session Tokens**: 64-byte URL-safe random tokens (512 bits of entropy)
- **Session Expiry**: 7-day expiration with automatic cleanup on query
- **Secure Comparison**: `hmac.compare_digest` for constant-time password verification

### Cookie Security
- **HTTP-only**: Prevents XSS attacks (JavaScript cannot access cookie)
- **SameSite=Lax**: CSRF protection (cookie not sent on cross-site requests)
- **7-day Expiration**: Automatic session timeout
- **Credentials Include**: CORS configured to allow credentials

### API Protection
- **Authentication Required**: All API endpoints protected except `/api/auth/login`
- **Decorator-based**: `@login_required` decorator validates session on every request
- **Automatic Redirect**: 401 responses trigger immediate login redirect via `auth.js`
- **Per-request Auth Check**: Session validated on every API call

### Input Validation
- **Pydantic Schemas**: All API inputs validated with Pydantic models
- **SQL Injection Protection**: Parameterized queries throughout (`%s` placeholders)
- **XSS Prevention**: No HTML rendering of user input, JSON only
- **CSRF Protection**: SameSite cookie attribute

### Session Management
- **Token-based**: Random URL-safe tokens stored in database
- **Expiry Enforcement**: Sessions auto-expire after 7 days
- **User Binding**: Sessions tied to specific user IDs
- **Logout Cleanup**: Sessions deleted from database on logout

---

## 🎨 UI/UX Design

### Design Philosophy

**Cinematic Mission Control Experience**: Inspired by AAA video game interfaces, anime aesthetics, and modern sci-fi command centers. The interface tells a story of operating a futuristic project management AI system.

### Color Palette

| Color | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| **Sky Deep** | `#0B0F2E` | `--sky-deep` | Primary background |
| **Sky Mid** | `#151A3E` | `--sky-mid` | Secondary background |
| **Sky Surface** | `#1E2550` | `--sky-surface` | Surface elements |
| **Sakura** (Pink) | `#FF6B9D` | `--sakura` | Primary actions, accents, branding |
| **Kira** (Blue) | `#7EB8FF` | `--kira` | Secondary elements, info, completed |
| **Sora** (Purple) | `#A78BFA` | `--sora` | Tertiary accents |
| **Ki** (Yellow) | `#FFD166` | `--ki` | Warnings, highlights, S-rank |
| **Midori** (Green) | `#06D6A0` | `--midori` | Success, completion, active |
| **Aka** (Red) | `#EF476F` | `--aka` | Danger, critical, overdue |

### Typography

- **Display Font**: Orbitron (Sci-fi, futuristic headings and buttons)
- **Body Font**: Inter (Clean, readable text for content)
- **Japanese Font**: Noto Sans JP (Anime aesthetic, cultural touch)

**Font Weights:**
- Regular (400): Body text
- Medium (500): Emphasized text
- SemiBold (600): Headings
- Bold (700): Display headings
- ExtraBold (800): Hero titles

### Key UI Components

1. **Glass Morphism Cards**: 
   - Translucent panels with `backdrop-blur`
   - Gradient borders with neon glow
   - Multiple layers for depth

2. **3D Card Transforms**: 
   - Hover effects with `translateY` and `scale`
   - Staggered entrance animations
   - Shadow depth perception

3. **Progress Rings**: 
   - Circular SVG progress indicators
   - Animated stroke-dashoffset
   - Dynamic colors based on completion

4. **Three-Dot Anime Loader**: 
   - Floating animation with spring physics
   - Sakura pink accent color
   - Smooth easing

5. **Toast Notifications**: 
   - Slide-up from bottom-right
   - Auto-dismiss after 3 seconds
   - Success (green) / Error (red) variants

6. **Modal System**: 
   - Layered modals with backdrop blur
   - Escape key to close
   - Click outside to close
   - Smooth fade-in/scale animations

7. **Badges**: 
   - Status badges (active=green, paused=yellow, completed=blue, dropped=red)
   - Priority badges (low=gray, medium=blue, high=orange, critical=red)
   - Pill-shaped with gradient backgrounds

8. **Mission Rank Display**:
   - Large letter grade (S, A, B, C)
   - Star rating (★★★★★)
   - Dynamic colors based on rank

9. **Achievement Cards**:
   - Unlocked: checkmark icon, full color
   - Locked: lock icon, muted gray
   - Smooth unlock animation

10. **Hero Banner**:
    - Full-width gradient background
    - Large project title
    - Badges and progress ring side-by-side

### Animations

**Card Entrance:**
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px) rotateX(10deg);
  }
  to {
    opacity: 1;
    transform: translateY(0) rotateX(0);
  }
}
```

**Hover Effects:**
- TranslateY(-4px) for lift effect
- Scale(1.02) for emphasis
- Glow shadow with matching color

**Loading States:**
- Three-dot floating animation
- Spinner rotation (360deg continuous)
- Skeleton screens with shimmer

**Page Transitions:**
- Fade and scale transforms
- Backdrop blur increase
- Staggered element appearance

**Micro-interactions:**
- Button press (scale down to 0.95)
- Checkbox toggle (scale bounce)
- Input focus (border glow pulse)

### Accessibility

- **Semantic HTML**: Proper use of `<main>`, `<header>`, `<section>`, `<article>`
- **ARIA Labels**: All interactive elements have labels
- **Keyboard Navigation**: Tab order, Enter/Space activation, Escape to close
- **Focus Indicators**: Visible focus outlines
- **Color Contrast**: WCAG AA compliant text contrasts
- **Screen Reader Support**: Role attributes, hidden decorative elements

### Responsive Design

**Breakpoints:**
- Mobile: < 768px (single column, stacked layout)
- Tablet: 768px - 1024px (2-column grid)
- Desktop: > 1024px (3-column dashboard grid)

**Mobile Optimizations:**
- Touch-friendly button sizes (min 44x44px)
- Full-width modals
- Simplified animations
- Reduced backdrop blur for performance

---

## 🔮 Future Roadmap

### Phase 1: Core Enhancements (Q3 2026)

#### 🎯 Enhanced Project Management
- [ ] **Project Templates**: Pre-built templates for common project types (Web App, Mobile App, Design, etc.)
- [ ] **Project Duplication**: Clone existing projects with all tasks and settings
- [ ] **Archive System**: Archive completed projects without deletion (hidden from main view)
- [ ] **Bulk Operations**: Multi-select projects for batch status updates
- [ ] **Project Tags/Labels**: Categorize projects with custom color-coded tags
- [ ] **Color Coding**: Custom color themes for individual projects
- [ ] **Project Search**: Full-text search across titles and descriptions
- [ ] **Sort Options**: Sort by name, date, priority, deadline, completion

#### ✅ Advanced Task Features
- [ ] **Subtasks**: Nested task hierarchy (tasks within tasks) with indentation
- [ ] **Task Dependencies**: Define task relationships and prerequisites (blocked by)
- [ ] **Task Due Dates**: Individual due dates for tasks (not just projects)
- [ ] **Task Assignment**: Assign tasks with due dates (future multi-user prep)
- [ ] **Task Priority**: Individual priority levels for tasks
- [ ] **Task Notes**: Rich text notes attached to tasks with markdown support
- [ ] **Task Attachments**: File uploads for task-related documents
- [ ] **Task Labels**: Custom labels/tags for tasks
- [ ] **Recurring Tasks**: Repeat tasks daily/weekly/monthly

### Phase 2: Collaboration & Multi-User (Q4 2026)

#### 👥 Team Features
- [ ] **Multi-User Support**: Multiple user accounts with role-based access
- [ ] **User Roles**: Admin, Manager, Member permission levels
- [ ] **Team Workspaces**: Shared project spaces for teams
- [ ] **Project Sharing**: Invite users to specific projects
- [ ] **Real-time Collaboration**: Live updates via WebSockets
- [ ] **Activity Feed**: See who did what and when
- [ ] **User Profiles**: Avatars, bios, status messages
- [ ] **Online Indicators**: Show who's currently active

#### 💬 Communication
- [ ] **Comments**: Thread discussions on projects and tasks
- [ ] **Mentions**: @mention users in comments
- [ ] **Notifications**: In-app and email notifications
- [ ] **Activity Log**: Comprehensive audit trail
- [ ] **@here/@everyone**: Notify all project members
- [ ] **Reactions**: Emoji reactions to comments

### Phase 3: Productivity & Intelligence (Q1 2027)

#### 📊 Advanced Analytics
- [ ] **Time Tracking**: Track time spent on projects/tasks
- [ ] **Burndown Charts**: Visual sprint progress tracking
- [ ] **Velocity Charts**: Track completion velocity over time
- [ ] **Productivity Insights**: AI-powered productivity analysis
- [ ] **Custom Reports**: Generate PDF/CSV reports
- [ ] **Velocity Metrics**: Track team/personal velocity over time
- [ ] **Forecasting**: Predict project completion dates based on velocity
- [ ] **Heatmaps**: Visual activity heatmaps

#### 🤖 AI Integration
- [ ] **Smart Suggestions**: AI-recommended task breakdowns
- [ ] **Auto-Categorization**: Automatic project tagging
- [ ] **Deadline Prediction**: ML-based deadline recommendations
- [ ] **Natural Language Input**: Create projects via text commands ("Create a web app project due next Friday")
- [ ] **Summary Generation**: Auto-generate project summaries
- [ ] **Smart Reminders**: Proactive deadline reminders
- [ ] **Risk Detection**: AI detects projects at risk of missing deadlines

### Phase 4: Integration & Ecosystem (Q2 2027)

#### 🔗 Third-Party Integrations
- [ ] **GitHub Integration**: Link commits and PRs to tasks
- [ ] **Google Calendar Sync**: Two-way calendar synchronization
- [ ] **Slack/Discord Webhooks**: Post updates to team channels
- [ ] **Trello Import**: Migrate boards from Trello
- [ ] **Jira Sync**: Bi-directional Jira synchronization
- [ ] **Email Integration**: Create tasks via email
- [ ] **Zapier/Make Support**: Automate workflows
- [ ] **Google Drive/Dropbox**: Link files to projects

#### 📱 Cross-Platform
- [ ] **Progressive Web App (PWA)**: Offline support, install to home screen
- [ ] **Mobile App**: Native iOS and Android applications
- [ ] **Desktop App**: Electron-based desktop application
- [ ] **Browser Extension**: Quick task capture from any webpage
- [ ] **CLI Tool**: Command-line interface for power users

### Phase 5: Enterprise Features (Q3 2027)

#### 🏢 Business Ready
- [ ] **Custom Workflows**: Define custom project workflows (Kanban, Scrum, etc.)
- [ ] **Automation Rules**: If-this-then-that automation
- [ ] **Public REST API**: Public REST API for integrations
- [ ] **Webhooks**: Real-time event notifications
- [ ] **SSO Support**: SAML, OAuth2, LDAP integration
- [ ] **Audit Logs**: Comprehensive compliance logging
- [ ] **Custom Fields**: Define custom fields for projects/tasks
- [ ] **SLA Tracking**: Service Level Agreement tracking

#### 📈 Scalability
- [ ] **Database Optimization**: Query caching, indexing
- [ ] **CDN Integration**: Cloudflare for static assets
- [ ] **Load Balancing**: Multi-instance deployment
- [ ] **Backup System**: Automated daily backups
- [ ] **Data Export**: Complete data export in JSON/CSV
- [ ] **Redis Caching**: Cache frequently accessed data
- [ ] **Elasticsearch**: Full-text search at scale

### Phase 6: UX & Accessibility (Q4 2027)

#### ♿ Accessibility
- [ ] **WCAG 2.1 AA Compliance**: Full accessibility standards
- [ ] **Keyboard Navigation**: Complete keyboard-only control
- [ ] **Screen Reader Support**: Optimized ARIA labels
- [ ] **High Contrast Mode**: Enhanced visibility option
- [ ] **Reduced Motion**: Respect prefers-reduced-motion
- [ ] **Font Scaling**: Support browser font size settings
- [ ] **Voice Control**: Voice commands for hands-free operation

#### 🎨 Customization
- [ ] **Theme Builder**: Custom color scheme creator
- [ ] **Light Mode**: Alternative light theme
- [ ] **Layout Options**: Grid, list, kanban, timeline views
- [ ] **Dashboard Widgets**: Customizable dashboard layout
- [ ] **Internationalization (i18n)**: Multi-language support (Japanese, Spanish, French, German)
- [ ] **Date/Time Formats**: Locale-specific formatting
- [ ] **Custom Fonts**: Upload custom fonts

### Technical Debt & Infrastructure

#### 🛠 Code Quality
- [ ] **Unit Tests**: Comprehensive test coverage (>80%)
- [ ] **E2E Tests**: Playwright/Cypress integration tests
- [ ] **CI/CD Pipeline**: GitHub Actions automation
- [ ] **Code Documentation**: JSDoc, Python docstrings
- [ ] **Performance Monitoring**: Sentry error tracking
- [ ] **Dependency Updates**: Automated dependency management
- [ ] **Security Audits**: Regular security scans
- [ ] **Load Testing**: Performance benchmarking

#### 🚀 Performance
- [ ] **Code Splitting**: Lazy load JavaScript modules
- [ ] **Image Optimization**: WebP, lazy loading, responsive images
- [ ] **Caching Strategy**: Service workers, API response caching
- [ ] **Database Indexing**: Optimize query performance
- [ ] **Bundle Optimization**: Minification, tree-shaking
- [ ] **HTTP/2 & HTTP/3**: Modern protocol support
- [ ] **Preloading**: Preload critical resources

---

## 🤝 Contributing

Contributions are welcome! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### Development Workflow

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make Your Changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests for new features (when test suite exists)
4. **Commit Your Changes**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
5. **Push to Your Fork**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**
   - Describe your changes clearly
   - Reference any related issues

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use Black formatter (line length 88)
- Use type hints where possible
- Write docstrings for functions

**JavaScript:**
- Use strict mode (`"use strict"`)
- Use ES6+ features (const, let, arrow functions, async/await)
- Use camelCase for variables and functions
- Add JSDoc comments for complex functions

**CSS:**
- Use BEM naming convention where applicable
- Use CSS custom properties for colors and shared values
- Group related properties together
- Add comments for complex selectors

**Commits:**
- Use conventional commits format:
  - `feat:` new feature
  - `fix:` bug fix
  - `docs:` documentation changes
  - `style:` formatting, no code change
  - `refactor:` code refactoring
  - `test:` adding tests
  - `chore:` maintenance tasks

### Reporting Issues

Please use GitHub Issues to report bugs or request features. Include:
- **Clear description** of the issue
- **Steps to reproduce** (for bugs)
- **Expected vs actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, browser, Python version)
- **Relevant logs** or error messages

### Feature Requests

When requesting features:
- Check if it's already on the roadmap
- Describe the use case and benefit
- Provide examples or mockups if possible
- Tag with `enhancement` label

### Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Update documentation if needed
- Ensure all tests pass (when test suite exists)
- Add screenshots for UI changes
- Be responsive to review feedback

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Kira Mission Tracker Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **Flask** - Lightweight and powerful web framework for Python
- **PostgreSQL** - Powerful, open-source object-relational database
- **NeonDB** - Serverless PostgreSQL platform for modern applications
- **Tailwind CSS** - Utility-first CSS framework
- **Google Fonts** - Open-source font library (Inter, Orbitron, Noto Sans JP)
- **Pydantic** - Data validation using Python type annotations
- **psycopg2** - PostgreSQL adapter for Python

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/indiser/kira-mission-tracker/issues)
- **GitHub Discussions**: [Community discussions](https://github.com/indiser/kira-mission-tracker/discussions)
- **Email**: indiser01@gmail.com

---

## 🎯 Repository Name & Description

### Recommended Repository Name
```
kira-mission-tracker
```

### Recommended Description
```
🎯 A full-stack personal project management system with a cinematic Mission Control UI inspired by AAA game interfaces. Built with Flask, PostgreSQL, and Vanilla JavaScript. Features session-based auth, real-time updates, and an immersive anime-inspired dashboard experience.
```

### Recommended Topics/Tags
```
flask
postgresql
project-management
task-tracker
python
javascript
glassmorphism
anime-ui
mission-control
dashboard
neondb
session-auth
vanilla-js
ui-design
```

---

<div align="center">

**Made with ❤️ and ☕**

*Transform chaos into clarity, one project at a time.*

**Version 1.0.0** • **Status: Production Ready** • **License: MIT**

</div>
