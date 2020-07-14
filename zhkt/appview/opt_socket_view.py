# import json
# from dwebsocket.decorators import require_websocket
# from base import http_tools
# from zhkt.websocket_zhkt import socketObj, tempObjs


# 发送消息
def send_socket_msg(session=None, msg=''):
    if session:
        session.send(msg)


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
#         if len(stuSessions):
#             for session in stuSessions:
#                 send_socket_msg(session, msg)
#     except Exception:
#         pass
#     finally:
#         pass


def startOneAct(bean, answerLimit):
    pass
