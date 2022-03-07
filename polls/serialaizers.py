from rest_framework import serializers

from .models import *

from rest_framework.exceptions import ValidationError


class MovieListSerializer(serializers.ModelSerializer):


    class Meta:
        model = Movie
        fields = 'id name duration date age_restriction '.split()




class MovieCreateValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=100)
    duration = serializers.IntegerField()
    date = serializers.DateField()
    age_restriction = serializers.CharField(min_length=2, max_length=3)


    def validate_name(self, name):
        movies = Movie.objects.filter(name=name)
        if movies.count() > 0:
            raise ValidationError("Такой фильм уже существует!!!")
        return name

    def validate_age_restriction(self, age):
        if age[-1] != '+':
            raise ValidationError('Последний символ должен быть +')
        try:
            int(age[:-1])
        except:
            raise ValidationError('До + должно быть число')
