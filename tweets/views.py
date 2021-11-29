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

    # def create(self, request, *args, **kwargs):
    #     # email = request.data.get('email')
    #     # user = User.objects.filter(email=email).first()
    #     # if email and user:
    #     #     return Response(
    #     #         {
    #     #             'error': 'Email has already been taken.'
    #     #         },
    #     #         status=status.HTTP_400_BAD_REQUEST
    #     #     )
    #     # return super().create(request, *args, **kwargs)
    #     print(self.request.user.id)
    #     return Response(
    #         {
    #             'create': 'tweet'
    #         },
    #         status=status.HTTP_201_CREATED
    #     )

    def perform_create(self, serializer):
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
