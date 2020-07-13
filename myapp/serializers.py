from rest_framework import serializers
from django.conf import settings
from .models import Notion

MAX_NOTION_LENGTH = settings.MAX_NOTION_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class NotionActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)
    
    def validate_action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for notions")
        return value


class NotionSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Notion
        fields = ['id','content','likes']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_NOTION_LENGTH:
            raise serializers.ValidationError("This notion is too long")
        return value