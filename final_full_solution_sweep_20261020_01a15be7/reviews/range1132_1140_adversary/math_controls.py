#!/usr/bin/env python3
"""New bounded exact controls, independent of archived executable programs."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import zipfile,json,math
H=Path(__file__).resolve().parent;P=H/'private'
def need(ok,why):
 if not ok:raise RuntimeError(why)
z=zipfile.ZipFile(P/'record23063072/OWR-14298580-008-source.zip')
cert=z.read('reproducibility/verifier/certificate_Sigma_30_47_83.txt').decode()
points=[tuple(map(int,line.split())) for line in cert.splitlines() if line and not line.startswith('#')]
N=30*47*83-30*47-30*83-47*83
need(F(-1)+F(29,30)+F(1,47)+F(1,83)==F(-1,117030),'Seifert normalization')
tau=[0]
for i in range(N+1):tau.append(tau[-1]+1+i-(29*i+29)//30-(i+46)//47-(i+82)//83)
need(len(points)==1707 and points[0]==(0,0) and points[-1]==(N+1,0),'certificate endpoints')
for (a,x),(b,y) in zip(points,points[1:]):
 need(a<b and tau[a]==x and tau[b]==y,'certificate sample')
 segment=tau[a:b+1];need(all(segment[j]<=segment[j+1] for j in range(len(segment)-1)) or all(segment[j]>=segment[j+1] for j in range(len(segment)-1)),'certificate interval')
levels=[x[1] for x in points];bars=Counter();globalmin=min(range(len(levels)),key=lambda j:(levels[j],j))
# Every finite component born at a local minimum dies at the lowest path barrier
# connecting it to a strictly older minimum. Scan each direction independently.
for m,birth in enumerate(levels):
 if m==globalmin or (m>0 and levels[m-1]<=birth) or (m+1<len(levels) and levels[m+1]<=birth):continue
 walls=[]
 for step in [-1,1]:
  wall=birth;j=m+step
  while 0<=j<len(levels):
   wall=max(wall,levels[j])
   if (levels[j],j)<(birth,m):walls.append(wall);break
   j+=step
 need(walls,'finite component older anchor');length=min(walls)-birth
 if length>0:bars[length]+=1
need(max(bars)==16 and bars[15]==0 and sum(bars.values())==853 and sum(k*v for k,v in bars.items())==4864,'barcode invariants')
# Polynomial operations over Q generate the fourth centered count moment
# directly from the inclusion probabilities; integrate exactly over [0,1/2].
def add(a,b):
 r=[F(0)]*max(len(a),len(b))
 for i,x in enumerate(a):r[i]+=x
 for i,x in enumerate(b):r[i]+=x
 return r
def mul(a,b):
 r=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):r[i+j]+=x*y
 return r
def scale(a,c):return [c*x for x in a]
def moment(q):
 probs=[add([1,-3,3],scale(q,-1)),add([0,3,-6],scale(q,3)),add([0,0,3],scale(q,-3)),q]
 total=[F(0)]
 for k,p in enumerate(probs):
  power=[F(1)]
  for _ in range(4):power=mul(power,[F(k,3),F(-1)])
  total=add(total,mul(p,power))
 return 2*sum(c*F(1,2)**(i+1)/(i+1) for i,c in enumerate(total))
lattice=moment([F(0),F(0),F(1,2)]);iid=moment([F(0),F(0),F(0),F(1)])
need(lattice==F(19,1620) and iid==F(4,405) and lattice-iid==F(1,540),'moments')
print(json.dumps({'status':'PASS','scope':'Exact certificate/barcode and moment controls; no rerun of archived code or independent HF analytic foundations','pr1132':{'tau_samples':len(tau),'turning_points':len(points),'min_tau':min(tau),'blocks':sum(bars.values()),'dimension':sum(k*v for k,v in bars.items()),'lengths':dict(sorted(bars.items()))},'pr1135':{'lattice':str(lattice),'iid':str(iid),'excess':str(lattice-iid)}},sort_keys=True))
