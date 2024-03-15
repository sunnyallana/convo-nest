from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    # Meta is used to specify the model and the fields that we want to use in the form. In this case, we are using the Room model and the fields name, topic, and description.
    class Meta:
        model = Room
        fields = '__all__' # This is how you include all the fields from the model in the form. In this case, we are including all the fields from the Room model in the form.
        exclude = ['participants', 'host'] # This is how you exclude fields from the form. In this case, we are excluding the participants and host fields from the form. We don't want the user to be able to set these fields when creating a new room. We want to set these fields in the view function instead.


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined']