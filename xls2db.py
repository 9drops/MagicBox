#!/usr/bin/python
import sys
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy as sa

sys.path.append(r'./utils')
from creat_insert_sql import SQLCreator as sc

# -*- coding: utf-8 -*-

"""
Author:Alan Chan
Date:17/12 2019
Description:XLS to Mysql table data
"""

class XLS2MYSQL:
    @classmethod
    def xls2db(cls, kpiname, period, stockcode, xlspath):
        tablename = sc.table_name(kpiname, period, stockcode)
        engine = create_engine('mysql+pymysql://root@localhost:3306/db_magic_box')
        #1.tablename不存在则创建表
        if engine.has_table(tablename) != True :
            sql = sc.create_table_sql(kpiname, period, stockcode)
            try:
                engine.execute(sa.text(sql))
            except:
                print("[Warnning]create table error!")

        df = pd.read_excel(xlspath)
        colnum = df.shape[1]

        for i in range(1, colnum):
            df = pd.read_excel(xlspath, index_col=0, usecols=[i])
            #2.插入行到mysql表
            insertsql = sc.insert_table_sql(tablename, df.index)
            #print("sql:", insert_sql)
            try:
                engine.execute(sa.text(insertsql))
            except:
                print("[Warnning]insert error!")
    
if __name__ == "__main__":
    args = sys.argv
    XLS2MYSQL.xls2db("cash", "period", 600276, "cash.xls")
