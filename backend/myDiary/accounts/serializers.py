from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from backend.MyDiary.accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

# 순환 참조를 막기 위해 사용함 (완전히 이해는 안됨)
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User        # CustomUser가 이미 AUTH_USER_MODEL에 설정되었으므로
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone', 'image']
        extra_kwargs = {
            'password': {'write_only': True},
            'image': {'required': False}
        }

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        
        image = data.get('image')
        if image and image.size > 5 * 1024 * 1024: 
            raise serializers.ValidationError({
                "image": "이미지 파일은 5MB 이하로 업로드 가능합니다."
            })
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        # django의 create_user() 메서드를 통해 비밀번호 자동 해싱
        user = User.objects.create_user(
            username = validated_data['username'],
            password = password,   # 이 필드를 create_user에서 해싱함
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', ''),
            email = validated_data.get('email'),
            phone = validated_data.get('phone', ''),
            # 이미지 필드는 없는 경우, 기본값 None 설정
            image = validated_data.get('image', None)
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("아이디와 비밀번호를 입력해주세요.")
        
        # 사용자 인증
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("아이디 또는 비밀번호가 유효하지 않습니다.")
        
        if not user.is_active:
            raise serializers.ValidationError("탈퇴한 회원입니다.")
        

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        data['tokens'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        # 인증된 사용자 반환
        data['user'] = user
        return data