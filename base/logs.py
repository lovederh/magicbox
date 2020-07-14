#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
将关键日志上传到上传系统服务器
方便追踪问题
"""
from base import db_tools, http_tools
from .common_tools import now, get_mac_address
from base.appview import config_view
from base.constant import SCH_IP_CONF_KEY


class Log():
    def __init__(self, module, content):
        self.module = module
        self.content = content
        self.ip = http_tools.get_host_ip()
        self.mac = get_mac_address()

    def record(self, create_time=now()):
        # 获取服务器ip地址
        sch_url = config_view.init_val_by_key(SCH_IP_CONF_KEY)
        try:
            # 调用上位系统日志模块接口，将日志内容上传
            rsp = http_tools.do_post(sch_url, "/api/magicbox/saveLog", json_data={"module": self.module, "content": self.content, "create_time": create_time, "mac": self.mac})
            if rsp.get("code") == 200:
                pass
            else:
                # 如果上位系统连接不上，那么就将日志内容存储在本地日志表，在合适的时机在上传
                db_tools.save_dict_to_db("base_log", {"module": self.module, "content": self.content, "create_time": create_time})
        except Exception as ex:
            print("日志服务调用失败:" + str(ex))
