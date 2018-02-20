#!/usr/bin/python
#coding:utf-8

import paramiko,chk,time

class sshdo(object):
    def run(self,ip,uname,userpwd,cmd):
        try:
            self.__ssh=paramiko.SSHClient()
            self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__ssh.connect(ip,22,uname,userpwd,timeout=3)
            self.__sussh=self.__ssh.invoke_shell()
            self.__sussh.settimeout(3)
            time.sleep(0.1)

            #root用户和普通用户默认提示符设置
            ps1 = "export PS1='# '"
            ps2 = "export PS1='$ '"

            if uname == 'root':
                self.__sussh.send('%s\n' % ps1)
                for m in chk.cmdc(cmd):
                    time.sleep(0.1)
                    self.__sussh.send('%s\n' % m)
                    time.sleep(0.1)

                #获取命令执行结果
                resp=self.__sussh.recv(-1)
                while not resp.endswith('#'):
                    rep=self.__sussh.recv(-1)
                    resp+=rep
                #命令返回结果str转list
                re = resp.splitlines()
                #处理后结果返回列表
                new_ret = chk.grep(re,cmd,ps1,ps2,'# ')
                #结果返回列表转字符串
                return '\n'.join(new_ret)
                #关闭连接
                self.__ssh.close()

            else:
                self.__sussh.send('%s\n' % ps2)
                for m in chk.cmdc(cmd):
                    time.sleep(0.1)
                    self.__sussh.send('%s\n' % m)
                    time.sleep(0.1)

                resp=self.__sussh.recv(-1)
                while not resp.endswith('$'):
                    rep=self.__sussh.recv(-1)
                    resp+=rep
                re = resp.splitlines()
                #处理后结果列表返回
                new_ret = chk.grep(re,cmd,ps1,ps2,'$ ')
                return '\n'.join(new_ret)
                #关闭连接    
                self.__ssh.close()
            
        except:
            return False