from django import forms
from django.forms.widgets import DateTimeInput, SelectMultiple, Textarea, CheckboxSelectMultiple, TextInput
from django.contrib.admin.widgets import AdminDateWidget, ManyToManyRawIdWidget, FilteredSelectMultiple
from django.contrib.auth.models import User
from mdeditor.fields import MDTextFormField

from .models import GiveImpression, Impression

class NewImpressionForm(forms.ModelForm):
    class Meta:
        model = Impression
        fields = ['impression']
        
