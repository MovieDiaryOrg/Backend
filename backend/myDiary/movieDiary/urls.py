from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import MovieJournalViewSet

app_name = 'movieDiary'

# urlpatterns = [
#     # 다이어리(MovieJournal) 관련
#     path('', views.createJournal, name='createJournal'),                    # 기록 생성
#     path('<int:pk>/', views.journalDetail, name='journalDetail'),           # 기록 조회 및 수정
#     path('<int:pk>/delete/', views.deleteJournal, name='deleteJournal'),    # 기록 삭제
#     path('<int:user_pk>/list/', views.journalList, name='journalList'),     # 기록 목록 조회
# ]


router = DefaultRouter()
router.register(r'', MovieJournalViewSet, basename='moviejournal')

# 커스텀 url 패턴
custom_urlpatterns = [
    path('<int:user_pk>/list/', MovieJournalViewSet.as_view({'get':'user_journals'}), name='journalList'),
    path('<int:journal_pk>/like/', views.createLike, name='createLike')
]

urlpatterns = router.urls + custom_urlpatterns