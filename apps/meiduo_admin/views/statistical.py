# -*- coding: UTF-8 -*-
# @创建时间: 2025/3/6 14:36   -- yh 
# @文件名:      statistical.py


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from datetime import date
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.meiduo_admin.serializers.serializers import CustomTokenObtainPairSerializer
from apps.users.models import User


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserTotalCountView(APIView):
    # 指定管理员权限
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request):
        # 获取当前日期
        now_date = date.today()
        # 获取所有用户总数
        count = User.objects.all().count()
        return Response({
            'count': count,
            'date' : now_date
        })
