import matplotlib.pyplot as plt 
import numpy as np 
import glob as glob 
from scipy.stats import linregress

pKaNames = np.genfromtxt('pKas/pKa.dat',skip_header=1,usecols=0,dtype='str') 
pKaDistro= np.genfromtxt('pKas/pKa.dat',skip_header=1,usecols=2) 

stds = [] 
for index, name in enumerate(pKaNames) : 
    try : 
        dataA = np.genfromtxt("A_State/%s/HBond/cro_num.xvg"%name,skip_header=23) 
        dataB = np.genfromtxt("B_State/%s/HBond/cro_num.xvg"%name,skip_header=23) 
    except : 
        print "File load for %s failed!"%name 
        continue 
    avgA,avgB = np.average(dataA[:,1]), np.average(dataB[:,1]) 
    stdA, stdB = np.std(dataA[:,1]), np.std(dataB[:,1]) 
    print stdA

    plt.scatter(stdA, pKaDistro[index]) 
#    plt.scatter(stdB, pKaDistro[index]) 


plt.show() 

print np.average(pKaDistro) 
print np.std(pKaDistro) 
