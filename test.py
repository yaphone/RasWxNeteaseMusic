from myapi import MyNetease

netease = MyNetease()
print netease.login("zhouyaphone@163.com", "a123456")
#coding=utf-8
import sys
from subprocess import PIPE, Popen
from threading  import Thread

mp3_url = "http://m2.music.126.net/DeRuZvVpYsqCHMngfISnwQ==/18724683022792919.mp3"

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

p = Popen("omxplayer " + mp3_url, shell=True, stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True # thread dies with the program
t.start()

# ... do other things here

# read line without blocking
try:
    #line = q.get_nowait() # or q.get(timeout=.1)
    line = q.get(timeout=3)
except Empty:
    print('no output yet')
else: # got line
    if "nice" in line:
        print "*******OK*******"
