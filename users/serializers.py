from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser as User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        '''
        Add custom claims here
        Implmentation is for demo purposes
        In fact, is_staff value can be retrieved by calling self.request.user.is_staff
        '''
        token['is_staff'] = user.is_staff
        return token

class CustomUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    '''
    Using a different API for updating of password
    '''
    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            raise serializers.ValidationError(
                {
                    'error': 'Incorrect API endpoint to update password.'
                }
            )
        return super().update(instance, validated_data)

class CustomUserPasswordSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, min_length=8, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            'new_password',
            'confirm_new_password'
        )

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            if not user.check_password(data['password']):
                raise serializers.ValidationError({
                    'error': 'Current password is incorrect.'
                })

            if data['new_password'] != data['confirm_new_password']:
                raise serializers.ValidationError({
                    'error': 'New password and confirm new password do not match.'
                })
        return data

    '''
    update method needs to be implmented
    '''
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        '''
        TODO:
        - invalidate all tokens that belong to this user
        '''
        return instance
