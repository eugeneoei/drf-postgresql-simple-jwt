from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from users.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_create'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
