from sys import exit 
import os 
import numpy as np 
import matplotlib.pyplot as plt 
import subprocess 

mutList = ["CN145_T203C", "CN145_T203H","CN145_T203N", "CN145_T203S", "CN145_T203Y","CN145_WT", "CN165_T203C", "CN165_T203H", "CN165_T203N", "CN165_T203S", "CN165_T203Y", "CN165_WT", "GFP_WT_T203C", "GFP_WT_T203H", "GFP_WT_T203N", "GFP_WT_T203S", "GFP_WT_T203Y", "GFP_WT"] 
index = 0

if not os.path.isdir("pKas") : 
    print "No pKas directory found" 
    exit 
os.chdir("pKas" ) 

f, axarr = plt.subplots(3,6,sharex='col', sharey='row') 
f.set_figheight(8 ) 
f.set_figwidth(15) 
f.subplots_adjust(wspace=0) 
f.text(0.5, 0.04, "ddG (kJ/mol) ", ha='center', va='center')
f.text(0.06, 0.5, 'Occurances', ha='center', va='center', rotation='vertical')
#f.tight_layout() 

def myround(x, base=6): 
    return int(base * round(float(x)/base)) 

for mut in mutList : 
    bashCommand = "/Users/jeremyfirst/Desktop/normal_distribution/tiltAngle -f %s_ddG_pKa.dat -o %s_hist.dat -n 25 -g %s_hist_fit.dat --overwrite 2&1>> %s.out "%(mut,mut,mut,mut) 

    p = subprocess.Popen(bashCommand, shell=True) 
    os.waitpid(p.pid, 0) 
    print "\tComplete!"

    axarr[index/6,index%6].set_title("%s"%mut) 

    try : 
        hist = np.genfromtxt("%s_hist.dat"%mut) 
        gaus = np.genfromtxt("%s_hist_fit.dat"%mut) 
    except : 
        print "Warning: %s failed!"%mut
        index+=1
        continue 

    axarr[index/6,index%6].scatter(hist[:,0],hist[:,1],marker='+',color='red') 
    axarr[index/6,index%6].plot(gaus[:,0],gaus[:,1],color='blue')  
    axarr[index/6,index%6].set_xlim([-10,20]) 
    axarr[index/6,index%6].set_ylim([0,0.36]) 
    index+=1

plt.setp([a.get_xticklabels() for a in axarr[0,:]], visible=False) 
plt.setp([a.get_yticklabels() for a in axarr[:,1]], visible=False) 


plt.savefig('all_distros.pdf',format='pdf') 
plt.close() 

for mut in mutList : 
    try : 
        hist = np.genfromtxt("%s_hist.dat"%mut) 
        gaus = np.genfromtxt("%s_hist_fit.dat"%mut) 
    except : 
        print "Warning: %s failed!"%mut
        index+=1
        continue 

    plt.scatter(hist[:,0],hist[:,1],marker='+',color='red')  
    plt.plot(gaus[:,0],gaus[:,1],color='blue') 
    plt.xlabel('ddG (kJ/mol)') 
    plt.ylabel('Occurances') 
    plt.axis('tight') 
    plt.savefig("%s_hist.pdf"%mut, format='pdf') 
    plt.close() 

