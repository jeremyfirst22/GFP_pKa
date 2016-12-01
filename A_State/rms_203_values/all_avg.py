import glob as glob 
import numpy as np 

dataFiles = glob.glob('*.xvg') 

with open('all_avg.dat','w') as f :
    f.write("%-25s\t%10s\n"%("MOLEC","AVERAGE") ) 
for molec in dataFiles : 
    data=np.genfromtxt(molec,skip_header=16)
    avg = np.average(data[:,1]) 
    with open('all_avg.dat','a') as f : 
        f.write("%-25s\t%10f\n"%(molec,avg) ) 


