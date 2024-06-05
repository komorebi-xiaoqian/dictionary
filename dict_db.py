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
import pymysql


class DictDB:
    def __init__(self):
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
        sql = "insert into user (name ,password) value (%s,%s);"
        try:
            self.cur.execute(sql, (name, password))
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False


# ---------------测试入口----------------#
if __name__ == '__main__':
    dict = DictDB()
    dict.register("komorebi", "123456")
