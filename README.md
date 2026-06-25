<div align="center">

# 🎯 Kira Mission Tracker

**A Full-Stack Personal Project Management System**

*Built with FastAPI · PostgreSQL · Vanilla JavaScript*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
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

**Project Tracker** (also known as **Kira Mission Tracker**) is a modern, full-stack personal project management application designed with a cinematic, anime-inspired UI aesthetic. Built entirely on FastAPI, it offers a unified architecture where the same server handles both API endpoints and frontend delivery, providing real-time project tracking, task management, and comprehensive analytics through an immersive "Mission Control" dashboard experience.

### Why This Project?

- **Unified Architecture**: Single FastAPI server handles both API and frontend (simplified deployment)
- **Modern UI/UX**: Inspired by AAA game interfaces and anime aesthetics with Mission Control theme
- **Real-time Updates**: Optimistic UI updates for instant feedback
- **Secure Authentication**: Session-based authentication with HTTP-only cookies and automatic redirects
- **Production-Ready**: Built with PostgreSQL/NeonDB for scalability
- **Zero Framework Frontend**: Pure Vanilla JavaScript with no dependencies
- **Dual View System**: Read-only Mission Control view + Edit override mode

---

## ✨ Key Features

### 🎯 Project Management
- **Create, Read, Update, Delete (CRUD)** operations for projects
- **Status Tracking**: Active, Paused, Completed, Dropped
- **Priority Levels**: Low, Medium, High, Critical (with visual indicators)
- **Deadline Management**: Set and track project deadlines with overdue alerts
- **Filtering**: Filter projects by status and priority

### ✅ Task Management
- **Sub-task Creation**: Break down projects into manageable tasks
- **Progress Tracking**: Visual progress bars showing task completion
- **Toggle Completion**: Instant task status updates with optimistic UI
- **Task Deletion**: Remove completed or obsolete tasks

### 📊 Analytics Dashboard (Mission Control)
- **Live Statistics**: Total projects, active, completed, and overdue counts
- **Mission Rank System**: Gamified ranking based on task completion (S, A, B, C ranks)
- **Progress Visualization**: Circular SVG progress rings and horizontal bars
- **Achievement System**: Unlock achievements as you progress
- **Dual View System**: 
  - **Read-Only Mission Control View**: Hero banner, 3-column dashboard layout, timeline
  - **Edit Override Mode**: Form-based editing with system override aesthetics
- **AI Summary Section**: Placeholder for future AI-powered project insights

### 🔐 Authentication & Security
- **Session-based Authentication**: Secure HTTP-only cookies
- **Password Hashing**: PBKDF2-HMAC-SHA256 with salt
- **Protected Routes**: All API endpoints require authentication
- **Auto-redirect**: Instant redirect to login on authentication failure

### 🎨 UI/UX Excellence
- **Cinematic Interface**: AAA game-inspired design language
- **Anime Aesthetics**: Japanese typography (Noto Sans JP), neon accents, glass morphism
- **Smooth Animations**: Spring physics, parallax effects, 3D transforms, staggered entrances
- **Responsive Design**: Fully responsive from mobile to desktop
- **Dark Theme**: Eye-friendly dark mode with vibrant accent colors (Sakura pink, Kira blue)
- **Toast Notifications**: Non-intrusive feedback for all actions
- **Loading States**: Three-dot floating anime loaders for all async operations
- **Empty States**: Elegant empty state designs with Japanese kanji (無 - "nothing")
- **Password Toggle**: Eye icon to show/hide passwords on login
- **Floating Labels**: Material-design inspired input labels
- **Backdrop Blur**: Glassmorphism effects throughout the UI
- **Animated Particles**: Background particle system on login page

---

## 🛠 Tech Stack

### Backend & Frontend (Unified)

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | FastAPI | High-performance REST API + Frontend server with automatic OpenAPI docs |
| **Server** | Uvicorn | ASGI server for async Python |
| **Static File Serving** | FastAPI StaticFiles | Serves CSS, JS, images, and favicon |
| **Template Serving** | FastAPI FileResponse | Serves HTML templates |
| **Database** | PostgreSQL (NeonDB) | Serverless PostgreSQL database |
| **Database Driver** | psycopg2-binary | PostgreSQL adapter for Python |
| **Schema Validation** | Pydantic | Data validation and settings management |
| **Environment** | python-dotenv | Environment variable management |
| **HTTP Client** | httpx | Async HTTP client for testing |

