#!/usr/bin/env python
#coding:utf-8

from pytool import sshdo
from ctrl import dbctrl
from multiprocessing import Process
from gevent import monkey; monkey.patch_all()
import time,gevent,conf,pika

#product       
def dbint(n):
    db = dbctrl.ctrl()
    db.conn()
    #[(A1,),(B2,)]
    ip_db = db.ip_select()
    cmd_db = db.cmd_select()
    if n == 'ip':
        return dict(ip_db)
    
    elif n == 'cmd':
        return dict(cmd_db)

def get_relt(ip):
    relt = [ip]
    ssh = sshdo.sshdo()
    for key,cmd in dbint('cmd'):
        #re = [xx,xxx,xxxx]
        re_cmd = ssh.run(ip, conf.username, conf.password, cmd)
        relt.append(re_cmd)
    return relt

#连接远程mq集群服务，传入消息头标签和消息内容
def prorun():
    try:
        #message [ip,[cmd_result1],[cmd_result2]...]
        conn = pika.BlockingConnection(pika.ConnectionParameters(*conf.rabbitmq_server))
        channel = conn.channel()
        channel.queue_declare(queue='listen', durable=True)
        for key,ip in dbint('ip'):
            message = get_relt(ip)
            channel.basic_publish(exchange='', routing_key='listen', body=message, properties=pika.BasicProperties(delivery_mode=2,))
        conn.close()
    except Exception,e:
        return e
        conn.close()
        
#consum
def callback(ch,method,properties,body):
    #list(body) : [ip,[cmd_result1],[cmd_reslut2]...]
    body_lt = list(body)
    ip = body_lt[0]
    for i in body_lt[1:]:
        i_str = "\n".join(i)
        db.osdt_insert(ip, i_str)
    ch.basic_ack(delivery_tag=method.delivery_tag)
        
def conrun():
    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(*conf.rabbitmq_server))
        channel = conn.channel()
        channel.queue_declare(queue='listen', durable=True, auto_delete=False)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback, queue='listen')
        channel.start_consuming()
    except Exception,e:
        return e

#gevent
def geventrun():
    gevent.joinall([gevent.spawn(pro), gevent.spawn(con)])

if __name__ == "__main__":
    while True:
        try:
            now = time.strftime("%Y%m%d%H%M%S", time.localtime())
            db = dbctrl.ctrl(now)
            db.osdt_mk()
            pro = prorun()
            con = conrun()
            p = Process(target=geventrun)  
            p.start()
            time.sleep(conf.interval)
        except:
            break