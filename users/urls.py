from django.urls import path

from .views import UserPasswordUpdate

app_name = 'users'
urlpatterns = [
    path('<pk>/password/', UserPasswordUpdate.as_view(), name='password_update'),
]