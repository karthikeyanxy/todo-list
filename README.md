# To-Do List — Django Web App

A To-Do List web app built with Python Django, Bootstrap 5, and SQLite. Features user registration and login, add/edit/delete tasks, priorities, due dates, categories, search and filters, and a dashboard with Total, Completed, Pending, and Overdue counts.

A college-ready To-Do List web application built with **Python Django**,
**HTML / CSS / Bootstrap 5** on the frontend, and **SQLite** as the database.
Frontend and backend are together in one app — run it with a single
`python manage.py runserver`, no separate frontend server needed.

Each user registers and logs in, and sees **only their own tasks**.
Tasks can be created, edited, deleted, searched, filtered, sorted, and
marked complete / pending.

## Features

- **User authentication (Django built-in auth):** Register, Login, Logout
- **Per-user data isolation:** every task query is filtered by
  `user=request.user`; a user cannot view or edit another user's task
  even by guessing its URL
- **Task fields:** title, description, due date, priority
  (Low / Medium / High), category (Personal / Work / Study / Other),
  completed flag, created date
- **Full CRUD:** create, list, edit, delete (with confirmation page),
  complete / incomplete toggle
- **Dashboard:** counts for Total, Completed, Pending, and Overdue tasks,
  plus an animated completion progress bar
- **Search & filter:** search by title, filter by status
  (All / Pending / Completed) and priority, sort by due date or newest
- **Bootstrap 5 UI:** responsive navbar (app name, username, logout),
  cards, priority/status badges, empty state when there are no tasks
- **Modern design:** indigo → violet gradient theme, Poppins / Inter
  fonts, soft pastel priority badges, animated progress bar, and pure-CSS
  animations — cards fade/slide in on load, lift on hover, and buttons
  have a subtle press effect (see `static/css/style.css`)
- **Django admin** enabled for the Task model (`/admin/`)
- **Feedback:** Django messages framework shows success messages
  after create / edit / delete / toggle

## Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | Python Django 5.2 |
| Frontend | HTML, CSS, Bootstrap 5 (CDN) |
| Database | SQLite (Django default, `db.sqlite3`) |
| Auth | Django built-in `auth.User` + `UserCreationForm` |

## Folder Structure

```
todo-list-django/
├── manage.py                  # Django command-line entry point
├── requirements.txt           # Django==5.2.19
├── README.md
├── db.sqlite3                 # Created by `migrate` (SQLite database)
├── todoproject/               # Project settings & root URLs
│   ├── settings.py            # INSTALLED_APPS, SQLite DB, auth redirects, static files
│   ├── urls.py                # admin/ + include('tasks.urls')
│   ├── asgi.py / wsgi.py
├── tasks/                     # The To-Do app
│   ├── models.py              # Task model (ForeignKey to User)
│   ├── views.py               # register, task_list, create, update, delete, toggle
│   ├── forms.py               # TaskForm (ModelForm), RegisterForm
│   ├── urls.py                # /, /add/, /<id>/edit/, /<id>/delete/, /<id>/toggle/, /login/, /register/, /logout/
│   ├── admin.py               # Task registered in Django admin
│   └── templates/tasks/
│       ├── base.html          # Bootstrap layout + navbar + messages
│       ├── task_list.html     # Dashboard + search/filter + task cards
│       ├── task_form.html     # Add / Edit form
│       ├── task_confirm_delete.html
│       ├── login.html
│       └── register.html
└── static/css/style.css       # Custom theme: gradient, cards, animations
```

## How to Run Locally

```bash
# 1. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create the database tables
python manage.py migrate

# 4. (Optional) Create an admin user for /admin/
python manage.py createsuperuser

# 5. Start the development server
python manage.py runserver
```

Then open in your browser:

- Home / Dashboard: http://127.0.0.1:8000/
- Register: http://127.0.0.1:8000/register/
- Login: http://127.0.0.1:8000/login/
- Admin: http://127.0.0.1:8000/admin/

> The home page redirects to `/login/` if you are not logged in.
> Register a new account first, then add tasks.

## Default URLs

| URL | What it does |
|---|---|
| `/` | Dashboard — task list, counts, search & filters |
| `/add/` | Create a new task |
| `/<id>/edit/` | Edit a task |
| `/<id>/delete/` | Delete confirmation, then delete |
| `/<id>/toggle/` | Mark complete / pending (POST) |
| `/register/` | Create an account |
| `/login/` | Log in |
| `/logout/` | Log out (POST) |
| `/admin/` | Django admin (Task model) |

## Database / ER Description (for Viva)

```
User (auth_user)  ── 1 : N ──►  Task (tasks_task)

User:  id, username, email, password (hashed), date_joined, ...
Task:  id, user_id (FK → auth_user.id, on_delete=CASCADE),
       title, description, due_date, priority, category,
       completed, created_at
```

- **One-to-Many:** one user has many tasks; each task belongs to one user.
- **ForeignKey with CASCADE:** deleting a user deletes all their tasks.
- **SQLite:** a single file `db.sqlite3`; no separate database server is
  needed. Django's ORM converts the `Task` model into SQL tables via
  `makemigrations` + `migrate` — no hand-written SQL is required.
- **MVT pattern:** Model (`models.py`) holds data, View (`views.py`)
  holds logic, Template (`templates/`) holds presentation. URLs in
  `urls.py` map a web address to a view.

## Viva Talking Points

1. **Why Django?** Batteries-included: built-in auth, admin, ORM, and
   forms, so a full CRUD app needs very little boilerplate.
2. **Why SQLite?** Zero-configuration, file-based, perfect for a
   college project and local demo; Django can switch to MySQL/PostgreSQL
   later by changing only `DATABASES` in `settings.py`.
3. **How is data kept private?** `@login_required` on every task view,
   plus `Task.objects.filter(user=request.user)` and
   `get_object_or_404(Task, pk=pk, user=request.user)` — so users only
   ever see their own rows.
4. **What is a ModelForm?** `TaskForm` is generated from the `Task`
   model; Django validates the input and saves it, and Bootstrap classes
   are added through widget attributes.
5. **What is a migration?** A versioned record of a model change.
   `makemigrations` creates it, `migrate` applies it to SQLite.
6. **How does login work?** Django's `LoginView` checks the username
   and password against the hashed password stored by `UserCreationForm`;
   a session cookie keeps the user logged in.
7. **What does `{% extends 'tasks/base.html' %}` do?** Template
   inheritance: every page reuses the same navbar, Bootstrap links, and
   messages area, and only fills in its own `content` block.

## Demo Script (2 minutes)

1. Open `/register/`, create an account — you land on the empty dashboard.
2. Click **Add Task**, fill in title / due date / priority / category, save.
3. Add 2–3 tasks, use **Search** and the **Status / Priority** filters.
4. Click **Mark Done** — the card is struck through and the counts update.
5. Click **Edit**, change the due date; click **Delete** and confirm.
6. Open `/admin/`, log in with the superuser, show the Task list.
