# -*- coding: UTF-8 -*-
'''
@Project ：dictionary 
@File    ：process_data_to_the_database.py
@IDE     ：PyCharm 
@Author  ：komorebi
@Email   ：komorebi.so.67@gmail.com
@Date    ：2024/6/5 21:18
把txt转存到mysql dict数据库中words表中
'''
import re

import pymysql


class Dict:
    def __init__(self):
        self.kwargs = {
            "user": "root",
            "password": "123456",
            "port": 33061,
            "database": "dict",
            "charset": "utf8"

        }
        self.db = pymysql.connect(**self.kwargs)
        self.cur = self.db.cursor()

    def get_data(self):
        """
        获取txt文件中单词和意思，并把他们加入到列表中
        :return: data 列表类型
        """
        data = []
        fr = open("dict.txt", "r")
        for line in fr.readlines():
            # [(word,mean)]
            data += re.findall(r"(\w+)\s+(.+)", line)
        fr.close()
        return data

    def insert_word(self):
        data = self.get_data()
        try:
            sql = "insert into words (word,mean) value (%s,%s)"
            self.cur.executemany(sql, data)
        except Exception as e:
            print(e)
            self.db.rollback()
        else:
            self.db.commit()

    def close(self):
        """
        关闭
        :return:
        """
        self.cur.close()
        self.db.close()


if __name__ == '__main__':
    dict = Dict()
    dict.insert_word()
    dict.close()
