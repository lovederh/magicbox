#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
所有终端连接, 通过此类来注册ip，mac, 名称
"""


class Hardware():

    def __init__(self, mac, ip, hostname):
        super().__init__()
        # 设备的mac地址
        self.mac = mac
        # 设备的ip地址
        self.ip = ip
        # 设备名称
        self.hostname = hostname

    # 获取设备mac地址
    def get_mac(self):
        return self.mac

    # 获取设备ip
    def get_ip(self):
        return self.ip

    # 获取设备名称
    def get_hostname(self):
        return self.hostname

    # 绑定设备和用户
    def bind(self, mac, username):
        # 用户绑定设备
        self.user_hardware = {mac, username}

    # 解绑用户和设备
    def unbind(self):
        self.user_hardware = {}

    # 获取设备绑定用户
    def get_user_hardware(self):
        return self.user_hardware
