'''
客户端访问服务器的主函数
'''
from Client.clientclasses import *
from getpass import getpass

def R_order(myorder):
    while True:
        try:
            name = input('请输入注册用户名：')
            if ' ' in name:
                print('姓名中不允许有空格，请重新输入：')
                break
            passwd = getpass('请输入密码：')
            passwd1 = getpass('请再次输入密码：')
            if passwd != passwd1:
                print('两次密码不一致，请重新输入：')
                break
            msg = 'R {} {}'.format(name,passwd)
            myorder.do_register(msg)
            break
        except KeyboardInterrupt:
            return
        except Exception:
            continue

def L_order(myorder):
    while True:
        try:
            name = input('请输入用户名：')
            # print('该出手是就出手')
            passwd = getpass('请输入登录密码：')
            msg = 'L {} {}'.format(name,passwd)
            myorder.do_login(msg)
            break
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(e)
            print('你再给我牛逼一次！')
            continue



def main():
    myorder = Myorder()
    while True:
        menu()
        msg = input('请输入命令代码：')
        if msg == 'R':
            R_order(myorder)
        elif msg == 'L':
            L_order(myorder)
        elif msg == 'Q':
            myorder.do_quit()
            sys.exit('您已成功退出')
        else:
            pass

if __name__ == '__main__':
    main()