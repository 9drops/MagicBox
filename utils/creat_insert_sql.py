#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

class SQLCreator:
    __dataFile = None
    __dbname = "db_magic_box"

    def __init__(self, dataFile, dbname = None):
        self.__dataFile = dataFile
        if dbname:
            self.__dbname = dbname

    def create_sqlFile(self):
        """
        Create SQL File tab_xxx_field.sql For sql model file tab_xxx_field.txt
        """
        sql, lines = None, None
        fileNameNoExt = os.path.splitext(self.__dataFile)[0]
        table_name    = os.path.basename(fileNameNoExt)
        create_tabel_sql = "use {};\ncreate table {}(field_name varchar(100) not null primary key, description varchar(200));\n".format(self.__dbname, table_name)
        sql_file      = fileNameNoExt + ".sql"
        with open (self.__dataFile, 'r') as f:
            lines = f.readlines()
        lines.remove("\n")
        writen_lines = 0
        count = int(len(lines) / 2)
        with open(sql_file, "w") as f:
            f.write(create_tabel_sql)
            for i in range(int(count)):
                index = int(i)
                sql = "insert into  {}(field_name, description) values ('{}', '{}');\n".format(table_name, lines[index].strip("\n"), lines[index + count].strip("\n"))
                if f.write(sql) > 0 :
                    writen_lines += 1
        if writen_lines != count :
            print("Create sql file failure!")

    @classmethod
    def table_name(cls, kpiName, period, stockCode):
        """
        table name: tab_{kpiName}_{period}_{stockCode}}
        """
        table = "tab_{}_{}_{}".format(kpiName, period, stockCode)
        return table
        
    @classmethod
    def create_table_sql(cls, kpiName, period, stockCode):
        """
        SQL string of caret table: tab_{kpiName}_{period}_{stockCode}}
        """
        lines = None
        dirPath = os.path.dirname(os.path.abspath(__file__))
        dataFile = dirPath + "/tab_" + kpiName + "_field.txt"
        tableName = "tab_{}_{}_{}".format(kpiName, period, stockCode)
        sql = "create table " + tableName
        with open (dataFile, 'r') as f:
            lines = f.readlines()
        lines.remove("\n")
        count = int(len(lines) / 2)
        for i in range(int(count)):
            index = int(i)
            if index == 0:
                sql += "(" + lines[i].strip("\n") + " varchar(32) primary key,"
            elif index == count - 1:
                sql += lines[i].strip("\n") + " varchar(32))"
            else:
                sql += lines[i].strip("\n") + " varchar(32),"
        return sql

    @classmethod
    def insert_table_sql(cls, table_name, row):
        values = ""
        for v in row:
            values += "'{}',".format(v)
        values = values.strip(',')
        sql = "insert into {} values ({})".format(table_name, values)
        return sql

if __name__ == "__main__":
    args = sys.argv
    if (len(args) < 2):
        print("Usage:", args[0], " tab_xxx_field.txt")
        exit(0)
    creator = SQLCreator(args[1])
    creator.create_sqlFile()
    # sql = creator.create_table_sql("main", "year", 123)
    # print("sql:", sql)