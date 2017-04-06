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
fig.text(0.5, 0.04, r"Time (ns)", ha='center', va='center') 
fig.text(0.08, 0.50, r"$\frac{d}{dt}\left < \Delta_a G \right > (\rm{kJ/mol})$", ha='center', va='center', rotation='vertical') 

for index,molec in enumerate(molecList ) : 
    fileNameA="../A_State/%s/6_NEARBY_WAT_ENERGIES/dG_xter_CRO.dat"%molec
    fileNameB="../B_State/%s/6_NEARBY_WAT_ENERGIES/dG_xter_CRB.dat"%molec
    print fileNameA,fileNameB

    if os.path.isfile("%s/%s"%(dirName,fileNameA) ): 
        print "%s data file found"%molec 
    else : 
        print "%s NOT FOUND!"%molec
        continue 

    dataA= np.genfromtxt("%s/%s"%(dirName,fileNameA) ) 
    dataB= np.genfromtxt("%s/%s"%(dirName,fileNameB) ) 
    
    dataA, dataB = dataA[:,1], dataB[:,1] 

    time = np.arange(0,50,50.0/len(dataA)) 
    print len(dataA) 

    firstDA, firstDB, rolAvgA, rolAvgB = [] , [] , [] , [] 
    firstDA.append(0) 
    firstDB.append(0) 

    for i in range(len(dataA) ) : 
        rolAvgA.append(np.average(dataA[:i] ) ) 
        rolAvgB.append(np.average(dataB[:i] ) ) 
    for i in range(len(rolAvgA)-1) :
        firstDA.append(rolAvgA[i+1]-rolAvgA[i])      
        firstDB.append(rolAvgB[i+1]-rolAvgB[i])      

    ax = axarr[index/7, index%7] 
    ax.plot(time,firstDA,color='b',label='A')
    ax.plot(time,firstDB,color='g',label='B')

    ax.set_xlim([0,50]) 
    ax.set_ylim([-1.5,1.5]) 
    ax.set_title("%s"%molec) 

    if not index%7 == 0 : 
        xticks = ax.xaxis.get_major_ticks() 
        xticks[0].label1.set_visible(False) 


plt.legend(loc='center left', bbox_to_anchor=(1, 1.75))

plt.savefig("%s/ddG_firstDerivative.pdf"%dirName,format='pdf') 





