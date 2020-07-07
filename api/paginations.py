from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import CursorPagination
from rest_framework.pagination import LimitOffsetPagination


#基础分页器



class MPageNumberPagination(PageNumberPagination):
    #指定每一页有多少数据
    page_size = 3
    #指定最多分多少页
    max_page_size = 7
    # 指定前端修改每页分页数量的 key
    page_size_query_param = "page_size"
    # 获取第几页的对象
    page_query_param = "page"


#偏移分页器

class MLimitOffsetPagination(LimitOffsetPagination):
    #默认获取的每一页的数量
    default_limit = 3
    # 指定前端修改每页数量的key
    limit_query_param = "limit"
    # 前端指定偏移的数量的key，下一页取值从所有对象中这个key的值的后一位开始取，取默认一页的数量
    offset_query_param = "offset"
    # 每页获取的最大数量,超过数量则以最大数量为准，默认的获取数量优先级也没有他高
    max_limit = 5


#游标分页器

class MCursorPagination(CursorPagination):
    #默认值
    cursor_query_param = "cursor"
    #默认一页分几个数据
    page_size = 3
    ordering = "-price"
    # 自定义一页几个数据
    page_size_query_param = "page_size"
    #最大
    max_page_size = 5