### Frontend Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **UI Framework** | Vanilla JavaScript | Zero dependencies, pure JavaScript |
| **Styling** | Custom CSS + Tailwind CDN | Modern utility-first CSS framework |
| **Typography** | Google Fonts | Inter, Orbitron, Noto Sans JP |
| **Icons** | Unicode + Custom SVG | Lightweight icon system |

### Development Tools

- **Code Quality**: ESLint, Black (Python formatter)
- **Version Control**: Git
- **API Documentation**: FastAPI automatic Swagger UI
- **Environment**: Virtual environments (venv)

---

## 🏗 Architecture

### System Design

```
┌─────────────────────────────────────┐
│          Browser                    │
│      (Port 8000)                    │
└──────────────┬──────────────────────┘
               │
               │ HTTP Requests
               ▼
┌──────────────────────────────────────┐
│     FastAPI Unified Server           │
│         (Port 8000)                  │
│  ┌────────────────────────────────┐  │
│  │  Frontend Routes                │  │
│  │  - / → index.html               │  │
│  │  - /login → login.html          │  │
│  │  - /static → Static files       │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌────────────────────────────────┐  │
│  │  API Routes (/api/*)            │  │
│  │  - Auth, Projects, Tasks, Stats │  │
│  └────────────────────────────────┘  │
└──────────────┬───────────────────────┘
               │
               │ SQL Queries
               ▼
      ┌─────────────────┐
      │  PostgreSQL DB  │
      │   (NeonDB)      │
      └─────────────────┘
```

### Data Flow

