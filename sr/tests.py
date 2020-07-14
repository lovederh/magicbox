# from django.test import TestCase
from django.test import TestCase
from sr.hardware import Hardware
from sr.magicbox import MagicBox
import logging


# Create your tests here.
class ModelTest(TestCase):
    logger = logging.getLogger(__name__)

    def setUp(self):
        # 测试设备连接初始化
        self.hardware = Hardware("1", "192.168.2.250", "pc")
        self.box = MagicBox()

    # 测试设备连接方法
    def test_hardware_get_mac(self):
        # 获取设备列表
        self.box.get_device_list()
        box_hardware = self.box.hardwares
        # 获取列表中第一个设备对象
        for item in box_hardware:
            mac = box_hardware[item].get_mac()
            self.logger.debug(mac)
        # self.assertEqual(mac, "EC:41:18:2C:92:AF")
