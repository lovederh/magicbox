from dwebsocket.decorators import require_websocket

import json

from base import http_tools

# 画屏列表对应session集合(mac为key, session对象为value)
hp_sessions = {}  # mac, session, ip, app_version


# 画屏连接webSocket
@require_websocket
def ws_hp_in(request):
    try:
        mac = request.GET.get("mac")  # 设备mac地址
        app_version = request.GET.get("app_version")  # 设备使用的客户端版本
        if mac:
            ip = http_tools.get_client_ip(request)  # 客户端ip
            session_obj = {
                'mac': mac,
                'session': request.websocket,
                'ip': ip,
                'app_version': app_version if app_version else '',
            }
            # 首次连接
            hp_sessions.update({mac: session_obj})
        else:
            request.websocket.close()
            return

        while True:
            message = request.websocket.wait()  # 等待客户端(画屏)发送消息状态
            if message:
                message = str(message, encoding="utf-8")  # 接到一体机推送的消息
                opt_hp_msg(json.loads(message))
            else:
                pass  # 接收的是心跳
    except Exception as e:
        print('websocket except: ', e)
        # 出现异常, 则移除绑定
        for (k, v) in hp_sessions.items():
            if v['session'] == request.websocket:
                hp_sessions.pop(k)  # 执行移除
                break
        request.websocket.close()


# 服务端接收到画屏推送的消息后, 处理(实际中没有此场景)
def opt_hp_msg(msg_json):
    pass


# 发送消息
def send_socket_msg(session=None, msg=''):
    if session:
        session.send(msg)


# 给所有画屏推送消息
def send_to_hp_list(data):
    try:
        msg = json.dumps(data).encode('utf-8')  # 转换为字符串发送
        if len(hp_sessions):
            for (k, v) in hp_sessions.items():
                send_socket_msg(v['session'], msg)
    except Exception as e:
        print('websocket except: ', e)
    finally:
        pass


# 通过mac地址, 给指定的画屏推送消息
def send_one_hp(mac, data):
    v = hp_sessions[mac]
    if v:
        try:
            msg = json.dumps(data).encode('utf-8')  # 转换为字符串发送
            send_socket_msg(v['session'], msg)
        except Exception as e:
            print('websocket except: ', e)
        finally:
            pass
