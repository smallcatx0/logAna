## 基于python的日志分析工具

> 最近项目调优，要分析thinkphp5的日志【sql】在网上找了很久没找到合适的日志查看工具。
>
> 于是，便自己造个轮子。



思路： 将log日志转化sqlite 在进行查询即可



### 日志转化

.log => sqlite 

正则提取日志中的关键信息

```verilog
[ 2019-04-08T17:39:02+08:00 ] 0.0.0.0 POST /budget/index.php/ware/index/submenu.html
[ sql ] [ DB ] CONNECT:[ UseTime:0.011009s ] mysql:host=192.168.2.194;dbname=budget;charset=utf8
[ sql ] [ SQL ] SHOW COLUMNS FROM `role` [ RunTime:0.026351s ]
[ sql ] [ SQL ] SELECT * FROM `role` WHERE  `id` = 10 LIMIT 1 [ RunTime:0.024732s ]
[ sql ] [ SQL ] SHOW COLUMNS FROM `auth` [ RunTime:0.012872s ]
[ sql ] [ SQL ] SELECT id,auth_pid, auth_name, auth_name as text,  auth_a, auth_c, if(auth_a is null or auth_a = '', 'closed', 'open') as state FROM `auth` WHERE  (   id in(1,5,8,19,21,24) and auth_pid=1 ) [ RunTime:0.015085s ]
```



数据库设计（父子表）

log_info

- id
- time
- method
- url
- sorce

log_item

- id
- pid
- type
- con
- use_time

