from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet

from .models import Tweet
from .serializers import TweetSerializer

# list
# create
# retrieve
# update
# partial_update
# destroy

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
            TODO:
            refactor - IsAdminOrTargetUser custom permissions

            covers update, partial_update and destroy actions
            '''
            pk = self.kwargs.get('pk')
            if pk ==  str(self.request.user.id):
                permission_classes = (permissions.IsAuthenticated,)
            else:
                permission_classes = (permissions.IsAdminUser,)

        return [permission() for permission in permission_classes]
