import re

from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.settings import api_settings

from api.models import User, Car

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserModelSerializer(ModelSerializer):
    # 自定义反序列化字段 代表这个字段只参与反序列化  且不会要求这个字段必须与model类映射
    user = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["user", "password", "username", "phone", "email"]

        extra_kwargs = {
            # 代表这些字段只参与序列化
            "username": {
                "read_only": True,
            },
            "phone": {
                "read_only": True,
            },
            "email": {
                "read_only": True,
            }

        }

    def validate_user(self, value):
        # print(value)
        return value

    def validate_password(self, value):
        # print(value)
        return value

    def validate(self, attrs):
        user = attrs.get("user")
        password = attrs.get("password")
        print(user, password)
        # 对于各种登录方式做处理  账号  邮箱  手机号
        if re.match(r'.+@.+', user):
            user_obj = User.objects.filter(email=user).first()
        elif re.match(r'1[3-9][0-9]{9}', user):
            user_obj = User.objects.filter(phone=user).first()
        else:
            user_obj = User.objects.filter(username=user).first()

        # 判断用户是否存在 且用户密码是否正确
        if user_obj and user_obj.check_password(password):
            # 签发token
            payload = jwt_payload_handler(user_obj)  # 生成载荷信息
            token = jwt_encode_handler(payload)  # 生成token
            # print(payload,token)
            self.token = token
            self.obj = user_obj

        return attrs


class CarModelSerializer(ModelSerializer):
    class Meta:
        model = Car
        # 最好采用自己指定的字段，因为可以添加自定义序列化或者反序列化字段

        fields = ("name", "price", "brand")
