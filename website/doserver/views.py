#coding:utf8
import redis
from django.http import HttpResponse
from django.template import loader,Context

def all():
    try:
        pool = redis.ConnectionPool(host='192.168.100.5',port=6379,db=0)
        conn = redis.StrictRedis(connection_pool = pool)

        #获取key总列表
        ip_list = conn.keys('*')
        
        #获取第一个key的value，转换为字典
        data_dict = eval(conn.get(ip_list[0]))
        
        #获取value字典内的key：对应cmd的description
        desc_list = ['IP']
        for key,value in data_dict.items():
            desc_list.append(key)

        #获取所有value的值:[[v1,v2..],[v1,v2..]...]
        data_list = []
        for ip in ip_list:
            #获取key：ip对应的值，并转换回字典格式
            value_dict = eval(conn.get(ip))
            #字典转列表，将key:ip添加至列表头部
            value_list = value_dict.values()
            value_list.insert(0,ip)
            #整合为列表
            data_list.append(value_list)
    
        return {'descript':desc_list,'data':data_list}

    except:
         return False

def index(request):
    #获取模板
    t = loader.get_template("table.html")
    #获取值
    data = all()
    desc_list = data['descript']
    data_list = data['data']
    
    #向模板提供数据
    c = Context({'desc':desc_list,'result':data_list})
    return HttpResponse(t.render(c))
