from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Messages, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
from django.http import HttpResponse


def loginUser(request):
    page = 'login'
    error_message = None  # Initialize error message variable

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
            error_message = 'User does not exist'  # Set error message
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Email or password is incorrect'  # Set error message

    context = {
        'page': page,
        'error_message': error_message  # Pass error message to template
    }
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    error_message = None  # Initialize error message variable

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Buying ourselves some time to modify the user object before saving it to the database.
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = "An error occurred while registering the user. Please try again."  # Set error message
    
    context = {
        'form': MyUserCreationForm(),
        'error_message': error_message  # Pass error message to template
    }
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

    topics = Topic.objects.all()[0:5]
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
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        
        # Instead of using the Room model directly, we use the RoomForm that we created in the forms.py file. This form is a ModelForm that is created from the Room model. We pass the request.POST to the form to create a new Room object.
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False) # Buying ourselves some time to modify the room object before saving it to the database.
        #     room.host = request.user
        #     room.save()
        return redirect('home')
    context = {'form': form,
               'topics': topics,
               }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    # RoomForm() gives you an empty form, and RoomForm(instance=room/initial=room) gives you a form that is pre-filled with the data from the room object.
    form = RoomForm(instance=room)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()

        # This updates the room object with the new data from the form and saves it to the database. We then redirect the user to the home page.
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
       
       
        return redirect('home')
    context = {'form': form,
               'topics': topics,
               'room': room,
               }
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


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        # request.FILES is used here because the avatar field is an ImageField. We use request.FILES to get the file data from the form. We then pass the request
        # instance parameter is used to specify the instance of the user object that we want to update. This is how we pre-fill the form with the data from the user object.
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    
    context = {
        'form': form
    }
    
    return render(request, 'base/update-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {
        'topics': topics
    }
    return render(request, 'base/topics.html', context) 

def activityPage(request):
    room_messages = Messages.objects.all()
    context = {
        'room_messages': room_messages,
        
    }
    return render(request, 'base/activity.html', context)