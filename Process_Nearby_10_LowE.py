#!/usr/bin/env python 

import numpy as np 
import os
import matplotlib.pyplot as plt
from sys import exit
from scipy.stats import linregress
import glob 

fileList = glob.glob('A_State/*/NEARBY_10_LOWE/dG_xter_CRO.dat') 
mutList = [] 
for item in fileList : 
    mut = item.split('/')[1]  
    if mut[-1:] == 'D' : continue 
    if mut[-1:] == 'B' : continue 
    if mut[-1:] == 'X' : continue 
    if mut[-1:] == 'Z' : continue 
    mutList.append(mut) 

exp_pKas= {
'CN145_T203C':7.86, 
'CN145_T203D':11.0, 
'CN145_T203F':7.35, 
'CN145_T203H':6.28, 
'CN145_T203N':7.22, 
'CN145_T203S':6.87, 
'CN145_T203W':'NA', 
'CN145_T203Y':8.04,
'CN145_WT':6.84, 
'CN165_T203C':7.60, 
'CN165_T203D':11.0, 
'CN165_T203F':7.52, 
'CN165_T203H':6.66, 
'CN165_T203N':7.43, 
'CN165_T203S':6.73, 
'CN165_T203W':'NA', 
'CN165_T203Y':7.95,
'CN165_WT':7.20, 
'GFP_WT_T203C':6.85, 
'GFP_WT_T203D':11.0, 
'GFP_WT_T203F':7.51, 
'GFP_WT_T203H':6.54, 
'GFP_WT_T203N':7.11, 
'GFP_WT_T203S':6.50, 
'GFP_WT_T203W':'NA', 
'GFP_WT_T203Y':7.95,
'GFP_WT':6.70} 

if not os.path.isdir("pKas") : 
    os.mkdir("pKas") 
os.chdir("pKas") 


with open ("pKa.dat", 'w') as f : 
    #f.write("    Mutation   Average pKa    stdpKa      Average ddG stdddG    Exper. pKa  Crystal pKa\n") 
    f.write("%14s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\n"%("Mutation", "Avg dpKa", "std", "Avg ddG", "std", "Exper pKa", "Cryst pKa") ) 

for index,mut in enumerate(mutList): 
    mut=mutList[index]
    outName = "Nearby_10_LowE_%s_ddG.pdf"%mut
    outData = "Nearby_10_LowE_%s_ddG_pKa.dat"%mut
    bashCommand = "/Users/jeremyfirst/Desktop/normal_distribution/tiltAngle -f %s_ddG_pKa.dat -o %s_hist.dat -g %s_hist_fit.dat"%(mut, mut, mut) 
    #print bashCommand
    dataFileA="../A_State/%s/NEARBY_10_LOWE/dG_xter_CRO.dat"%mut
    dataFileB="../B_State/%s/NEARBY_10_LOWE/dG_xter_CRB.dat"%mut

    print "%s"%mut

    try :
        dataA = np.genfromtxt(dataFileA) 
        dataB = np.genfromtxt(dataFileB) 
    except : 
        print "\tdG dat files not found for %s"%mut 
        with open("pKa.dat", 'a') as f: 
            f.write("%14s\t%10f\t%10f\t%10f\t%10f\t%10f\t%10f\n"%(mut, 0.0,0.0,0.0,0.0,0.0,0.0) )
