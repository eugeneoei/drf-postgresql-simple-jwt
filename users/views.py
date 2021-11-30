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
                    'error': 'Email has already been taken.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = (permissions.AllowAny,)
        elif self.action in ['retrieve', 'update', 'partial_update']:
            '''
            TODO:
            refactor - IsAdminOrTargetUser custom permissions
            '''
            pk = self.kwargs.get('pk')
            if pk ==  str(self.request.user.id):
                permission_classes = (permissions.IsAuthenticated,)
            else:
                permission_classes = (permissions.IsAdminUser,)
        else:
            # covers list and destroy actions
            permission_classes = (permissions.IsAdminUser,)

        return [permission() for permission in permission_classes]

'''
TODO:
- Add UpdateAPIView to allow user to update password
- Check if given password matches current password
- Check if new password matches confirm password
- Check if new password matches current password
'''
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

    # def patch(self, request, *args, **kwargs):

    #     '''
    #     accepts:
    #     - password
    #     - new_password
    #     - confirm_new_password

    #     pop password and confirm_new_password???
    #     '''

    #     is_current_password_valid = self.request.user.check_password(request.data.get('password'))
    #     # print('is_current_password_valid >>', self.request.user.check_password(request.data.get('password')))
    #     if not is_current_password_valid:
    #         return Response(
    #             {
    #                 'error': 'Current password is incorrect.'
    #             },
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     return super().patch(request, *args, **kwargs)




    #     # print('pk >>', self.kwargs.get('pk'))
    #     # print('user.id >>', self.request.user.id)
    #     # pk = self.kwargs.get('pk')
    #     # if pk ==  str(self.request.user.id):
    #     #     permission_classes = (permissions.IsAuthenticated,)

    #     return Response(
    #         {
    #             'error': 'Method not allowed.'
    #         },
    #         status=status.HTTP_405_METHOD_NOT_ALLOWED
    #     )