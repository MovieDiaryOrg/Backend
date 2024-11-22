from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.views import UserDetailsView
from .serializers import CustomUserDetailSerializer
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
import logging

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
    serializer_class = CustomUserDetailSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_object(self):
        return self.request.user

    # PATCH 요청: 회원 정보 수정 
    def patch(self, request, *args, **kwargs):
        # 요청 데이터 로깅
        logger.info(f"Request Data: {request.data}")
        logger.info(f"Request Files: {request.FILES}")

        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.data, partial=True)
        
        # 유효성 검사 결과 로깅
        if not serializer.is_valid():
            logger.error(f"Serializer Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 저장 전 데이터 로깅
        logger.info(f"Validated Data: {serializer.validated_data}")
        
        try:
            # 저장 시도 (CustomUserDetailSerializer의 update() 메서드 실행)
            serializer.save()
            
            # 저장 후 객체 상태 로깅
            logger.info(f"Updated User Data: {self.object.__dict__}")
            
            return Response({
                'user': serializer.data,
                'message': '회원 정보 수정에 성공했습니다.',
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Save Error: {str(e)}")
            return Response({
                'error': str(e)
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