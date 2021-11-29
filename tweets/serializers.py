from rest_framework import serializers
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):

    # content = serializers.TextField(required=True)
    content = serializers.CharField(required=True)

    class Meta:
        model = Tweet
        # fields = ('id', 'user', 'content', 'created_at', 'updated_at')
        # fields = ('id', 'content', 'created_at', 'updated_at')
        fields = '__all__'
        depth = 1