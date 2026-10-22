"""Independent combinatorial check of HSWW v2 Proposition 8.7 numbers.
Conditional on the cone-image identification of Proposition 8.1; not a
certification of the external algebro-geometric proof or a two-summand bridge.
"""
from itertools import combinations
from fractions import Fraction
import json

def rank(a):
 a=[[Fraction(x) for x in row] for row in a];r=0
 if not a:return 0
 for col in range(len(a[0])):
  p=next((i for i in range(r,len(a)) if a[i][col]),None)
  if p is None:continue
  a[r],a[p]=a[p],a[r];v=a[r][col];a[r]=[x/v for x in a[r]]
  for i in range(r+1,len(a)):
   v=a[i][col]
   if v:a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r

def topo(triangles):
 levels=[sorted({x for t in triangles for x in combinations(t,k)}) for k in (1,2,3)]
 ranks=[]
 for k in (1,2):
  ix={x:i for i,x in enumerate(levels[k-1])};mat=[[0]*len(levels[k]) for _ in levels[k-1]]
  for j,s in enumerate(levels[k]):
   for i in range(k+1):mat[ix[s[:i]+s[i+1:]]][j]=(-1)**i
  ranks.append(rank(mat))
 return {'f_vector':list(map(len,levels)),'rational_boundary_ranks':ranks,
 'ordinary_betti':[len(levels[0])-ranks[0],len(levels[1])-sum(ranks),len(levels[2])-ranks[1]]}
t=set(combinations(range(10),3))
for face,new in [((1,2,3),10),((4,5,6),11)]:
 t.remove(face)
 t.update(tuple(sorted(edge+(new,))) for edge in combinations(face,2))
a=topo(t);b=topo({tuple(sorted(10 if x==11 else x for x in f)) for f in t})
if a!={'f_vector':[12,51,124],'rational_boundary_ranks':[11,40],'ordinary_betti':[1,0,84]}:raise RuntimeError(a)
if b!={'f_vector':[11,51,124],'rational_boundary_ranks':[10,40],'ordinary_betti':[1,1,84]}:raise RuntimeError(b)
print(json.dumps({'before_ray_identification':a,'after_ray_identification':b,'conditional_on_external_Prop_8_1':True,'establishes_exact_target_representation':False},indent=2))
