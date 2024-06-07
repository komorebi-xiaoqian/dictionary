# -*- coding: UTF-8 -*-
'''
@Project ：dictionary 
@File    ：dict_server_controller.py
@IDE     ：PyCharm 
@Author  ：komorebi
@Email   ：komorebi.so.67@gmail.com
@Date    ：2024/6/4 20:22
字典服务端逻辑处理，采用多进程
'''
from multiprocessing import Process
from dict_db import DictDB


class DictServerController(Process):
    db = DictDB()  # 得到数据库处理对象
    name = ''  # 存储当时用户登录的账号信息

    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self) -> None:
        # 　循环接收请求，分情况讨论
        while True:
            request = self.conn.recv(1024).decode()
            request = request.split("\t")
            if request[0] == "R":
                self._register(request[1], request[2])
            elif not request or request[0] == "E":
                print("客户端退出")
                break  # 客户端退出
            elif request[0] == "L":
                self._login(request[1], request[2])
            elif request[0] == "Q":
                self._query(request[1])
            elif request[0] == "H":
                self._history()

    def _register(self, name, password):
        """
        注册服务端，处理客户端的注册请求，并发送注册情况给客户端
        :param name: 用户账号
        :param password: 用户密码
        :return:
        """
        if self.db.register(name, password):
            self.conn.send(b"T")
        else:
            self.conn.send(b"F")

    def _login(self, name, password):
        """
        登录服务端，处理客户端的登录请求，并发送登录情况给客户端
        :param name: 用户账号
        :param password: 用户密码
        :return:
        """
        if self.db.login(name, password):
            self.name = name
            self.conn.send(b"T")
        else:
            self.conn.send(b"F")

    def _query(self, word):
        """
        查单词服务端，处理客户端的查单词请求，并响应查询到的结果
        :param word:  单词
        :return:
        """
        mean = self.db.query(word)
        if mean:
            self.db.insert_history(self.name, word)
            response = "T\t" + mean[0]
            self.conn.send(response.encode())
        else:
            self.conn.send(b"F")

    def _history(self):
        """
        查历史记录服务端，处理客户端的查历史记录请求，并响应查询到的结果
        :return:
        """
        # 临时存储((name,word,time),...)
        print(self.name)
        tmp = self.db.history(self.name)
        if tmp:
            response = "T\t"
            for one in tmp:
                response += "%s,%s,%s;" % one
            self.conn.send(response.encode())
        else:
            self.conn.send(b"F")
