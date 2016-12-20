import glob 
import numpy as np 
import matplotlib.pyplot as plt
from sys import exit
import os 
from scipy.stats import linregress

from matplotlib import rc_file

force_dir='APBS_6_nearby_wat_force'
save_dir='force_calc_6_nearby_APBS' 

force_files = glob.glob('[AB]_State/*/%s/coloumb_field.out'%force_dir) 

molList= []
for item in force_files : 
    state, molec,throwAway,field = item.split('/') 
    if not os.path.isfile("%s/%s/%s/rxn_field.out"%(state,molec,force_dir)) : 
        print "Not found, removing!"
        force_files.remove(item) 
    else : 
        molList.append([state, molec]) 

mutToExp = {
'CN145_T203C':2225.5, 
'CN145_T203F':2225.9, 
'CN145_T203H':2226.1,
'CN145_T203N':2225.4,
'CN145_T203S':2225.6,
'CN145_T203Y':2226.8,
'CN145_WT':2225.7,
'CN165_T203C':2234.1,
'CN165_T203F':2233.7,
'CN165_T203H':2233.5,
'CN165_T203N':2234.0,
'CN165_T203S':2234.3,
'CN165_T203Y':2233.5,
'CN165_WT':2234.4
}

mutExppKa={
    'CN145_WT':    [6.63,0.04],
    'CN145_T203F': [7.20,0.04],
    'CN145_T203C': [7.86,0.04], 
    'CN145_T203H': [6.28,0.05], 
    'CN145_T203N': [7.22,0.04],
    'CN145_T203S': [6.88,0.07], 
    'CN145_T203Y': [7.95,0.04],
    'CN165_WT':    [7.17,0.03], 
    'CN165_T203F': [7.51,0.05], 
    'CN165_T203C': [7.65,0.04],  
    'CN165_T203H': [6.77,0.05], 
    'CN165_T203N': [7.42,0.06], 
    'CN165_T203S': [6.73,0.05], 
    'CN165_T203Y': [7.95,0.03]}

molList = sorted(molList ) 
numMols = len(molList) /2
data = [] 
for molec in range(numMols ) : 
    if not molList[molec][1] == molList[molec+numMols][1] : 
        print "Logical fallicy! Your A & B states do not align. Cowardly exitting.\n %s\t%s"%(molList[molec][1], molList[molec+numMols][1]) 
        exit() 
    try : 
        rxn_fieldA = np.genfromtxt("%s/%s/%s/rxn_field.out"%(molList[molec][0],molList[molec][1],force_dir) ) 
        coloumb_fieldA = np.genfromtxt("%s/%s/%s/coloumb_field.out"%(molList[molec][0],molList[molec][1],force_dir) ) 
        rxn_fieldB = np.genfromtxt("%s/%s/%s/rxn_field.out"%(molList[molec+numMols][0],molList[molec+numMols][1],force_dir) ) 
        coloumb_fieldB = np.genfromtxt("%s/%s/%s/coloumb_field.out"%(molList[molec+numMols][0],molList[molec+numMols][1],force_dir) ) 
    except : 
        print "ERROR: %s failed!"%molList[molec]
        continue 
    try : 
        print mutToExp[molList[molec][1]]
    except : 
        print molList[molec][1]
        continue
    solventFieldA = np.average(rxn_fieldA[20:]) + np.average(coloumb_fieldA[20:]) 
    solventFieldB = np.average(rxn_fieldB[20:]) + np.average(coloumb_fieldB[20:]) 
    data.append([molList[molec][1],solventFieldA, solventFieldB]) 

for molec in data : 
    try : 
        pKa = float(mutExppKa[molec[0]][0]) 
    except (KeyError, ValueError) : 
        print "%s pKa not found!"%molec[0]
        data.remove(molec) 
        print molec[0], " removed!"
        continue
    #print molec[0],pKa
    ratio = 10**+(7.4 - pKa) 
    weightedF = molec[2] * ratio/(ratio+1) + (1)/(ratio+1)*molec[1] 
    molec.append(weightedF) 

for item in data : print item 

if not os.path.isdir(save_dir) : 
    os.mkdir(save_dir) 
os.chdir(save_dir) 

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
stateToMarker = { 
"A":'v', 
"B":'D' 
} 

with open('forces.dat','w') as f: 
    f.write("Name      SolventFieldA   SolventFieldB    WeightedField\n") 
with open('forces.dat','a') as f : 
    for item in data : 
        f.write("%s\t%f\t%f\t%f\n"%(item[0],item[1],item[2],item[3]) ) 

names= np.genfromtxt('forces.dat',skip_header=1,usecols=0,dtype='str') 
dataA= np.genfromtxt('forces.dat',skip_header=1,usecols=1) 
dataB= np.genfromtxt('forces.dat',skip_header=1,usecols=2) 
dataW= np.genfromtxt('forces.dat',skip_header=1,usecols=3) 

rc_file('../force_rc.rc') 
fig1, axarr = plt.subplots(1,2,sharey='col') 
#fig2, ax2 = plt.subplots(1,1) 

ax1 = axarr[0]
ax2 = axarr[1]

ax1.set_xlabel(r"Experimental frequency (cm$^{-1}$)")
ax2.set_xlabel(r"Experimental frequency (cm$^{-1}$)")
ax1.set_ylabel(r"Calculated Field (k$_b$T/$e\AA$)") 


CN145, CN165 = [],[]
for i in range(len(dataW)) : 
    if names[i][:5] == 'CN145' : 
        CN145.append([mutToExp[names[i]],dataW[i]])
        ax1.scatter(mutToExp[names[i]],dataW[i],color=mutToColor[names[i][-1]],marker='o') 
    if names[i][:5] == 'CN165' : 
        CN165.append([mutToExp[names[i]],dataW[i]])
        ax2.scatter(mutToExp[names[i]],dataW[i],color=mutToColor[names[i][-1]],marker='o') 

CN145 = np.array(CN145) 
CN165 = np.array(CN165) 

x = np.arange(min(CN145[:,0]), max(CN145[:,0]),0.001 ) 
slope, intercept, r_value, p_value, std_error = linregress(CN145[:,0],CN145[:,1]) 
ax1.plot(x,x*slope + intercept,label="r = %.3f"%r_value) 
ax1.legend(loc=0) 
#fig1.savefig('CN145.pdf',format='pdf') 

x = np.arange(min(CN165[:,0]), max(CN165[:,0]),0.001)  
slope, intercept, r_value, p_value, std_error = linregress(CN165[:,0],CN165[:,1]) 
ax2.plot(x,x*slope + intercept,label="r = %.3f"%r_value) 
ax2.legend(loc=4) 
#fig2.savefig('CN165.pdf',format='pdf') 

start, end = 2233.5, 2235.0 #ax2.get_xlim() 
#start, end = np.around(start,1), np.around(end,0) 
print start, end 
ax2.xaxis.set_ticks(np.arange(start,end,0.5) ) 

fig1.savefig('forces.pdf',format='pdf') 



