from django.urls import path

from .views import UserPasswordUpdate, UserTweetList

app_name = 'users'
urlpatterns = [
    path('<pk>/password/', UserPasswordUpdate.as_view(), name='password_update'),
    path('<pk>/tweets/', UserTweetList.as_view(), name='tweet_list'),
]