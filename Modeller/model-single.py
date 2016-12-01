from modeller import *
from modeller.automodel import *
#from modeller import soap_protein_od

log.verbose()
env = environ()

env.io.hetatm = True 
env.io.water= True 

a = automodel(env, alnfile='WTGFP-2b3pA.ali',
              knowns='2b3pA', sequence='WTGFP',
              assess_methods=(assess.DOPE,
                              #soap_protein_od.Scorer(),
                              assess.GA341))
a.starting_model = 1
a.ending_model = 5
a.make()
