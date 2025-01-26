from django.shortcuts import render
from django.views import View


# Create your views here.


class OrderSettlementView(View):
    """结算订单"""
    @staticmethod
    def get(request):
        return render(request, "place_order.html")