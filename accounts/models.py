from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    friends = models.ManyToManyField("User", blank=True)
    slug = models.SlugField(default="", null=False)
    chats = models.ManyToManyField("Chat_Users", blank=True)
    
# Create your models here.

class Friend_Request(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)

class Chat_Users(models.Model):
    name = models.CharField(max_length=30)
    users = models.ManyToManyField("User", blank=True)
    permitted_users = models.ManyToManyField("User", related_name="permitted_users", blank=True)