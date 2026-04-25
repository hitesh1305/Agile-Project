# 🗂️ Agile Project Management Tool

A lightweight, full-stack project management app built for small teams — structured, trackable, and easy to extend.

> **Live Demo:** [agile-project-yrol.onrender.com](https://agile-project-yrol.onrender.com/)

---

## 📌 Overview

Work is organized in a clean three-level hierarchy:

```
Project  →  Story  →  Task
```

| Level | Represents |
|-------|-----------|
| **Project** | The overall goal |
| **Story** | A feature or requirement |
| **Task** | The actual work item |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask |
| Database | PostgreSQL (Supabase) |
| ORM | SQLAlchemy |
| Auth | Flask-Login |
| Frontend | HTML + Bootstrap |
| Deployment | Render |

---

## ✨ Features

### 🔐 Role-Based Access Control

| Role | Permissions |
|------|------------|
| **Admin** | Manage users and roles |
| **Manager** | Create and update projects, stories, and tasks |
| **Viewer** | Read-only access |

### 📋 Task Management
- Create tasks under stories
- Assign tasks to users
- Track status: `To Do` → `In Progress` → `Done`

### 📈 Automatic Progress Tracking
- All tasks done → Story marked **Done**
- All stories done → Project marked **Done**

### ⏰ Due Dates & Overdue Detection
- Projects have due dates
- Missed deadlines auto-mark the project as **Overdue**

### ⚙️ Background Processing
A background thread periodically checks deadlines and updates project statuses — a simple implementation of async behavior.

---

## 🗄️ Database Schema

```
User
 └── assigned Tasks

Project
 └── Stories
      └── Tasks
```

**Relationships:**
- A Project has many Stories
- A Story has many Tasks
- A Task is assigned to one User

---

## 🌐 API Routes

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/login` | Login page | Public |
| `POST` | `/login` | Authenticate user | Public |
| `GET` | `/dashboard` | User dashboard | Auth |
| `GET/POST` | `/create_project` | Create a project | Manager |
| `GET` | `/view_projects` | View all projects | Auth |
| `GET` | `/project/<id>` | Project details | Auth |
| `GET/POST` | `/create_story/<project_id>` | Create a story | Manager |
| `GET` | `/story/<id>` | Story and tasks | Auth |
| `GET/POST` | `/create_task/<story_id>` | Create a task | Manager |
| `GET` | `/update_task/<task_id>/<status>` | Update task status | Manager |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- pip

### Installation

```bash
# 1. Clone the repository
git clone <repo-link>
cd agile-project

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

---

## 🔑 Test Credentials (Demo)

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Manager | `manager` | `123` |
| Viewer | `viewer` | `123` |

---

## 🏗️ Architecture

```
├── models/       # SQLAlchemy models & DB schema
├── routes/       # Application logic & endpoints
└── templates/    # Jinja2 HTML templates (Bootstrap)
```

The backend communicates with a cloud PostgreSQL database via SQLAlchemy. The layered structure keeps concerns cleanly separated.

---

## ⚖️ Design Decisions

| Decision | Reason |
|----------|--------|
| Flask over Django | Simplicity, faster development |
| SQLite → PostgreSQL | Persistence and production-readiness |
| Background thread for async | Avoid added complexity of a task queue |
| Bootstrap UI | Clean interface without a frontend framework |

---

## ⚠️ Known Limitations

- Passwords stored in plain text *(no hashing)*

---


## 🤖 AI Usage

AI tools were used during development for debugging, structuring, and speeding up implementation. All logic and decisions were reviewed and verified before use.

---
