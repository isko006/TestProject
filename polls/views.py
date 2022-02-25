from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serialaizers import *
from .models import *


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def movies_list_view(request):
    if request.method == 'POST':
        serializer = MovieCreateValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={'message': 'error',
                      'errors': serializer.errors},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        name = request.data.get('name', '')
        duration = request.data.get('duration', 0)
        date = request.data.get('date', '')
        age_restriction = request.data.get('age_restriction', '')
        movie = Movie.objects.create(name=name, duration=duration,
                                     date=date, age_restriction=age_restriction)
        movie.genres.set(request.data['genres'])
        movie.save()
        return Response(data={'message': 'you created movie!',
                              'movie': MovieListSerializer(movie).data})


    movies = Movie.objects.all()
    data = MovieListSerializer(movies, many=True).data
    return Response(data=data)


@api_view(['GET', 'PUT', 'DELETE'])
def movies_item_view(request, pk):
    movie = Movie.objects.get(id=pk)
    if request.method == 'DELETE':
        movie.delete()
        return Response(data={'massage': 'Movie removed!!!'})
    elif request.method == 'PUT':
        movie.name = request.data.get('name')
        movie.duration = request.data.get('duration')
        movie.date = request.data.get('date')
        movie.age_restriction = request.data.get('age_restriction')
        movie.save()
        return Response(data={'massage': 'Movie updated',
                              'movie': MovieListSerializer(movie).data})

    data = MovieListSerializer(movie, many=False).data
    return Response(data=data)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response(data={
                'token': token.key
            })
        else:
            return Response(data={
                'massage': 'User not found!!!'
            }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def register(request):
    username = request.data['username']
    password = request.data['password']
    user = User.objects.create(username=username,
                               email=username,
                               password=password,
                               is_active=True)
    return Response(data={'massage': 'User created'})