# -*- coding:utf-8 -*-
import socket
from time import sleep
from datetime import datetime
import threading


class SocketClient():
    client = None
    # 回调函数
    callback = None
    # 缓冲区大小
    _BUFFER_SIZE = 512

    def __init__(self, foo=None, ip="127.0.0.1", port=10086):
        self.callback = foo
        self.ip = ip
        self.port = port

    # 心跳包线程
    def heartBeat(self, conn):
        sum = 0   # 无回应次数
        while True:
            # 5分钟心跳一次
            sleep(300)
            if sum < 3:
                try:
                    hb = "hreatBeat"
                    conn.sendall(hb.encode())
                    sum = 0
                except socket.error:
                    sum = sum + 1
                    continue
            else:
                conn.close()
                break

    def process(self, tcpCliSock):
        #  创建心跳包线程
        #  须记住，创建新线程时 args参数如果只有一个的话一定要加个逗号！！
        thr = threading.Thread(target=self.heartBeat, args=(tcpCliSock, ))
        thr.start()
        while True:
            print("waiting receive msg from server... ")
            data = tcpCliSock.recv(self._BUFFER_SIZE)
            if data:
                print(data.decode())
            else:
                break
            # 收到数据后转发给业务处理层进行业务处理
            if self.callback:
                self.callback(data.decode())

    def run(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client.connect((self.ip, self.port))
        except socket.error as ex:
            print(ex)
        else:
            msg = str(datetime.now())[:19]
            print(msg)
            msg = msg.encode()
            self.client.sendall(msg)
            t = threading.Thread(target=self.process, args=(self.client, ))
            t.start()

    def sendMsg(self, msg):
        self.client.sendall(msg.encode())


# if __name__ == "__main__":
#     client = SocketClient()
#     client.run()
