from django.contrib import admin

from .models import Notion
# Register your models here.

class NotionAdmin(admin.ModelAdmin):
    list_display = ['__str__','user']
    search_fields = ['user__username','user__email']
    class Meta:
        model = Notion


admin.site.register(Notion,NotionAdmin)