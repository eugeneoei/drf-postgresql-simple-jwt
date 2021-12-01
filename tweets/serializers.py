from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Tweet
from users.serializers import CustomUserSerializer as UserSerializer
from users.models import CustomUser as User
from comments.serializers import CommentSerializer
from comments.models import Comment

class TweetUserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name'
        )


# class CommentsListingField(serializers.RelatedField):

#     def to_representation(self, value):
#         '''
#         QUESTIONS: is this the right way?
#         '''
#         user = get_object_or_404(User, pk=value.user_id)
#         return {
#             'id': value.id,
#             'content': value.content,
#             'created_at': value.created_at,
#             'user': {
#                 'id': user.id,
#                 'first_name': user.first_name,
#                 'last_name': user.last_name
#             }
#         }


class TweetSerializer(serializers.ModelSerializer):

    content = serializers.CharField(required=True)
    '''
    Populate parent object
    Resources:
    - https://stackoverflow.com/questions/61617985/creating-a-serializer-to-work-with-model-relationships
    '''
    # this approach populates parent object based on parents's serializer.
    # in this case, populates fields defined in UserSerializer
    user_details = UserSerializer(source='user', read_only=True)
    # this approach populates specific fields in parent object using a different serializer
    # in this case, populates fields defined in TweetUserSerializer
    user = TweetUserSerializer()

    '''
    Populate child objects
    '''
    # comments = CommentsListingField(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    '''
    QUESTIONS:
    - why "user_details" variable can be replaced with another variable name but not "user" variable?
    '''

    class Meta:
        model = Tweet
        fields = (
            'id',
            'content',
            'created_at',
            'updated_at',
            'user_details',
            'user',
            'comments'
        )

class TweetListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = (
            'id',
            'content',
            'created_at'
        )