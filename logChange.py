import re
import os
import time

class logChange:
    """日志提取转化  
    @author Tan<smallcatx0@gmail.com>
    """
    info = {} # 日志记录信息
    items = {} # 日志内容
    dbPath = ''
    initDbSql = ''
    _db = None


    def __init__(self,conf={}):
        self.dbPath = conf['dbPath'] if 'dbPath' in conf else 'log.db'
        self.initDbSql = conf['initDbSql'] if 'initDbSql' in conf else 'initDb.sql'

    # 解析日志头部(请求时间，ip，方法，地址)
    def anaHead(self,headstr):
        '''解析日志头部(请求时间，ip，方法，地址)
        
        @param headstr [str] 每条日志的第一行记录
        @return [dict] 解析出的头部信息
        '''
        info = {}
        headinfo = headstr
        # 拆解数据
        recpTime = re.compile(r'\[([0-9A-Z:\+\- ]+)\]')
        timestr = recpTime.search(headinfo).group(1).strip()
        times = timestr.split('+')[0]
        info['time'] = int(time.mktime(time.strptime(times,"%Y-%m-%dT%H:%M:%S")))
        headinfo = recpTime.sub('',headinfo).strip()
        headinfos = headinfo.split(" ")
        info['ip'] = headinfos[0]
        info['method'] = headinfos[1]
        info['url'] = headinfos[2]
        info['source'] = headstr
        self.info = info
        return info

    # 解析一条日志数据
    def anaItem(self,itemstr):
        '''解析一条日志

        @param itemstr [str] 一条日志数据
        '''
        itemList = itemstr.split("\n")
        info = self.anaHead(itemList[0])
        items = []
        for one in itemList[1:]:
            if(one.strip()==''):continue
            tmp = {}
            recpType =re.compile(r'\[([ \w]+)\]')
            types = recpType.findall(one)
            tmp['level'] = types[0].strip()
            tmp['type'] = types[1].strip()
            remain = recpType.sub('',one).strip()
            recpTime = re.compile(r'\[.+Time:(.+)\]')
            tmp['dt'] = recpTime.search(remain).group(1)
            tmp['con'] = recpTime.sub('',remain).strip()
            tmp['source'] = one
            items.append(tmp)
        self.items = items
        return (info,items)

    # 获取日志（切割成单条）
    def fileGetCons(self,filePath):
        '''从文件中获取日志

        @param filePath [str] 日志文件的路径
        @return [list] 日志数据列表
        '''
        with open(filePath,encoding='utf-8') as fp :
            sginLine = fp.readline()
            content = fp.read()
        cons = content.split(sginLine) # 以第一行进行分割
        return cons
    
    # 初始化数据库
    def initDb(self,initSqlFile=''):
        '''初始化数据库

        @param initSqlFile [str] 建表语句所在路径
        '''
        import EasySqlite
        initSqlFile = self.initDbSql if initSqlFile.strip() == '' else initSqlFile
        if(os.path.exists(self.dbPath)):
            self._db = EasySqlite.EasySqlite(self.dbPath)
            return True
        else:
            self._db = EasySqlite.EasySqlite(self.dbPath)
            res = self._db.execSqlScript(initSqlFile)
            if res:
                self._db.commit()
            return res

    # 将解析的一条日志数据存入数据库
    def saveToDb(self):
        '''将解析的一条日志数据存入数据库

        '''
        infoData = self.info
        res = self._db.table('log_info').insert(infoData)
        if res:
            self._db.commit()
            infoId = res
        else :
            print(self._db.errorMsg)
            return False

        itemsData = []
        for one in self.items:
            one['pid'] = infoId
            itemsData.append(one)
        
        res = self._db.table('log_items').insertAll(itemsData)
        self._db.commit()
        return True

    # 将一日志文件转化为sqlite
    def fileConv(self,filePath):
        '''将一日志文件转化为sqlite

        @param filePath [str] 日志文件的路径
        '''
        logList = self.fileGetCons(filePath)
        taskLen = len(logList)
        i = 0
        for one in logList:
            i += 1
            self.anaItem(one) # 解析一条日志
            self.saveToDb() # 存到数据库
            printStr = "[%d/%d] add: %s(%d)" %(i,taskLen,self.info['source'],len(self.items))
            print(printStr)
        return True


if __name__ == "__main__":
    logC = logChange()
    logC.initDb()
    logC.fileConv('log/201904/10_sql.log')
    # logItems = logC.fileGetCons('log/201904/09_sql.log')
    # res = logC.anaItem(logItems[3])
    # logC.saveToDb()
    # res = logC.initDb()
    # print()
