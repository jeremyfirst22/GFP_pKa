import numpy as np 
import matplotlib.pyplot as plt 

pKaData = np.genfromtxt('pKas/pKa.dat',skip_header=1,usecols=3) 

print pKaData
