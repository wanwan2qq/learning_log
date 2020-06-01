from django import forms
from django.forms.widgets import DateTimeInput, SelectMultiple, Textarea, CheckboxSelectMultiple
from django.contrib.admin.widgets import AdminDateWidget, ManyToManyRawIdWidget, FilteredSelectMultiple
from django.contrib.auth.models import User

from .models import Todo, Community

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['todo', 'text', 'community', 'priority', 'start_time', 'finish_time', 'status']
        widgets = {
            'community': SelectMultiple(attrs={'class': "form-control"}),
            }

class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        fields =['name', 'member']
        widgets = {
            'member': SelectMultiple,
            }
