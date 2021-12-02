from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin

from users.models import CustomUser as User
from .models import Tweet
from .serializers import TweetSerializer
from .permissions import IsTweetOwner

class TweetViewSet(ModelViewSet):

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        '''
        overwrite method to set user field in Tweet to user in request

        Resources:
        - https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-perform-create
        '''
        serializer.save(user=self.request.user)

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            permission_classes = (permissions.AllowAny,)
        elif self.action == 'create':
            permission_classes = (permissions.IsAuthenticated,)
        else:
            '''
            covers update, partial_update and destroy
            '''
            permission_classes = (IsTweetOwner, )

        return [permission() for permission in permission_classes]

class UserTweetList(ListModelMixin, GenericViewSet):

    serializer_class = TweetSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self,):
        user = get_object_or_404(User, pk=self.kwargs.get('user_pk'))
        return Tweet.objects.filter(user=user)
