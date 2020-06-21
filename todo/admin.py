from django.contrib import admin

# Register your models here.
from .models import Todo, Priority, Community, InterestingSentences, MeetingAgenda


class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_time',
        'last_modified_time']
    fields = ['name', 'owner', 'member']

class TodoAdmin(admin.ModelAdmin):
    list_display = ['todo', 'text', 'owner', 'is_week_todo', 'process_status',
        'status', 'priority', 'start_time', 
        'finish_time', 'created_time', 'last_modified_time']
    fields = ['todo', 'text', 'owner', 'community', 'follower', 'process_status',
        'status', 'priority', 'start_time', 
        'finish_time']

class MeetingAgendaAdmin(admin.ModelAdmin):
    list_display = ['agenda', 'community', 'proposed_user', 'owner',
        'status', 'action_plan', 'track_record', 'proposed_date',
        'deadline', 'created_time', 'last_modified_time']



admin.site.register(Todo, TodoAdmin)
admin.site.register(Priority)
admin.site.register(Community, CommunityAdmin)
admin.site.register(InterestingSentences)
admin.site.register(MeetingAgenda, MeetingAgendaAdmin)