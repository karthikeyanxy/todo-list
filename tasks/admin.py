"""Admin for the Task model — visit /admin/ after createsuperuser."""
from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'category',
                    'due_date', 'completed', 'created_at')
    list_filter = ('completed', 'priority', 'category', 'due_date')
    search_fields = ('title', 'description', 'user__username')
    list_editable = ('completed',)
    ordering = ('-created_at',)
