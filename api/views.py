import re

from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from api.filter import LimitFilter, CarFilterSet
from api.models import User, Car
from api.paginations import MPageNumberPagination, MLimitOffsetPagination, MCursorPagination
from api.serializers import UserModelSerializer, CarModelSerializer
from utils.response import APIResponse


from rest_framework.filters import SearchFilter,OrderingFilter

class UserAPIView(APIView):
    # 登录请求不需要认证，而别的请求需要认证token（携带token才可以）
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    # 必须先生成token，并且携带token才可以访问到
    def get(self, request, *args, **kwargs):  # 打印的password是加密后的
        return APIResponse(results={"username": request.user.username, "password": request.user.password})


class LoginAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # 账号为user，密码为password（通过前端传递）
        # user = request.data.get("user")
        # password = request.data.get("password")

        user_ser = UserModelSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)

        return APIResponse(data_message="成功", token=user_ser.token, results=UserModelSerializer(user_ser.obj).data)

    # 如果不自定义序列化器，则自己也可以写判断逻辑，只是效率比较低，难以维护
    def post_two(self, request, *args, **kwargs):
        user = request.data.get("user")
        password = request.data.get("password")

        # 对于各种登录方式做处理  账号  邮箱  手机号
        if re.match(r'.+@.+', user):
            user_obj = User.objects.filter(email=user).first()
        elif re.match(r'1[3-9][0-9]{9}', user):
            user_obj = User.objects.filter(phone=user).first()
        else:
            user_obj = User.objects.filter(username=user).first()

        # 判断用户名和密码是否正确
        if user_obj and user_obj.check_password(password):
            # 签发token
            payload = jwt_payload_handler(user_obj)  # 生成载荷信息
            token = jwt_encode_handler(payload)  # 生成token
            # print(payload,token)
            return APIResponse(results={"username": user_obj.username}, token=token)

        return APIResponse(data_message="程序出错，请重试！")


class CarListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer

    #这个参数是用来配置过滤的类的
    filter_backends = [SearchFilter,OrderingFilter,LimitFilter,DjangoFilterBackend]
    #指定搜索的条件，键名在postman必须为search，匹配列表里的条件（模糊查询）
    search_fields = ["name","price"]
    #指定排序的规则和条件
    #默认不写是升序，降序需将其变为  -price
    ordering = ["price"]

    #指定分页器
    # pagination_class = MPageNumberPagination
    # pagination_class = MLimitOffsetPagination
    # pagination_class = MCursorPagination

    # django-filter 查询   通过filter_class指定过滤器（精确查询）
    filter_class = CarFilterSet