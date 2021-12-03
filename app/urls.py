from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from users.views import CustomTokenObtainPairView, UserViewSet
from tweets.views import TweetViewSet, UserTweetList
from comments.views import CommentViewSet
from tweet_reactions.views import CreateUpdateDestroyTweetReaction

router = DefaultRouter()
router.register(r'api/users', UserViewSet, basename='users')
router.register(r'api/tweets', TweetViewSet, basename='tweets')

user_tweets_router = NestedSimpleRouter(router, r'api/users', lookup='user')
user_tweets_router.register(r'tweets', UserTweetList, basename='user_tweets')

# value in lookup becomes variable represented in url params => "<lookup_string>_pk"
tweets_router = NestedSimpleRouter(router, r'api/tweets', lookup='tweet')
tweets_router.register(r'comments', CommentViewSet, basename='tweet_comments')
tweets_router.register(r'reactions', CreateUpdateDestroyTweetReaction, basename='tweet_reactions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include(tweets_router.urls)),
    path('', include(user_tweets_router.urls)),
    path('api/users/<pk>/', include('users.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_create'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
