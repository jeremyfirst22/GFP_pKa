#!/usr/bin/env python 

import matplotlib.pyplot as plt 
import numpy as np 
import os.path
from sys import exit 


molecList=[
"CN145_T203C", 
#"CN145_T203D",  
"CN145_T203F",
"CN145_T203H",
"CN145_T203N",
"CN145_T203S",
#"CN145_T203W",
"CN145_T203Y",
"CN145_WT", 
"CN165_T203C", 
#"CN165_T203D",  
"CN165_T203F",
"CN165_T203H",
"CN165_T203N",
"CN165_T203S",
#"CN165_T203W",
"CN165_T203Y",
"CN165_WT", 
"GFP_WT_T203C", 
#"GFP_WT_T203D",  
"GFP_WT_T203F", 
"GFP_WT_T203H",
"GFP_WT_T203N",
"GFP_WT_T203S",
#"GFP_WT_T203W",
"GFP_WT_T203Y",
"GFP_WT" 
]


f, axarr = plt.subplots(3,7,sharex='col', sharey='row') 
f.set_figheight(8) 
f.set_figwidth(15) 
f.subplots_adjust(wspace=0) 
f.text(0.5, 0.04, "Time (ns)", ha='center', va='center') 
f.text(0.08, 0.50, 'RMSD (nm)', ha='center', va='center', rotation='vertical') 

#index=0

index=0
for molec in molecList: 
    print "%5i%15s"%(index,molec) , 

    fileNameNew="%s_rms.xvg"%molec
    fileNameOld="old_%s_rms.xvg"%molec


    ax = axarr[index/7, index%7] 
#    try : 
#        dataOld = np.genfromtxt(fileNameOld, skip_header=16) 
#        dataOld[:,0] = dataOld[:,0]/1000 
#        ax.plot(dataOld[:,0],dataOld[:,1], color='b') 
#        ax.set_xlim([0,50]) 
#        ax.set_ylim([0,0.6 ])
#        ax.set_title("%s"%molec) 
#
#        xticks = ax.xaxis.get_major_ticks()
#        xticks[0].label1.set_visible(False)
#        #xticks[-1].label1.set_visible(False)
#        print "OLD, success", 
#    except :
#        print "OLD, SKIPPED" 
#        continue 

    try : 
        dataNew = np.genfromtxt(fileNameNew, skip_header=16) 
        dataNew[:,0] = dataNew[:,0]/1000 
        ax.plot(dataNew[:,0],dataNew[:,1], color='g') 
        ax.set_xlim([0,50]) 
        ax.set_ylim([0,0.34])
        ax.set_title("%s"%molec) 

        xticks = ax.xaxis.get_major_ticks()
        xticks[0].label1.set_visible(False)
        #xticks[-1].label1.set_visible(False)
        print "NEW, success", 
    except :
        print "NEW, SKIPPED", 
        continue 


    print 
    index+=1

plt.setp([a.get_xticklabels() for a in axarr[0,:]], visible=False) 
plt.setp([a.get_yticklabels() for a in axarr[:,1]], visible=False) 
plt.savefig('all_new_rms.png', format='png') 
