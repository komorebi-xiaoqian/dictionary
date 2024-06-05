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
                if self.controller.login(name,password):
                    print("登陆成功")
                    self. _menu_two()
                else:
                    print("登录失败")
            elif cmd == "2":
                name = input("请输入昵称:")
                password = input("请输入密码:")
                if self.controller.register(name, password):
                    print("注册成功")
                else:
                    print("注册失败")
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
                pass
            elif cmd == "2":
                pass
            elif cmd == "3":
                pass
            else:
                print("请输入正确的选项！")

    def main(self):
        self._menu_one()


# ----------------客户端启动入口---------------- #

if __name__ == '__main__':
    dict = DictView()
    dict.main()
