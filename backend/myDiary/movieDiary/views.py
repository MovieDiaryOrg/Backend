from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieJournalSerializer
from rest_framework.permissions import IsAuthenticated
from .models import MovieJournal, Movie, MovieEvaluation

"""
ModelViewSet은 기본적인 CRUD 작업을 제공하며, 
커스텀 동작이 필요하다면 ViewSet의 메서드를 오버라이드하거나 @action 데코레이터를 사용해야 함.
"""

class MovieJournalViewSet(ModelViewSet):
    queryset = MovieJournal.objects.all()
    serializer_class = MovieJournalSerializer
    permission_classes = [IsAuthenticated]          # 인증된 사용자만 접근 가능함
    
    # ModelViewSet 클래스가 상속받는 mixins.CreateModelMixin 클래스의 create() 오버라이딩
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # OpenAI API를 이용해 감상문 분석    
        self.create_ai_analystic()

        # OpenAI API를 이용해 그림 생성
        self.create_ai_img()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def create_ai_analystic(self):
        """
        OpenAI API를 이용해 추천 영화 및 그림 생성 프롬프트 생성
        """

    def create_ai_img(self):
        """
        DALL.E3를 이용해 그림 생성
        """

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