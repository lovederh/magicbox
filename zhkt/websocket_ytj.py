import json
import time
from dwebsocket.decorators import require_websocket
from base import common_tools, http_tools
from zhkt.appview import opt_socket_view
from zhkt import zhkt_tools


# socket大对象
socketObj = {
    'mainId': '',  # 当前课堂Id
    'opt': '',  # 当前课堂操作
    'actQuesId': '',  # 当前互动题目Id
    'ytjSession': {'mac': '', 'session': None, 'ip': '', 'app_version': ''},  # 存储连接一体机的websocket
    'stuSessions': {},  # 学生id与对应的session对象(mac, session, ip, app_version)
}
# 课堂互动的临时对象
tempObjs = {
    'answerLimit': 1,  # 抢答时, 限制的抢答人数(默认为1)
    'qdStudentIds': set(),  # 已签到学生(使用set防止出现重复)
    'handStuList': [],  # 有效的举手学生(抢答时, 只存储1个)
    'quesAnlsObj': {},  # 投票选项统计对象(出现学生修改投票结果时, 执行重新查询, 否则正常按照选项累计)
}


# 一体机webSocket (一体机连接)
@require_websocket
def ws_ytj_in(request):
    try:
        mainId = request.GET.get("mainId")
        if mainId:
            # 首次连接
            mac = request.GET.get("mac")  # 设备mac地址
            app_version = request.GET.get("app_version")  # 设备使用的客户端版本
            ip = http_tools.get_client_ip(request)  # 客户端ip
            if socketObj['mainId'] != mainId:
                socketObj['opt'] = ''
                socketObj['actQuesId'] = ''
                socketObj['mainId'] = mainId
                socketObj['stuSessions'] = {}  # 清除已连入学生
            socketObj['ytjSession'] = {'mac': mac, 'session': request.websocket, 'ip': ip, 'app_version': app_version}

            # 判断当前课堂状态, 执行不同行为
            if 'startAct' == socketObj['opt']:  # 正在进行互动
                bean = zhkt_tools.act_ques_by_id(mainId, socketObj['actQuesId'])
                opt_socket_view.startOneAct(bean, tempObjs['answerLimit'])
            elif 'testStart' == socketObj['opt']:  # 开始测验
                print('----------------- 唤醒学生 开始测验...')
        else:
            request.websocket.close()
            return

        while True:
            message = request.websocket.wait()
            if message:
                message = str(message, encoding="utf-8")  # 接到一体机推送的消息
                opt_ytj_msg(json.loads(message))
            else:
                pass  # 接收的是心跳
    except Exception as e:
        print('websocket except: ', e)
        request.websocket.close()
        socketObj['ytjSession'] = {'mac': '', 'session': None, 'ip': '', 'app_version': ''}  # 清除当前socket信息


# 服务端接收到一体机推送的消息后, 处理(实际中一体机都是发送请求, 即没有此场景)
def opt_ytj_msg(msg_json):
    pass


# # 发送消息
# def send_socket_msg(session=None, msg=''):
#     if session:
#         session.send(msg)
#
#
# # 服务端发送消息 (推送给一体机)
# def send2ytj(data):
#     try:
#         global ytj_session
#         if ytj_session:
#             msg = json.dumps(data).encode('utf-8')
#             send_socket_msg(ytj_session, msg)
#     except Exception:
#         pass
#     finally:
#         pass
#
#
# def send2stu_list(data):
#     try:
#         msg = json.dumps(data).encode('utf-8')
#         if len(stu_sessions):
#             for session in stu_sessions:
#                 send_socket_msg(session, msg)
#     except Exception:
#         pass
#     finally:
#         pass

