from django.urls import path, include
from .views import CustomUserUpdateView, UserDeleteView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),    
    path('dj-rest-auth/user/', CustomUserUpdateView.as_view(), name='user_details'),
    path('user/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
