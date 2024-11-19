import requests
import json
from django.conf import settings

# TMDB API 키
api_key = settings.TMDB_API_KEY

# API 응답을 JSON 형식으로 담음
movies = []
genres = []

# 장르 데이터 받아오는 함수
def pull_genres():
    url = "https://api.themoviedb.org/3/genre/movie/list"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key,
        "language": "ko-KR"
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
def pull_kr_movies():
    url = "https://api.themoviedb.org/3/movie/top_rated"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    params = {
        "language": "ko-KR",
        "page": 3
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    for item in data['results']:
        try:
            dict = {
                'model': 'movies.movie',
                'pk': item['id'],
                'fields': {
                    "title": item['title'],
                    "release_date": item['release_date'],
                    "description": item['overview'],
                    "original_language": item['original_language'],
                    "poster_path": item['poster_path'],
                    "vote_average": item['vote_average'],
                    "adult": item['adult']
                }
            }
            movies.append(dict)
        except:
            pass
    
    with open('./fixtures/kor_movies.json', 'w', encoding='utf-8') as f:
        # json.dump: Python 객체를 JSON 형식으로 변환하여 파일에 저장하는 함수
        json.dump(movies, f, ensure_ascii=False, indent=4)


# 외국 영화 데이터 받아오는 함수
def pull_eng_movies():
    url = "https://api.themoviedb.org/3/movie/top_rated"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    params = {
        "language": "en-US",
        "page": 3
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    for item in data['results']:
        try:
            dict = {
                'model': 'movies.movie',
                'pk': item['id'],
                'fields': {
                    "title": item['title'],
                    "release_date": item['release_date'],
                    "description": item['overview'],
                    "original_language": item['original_language'],
                    "poster_path": item['poster_path'],
                    "vote_average": item['vote_average'],
                    "adult": item['adult']
                }
            }
            movies.append(dict)
        except:
            pass
    
    with open('./fixtures/eng_movies.json', 'w', encoding='utf-8') as f:
        # json.dump: Python 객체를 JSON 형식으로 변환하여 파일에 저장하는 함수
        json.dump(movies, f, ensure_ascii=False, indent=4)



if __name__ == '__main__':
    # 1. 장르 데이터 받아옴 (장르 더미 데이터 생성)
    pull_genres()
    # 2. 한국 영화 데이터 받아옴 (더미 데이터 생성)
    pull_kr_movies()
    # 2-2. 외국 영화 데이터 받아옴 (더미 데이터 생성)
    pull_eng_movies()