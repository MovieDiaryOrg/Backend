from movieDiary.serializers import TestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movies.models import Movie
from movieDiary.models import LikedJournal, MovieJournal
from django.db.models import Count


@api_view(['GET'])
def mainPage(request): 
    # 오늘의 영화 반환 (좋아요를 가장 많이 받은 게시물의 영화)
    most_liked = (
        LikedJournal.objects
        .values('movie_journal_id')  # movie_journal_id 기준 그룹화
        .annotate(count=Count('movie_journal_id'))  # 등장 횟수 계산
        .order_by('-count')  # 내림차순 정렬
        .first()  # 가장 많은 movie_journal_id 가져오기
    )
    
    if not most_liked:
        movie = Movie.objects.filter(tmdb_id=693134).first()
        most_liked = {
            'count': 0
        }
    else:
        movie_journal_id = most_liked['movie_journal_id']
        print(f'movie_journal_id = {movie_journal_id}')
        movie = Movie.objects.filter(movieJournal__id=movie_journal_id).first()
    
    if not movie:
        return Response({"message": "No movie found for the most liked journal."}, status=404)
    
    # 기록 목록 제공
    movie_journals = MovieJournal.objects.annotate(likes_count=Count('likes')).select_related('user', 'movie')
    movie_journal_serializer = TestSerializer(movie_journals, many=True)
    
    response_data = {
        "popular_movie":{
            "tmdb_id": movie.tmdb_id,
            "title": movie.title,
            "genre": [genre.genre.name for genre in movie.movie_genre.all()],  # 수정된 장르 처리
            "image": movie.poster_path,
            "description": movie.description,
            "release_date": movie.release_date,
            "vote_average": movie.vote_average,
            "liked_count": most_liked['count'],
        },
        "movie_journals": []
    }
    
    # 직렬화된 데이터를 가져온 뒤 각 감상문별 좋아요 수 추가
    movie_journal_data = movie_journal_serializer.data
    for journal in movie_journal_data:
        journal_id = journal['id']
        journal_title = find_movie_title(journal['movie'])
        likes_count = LikedJournal.objects.filter(movie_journal_id=journal_id).count()  # 좋아요 수 계산
        journal['likes_count'] = likes_count  # 좋아요 수 추가
        
        response_data["movie_journals"].append({ 
            "title": journal_title,
            "movie_journal": journal
        })
    
    return Response(response_data)


def find_movie_title(movieObj):
    start = movieObj.find("(")
    movie_id = int(movieObj[start + 1:-1])
    
    find_movie = Movie.objects.get(pk=movie_id)
    return find_movie.title