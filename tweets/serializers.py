from rest_framework import serializers
from .models import Tweet
from users.models import CustomUser as User
from users.serializers import CustomUserSerializer as UserSerializer

class TweetSerializer(serializers.ModelSerializer):

    content = serializers.CharField(required=True)
    '''
    Or populating whole User object based on serializer
    Resources:
    - https://stackoverflow.com/questions/61617985/creating-a-serializer-to-work-with-model-relationships
    TODO:
    1. How to populate selected fields?
    '''
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Tweet
        fields = (
            'id',
            'content',
            'created_at',
            'updated_at',
            'user_details'
        )