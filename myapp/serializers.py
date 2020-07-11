from rest_framework import serializers
from django.conf import settings
from .models import Notion

MAX_NOTION_LENGTH = settings.MAX_NOTION_LENGTH

class NotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notion
        fields = ['content']

    def validate_content(self, value):
        if len(value) > MAX_NOTION_LENGTH:
            raise serializers.ValidationError("This notion is too long")
        return value