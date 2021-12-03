
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView

from .models import CustomUser as User
from .serializers import (
    CustomUserSerializer as UserSerializer,
    CustomUserPasswordSerializer as UserPasswordSerializer,
    CustomTokenObtainPairSerializer
)
from .permissions import IsUserObjectOwner

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['head', 'get', 'post', 'patch']

    def get_permissions(self):
        if self.action in ['create', 'retrieve', 'list']:
            permission_classes = (permissions.AllowAny,)

        elif self.action in ['update', 'partial_update']:
            permission_classes = (IsUserObjectOwner,)
        else:
            # covers destroy action
            permission_classes = (permissions.IsAdminUser,)

        return [permission() for permission in permission_classes]


class UserPasswordUpdate(UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserPasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['head', 'patch']
