#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
基础配置
"""
# 学校访问地址 - 配置key
SCH_IP_CONF_KEY = 'sch_ip'
# 盒子程序对外开放的端口号
MH_PORT_CONF_KEY = 'mh_port'

"""
终端设备管理
"""
# 终端设备类型: 画屏
TERMINAL_TYPE_PS = 'ps'  # painting screen
# 终端设备类型: 一体机
TERMINAL_TYPE_YTJ = 'ytj'

"""
智慧课堂
"""
# 智慧课堂 - 课堂状态: 未开始(新建)
KT_STATUS_NEW = '52006001'
# 智慧课堂 - 课堂状态: 进行中
KT_STATUS_START = '52006001'
# 智慧课堂 - 课堂状态: 已完成
KT_STATUS_END = '52006001'

# 资源状态: 未发布
SOURCE_STATUS_NOT = "52007001"
# 资源状态: 已发布
SOURCE_STATUS_OK = "52007002"

# 评价指标类型: 教师(被评价)
QUOTA_TYPE_TEACHER = "tch"
# 评价指标类型: 学生(被评价)
QUOTA_TYPE_STUDENT = "stu"

# 互动题目状态: 未开始
QUES_STATUS_NEW = "未开始"
# 互动题目状态: 进行中
QUES_STATUS_START = "进行中"
# 互动题目状态: 已结束
QUES_STATUS_END = "已结束"

# 互动题目评价方式: 对错
QUES_EVALUATE_YN = "52001001"
# 互动题目评价方式: 评级(5星)
QUES_EVALUATE_STAR = "52001002"

# 举手
ACT_TYPE_HAND_UP = "52003001"
# 抢答
ACT_TYPE_RUSH_FIRST = "52003002"
# 随机回答
ACT_TYPE_RANDOM = "52003003"
# 投票
ACT_TYPE_VOTE_ANSWER = "52003004"

# 评价: 最大分数
QUOTA_MAX_SCORE = 5
# 评价: 最多的评价项个数
QUOTA_ITEM_MAX_NUM = 10

# 测验题目添加场景: PC端(默认)
TEST_QUES_PC_OPT = "pc"
# 测验题目添加场景: app端
TEST_QUES_APP_OPT = "app"

# 题目类型: 单选
QUES_TYPE_RADIO = "24004001"
# 题目类型: 多选
QUES_TYPE_MULTIPLE = "24004002"
# 题目类型: 判断
QUES_TYPE_JUDGE = "24004003"
# 题目类型: 简答
QUES_TYPE_SHORT_ANSWER = "24004005"

ZHKT_OPT_START_QD = "startQd"  # 一体机 - 开始签到
ZHKT_OPT_TO_WAIT = "toWait"  # 一体机 - 反馈给学生等待状态(结束签到 / 互动)
ZHKT_OPT_LEAVE = "leave"  # 一体机反馈: 学生离开 / 画屏下课, 使其主动断开socket释放资源
ZHKT_OPT_STU_QIAN_DAO = "qianDao"  # 学生小程序 - 参与签到
ZHKT_OPT_STU_HAND_UP = "handUp"  # 学生小程序 - 执行举手
ZHKT_OPT_STU_VOTE_ANSWER = "voteAnswer"  # 学生小程序 - 投票或作答
ZHKT_OPT_START_ACT = "startAct"  # 一体机 - 开始一个互动
ZHKT_OPT_VOTE_RESULT = "voteResult"  # 学校服务 - 推送投票结果
ZHKT_OPT_WAIT_RUSH = "waitRush"  # 等待抢答学生
ZHKT_OPT_KT_START = "ktStart"  # 画屏 - 进入开始课堂模式
ZHKT_OPT_TEST_START = "testStart"  # 进入测验
ZHKT_OPT_TEST_END = "testEnd"  # 测验结束(小程序端使用)
ZHKT_OPT_RUSH_BEGIN = "rushBegin"  # 画屏进入3秒等待(开始抢答)
ZHKT_OPT_VOTE_SHORT = "voteShort"  # 临时投票
