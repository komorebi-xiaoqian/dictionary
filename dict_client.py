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
from dict_client_controller import DictClientController


class DictView:
    def __init__(self):
        self.controller = DictClientController()

    def _menu_one(self):
        """
        一级页面
        :return:
        """
        while True:
            print("""
            -----------欢迎使用本在线词典---------------
            1.登录            2.注册            3.退出
            ----------------------------------------
            """)
            cmd = input("请输入选项:")
            if cmd == "1":
                name = input("请输入账号:")
                password = input("请输入密码:")
                if self.controller.login(name, password):
                    print("登录成功")
                    self._menu_two()
                else:
                    print("登录失败,账号或密码输入错误")
            elif cmd == "2":
                name = input("请输入账号:")
                password = input("请输入密码:")
                resource = self.controller.register(name, password)
                print(resource)

            elif cmd == "3":
                self.controller.exit()
                sys.exit("感谢使用本在线字典")
            else:
                print("请输入正确的选项！")

    def _menu_two(self):
        """
        二级页面
        :return:
        """
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
        """
        调用一级页面，启动客户端
        :return:
        """
        self._menu_one()


# ----------------客户端启动入口---------------- #

if __name__ == '__main__':
    dict = DictView()
    dict.main()
