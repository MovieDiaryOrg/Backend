import requests
import json
import os
import sys
import django
from django.conf import settings

# Django 프로젝트 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치
project_root = os.path.dirname(current_dir)  # 프로젝트 루트 경로(MyDiary)
sys.path.append(project_root)


# Django 환경 설정 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myDiary.settings')
django.setup()


# TMDB API 키
api_key = settings.TMDB_API_KEY

# API 응답을 JSON 형식으로 담음
movies = []
genres = []
movie_genre = []

# 장르 데이터 받아오는 함수
def pull_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=ko-KR"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key,
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    for item in data['genres']:
        try:
            dict = {
                'model': 'movies.genre',
                'pk': item['id'],
                'fields': {
                    'name': item['name']
                }
            }
            genres.append(dict)
        except:
            pass
    with open('./fixtures/genres.json', 'w', encoding='utf-8') as f:
        # json.dump: Python 객체를 JSON 형식으로 변환하여 파일에 저장하는 함수
        json.dump(genres, f, ensure_ascii=False, indent=4)


# 한국 영화 데이터 받아오는 메서드
def pull_kr_movies(pg_num):
    url = "https://api.themoviedb.org/3/movie/top_rated"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    params = {
        "language": "ko-KR",
        "page": str(pg_num)
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    for item in data['results']:
        try:
            dict1 = {
                'model': 'movies.movie',
                'pk': item['id'],
                'fields': {
                    "title": item['title'],
                    "release_date": item['release_date'],
                    "description": item['overview'],
                    "original_language": item['original_language'],
                    "poster_path": 'https://image.tmdb.org/t/p/w600_and_h900_bestv2' + item['poster_path'],
                    "vote_average": item['vote_average'],
                    "adult": item['adult']
                }
            }
            
            for gr in item['genre_ids']:
                dict2 = {
                    'model': 'movies.moviegenre',
                    'fields': {
                        'movie_id': item['id'],
                        'genre_id' : int(gr)
                    }
                }
                movie_genre.append(dict2)
            movies.append(dict1)
        except:
            pass


# 외국 영화 데이터 받아오는 함수
def pull_eng_movies(pg_num):
    url = "https://api.themoviedb.org/3/movie/top_rated"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    params = {
        "language": "en-US",
        "page": str(pg_num)
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    for item in data['results']:
        try:
            dict1 = {
                'model': 'movies.movie',
                'pk': item['id'],
                'fields': {
                    "title": item['title'],
                    "release_date": item['release_date'],
                    "description": item['overview'],
                    "original_language": item['original_language'],
                    "poster_path": 'https://image.tmdb.org/t/p/w600_and_h900_bestv2' + item['poster_path'],
                    "vote_average": item['vote_average'],
                    "adult": item['adult']
                }
            }
            
            for gr in item['genre_ids']:
                dict2 = {
                    'model': 'movies.moviegenre',
                    'fields': {
                        'movie_id': item['id'],
                        'genre_id' : int(gr)
                    }
                }
                movie_genre.append(dict2)
            movies.append(dict1)
        except:
            pass


if __name__ == '__main__':
    cnt = 1

    # 1. 장르 데이터 받아옴 (장르 더미 데이터 생성)
    pull_genres()
    # 2. 한국 영화 데이터 받아옴 (더미 데이터 생성)
    # while cnt < 400:
    #     pull_kr_movies(cnt)
    #     cnt += 1
    # 2-2. 외국 영화 데이터 받아옴 (더미 데이터 생성)
    # while cnt < 400:
    #     pull_eng_movies(cnt)
    #     cnt += 1

    # with open('./fixtures/movies.json', 'w', encoding='utf-8') as f:
    #     # json.dump: Python 객체를 JSON 형식으로 변환하여 파일에 저장하는 함수
    #     json.dump(movies, f, ensure_ascii=False, indent=4)

    # with open('./fixtures/movie_genre.json', 'w', encoding='utf-8') as f:
    #     # json.dump: Python 객체를 JSON 형식으로 변환하여 파일에 저장하는 함수
    #     json.dump(movie_genre, f, ensure_ascii=False, indent=4)