# -*- coding: UTF-8 -*-
# @创建时间: 2025/3/6 17:14   -- yh 
# @文件名:      serializers.py


# apps/meiduo_admin/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
# from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView

# 创建自定义的 TokenObtainPairSerializer，去掉 refresh 令牌，并返回你自定义的结构。
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        return {
            "token": str(refresh.access_token),  # 直接返回 access 令牌
            "id"   : self.user.id,
            "username" : self.user.username,
        }

# 移除 refresh 令牌（可选） 如果你不需要 refresh 令牌，可以在序列化器中禁用它：
class CustomTokenObtainSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token.access_token  # 直接返回 access 令牌，不包含 refresh

# 移除 refresh 令牌（可选） 如果你不需要 refresh 令牌，可以在序列化器中禁用它：
class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer

