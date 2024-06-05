# -*- coding: UTF-8 -*-
'''
@Project ：dictionary 
@File    ：dict_client_controller.py
@IDE     ：PyCharm 
@Author  ：komorebi
@Email   ：komorebi.so.67@gmail.com
@Date    ：2024/6/5 15:20
字典客户端Controller层
'''
from socket import *


class DictClientController:
    def __init__(self):
        self.tcp = self._create_socket()

    def _create_socket(self):
        """
        初始化网络服务
        :return: tcp 套接字类型
        """
        tcp = socket()
        tcp.connect(("127.0.0.1", 8888))  # 服务器地址
        return tcp

    def register(self, name, password):
        """
        注册模块
        :param name: 接收昵称
        :param password: 接受密码
        :return: True or False 布尔类型
        """
        request = f"R\t{name}\t{password}"
        self.tcp.send(request.encode())
        response = self.tcp.recv(1024).decode()
        if response == "T":
            return True
        else:
            return False

    def exit(self):
        """
        退出模块
        :return: True 布尔类型
        """
        self.tcp.send(b"E")
        self.tcp.close()
