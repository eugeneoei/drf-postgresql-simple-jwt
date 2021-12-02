from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentOwner
from tweets.models import Tweet

class CommentViewSet(ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        '''
        QUESTIONS
        is there a better way to filter? doesn't seem like an implementation like this will scale well
        '''
        queryset = Comment.objects.all()
        tweets_pk = self.kwargs.get('tweet_pk')
        queryset = queryset.filter(tweet_id=tweets_pk)
        return queryset

    def perform_create(self, serializer):
        tweets_pk = self.kwargs.get('tweet_pk')
        tweet = get_object_or_404(Tweet, pk=tweets_pk)
        serializer.save(user=self.request.user, tweet=tweet)

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            permission_classes = (permissions.AllowAny,)
        elif self.action == 'create':
            permission_classes = (permissions.IsAuthenticated,)
        else:
            '''
            covers update, partial_update and destroy
            '''
            permission_classes = (IsCommentOwner, )

        return [permission() for permission in permission_classes]
