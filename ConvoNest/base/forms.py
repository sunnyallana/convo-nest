from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    # Meta is used to specify the model and the fields that we want to use in the form. In this case, we are using the Room model and the fields name, topic, and description.
    class Meta:
        model = Room
        fields = ['name', 'topic', 'description']