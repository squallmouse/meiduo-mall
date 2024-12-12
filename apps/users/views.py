from django.shortcuts import render
from django.views import View

# Create your views here.




class Register(View):
    """用户注册"""
    def get(self, request):
        """返回渲染后的注册页面"""
        return render(request, 'register.html')



