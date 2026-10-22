from exact_geometry import *
from functools import lru_cache
from pathlib import Path
from hashlib import sha256
import json,sys
c=0;cases=[];cert=[]
def ck(v):
 global c
 c+=1;assert v
def hull(P):
 P=sorted(set(P));H=[]
 for pts in [P,P[::-1]]:
  C=[]
  for p in pts:
   while len(C)>1 and cross(sub(C[-1],C[-2]),sub(p,C[-1]))<=0:C.pop()
   C.append(p)
  H+=C[:-1]
 return H
for m in [2,3]:
 K=list(map(pt,[(0,0),(m,0),(1,1),(0,1)]));D=hull([sub(a,b) for a in K for b in K]);U=[pt((x,y)) for x in range(-m,m+1) for y in range(-1,2) if inside(pt((x,y)),D)];V=[pt((x,y)) for x in range(-2*m,2*m+1) for y in range(-2,3) if inside(pt((F(x,2),F(y,2))),D)]
 ps=[[(a+x,b+y) for a,b in K] for x,y in U];cv=masks(ps);maximal=[a for a in cv if not any(a!=b and a&b==a for b in cv)];bybit=[[a for a in maximal if a>>i&1] for i in range(len(U))]
 @lru_cache(None)
 def tau(S):
  if not S:return 0
  i=(S&-S).bit_length()-1
  return 1+min(tau(S&~a) for a in bybit[i])
 bad=[];critical=[]
 for S in range(1,1<<len(U)):
  t=tau(S);ck(1<=t<=S.bit_count())
  if t<=3:continue
  bad.append(S)
  if all(tau(S^(1<<i))<=3 for i in range(len(U)) if S>>i&1):critical.append(S);ck(t==4)
 entries=[]
 for S in critical:
  T=[t for i,t in enumerate(U) if S>>i&1];C=[]
  for v in V:
   good=all(inside(sub(t,v),D) for t in T);c+=1
   if good:C.append(v)
  ck(C==[pt((0,0))]);entries.append({'mask':S,'common_neighbors':[[int(x),int(y)] for x,y in C]})
 for S in bad:ck(any(S&T==T for T in critical))
 cert.append({'m':m,'U':[[int(x),int(y)] for x,y in U],'V':[[int(x),int(y)] for x,y in V],'critical':entries})
 cases.append({'m':m,'U_size':len(U),'V_size':len(V),'subsets':1<<len(U),'bad_subsets':len(bad),'critical_subsets':len(critical)})
b=(json.dumps(cert,indent=2,sort_keys=True)+'\n').encode();p=Path(__file__).resolve().parent/'LATTICE_CERTIFICATE.json'
if '--emit' in sys.argv:p.write_bytes(b)
else:ck(p.read_bytes()==b)
# The emission also counts the successful exact equality for an identical receipt.
if '--emit' in sys.argv:ck(p.read_bytes()==b)
print(json.dumps({'assertions':c,'cases':cases,'certificate_sha256':sha256(b).hexdigest(),'scope':'Exhaustive finite reduction proves all integer-translated families for exactly the stated two bodies; real-translation conjecture remains open'},indent=2,sort_keys=True))
