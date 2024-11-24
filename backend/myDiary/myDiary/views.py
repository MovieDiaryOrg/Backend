from movieDiary.serializers import TestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movies.models import Movie
from movieDiary.serializers import MovieJournalSerializer
from movieDiary.models import LikedJournal, MovieJournal
from django.db.models import Count


@api_view(['GET'])
def mainPage(request): 
    # 오늘의 영화 반환
    most_liked = (
        LikedJournal.objects
        .values('movie_journal_id')  # movie_journal_id 기준 그룹화
        .annotate(count=Count('movie_journal_id'))  # 등장 횟수 계산
        .order_by('-count')  # 내림차순 정렬
        .first()  # 가장 많은 movie_journal_id 가져오기
    )
    
    if not most_liked:
        return Response({"message": "No liked journals found."}, status=404)
    
    movie_journal_id = most_liked['movie_journal_id']
    movie = Movie.objects.filter(moviejournal__id=movie_journal_id).first()
    
    if not movie:
        return Response({"message": "No movie found for the most liked journal."}, status=404)

    
    # 기록 목록 제공
    movie_journals = MovieJournal.objects.all()
    movie_journal_serializer = MovieJournalSerializer(movie_journals, many=True)
    
    return Response({
        "popular_movie":{
            "tmdb_id": movie.tmdb_id,
            "title": movie.title,
            "poster_path": movie.poster_path,
            "description": movie.description,
            "release_date": movie.release_date,
            "vote_average": movie.vote_average,
            "liked_count": most_liked['count']    
        },
        "movie_journals": movie_journal_serializer.data
    })
    
    
