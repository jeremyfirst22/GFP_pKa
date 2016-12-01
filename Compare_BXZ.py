#!/usr/bin/env python 

import numpy as np 
import glob as glob 

print "\n\n\t***** e = 2, Implicit Water*****\n\n" 
fileList = glob.glob('?_State/*_T203[BCHXZ]/FREE_ENERGIES/dG_xter_CR?.dat') 
fileList = sorted(fileList) 

for index in range(len(fileList)/2) :     
    name = fileList[index].split('/')[1]
    if name != fileList[index+len(fileList)/2].split('/')[1] : 
        print "%-15s\tERROR\t%s"%(name,fileList[index+len(fileList)/2].split('/')[1]) 

        continue

    dataA = np.genfromtxt(fileList[index]) 
    dataB = np.genfromtxt(fileList[index+len(fileList)/2]) 

    avgA = np.average(dataA) 
    avgB = np.average(dataB) 

    ddG = avgB - avgA 
    dpKa = ddG / 2.5 / 2.303 
    pKa = dpKa + 8.2 
    print "%-15s\t%5f"%(name, pKa) 


print "\n\n\t***** e = 20, Implicit Water*****\n\n" 
fileList = glob.glob('?_State/*_T203[BCHXZ]/20_FREE_ENERGIES/dG_xter_CR?.dat') 
fileList = sorted(fileList) 

for index in range(len(fileList)/2) :     
    name = fileList[index].split('/')[1]
    if name != fileList[index+len(fileList)/2].split('/')[1] : 
        print "%-15s\tERROR\t%s"%(name,fileList[index+len(fileList)/2].split('/')[1]) 
        continue

    dataA = np.genfromtxt(fileList[index]) 
    dataB = np.genfromtxt(fileList[index+len(fileList)/2]) 

    avgA = np.average(dataA) 
    avgB = np.average(dataB) 

    ddG = avgB - avgA 
    dpKa = ddG / 2.5 / 2.303 
    pKa = dpKa + 8.2 
    print "%-15s\t%5f"%(name, pKa) 

    
print "\n\n\t***** e = 2, 5 A explicit  *****\n\n" 
fileList = glob.glob('?_State/*_T203[BCHXZ]/LOWE_NEARBY_WAT_ENERGIES/dG_xter_CR?.dat') 
fileList = sorted(fileList) 

for index in range(len(fileList)/2) :     
    name = fileList[index].split('/')[1]
    if name != fileList[index+len(fileList)/2].split('/')[1] : 
        print "%-15s\tERROR\t%s"%(name,fileList[index+len(fileList)/2].split('/')[1]) 
        continue

    dataA = np.genfromtxt(fileList[index]) 
    dataB = np.genfromtxt(fileList[index+len(fileList)/2]) 

    avgA = np.average(dataA) 
    avgB = np.average(dataB) 

    ddG = avgB - avgA 
    dpKa = ddG / 2.5 / 2.303 
    pKa = dpKa + 8.2 
    print "%-15s\t%5f"%(name, pKa) 


print "\n\n\t***** e = 20, 5 A explicit  *****\n\n" 
fileList = glob.glob('?_State/*_T203[BCHXZ]/NEARBY_WAT_ENERGIES/dG_xter_CR?.dat') 
fileList = sorted(fileList) 

for index in range(len(fileList)/2) :     
    name = fileList[index].split('/')[1]
    if name != fileList[index+len(fileList)/2].split('/')[1] : 
        print "%-15s\tERROR\t%s"%(name,fileList[index+len(fileList)/2].split('/')[1]) 
        continue

    dataA = np.genfromtxt(fileList[index]) 
    dataB = np.genfromtxt(fileList[index+len(fileList)/2]) 

    avgA = np.average(dataA) 
    avgB = np.average(dataB) 

    ddG = avgB - avgA 
    dpKa = ddG / 2.5 / 2.303 
    pKa = dpKa + 8.2 
    print "%-15s\t%5f"%(name, pKa) 


print "\n\n\t***** e = 2,10 A explicit  *****\n\n" 
fileList = glob.glob('?_State/*_T203[BCHXZ]/NEARBY_10_LOWE/dG_xter_CR?.dat') 
fileList = sorted(fileList) 

for index in range(len(fileList)/2) :     
    name = fileList[index].split('/')[1]
    if name != fileList[index+len(fileList)/2].split('/')[1] : 
        print "%-15s\tERROR\t%s"%(name,fileList[index+len(fileList)/2].split('/')[1]) 
        continue

    dataA = np.genfromtxt(fileList[index]) 
    dataB = np.genfromtxt(fileList[index+len(fileList)/2]) 

    avgA = np.average(dataA) 
    avgB = np.average(dataB) 

    ddG = avgB - avgA 
    dpKa = ddG / 2.5 / 2.303 
    pKa = dpKa + 8.2 
    print "%-15s\t%5f"%(name, pKa) 


print "\n\n\t***** e = 20,10 A explicit  *****\n\n" 
fileList = glob.glob('?_State/*_T203[BCHXZ]/NEARBY_10_ENERGIES/dG_xter_CR?.dat') 
fileList = sorted(fileList) 

for index in range(len(fileList)/2) :     
    name = fileList[index].split('/')[1]
    if name != fileList[index+len(fileList)/2].split('/')[1] : 
        print "%-15s\tERROR\t%s"%(name,fileList[index+len(fileList)/2].split('/')[1]) 

    dataA = np.genfromtxt(fileList[index]) 
    dataB = np.genfromtxt(fileList[index+len(fileList)/2]) 

    avgA = np.average(dataA) 
    avgB = np.average(dataB) 

    ddG = avgB - avgA 
    dpKa = ddG / 2.5 / 2.303 
    pKa = dpKa + 8.2 
    print "%-15s\t%5f"%(name, pKa) 


print "\n\n\t***** e = 6 , Implicit Water*****\n\n" 
fileList = glob.glob('?_State/*_T203[BCHXZ]/6_FREE_ENERGIES/dG_xter_CR?.dat') 
fileList = sorted(fileList) 

for index in range(len(fileList)/2) :     
    name = fileList[index].split('/')[1]
    if name != fileList[index+len(fileList)/2].split('/')[1] : 
        print "%-15s\tERROR\t%s"%(name,fileList[index+len(fileList)/2].split('/')[1]) 

    dataA = np.genfromtxt(fileList[index]) 
    dataB = np.genfromtxt(fileList[index+len(fileList)/2]) 

    avgA = np.average(dataA) 
    avgB = np.average(dataB) 

    ddG = avgB - avgA 
    dpKa = ddG / 2.5 / 2.303 
    pKa = dpKa + 8.2 
    print "%-15s\t%5f"%(name, pKa) 


print "\n\n\t***** e = 6, 5 A Explicit *****\n\n" 
fileList = glob.glob('?_State/*_T203[BCHXZ]/NEARBY_10_ENERGIES/dG_xter_CR?.dat') 
fileList = sorted(fileList) 

for index in range(len(fileList)/2) :     
    name = fileList[index].split('/')[1]
    if name != fileList[index+len(fileList)/2].split('/')[1] : 
        print "%-15s\tERROR\t%s"%(name,fileList[index+len(fileList)/2].split('/')[1]) 

    dataA = np.genfromtxt(fileList[index]) 
    dataB = np.genfromtxt(fileList[index+len(fileList)/2]) 

    avgA = np.average(dataA) 
    avgB = np.average(dataB) 

    ddG = avgB - avgA 
    dpKa = ddG / 2.5 / 2.303 
    pKa = dpKa + 8.2 
    print "%-15s\t%5f"%(name, pKa) 
