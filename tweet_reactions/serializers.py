from rest_framework import serializers

from .models import TweetReaction


class TweetReactionSerializer(serializers.ModelSerializer):

    type = serializers.CharField(required=True)

    class Meta:
        model = TweetReaction
        fields = (
            'id',
            'user',
            'type'
        )