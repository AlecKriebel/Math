import json,sys,hashlib
from pathlib import Path
from fractions import Fraction as F
ROOT=Path('/mnt/data/k3p_identifiability_final');sys.path[:0]=[str(ROOT/'software'),str(ROOT/'software/atlas')]
import k3p_atlas_core as k3
from k3p_three_port_models import tree_descriptor,sunlet_descriptor,labels

def cert_at(desc,edges,lams):
 J=k3.descriptor_jacobian(desc,edges,lams);rank,rows,cols=k3.exact_rank_pivots(J);det=k3.determinant_square([[J[i][j] for j in cols] for i in rows])
 return {'rank':rank,'rows':rows,'columns':cols,'determinant':str(det),'edge_triples':[[str(x) for x in e] for e in edges],'lambdas':[str(x) for x in lams]}
T=tree_descriptor();tp=tuple((F(2,5),F(3,7),F(4,9)) for _ in range(3));tc=cert_at(T,tp,())
# exact common point: a,b,c,d,e isotropic 1/2; f isotropic 1/3; delta 1/2
sp=((F(1,2),)*3,)*3+((F(1,3),)*3,)+((F(1,2),)*3,)*2
vals=[];sc=[]
for o in (1,2,3):
 d=sunlet_descriptor(o);vals.append(k3.eval_descriptor(d,sp,(F(1,2),)));sc.append(cert_at(d,sp,(F(1,2),)))
assert vals[0]==vals[1]==vals[2]
assert tc['rank']==9 and all(x['rank']==14 for x in sc)
# strict domain/CT checks
for e in sp:
 c,g,t=e;assert 1+c-g-t>0 and 1-c+g-t>0 and 1-c-g+t>0 and c>g*t and g>c*t and t>c*g
payload={'schema':'k3p-three-port-ranks-v2','coordinate_labels':labels(),'tree':tc,'sunlet_orientations':{str(o):c for o,c in zip((1,2,3),sc)},'common_tensor':[str(x) for x in vals[0]],'common_point_strict_continuous_time':True}
out=ROOT/'software/certificates/k3p_three_port_ranks.json';out.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
print('K3P_TREE_RANK',tc['rank']);print('K3P_TRIANGLE_RANKS',[x['rank'] for x in sc]);print('K3P_COMMON_TRIANGLE_TENSOR_PASS')
