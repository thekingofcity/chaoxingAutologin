import sys
import os
from ctypes import *
import time
import subprocess
import requests

YDMApi = windll.LoadLibrary('yundamaAPI-x64')
appId = 3510   # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
appKey = b'7281f8452aa559cdad6673684aa8f575'     # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
YDMusername = b''
YDMpassword = b''

username = ''# Should only contain 9 numbers
password = ''

def code_verificate(path):
    # 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
    codetype = 1004
    # 分配30个字节存放识别结果
    result = c_char_p(b"                              ")
    # 识别超时时间 单位：秒
    timeout = 60
    # 验证码文件路径
    filename = path
    # 一键识别函数，无需调用 YDM_SetAppInfo 和 YDM_Login，适合脚本调用
    captchaId = YDMApi.YDM_EasyDecodeByPath(YDMusername, YDMpassword, appId, appKey, filename, codetype, timeout, result)
    # print("一键识别：验证码ID：%d，识别结果：%s" % (captchaId, result.value))
    return result.value

def login(path):
    loginSession = requests.Session()
    login_index = loginSession.get('https://passport2.chaoxing.com/login?fid=243&refer=http://i.mooc.chaoxing.com')
    # print(loginSession.cookies['JSESSIONID'])
    # print(loginSession.cookies['route'])
    code_url = 'https://passport2.chaoxing.com/num/code?' + str(int(time.time()))
    code = loginSession.get(code_url)
    with open('code.jpg', 'wb') as file:
        file.write(code.content)
    code_var = code_verificate(b'code.jpg')
    numcode = str(code_var)
    numcode = numcode[2:6]
    headers={
        "Host":"passport2.chaoxing.com",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language":"en-US,en;q=0.5",
        "Referer":"https://passport2.chaoxing.com/login?fid=243&refer=http://i.mooc.chaoxing.com",
        "Content-Type":"application/x-www-form-urlencoded",
        "Cookie":"fid=243; checkbrower=1; ptrmooc=t; JSESSIONID="+loginSession.cookies['JSESSIONID']+"; route="+loginSession.cookies['route'],
        "Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1"
    }
    formData = 'allowJoin=0&f=0&fid=243&fidName=%E4%B8%9C%E5%8D%8E%E5%A4%A7%E5%AD%A6&isCheckNumCode=1&numcode=' +\
        numcode + '&password='+password+'&pid=-1&pidName=&productid=&refer_0x001=http%253A%252F%252Fi.mooc.chaoxing.com'+\
        '&uname='+username+'&verCode='
    # main = requests.post("https://passport2.chaoxing.com/login?refer=http://i.mooc.chaoxing.com",data=formData,headers=headers)
    # print(main.status_code)
    # Should get 302 but always get 200
    # curl in the following works
    curl = path + 'curl "https://passport2.chaoxing.com/login?refer=http"%"3A"%"2F"%"2Fi.mooc.chaoxing.com" -H '+\
        '"Host: passport2.chaoxing.com" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) '+\
        'Gecko/20100101 Firefox/57.0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" '+\
        '-H "Accept-Language: en-US,en;q=0.5" --compressed -H "Referer: '+\
        'https://passport2.chaoxing.com/login?fid=243&refer=http://i.mooc.chaoxing.com" -H "Content-Type: '+\
        'application/x-www-form-urlencoded" -H "Cookie: fid=243; checkbrower=1; ptrmooc=t; JSESSIONID=' +\
        loginSession.cookies['JSESSIONID']  + '; route=' + loginSession.cookies['route'] +\
         '" -H "Connection: keep-alive" -H "Upgrade-Insecure-Requests: 1" --data "'+formData +'" -w %{http_code}'
    # Tips for further operation
    # When replace " -w %{http_code} " in the end of curl with " -D <file> " e.g. headers.txt
    # all the cookies resposed from server were saved
    # then use -c, --cookie-jar to read or manipulate them
    print(curl)
    ret = subprocess.Popen(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sout = ret.stdout.readlines()
    return str(sout[0])

def main():
    i = 0
    count = 200
    print('将要执行'+str(count)+'次')
    while i<=count:
        print(login(os.getcwd()+'\\AMD64\\')+'   最终阶段执行中'+str(i/count)+'%')
        i += 1
    

if __name__ == '__main__':
    main()
