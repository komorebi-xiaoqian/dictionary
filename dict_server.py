# -*- coding: UTF-8 -*-
'''
@Project ：dictionary 
@File    ：dict_server.py
@IDE     ：PyCharm 
@Author  ：komorebi
@Email   ：komorebi.so.67@gmail.com
@Date    ：2024/6/4 20:01

在线字典服务端
'''

from socket import *
from dict_server_controller import *


class DictServer:
    """
    字典网络服务类
    """

    def __init__(self, host='', port=0):
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.tcp = self._create_socket()
        self.db = DictDB()

    def start(self):
        """
        网络服务启动，开始监听端口、连接服务端
        :return:
        """
        self.tcp.listen(5)
        print("Listen the port %d" % self.port)
        while True:
            conn, addr = self.tcp.accept()
            print("Content From", conn)
            controller = DictServerController(conn)
            controller.start()

    def _create_socket(self):
        """
        创建TCP套接字
        :return:
        """
        tcp = socket()
        tcp.bind(self.address)
        return tcp


# ----------------服务端启动入口---------------- #

if __name__ == '__main__':
    dict = DictServer(host='0.0.0.0', port=8888)
    dict.start()
