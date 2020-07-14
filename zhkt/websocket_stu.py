import json
import time
from dwebsocket.decorators import require_websocket
from base import common_tools, http_tools
from zhkt.appview import opt_socket_view
from zhkt import zhkt_tools
from zhkt.websocket_ytj import socketObj


# 一体机webSocket (学生端连接)
@require_websocket
def ws_ytj_stu_in(request):
    try:
        mainId = request.GET.get("mainId")
        studentId = request.GET.get("studentId")
        if mainId and studentId:
            if mainId != socketObj['mainId']:
                request.websocket.close()  # 进入的是错误的课堂, 直接返回
            # 首次连接(学生session集合中, 学生id为key, session对象为value)
            mac = request.GET.get("mac")  # 设备mac地址
            app_version = request.GET.get("app_version")  # 设备使用的客户端版本
            ip = http_tools.get_client_ip(request)  # 客户端ip
            socketObj['stuSessions'].update({studentId: {'mac': mac, 'session': request.websocket, 'ip': ip, 'app_version': app_version}})

            # 判断当前课堂状态, 执行不同行为
            if 'startAct' == socketObj['opt']:  # 正在进行互动
                # 唤醒学生
                print('--------新加入学生 直接参与互动...')

            elif 'testStart' == socketObj['opt']:  # 开始测验
                # 处于开始签到
                print('----------新加入学生 直接# 开始测验...')
        else:
            request.websocket.close()
            return

        while True:
            message = request.websocket.wait()
            if message:
                # 接到学生推送的消息
                message = str(message, encoding="utf-8")  # 接到一体机推送的消息
                opt_stu_msg(json.loads(message))
            else:
                pass  # 接收的是心跳
    except Exception as e:
        print('websocket except: ', e)
        # 出现异常, 则移除绑定
        for (k, v) in socketObj['stuSessions'].items():
            if v['session'] == request.websocket:
                socketObj['stuSessions'].pop(k)  # 执行移除
                break
        request.websocket.close()


# 服务端接收到学生推送的消息后, 处理
def opt_stu_msg(msg_json):
    opt = msg_json['opt']
    mainId = msg_json['mainId']
    if "handUp" == opt:  # 学生举手 / 抢答举手
        createTimeStamp = int(round(time.time() * 1000))  # 举手对应的毫秒级时间戳
        # ZhktSchSocketHandler.studentHandUp(schoolCode, mainId, createTimeStamp, msgJSON);
    elif "voteAnswer" == opt:  # 投票
        createTime = common_tools.now()  # 学生操作的时间(投票时间)
        # ZhktSchSocketHandler.stuVoteAnswer(schoolCode, mainId, createTime, msgJSON);
