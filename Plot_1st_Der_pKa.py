import matplotlib.pyplot as plt 
import numpy as np 
import glob as glob 
import os.path
from sys import exit

from matplotlib import rc_file

dirName='pKas'

if not os.path.isdir(dirName) : 
    print "%s directory not found. exitting"%dirName
    exit() 

molecList=[
"CN145_T203C", "CN145_T203F", "CN145_T203H", "CN145_T203N", "CN145_T203S", "CN145_WT", "CN145_T203Y",
"CN165_T203C", "CN165_T203F", "CN165_T203H", "CN165_T203N", "CN165_T203S", "CN165_WT", "CN165_T203Y",
"GFP_WT_T203C", "GFP_WT_T203F", "GFP_WT_T203H", "GFP_WT_T203N", "GFP_WT_T203S", "GFP_WT", "GFP_WT_T203Y"] 


#rc_file('firstDer_rc.rc') 

fig, axarr = plt.subplots(3,7,sharex='col',sharey='row') 
fig.set_figheight(8) 
fig.set_figwidth(15) 
fig.subplots_adjust(wspace=0) 
fig.text(0.5, 0.04, "Time (ns)", ha='center', va='center') 
fig.text(0.08, 0.50, "$\\frac{d}{dt}$pK$_a$ (ns$^{-1}$)", ha='center', va='center', rotation='vertical') 

for index,molec in enumerate(molecList ) : 
    fileName="%s_ddG_pKa.dat"%molec 
    print fileName

    if os.path.isfile("%s/%s"%(dirName,fileName) ): 
        print "%s data file found"%molec 
    else : 
        print "%s NOT FOUND!"%molec
        continue 

    data = np.genfromtxt("%s/%s"%(dirName,fileName) ) 

    time = np.arange(0,50,50.0/len(data)) 
    print len(data) 

    firstD, rolAvg = [] , [] 
    firstD.append(0) 

    for i in range(len(data[:,1])) :
        rolAvg.append(np.average(data[:i,1]) ) 
    for i in range(len(rolAvg)-1) :
        firstD.append(rolAvg[i+1]-rolAvg[i])      

    ax = axarr[index/7, index%7] 
    ax.plot(time,firstD)

    ax.set_xlim([0,50]) 
    ax.set_ylim([-1.5,1.5]) 
    ax.set_title("%s"%molec) 

    xticks = ax.xaxis.get_major_ticks() 
    xticks[0].label1.set_visible(False) 
    ax.set_xticks(np.arange(0,51,10))

plt.setp([a.get_xticklabels() for a in axarr[0,:]], visible=False) 
plt.setp([a.get_yticklabels() for a in axarr[:,1]], visible=False) 
plt.savefig('pKas/firstDerivative.pdf',format='pdf') 





