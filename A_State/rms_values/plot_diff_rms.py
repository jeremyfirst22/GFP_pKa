#!/usr/bin/env python 

import matplotlib.pyplot as plt 
import numpy as np 
import os.path
from sys import exit 

molecList=[
"CN145_T203C", 
"CN145_T203D",  
"CN145_T203F",
"CN145_T203H",
"CN145_T203N",
"CN145_T203S",
"CN145_T203W",
"CN145_T203Y",
"CN145_WT", 
"CN165_T203C", 
"CN165_T203D",  
"CN165_T203F",
"CN165_T203H",
"CN165_T203N",
"CN165_T203S",
"CN165_T203W",
"CN165_T203Y",
"CN165_WT", 
"GFP_WT_T203C", 
"GFP_WT_T203D",  
"GFP_WT_T203F", 
"GFP_WT_T203H",
"GFP_WT_T203N",
"GFP_WT_T203S",
"GFP_WT_T203W",
"GFP_WT_T203Y",
"GFP_WT" 
]

for molec in molecList : 
    fileNameNew="%s_rms.xvg"%molec
    fileNameOld="old_%s_rms.xvg"%molec

    print "%15s"%molec, 
    if not ( os.path.isfile(fileNameOld) ) : 
        print "No file found!" 
        continue 
    print 

    try : 
        dataOld = np.genfromtxt(fileNameOld, skip_header=16) 
    except :
        print "ERROR: File import failed! %s" %fileNameOld
        continue 

    try : 
        dataNew = np.genfromtxt(fileNameNew, skip_header=16) 
    except :
        print "ERROR: File import failed! %s" %fileNameNew
        continue 
    dataOld[:,0] = dataOld[:,0]/1000
    dataNew[:,0] = dataNew[:,0]/1000

    plt.plot(dataOld[:,0],dataOld[:,1],label="old")
    plt.plot(dataNew[:,0],dataNew[:,1],label="new")  
    plt.legend() 
    plt.xlabel("Time (ns)") 
    plt.ylabel("RMSD (nm)") 
    plt.title("%s"%molec) 

    plt.savefig("%s.pdf"%molec, format='pdf') 
    plt.close() 



