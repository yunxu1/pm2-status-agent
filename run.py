#!/Users/yunxu/pyvirtaul/scan/bin/python
# -*- coding:utf-8 -*-
from bottle import *
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import ast
import json
import MySQLdb
import datetime
from time import time

class DB():

    def __conn(self):
        try:
            conn = MySQLdb.connect("10.211.55.12", "root", "root", "pm2manager")
            return conn
        except Exception,e:
            print e


    def executeUpdate(self,sql,args=None):
        #print sql

        rows=-1
        con = self.__conn()
        try:

            c=con.cursor()
            if args:
                #print args
                rows= c.execute(sql,args)
            else:
                rows= c.execute(sql)
            con.commit()
        except Exception,e:
            print e
        finally:
            con.close()
        return rows


    def QueryByNameAndHost(self,name,host):
        sql='select count(1) from proccesMgr where name=%s and host=%s'

        con=self.__conn()
        try:
            cursor = con.cursor()
            cursor.execute(sql,(name,host))
            res=cursor.fetchone()
            return res[0]
        except Exception,e:
            print e
        finally:
            con.close()

    def QueryShow(self):
        sql='select id,name,host,pid,status,createtime from proccesMgr where name!=\'pmagent\''
        con=self.__conn()
        try:
            c=con.cursor()
            c.execute(sql)
            res=c.fetchall()
            return res
        except Exception,e:
            print e

        finally:
            con.close()



db=DB()

#获取agent发送来的数据,如果是新数据就添加,是旧数据就通过进程名和IP更新进程的PID和状态以及更新时间
def ProcesStatusUpdate(msg):
    msg = ast.literal_eval(msg)

    host=msg['host']
    process_list=msg['proccess']
    proccess_name_list=msg['proccessNameItem']

    #删除这个host主机里没有的进程信息,如果pm2下delete掉一个任务,那么就对比数据,删除多余的进程信息
    if proccess_name_list:
        sql_where= ','.join(proccess_name_list)
        sql="delete from proccesMgr where host='%s' and name not in (%s)"%(host,sql_where)
        db.executeUpdate(sql)
    else:#如果某个pm2删除了所有进程,这里跟着删除
        sql="delete from proccesMgr where host='%s'"%host
        db.executeUpdate(sql)
    #更新数据库的信息或者添加新的进程信息进去
    for info in process_list:
        status = 1 if info['status'].lower() == 'online' else 0
        ts = time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        res = db.QueryByNameAndHost(info['name'], host)
        if res <= 0:
            sql = 'insert into proccesMgr(name,host,pid,status,createtime) values (%s,%s,%s,%s,%s)'
            db.executeUpdate(sql, (info['name'], host, info['pid'], status, timestamp))
        else:
            sql = 'update proccesMgr set status=%s,pid=%s,createtime=%s where name=%s and host=%s'
            db.executeUpdate(sql, (status, info['pid'],timestamp, info['name'], host))


#输出数据库中进程的所有状态
def show(ws):
    try:
        info = list()
        cursor = db.QueryShow()
        for rows in cursor:
            id, name, host, pid, status, createtime = rows
            proinfo = {"id": id, "name": name, "host": host, "pid": pid, "status": int(status),
                       "createtime": str(createtime)}
            info.append(proinfo)
        msg = json.dumps(info)
        try:
            ws.send(msg)
        except Exception, e:
            print e
            pass
    except Exception, e:
        print e



@get('/websocket', apply=[websocket])
def proccessMonitor(ws):
    while True:
        msg = ws.receive()
        if msg=='show':
            show(ws)
        elif msg is not None:
            ProcesStatusUpdate(msg)
        else:break


@route('/')
def index():
    return 'hi~'

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, server=GeventWebSocketServer)