import numpy as np 
import glob as glob 
import matplotlib.pyplot as plt

files = glob.glob('?_State/*/HBond/cnf_num.xvg') 
files = sorted(files) 

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

mutExppKa = { 
    'CN145_T203C':7.86, 
    #'CN145_T203D':11.0, 
    'CN145_T203F':7.35, 
    'CN145_T203H':6.28, 
    'CN145_T203N':7.22, 
    'CN145_T203S':6.87, 
    #'CN145_T203W':'NA', 
    'CN145_T203Y':8.04,
    'CN145_WT':6.84, 
    'CN165_T203C':7.60, 
    #'CN165_T203D':11.0, 
    'CN165_T203F':7.52, 
    'CN165_T203H':6.66, 
    'CN165_T203N':7.43, 
    'CN165_T203S':6.73, 
    #'CN165_T203W':'NA', 
    'CN165_T203Y':7.95,
    'CN165_WT':7.20 
} 

#data = [] 
#for file in files : 
#    data.append(np.genfromtxt(file,skip_header=23)) 
#
#print "**CNF HBond**"
#numMols = len(files)/2
#hbondData = [] 
#for index in range(numMols) : 
#    aFile = files[index] 
#    bFile = files[index+numMols]
#    if files[index].split('/')[1] != files[index+numMols].split('/')[1] :
#        print "ERROR!" 
#        break 
#    else : 
#        name = files[index].split('/')[1]
#
#    aAvg,aStd = np.average(data[index][:,1]), np.std(data[index][:,1]) 
#    bAvg,bStd = np.average(data[index+numMols][:,1]), np.std(data[index+numMols][:,1]) 
#
#    try : 
#        pKa = float(mutExppKa[name]) 
#    except : 
#        print "%-15s pKa not found! Skipping."%name
#        continue 
#
#    ratio = 10**+(7.4 - pKa) 
#    wAvg = bAvg * ratio/(ratio/1) + (1)/(ratio+1)*aAvg 
#    hbondData.append([name,wAvg]) 
#    print "%-15s\t%8f\t"%(name, wAvg)
#
#pnts = len(hbondData) / 2
#for index in range(len(hbondData)/2 ): 
#    name, wAvg = hbondData[index][0],hbondData[index][1]
#    plt.bar(index*2, wAvg, color=mutToColor[name[-1]]) 
#    plt.bar(index*2+1, hbondData[index+pnts][1], color=mutToColor[name[-1]]) 
#
#plt.show() 
#plt.close() 
#exit() 



files = glob.glob('?_State/*/HBond/cro_num.xvg') 
files = sorted(files) 

data = [] 
for file in files : 
    data.append(np.genfromtxt(file,skip_header=23)) 

print "**CRO HBond**"
for index in range(len(data)) : 
    print "%15s\t%15s\t%15s"%(files[index].split('/')[0],files[index].split('/')[1],files[index].split('/')[2]), 
    print "%10f\n"%(np.average(data[index][:,1]) ),

for index in range(len(data)/2) : 
    plt.errorbar(index,np.average(data[index][:,1]),yerr=np.std(data[index][:,1]),marker='o')  
    plt.errorbar(index,np.average(data[index+len(data)/2][:,1]),yerr=np.std(data[index+len(data)/2][:,1]),marker='D')  

plt.show() 
plt.close() 

exit() 



files = glob.glob('?_State/*/dist_203_CRO/*.xvg') 
files = sorted(files) 

data = [] 
for file in files : 
    data.append(np.genfromtxt(file,skip_header=23)) 

print "**CRO-203 Dist**"
for index in range(len(data)) : 
    print "%15s\t%15s\t%15s"%(files[index].split('/')[0],files[index].split('/')[1],files[index].split('/')[2]), 
    print "%10f\n"%(np.average(data[index][:,1]) ),

for index in range(len(data)/2) : 
    plt.errorbar(index,np.average(data[index][:,1]),yerr=np.std(data[index][:,1]),marker='o')  
    plt.errorbar(index,np.average(data[index+len(data)/2][:,1]),yerr=np.std(data[index+len(data)/2][:,1]),marker='D')  

plt.show() 
plt.close() 

files = glob.glob('?_State/*/dist_CNF_CRO/*.xvg') 
files = sorted(files) 

data = [] 
for file in files : 
    data.append(np.genfromtxt(file,skip_header=23)) 

print "**CRO-CNF Dist**"
for index in range(len(data)) : 
    print "%15s\t%15s\t%15s"%(files[index].split('/')[0],files[index].split('/')[1],files[index].split('/')[2]), 
    print "%10f\n"%(np.average(data[index][:,1]) ),

for index in range(len(data)/2) : 
    plt.errorbar(index,np.average(data[index][:,1]),yerr=np.std(data[index][:,1]),marker='o')  
    plt.errorbar(index,np.average(data[index+len(data)/2][:,1]),yerr=np.std(data[index+len(data)/2][:,1]),marker='D')  

plt.show() 
plt.close() 
