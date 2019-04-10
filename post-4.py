import urllib.request
import urllib.parse
import json

post_url = 'https://fanyi.baidu.com/v2transapi'
word= 'wolf'
formdata = {
    'from':	'en',
    'to':	'zh',
    'query':word,
    'transtype'	:'realtime',
    'simple_means_flag':	'3',
    'sign':	'275695.55262',
    'token':'2b63cc3e3cf3f70d00950e8288863805',
}
headers= {
    'Host': 'fanyi.baidu.com',
    'Connection': 'keep-alive',
    'Content-Length': '120',
    'Accept': '*/*',
    'Origin': 'https://fanyi.baidu.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'https://fanyi.baidu.com/?aldtype=16047',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 
    'Cookie': 'BIDUPSID=1CFE3235A890AFF063223A6560D043F9; PSTM=1542082709; BAIDUID=B4941C68B4144C62397EE207A48688E5:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; delPer=0; PSINO=1; H_PS_PSSID=1465_21093_28775_28723_28557_28839_28584_28603_28606; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1554691233,1554692384,1554775194; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1554775194',
}
request = urllib.request.Request(url=post_url,headers=headers)
formdata = urllib.parse.urlencode(formdata).encode()
response = urllib.request.urlopen(request,formdata)
con = response.read().decode()
res = json.loads(con)
print(res)