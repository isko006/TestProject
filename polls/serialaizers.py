from rest_framework import serializers
from polls.models import Movie

class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = 'id name duration date age_restriction'


class MovieCreateValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=50)
    duration = serializers.IntegerField()
    date = serializers.DateField()
    age_restriction = serializers.CharField(min_length=2, max_length=3)

