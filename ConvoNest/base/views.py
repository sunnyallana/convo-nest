from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Messages
from .forms import RoomForm
from django.db.models import Q
from django.http import HttpResponse

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
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
    context = {
        'page': page
    }
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    context = {
        'form': UserCreationForm(),
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # This creates a new user object from the form data, but does not save it to the database yet. This is useful when you want to modify the user object before saving it to the database.
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred while registering the user. Please try again.")
    return render(request, 'base/login_register.html', context)


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
    room_messages = Messages.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.messages_set.all().order_by('created') # This is how you access the related objects of a model. In this case, we are accessing the messages related to the room object. We use the related name of the messages field, which is set to messages_set by default. We then use the all() method to get all the related messages objects.
    room_participants = room.participants.all() # set.all() is not used here because the participants field is a ManyToManyField. We use the related name of the participants field, which is set to participants by default. We then use the all() method to get all the related participants objects.

    if request.method == 'POST':
        message = Messages.objects.create(
            user=request.user,
            room=room,
            content=request.POST.get('content'), # This is how you get the data from the form. The request.POST.get('content') gets the data from the form with the name content. This is how you access the data from the form in the view function.
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id) # room.id is not in models.py but it is the primary key of the room object. We use it to redirect the user to the room page after they have submitted the form.
    
    context = {'room': room,
               'room_messages': room_messages,
               'room_id': pk,
                'room_participants': room_participants,
               }
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.messages_set.all()
    topics = Topic.objects.all()
    context = {'user': user,
               'rooms': rooms,
               'room_messages': room_messages,
               'topics': topics,
               }
    return render(request, 'base/user_profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        # Instead of using the Room model directly, we use the RoomForm that we created in the forms.py file. This form is a ModelForm that is created from the Room model. We pass the request.POST to the form to create a new Room object.
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False) # Buying ourselves some time to modify the room object before saving it to the database.
            room.host = request.user
            room.save()
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
    return render(request, 'base/delete.html', {'object': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Messages.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed here")
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'object': message})



