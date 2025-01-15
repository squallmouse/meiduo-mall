# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/14 23:09   -- yh 
# @文件名:      utils.py
from apps.goods.models import GoodsChannel


def get_categories():
    categories = {}

    #  获取所有的商品频道 所有的频道都对应着一级商品类别
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')

    for channel in channels:
        # 获取当前频道所在的组
        goodsGroupID = channel.group_id
        if goodsGroupID not in categories:
            categories[goodsGroupID] = {"channels": [], "sub_cats": []}
        cat1 = channel.category
        # {"id":1, "name":"手机", "url":"http://shouji.jd.com/"},
        categories[goodsGroupID]["channels"].append({
            "id"  : cat1.id,
            "name": cat1.name,
            "url" : channel.url
        })

        cat2s = cat1.subs.all()
        for cat2 in cat2s:
            cat2.sub_cats = []
            cat3s = cat2.subs.all()
            for cat3 in cat3s:
                cat2.sub_cats.append(cat3)
            categories[goodsGroupID]["sub_cats"].append(cat2)

    return categories