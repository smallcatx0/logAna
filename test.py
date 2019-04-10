import re


# 拆解单条日志

# 转化储存到sqlite


# 从文件中读取日志文本并单条拆解
def fileGetCons(filePath):
    with open(filePath,encoding='utf-8') as fp :
        sginLine = fp.readline()
        content = fp.read()
    cons = content.split(sginLine) # 以第一行进行分割
    return cons

# 解析请求头
def anaHead(head):
    info = {}
    headinfo = head
    # 拆解数据
    info['time'] = re.search(r'\[[0-9A-Z:\+\- ]+\]',headinfo).group()
    headinfo = headinfo.replace(info['time'],'').strip()
    headinfos = headinfo.split(" ")
    info['ip'] = headinfos[0]
    info['method'] = headinfos[1]
    info['url'] = headinfos[2]
    info['source'] = head

    return info

# 解析一条日志数据
def anaItem(itemstr):
    itemList = itemstr.split("\n")
    info = anaHead(itemList[0])
    items = []
    for one in itemList[2:]:
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
    print(info)
    print(items)

if __name__ == '__main__':
    # res = fileGetCons("D:/codeApp/PHPWAMP_IN3/wwwroot/budget/runtime/log/201904/08_sql.log")
    # print(res[3])
    # res = anaHead("[ 2019-04-08T17:39:02+08:00 ] 0.0.0.0 POST /budget/index.php/ware/index/submenu.html")
    # print(res)
    item = """[ 2019-04-08T17:39:02+08:00 ] 0.0.0.0 POST /budget/index.php/ware/index/submenu.html
[ sql ] [ DB ] CONNECT:[ UseTime:0.011009s ] mysql:host=192.168.2.194;dbname=budget;charset=utf8
[ sql ] [ SQL ] SHOW COLUMNS FROM `role` [ RunTime:0.026351s ]
[ sql ] [ SQL ] SELECT * FROM `role` WHERE  `id` = 10 LIMIT 1 [ RunTime:0.024732s ]
[ sql ] [ SQL ] SHOW COLUMNS FROM `auth` [ RunTime:0.012872s ]
[ sql ] [ SQL ] SELECT id,auth_pid, auth_name, auth_name as text,  auth_a, auth_c, if(auth_a is null or auth_a = '', 'closed', 'open') as state FROM `auth` WHERE  (   id in(1,5,8,19,21,24) and auth_pid=1 ) [ RunTime:0.015085s ]
"""
    anaItem(item)
