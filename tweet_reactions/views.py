from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework import permissions, status

from tweets.models import Tweet
from .serializers import TweetReactionSerializer
from .permissions import IsTweetReactionOwner
from .models import TweetReaction

# print(Tweet.does)

class CreateUpdateDestroyTweetReaction(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):

    queryset = TweetReaction.objects.all()
    serializer_class = TweetReactionSerializer
    http_method_names = ['head', 'post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        '''
        if user already has a reaction to Tweet return 400 error
        '''
        tweet_id = self.kwargs.get('tweet_pk')
        try:
            print('checking')
            tweet_reaction = TweetReaction.objects.get(user_id=self.request.user, tweet_id=tweet_id)
            return Response(
                {
                    'error': f'Already reacted with {tweet_reaction.type}. Did you call the right API?'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print('performing_create')
        tweet_pk = self.kwargs.get('tweet_pk')
        tweet = get_object_or_404(Tweet, pk=tweet_pk)
        serializer.save(user=self.request.user, tweet=tweet)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = (permissions.IsAuthenticated,)
        else:
            permission_classes = (permissions.IsAuthenticated, IsTweetReactionOwner)
        return [permission() for permission in permission_classes]