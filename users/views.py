from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView, ListAPIView

from .models import CustomUser as User
from .serializers import (
    CustomUserSerializer as UserSerializer,
    CustomUserPasswordSerializer as UserPasswordSerializer,
    CustomTokenObtainPairSerializer
)
from .permissions import IsUserObjectOwner
from tweets.models import Tweet
from tweets.serializers import TweetListSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    '''
    Overwrite create method, else Django throws 500 error
    '''
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if email and user:
            return Response(
                {
                    'error': 'Email is already in used.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     queryset = SignupRequest.objects.filter(user=self.request.user)
    #     if queryset.exists():
    #         raise ValidationError('You have already signed up')
    #     serializer.save(user=self.request.user)

    def destroy(self):
        return Response(
            {
                'error': 'Not allowed.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

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

    def put():
        return Response(
            {
                'error': 'Method not allowed.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

class UserTweetList(ListAPIView):

    serializer_class = TweetListSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self,):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return Tweet.objects.filter(user=user)

