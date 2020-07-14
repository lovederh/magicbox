from django.test import TestCase
from base import models
from base import db_tools
from sr.hardware import Hardware
from sr.magicbox import MagicBox
from .logs import Log
import logging


# Create your tests here.
class ModelTest(TestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        # 测试数据库连接方法初始化
        models.User.objects.create(username="1001001", userType="8001", realname="张三", dataid='1', org_label='信息中心')
        models.Config.objects.create(key="sch_ip", value="	http://192.168.1.250:8888", remark="服务器ip")
        # 测试设备连接初始化
        self.hardware = Hardware("1", "192.168.2.250", "pc")
        self.box = MagicBox()

    def test_find_dict_by_sql(self):
        # res = models.User.objects.get(username='1001001')
        res = db_tools.find_dict_by_sql("select realname from base_user where username = '1001001'")
        self.assertEqual(res.get('realname'), '张三')

    # 测试日志文件
    def test_log_record(self):
        log = Log("log", "this is test log content")
        self.logger.debug("test logging")
        log.record()
