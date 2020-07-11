from django.db import models
import random
from django.conf import settings 

User = settings.AUTH_USER_MODEL
# Create your models here.
class NotionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notion = models.ForeignKey("Notion", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Notion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='notion_user', blank=True, through=NotionLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank =True, null= True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering: ['-id']

    def serialize(self):
        return{
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,120)
        }