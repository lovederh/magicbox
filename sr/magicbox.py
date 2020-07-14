#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from openwrt_luci_rpc import OpenWrtRpc
from sr.hardware import Hardware
from base.logs import Log
from base import http_tools


# 智慧魔盒对像
class MagicBox():
    hardwares = {}

    def __init__(self):
        self._IP = '192.168.2.1'
        self._USER = 'root'
        self._PWD = 'root'

    def get_device_list(self):
        try:
            # 建立和路由器的连接
            router = OpenWrtRpc(self._IP, self._USER, self._PWD)
        except Exception:
            # 连接失败 记录日志
            Log("magicbox", "魔盒连接失败，请检查ip %s 用户 %s 密码 %s" % (self._IP, self._USER, self._PWD)).record()
        else:
            result = router.get_all_connected_devices(only_reachable=True)
            for device in result:
                print("device >> ", device)
                mac = device.mac
                ip = device.ip
                hostname = device.hostname
                h = Hardware(mac, ip, hostname)
                self.hardwares[mac] = h
            # 保存设备到hardware表中
            # hardware_view.saveBatch(self.hardwares)

    # 调用openwrt_api，获取认证token
    # 测试 curl -i -X POST -d '{"method":"admin_login","params":["root"]}' http://192.168.2.1/cgi-bin/luci/api/auth
    # 返回值 {"id":"","result":{"token":"bd946bd87ff467ca9ca0663b4058f114"},"error":null}
    def call_openwrt_api_auth(self):
        rsp = http_tools.do_post(self._iP, "/cgi-bin/luci/api/auth", json_data={"method": "admin_login", "params": ["root"]})
        self._token = rsp.result.token

    # 获取dhcp在线设备列表
    # curl -i -X POST -d '{"method":"get_dhcp_leases"}' http://192.168.2.1/cgi-bin/luci/api/net?auth=bd946bd87ff467ca9ca0663b4058f114
    # 返回值 {"id":"","result":[{"expires":-27592,"macaddr":"48:d7:05:b7:a7:b5","ipaddr":"192.168.8.221","hostname":"appledeAir"}],"error":null}
    def get_online_hardware_list(self):
        # 如何_token不存在，调用认证
        if not self._token:
            self.call_openwrt_api_auth()
        # 判断是否已经获取_token，如果获取调用方法，如果未获取反回失败信息
        if self._token:
            rsp = http_tools.do_post(self._iP, "/cgi-bin/luci/api/net?auth="+self._token, json_data={"method": "admin_login", "params": ["root"]})
            print(rsp)
            devices = rsp.result
            if devices:
                for v in devices:
                    self.hardwares[v['mac']] = v
