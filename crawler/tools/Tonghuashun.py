#!/bin/python
#coding=utf-8
import os
from urllib2 import *
from bs4 import BeautifulSoup #html解析
import json
import time
import datetime
import sqlite3
from Log import *
from Database import *
class Tonghuashun(object):
    homePage='http://stockpage.10jqka.com.cn/'
    def __init__(self,filePath,hp=None):
        self.filePath=filePath
        if os.path.exists(self.filePath)==False:
            os.makedirs(self.filePath)
        self.databasePath=filePath+'stockPrediction.db'
        self.log=Log()
        self.db=Database(self.databasePath)
        dt=datetime.datetime.now()
        curtime=dt.strftime('%H')
        if int(curtime)<9:
            dt=dt-datetime.timedelta(days=1)
        self.date=dt.strftime('%Y-%m-%d').decode('utf-8')
        strStart='calculating date:'+self.date
        print strStart
        self.log.runLog(strStart)
        if hp!=None:
            self.homePage=hp;
    def refreshOneStock(self,id):
        url=self.homePage+r'spService/'+str(id)+r'/Header/realHeader'
        print url
        headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}  
        req = Request(url=url,headers=headers)  
        try:
            responce=urlopen(req)
            try:
                jsonData=responce.read()
                try:
                    arrInfo=json.loads(jsonData)
                    if arrInfo['stockname']=='':
                        strLog=str(id)+' is Null!'
                        self.log.runLog(strLog)
                        arrInfo=None        
                except:
                    strLog='crawler can\'t get data by '+str(id)
                    self.log.errorLog(strLog)
                    arrInfo=None
            except:
                strLog='http responce error '+str(id)
                print strLog
                self.log.errorLog(strLog)
                arrInfo=None        
        except:
            strLog='Taking a break from '+str(id)
            print strLog
            self.log.errorLog(strLog)
            time.sleep(5)
            arrInfo=None        
        finally:
            return arrInfo
    def normalizeName(self,name):
        out=name.replace('*','')
        return out.decode('utf-8')
    def normalizeCJL(self,cjl):
        if u'手' in cjl:
            arr=cjl.split(u'手')
            cjl=arr[0]
        cjl=cjl.decode('utf-8')
        return cjl
    def refreshStock(self,type,start,end):
        typePath=self.filePath+type+'\\'
        if os.path.exists(typePath)==False:
            os.mkdir(typePath)
        for i in range(start,end):
            id='%06d'%i
            stockInfo=self.refreshOneStock(id)
            if stockInfo==None:
                continue
            name=stockInfo['stockname']
            name=self.normalizeName(name)
            cjl=self.normalizeCJL(stockInfo['cjl'])
            strInfo=id+'\t'+self.date+'\t'+type+'\t'+stockInfo['fieldname']+\
            '\t'+name+'\t'+stockInfo['kp']+'\t'+stockInfo['xj']+'\t'+\
            stockInfo['zg']+'\t'+stockInfo['zd']+'\t'+cjl
            print strInfo
            arrStockInfo=strInfo.split('\t')
            self.db.refreshStockDaily(arrStockInfo)
            time.sleep(1)
    def refreshIndex(self):
        indexPath=self.filePath+u'指数\\'
        if os.path.exists(indexPath)==False:
            os.mkdir(indexPath)
        url=r'http://q.10jqka.com.cn/interface/stock/zs/zdf/desc/1/quote/quote'
        print url
        headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}  
        req = Request(url=url,headers=headers)  
        responce=urlopen(req)
        jsonData=responce.read()
        try:
            arrInfo=json.loads(jsonData)
            for idx in arrInfo['data']:
                #上证 深成指 沪深300
                if idx['indexcode']=='1A0001' or idx['indexcode']=='399001' \
                or idx['indexcode']=='1B0300':
                    strIndex=idx['indexcode']+'\t'+self.date+'\t'+idx['zxj']+\
                    '\t'+idx['zde']+'\t'+idx['zdf']
                    arrIndex=strIndex.split('\t')
                    self.db.refreshIndexDaily(arrIndex)
        except:
            strLog='crawler can\'t get index data from '+url
            print strLog
            self.log.errorLog(strLog)
    def run(self):
        self.refreshIndex()
        self.refreshStock(u'深证A股',1,2)
        '''self.refreshStock(u'深证A股',1690,1899)
        self.refreshStock(u'上证A股',600000,602000)
        self.refreshStock(u'上证A股',600525,602000)
        self.refreshStock(u'上证A股',603000,603333)
        self.refreshStock(u'中小板',2001,2800)
        self.refreshStock(u'创业板',300001,300350)'''
        self.log.close()
        self.db.close()
        print 'tonghuashun done!'

