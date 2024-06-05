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

    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self) -> None:
        while True:
            request = self.conn.recv(1024).decode()
            request = request.split("\t")
            if request[0] == "R":
                self._register(request[1], request[2])
            elif not request or request[0] == "E":
                print("客户端退出")
                break  # 客户端退出

    def _register(self, name, password):
        if self.db.register(name, password):
            self.conn.send(b"T")
        else:
            self.conn.send(b"F")
