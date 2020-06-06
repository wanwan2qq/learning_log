from django.contrib import admin

# Register your models here.
from .models import Todo, Priority, Community, InterestingSentences


class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_time',
        'last_modified_time']
    fields = ['name', 'owner', 'member']

class TodoAdmin(admin.ModelAdmin):
    list_display = ['todo', 'text', 'owner', 'is_week_todo',
        'status', 'priority', 'start_time', 
        'finish_time', 'created_time', 'last_modified_time']
    fields = ['todo', 'text', 'owner', 'community',
        'status', 'priority', 'start_time', 
        'finish_time']



admin.site.register(Todo, TodoAdmin)
admin.site.register(Priority)
admin.site.register(Community, CommunityAdmin)
admin.site.register(InterestingSentences)