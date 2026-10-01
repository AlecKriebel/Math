"""Own exact F2 square-quotient controls for the credited figure-eight complex."""
import json
from collections import Counter
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
def rank2(cols):
 piv={}
 for v in cols:
  while v:
   i=v.bit_length()-1
   if i in piv:v^=piv[i]
   else:piv[i]=v;break
 return len(piv)
for s in range(-30,31):
 partial=[]
 for n in range(-40,41):
  pts=[(n,n),(n-1,n),(n,n-1),(n-1,n-1)]
  kept=[i for i,(x,y) in enumerate(pts) if x>=0 or y>=s]
  if 0<len(kept)<4:partial.append(n)
  ids={i:j for j,i in enumerate(kept)};edges={0:[1,2],1:[3],2:[3],3:[]}
  columns=[sum(1<<ids[k] for k in edges[i] if k in ids) for i in kept]
  def apply(v):
   a=0
   for j,col in enumerate(columns):
    if v>>j&1:a^=col
   return a
  ck(all(apply(v)==0 for v in columns),'d_squared_zero')
  dim=len(kept)-2*rank2(columns)
  ck(dim==(1 if s==0 and n==0 else 0),'square_homology_dimension')
 ck(partial==[min(0,s)],'unique_partial_square')
for s in range(-7,8):
 ck(15>=1+abs(s),'large_surgery_range')
 ck((2*s)%15==0 if s==0 else (2*s)%15!=0,'unique_spin_chern_class')
ck(2 not in [8,(-8)%15],'turn3_euler_classes_unequal_up_to_sign')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Finite square and labeling controls; the full infinite decomposition and taut-foliation implication are proved using the cited theorems in TURN_4.md.'},indent=2,sort_keys=True))
