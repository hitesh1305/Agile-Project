# 🗂️ Agile Project Management Tool

A lightweight, full-stack project management web application built for small teams (3–10 users) using a simple agile workflow. Work is organized hierarchically so progress is always visible at every level.

> **Live Demo:** [agile-project-yrol.onrender.com](https://agile-project-yrol.onrender.com)  

---

## 📌 Project Overview

Work is structured in a clean three-level hierarchy:

```
Project  →  User Story  →  Task
```

| Level | Represents |
|-------|-----------|
| **Project** | The overall goal or initiative |
| **User Story** | A feature or functional requirement |
| **Task** | The individual unit of work |

This model maps directly to how small agile teams think — projects broken into stories, stories broken into executable tasks — with automatic rollup of completion status at each level.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask (Python) |
| Database | PostgreSQL via Supabase *(SQLite used initially)* |
| ORM | SQLAlchemy |
| Authentication | Flask-Login |
| Frontend | HTML + Bootstrap (Jinja2 templates) |
| Deployment | Render |

---

## ✨ Features

### 🔐 Role-Based Access Control

Three roles are supported, each with scoped permissions:

| Role | Permissions |
|------|------------|
| **Admin** | Manage users and assign roles |
| **Manager** | Create, update, and manage projects, stories, and tasks |
| **Viewer** | Read-only access across all work items |

### 📋 Work Item Management
- Create and organize Projects, User Stories, and Tasks
- Assign tasks to team members
- Track task status: `To Do` → `In Progress` → `Done`

### 📈 Automatic Progress Tracking
- When all tasks under a story are complete → Story is automatically marked **Done**
- When all stories under a project are complete → Project is automatically marked **Done**
- Progress rolls up the hierarchy without manual updates

### ⏰ Due Dates & Overdue Detection
- Projects support due dates
- Projects not completed by their due date are automatically flagged as **Overdue**

### ⚙️ Asynchronous Background Workflow

A background thread runs on a periodic interval and:
- Scans all active projects
- Compares current date against project due dates
- Automatically updates project status to **Overdue** when deadlines are missed

**Design notes:**
- Implemented using Python's `threading.Thread` with a `time.sleep` loop
- Runs independently of the request/response cycle
- Failure handling: the thread is daemonized (exits with the main process) and wrapped in a `try/except` to log errors without crashing the app
- **Limitation:** No retry mechanism — a missed check window is skipped. For production, this would be replaced with Celery + Redis for reliable scheduling, retries, and observability.

---

## 🗄️ Database Schema

### Entities

```
User
  - id (PK)
  - username
  - password
  - role (admin | manager | viewer)

Project
  - id (PK)
  - name
  - description
  - status (active | done | overdue)
  - due_date

Story
  - id (PK)
  - title
  - status (to_do | in_progress | done)
  - project_id (FK → Project)

Task
  - id (PK)
  - title
  - status (to_do | in_progress | done)
  - story_id (FK → Story)
  - assigned_to (FK → User)
```

### Relationships

```
User         ──< Task         (one user assigned to many tasks)
Project      ──< Story        (one project has many stories)
Story        ──< Task         (one story has many tasks)
```

---

## 🌐 API Documentation

### Authentication

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/login` | Render login page | Public |
| `POST` | `/login` | Authenticate and create session | Public |
| `GET` | `/logout` | End session | Auth |

### Dashboard

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/dashboard` | View personal dashboard | Auth |

### Projects

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/view_projects` | List all projects | Auth |
| `GET` | `/project/<id>` | View project details and stories | Auth |
| `GET/POST` | `/create_project` | Create a new project | Manager |

### Stories

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET/POST` | `/create_story/<project_id>` | Create a story under a project | Manager |
| `GET` | `/story/<id>` | View story details and tasks | Auth |

### Tasks

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET/POST` | `/create_task/<story_id>` | Create a task under a story | Manager |
| `GET` | `/update_task/<task_id>/<status>` | Update a task's status | Manager |

---

## 🏗️ Architecture

```
├── app.py              # App entry point, background thread init
├── models.py           # SQLAlchemy models and relationships
├── routes.py           # Route handlers and business logic
├── templates/          # Jinja2 HTML templates (Bootstrap)
└── requirements.txt
```

The application follows a simple layered structure:
- **Models** define the schema and enforce relationships
- **Routes** handle request logic, auth checks, and status transitions
- **Templates** render server-side HTML via Jinja2

The backend connects to a cloud-hosted PostgreSQL instance (Supabase) via SQLAlchemy. The background scheduler runs as a daemon thread alongside the Flask dev server.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Local Setup

```bash
# 1. Clone the repository
git clone <repo-link>
cd agile-project

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

The app will be available at `http://localhost:5000`.

---

## 🔑 Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Manager | `manager` | `123` |
| Viewer | `viewer` | `123` |

---

## ⚖️ Design Decisions & Tradeoffs

| Decision | Rationale | Tradeoff |
|----------|-----------|----------|
| Flask over Django | Lightweight, fast to prototype, minimal boilerplate | Less built-in structure for larger apps |
| SQLite → PostgreSQL | Started simple, migrated to persistent cloud DB for deployment | Added config complexity |
| Background thread for async | No external dependencies, simple to implement | Not reliable for production — no retries, no persistence across restarts |
| Bootstrap + server-side templates | Fast to build, no build toolchain needed | Less interactive than a SPA frontend |
| Session-based auth (Flask-Login) | Simple and sufficient for the scope | Doesn't scale to stateless/API-first architectures |

---

## 🔒 Security Considerations

**Implemented:**
- Role-based access control on all routes
- Session-based authentication via Flask-Login
- Route protection — unauthenticated users are redirected

**Known Limitations:**
- Passwords are stored in plain text — should use `bcrypt` hashing
- No CSRF protection on forms
- No rate limiting on login endpoint
- No input sanitization beyond ORM-level protection
- No HTTPS enforcement in local dev

These are acceptable for an internal prototype but would need to be addressed before any production or public-facing deployment.

---

## 🔮 What I'd Improve With More Time

- [ ] **Password hashing** — integrate `bcrypt` for secure credential storage
- [ ] **Celery + Redis** — replace background thread with a proper task queue supporting retries, scheduling, and failure visibility
- [ ] **Real-time updates** — use WebSockets or SSE to push status changes to connected clients
- [ ] **Notifications & reminders** — email or in-app alerts for upcoming deadlines and task assignments
- [ ] **Pagination and filtering** — handle larger datasets across project/story/task lists
- [ ] **CSRF protection** — add `Flask-WTF` for form security
- [ ] **Better UI/UX** — more interactive task board (drag-and-drop kanban style)
- [ ] **Test coverage** — unit tests for models and route logic, integration tests for the async workflow

---

## 🤖 AI Usage

AI tools (primarily Claude and GitHub Copilot) were used during development for:
- Debugging SQLAlchemy relationship issues
- Structuring the background thread implementation
- Speeding up boilerplate (route scaffolding, template layout)

All logic was reviewed, understood, and verified before being used. AI was treated as a pair-programmer, not an author.

---
