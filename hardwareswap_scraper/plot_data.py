import os
from datetime import datetime
import time
import numpy as np
import matplotlib.pyplot as plt

avg_over = 25
fnames = [x for x in os.listdir() if ("valid_prices" in x) and (x[0] != ".")]
print(fnames)
#fnames = ["2080_valid_prices.csv"]

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    ret[n-1:] = ret[n - 1:] / n
    
    count = np.arange(1,n,1)
    ret[:n-1] = ret[:n-1]/count
    

    return ret

outdata = {}

for fname in fnames:
    id = fname[:4]
    with open(fname,'r') as f:
        data = f.readlines()
    if len(data) <=1:
        continue
    outdata[id] = np.zeros((2,len(data)-1),dtype=np.float32)
    for idx,line in enumerate(data):
        if idx == 0:
            continue
        l = line.split(",")
        if "ti" not in l[1].lower():
            continue
        year = int(l[4])
        month = int(l[5])
        day = int(l[6])
        hour = int(l[7])
        minute = int(l[8])
        dt = datetime.strptime("{}-{}-{}-{}-{}".format(year,month,day,hour,minute),"%Y-%m-%d-%H-%M")
        t = time.mktime(dt.timetuple())
        price = float(int(l[2]))

        outdata[id][0,idx-1] = t
        outdata[id][1,idx-1] = price
    outdata[id] = outdata[id][:,np.argsort(outdata[id][0,:])]
    locs = np.where(outdata[id] >0.)
    outdata[id] = outdata[id][:,locs[1][0]:]
    avg_over_instance = min(avg_over,int(outdata[id][0,:].shape[0]/4))
    outdata[id][1,:] = moving_average(outdata[id][1,:],n=avg_over_instance)

    print(outdata[id][0,:10])
    label = fname[:fname.find("_")]
    plt.plot(outdata[id][0,1:],outdata[id][1,1:],label=label)
plt.legend()
plt.show()

        

    