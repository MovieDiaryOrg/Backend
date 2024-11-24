from django.urls import path
from . import views
from .views import MovieViewSet

app_name = 'movies'

urlpatterns = [
    path('', MovieViewSet.as_view({'get': 'list'}), name='filterMovie'), # 영화 전체 목록과 필터링 기능
]
