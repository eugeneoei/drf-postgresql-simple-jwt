from django.core.paginator import Paginator
from rest_framework import serializers

from app.settings import COMMENTS_PAGE_SIZE
from .models import Tweet
# from users.serializers import CustomUserSerializer as UserSerializer
from users.models import CustomUser as User
from comments.serializers import CommentSerializer
from tweet_reactions.serializers import TweetReactionSerializer

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


class TweetSerializer(serializers.ModelSerializer):

    content = serializers.CharField(required=True)
    '''
    Populate related objects.
    Related objects must be read only. Otherwise, perform_create in views will not be called.

    Resources:
    - https://stackoverflow.com/questions/61617985/creating-a-serializer-to-work-with-model-relationships
    '''
    # # this approach populates parent object based on parents's serializer.
    # # in this case, populates fields defined in UserSerializer
    # user_details = UserSerializer(source='user', read_only=True)
    # # this approach populates specific fields in parent object using a different serializer
    # # in this case, populates fields defined in TweetUserSerializer
    user = TweetUserSerializer(read_only=True)

    '''
    returns all comments
    '''
    # comments = CommentSerializer(many=True, read_only=True)
    '''
    returns paginated comments
    get more comments through /api/tweets/:id/comments?page=<page_number>
    '''
    comments = serializers.SerializerMethodField('paginated_comments')

    '''
    TODO:
    Return total count of each reaction?
    Return flag if user reacted to tweet?
    achieve using SerializerMethodField where you get all objects and count?
    '''
    reactions = TweetReactionSerializer(read_only=True, many=True)

    class Meta:
        model = Tweet
        fields = (
            'id',
            'content',
            'created_at',
            'updated_at',
            # 'user_details',
            'user',
            'comments',
            'reactions'
        )

    def paginated_comments(self, obj):
        page_size = COMMENTS_PAGE_SIZE if COMMENTS_PAGE_SIZE else None
        if page_size:
            paginator = Paginator(obj.comments.all(), page_size)
            # return first page comments only
            comments = paginator.page(1)
            serializer = CommentSerializer(comments, many=True)
            '''
            QUESTIONS:
            - how to return paginated info such as total object count, number of pages etc?
            - information is available in paginator object
                > paginator.count
                > paginator.num_pages
                > paginator.page_range
            '''
            return serializer.data

        # QUESTIONS: correct way to throw an exception?
        raise Exception('PAGE_SIZE not set for REST_FRAMEWORK in settings.py')
