'''
将服务器端的登录注册及数据库操作等功能封装成类，供服务端主函数调用
'''
from Server.mysqlpy import *
from hashlib import sha1
from multiprocessing import Process
from socket import *
from Server.menu import *
from signal import *
from Server.work import workfunc

#服务端的地址设定为固定值．
HOST = ''
PORT = 8888
ADDR = (HOST, PORT)
BUFSIZE = 1024

#建立服务端注册/登录/退出等功能的类
class Mysqlfunc1(object):
    def __init__(self, database):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(ADDR)
        self.sockfd.listen(5)
        self.database = database
        self.mysql = Mysqlhelp(self.database)

    #服务端利用多进程，循环接收客户端访问
    #Mysqlfunc1类的执行方法
    def serverForever(self):
        signal(SIGCHLD, SIG_IGN)
        while True:
            connfd, cliaddr = self.sockfd.accept()
            p = Process(target=self.handlerclient, args=(connfd,cliaddr))
            p.start()

    #子进程的执行函数,执行用户的注册，登录等功能
    def handlerclient(self, connfd, cliaddr):
        print('客户端%s已建立连接',cliaddr)
        while True:
            #循环接收客户端的请求命令，进行处理
            data = connfd.recv(BUFSIZE).decode()
            if data[0] == 'R':
                self.do_register(connfd, data)
            elif data[0] == 'L':
                self.do_login(connfd, data)
            elif data == 'Q':
                connfd.close()
                print('%s已断开连接．'%cliaddr)
            else:
                pass
            # #处理客户端数据库访问请求
            # else:
            #     self.do_work()
            #     pass

    # 服务端处理客户端的用户注册申请
    def do_register(self,connfd, data):
        #收到客户端的注册请求，分离出注册的姓名和密码
        name = data.split()[1]
        passwd = data.split()[2]
        # print(msg)
        #查看用户数据库中是否存在新提交的注册用户名
        sql1 = "select * from user where name = '%s'"%name
        res1 = self.mysql.getone(sql1)
        print('res1=', res1)
        #如果注册名已经存在，给客户段返回Exist，返回到上级程序，继续等待．
        if res1 != None:
            connfd.send(b'Exist')
            return           #不能退出
        #如果注册名不存在，向用户名数据库添加新的用户和密码记录．
        else:
            sql2 = "insert into user (name,passwd) values ('%s','%s')"\
            %(name,passwd)
            res2 = self.mysql.work(sql2)  #添加执行结束，获取返回值
            if res2 == 1:
                connfd.send(b'Success')
            else:
                connfd.send(b'Fail')
            return

    #客户登录方法
    def do_login(self,connfd, data):
        #收到客户端的登录请求，分离出姓名和密码
        name = data.split()[1]
        passwd = data.split()[2]

        #查看用户数据库中是否存在用户名
        sql1 = "select * from user where name = '%s'"%name
        res1 = self.mysql.getone(sql1)
        #如果用户名已经存在，给客户端返回Exist，返回到上级程序，继续等待．
        if res1 != None:
            print('我已经收到１１１１！')
            sql = "select passwd from user where name= '%s'"%name
            passwd1 = self.mysql.getall(sql)[0][0]
            print(passwd1)
            if passwd == passwd1:
                connfd.send(b'OK')
                # name1 = name
                self.do_work(connfd)
                return
            else:
                connfd.send(b'Wrong')
        else:
            print('该用户不存在！')
            connfd.send(b'FALL')
        return


    #处理客户端的数据库访问请求
    def do_work(self,connfd):

        while True:
            msg = connfd.recv(1024).decode()
            if msg[0] == 'A':
                data = msg.split('*')
                res2 = workfunc.do_add(data)
                if res2 == 1:
                    connfd.send(b'OK')
                else:
                    connfd.send(b'NO')
            elif msg[0] == 'C':
                data = msg.split('*')
                res2 = workfunc.do_change(data)
                if res2 == 1:
                    connfd.send(b'OK')
                else:
                    connfd.send(b'NO')
            elif msg[0] == 'D':
                data = msg.split('*')
                res2 = workfunc.do_delete(data)
                if res2 == 1:
                    connfd.send(b'OK')
                else:
                    connfd.send(b'NO')
            elif msg[0] == 'S':
                data = msg.split('*')
                res2 = workfunc.do_search(data)
                connfd.send(str(res2).encode())
                # do_search()
            elif msg == '*back*':
                # print('我收到了******')
                break
            else:
                pass






    #后台打印用户退出记录
    def do_quit(self,cliaddr):
        print('客户端%s已断开连接．',cliaddr)
        
