from rest_framework import serializers
from .models import Tweet
from users.models import CustomUser as User
from users.serializers import CustomUserSerializer as UserSerializer

class TweetSerializer(serializers.ModelSerializer):

    content = serializers.CharField(required=True)
    '''
    Populate user details in each tweet
    Resources:
    - https://stackoverflow.com/questions/61617985/creating-a-serializer-to-work-with-model-relationships
    '''
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'user_details', 'content', 'created_at', 'updated_at')