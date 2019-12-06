#!/usr/bin/python
import pymongo
import subprocess
import time
from datetime import timedelta, date, datetime
import os
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%dT %H:%M:%S',
                    #filename='../../log/realTime_{:%Y-%m-%d}.log'.format(datetime.now()))
                    filename='/python/log/realTime_{:%Y-%m-%d}.log'.format(datetime.now()))

stockList = ["01|02","20","03","21","12","04|18|14","28","05|22","06|08|09","10|11|15","25|24","31|27","26|29","39|23|16|17","00"]
#stockList = ["01"]
cmd = 'python3 /python/stock/app/stock.py TWSE "{}"'
#cmd = 'python ./stock.py TWSE "{}"'
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
logging.debug("Files in '%s': %s" % (cwd, files))

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
        p[i].poll()
        logging.info(str(i) + " code(" + str(p[i].pid) + ")=" + str(p[i].returncode))
        if p[i].returncode == 0:
            stop = stop - 1
            p[i].kill
        elif p[i].returncode == None:
            #p[i].poll()
            None
        elif p[i].returncode != 0:
            p[i].kill
            p[i] = subprocess.Popen(cmd.format(stockList[i]), shell=True)
            
    time.sleep(10)
    logging.info(stop)
    """
    if stop == 0:
        for i in range(len(stockList)):
            fp[i].close()
    """        
