import glob 
import numpy as np 
import matplotlib.pyplot as plt 
from sys import exit 
import os 
from scipy.stats import linregress

from matplotlib import rc_file 

rmsd_dir='rmsd'

molList=[
'GFP_WT',
'GFP_WT_T203C',
'GFP_WT_T203F',
'GFP_WT_T203H',
'GFP_WT_T203N',
'GFP_WT_T203S',
'GFP_WT_T203Y',
'CN145_WT',
'CN145_T203C',
'CN145_T203F',
'CN145_T203H',
'CN145_T203N',
'CN145_T203S',
'CN145_T203Y',
'CN165_WT',
'CN165_T203C',
'CN165_T203F',
'CN165_T203H',
'CN165_T203N',
'CN165_T203S',
'CN165_T203Y']

if not os.path.isdir('rmsd_plots') : 
    os.mkdir('rmsd_plots') 

for state in 'A_State','B_State' : 

    f, axarr = plt.subplots(3,7,sharex='col',sharey='row') 
    f.set_figheight(8) 
    f.set_figwidth(15) 
    f.subplots_adjust(wspace=0) 
    f.text(0.5, 0.04, "Time (ns)", ha='center', va='center') 
    f.text(0.08, 0.50, r"RMSD ($\AA$)", ha='center', va='center', rotation='vertical') 

    for index, molec in enumerate(molList) : 
        ax = axarr[index/7,index%7]
        data_file = "%s/%s/%s/%s.crystal.xvg"%(state,molec, rmsd_dir, molec)  
        try : 
            data = np.genfromtxt(data_file,skip_header=16) 
            data[:,0] = data[:,0] / 1000  ## ps -> ns 
            data[:,1] = data[:,1] * 10 ## nm -> Ang
            
            ax.plot(data[:,0],data[:,1]) 
            ax.set_xlim([0,50]) 
            ax.set_ylim([0,2.5])  
            ax.set_title("%s"%molec) 
            print "%s\tSuccess!"%molec
        except : 
            print "%s\tFailed!"%molec
            continue 
    
    plt.savefig("rmsd_plots/%s_rmsd.png"%state,format='png') 
    plt.close() 
