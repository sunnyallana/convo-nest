from django.contrib import admin
from .models import Room, Topic, Messages, User

# Register your models here.
admin.site.register(User) # Registering the Custom User model with the admin site.
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Messages)