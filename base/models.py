from django.db import models


# base_user表
class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)  # 主键用户Id
    username = models.CharField(max_length=50)  # 用户账号
    userType = models.CharField(max_length=20, null=True)  # 用户类型
    realname = models.CharField(max_length=50, null=True)  # 用户姓名
    dataid = models.CharField(max_length=100, null=True)  # 数据来源Id
    org_label = models.CharField(max_length=200, null=True)  # 部门名称


# base_config表
class Config(models.Model):
    id = models.BigAutoField(primary_key=True)  # 主键Id
    key = models.CharField(max_length=50, null=True)  # key
    value = models.CharField(max_length=1000, null=True)  # value
    remark = models.CharField(max_length=200, null=True)  # 备注


# base_files表
class Files(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    file_name = models.CharField(max_length=50, null=True)  # 文件存储名
    file_real_name = models.CharField(max_length=200, null=True)  # 文件真实名
    file_size = models.CharField(max_length=20, null=True)  # 文件大小
    file_path = models.CharField(max_length=100, null=True)  # 文件相对路径
    ext_file_name = models.CharField(max_length=100, null=True)  # 相关扩展文件名
    file_type = models.CharField(max_length=10, null=True)  # 文件类型
    main_id = models.CharField(max_length=50, null=True)  # 关于课堂id


# base_log表
class Log(models.Model):
    id = models.UUIDField(primary_key=True)  # 主键uuid
    module = models.CharField(max_length=64)  # 模块
    content = models.CharField(max_length=1024, null=True)  # 模块内容
    create_time = models.CharField(max_length=64, null=True)  # 创建时间


# base_terminal_equ表(终端设备绑定表)
class Terminal_Equ(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # 主键Id
    mac = models.CharField(max_length=50, null=True)  # mac地址
    equ_name = models.CharField(max_length=100, null=True)  # 终端设备名称
    alias_name = models.CharField(max_length=50, null=True)  # 别名
    equ_type = models.CharField(max_length=10, null=True)  # 终端类型(一体机/画屏)
    app_version = models.CharField(max_length=20, null=True)  # 所装软件版本
    create_time = models.CharField(max_length=20, null=True)  # 绑定时间
    last_online = models.CharField(max_length=20, null=True)  # 最后上线时间
    close_time = models.CharField(max_length=20, null=True)  # 定时关机时间(设置项)
    weekup_time = models.CharField(max_length=20, null=True)  # 定时开机时间(设置项)
    ps = models.CharField(max_length=500, null=True)  # 备注
