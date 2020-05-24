from django import forms
from django.forms.widgets import DateTimeInput, SelectMultiple

from .models import Todo, Community

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['todo', 'text', 'community', 'priority', 'status']
        widgets = {
            'community': SelectMultiple(attrs={'class': "form-control"}),
            }
