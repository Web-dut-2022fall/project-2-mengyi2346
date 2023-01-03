from calendar import c
from django.contrib.auth.models import AbstractUser
from django.db import models

"""
用户模型
"""
class User(AbstractUser):
    pass
    # #用户名
    # userName = models.CharField('用户名', primary_key=True, max_length=64)
    # #邮箱
    # userEmail =models.CharField('邮箱', max_length=64)
    # #密码
    # userPassword =models.CharField('密码', max_length=64)

class auctions(models.Model):
    title=models.CharField('商品名称', max_length=64)
    description=models.CharField('描述',  max_length=64)
    startbid = models.CharField('起始价格', max_length=64)
    category= models.CharField('类别', max_length=64)
    image=models.CharField('图片url',max_length=256)
    createTime = models.CharField('创建时间',max_length=128)
    createby = models.CharField('创建者',max_length=128)
    status = models.CharField('商品状态',max_length=128)

class bids(models.Model):
    title=models.CharField('商品名称', max_length=64)
    nowbid = models.CharField('现在价格', max_length=64)
    createby = models.CharField('竞拍发起者', max_length=64)


class wathclist(models.Model):
    user =  models.CharField('用户名称',max_length=64)
    title=models.CharField('商品名称', max_length=64)
    description=models.CharField('描述',  max_length=64)
    startbid = models.CharField('起始价格', max_length=64)
    category= models.CharField('类别', max_length=64)
    image=models.CharField('图片url',max_length=256)
    createTime = models.CharField('创建时间',max_length=128)
    
class comments(models.Model):
    title = models.CharField('商品名称', max_length=64)
    name = models.CharField('用户',max_length=128)
    content = models.CharField('用户',max_length=512)