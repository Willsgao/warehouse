#!/usr/bin/env python3
#!coding = utf-8
'''
服务端运行的主程序．
'''
#从方法类模块中导入sql执行方法
from Server.serverclasses import *

def main():
    mysql1 = Mysqlfunc1('warehouse')
    mysql1.serverForever()



if __name__ == "__main__":
    main()
