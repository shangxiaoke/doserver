#!/usr/bin/env python
#coding:utf8

import redis,conf
class ctrl(object):
    def conn(self):
        try:
            self.__pool = redis.ConnectionPool(*conf.cache)
            self.__conn = redis.StrictRedis(connection_pool = self.__pool)
            return True
        except:
            return False
        
    def expire(self,key,seconds):
        self.__conn.expire(key, seconds)
    
    def update(self,key,value):
        if self.__conn.exists(key):
            self.__conn.set(key,value)
        else:
            self.__conn.set(key,value)
    
    def get(self,key):
        reva = self.__conn.get(key)
        if not reva:
            return False
        else:
            return reva