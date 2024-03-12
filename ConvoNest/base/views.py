from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.http import HttpResponse

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            user = None
            messages.error(request, 'User does not exist') # This is how you display a message to the user. The first argument is the request object, and the second argument is the message that you want to display. The message is displayed in the template using the messages framework.
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # topic__name is used to perform a query on the name field of the topic field of the Room model. This is a way to perform a query on a related model. In this case, we are performing a query on the name field of the topic field of the Room model.
    
    # __icontains is used to perform a case-insensitive match. This means that the query will match any object that contains the search term, regardless of the case of the search term or the object.
    
    # [:5] is used to get the first 5 objects from the queryset. This is a way to limit the number of objects that are returned from the database. This is useful when you have a large number of objects and you only want to display a few of them.

    # Q is used to perform complex queries. We can use (OR '|' and AND '&'). In this case, we are performing a query that matches any object that contains the search term in the name, or description fields of the Room model. This is a way to perform a query that matches any object that contains the search term in multiple fields of the model.
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)  | # Directly accessible attributes do not have to be prefixed by the model name.
        Q(description__icontains=q)               
    )

    topics = Topic.objects.all()

    room_count = rooms.count()

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'base/room.html', {'room': room})

@login_required(login_url='login')
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


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
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


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    
    if request.method == 'POST':
        # To delete the room object, we call the delete() method on the room object and then redirect the user to the home page.
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html', {'object': room})




