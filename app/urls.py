from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

from users.views import CustomTokenObtainPairView, UserViewSet
from tweets.views import TweetViewSet
from comments.views import CommentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tweets', TweetViewSet, basename='tweet')
# router.register(r'tweets/<pk>/comments', CommentViewSet, basename='comments')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/<pk>/', include('users.urls')),
    # path('api/tweets/<pk>/comments/', include('comments.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_create'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
