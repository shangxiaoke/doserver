#!/usr/bin/env python
#coding:utf8

import mysql.connector,conf
from mysql.connector import errorcode

class ctrl(object):
    def conn(self):
        try:
            self.__cnx = mysql.connector.connect(**conf.doserver_db)
            self.__cursor = self.__cnx.cursor()
        except mysql.connector.Error as err:
            self.__cursor.close()
            self.__cnx.close()
            return False

    def close(self):
        self.__cursor.close()
        self.__cnx.close()
 
    #日期数据表创建
    def osdt_mk(self,tbname):
        try:
            sql_A = "CREATE TABLE IF NOT EXISTS `%s` (`ipaddress` varchar(32) NOT NULL primary key)" % tbname
            self.__cursor.execute(sql_A)
            #{'description1':'command1'...}
            cmd_d = dict(self.cmd_select())
            for key,value in cmd_d.items():
                sql_B = "ALTER TABLE `%s` ADD `%s` text" % (tbname, key)
                self.__cursor.execute(sql_B)
            self.__cnx.commit()
            return True
        except:
            self.__cnx.rollback()
            return False
        finally:
            self.close()

    #日期数据表osdt插入方法
    def osdt_insert(self,tbname,colume,ip,ret):
        sql = "INSERT INTO `%s` (`ipaddress`,`%s`) VALUES ('%s', '%s')" % (tbname,colume,ip,ret)
        try:
            self.__cursor.execute(sql)
            self.__cnx.commit()
            return True
        except:
            self.__cnx.rollback()
            return False
        finally:
            self.close()

    #日期数据表osdt查询方法
    def osdt_select(self,tbname):
        sql = "SELECT * FROM `%s`" % (tbname)
        try:
            self.__cursor.execute(sql)
            result=self.__cursor.fetchall()
            return result
        except:
            return False
        finally:
            self.close()

    #表cmdt插入方法
    def cmd_insert(self,name,cmd):
        sql = "INSERT INTO `cmd_config` (`description`,`command`) VALUES ( '%s', '%s')" % (name,cmd)
        try:
            self.__cursor.execute(sql)
            self.__cnx.commit()
            return True
        except:
            self.__cnx.rollback()
            return False
        finally:
            self.close()   

    #表cmdt更新方法
    def cmd_update(self,key,value):
        sql = "UPDATE `cmd_config` SET `command`='%s' WHERE `description`='%s'" % (key, value)
        try:
            self.__cursor.execute(sql)
            self.__cnx.commit()
            return True
        except:
            self.__cnx.rollback()
            return False
        finally:
            self.close()

    #表cmdt查询方法
    def cmd_select(self):
        sql = "SELECT * FROM `cmd_config`"
        try:
            self.__cursor.execute(sql)
            result=self.__cursor.fetchall()
            return result
        except:
            return False
        finally:
            self.close()
    #表cmdt删除方法
    def cmd_delete(self,key):
        sql = "DELETE FROM `doserver`.`cmd_config` WHERE `description`='%s' or `command`='%s'" % key
        try:
            self.__cursor.execute(sql)
            self.__cnx.commit()
            return True
        except:
            self.__cnx.rollback()
            return False
        finally:
            self.close()

    #表ipdt插入方法
    def ip_insert(self,ip):
        sql = "INSERT INTO `ip_config` (`ipaddress`) VALUES ('%s')" % (ip)
        try:
            self.__cursor.execute(sql)
            self.__cnx.commit()
            return True
        except:
            self.__cnx.rollback()
            return False
        finally:
            self.close()

    #表ipdt更新方法
    def ip_update(self,new,old):
        sql = "UPDATE `ip_config` SET `ipaddress`='%s' WHERE `ipaddress`='%s'" % (new,old)
        try:
            self.__cursor.execute(sql)
            self.__cnx.commit()
            return True
        except:
            self.__cnx.rollback()
            return False
        finally:
            self.close()

    #表ipdt查询方法
    def ip_select(self):
        sql = "SELECT * FROM `ip_config`"
        try:
            self.__cursor.execute(sql)
            result=self.__cursor.fetchall()
            return result
        except:
            return False
        finally:
            self.close()