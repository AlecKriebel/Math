from simplicial import *
from collections import Counter
import json
checks=0;cats={};rows=[]
def ck(x,k):
 global checks
 assert x,k;checks+=1;cats[k]=cats.get(k,0)+1
RP,S=surface_models();BRP,labels=barycentric(RP)
for name,K,expected in [('icosahedral_sphere',S,[1,0,1]),('projective_plane',RP,[1,0,0]),('flag_projective_plane',BRP,[1,0,0])]:
 cs,D=boundaries(K);ck(mm(D[0],D[1])==zeros(len(cs[0]),len(cs[2])),'boundary_squared_zero')
 counts=Counter(e for f in cs[2] for e in combinations(f,2));ck(set(counts.values())=={2},'surface_edge_incidence')
 for v, in cs[0]:
  lk={tuple(x for x in f if x!=v) for f in K if v in f and len(f)>1}
  b=betti(lk);ck(b==[1,1],'circle_vertex_link')
 ck(betti(K)==expected,'global_rational_homology');ck(betti(K,2)==([1,1,1] if 'projective' in name else [1,0,1]),'global_mod2_homology')
 data=[]
 if name!='projective_plane':
  ck(cliques(K)==K,'flag_property')
  for f in sorted(K,key=lambda x:(len(x),x)):
   C=puncture(K,f);b=betti(C);bp=betti(C,2)
   b+= [0]*(3-len(b));bp += [0]*(3-len(bp))
   ck(b==([1,1,0] if 'projective' in name else [1,0,0]),'all_simplex_deletions_Q')
   ck(bp==b,'all_simplex_deletions_F2');data.append((f,b))
  sq=square(K);ck((sq is None)==(name=='icosahedral_sphere'),'hyperbolicity_square_gate')
  row={'name':name,'vertices':len(cs[0]),'edges':len(cs[1]),'triangles':len(cs[2]),'nonempty_simplex_deletions':len(data),'induced_square':sq,'predicted_cd_Q':2 if 'projective' in name else 3,'predicted_cd_Z':3};rows.append(row)
# A canonical square in the barycentric subdivision across any original edge.
for e in [f for f in RP if len(f)==2]:
 ts=[f for f in RP if len(f)==3 and set(e)<=set(f)];ck(len(ts)==2,'two_cofaces')
 ids=[labels.index((e[0],)),labels.index(ts[0]),labels.index((e[1],)),labels.index(ts[1])];vs,E=graph(BRP)
 ck(all(frozenset((ids[i],ids[(i+1)%4])) in E for i in range(4)) and frozenset((ids[0],ids[2])) not in E and frozenset((ids[1],ids[3])) not in E,'barycentric_induced_square')
for n in range(2,101):ck(3*n>=2*(n+1),'manifold_ratio_bound')
print(json.dumps({'assertions':checks,'categories':cats,'models':rows,'scope':'All simplex deletions in two explicit flag surface nerves; only the sphere model passes the no-square gate. General manifold exclusion proved in TURN_2.md.'},sort_keys=True,indent=2))
