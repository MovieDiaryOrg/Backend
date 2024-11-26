from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.views import UserDetailsView
from .serializers import CustomUserUpdateSerializer
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from .models import CustomUser
from rest_framework.decorators import api_view
from movieDiary.serializers import JournalCommentSerializer


# CBV(Class-Based View, 클래스 기반 뷰)
# 클래스 매개변수에 LoginRequiredMixin을 추가하면, 인증된 사용자만 뷰에 접근하도록 할 수 있다.
class UserRegisterAPIView(APIView):
    def post(self, request: Request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)     # JWT 토큰 생성
            profile_image_url = (
                request.build_absolute_uri(user.profile_image.url)
                if user.profile_image else None
            )
            return Response(
                {
                    'user': serializer.data,
                    'profile_image_url': profile_image_url,
                    'message': 'Register successful',
                    'token': {
                        'access': str(refresh_token.access_token),
                        'refresh': str(refresh_token)
                    },
                },
                status = status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    def post(self, request: Request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = validated_data.get('user')
            tokens = validated_data.get('tokens')

            return Response({
                'user': {
                    'username':user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': user.phone
                },
                'message': '로그인에 성공하였습니다.',
                'token': tokens,
            },
            status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

logger = logging.getLogger(__name__)

class CustomUserUpdateView(UserDetailsView):
    serializer_class = CustomUserUpdateSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        
        # 요청 데이터 로깅
        logger.info(f"Request Data: {request.data}")
        logger.info(f"Request Files: {request.FILES}")

        # Serializer 초기화 (partial=True로 부분 수정 허용)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        # 데이터 유효성 검사
        if not serializer.is_valid():
            logger.error(f"Serializer Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 유효성 통과 후 validated_data 확인
        logger.info(f"Validated Data: {serializer.validated_data}")

        # 비밀번호 변경 여부 확인
        new_password = serializer.validated_data.get('new_password1')
        try:
            # Serializer의 update() 메서드에서 비밀번호 변경 및 회원 정보 수정 처리
            serializer.save()

            # 저장 후 상태 로깅
            logger.info(f"Updated User Data: {user.__dict__}")

            # 성공 응답 반환
            response_data = {
                'user': serializer.data,
                'message': '회원 정보 및 비밀번호 변경에 성공했습니다.' if new_password else '회원 정보 수정에 성공했습니다.'
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Save Error: {str(e)}")
            return Response({
                'error': str(e),
                'message': '회원 정보 수정 중 오류가 발생했습니다.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    
    def delete(self, request):
        try:
            # 현재 사용자 객체 가져오기
            user = self.get_object()
            
            # 로그인 토큰 무효화
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
            
            # JWT 토큰 블랙리스트에 추가 (선택적)
            try:
                refresh_token = request.data.get('refresh_token')
                if refresh_token:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
            except Exception as e:
                logger.warning(f"Token blacklist failed: {str(e)}")
            
            # 사용자 비활성화
            user.is_active = False
            user.save()
            
            # 로그아웃
            logout(request)
            
            # 성공 응답
            return Response({
                'message': '회원 탈퇴가 성공적으로 처리되었습니다.',
                'detail': '계정이 비활성화되었습니다.'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"User deletion failed: {str(e)}")
            return Response({
                'message': '회원 탈퇴 처리 중 오류가 발생했습니다.',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        response_data = self.detail()
        return Response(response_data)
    
    def detail(self):
        user = self.request.user
    
        # 좋아요한 감상문 리스트
        liked_journals = user.likes.all()
        response_like = [
            {
                'id': like.id,
                'title': like.movie_journal.movie.title,
                'image': like.movie_journal.ai_img.url if like.movie_journal.ai_img else None,
                'writer': like.movie_journal.user.username,
                'evaluation': like.movie_journal.evaluation,
                'like_count': like.movie_journal.likes.count()
            }
            for like in liked_journals]
        
        # 작성한 댓글 리스트
        write_comments = [
            {
                'id': comment.id,
                'content': comment.content,
                'created_at': comment.created_at,
                'movie_journal': comment.movie_journal.id,
                'movie_title': comment.movie_journal.movie.title
            }
            for comment in user.comments.select_related('movie_journal__movie').all()
            # selected_related: JOIN 쿼리 사용 -> N + 1 문제 방지
        ]
        
        followers = user.followers.all()
        followings = user.followings.all()
        
        # 팔로워/팔로잉 데이터 직렬화
        followers_data = [{"id": follower.id, 
                           "username": follower.username,
                           "email": follower.email,
                           "profile_image": follower.profile_image.url if follower.profile_image else None
                           } 
                          for follower in followers]
        
        followings_data = [{"id": following.id, 
                            "username": following.username,
                            "email": following.email,
                            "profile_image": following.profile_image.url if following.profile_image else None
                           } 
                           for following in followings]
        
        response_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'profile_image': user.profile_image.url if user.profile_image else None,
            'follower_count': followers.count(),
            'following_count': followings.count(),
            'liked_journals': response_like,
            'write_comments': write_comments,
            'followers': followers_data,
            'followings': followings_data
        }
        
        return response_data

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]




@api_view(['POST', 'DELETE'])
@login_required
def follow(request, pk):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(CustomUser, pk=pk)

        if request.user != user_to_follow:
            if user_to_follow in request.user.followings.all():
                # 언팔로우 처리
                request.user.followings.remove(user_to_follow)
                return Response("언팔로우", status=status.HTTP_200_OK)
            else:
                # 팔로우 처리
                request.user.followings.add(user_to_follow)
                return Response("팔로잉", status=status.HTTP_200_OK)

