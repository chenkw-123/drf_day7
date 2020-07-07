#自定义过滤器
from django_filters.rest_framework import FilterSet

from api.models import Car


class LimitFilter:

    def filter_queryset(self,request,queryset,view):
        limit = request.query_params.get("limit")
        # print(limit)
        if limit:
            limit = int(limit)
            return queryset[:limit]

        return queryset


# django-filter过滤器类
class CarFilterSet(FilterSet):
    from django_filters import filters

    min_price = filters.NumberFilter(field_name="price",lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price",lookup_expr="lte")

    class Meta:
        model = Car
        #根据品牌筛选数据  (精确查询)
        fields = ["brand","min_price", "max_price","price"]