# b29-drf-assgn: Creative Studio Workflow System

A full-stack workflow management system designed for creative studios to manage projects and tasks with team isolation and Role-Based Access Control (RBAC).
check the deployed project at https://mdg-drf-assign.vercel.app/
## Technology Stack

* **Backend**: Django REST Framework (DRF), Django Filters
* **Frontend**: React, Axios, React Router, Vite
* **Database**: SQLite (default dev database)

---

## Core Features

### 1. Studio Multi-Tenancy & Isolation
* Support for multiple creative studios.
* strict data isolation: users can only view or manage projects/tasks in studios where they have an active membership.

### 2. Role-Based Access Control (RBAC)
* Supported Roles: Studio Admin, Project Lead, Designer, Writer, Reviewer, Client Viewer.
* Enforced permission policies:
  * Client Viewers have read-only access and cannot create/edit tasks or add comments/attachments.
  * Studio Admins and Project Leads have full management and deletion rights.
  * Assignee validation restricts task assignment to studio members (excluding Client Viewers).

### 3. Workflow Stage Management
* Tasks transition through defined stages: Draft, Review, Revision, Approved, Completed.
* Stage transition guardrules prevent out-of-order stage changes (e.g., Draft must go to Review first).

### 4. Task Metadata & Collaboration
* File attachments and comment/feedback threads on individual tasks.
* Deadlines, priority levels (Low, Medium, High, Urgent), and customizable tags per studio.

### 5. Search and Filtering
* Backend-supported search on task titles and descriptions.
* Filters for task stage, priority, and assignee.

### 6. Notifications
* Event-driven notification system for task assignment, status updates, and new comments.

---

## Getting Started

### Backend Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```
   The backend will run on `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:5173`.

---
