from django import http
from django.shortcuts import render
# from django.utils import http
from django.views import View

from apps.areas.models import Area
from meiduo.utils.response_code import RETCODE


# Create your views here.


class AreasView(View):
    """查询省市区"""

    @staticmethod
    def get(request):
        # 获取查询参数 area_id
        area_id = request.GET.get("area_id")
        # 如果没有area_id 参数, 查询省份数据
        if not area_id:
            try:
            # 查找出省份数据
                provinces = Area.objects.filter(parent=None)
            except Area.DoesNotExist:
                return http.JsonResponse({"code": RETCODE.NODATAERR, "errmsg": "没有数据"})
            else:
                province_list = []
                # for -- in  批量循环装入数据
                for province in provinces:
                    item = {
                        "name": province.name,
                        "id"  : province.id,
                    }
                    province_list.append(item)
            # 返回数据
            return http.JsonResponse({"code": 0, "errmsg": "ok", "province_list": province_list})
        else:
            # 查找 市 或 地区
            # 由area_id 查找 省或市
            try:
                area = Area.objects.get(id=area_id)
                areas = Area.objects.filter(parent=area)
            except Area.DoesNotExist:
                return http.JsonResponse({"code": RETCODE.NODATAERR, "errmsg": "没有数据"})
            else:
                subs = []
                for city in areas:
                    item = {
                        "name": city.name,
                        "id"  : city.id,
                    }
                    subs.append(item)
                sub_data = {
                    "id"  : area.id,
                    "name": area.name,
                    "subs": subs
                }
            return http.JsonResponse({"code": RETCODE.OK, "errmsg": "ok", "sub_data": sub_data})
            # if area.parent is None:
            #     #  area是省份,查找 市
            #     for city in areas:
            #         item = {
            #             "name": city.name,
            #             "id":city.id,
            #         }
            #         subs.append(item)
            # else:
            #     #  area是市,查找 区

        return http.JsonResponse({"code": 0, "errmsg": "ok", "province_list": []})
