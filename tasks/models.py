"""
Task model for the To-Do List app.

ER / Database design (for viva):
    User (Django built-in auth.User)  --1:N-->  Task
    - One user can have MANY tasks.
    - Each task belongs to exactly ONE user (ForeignKey, CASCADE:
      deleting a user deletes their tasks).
    - SQLite stores this in the `tasks_task` table; Django creates
      it automatically from this model via migrations.
"""
from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    """A single to-do item owned by one user."""

    # Choices shown as dropdowns in forms and the admin.
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    CATEGORY_CHOICES = [
        ('Personal', 'Personal'),
        ('Work', 'Work'),
        ('Study', 'Study'),
        ('Other', 'Other'),
    ]

    # --- Fields ---
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks',
        help_text="Owner of this task — each user sees only their own tasks."
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='Personal')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Newest first by default.
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({'Done' if self.completed else 'Pending'})"

    @property
    def is_overdue(self):
        """True when a pending task's due date has passed. Used for badges."""
        from django.utils import timezone
        if self.due_date and not self.completed:
            return self.due_date < timezone.localdate()
        return False
