from django import forms
from django.forms.widgets import DateTimeInput, SelectMultiple, Textarea, CheckboxSelectMultiple
from django.contrib.admin.widgets import AdminDateWidget, ManyToManyRawIdWidget, FilteredSelectMultiple
from django.contrib.auth.models import User


class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name']