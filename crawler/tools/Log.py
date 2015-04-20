#!/bin/python
#coding=utf-8
import os
import time
class Log(object):
    logpath=r'D:\WorkSpace\python\StockPrediction\Log'+"\\"
    def __init__(self,logpath=None):
        if logpath!=None:
            self.logpath=logpath
        if os.path.exists(self.logpath)==False:
            os.makedirs(self.logpath)
        self.frun=open(self.logpath+'run_log.txt','a+')
        self.ferror=open(self.logpath+'error_log.txt','a+')
        self.fdataError=open(self.logpath+'database_error_log.txt','a+')
        return
    def runLog(self,content):
        self.frun.write(content+'\n')
    def errorLog(self,content):
        curtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        self.ferror.write('['+curtime+']'+content+'\n')
    def dataErrorLog(self,content):
        curtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        self.fdataError.write('['+curtime+']'+content+'\n')
    def close(self):
        self.frun.close()
        self.ferror.close()
        self.fdataError.close()
    