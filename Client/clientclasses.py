'''
创建客户端访问数据库所需要的各种功能类
'''
from socket import *
import sys,os

HOST = ''
PORT = 8888
ADDR = (HOST, PORT)
BUFSIZE = 1024

#创建客户端访问数据库的类
class Myorder(object):
    def __init__(self):
        self.sockfd = socket()
        self.sockfd.connect(ADDR)

    #客户端注册程序块
    def do_register(self,msg):
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(BUFSIZE).decode()
        if data == 'Success':
            print('您已注册成功！请登录！')
        elif data == 'Exist':
            print('该用户名已存在，请重新输入．')
        else:
            print('其他原因注册失败，请重新输入．')
        return

    #客户端登录程序块
    def do_login(self,msg):
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(BUFSIZE).decode()
        if data == 'OK':
            print('您已成功登录！')
            self.do_work()
        elif data == 'Wrong':
            print('密码输入有误，请重新输入．')
        elif data == 'FALL':
            print('该用户不存在，请重新输入．')
        return

    #通知服务端客户端断开连接退出
    def do_quit(self):
        self.sockfd.send(b'Q')
        return

    #创建数据库执行方法，内部建立增删改查函数，提交命令．
    #数据库操作的核心程序部分，需要重点考虑如何与数据库对接．
    def do_work(self):

        while True:
            dbsmenu()
            dbmsg = input('请输入操作命令：')

            # 客户端发起添加数据库信息的指令
            if dbmsg == 'A':
                while True:
                    msg = '*'
                    try:
                        a = input('请输入产品类别：')
                        b = input('请输入产品名称：')
                        c = input('请输入产品简介：')
                        msg = 'A*{}*{}*{}'.format(a,b,c)
                        self.sockfd.send(msg.encode())
                        print('发起产品添加')
                        data = self.sockfd.recv(128).decode()
                        if data == 'OK':
                            print('插入成功！')
                        elif data == 'NO':
                            print('插入失败！')
                        else:
                            print('未知原因错误！')
                    except KeyboardInterrupt:
                        break

            # 客户端发起更改数据库信息的指令
            elif dbmsg == 'C':
                while True:
                    msg = '*'
                    try:
                        name = input('请输入产品名：')
                        a = input('请输入产品类别：')
                        b = input('请输入产品名称：')
                        c = input('请输入产品简介：')
                        msg = 'C*{}*{}*{}*{}'.format(name,a,b,c)
                        self.sockfd.send(msg.encode())
                        print('发起产品修改')
                        data = self.sockfd.recv(128).decode()
                        if data == 'OK':
                            print('修改成功！')
                        elif data == 'NO':
                            print('修改失败！')
                        else:
                            print('未知原因错误！')
                    except KeyboardInterrupt:
                        break

            # 客户端发起删除数据库信息的指令
            elif dbmsg == 'D':
                while True:
                    try:
                        name = input('请输入产品名：')
                        msg = 'D*{}'.format(name)
                        self.sockfd.send(msg.encode())
                        print('提起删除申请！')
                        data = self.sockfd.recv(128).decode()
                        if data == 'OK':
                            print('删除成功！')
                        elif data == 'NO':
                            print('删除失败！')
                        else:
                            print('未知原因错误！')
                    except KeyboardInterrupt:
                        break

            # 客户端发起查询数据库信息的指令
            elif dbmsg == 'S':
                while True:
                    try:
                        name = input('请输入产品名：')
                        msg = 'S*{}'.format(name)
                        self.sockfd.send(msg.encode())
                        print('提起查找申请！')
                        data = self.sockfd.recv(1024).decode()
                        for line in eval(data):
                            print(line)
                            # 此处需要根据具体数据库进一步细化！
                    except KeyboardInterrupt:
                        break

            # 客户端退出二级命令菜单
            elif dbmsg == 'B':
                return


#主命令菜单，一级命令菜单
def menu():
    print('********************')
    print('*****注册命令：R*****')
    print('***** 登录命令：L*****')
    print('******退出命令：Q ****')
    print('*********************')
    print('执行命令，请输入命令字母！')

#数据库操作命令菜单
def dbsmenu():
    print('****　 数据库命令 ****')
    print('***** 查看数据：S ****')
    print('***** 修改数据：C ****')
    print('*****　添加数据：A ****')
    print('***** 删除数据：D ****')
    print('***** 退回上级：B ****')
    print('********************')
