'''
将数据库增删改查的功能封装成类供客户端调用
'''
from .mysqlpy import Mysqlhelp


class Sqlfunction(object):
    def __init__(self,dbs):
        self.dbs = dbs
        self.mysql = Mysqlhelp(self.dbs)

    def do_add(self,data):
        sql = "insert into product(产品类别,产品名称,产品简介)\
        values('%s','%s','%s')"%(data[1],data[2],data[3])
        res1 = self.mysql.work(sql)
        return res1

    def do_change(self,data):
            # print(line[1],line[2],line[3],line[0])
        sql = "update product set 产品类别='%s',产品名称='%s',产品简介\
        ='%s' where 产品名称='%s'"%(data[2],data[3],data[4],data[1])
        res1 = self.mysql.work(sql)
        return res1

    def do_search(self,data):
        sql = "select * from product where 产品名称='%s'"%data[1]
        try:
            res1 = self.mysql.getall(sql)
        except Exception as e:
            print(e)
        return res1

    def do_delete(self,data):
        sql = "delete from product where 产品名称='%s'"%data[1]
        res1 = self.mysql.work(sql)
        return res1








workfunc = Sqlfunction('warehouse')
