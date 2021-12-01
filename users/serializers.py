# from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser as User
# from tweets.models import Tweet

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

'''
to modify data returned. otherwise, returns tweet id only
works only if there is a many-to-one relationship established
'''
class TweetsListingField(serializers.RelatedField):

    def to_representation(self, value):
        return {
            'id': value.id,
            'content': value.content,
            'created_at': value.created_at
        }


# class UserTweetSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Tweet
#         fields = (
#             'id',
#             'content',
#             'created_at'
#         )


class CustomUserSerializer(serializers.ModelSerializer):

    '''
    NOTE: write_only=True fields are not returned by serializer
    '''
    email = serializers.EmailField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    '''
    Possible approaches to return related model. Though, unlikely to be applicable for many-to-one relationship
    since query will not be efficient and response will bloat.

    In this case, a better implementation could be to have an endpoint to return tweets of a user eg
    /users/:id/tweets/

    Seems more ideal for one-to-one relationship.
    '''
    # returns formatted tweets
    tweets = TweetsListingField(many=True, read_only=True)
    # # returns paginated tweets
    # tweets = serializers.SerializerMethodField('paginated_tweet')

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'tweets', # refers to related_name in Tweets model
            'password'
        )
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

    # def paginated_tweet(self, obj):
    #     page_size = self.context['request'].query_params.get('size') or 2
    #     # page_size = self.context['request'].query_params.get('size') or 10
    #     paginator = Paginator(obj.tweets.all(), page_size)
    #     page = self.context['request'].query_params.get('page') or 1
    #     tweets = paginator.page(page)
    #     serializer = UserTweetSerializer(tweets, many=True)
    #     print('')
    #     print('obj >>', obj)
    #     print('count >>', paginator.count)
    #     print('num_pages >>', paginator.num_pages)
    #     print('page_range >>', paginator.page_range)
    #     print('-----------------------')
    #     '''
    #     QUESTIONS: how to return paginated info such as total object count, number of pages etc?
    #     '''
    #     return serializer.data


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
