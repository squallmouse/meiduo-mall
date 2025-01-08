from django import http
from django.core.cache import cache
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
            province_list = cache.get("province_list")
            if not province_list:
                try:
                    # 查找出省份数据
                    provinces = Area.objects.filter(parent=None)
                    cache.set("province_list",provinces, 3600)
                except Area.DoesNotExist:
                    return http.JsonResponse({"code": RETCODE.NODATAERR, "errmsg": "省级数据查找错误"})
                else:
                    province_list = []
                    # for -- in  批量循环装入数据
                    for province in provinces:
                        item = {"name": province.name, "id": province.id, }
                        province_list.append(item)
                    cache.set("province_list", province_list, 3600)
            # 返回数据
            return http.JsonResponse({"code": 0, "errmsg": "ok", "province_list": province_list})
        else:
            # 查找 市 或 地区
            # 由area_id 查找 省或市
            sub_data = cache.get("sub_area_" + area_id)
            if not sub_data:
                try:
                    area = Area.objects.get(id=area_id)
                    areas = area.subs.all()

                except Area.DoesNotExist:
                    return http.JsonResponse({"code": RETCODE.NODATAERR, "errmsg": "市区数据查找错误"})
                else:
                    subs = []
                    for city in areas:
                        item = {"name": city.name, "id": city.id, }
                        subs.append(item)
                    sub_data = {
                        "id"  : area.id,
                        "name": area.name,
                        "subs": subs
                    }

                    cache.set("sub_area_" + area_id, sub_data, 3600)

            return http.JsonResponse({"code": RETCODE.OK, "errmsg": "ok", "sub_data": sub_data})


