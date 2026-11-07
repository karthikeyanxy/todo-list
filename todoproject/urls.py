"""
Project-level URLs.
- '' (home) -> tasks app (dashboard, CRUD, auth)
- admin/    -> Django admin
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
]
