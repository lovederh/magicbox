from django.apps import AppConfig
from .socket_server import SocketServer
import threading
# import os


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        print("base项目初始化完成了")
        # if os.environ.get('RUN_MAIN', None) == 'true':
        # 调用其他业务功能
        t = threading.Thread(target=self.start_server, args=())
        t.start()

    # socket通讯数据回调
    def callback(self, data):
        print("数据回调==》", data)

    # 启动socketserver端
    def start_server(self):
        server = SocketServer(self.callback)
        server.run()
