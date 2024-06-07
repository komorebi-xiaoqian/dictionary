# -*- coding: UTF-8 -*-
'''
@Project ：dictionary 
@File    ：dict_db.py
@IDE     ：PyCharm 
@Author  ：komorebi
@Email   ：komorebi.so.67@gmail.com
@Date    ：2024/6/5 16:07
在线字典服务器端数据层，必要的数据支持
'''
import hashlib

import pymysql


# 密码加密 使用哈希算法加密(小测试，用处不大，可以使用其他加密算法)
def change_passwd(passwd):
    hash = hashlib.sha256()
    hash.update(passwd.encode())
    return hash.hexdigest()


class DictDB:
    def __init__(self):
        # 连接数据库
        self.kwargs = {
            "user": "root",
            "password": "123456",
            "port": 3306,
            "database": "dict",
            "charset": "utf8"

        }
        self.db = pymysql.connect(**self.kwargs)
        self.cur = self.db.cursor()

    def register(self, name, password):
        """
        注册数据支持
        :param name: 接收账户信息
        :param password: 接收密码信息
        :return: T or F bool类型
        """
        password = change_passwd(password)
        sql = "insert into user (name ,password) value (%s,%s);"
        try:
            self.cur.execute(sql, (name, password))
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    def login(self, name, password):
        """
        登录数据支持
        :param name: 接收账户信息
        :param password: 接收密码信息
        :return: T or F bool类型
        """
        password = change_passwd(password)
        sql = "select id from user where name = %s and password = %s;"
        self.cur.execute(sql, (name, password))
        if self.cur.fetchone():
            return True
        return False

    def query(self, word):
        """
        查单词数据支持
        :param word: 用户输入的单词
        :return: 查询结果 (mean,) or None
        """
        sql = "select mean from words where word = %s;"
        self.cur.execute(sql, (word,))
        return self.cur.fetchone()

    def insert_history(self, name, word):
        """
        插入历史记录
        :param name: 用户账号
        :param word: 查询的单词
        :return:
        """
        sql = "select id from user where name=%s;"
        self.cur.execute(sql, (name,))
        user_id = self.cur.fetchone()[0]
        sql = "select id from words where word=%s;"
        self.cur.execute(sql, (word,))
        words_id = self.cur.fetchone()[0]
        sql = "insert into history (user_id,words_id) values (%s,%s);"
        self.cur.execute(sql, [user_id, words_id])
        self.db.commit()

    def history(self, name):
        """
        查询历史记录数据支持
        :param name: 用户账号
        :return: 查询结果 ((name,word,time),...) or None
        """
        sql = """
               SELECT user.name, words.word, history.time
               FROM user
               INNER JOIN history ON user.id = history.user_id
               INNER JOIN words ON words.id = history.words_id
               WHERE user.name = %s
               ORDER BY history.time DESC
               LIMIT 10;
           """
        self.cur.execute(sql, (name,))
        return self.cur.fetchall()


# ---------------测试入口----------------#
if __name__ == '__main__':
    dict = DictDB()
    # dict.register("komorebi", "123456")
    # dict.login("komorebi", "123456")
    # dict.query("a")
    # dict.insert_history("komorebi", "a")
    dict.history("komorebi")
