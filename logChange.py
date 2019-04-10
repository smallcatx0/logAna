import re
import time

class logChange:
    """单条日志提取转化
    """
    info = {} # 日志记录信息
    items = {} # 日志内容

    def anaHead(self,head):
        '''解析请求头
        '''
        info = {}
        headinfo = head
        # 拆解数据
        recpTime = re.compile(r'\[([0-9A-Z:\+\- ]+)\]')
        timestr = recpTime.search(headinfo).group(1).strip()
        times = timestr.split('+')[0]
        info['timestamp'] = time.mktime(time.strptime(times,"%Y-%m-%dT%H:%M:%S"))
        headinfo = recpTime.sub('',headinfo).strip()
        headinfos = headinfo.split(" ")
        info['ip'] = headinfos[0]
        info['method'] = headinfos[1]
        info['url'] = headinfos[2]
        info['source'] = head
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
            recpType =re.compile(r'\[[ \w]+\]')
            tmp['type'] = recpType.findall(one)
            remain = recpType.sub('',one).strip()
            recpTime = re.compile(r'\[.+Time:(.+)\]')
            tmp['time'] = recpTime.search(remain).group(1)
            tmp['con'] = recpTime.sub('',remain).strip()
            tmp['source'] = one
            items.append(tmp)
        self.items = items
        return (info,items)



if __name__ == "__main__":
    item = """[ 2019-04-08T17:39:02+08:00 ] 0.0.0.0 POST /budget/index.php/ware/index/submenu.html
[ sql ] [ DB ] CONNECT:[ UseTime:0.011009s ] mysql:host=192.168.2.194;dbname=budget;charset=utf8
[ sql ] [ SQL ] SHOW COLUMNS FROM `role` [ RunTime:0.026351s ]
[ sql ] [ SQL ] SELECT * FROM `role` WHERE  `id` = 10 LIMIT 1 [ RunTime:0.024732s ]
[ sql ] [ SQL ] SHOW COLUMNS FROM `auth` [ RunTime:0.012872s ]
[ sql ] [ SQL ] SELECT id,auth_pid, auth_name, auth_name as text,  auth_a, auth_c, if(auth_a is null or auth_a = '', 'closed', 'open') as state FROM `auth` WHERE  (   id in(1,5,8,19,21,24) and auth_pid=1 ) [ RunTime:0.015085s ]
"""
    lc = logChange()
    res = lc.anaItem(item)
    print(res)
