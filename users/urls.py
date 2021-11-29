from django.urls import path

from .views import HelloWorldView, UserCreate, Protected

app_name = 'users'
urlpatterns = [
    path('hello/', HelloWorldView.as_view(), name='hello_world'),
    path('', UserCreate.as_view(), name='users_create'),
    path('protected/', Protected.as_view(), name='users_protected')
]
