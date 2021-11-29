from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView

from .models import CustomUser
from .serializers import CustomUserSerializer

class HelloWorldView(APIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(
            data={
                'hello': 'world'
            },
            status=status.HTTP_200_OK
        )

class Protected(APIView):

    # permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(
            data={
                'protected': 'route'
            },
            status=status.HTTP_200_OK
        )

class UserCreate(CreateAPIView):

    '''
    TODO: check if email already exist before creation
    '''

    permission_classes = (permissions.AllowAny,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
