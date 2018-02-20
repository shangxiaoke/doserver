#!/usr/bin/env python
#coding:utf-8
from pytool import sshdo
from ctrl import dbctrl
from multiprocessing import Pool
import time,conf,pika

#product       
def dbint(n):
    db = dbctrl.ctrl()
    db.conn()
    
    if n == 'ip':
        ip_db = dict(db.ip_select())
        return ip_db
    
    elif n == 'cmd':
        cmd_db = dict(db.cmd_select())
        return cmd_db
    
def get_relt(ip):
    results = {'time':nowtm,'ipaddress':ip}
    ssh = sshdo.sshdo()
    for key,cmd in dbint('cmd').items():
        #type(re_cmd)=str
        re_cmd = ssh.run(ip, conf.username, conf.password, cmd)
        results.update({key:re_cmd})
    return results

#连接远程mq集群服务，传入消息头标签和消息内容
def prorun(message):
    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(*conf.rabbitmq_server))
        channel = conn.channel()
        channel.queue_declare(queue='result', durable=True)
        channel.basic_publish(exchange='', routing_key='result', body=message, properties=pika.BasicProperties(delivery_mode=2,))
        conn.close()
    except Exception,e:
        return e
        conn.close()

if __name__ == "__main__":
    global nowtm
    while True:
        nowtm = time.strftime("%Y%m%d%H%M%S", time.localtime())
        p = Pool(conf.poolnum)
        while True:
            try:
                for key,ip in dbint('ip').items():
                    p.apply_async(prorun,args=(str(get_relt(ip))))
                p.close()
                p.join()
                break
                time.sleep(conf.interval)
            except:
                break