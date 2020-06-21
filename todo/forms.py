from django import forms
from django.forms.widgets import DateTimeInput, SelectMultiple, Textarea, CheckboxSelectMultiple
from django.contrib.admin.widgets import AdminDateWidget, ManyToManyRawIdWidget, FilteredSelectMultiple
from django.contrib.auth.models import User

from .models import Todo, Community

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['todo', 'text', 'community', 'is_week_todo', 'priority', 'process_status', 'start_time', 'due_time']
        widgets = {
            'community': SelectMultiple(attrs={'class': "form-control"}),
            }
        help_texts = {
            'start_time': '* 未填写开始时间，将自动填入创建时间',
        }

class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        fields =['name', 'member']
        widgets = {
            'member': SelectMultiple,
            }
