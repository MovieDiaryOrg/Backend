from django.db import models
from accounts.models import CustomUser
from movies.models import Movie

# Create your models here.
class MovieJournal(models.Model):
    content = models.TextField()
    ai_img = models.ImageField(upload_to='ai_images/', null=True, blank=True)
    watched_date = models.DateField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    recommended_list = models.JSONField(default=list)        # 기본값을 빈 리스트로 설정함
    evaluation = models.CharField(default=0, max_length=50, blank=False)          # 'good/not bad/bad' 중에 선택되어 입력
    hide = models.BooleanField(default=False,)
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='movieJournal')
    # 해당 영화에 대한 감상문이 하나라도 작성되어 있으면 영화 정보를 삭제할 수 없도록 함
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name='movieJournal')
    
    
class Recommended(models.Model):
    reason = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_journal = models.ForeignKey(MovieJournal, on_delete=models.CASCADE, related_name='recommends')


class LikedJournal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'likes')
    movie_journal = models.ForeignKey(MovieJournal, on_delete=models.CASCADE, related_name='likes')


class JournalComment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    movie_journal = models.ForeignKey(MovieJournal, on_delete=models.CASCADE, related_name='comments')
