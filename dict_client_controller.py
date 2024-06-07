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
        if re.match("^[_0-9a-z]{6,16}$", info):
            return True
        return False

    def __init__(self, host="127.0.0.1", port=8888):
        self.__host = host
        self.__port = port
        self.address = (self.__host, self.__port)  # 服务器地址
        self.tcp = self._create_socket()

    def _create_socket(self):
        """
        初始化网络服务
        :return: tcp 套接字类型
        """
        tcp = socket()
        tcp.connect(self.address)
        return tcp

    def register(self, name, password):
        """
        注册模块
        :param name: 接收账号
        :param password: 接受密码
        :return: True or False 布尔类型
        """
        if DictClientController._check(password):
            request = f"R\t{name}\t{password}"
            self.tcp.send(request.encode())
            response = self.tcp.recv(1024).decode()
            if response == "T":
                return "注册成功"
            else:
                return "注册失败，当前账户已经存在"
        else:
            return "注册失败，密码需为大于6位数字字母下划线"

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
        :param name: 接收账号
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
        """
        查询单词模块，发送请求，有值，按照通信协议进行解析，通信协议为"T\tmean"
        :param word: 用户输入的单词，str类型
        :return: 查询结果 str类型，没有返回False
        """
        request = f"Q\t{word}"
        self.tcp.send(request.encode())
        response = self.tcp.recv(1024).decode()
        response = response.split("\t")
        if response[0] == "T":
            return "%s : %s\n" % (word, response[1])
        return False

    def history(self):
        """
        发送请求，查询历史记录，有值，按照通信协议进行解析，通信协议为"T\tname,word,time;..."
        :return: 查询结果 str类型，没有返回False
        """
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
