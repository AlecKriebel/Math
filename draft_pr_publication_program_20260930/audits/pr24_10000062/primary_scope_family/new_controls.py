#!/usr/bin/env python3
"""Independent exact controls, no imports from original/review programs.
Finite checks supplement, rather than replace, REPORT's universal arguments.
"""
from fractions import Fraction as F
from itertools import combinations,product
from collections import Counter
from functools import cmp_to_key
from math import gcd,lcm
from pathlib import Path
import json

def sub(a,b): return a[0]-b[0],a[1]-b[1]
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def closest(e):
 a,b=e;v=sub(b,a);t=max(F(0),min(F(1),-dot(a,v)/dot(v,v)))
 p=(a[0]+t*v[0],a[1]+t*v[1]);return dot(p,p),p

def line(a,b,c):
 v=sub(b,a);q=(-v[1],v[0],v[1]*a[0]-v[0]*a[1])
 if q[0]*c[0]+q[1]*c[1]+q[2]<0:q=tuple(-z for z in q)
 mul=lcm(*(z.denominator for z in q));q=tuple(int(z*mul) for z in q);g=gcd(*q)
 return tuple(z//g for z in q)

def angle_cmp(u,v):
 h=lambda p:0 if p[1]>0 or (p[1]==0 and p[0]>=0) else 1
 if h(u)!=h(v):return h(u)-h(v)
 d=det(u,v);return -1 if d>0 else 1 if d<0 else 0

def make(sign,rootj=0,rootk=0,upper=False,guard=3,mirror=True):
 dd=lambda j:F(1)+F(sign(j),2)
 aa={0:F(0)}
 for j in range(0,rootj+guard+2):aa[j+1]=aa[j]+dd(j)+1
 for j in range(-1,rootj-guard-2,-1):aa[j]=aa[j+1]-dd(j)-1
 center=(aa[rootj]+2*rootk+(dd(rootj) if upper else 0),F(4*rootj+(1 if upper else 0)))
 def transform(p):
  x,y=sub(p,center)
  if upper:x,y=-x,-y
  if mirror and dd(rootj)==F(3,2):x=-x
  return x,y
 rows=[]
 for j in range(rootj-guard,rootj+guard+1):rows.extend([(aa[j],F(4*j)),(aa[j]+dd(j),F(4*j+1))])
 ts=set()
 for (a,y),(b,z) in zip(rows,rows[1:]):
  # Independently form a strip parallelogram between matching row points,
  # split from its lower-right corner to its upper-left corner.
  for k in range(rootk-13,rootk+14):
   ll=(a+2*k,y);lr=(a+2*k+2,y);ul=(b+2*k,z);ur=(b+2*k+2,z)
   ts.add(tuple(sorted(transform(v) for v in [ll,lr,ul])))
   ts.add(tuple(sorted(transform(v) for v in [lr,ur,ul])))
 return ts

def sig(ts,r2=F(10),include_points=True):
 es={tuple(sorted(e)) for t in ts for e in combinations(t,2)};vs={v for e in es for v in e}
 edge_kind={e:closest(e) for e in es}
 visible_vs=frozenset(v for v in vs if dot(v,v)<=r2)
 keys={};boundary_points=set()
 for e,(d,p) in edge_kind.items():
  if d<r2:keys[e]=('seg',e)
  elif d==r2 and include_points:boundary_points.add(p)
 # Canonical labels for collapsed external edge pieces use exact cyclic
 # order around their retained endpoint, not their off-disk endpoint.
 for p in boundary_points:
  incident=[e for e in es if p in e]
  incident.sort(key=cmp_to_key(lambda e,f:angle_cmp(sub(e[1] if e[0]==p else e[0],p),sub(f[1] if f[0]==p else f[0],p))))
  assert len(incident)==6
  for rank,e in enumerate(incident):
   if edge_kind[e][0]==r2:keys[e]=('ptedge',p,rank)
 fs=[];incidences=[];pointface_counts=Counter();areafaces=0
 for t in ts:
  a,b,c=t;q=[line(a,b,c),line(b,c,a),line(c,a,b)]
  minimum=(F(0),(F(0),F(0))) if all(z[2]>=0 for z in q) else min(closest(e) for e in combinations(t,2))
  d,p=minimum
  if d>r2 or (d==r2 and not include_points):continue
  ekeys=tuple(sorted(keys[e] for e in combinations(t,2) if e in keys))
  if d<r2:
   active=tuple(sorted(line(*e,next(v for v in t if v not in e)) for e in combinations(t,2) if edge_kind[tuple(sorted(e))][0]<r2))
   fk=('face',active);areafaces+=1
  else:fk=('ptface',p,ekeys);pointface_counts[p]+=1
  fs.append(fk);incidences.append((fk,ekeys,tuple(v for v in t if v in visible_vs)))
 edgeinc=tuple(sorted((keys[e],tuple(v for v in e if v in visible_vs)) for e in keys))
 return (visible_vs,frozenset(keys.values()),tuple(sorted(fs)),edgeinc,tuple(sorted(incidences))),{'vertices':len(visible_vs),'positive_edges':sum(k[0]=='seg' for k in keys.values()),'singleton_edges':sum(k[0]=='ptedge' for k in keys.values()),'area_faces':areafaces,'singleton_faces':sum(pointface_counts.values())}

def main():
 baseline,counts=sig(make(lambda j:-1));checks=0;cases=[]
 # Six independent bits, shifted centers in both directions and row types;
 # the seventh/outer bits follow two deliberately unrelated continuations.
 for bits in product([-1,1],repeat=6):
  f=lambda j,bits=bits:bits[j+3] if -3<=j<=2 else (1 if j%3 else -1)
  for upper in [False,True]:
   rootj=(-1,0,1)[sum(bits)%3];rootk=sum((i+1)*b for i,b in enumerate(bits))%5-2
   s,c=sig(make(f,rootj,rootk,upper));assert s==baseline,(bits,rootj,rootk,upper);checks+=1
   cases.append({'bits':bits,'rootj':rootj,'rootk':rootk,'upper':upper,'pass':True})
 # Guard enlargement cannot change any positive or collapsed cell/incidence.
 f=lambda j: -1 if j in [-7,-4,0,5,9] else 1
 for upper in [False,True]:
  assert sig(make(f,0,-3,upper,guard=3))[0]==sig(make(f,0,-3,upper,guard=7))[0];checks+=1
 # Boundary handling is material: deleting collapsed traces changes signature.
 assert sig(make(f),include_points=False)[0]!=sig(make(f))[0];checks+=1
 # Whole-disk versus corona and fixed-radius controls.
 f0=lambda j:-1
 f1=lambda j:1 if j==-1 else -1
 assert sig(make(f0))[0]==sig(make(f1))[0];checks+=1
 assert sig(make(f0),F(1001,100))[0]!=sig(make(f1),F(1001,100))[0];checks+=1
 # New independent symmetry controls: geometrically exact edge action of
 # periodic, single-defect, complemented defect and reversal cases.
 symmetry=[]
 tests=[('all_minus',lambda j:-1,[(1,1,0,0),(1,1,F(3,2),4),(-1,-1,F(1,2),1)]),
        ('single_minus',lambda j:-1 if j==0 else 1,[(1,1,2,0),(-1,-1,F(1,2),1)]),
        ('single_plus',lambda j:1 if j==0 else -1,[(1,1,2,0),(-1,-1,F(3,2),1)])]
 for name,fn,maps in tests:
  ts=make(fn,mirror=False,guard=5);edges={tuple(sorted(e)) for t in ts for e in combinations(t,2)}
  for sx,sy,tx,ty in maps:
   transformed={tuple(sorted((sx*v[0]+tx,sy*v[1]+ty) for v in e)) for e in edges}
   def interior(e):return all(-8<v[0]<8 and -8<v[1]<8 for v in e)
   expected={e for e in edges if interior(e)};actual={e for e in transformed if interior(e)}
   assert expected==actual,(name,(sx,sy,tx,ty));checks+=1;symmetry.append({'sequence':name,'map':[sx,sy,str(tx),str(ty)],'interior_edge_action':'passed'})
 # Defect forbids a vertical period; constant and alternating controls allow
 # one/two-layer screw translations, so noncocompactness is sequence-specific.
 for period,fn in [(1,lambda j:-1),(2,lambda j:1 if j%2 else -1)]:
  tx=sum(F(1)+F(fn(j),2)+1 for j in range(period));ts=make(fn,guard=5,mirror=False)
  es={tuple(sorted(e)) for t in ts for e in combinations(t,2)}
  mov={tuple(sorted((v[0]+tx,v[1]+4*period) for v in e)) for e in es}
  inside=lambda e:all(-8<v[0]<8 and -6<v[1]<6 for v in e)
  assert {e for e in es if inside(e)}=={e for e in mov if inside(e)};checks+=1
 for m in range(-8,9):
  if m:assert any(((-1 if j==0 else 1)!=(-1 if j+m==0 else 1)) for j in [0,-m]);checks+=1
 out={'status':'passed','arithmetic':'Fraction','checks':checks,'rooted_full_cell_incidence_cases':len(cases),'counts':counts,'controls':['guard 3 to 7','collapsed boundary traces deletion','larger radius distinguishes prior chirality','periodic sequence vertical period','single defect reversal half-turn','complemented single defect half-turn','alternating two-layer period','nonzero single-defect shifts rejected'],'symmetry_controls':symmetry,'cases':cases,'limits':'Finite tests do not establish infinite locality, complete symmetry, or global priority. REPORT supplies analytic audit.'}
 Path(__file__).with_name('new_control_results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
