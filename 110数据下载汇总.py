# -*- coding: UTF-8 -*-

from urllib import request, parse
from urllib.parse import quote
import urllib.parse

import time
import json
#import pyodbc
import random
import sys
import hashlib

from inc import fun
import os

#============================时间到强制结束线程
import threading
import inspect
import ctypes

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

#=============================

def get_htmll(urll, p=0, dataa=None):     #请求页面，这个函数要用线程，长时间不响应就杀死线程，参数5秒有时不起作用
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    try:
        req = request.Request(urll, headers=headers)
        with request.urlopen(req, timeout=120) as resp:
            #htmll=resp.read().decode("GBK","ignore")
            htmll=resp.read().decode("utf-8","replace")
            #with open('aaa.txt', 'a', encoding='utf-8', newline='\r\n') as f:
                #f.write(htmll)
            return htmll
    except Exception as e:
        print(e)
        htmll=""
        with open(f'err.txt', 'a', encoding='utf-8', newline='\r\n') as f:
            f.write(str(p)+"\r\n")
        return htmll


def get_htmll2(urll, p, dataa=None):     #请求页面，这个函数要用线程，长时间不响应就杀死线程，参数5秒有时不起作用
    #headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36'}
    
    #data={"areaSn":"","entType":"02","entName":"","pageIndex":p}
    data={"jjrSel":"","p":p}
    data=urllib.parse.urlencode(data)
    data=bytes(data,'utf-8')
    
    try:
        #req = request.Request(urll, headers=headers)
        req = request.Request(urll, headers=headers, data=data, method="POST")
        with request.urlopen(req, timeout=120) as resp:
            #htmll=resp.read().decode("GBK","ignore")
            htmll=resp.read().decode("utf-8","replace")
            #with open('aaa.txt', 'a', encoding='utf-8', newline='\r\n') as f:
                #f.write(htmll)
            return htmll
    except Exception as e:
        print(e)
        htmll=""
        with open(f'err.txt', 'a', encoding='utf-8', newline='\r\n') as f:
            f.write(str(p)+"\r\n")
        return htmll


if __name__ == "__main__":

    with open('Data\\000_all_data.txt', 'r', encoding='utf-8-sig', newline='\r\n') as f:
        ddd=json.loads(f.read())

    neww=1
    for i in range(1,999999):
        #time.sleep(random.randint(1,1))
        time.sleep(1.2)
        if neww==0:
            break
        neww=0
        url=f"http://www.xinfadi.com.cn/getPriceData.html?limit=500&current={i}&pubDateStartTime=&pubDateEndTime=&prodPcatid=&prodCatid=&prodName="
        print(i)

        try:
            htmll=get_htmll(urll=url,p=i)
            ooo=json.loads(htmll)
            if ooo["list"]!=[]:
                for oo in ooo["list"]:
                    if str(oo["id"]) not in ddd.keys():
                        neww=1
                        ddd[oo["id"]]=[oo["prodName"],oo["prodCatid"],oo["prodCat"]\
                                       ,oo["prodPcatid"],oo["prodPcat"]\
                                       ,oo["lowPrice"],oo["highPrice"]\
                                       ,oo["avgPrice"],oo["place"],oo["specInfo"]\
                                       ,oo["unitInfo"],oo["pubDate"][:10],oo["status"]]
##                with open(f'Data\\{i}_1000.txt', 'w', encoding='utf-8', newline='\r\n') as f:
##                    f.write(json.dumps(ooo, indent=4, ensure_ascii=False)+"\r\n")
            else:
                break
        except:
            print("--Err--")
            
        if int(i)//10==int(i)/10:
            with open(f'Data\\000_all_data.txt', 'w', encoding='utf-8', newline='\r\n') as f:
                f.write(json.dumps(ddd, indent=4, ensure_ascii=False)+"\r\n")

        
    with open(f'Data\\000_all_data.txt', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(json.dumps(ddd, indent=4, ensure_ascii=False)+"\r\n")

    print("--end--")
                
                

