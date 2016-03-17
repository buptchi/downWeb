#!/usr/bin/python
# -*-coding:utf-8-*-

import urllib
import re
import os
import fileinput
import time
import threading
import argparse


def downweb(main_url, pre_path):
    print "backup start    " + time.strftime('%H %M %S', time.localtime())

    backup_time = time.strftime('%Y%m%d%H%M', time.localtime())
    prefix_path = '.' + pre_path + '/' + backup_time
    img_path = prefix_path + '/images/'
    css_path = prefix_path + '/css/'
    js_path = prefix_path + '/js/'
    html = prefix_path + '/index.html'

    if not os.path.exists(prefix_path):
        os.makedirs(img_path)
        os.makedirs(css_path)
        os.makedirs(js_path)
    else:
        print "This minute already backs up. So skip   " + time.strftime('%H %M %S', time.localtime())
        return

    try:
        urllib.urlretrieve(main_url, html)
    except IOError, e:
        print e
        return

    for line in fileinput.input(html, inplace=1):
        img_result1 = re.search(r'<img src="(.*)" alt=', line)
        if img_result1:
            img_url = img_result1.group(1)
            img_name = img_url.split('/')[-1]
            try:
                urllib.urlretrieve(img_url, img_path+img_name)
            except IOError, e:
                print e
            print re.sub(r'http.*" alt', './images/'+img_name+'" alt', line),
            continue
        img_result2 = re.search(r'<img src="(.*)" original="(.*)" width', line)
        if img_result2:
            img_url = img_result2.group(2)
            img_name = img_url.split('/')[-1]
            try:
                urllib.urlretrieve(img_url, img_path+img_name)
            except IOError, e:
                print e
            print re.sub(r'http.*" original', './images/'+img_name+'" original', line),
            continue
        css_result = re.search(r'<link rel="stylesheet" type="text/css" href="(.*)" media', line)
        if css_result:
            css_url = css_result.group(1)
            css_name = css_url.split('/')[-1]
            try:
                urllib.urlretrieve(css_url, css_path+css_name)
            except IOError, e:
                print e
            print re.sub(r'http.*" media', './css/'+css_name+'" media', line),
            continue
        js_result = re.search(r'<script type="text/javascript" src="(.*)"></script>', line)
        if js_result:
            js_url = js_result.group(1)
            js_name = js_url.split('/')[-1]
            try:
                urllib.urlretrieve(js_url, js_path+js_name)
            except IOError, e:
                print e
            print re.sub(r'http.*"><', './js/'+js_name+'"><', line),
            continue
        print line,

    fileinput.close()

    print "backup end      " + time.strftime('%H %M %S', time.localtime())


def runbackup():
    global t
    t = threading.Timer(interval, runbackup)
    t.start()
    downweb(main_url, pre_path)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="back up interval second", type=int, default=60)
    parser.add_argument("-u", help="main url", default="http://m.sohu.com")
    parser.add_argument("-o", help="back up destination path, such as /tmp/backup", default="/tmp/backup")
    args = parser.parse_args()
    interval = args.d
    main_url = args.u
    pre_path = args.o

    if interval < 60:
        print u"备份时间小于60s, 下面按60s间隔备份"
        interval = 60
    if pre_path[-1] == '/':             #如果输入的目录后缀有"/"，则将其去掉，统一格式
        pre_path = pre_path[0:len(pre_path)-1]
    url_result = re.search(r'http://.*', main_url)
    if not url_result:
        print u"链接输入错误"
    else:
        print u"run back up"
        t = threading.Timer(interval, runbackup)
        t.start()
        downweb(main_url, pre_path)

