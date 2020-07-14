# -*- coding:utf-8 -*-
import socket
from time import sleep
import select
import threading


class SocketServer():
    # 回调函数
    callback = None
    # 缓冲区大小
    _BUFFER_SIZE = 512

    # foo 为回调函数
    def __init__(self, foo=None, ip="0.0.0.0", port=10086, heart_time=1):
        self.callback = foo
        self.ip = ip
        self.port = port

    # 心跳包线程
    def heartBeat(self, conn):
        sum = 0   # 无回应次数
        while True:
            # 10分钟心跳一次
            sleep(600)
            if sum < 3:
                try:
                    hb = "heartBeat"
                    conn.sendall(hb.encode())
                    sum = 0
                except socket.error:
                    sum = sum + 1
                    continue
            else:
                conn.close()
                break

    def process(self, tcpCliSock, addr):
        #  创建心跳包线程
        #  须记住，创建新线程时 args参数如果只有一个的话一定要加个逗号！！
        thr = threading.Thread(target=self.heartBeat, args=(tcpCliSock,))
        thr.start()
        print("connect from " + str(addr))
        while True:
            print("waiting receive msg from client...")
            data_bytes = tcpCliSock.recv(self._BUFFER_SIZE)
            if data_bytes:
                print(data_bytes.decode())
            else:
                break
            # 收到数据后转发给业务处理层进行处理
            if self.callback:
                self.callback(data_bytes.decode())

    def run(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.ip, self.port))
            server.listen(5)
        except socket.error as ex:
            print(ex)
        else:
            while True:
                r, w, e = select.select([server, ], [], [], 1)
                # enumerate()分别列举出list r中的序号和内容
                for i, server in enumerate(r):
                    conn, addr = server.accept()
                    t = threading.Thread(target=self.process, args=(conn, addr))
                    t.start()

    def sendMsg(self, msg):
        self.client.sendall(msg.encode())


# if __name__ == "__main__":
#     server = SocketServer()
#     server.run()
