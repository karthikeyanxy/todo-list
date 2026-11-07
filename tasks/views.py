"""
Views for the To-Do app.

Security rule used everywhere: every task query is filtered by
`user=request.user`, and single-task lookups use get_object_or_404
with `user=request.user`. So a user can never see, edit, delete or
toggle another user's task — even by guessing its URL / id.
All task views are protected with @login_required.
"""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import RegisterForm, TaskForm
from .models import Task


def register(request):
    """Create a new account, log the user in, and go to the dashboard."""
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in straight after registering
            messages.success(request, f"Welcome, {user.username}! Your account was created.")
            return redirect('task_list')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})


@login_required
def task_list(request):
    """
    Dashboard: counts + searchable / filterable / sortable task list.
    GET params: q (search title), status (all/pending/completed),
    priority (All/Low/Medium/High), sort (due_date/-due_date/created).
    """
    tasks = Task.objects.filter(user=request.user)
    today = timezone.localdate()

    # --- Dashboard counts (computed before filtering, so they are totals) ---
    total = tasks.count()
    completed_count = tasks.filter(completed=True).count()
    pending_count = total - completed_count
    overdue_count = tasks.filter(
        completed=False, due_date__lt=today).count()
    completion_pct = round(completed_count / total * 100) if total else 0

    # --- Search: title contains the query (case-insensitive) ---
    q = request.GET.get('q', '').strip()
    if q:
        tasks = tasks.filter(title__icontains=q)

    # --- Filter by status ---
    status = request.GET.get('status', 'all')
    if status == 'pending':
        tasks = tasks.filter(completed=False)
    elif status == 'completed':
        tasks = tasks.filter(completed=True)

    # --- Filter by priority ---
    priority = request.GET.get('priority', 'All')
    if priority in ('Low', 'Medium', 'High'):
        tasks = tasks.filter(priority=priority)

    # --- Sort ---
    sort = request.GET.get('sort', 'due_date')
    if sort == 'due_date':
        # Tasks with no due date last; use two queries merged in Python
        # is avoided — instead order by due_date nulls-last via Coalesce
        # is overkill here, so plain ordering is used.
        tasks = tasks.order_by('due_date', '-created_at')
    elif sort == '-due_date':
        tasks = tasks.order_by('-due_date', '-created_at')
    elif sort == 'priority':
        tasks = tasks.order_by('-priority', '-created_at')
    else:  # newest
        tasks = tasks.order_by('-created_at')

    context = {
        'tasks': tasks,
        'total': total, 'completed_count': completed_count,
        'pending_count': pending_count, 'overdue_count': overdue_count,
        'completion_pct': completion_pct,
        'q': q, 'status': status, 'priority': priority, 'sort': sort,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    """Create a task. The owner is set from request.user, never from the form."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" created.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html',
                  {'form': form, 'title': 'Add New Task'})


@login_required
def task_update(request, pk):
    """Edit a task — only if it belongs to the logged-in user."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html',
                  {'form': form, 'title': 'Edit Task', 'task': task})


@login_required
def task_delete(request, pk):
    """Delete with a confirmation page (GET shows it, POST deletes)."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle(request, pk):
    """Mark complete / incomplete. POST only, then back to the list."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
        state = 'completed' if task.completed else 'marked as pending'
        messages.success(request, f'Task "{task.title}" {state}.')
    return redirect('task_list')
