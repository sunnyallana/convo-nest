from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)

@api_view(['GET']) # This is a decorator that takes a list of methods that the view should respond to
def getRooms(request):
    rooms = Room.objects.all()  
    serializer = RoomSerializer(rooms, many=True) # many means that we are serializing multiple objects
    # return Response(rooms) - This is wrong because Response expects a dictionary or a list, not a queryset
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
