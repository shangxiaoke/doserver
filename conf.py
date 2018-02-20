#!/usr/bin/env python
#coding:utf-8

#pip：pika/mysql-connect/redis

#ssh
username = ''
password = ''

#SQL数据库连接配置
doserver_db = {'host':'192.168.100.5',
             'port':3306,
             'user':'doserver',
             'password':'doserver123',
             'database':'doserver',
             'charset':'utf8'}

#rabbitmq
rabbitmq_server = ('192.168.100.5',5672)

#redis
cache = ['192.168.100.5',6379,'db0']

#multiprocessing
poolnum = ''
interval = '' 