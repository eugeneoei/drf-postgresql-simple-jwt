from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework import permissions, status

from tweets.models import Tweet
from .serializers import TweetReactionSerializer
from .permissions import IsTweetReactionOwner
from .models import TweetReaction

class CreateUpdateDestroyTweetReaction(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):

    queryset = TweetReaction.objects.all()
    serializer_class = TweetReactionSerializer
    http_method_names = ['head', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        tweet_pk = self.kwargs.get('tweet_pk')
        tweet = get_object_or_404(Tweet, pk=tweet_pk)
        serializer.save(user=self.request.user, tweet=tweet)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = (permissions.IsAuthenticated,)
        else:
            permission_classes = (permissions.IsAuthenticated, IsTweetReactionOwner)
        return [permission() for permission in permission_classes]