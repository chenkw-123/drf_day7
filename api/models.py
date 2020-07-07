from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)

    class Meta:
        db_table = "api_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Car(models.Model):
    name = models.CharField(max_length=20,unique=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    brand = models.CharField(max_length=20,verbose_name="车标")

    class Meta:
        db_table = "car"
        verbose_name = "汽车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name