from rest_framework import serializers
from .models import MovieJournal, JournalComment, Recommended
from movies.models import Movie
from movies.serializers import MovieSerializer

class MovieJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieJournal
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'modified_at']  # 자동 생성 필드


class TestSerializer(serializers.ModelSerializer):
    # MovieJournal 관련 필드
    # 여기에 포함된 필드들은 무조건 입력받도록 요청하게 되므로, 
    # 필드는 존재하나 값을 입력받지 않도록 하고 싶으면 ModelSerializer의 필드에만 포함시키면 됨
    content = serializers.CharField()
    watched_date = serializers.DateField()
    user = serializers.SerializerMethodField()
    movie = serializers.CharField()
    evaluation = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = MovieJournal  # 어떤 모델을 기반으로 하는지 지정 -> 왜 꼭 해야하지?
        fields = ['id', 'content', 'watched_date', 'created_at', 'modified_at', 'movie', 'user', 'ai_img', 'evaluation']  # 포함할 필드 명시
        read_only_fields = ['id', 'created_at', 'modified_at', 'ai_img']
    
    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
        }
    
    # save() 메서드 실행 시 자동으로 호출됨
    def create(self, validated_data):
        print(f"validated_data = {validated_data['movie']}")
        selected_movie = self.get_movie(validated_data['movie'])
        
        # MovieJournal 생성
        movieJournal = MovieJournal.objects.create(
            content = validated_data['content'],
            ai_img = None,
            watched_date = validated_data['watched_date'],
            user = self.context['request'].user,         # request에서 user 정보 가져옴
            movie = selected_movie,
            evaluation = validated_data['evaluation'],
            hide = validated_data['hide'] if 'hide' in validated_data else False
        )

        return {
            "movieJournal": movieJournal,
        }
        
    def get_movie(self, movie_title):
        return Movie.objects.get(title=movie_title)

    
    def update(self, instance, validated_data):
        # 영화 제목이 전달되었을 경우, Movie 객체를 가져오기
        if 'movie' in validated_data:
            movie_title = validated_data.pop('movie')  # validated_data에서 'movie' 제거
            try:
                validated_data['movie'] = self.get_movie(movie_title)  # Movie 객체로 변환
            except Movie.DoesNotExist:
                raise serializers.ValidationError({"movie": f"Movie with title '{movie_title}' does not exist."})
        
        # 기존의 필드를 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    

class JournalCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalComment
        fields = ['id', 'content', 'user', 'created_at']  # 필요한 필드만 포함
        

class RecommendedMovieSerializer(serializers.ModelSerializer):
    # Movie 데이터를 직렬화함
    movie = MovieSerializer() 

    class Meta:
        model = Recommended
        fields = ['movie', 'reason']  # 필요한 필드만 직렬화