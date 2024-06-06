# -*- coding: UTF-8 -*-
'''
@Project ：dictionary 
@File    ：dict_client.py
@IDE     ：PyCharm 
@Author  ：komorebi
@Email   ：komorebi.so.67@gmail.com
@Date    ：2024/6/4 20:13
字典客户端View层
'''
import sys
from socket import *
from dict_client_controller import DictClientController
class Sock:
    def __init__(self, host="127.0.0.1", port=8888):
        self.__host = host
        self.__port = port
        self.address = (self.__host, self.__port)
        self.sock = self.__create_sock()

    def __create_sock(self):
        sock = socket()
        sock.connect(self.address)
        return sock
class  DictClientController:
    def __init__(self):
        self.__sock = Sock().sock

    def login(self, name, passwd):
        msg = f"L\t{name}\t{passwd}"
        self.__sock.send(msg.encode())
        data = self.__sock.recv(1024)
        if data == b"T":
            return True
        else:
            return False

    def register(self, name, passwd):
        if " " in name or " " in passwd:
            print("名字和密码里不能有空格")
        msg = f"R\t{name}\t{passwd}"
        self.__sock.send(msg.encode())
        data = self.__sock.recv(10)
        if data == b"T":
            return True
        else:
            return False

    def select(self):
        while True:
            word = input("Word:")
            if word == "##":
                break  
            request = "Q\t" + word
            self.__sock.send(request.encode())
            response = self.__sock.recv(1024).decode()
            tmp = response.split('\t', 1)
            if tmp[0] == 'T':
                print("%s : %s\n" % (word, tmp[1]))
            else:
                print("%s : Not Found!\n" % word)

    def history(self):
        self.__sock.send(b"H")
        response = self.__sock.recv(1024 * 10).decode()
        tmp = response.split("\t")
        if tmp[0] == 'T':
            for row in tmp[1].split(';'):
                print(row)
        else:
            print("您当前还没有查询记录")

    def exit(self):
        self.__sock.send(b"E")
        self.__sock.close()
        sys.exit()

class DictView:
    def __init__(self):
        self.controller = DictClientController()

    def _menu_one(self):
        while True:
            print("""
            -----------欢迎使用本在线词典---------------
            1.登录            2.注册            3.退出
            ----------------------------------------
            """)
            cmd = input("请输入选项:")
            if cmd == "1":
                name = input("请输入昵称:")
                password = input("请输入密码:")
                if self.controller.login(name, password):
                    print("登录成功")
                    self._menu_two()
                else:
                    print("登录失败,账号或密码输入错误")
            elif cmd == "2":
                name = input("请输入昵称:")
                password = input("请输入密码:")
                if self.controller.register(name, password):
                    print("注册成功")
                else:
                    print("注册失败,账号已存在或密码需为大于6位数字字母下划线")
            elif cmd == "3":
                self.controller.exit()
                sys.exit("感谢使用本在线字典")
            else:
                print("请输入正确的选项！")

    def _menu_two(self):
        while True:
            print("""
            -----------欢迎使用本在线词典---------------
            1.查单词          2.历史记录          3.注销
            ----------------------------------------
            """)
            cmd = input("请输入选项:")
            if cmd == "1":
                while True:
                    word = input("请输入要查询的单词:")
                    if not word or word == "##":
                        break
                    response = self.controller.query(word)
                    if response:
                        print(response)
                    else:
                        print("没有找到该单词！\n")
            elif cmd == "2":
                response = self.controller.history()
                if response:
                    print(response)
                else:
                    print("您还没查找记录哦！\n")
            elif cmd == "3":
                break
            else:
                print("请输入正确的选项！")

    def main(self):
        self._menu_one()


# ----------------客户端启动入口---------------- #

if __name__ == '__main__':
    dict = DictView()
    dict.main()
