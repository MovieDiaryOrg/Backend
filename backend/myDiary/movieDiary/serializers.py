from rest_framework.serializers import DecimalField
from rest_framework import serializers
from .models import MovieJournal, JournalComment, MovieEvaluation, LikedJournal
from movies.models import Movie
from accounts.models import CustomUser

class MovieJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieJournal
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'modified_at']  # 자동 생성 필드
    
    # def validate_evaluation(self, value):
    #     # 검증 로직
    #     if value < 0 or value > 5.0:
    #         raise serializers.ValidationError("평가 점수는 0에서 5 사이여야 합니다.")
    #     return value


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieEvaluation
        fields = '__all__'
        read_only_fields = ['movie', 'user']            # 자동 생성 필드


class TestSerializer(serializers.ModelSerializer):
    # MovieJournal 관련 필드
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()
    watched_date = serializers.DateField()
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    # MovieEvaluation 관련 필드
    # 전체 자릿수: 4자, 소수점 아래 자릿수: 2자
    evaluation = serializers.DecimalField(max_digits=4, decimal_places=2, required=True)

    class Meta:
        model = MovieJournal  # 어떤 모델을 기반으로 하는지 지정 -> 왜 꼭 해야하지?
        fields = ['title', 'content', 'watched_date', 'movie', 'evaluation']  # 포함할 필드 명시

    # save() 메서드 실행 시 자동으로 호출됨
    def create(self, validated_data):
        # MovieJournal 생성
        movieJournal = MovieJournal.objects.create(
            title = validated_data['title'],
            content = validated_data['content'],
            ai_img = None,
            watched_date = validated_data['watched_date'],
            user = self.context['request'].user,         # request에서 user 정보 가져옴
            movie = validated_data['movie']
        )

        # MovieEvaluation 생성
        movieEvaluation = MovieEvaluation.objects.create(
            user = self.context['request'].user,
            movie = validated_data['movie'],
            evaluation = validated_data['evaluation']
        )

        return {
            "movieJournal": movieJournal,
            "movieEvaluation": movieEvaluation
        }
