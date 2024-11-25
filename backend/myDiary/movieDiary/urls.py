from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import MovieJournalViewSet

app_name = 'movieDiary'

router = DefaultRouter()
router.register(r'', MovieJournalViewSet, basename='moviejournal')

# 커스텀 url 패턴
custom_urlpatterns = [
    path('list/', MovieJournalViewSet.as_view({'get': 'journalList'}), name='journalList'),
    path('<int:journal_pk>/like/', views.createLike, name='createLike'),
    path('<int:journal_pk>/comment/', views.createJournalComment, name='createJournalComment'),
    path('<int:comment_pk>/comment/delete/', views.deleteJournalComment, name='deleteJournalComment')
]

urlpatterns = router.urls + custom_urlpatterns