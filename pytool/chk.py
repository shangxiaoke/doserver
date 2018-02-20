#/usr/bin/env python
#coding:utf-8

#IP合法检测
def ipchk(addr):
    b=addr.split('.')
    if len(b) == 4 and b[0] != '0' and b[3] != '0':
        try:
            if 255 > int(b[0]) and int(b[1]) and int(b[2]) and int(b[3]) >= 0:
                return True
        except:
            return False
    else:
        return False

#IP传递方法，列表或者IP文件
def ipc(ip):
    if type(ip) is list:
        for i in ip:
            yield i

#使cmd参数支持列表或文件
def cmdc(cmd):
    if type(cmd) is list:
        for i in cmd:
            yield i
#结果处理，排除自定义和杂项
def grep(relist,cmd,ps1,ps2,tag):
    rel=[]
    for i in relist:
        if (i != '') and (i !=' ') and \
        (ps1 not in i) and (ps2 not in i) and \
        not i.startswith('Last login: ') and \
        not i.endswith('#') and not i.endswith('$'):
            for ct in cmd:
                st = tag+ct
                if st != i:
                    rel.append(i)    
    return rel