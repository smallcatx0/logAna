import re
import os
import time

class logChange:
    """日志提取转化
    """
    info = {} # 日志记录信息
    items = {} # 日志内容
    dbPath = ''
    initDbSql = ''
    _db = None


    def __init__(self,conf={}):
        import EasySqlite
        self.dbPath = conf['dbPath'] if 'dbPath' in conf else 'log.db'
        self.initDbSql = conf['initDbSql'] if 'initDbSql' in conf else 'initDb.sql'
        self._db = EasySqlite.EasySqlite(self.dbPath)


    def anaHead(self,headstr):
        '''解析日志头部(请求时间，ip，方法，地址)
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
    
    def fileGetCons(self,filePath):
        with open(filePath,encoding='utf-8') as fp :
            sginLine = fp.readline()
            content = fp.read()
        cons = content.split(sginLine) # 以第一行进行分割
        return cons
    
    # 初始化数据库
    def initDb(self,initSqlFile=''):
        initSqlFile = self.initDbSql if initSqlFile.strip() == '' else initSqlFile
        db = self._db
        if(os.path.exists(self.dbPath)):
            self._db = db
            return db
        res = db.execSqlScript(initSqlFile)
        if res:
            db.commit()
        return res

    def saveToDb(self):
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
        print(res)

if __name__ == "__main__":
    logC = logChange()
    logItems = logC.fileGetCons('log/201904/09_sql.log')
    res = logC.anaItem(logItems[3])
    logC.saveToDb()
    # res = logC.initDb()
    print(res[0])
