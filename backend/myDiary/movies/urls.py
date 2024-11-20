from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movieList, name='filterMovie'),            # 영화 전체 목록과 필터링 기능
    path('create/', views.createMovie, name='createMovie'),     # 영화 등록
    path('<int:pk>/', views.movieDetail, name='movieDetail'),   # 영화 상세보기, 수정
    path('<int:pk>/delete/', views.deleteMovie, name='deleteMovie'),    # 영화 삭제
]
