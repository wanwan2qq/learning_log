from django.contrib import admin

# Register your models here.
from .models import Impression, GiveImpression, PickCoin


class ImpressionAdmin(admin.ModelAdmin):
    list_display = ['impression', 'preset', 'created_time',
        'last_modified_time']
    fields = ['impression', 'preset']

class GiveImpressionAdmin(admin.ModelAdmin):
    list_display = ['impression', 'user', 'remarks', 'picks', 'praise_user', 'created_time', 'last_modified_time']
    fields = ['impression', 'user', 'remarks', 'picks', 'praise_user']

class PickCoinAdmin(admin.ModelAdmin):
    list_display = ['user', 'pick_coin_num', 'key_user']




admin.site.register(Impression, ImpressionAdmin)
admin.site.register(GiveImpression, GiveImpressionAdmin)
admin.site.register(PickCoin, PickCoinAdmin)
