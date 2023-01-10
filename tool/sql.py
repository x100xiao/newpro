#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/27
@Author  : LL
@File    : mysql_.py
'''

import pymysql
from config.config import MYSQL_CONFIG
from tool.log import logger


class MysqlDb():

    def __init__(self, host, port, user, password, db_name):

        self.db = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=db_name
        )
        self.cur = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
        self.cur.close()
        self.db.close()

    def select_db(self, sql):
        """查询"""
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def execute_db(self, sql):
        """更新/插入/删除"""
        try:
            self.cur.execute(sql)
            self.db.commit()
        except Exception as e:
            logger.error("操作出现错误：{}".format(e))
            self.db.rollback()


mysql_db = MysqlDb(*MYSQL_CONFIG)


if __name__ == '__main__':
    # aa='99' #参数化sql

    print(mysql_db.select_db("SELECT ID FROM patient_statistics_data WHERE device_id = 'GB-2B004519'"))
    # mysql_db.execute_db("INSERT INTO case_test(title,ex) VALUES ('1', '1');")
    # mysql_db.execute_db(f"UPDATE case_test SET title = '标题2', ex = {aa} WHERE id = 1;")
    # mysql_db.execute_db(f"delete from case_test where ex={aa}")
    # # 多表联查
    # print(mysql_db.select_db("SELECT * FROM case_test t left join case_data d on t.id=d.case_id "))

