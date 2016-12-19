import matplotlib.pyplot as plt 
import matplotlib.lines as mlines 
import matplotlib.patches as mpatches
from matplotlib import rc_file

rc_file('legend_rc.rc') 

fig1, ax1 = plt.subplots(1,1) 

blu_dot = mlines.Line2D([],[], linestyle='None',color='b', marker='o',label="WT") 
mag_dot = mlines.Line2D([],[], linestyle='None',color='m', marker='o',label="S203") 
gre_dot = mlines.Line2D([],[], linestyle='None',color='g', marker='o',label="N203") 
yel_dot = mlines.Line2D([],[], linestyle='None',color='y', marker='o',label="Y203") 
ora_dot = mlines.Line2D([],[], linestyle='None',color='#FFA500', marker='o',label="H203") 
red_dot = mlines.Line2D([],[], linestyle='None',color='r', marker='o',label="F203") 
cya_dot = mlines.Line2D([],[], linestyle='None',color='c', marker='o',label="C203") 

circ= mlines.Line2D([],[], color='w', marker='o', label="WT") 
squar= mlines.Line2D([],[], color='w', marker='s', label=r"$p$CNF 145") 
diam = mlines.Line2D([],[], color='w', marker='D', label=r"$p$CNF 165") 

first_legend=ax1.legend(handles=[circ, squar, diam, blu_dot, mag_dot, gre_dot, yel_dot, red_dot, ora_dot, cya_dot], numpoints=1)
ax1.add_artist(first_legend)
ax1.legend(handles=[blu_dot, mag_dot, gre_dot, yel_dot, red_dot, ora_dot, cya_dot],numpoints=1,loc=2)

plt.savefig('legend.pdf',format='pdf') 

