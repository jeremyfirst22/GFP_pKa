import glob as glob 

import matplotlib.pyplot as plt 
import numpy as np 

print "\t\t*** Andrews HBond***\n" 

datafiles = glob.glob('?_State/*/HBond_nit/*.frame_hb.xvg') 
datafiles = sorted(datafiles) 

halfWay = np.size(datafiles) / 2
avgs, stds = [], [] 
for index, file in enumerate(datafiles ): 
    data = np.genfromtxt(file, skip_header=23) 
    avg = np.average(data[:,2]) 
    std = np.std(data[:,2]) 

    plt.errorbar(index%halfWay, avg, yerr=std,marker='D') 
    print "%10s\t%10s\t%5f\t%5f"%(file.split('/')[0],file.split('/')[1],avg,std)  

plt.show() 
plt.close() 


print "\t\t*** GMX HBond ***\n" 

datafiles = glob.glob('?_State/*/HBond/cnf_num.xvg') 
datafiles = sorted(datafiles) 

halfWay = np.size(datafiles) / 2
avgs, stds = [], [] 
for index, file in enumerate(datafiles ): 
    data = np.genfromtxt(file, skip_header=23) 
    avg = np.average(data[:,1]) 
    std = np.std(data[:,1]) 

    plt.errorbar(index%halfWay, avg, yerr=std,marker='D') 
    print "%10s\t%10s\t%5f\t%5f"%(file.split('/')[0],file.split('/')[1],avg,std)  

plt.show() 
plt.close() 
