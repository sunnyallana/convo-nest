from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    
    #Participants
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    
    # auto_now_add is used to set the value of the field to the current date and time when the object is first created. auto_now is used to set the value of the field to the current date and time every time the object is saved.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Specifying Order of QuerySets. For ascending order, use the prefix - (a hyphen) before the field name. For descending order, use the field name without the prefix.
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
class Messages(models.Model):
    #Room
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #Text
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50]
