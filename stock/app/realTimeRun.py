#!/usr/bin/python
import pymongo
import subprocess
import time
from datetime import timedelta, date, datetime
import os
import logging

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%dT %H:%M:%S',
                    filename='../../log/realTime_{:%Y-%m-%d}.log'.format(datetime.now()))

stockList = ["01|02","20","03","21","12","04|18|14","28","05|22","06|08|09","10|11|15","25|24","31|27","26|29","39|23|16|17","00"]

cmd = 'python3 ./stock.py TWSE "{}"'
#cmd = 'python ./stock.py TWSE "{}"'
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
logging.error("Files in '%s': %s" % (cwd, files))

def runCom(L):
    return subprocess.Popen(cmd.format(L), shell=True)
p = list( map(runCom, stockList)) 

def logW(L):
    return open("/python/log/stock{}.log".format(L.replace("|","_"),"a+"))
#fp = list( map(logW, stockList))

stop = len(stockList)

while stop > 0:
    for i in range(len(stockList)):
        #fp[i].write(p[i].stdout.readline())
        logging.error(str(i) + " code(" + str(p[i].pid) + ")=" + str(p[i].returncode))
        p[i].poll()
        if p[i].returncode == 0:
            stop = stop - 1
            p[i].kill
        elif p[i].returncode == None:
            p[i].poll()
        elif p[i].returncode != 0:
            p[i].kill
            p[i] = subprocess.Popen(cmd.format(stockList[i]), shell=True)
            
    time.sleep(10)
    logging.error(stop)
    """
    if stop == 0:
        for i in range(len(stockList)):
            fp[i].close()
    """        