1. **User Interaction** → Browser sends request to FastAPI server (port 8000)
2. **Static Assets** → FastAPI serves HTML templates and static files (CSS, JS, favicon)
3. **API Calls** → JavaScript makes async fetch calls to FastAPI API routes (/api/*)
4. **Authentication** → Session cookie validates user identity
5. **Database Operations** → FastAPI executes raw SQL queries via psycopg2
6. **Response** → JSON data returned to frontend, UI updates dynamically

### Authentication Flow

```
┌─────────┐        ┌──────────┐       ┌──────────┐
│ Browser │───────▶│  Login   │──────▶│  FastAPI │
│         │        │  Page    │       │  /auth   │
└─────────┘        └──────────┘       └────┬─────┘
     ▲                                      │
     │                                      │
     │              ┌──────────┐            │
     └──────────────│  Cookie  │◀───────────┘
         Session ID │  Storage │   HTTP-only
                    └──────────┘   SameSite
```

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

5. **Start the Application Server**

```bash
uvicorn backend.main:app --reload --port 8000
```

The application will be available at `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs`

6. **Access the Application**

Open your browser and navigate to:
```
http://localhost:8000/login
```

**Default Credentials:**
- Username: `indiser`
- Password: `RANA`

> **Note**: These credentials are configured in your `.env` file and seeded automatically on first startup if no users exist in the database.

---

## 📁 Project Structure

```
project-tracker/
│
├── backend/                      # FastAPI Unified Server
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI app (API routes + frontend serving)
│   ├── database.py              # PostgreSQL connection & migrations
│   ├── schemas.py               # Pydantic models for validation
│   ├── crud.py                  # Database operations (raw SQL)
│   └── auth_service.py          # Authentication logic & session management
│
├── frontend/                     # Frontend Assets
│   ├── templates/               # HTML Templates
│   │   ├── index.html          # Main dashboard
│   │   └── login.html          # Login page
│   │
│   └── static/                  # Static Assets
│       ├── app.js              # Main application logic
│       ├── auth.js             # Authentication interceptor
│       ├── login.js            # Login page logic
│       ├── style.css           # Global styles & components
│       ├── dashboard.css       # Mission Control dashboard styles
│       ├── login.css           # Login page styles
│       └── favicon/            # Application icons
│           ├── android-chrome-192x192.png
│           ├── android-chrome-512x512.png
│           ├── apple-touch-icon.png
│           ├── favicon-16x16.png
│           ├── favicon-32x32.png
│           ├── favicon.ico
│           └── site.webmanifest
│
├── .env                         # Environment variables (create this)
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Key Files Explained

#### Backend Files

- **`main.py`**: Central FastAPI application with:
  - All API routes (auth, projects, tasks, stats)
  - Frontend route handlers (/, /login)
  - Static file mounting (/static)
  - Template serving via FileResponse
- **`database.py`**: Database connection setup, migration runner, table creation, admin user seeding
- **`schemas.py`**: Pydantic schemas for request/response validation
- **`crud.py`**: Raw SQL queries for all database operations
- **`auth_service.py`**: Password hashing, session management, authentication helpers

#### Frontend Files

- **`index.html`**: Main dashboard with stats, project cards, modals, read-only/edit views
- **`login.html`**: Authentication page with floating label inputs and password toggle
- **`app.js`**: All frontend logic (API calls, DOM manipulation, state management)
- **`auth.js`**: Global fetch interceptor for automatic authentication and redirect
- **`login.js`**: Login form handling with validation
- **`style.css`**: Design system (variables, components, animations)
- **`dashboard.css`**: Mission Control-specific styles (3-column layout, progress rings)

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
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
GET /static/{path}

Examples:
- /static/app.js
- /static/style.css
- /static/favicon/favicon.ico
```

---

### API Endpoints

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
Sets HTTP-only cookie: session_id
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
```

### Project Endpoints

#### List All Projects
```http
GET /api/projects?status={status}&priority={priority}

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
```

#### Update Project Status
```http
PATCH /api/projects/{project_id}/status
Content-Type: application/json

{
  "status": "active|paused|completed|dropped"
}

Response: 200 OK
```

#### Delete Project
```http
DELETE /api/projects/{project_id}

Response: 204 No Content
```

### Task Endpoints

#### Add Task to Project
```http
POST /api/projects/{project_id}/tasks
Content-Type: application/json

{
  "title": "string"
}

Response: 201 Created
```

#### Toggle Task Completion
```http
PATCH /api/tasks/{task_id}/toggle

Response: 200 OK
```

#### Delete Task
```http
DELETE /api/tasks/{task_id}

Response: 204 No Content
```

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
- **Trigger**: Auto-update `updated_at` on project modifications

---

## 🔒 Security Features

### Authentication
- **Password Hashing**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Random Salt**: 16 bytes of cryptographically secure random data
- **Session Tokens**: 64-byte URL-safe random tokens
- **Session Expiry**: 7-day expiration with automatic cleanup

### Cookie Security
- **HTTP-only**: Prevents XSS attacks
- **SameSite=Lax**: CSRF protection
- **7-day Expiration**: Automatic session timeout

### API Protection
- **Authentication Required**: All API endpoints protected (except login)
- **Automatic Redirect**: 401 responses trigger immediate login redirect
- **CORS Configuration**: Credentials allowed for cross-origin requests

### Input Validation
- **Pydantic Schemas**: All API inputs validated
- **SQL Injection Protection**: Parameterized queries throughout
- **XSS Prevention**: Client-side sanitization

---

## 🎨 UI/UX Design

### Design Philosophy

**Cinematic Experience**: Inspired by AAA video game interfaces, anime aesthetics, and modern design systems.

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| **Sakura** (Pink) | `#FF6B9D` | Primary actions, accents |
| **Kira** (Blue) | `#7EB8FF` | Secondary elements, info |
| **Sora** (Purple) | `#A78BFA` | Tertiary accents |
| **Ki** (Yellow) | `#FFD166` | Warnings, highlights |
| **Midori** (Green) | `#06D6A0` | Success, completion |
| **Aka** (Red) | `#EF476F` | Danger, critical |

### Typography

- **Display**: Orbitron (Sci-fi, futuristic headings)
- **Body**: Inter (Clean, readable text)
- **Japanese**: Noto Sans JP (Anime aesthetic)

### Key UI Components

1. **Glass Morphism Cards**: Translucent panels with backdrop blur
2. **3D Transforms**: Hover effects with depth perception
3. **Progress Rings**: Circular SVG progress indicators
4. **Animated Loaders**: Three-dot floating animation
5. **Toast Notifications**: Slide-up notifications with auto-dismiss
6. **Modal System**: Layered modals with backdrop blur
7. **Achievement System**: Gamified badges for engagement

### Animations

- **Card Entrance**: Staggered fade-in with 3D rotation
- **Hover Effects**: TranslateY + scale with glow shadows
- **Loading States**: Smooth skeleton screens and spinners
- **Page Transitions**: Fade and scale transforms
- **Micro-interactions**: Spring physics for natural feel

---

## 🔮 Future Roadmap

### Phase 1: Core Enhancements (Q3 2026)

#### 🎯 Enhanced Project Management
- [ ] **Project Templates**: Pre-built templates for common project types
- [ ] **Project Duplication**: Clone existing projects with all tasks
- [ ] **Archive System**: Archive completed projects without deletion
- [ ] **Bulk Operations**: Multi-select projects for batch status updates
- [ ] **Project Tags/Labels**: Categorize projects with custom tags
- [ ] **Color Coding**: Custom color themes for individual projects

#### ✅ Advanced Task Features
- [ ] **Subtasks**: Nested task hierarchy (tasks within tasks)
- [ ] **Task Dependencies**: Define task relationships and prerequisites
- [ ] **Task Assignment**: Assign tasks with due dates
- [ ] **Task Priority**: Individual priority levels for tasks
- [ ] **Task Notes**: Rich text notes attached to tasks
- [ ] **Task Attachments**: File uploads for task-related documents

### Phase 2: Collaboration & Multi-User (Q4 2026)

#### 👥 Team Features
- [ ] **Multi-User Support**: Multiple user accounts with role-based access
- [ ] **User Roles**: Admin, Manager, Member permission levels
- [ ] **Team Workspaces**: Shared project spaces for teams
- [ ] **Project Sharing**: Invite users to specific projects
- [ ] **Real-time Collaboration**: Live updates via WebSockets
- [ ] **Activity Feed**: See who did what and when

#### 💬 Communication
- [ ] **Comments**: Thread discussions on projects and tasks
- [ ] **Mentions**: @mention users in comments
- [ ] **Notifications**: In-app and email notifications
- [ ] **Activity Log**: Comprehensive audit trail

### Phase 3: Productivity & Intelligence (Q1 2027)

#### 📊 Advanced Analytics
- [ ] **Time Tracking**: Track time spent on projects/tasks
- [ ] **Burndown Charts**: Visual sprint progress tracking
- [ ] **Productivity Insights**: AI-powered productivity analysis
- [ ] **Custom Reports**: Generate PDF/CSV reports
- [ ] **Velocity Metrics**: Track team/personal velocity over time
- [ ] **Forecasting**: Predict project completion dates

#### 🤖 AI Integration
- [ ] **Smart Suggestions**: AI-recommended task breakdowns
- [ ] **Auto-Categorization**: Automatic project tagging
- [ ] **Deadline Prediction**: ML-based deadline recommendations
- [ ] **Natural Language Input**: Create projects via text commands
- [ ] **Summary Generation**: Auto-generate project summaries

### Phase 4: Integration & Ecosystem (Q2 2027)

#### 🔗 Third-Party Integrations
- [ ] **GitHub Integration**: Link commits and PRs to tasks
- [ ] **Google Calendar Sync**: Two-way calendar synchronization
- [ ] **Slack/Discord Webhooks**: Post updates to team channels
- [ ] **Trello Import**: Migrate boards from Trello
- [ ] **Jira Sync**: Bi-directional Jira synchronization
- [ ] **Email Integration**: Create tasks via email

#### 📱 Cross-Platform
- [ ] **Progressive Web App (PWA)**: Offline support, install to home screen
- [ ] **Mobile App**: Native iOS and Android applications
- [ ] **Desktop App**: Electron-based desktop application
- [ ] **Browser Extension**: Quick task capture from any webpage

### Phase 5: Enterprise Features (Q3 2027)

#### 🏢 Business Ready
- [ ] **Custom Workflows**: Define custom project workflows
- [ ] **Automation Rules**: If-this-then-that automation
- [ ] **API Access**: Public REST API for integrations
- [ ] **Webhooks**: Real-time event notifications
- [ ] **SSO Support**: SAML, OAuth2, LDAP integration
- [ ] **Audit Logs**: Comprehensive compliance logging

#### 📈 Scalability
- [ ] **Database Optimization**: Query caching, indexing
- [ ] **CDN Integration**: Cloudflare for static assets
- [ ] **Load Balancing**: Multi-instance deployment
- [ ] **Backup System**: Automated daily backups
- [ ] **Data Export**: Complete data export in JSON/CSV

### Phase 6: UX & Accessibility (Q4 2027)

#### ♿ Accessibility
- [ ] **WCAG 2.1 AA Compliance**: Full accessibility standards
- [ ] **Keyboard Navigation**: Complete keyboard-only control
- [ ] **Screen Reader Support**: Optimized ARIA labels
- [ ] **High Contrast Mode**: Enhanced visibility option
- [ ] **Reduced Motion**: Respect prefers-reduced-motion
- [ ] **Font Scaling**: Support browser font size settings

#### 🎨 Customization
- [ ] **Theme Builder**: Custom color scheme creator
- [ ] **Light Mode**: Alternative light theme
- [ ] **Layout Options**: Grid, list, kanban views
- [ ] **Dashboard Widgets**: Customizable dashboard layout
- [ ] **Internationalization (i18n)**: Multi-language support
- [ ] **Date/Time Formats**: Locale-specific formatting

### Technical Debt & Infrastructure

#### 🛠 Code Quality
- [ ] **Unit Tests**: Comprehensive test coverage (>80%)
- [ ] **E2E Tests**: Playwright/Cypress integration tests
- [ ] **CI/CD Pipeline**: GitHub Actions automation
- [ ] **Code Documentation**: JSDoc, Python docstrings
- [ ] **Performance Monitoring**: Sentry error tracking
- [ ] **Dependency Updates**: Automated dependency management

#### 🚀 Performance
- [ ] **Code Splitting**: Lazy load JavaScript modules
- [ ] **Image Optimization**: WebP, lazy loading, responsive images
- [ ] **Caching Strategy**: Service workers, API response caching
- [ ] **Database Indexing**: Optimize query performance
- [ ] **Bundle Optimization**: Minification, tree-shaking

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### Development Workflow

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make Your Changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests for new features
4. **Commit Your Changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to Your Fork**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Code Style

- **Python**: Follow PEP 8, use Black formatter
- **JavaScript**: Follow Airbnb style guide, use ESLint
- **CSS**: Use BEM naming convention
- **Commits**: Use conventional commits (feat, fix, docs, etc.)

### Reporting Issues

Please use GitHub Issues to report bugs or request features. Include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, browser, Python version)

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

- **FastAPI** - Modern, fast web framework for Python (handling both API and frontend)
- **PostgreSQL** - Powerful, open-source object-relational database
- **NeonDB** - Serverless PostgreSQL platform
- **Tailwind CSS** - Utility-first CSS framework
- **Google Fonts** - Open-source font library

---

## 🔑 Architecture Evolution

This project has evolved to use a **unified FastAPI architecture** where a single server handles both API endpoints and frontend delivery. This simplifies deployment and removes the need for a separate Flask server.

**Key Benefits:**
- ✅ Single server (port 8000) instead of two
- ✅ Simplified deployment and maintenance
- ✅ Better performance (no HTTP round-trips between servers)
- ✅ Unified codebase in `backend/main.py`
- ✅ Easier development workflow

**What Changed:**
- Removed `frontend/app.py` (Flask server)
- Added frontend routes to `backend/main.py` (`/`, `/login`)
- FastAPI now serves both API responses and HTML templates

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/indiser/kira-mission-tracker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/indiser/kira-mission-tracker/discussions)
- **Email**: indiser01@gmail.com

---

<div align="center">

**Made with ❤️ and ☕**

*Transform chaos into clarity, one project at a time.*

</div>
