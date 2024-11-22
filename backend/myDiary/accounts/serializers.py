from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
import logging
from django.core.files.storage import default_storage

# 순환 참조를 막기 위해 사용함 (완전히 이해는 안됨)
# AUTH_USER_MODEL에 설정된 CustomUser 가져옴
User = get_user_model()

class UserRegisterSerializer(RegisterSerializer):
    # 추가 필드
    """
        models.py에서 CustomUser에 phone과 image 필드가 정의되어 있어도,
        serializer 클래스에 phone과 image 필드를 명시적으로 정의해줘야 하는데
        이는 Serializer가 데이터 검증과 직렬화를 담당하기 떄문
    """
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)
    phone = serializers.CharField(required=True, max_length=30)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    def validate(self, data):
        # 비밀번호 확인 및 추가 검증 로직
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        
        # image = data.get('profile_image')
        # if image and image.size > 5 * 1024 * 1024: 
        #     raise serializers.ValidationError({
        #         "image": "이미지 파일은 5MB 이하로 업로드 가능합니다."
        #     })
        
        """
        부모 클래스의 validate 메서드 호출 결과를 반환
        (validate 메서드가 부모 클래스에서 정의한 기본 검증 로직을 유지하면서 추가적인 검증 로직을 더할 때 사용)
        따라서 부모 클래스가 검증된 데이터를 반환하게 됨
        """
        return super().validate(data)  
        

    def save(self, request):
        user = super().save(request)
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.phone = self.validated_data.get('phone', '')
        user.profile_image = self.validated_data.get('profile_image', None)
        user.save()
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
    

logger = logging.getLogger(__name__)

class CustomUserUpdateSerializer(UserDetailsSerializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        from .models import CustomUser
        model = CustomUser
        fields = ['username', 'email', 'phone', 'first_name', 'last_name', 'profile_image']
        read_only_fields = ('username',)

    def update(self, instance, validated_data):
        logger.info(f"Updating user with data: {validated_data}")
        
        # profile_image 처리
        if 'profile_image' in validated_data:
            # 기존 이미지가 있다면 삭제
            if instance.profile_image:
                default_storage.delete(instance.profile_image.path)
            instance.profile_image = validated_data.pop('profile_image')
            
        # email 처리
        if 'email' in validated_data:
            instance.email = validated_data.pop('email')
            
        # phone 처리
        if 'phone' in validated_data:
            instance.phone = validated_data.pop('phone')
            
        # 나머지 필드들 처리
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()                 # DB update 실행
        logger.info(f"Updated user instance: {instance.__dict__}")
        return instance
        
    def to_representation(self, instance):
        """사용자 정보를 응답할 때 이미지 URL 처리"""
        ret = super().to_representation(instance)
        if instance.profile_image:
            ret['profile_image'] = self.context['request'].build_absolute_uri(instance.profile_image.url)
        return ret