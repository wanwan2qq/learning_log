from django import forms
from django.forms.widgets import TextInput, Select, SelectMultiple

from .models import Post, Category, Tag
from mdeditor.fields import MDTextFormField

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'tags']
        widgets = {
            'title': TextInput(attrs={'class': "form-control"}),
            'body': MDTextFormField,
            'category': Select(attrs={'class': "form-control"}),
            'tags': SelectMultiple(attrs={'class': "form-control"}),
            }

class CateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': '分类'}
        widgets = {
            'name': TextInput(attrs={'class': "form-control"}),
            }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {'name': '标签'}
        widgets = {
            'name': TextInput(attrs={'class': "form-control"}),
            }
