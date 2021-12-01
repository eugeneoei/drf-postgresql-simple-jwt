from rest_framework import serializers

from .models import Comment
from users.models import CustomUser as User
from tweets.models import Tweet


class CommentUserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name'
        )


class CommentSerializer(serializers.ModelSerializer):

    content = serializers.CharField(required=True)
    user = CommentUserSerializer(read_only=True)
    # parent_id = serializers.PrimaryKeyRelatedField(queryset=Tweet.objects.all(), source='tweet.id')

    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'created_at',
            'user',
            # 'parent_id'
        )
