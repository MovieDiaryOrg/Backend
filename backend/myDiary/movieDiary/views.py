# views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieJournalSerializer, TestSerializer
from rest_framework.permissions import IsAuthenticated
from .models import MovieJournal, MovieEvaluation, Recommended
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
            self.movie_evaluation = rslt['movieEvaluation']
        else:
            self.movie_journal = rslt
        print(f'MovieJournal 객체가 생성되었습니다: {self.movie_journal}')

        # OpenAI API를 이용해 감상문 분석    
        self.create_ai_analystic(self.movie_journal.content)

        # OpenAI API를 이용해 그림 생성
        self.create_ai_img()
    
        response_data = {
            'url': ''                   # 클라이언트가 상세페이지를 조회하기 위해 사용할 url만 반환함
        }

        headers = self.get_success_headers(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    # mixin.CreateModelMixin 클래스 내부 메소드 오버라이딩
    def perform_create(self, serializer):
        return serializer.save()

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

    # ModelViewSet에서 destroy(delete) 메서드가 기본 제공되므로 오버라이드할 필요 없음
    # 특정 다이어리(journal)를 삭제함
    # @action(detail=True, method=['DELETE'], url_path='delete')
    # def delete_journal(self, request, pk=None):
    #     journal = self.get_object()
    #     journal.delete()
    #     return Response({'message': 'Journal deleted'}, status=status.HTTP_204_NO_CONTENT)