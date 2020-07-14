from django.db import models


# 连接到此设备的设备列表
class Hardware(models.Model):
    id = models.UUIDField(primary_key=True)  # 主键uuid
    # 设备名称
    hostname = models.CharField(max_length=128, null=True)
    # 设备命名
    alias_name = models.CharField(max_length=128, null=True)
    # 设备ip
    ip = models.CharField(max_length=32, null=True)
    # 设备mac
    mac = models.CharField(max_length=64, null=True)
    # 常用人用户ID
    username = models.CharField(max_length=64, null=True)
    # 创建时间
    create_time = models.CharField(max_length=64, null=True)
    # 上线时间
    online_time = models.CharField(max_length=64, null=True)
    # 设备类型 画屏 学生端 老师端 一体机 网关飞比 网关zigbee 班牌
    hardware_type = models.CharField(max_length=64, null=True)
