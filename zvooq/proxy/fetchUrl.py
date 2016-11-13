# coding: UTF-8

#проверка многопоточности: узнаем pid flask приложения, запускаем 
#конкурентные запросы и смотрим, как в рамках своего процесса flask
#создает количество потоков по числу конкурентных запросов
#user@user-VirtualBox:~/workspace/iasbp/default/score$ sudo netstat -nlp | grep :5000
#tcp        0      0 127.0.0.1:5000          0.0.0.0:*               LISTEN      28271/python    
#user@user-VirtualBox:~/workspace/iasbp/default/score$ ps -T -p 28271
#   PID  SPID TTY          TIME CMD
# 28271 28271 pts/20   00:00:00 python
# 28271 28312 pts/20   00:00:00 python
# 28271 28313 pts/20   00:00:00 python
# 28271 28314 pts/20   00:00:00 python
# 28271 28315 pts/20   00:00:00 python
# 28271 28316 pts/20   00:00:00 python
# 28271 28317 pts/20   00:00:00 python
# 28271 28318 pts/20   00:00:00 python
# 28271 28319 pts/20   00:00:00 python
# 28271 28320 pts/20   00:00:00 python

import urllib2
from random import choice
from string import digits
from multiprocessing.pool import ThreadPool

urls = []
for i in range(9):
    urls.append('http://localhost:5000/from_cache?key=%s' % (''.join(choice(digits) for i in range(5))))
    
def fetch_url(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()

results = ThreadPool(20).imap_unordered(fetch_url, urls)

for res in results:
    print res