from django.urls import path, include
from .views import CustomUserDetailsView, UserDeleteView

app_name = 'accounts'

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),    
    path('dj-rest-auth/user/', CustomUserDetailsView.as_view(), name='user_details'),
    path('user/delete/', UserDeleteView.as_view(), name='user_delete')
]
