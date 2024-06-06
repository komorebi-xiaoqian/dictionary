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
import re
from socket import *


class DictClientController:
    @staticmethod
    def _check(info):
        """
        正则匹配，判断注册的昵称和密码是否符合规范
        :param info:
        :return:
        """
        if re.findall(r"^\w{6,}$", info):
            return True
        return False

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
        if DictClientController._check(password):
            request = f"R\t{name}\t{password}"
            self.tcp.send(request.encode())
            response = self.tcp.recv(1024).decode()
            if response == "T":
                return True
        return False

    def exit(self):
        """
        退出模块
        :return: True 布尔类型
        """
        self.tcp.send(b"E")
        self.tcp.close()

    def login(self, name, password):
        """
        登录模块
        :param name: 接收昵称
        :param password: 接受密码
        :return: True or False 布尔类型
        """

        request = f"L\t{name}\t{password}"
        self.tcp.send(request.encode())
        response = self.tcp.recv(1024).decode()
        if response == "T":
            return True
        return False

    def query(self, word):
        request = f"Q\t{word}"
        self.tcp.send(request.encode())
        response = self.tcp.recv(1024).decode()
        response = response.split("\t")
        if response[0] == "T":
            return "%s : %s\n" % (word, response[1])
        return False

    def history(self):
        request = b"H"
        self.tcp.send(request)
        response = self.tcp.recv(1024).decode()
        response = response.split("\t", 1)
        if response[0] == "T":
            data = ''
            for row in response[1].split(";"):
                data += f"{row}\n"
            return data
        return False
