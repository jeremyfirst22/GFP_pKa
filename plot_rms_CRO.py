#! /usr/bin/env python 

import glob as glob 
import matplotlib.pyplot as plt 
import numpy as np 
from sys import exit

datafiles = glob.glob('?_State/rms_CR?_values/*.xvg') 

for molec in datafiles : 
    if 'T203B' in molec : datafiles.remove(molec) ; continue 
    if 'T203D' in molec : datafiles.remove(molec) ; continue 
    if 'T203W' in molec : datafiles.remove(molec) ; continue 
    if 'T203X' in molec : datafiles.remove(molec) ; continue 
    if 'T203Z' in molec : datafiles.remove(molec) ; continue 

names = [] 
avgA, avgB = [], [] 
stdA, stdB = [], [] 
for index in range(len(datafiles)/2)  : 
    name = datafiles[index].split('/')[2][:-12]
    names.append(name) 
    try : 
        dataA = np.genfromtxt(datafiles[index], skip_header=16) 
        dataB = np.genfromtxt(datafiles[index+len(datafiles)/2], skip_header=16) 
    except : 
        continue

    avgA.append(np.average(dataA[:,1]) ) 
    avgB.append(np.average(dataB[:,1]) ) 

    stdA.append(np.std(dataA[:,1]) ) 
    stdB.append(np.std(dataB[:,1]) ) 

for index, pnt in enumerate(avgA) : 
    plt.errorbar(index,avgA[index], yerr=stdA[index],marker='o') 
    plt.errorbar(index,avgB[index], yerr=stdB[index],marker='D') 

plt.show() 
plt.close() 

f,axarr = plt.subplots(3,6,sharex='col',sharey='row') 

for index in range(len(datafiles)/2)  : 
    ax = axarr[index/6,index%6] 

    dataA = np.genfromtxt(datafiles[index], skip_header=16) 
    dataB = np.genfromtxt(datafiles[index+len(datafiles)/2], skip_header=16) 

    ax.plot(dataA[:,1],'r-')
    ax.plot(dataB[:,1],'b-')

    ax.set_title(names[index]) 

plt.show() 
    