#            f.write("%14s\t%10s\t%10s\n"%(mut, "ERROR", "ERROR") )
        continue 

    ddG = dataB[:,1] - dataA[:,1]
    simTime = dataA[:,0] 
    simTime = simTime  / 1000

    ##Throw away the first 10ns for 'equilibration' time
    ddG = ddG[20:] 
    simTime = simTime[20:] 

    if len(ddG) != 101 : 
        print "\tWarning: %i frames found!"%(len(ddG))

    dpKa = ddG / 2.5 / 2.303 ## pKa = Del G / (RT ln(10 ) ) 

    #avg_ddG = np.average(ddG[20:100]) 
    #avg_dpKa = np.average(dpKa[20:100]) 
    avg_ddG = np.average(ddG) 
    avg_dpKa = np.average(dpKa) 
    
    with open(outData, 'w') as f: 
        f.write('#Avg: ddG     dpKa\n') 
        f.write("#%8f %8f\n"%(avg_ddG,avg_dpKa) ) 
        for i in range(len(ddG) ) : 
            f.write(" %8f %8f\n"%(ddG[i], dpKa[i]) ) 

    rolAvg = np.zeros(len(ddG)) 
    rolAvg[0] = ddG[0]
    for i in range(1,len(ddG)) : 
        rolAvg[i] = np.average(ddG[:i])

    #print rolAvg

    convergance=np.zeros(len(ddG)) 

    #convergance[:20] = np.average(ddG[:20]) 
    convergance[0:50] = np.average(ddG[0:50]) 
    convergance[50:101] = np.average(ddG[50:101]) 
    stdpKa = np.std(dpKa) 
    stdddG = np.std(ddG) 
    fig, ax1 = plt.subplots()
    ax1.plot(simTime, rolAvg) 
    ax1.plot(simTime, ddG) 
    ax1.plot(simTime, convergance)

    ax1.set_xlabel('Simulation time (ns)') 
    ax1.set_ylabel('Calculated ddG (kJ/mol)') 
    ax1.set_label("%s"%mut) 

    ax2 = ax1.twinx()
    mn, mx = ax1.get_ylim() 
    ax2.set_ylim(mn/2.5/2.303, mx/2.5/2.303) 
    ax2.set_ylabel('dpKa') 
    fig.savefig(outName, format='pdf') 
    plt.close()

    with open("pKa.dat", 'a') as f : 
        if exp_pKas[mut] == 'NA' : continue 
        f.write("%14s\t%10f\t%10f\t%10f\t%10f\t%10s\t%10f\n"%(mut, avg_dpKa, stdpKa, avg_ddG, stdddG, exp_pKas[mut],dpKa[0]) ) 

### Plotting
labels= np.genfromtxt('pKa.dat',skip_header=1,usecols = (0), dtype='str') 
pKa   = np.genfromtxt('pKa.dat',skip_header=1,usecols = (1) ) 
stdpKa= np.genfromtxt('pKa.dat',skip_header=1,usecols = (2) ) 
ddG   = np.genfromtxt('pKa.dat',skip_header=1,usecols = (3) ) 
stdddG= np.genfromtxt('pKa.dat',skip_header=1,usecols = (4) ) 
exper = np.genfromtxt('pKa.dat',skip_header=1,usecols = (5) ) 
cryst = np.genfromtxt('pKa.dat',skip_header=1,usecols = (6) ) 

pKa +=  8.2
cryst += 8.2

x = np.arange(exper.min(),exper.max(),.01) 


mutToColor={
    "C":'c',
    "D":'k',
    "F":'r',
    "H":'#FFA500',
    "N":'g',
    "S":'m',
    "W":'k',
    "Y":'y',
    "T":'b'
}

nitToMarker={
    "CN145":'s', 
    "CN165":'D', 
    "GFP_W":'o'
}

### ddG vs Experimental 
fig1 = plt.figure() 
ax1 = fig1.add_subplot(111) 
for pnt in range(len(exper) ) : 
#    if exper[pnt] == 0 : continue 
     ax1.errorbar(exper[pnt],  pKa[pnt],marker=nitToMarker[labels[pnt][:5]],color=mutToColor[labels[pnt][-1:]],xerr=0.1,yerr=stdpKa[pnt] ) 

slope, intercept, r_value, p_value, std_err = linregress(exper, pKa) 
ax1.plot(x,x*slope+intercept, 'b-', label="r = %.3f"%r_value) 
print "r = ", r_value, "\tr^2 = ", r_value**2

ax1.set_ylabel('Calculated pKa') 
ax1.set_xlabel('Experimental (pKa)') 

ax12 = ax1.twinx()
mn, mx = ax1.get_ylim() 
ax12.set_ylim((mn-8.2)*2.5*2.303, (mx-8.2)*2.5*2.303) 
ax12.set_ylabel('ddG (kJ/mol)') 

ax1.legend() 
fig1.savefig('Nearby_10_LowE_pKa.pdf', format='pdf') 

fig2 = plt.figure() 
ax2 = fig2.add_subplot(111) 
for pnt in range(len(exper) ) : 
    ax2.errorbar(exper[pnt],  cryst[pnt],marker=nitToMarker[labels[pnt][:5]],color=mutToColor[labels[pnt][-1:]],xerr=0.1) 

slope, intercept, r_value, p_value, std_err = linregress(exper, cryst) 
ax2.plot(x,x*slope+intercept,label="r = %f"%r_value) 
print r_value**2, "  ", r_value, "slope=  ", slope

ax2.set_ylabel('Calculated pKa') 
ax2.set_xlabel('Experimental (pKa)') 

ax22 = ax2.twinx()
mn, mx = ax2.get_ylim() 
ax22.set_ylim((mn-8.2)*2.5*2.303, (mx-8.2)*2.5*2.303) 
ax22.set_ylabel('ddG (kJ/mol)') 

fig2.savefig('Nearby_10_LowE_pKa_cryst.pdf', format='pdf') 




