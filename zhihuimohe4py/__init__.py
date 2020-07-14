#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql
# 增加此配置，解决pymysql版本兼空问题
pymysql.version_info = (1, 3, 13, "final", 0)
# 使用pymysql作为mysql引擎
pymysql.install_as_MySQLdb()
