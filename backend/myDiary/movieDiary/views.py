# views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .serializers import MovieJournalSerializer, TestSerializer
from rest_framework.permissions import IsAuthenticated
from .models import MovieJournal, Recommended, LikedJournal
from movies.models import Movie, Genre, MovieGenre
from django.conf import settings
from openai import OpenAI
import json
from django.core.exceptions import ValidationError

"""
ModelViewSet은 기본적인 CRUD 작업을 제공하며, 
커스텀 동작이 필요하다면 ViewSet의 메서드를 오버라이드하거나 @action 데코레이터를 사용해야 함.
"""

class MovieJournalViewSet(ModelViewSet):
    queryset = MovieJournal.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]          # 인증된 사용자만 접근 가능함
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dalle_prompt = ''  # 인스턴스 속성으로 dalle_prompt 선언
        self.movie_journal = None
        self.movie_evaluation = None
        self.OPENAI_API_KEY = settings.OPENAI_API_KEY
    
    # 상세조회
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data
        movie_title = self.get_movie_id(data)
        
        data['movie'] = movie_title
        data['likes'] = len(instance.likes.all())
        data['comments'] = instance.comments.all()

        return Response(data)

    # ModelViewSet 클래스가 상속받는 mixins.CreateModelMixin 클래스의 create() 오버라이딩
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):                   # 유효성 검사
            print(serializer.errors)
            raise ValidationError(serializer.errors)
        
        # MovieJournal, MovieEvaluation 객체 생성
        rslt = self.perform_create(serializer)

        print(f'rslt = {rslt}')

        if isinstance(rslt, dict):
            if not rslt.get("movieJournal"):
                raise ValueError("MovieJournal 객체 생성에 실패했습니다.")
            self.movie_journal = rslt['movieJournal']
        else:
            self.movie_journal = rslt
        print(f'MovieJournal 객체가 생성되었습니다: {self.movie_journal}')

        # OpenAI API를 이용해 감상문 분석    
        self.create_ai_analystic(self.movie_journal.content)

        # OpenAI API를 이용해 그림 생성
        self.create_ai_img()
    
        response_data = {
            'url': f'http://localhost:8000/movieDiary/{self.movie_journal.id}/'                   # 클라이언트가 상세페이지를 조회하기 위해 사용할 url만 반환함
        }

        headers = self.get_success_headers(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    # 수정 요청 처리 (PATCH)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # partial 여부 결정
        instance = self.get_object()  # 기존 인스턴스 가져오기
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if not serializer.is_valid(raise_exception=True):
            print(serializer.errors)
            raise ValidationError(serializer.errors)

        # MovieJournal 객체 업데이트
        self.movie_journal = serializer.save()
        print(f"MovieJournal 객체가 수정되었습니다: {self.movie_journal}")

        # OpenAI API를 이용해 감상문 분석
        self.create_ai_analystic(self.movie_journal.content)

        # OpenAI API를 이용해 그림 생성
        self.create_ai_img()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        print(f'list_request = {request.data}')
        # queryset = self.filter_queryset(self.get_queryset())

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
    
    
    # mixin.CreateModelMixin 클래스 내부 메소드 오버라이딩
    def perform_create(self, serializer):
        return serializer.save()

    def get_movie_id(self, data):
        to_slice = data['movie']
        position = to_slice.find('(')
        movie_id = int(to_slice[position+1:-1])
        
        title = Movie.objects.get(tmdb_id=movie_id).title
        
        return title
        
    def create_ai_analystic(self, content):
        """
        OpenAI API를 이용해 추천 영화 및 그림 생성 프롬프트 생성
        """
        client = OpenAI(api_key=self.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model = "gpt-4o",
            messages = [
                {
                    "role": "system",
                    "content": "아래 기준에 따라 영화 리뷰를 분석하여 리뷰어의 만족도를 분석하세요. 응답은 반드시 JSON 객체여야 하며, JSON 스키마는 response_format를 따릅니다. 그리고 이어서 볼 만한 실제 영화 세 편을 추천하고, 영화 개봉일과 추천 이유를 포함하여 작성하세요. 그리고 DALL.E에게 리뷰에 담긴 리뷰어의 감정이나 영화의 줄거리를 잘 설명하는 그림을 요청하기 위한 프롬프트를 작성합니다. 그림의 스타일은 색연필이나 크레용으로 그려진 그림입니다. 1. Positive words describe feelings: good, great, inspiring, funny, enjoyable, enjoyable, cool, impressive, impressive, great, lovely, fascinating. Evaluate a movie: perfect, artistic, engaging, entertaining, emotional, fresh, moving, intense, shocking, admire, impressive. Acting/Characters: Great acting, naturalistic, characters come alive, relatable, realistic, great characters, fits the part, well acted. Directing/Composition: Interesting, thrilling, well-structured, perfectly directed, engaging, rhythmic, stylishly directed, original, novel. 2. negative words express emotions: disappointing, not good, unfortunate, boring, unpleasant, childish, awkward, unnecessary, unreasonable. Evaluate the movie: unrealistic, flimsy, lacking, predictable, clichéd, distracting, disappointing, old, outdated. Acting/Characters: Unnatural, out of place, forced, exaggerated, unsympathetic, hard to understand, unlikable. Directing/Composition: Loose, predictable, convoluted, wordy, esoteric, uninvolving, sloppy, exhausting. 3. neutral words express anticipation: anticipated, unexpected, surprising, twist, mystery, meaningful, thought-provoking. Evaluate the movie: decent, unique, independent, emotional, lingering, noteworthy, noteworthy. Acting/Characters: Acting, Characterization, Acting, Symbolic. Directing/Composition: Epic, well organized, well directed, has style'"
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            
            response_format = {
                "type": "json_schema",
                "json_schema" : {
                    "name": "diary_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "analysis": {
                                "type": "string",
                                "description": "A detailed analysis of the movie review."
                            },
                            "movie_recommendations": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties":{
                                        "title": {
                                            "type": "string",
                                            "description": "The title of the recommended movie."
                                        },
                                        "release_date" :{
                                            "type": "string",
                                            "description": "The release date of the movie."
                                        },
                                        "reason": {
                                            "type": "string",
                                            "description": "The reason for recommending the movie in korean."
                                        }
                                    },
                                    "required": ["title", "release_date", "reason"],
                                    "additionalProperties": False
                                }
                            },
                            "dalle_prompt": {
                                "type": "string",
                                "description": "The prompt for generating an image using DALL.E3 in english."
                            }
                        },
                        "required": ["analysis", "movie_recommendations", "dalle_prompt"],
                        "additionalProperties": False
                    }
                }
            }
        )

        response_content = response.choices[0].message.content
        try:
            parsed_content = json.loads(response_content)
        except json.JSONDecodeError as e:
            print(f'JSON 파싱 중 오류 발생 : {e}')
        
        random_recommend = [(11, '광선검이 멋져요'), (13, '불가능에 대한 고찰'), (105, '유쾌함에 취하고 싶다')]
        idx = 0

        analysis = json.loads(response_content)["analysis"]
        movie_recommend = json.loads(response_content)["movie_recommendations"]
        made_prompt = json.loads(response_content)["dalle_prompt"]

        # dall.e에 사용할 프롬프트 저장
        self.dalle_prompt = made_prompt

        # recommended 객체 생성
        for recommend in movie_recommend:
            movie = Movie.objects.filter(title=recommend['title'])
            if movie:
                reason = recommend['reason']
            else:
                movie = Movie.objects.filter(tmdb_id= random_recommend[idx][0])
                reason = random_recommend[idx][1]
                idx += 1
            
            recommended = Recommended(movie=movie[0], movie_journal=self.movie_journal, reason=reason)
            recommended.save()

    def create_ai_img(self):
        """
        DALL.E3를 이용해 그림 생성
        """
        client = OpenAI(api_key=self.OPENAI_API_KEY)
        response = client.images.generate(
            model="dall-e-3",
            prompt= self.dalle_prompt,
            size="1024x1024",
            quality="hd",
            n=1
        )

        ai_image_url = response.data[0].url
        self.movie_journal.ai_img = ai_image_url
        self.movie_journal.save()               # 수정사항 저장

    # 로그인한 사용자의 다이어리 목록 반환
    @action(detail=False, methods=["GET"], url_path='(?P<user_pk>[^/.]+)/list')
    # detail=False는 단일 객체가 아닌, 목록 조회용 메서드임을 나타냄
    def user_journals(self, request, user_pk=None):
        if user_pk:
            journals = self.queryset.filter(user_id=user_pk)
        else:
            journals = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(journals, many=True)
        return Response(serializer.data)
    

@login_required
@api_view(['POST'])
def createLike(request, journal_pk):
    movie_journal = MovieJournal.objects.get(pk=journal_pk)

    # 중복 체크 및 LikedJournal 생성
    like, created = LikedJournal.objects.get_or_create(movie_journal = movie_journal, user=request.user)

    if created:
        message = "Like created successfully!"
    else:
        # 기존 LikedJournal 객체 삭제
        like.delete()
        message = "Like removed successfully."

    return JsonResponse({"message": message})



