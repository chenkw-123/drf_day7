from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken, obtain_jwt_token

from api import views

urlpatterns = [
    #只需注册路由，内部自己完成了用户校验与token生成
    url(r"login/", ObtainJSONWebToken.as_view()),  #基本的获取token的方式
    url(r"login_user/", obtain_jwt_token),  # 源码中定义了obtain_jwt_token=ObtainJSONWebToken.as_view()
    path("user/", views.UserAPIView.as_view()),
    path("check/", views.LoginAPIView.as_view()),
]
