from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.settings import REST_FRAMEWORK as REST_FRAMEWORK_SETTINGS
from .models import CustomUser as User
from tweets.serializers import TweetSerializer

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


class CustomUserSerializer(serializers.ModelSerializer):

    '''
    NOTE: write_only=True fields are not returned by serializer
    '''
    email = serializers.EmailField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8, write_only=True)

    # 3 possible approaches to return data of related model.
    '''
    Approach 1
    returns formatted tweets
    '''
    # tweets = TweetsListingField(many=True, read_only=True)
    '''
    Approach 2
    return paginated tweets of a user - refer to paginated_tweet method
    - cant possibly return all tweets of a user in one response
    - to get more tweets of a user, make API endpoint to /users/:id/tweets/
    '''
    tweets = serializers.SerializerMethodField('paginated_tweet')

    '''
    Approach 3
    returns user tweets based on TweetSerializer
    '''
    # tweets = TweetSerializer(many=True, read_only=True)

    class Meta:
        model = User
        # every field could be attribute of model or a method => because using ModelSerializer?
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'tweets', # refers to related_name in Tweets model
            'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    '''
    Updating of password is through a different endpoint (/api/users/:id/password) and serializer (CustomUserPasswordSerializer)
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

    def validate_password_and_confirm_password(self, password, confirm_password):
        if not password == confirm_password:
            raise serializers.ValidationError({
                'error': 'Password and confirm password do not match.'
            })
        return

    def validate_email_existence(self, email):
        user = User.objects.filter(email=email).first()
        if user:
            raise serializers.ValidationError({
                'error': 'Email has already been taken.'
            })
        return

    def validate(self, attrs):
        '''
        validate that:
        1. password and confirm_password match
        2. email does not exist in DB
        '''
        data = self.context.get('request').data
        password = data.get('password')
        confirm_password = data.get('confirm_password', None)
        email = data.get('email')

        self.validate_password_and_confirm_password(password, confirm_password)
        # if not password == confirm_password:
        #     raise serializers.ValidationError({
        #         'error': 'Password and confirm password do not match.'
        #     })

        self.validate_email_existence(email)
        # user = User.objects.filter(email=email).first()
        # if user:
        #     raise serializers.ValidationError({
        #         'error': 'Email has already been taken.'
        #     })

        return super().validate(attrs)

    def get_pagination_results(self, object_serializer, objects, page_size):
        paginator = Paginator(objects, page_size)
        # return first page tweets only
        results = paginator.page(1)
        results_count = paginator.count
        total_num_of_pages = paginator.num_pages
        # paginator.page_range returns a Range object so we need to convert it to a list
        page_range = list(paginator.page_range)
        has_next_page = total_num_of_pages > 1
        serializer = object_serializer(results, many=True)
        return {
            'data': serializer.data,
            'count': results_count,
            'num_pages': total_num_of_pages,
            'has_next_page': has_next_page,
            'page_range': page_range
        }

    def paginated_tweet(self, obj):
        page_size = REST_FRAMEWORK_SETTINGS.get('PAGE_SIZE', None)
        if page_size:
            # paginator = Paginator(obj.tweets.all(), page_size)
            # # return first page tweets only
            # tweets = paginator.page(1)
            # serializer = TweetSerializer(tweets, many=True)
            # tweets_count = paginator.count
            # total_num_of_pages = paginator.num_pages
            # # paginator.page_range returns a Range object so we need to convert it to a list
            # page_range = list(paginator.page_range)
            # has_next_page = total_num_of_pages > 1
            # return {
            #     'data': serializer.data,
            #     'count': tweets_count,
            #     'num_pages': total_num_of_pages,
            #     'has_next_page': has_next_page,
            #     'page_range': page_range
            # }

            tweets = obj.tweets.all()
            return self.get_pagination_results(TweetSerializer, tweets, page_size)

        # QUESTIONS: correct way to throw an exception?
        raise Exception('PAGE_SIZE not set for REST_FRAMEWORK in settings.py')


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
