from rest_framework import serializers

from .models import Comment
from users.models import CustomUser as User


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

    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'created_at',
            'user'
        )
