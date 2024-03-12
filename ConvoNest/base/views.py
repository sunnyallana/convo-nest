from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm
# Create your views here.

def home(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'base/room.html', {'room': room})


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        # Instead of using the Room model directly, we use the RoomForm that we created in the forms.py file. This form is a ModelForm that is created from the Room model. We pass the request.POST to the form to create a new Room object.
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # RoomForm() gives you an empty form, and RoomForm(instance=room/initial=room) gives you a form that is pre-filled with the data from the room object.
    form = RoomForm(instance=room)
    if request.method == 'POST':
        # This updates the room object with the new data from the form and saves it to the database. We then redirect the user to the home page.
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteForm(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        # To delete the room object, we call the delete() method on the room object and then redirect the user to the home page.
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html', {'object': room})




