from django.contrib import admin

from .models import Notion, NotionLike
# Register your models here.

class NotionLikeAdmin(admin.TabularInline):
    model = NotionLike


class NotionAdmin(admin.ModelAdmin):
    inlines = [NotionLikeAdmin]
    list_display = ['__str__','user']
    search_fields = ['user__username','user__email']
    class Meta:
        model = Notion


admin.site.register(Notion,NotionAdmin)