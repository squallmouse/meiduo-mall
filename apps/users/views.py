from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, HttpResponse
from django.views import View


# Create your views here.


class Register(View):
    """用户注册"""

    def get(self, request):
        """返回渲染后的注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """实现用户注册"""
        dict = request.POST
        userName = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        allow = dict.get('allow')

        if not all([userName, password, password2, mobile, allow]):
            return HttpResponseForbidden('缺少必传参数')

        return JsonResponse({'code': 0})
