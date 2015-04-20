#!/bin/python
#coding=utf-8
import sqlite3
from Log import *
class Database(object):
    def __init__(self,databasePath):
        self.log=Log()
        self.index_info='index_info'
        self.index_daily='index_daily'
        self.stock_info='stock_info'
        self.stock_daily='stock_daily'
        self.stock_daily_hu='stock_daily_hu'
        self.stock_daily_shen='stock_daily_shen'
        self.stock_daily_chuang='stock_daily_chuang'
        self.bankuai_info='bankuai_info'
        try:
            self.sqlConn=sqlite3.connect(databasePath)
            self.sqlConn.isolation_level=None #不需要每句都commit
            self.cur=self.sqlConn.cursor()
            self.createTables()
        except sqlite3.Error,e:
            strError='连接数据库失败:'+e.args[0]
            self.log.dataErrorLog(strError)
            return None
    def createTables(self):
        #股票id名称映射
        sqlCreate='create table if not exists '+self.stock_info+'(id integer primary key autoincrement, \
                    stock_id TEXT,name TEXT,bankuai text,hangye text)'
        self.cur.execute(sqlCreate)
        #所有股票每日信息
        sqlCreate='create table if not exists '+self.stock_daily+'(id integer primary key autoincrement, \
                    stock_id TEXT,trade_date date,kaipan numeric, shoupan numeric, \
                    zuigao numeric,zuidi numeric,cjl TEXT)'
        self.cur.execute(sqlCreate)
        #沪市股票每日信息
        sqlCreate='create table if not exists '+self.stock_daily_hu+'(id integer primary key autoincrement, \
                    stock_id TEXT,trade_date date,kaipan numeric, shoupan numeric, \
                    zuigao numeric,zuidi numeric,cjl TEXT)'
        self.cur.execute(sqlCreate)
        #深市股票每日信息
        sqlCreate='create table if not exists '+self.stock_daily_shen+'(id integer primary key autoincrement, \
                    stock_id TEXT,trade_date date,kaipan numeric, shoupan numeric, \
                    zuigao numeric,zuidi numeric,cjl TEXT)'
        self.cur.execute(sqlCreate)
        #创业板股票每日信息
        sqlCreate='create table if not exists '+self.stock_daily_chuang+'(id integer primary key autoincrement, \
                    stock_id TEXT,trade_date date,kaipan numeric, shoupan numeric, \
                    zuigao numeric,zuidi numeric,cjl TEXT)'
        self.cur.execute(sqlCreate)
        #指数信息
        sqlCreate='create table if not exists '+self.index_info+'(id integer primary key autoincrement, \
                   index_id TEXT,name TEXT)'
        self.cur.execute(sqlCreate)
        #指数每日信息
        sqlCreate='create table if not exists '+self.index_daily+'(id integer primary key autoincrement, \
                   index_id TEXT,name TEXT,trade_date TEXT,value numeric,zde numeric,zdf numeric)'
        self.cur.execute(sqlCreate)
        #板块对应表名信息
        sqlCreate='create table if not exists '+self.bankuai_info+'(id integer primary key autoincrement, \
                   name TEXT,refer_table TEXT)'
        self.cur.execute(sqlCreate)
    def selectStockById(self,stock_id):
        res=[]
        sqlSel='select * from '+self.stock_info+' where stock_id=?'
        try:
            self.cur.execute(sqlSel,[stock_id])
            res=self.cur.fetchall()
        except sqlite3.Error,e:
            strError='查询失败:'+e.args[0]
            self.log.dataErrorLog(strError)
        return res 
    def insertStock(self,stock_id,stock_name,type,hangye):
        sqlIns='insert into '+self.stock_info+'(stock_id,name,bankuai,hangye) values(?,?,?,?)'
        try:
            self.cur.execute(sqlIns,[stock_id,stock_name,type,hangye])
        except sqlite3.Error,e:
            strError='插入表失败:'+e.args[0]
            self.log.dataErrorLog(strError)
    def selectStockDailyByIdDate(self,stock_id,cur_date,table):
        res=[]
        params=[stock_id,cur_date]
        sqlSel='select * from '+table+' where stock_id=? and trade_date=?'
        try:
            self.cur.execute(sqlSel,params)
            res=self.cur.fetchall()
        except sqlite3.Error,e:
            strError='查询失败:'+e.args[0]
            self.log.dataErrorLog(strError)
        return res
    def insertStockDaily(self,arrStock,table):
        sqlIns='insert into '+table+'(stock_id,trade_date,kaipan,shoupan,zuigao,zuidi,cjl) values \
            (?,?,?,?,?,?,?) '
        try:
            self.cur.execute(sqlIns,arrStock)
        except sqlite3.Error,e:
            strError='插入表失败:'+e.args[0]
            self.log.dataErrorLog(strError)
    def selectIndexDailyByIdDate(self,index_id,cur_date):
        res=[]
        params=[index_id,cur_date]
        sqlSel='select * from '+self.index_daily+' where index_id=? and trade_date=?'
        try:
            self.cur.execute(sqlSel,params)
            res=self.cur.fetchall()
        except sqlite3.Error,e:
            strError='查询失败:'+e.args[0]
            self.log.dataErrorLog(strError)
        return res
    def selectBankuaiInfoByName(self,bankuai_name):
        res=[]
        sqlSel='select * from '+self.bankuai_info+' where name=?'
        try:
            self.cur.execute(sqlSel,[bankuai_name])
            res=self.cur.fetchall()
        except sqlite3.Error,e:
            strError='查询失败:'+e.args[0]
            self.log.dataErrorLog(strError)
        return res
    def insertIndexDaily(self,arrIndex):
        sqlIns='insert into '+self.index_daily+'(index_id,trade_date,value,zde,zdf) values \
            (?,?,?,?,?)'
        try:
            self.cur.execute(sqlIns,arrIndex)
        except sqlite3.Error,e:
            strError='插入表失败:'+e.args[0]
            self.log.dataErrorLog(strError)
    def ifAddStock(self,stock):
        if not self.selectStockById(stock[0]):
            self.insertStock(stock[0],stock[4],stock[2],stock[3])
    def refreshStockDaily(self,arrStock):
        self.ifAddStock(arrStock)
        #删除stockname，type和行业
        type=arrStock[2]
        tableInfo=self.selectBankuaiInfoByName(type)
        tableName=tableInfo[0][2]
        del arrStock[2:5]
        if not self.selectStockDailyByIdDate(arrStock[0],arrStock[1],tableName):
            self.insertStockDaily(arrStock,tableName)
    def refreshIndexDaily(self,arrIndex):
        #查询当日是否有数据，没有才插入
        if not self.selectIndexDailyByIdDate(arrIndex[0],arrIndex[1]):
            self.insertIndexDaily(arrIndex)
    def close(self):
        if self.cur is not None:
            self.cur.close()
        if self.sqlConn is not None:
            self.sqlConn.close()
    
        
        