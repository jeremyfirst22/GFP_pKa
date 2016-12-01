from modeller import *

env = environ()

env.io.water = True 
env.io.hetatm = True 

aln = alignment(env)
mdl = model(env, file='2b3p', model_segment=('FIRST:A','LAST:A'))
aln.append_model(mdl, align_codes='2b3pA', atom_files='2b3p.pdb')
aln.append(file='WTGFP.ali', align_codes='WTGFP')
aln.align2d()
aln.write(file='WTGFP-2b3pA.ali', alignment_format='PIR')
aln.write(file='WTGFP-2b3pA.pap', alignment_format='PAP')
