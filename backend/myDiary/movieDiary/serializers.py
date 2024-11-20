from rest_framework import serializers
from .models import MovieJournal, JournalComment, MovieEvaluation, LikedJournal

class MovieJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieJournal
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'modified_at']  # 자동 생성 필드
