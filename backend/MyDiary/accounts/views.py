from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# 왜 클래스로 생성했는지 이해 안 감
class UserRegisterAPIView(APIView):
    def post(self, request: Request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)     # JWT 토큰 생성
            return Response(
                {
                    'user': serializer.data,
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
