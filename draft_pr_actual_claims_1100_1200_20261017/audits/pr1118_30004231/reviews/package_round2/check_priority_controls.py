from fractions import Fraction
from itertools import combinations,product
import json,pathlib
h=pathlib.Path(__file__).resolve().parent
def req(x,m):
 if not x:raise RuntimeError(m)
def rank(a):
 a=[[Fraction(x) for x in r] for r in a];k=0
 for j in range(len(a[0]) if a else 0):
  p=next((i for i in range(k,len(a)) if a[i][j]),None)
  if p is None:continue
  a[k],a[p]=a[p],a[k];d=a[k][j];a[k]=[x/d for x in a[k]]
  for i in range(k+1,len(a)):
   if a[i][j]:
    c=a[i][j];a[i]=[x-c*y for x,y in zip(a[i],a[k])]
  k+=1
  if k==len(a):break
 return k
def homology(triangles):
 levels=[sorted({tuple(c) for t in triangles for c in combinations(sorted(t),i)}) for i in (1,2,3)]
 ranks=[]
 for k in (1,2):
  idx={t:i for i,t in enumerate(levels[k-1])};a=[[0]*len(levels[k]) for _ in levels[k-1]]
  for j,t in enumerate(levels[k]):
   for i in range(k+1):a[idx[t[:i]+t[i+1:]]][j]=(-1)**i
  ranks.append(rank(a))
 return {'fvector':list(map(len,levels)),'boundary_ranks':ranks,'betti':[len(levels[0])-ranks[0],len(levels[1])-sum(ranks),len(levels[2])-ranks[1]]}
triangles={frozenset(t) for t in combinations(range(10),3)}
for face,v in [(frozenset((1,2,3)),10),(frozenset((4,5,6)),11)]:
 req(face in triangles,'stellar face absent');triangles.remove(face)
 triangles|={frozenset(edge)|{v} for edge in combinations(face,2)}
before=homology(triangles)
after=homology({frozenset(10 if x==11 else x for x in t) for t in triangles})
req(before=={'fvector':[12,51,124],'boundary_ranks':[11,40],'betti':[1,0,84]},'before')
req(after=={'fvector':[11,51,124],'boundary_ranks':[10,40],'betti':[1,1,84]},'v2 link')
# Distinct two-summand representations with identical complete sum normal fan.
# The fan of Q equals that of 2Q by positive scaling. Canonical Q+Q faces
# always have dimensions (r,r,r), never positive/additive.
D=[(0,0,0,0)]+[tuple(int(i==j) for i in range(4)) for j in range(4)]
Q=set(tuple(x-y for x,y in zip(a,b)) for a in D for b in D)
def exp(v,u):
 top=max(sum(x*y for x,y in zip(a,u)) for a in v)
 return frozenset(a for a in v if sum(x*y for x,y in zip(a,u))==top)
def dim(v):
 v=list(v);return rank([[x-y for x,y in zip(a,v[0])] for a in v[1:]])
faces={exp(Q,u) for u in product(range(-2,3),repeat=4)}
req(len(faces)==181,'Q fan supports')
req(all(dim(f)==dim({tuple(2*x for x in a) for a in f}) for f in faces),'scaling dimension')
req(not any(dim(f)>0 and dim(f)==2*dim(f) for f in faces),'Q+Q empty exact filter')
r={'HSWW_v2_combinatorial_check':{'before_identification':before,'after_identification':after,'limit':'Checks the stated twice-subdivided simplex skeleton and vertex identification, conditional on the primary geometric fan identification; no independent proof of the whole schön embedding claimed.'},'normal_fan_only_transfer_control':{'Q_nonempty_support_faces':len(faces),'Q_plus_Q_qualifiers':0,'original_D_minus_D_qualifiers':50,'conclusion':'The complete sum normal fan alone does not determine the printed exact positive/additive filtered poset. No impossibility of other representations is claimed.'}}
(h/'evidence/PRIORITY_CONTROLS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
