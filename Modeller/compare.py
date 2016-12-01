from modeller import *

env = environ()
aln = alignment(env)
for (pdb, chain) in (('2b3p', 'A'), ('4xbi', 'A'), ('5dph', 'A'),
                     ('5dpi', 'A'), ('5dpj', 'A')) : 
    m = model(env, file=pdb, model_segment=('FIRST:'+chain, 'LAST:'+chain))
    aln.append_model(m, atom_files=pdb, align_codes=pdb+chain)
aln.malign()
aln.malign3d()
aln.compare_structures()
aln.id_table(matrix_file='family.mat')
env.dendrogram(matrix_file='family.mat', cluster_cut=-1.0)
