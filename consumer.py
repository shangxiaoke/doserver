#!/usr/bin/env python
#coding:utf-8
from ctrl import dbctrl, cache_ctrl
import conf,pika
        
def conrun():
    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(*conf.rabbitmq_server))
        channel = conn.channel()
        channel.queue_declare(queue='result', durable=True, auto_delete=False)
        channel.basic_qos(prefetch_count=1)
        for method, properties, body in channel.consume('result'):
            #首先连接数据库，如果连接失败直接退出
            db = dbctrl.ctrl() 
            cache = cache_ctrl.ctrl()
            #如果连接成功
            if db.conn() and cache.conn():
                #字符串转字典
                dict_body = eval(body)
                nowtm = dict_body['time']
                ip = dict_body['ipaddress']
                if db.osdt_mk(nowtm):
                    del dict_body['time']
                    del dict_body['ipaddress']
                    #数据库处理
                    for key,value in dict_body.items():
                        db.osdt_insert(nowtm, key, ip, value)
                    #cache处理
                    cache.update(ip, str(dict_body))
            channel.basic_ack(method.delivery_tag)
        channel.cancel()
    except Exception,e:
        return e

if __name__ == "__main__":
    while True:
        try:
            conrun()
        except:
            break