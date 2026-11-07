"""
Forms for the To-Do app.

- TaskForm: a ModelForm bound to Task. Django renders the fields,
  validates them, and saves them — no manual request.POST parsing.
  Bootstrap styling is added via widget attrs (class="form-control").
- RegisterForm: extends Django's UserCreationForm (username + password
  with built-in validation) and adds an optional email field.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Task


class TaskForm(forms.ModelForm):
    """Create / edit a task. `user` and `completed` are set in the view,
    not by the user, so they are excluded here."""

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. Finish Django project'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Add details (optional)'}),
            # HTML5 date picker — returns a date Django can save directly.
            'due_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }


class RegisterForm(UserCreationForm):
    """Sign-up form: username, email, password1, password2."""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'you@example.com'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes to the inherited fields.
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
