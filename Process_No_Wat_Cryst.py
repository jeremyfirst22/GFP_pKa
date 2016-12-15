#!/usr/bin/env python 

import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import os.path
import glob 
from scipy.stats import linregress

from matplotlib import rc_file


if not os.path.isdir('no_wat_cryst_pKas') : 
    print "Directory no_wat_cryst_pKas does not exist; Run Cryst_no_water_pKa.sh to generate data"
    exit() 
else : 
    os.chdir('no_wat_cryst_pKas') 

exp_pKas= {
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
'CN165_T203Y': [7.95,0.03], 
'GFP_WT':      [6.70,0.07], 
'GFP_WT_T203F':[7.50,0.03],
'GFP_WT_T203C':[6.85,0.05],
'GFP_WT_T203H':[6.54,0.03],
'GFP_WT_T203N':[7.11,0.08],
'GFP_WT_T203S':[6.48,0.07],
'GFP_WT_T203Y':[7.95,0.04]}

data = [] 
for ddGfile in glob.glob('*.ddG') : 
    molec = ddGfile[:-4] 
#    if molec[-1:] == 'N' : continue
    with open(ddGfile, 'r') as f : 
        ddG = float(f.read() ) 
    dpKa = ddG / 2.5 / 2.303  
    dpKa +=8.2

    try : 
        exp = float(exp_pKas[molec][0]) 
    except KeyError : 
        print "Warning! %s not found in exp_data!"%molec
        continue 
    except ValueError : 
        print "Warning! %s has no experimental data"%molec
        continue 

    data.append([molec, ddG, exp, dpKa]) 
data = np.array(data)

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
    'GFP_W':'o', 
    'CN145':'s',
    'CN165':'D'} 
rc_file('../pKa_rc.rc') 

fig1 = plt.figure() 
ax1 = fig1.add_subplot(111) 

for pt in range(len(data)) : 
    ax1.scatter(data[pt,2],data[pt,3],marker=nitToMarker[data[pt,0][:5]],color=mutToColor[data[pt,0][-1:]], edgecolors='k') 

ax1.set_xlabel(r"Experimental pK$_a$") 
ax1.set_ylabel(r"Calculated pK$_a$") 
ax1b = ax1.twinx() 
mn, mx = ax1.get_ylim() ; ax1b.set_ylim((mn-8.2)*2.5*2.303, (mx-8.2)*2.5*2.303) 
ax1b.set_ylabel(r"$\Delta\Delta$G (kJ/mol)") 

x = np.arange(np.min(data[:,2].astype(np.float)), np.max(data[:,2].astype(np.float)) ,0.01) 
slope, intercept, r_value, p_value, std_err = linregress(data[:,2].astype(np.float), data[:,3].astype(np.float)) 
ax1.plot(x, x*slope + intercept, '-',label="r = %f"%r_value) 
print slope, r_value, r_value**2

best_fit = mlines.Line2D([],[], color='blue', label="r =  %.3f"%r_value) 
##red_dot = mlines.Line2D([],[],color='red',linestyle='None',marker='o',label='red_dot') 

blu_dot = mlines.Line2D([],[], linestyle='None',color='b', marker='o',label="WT") 
mag_dot = mlines.Line2D([],[], linestyle='None',color='m', marker='o',label="T203S") 
gre_dot = mlines.Line2D([],[], linestyle='None',color='g', marker='o',label="T203N") 
yel_dot = mlines.Line2D([],[], linestyle='None',color='y', marker='o',label="T203Y") 
ora_dot = mlines.Line2D([],[], linestyle='None',color='#FFA500', marker='o',label="T203H") 
red_dot = mlines.Line2D([],[], linestyle='None',color='r', marker='o',label="T203F") 
cya_dot = mlines.Line2D([],[], linestyle='None',color='c', marker='o',label="T203C") 

circ= mlines.Line2D([],[], color='w', marker='o', label="WT") 
squar= mlines.Line2D([],[], color='w', marker='s', label="pCNF 145") 
diam = mlines.Line2D([],[], color='w', marker='D', label="pCNF 165") 

#first_legend=ax1.legend(handles=[blu_dot, mag_dot, gre_dot, yel_dot, red_dot, ora_dot, cya_dot], numpoints=1) 
#ax1.add_artist(first_legend) 
#ax1.legend(handles=[best_fit,circ, squar, diam],numpoints=1,loc=2) 
ax1.legend(handles=[best_fit],loc=2) 


fig1.savefig('no_wat_cryst_pKas.pdf', fomat='pdf') 
        






