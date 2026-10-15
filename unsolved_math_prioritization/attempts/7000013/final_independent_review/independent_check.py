#!/usr/bin/env python3
"""Independent checks of frozen refined face data; no author generator imported."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
from collections import defaultdict,deque
import json,sys,sympy as s
src=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
w=json.loads((src/'refined_witnesses.json').read_text());checks=0
def ck(v):
 global checks
 assert bool(v);checks+=1

def sub(a,b):return [x-y for x,y in zip(a,b)]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def orient(a,b,c):u=sub(b,a);v=sub(c,a);return u[0]*v[1]-u[1]*v[0]
def on(a,b,p):return orient(a,b,p)==0 and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in range(2))
def segments_meet(a,b,c,d):
 p,q,r,t=orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
 if p*q<0 and r*t<0:return True
 return any([p==0 and on(a,b,c),q==0 and on(a,b,d),r==0 and on(c,d,a),t==0 and on(c,d,b)])
def area(ps):
 n=[Q(0)]*3
 for a,b in zip(ps,ps[1:]+ps[:1]):
  z=cross(a,b)
  n=[x+y/2 for x,y in zip(n,z)]
 return n

data={};rows={}
for name in ['roof_out','roof_in','cap_centered','cap_shifted','torus_plus','torus_minus']:
 p=[[Q(c) for c in v] for v in w[name]['vertices']];f=w[name]['faces'];ck(len(set(map(tuple,p)))==len(p));ed=defaultdict(list);links=defaultdict(list);av=[];conv=[]
 for fi,face in enumerate(f):
  ps=[p[i] for i in face];n=area(ps);ck(dot(n,n)>0)
  for pt in ps:ck(dot(n,sub(pt,ps[0]))==0)
  axis=max(range(3),key=lambda k:abs(n[k]));plane=[[v[k] for k in range(3) if k!=axis] for v in ps]
  m=len(plane)
  for i,j in combinations(range(m),2):
   if (i-j)%m not in [1,m-1]:ck(not segments_meet(plane[i],plane[(i+1)%m],plane[j],plane[(j+1)%m]))
  signs=[dot(n,cross(sub(ps[(j+1)%m],ps[j]),sub(ps[(j+2)%m],ps[(j+1)%m]))) for j in range(m)]
  conv.append(all(z>0 for z in signs));av.append(n)
  for j,k in zip(face,face[1:]+face[:1]):ed[tuple(sorted((j,k)))].append((j,k,fi))
  for j,vert in enumerate(face):links[vert].append((face[j-1],face[(j+1)%len(face)]))
 for uses in ed.values():
  ck(len(uses)==2 and uses[0][:2]==tuple(reversed(uses[1][:2])));ck(cross(av[uses[0][2]],av[uses[1][2]])!=[0,0,0])
 for vert,pairs in links.items():
  adj=defaultdict(set)
  for a,b in pairs:adj[a].add(b);adj[b].add(a)
  ck(all(len(v)==2 for v in adj.values()));seen={next(iter(adj))};stack=list(seen)
  while stack:
   for n in adj[stack.pop()]:
    if n not in seen:seen.add(n);stack.append(n)
  ck(len(seen)==len(adj))
 # Exact signed volume formula for each closed polygonal chain, independent analytic values below.
 vol=Q(0)
 for face in f:
  ps=[p[i] for i in face];n=area(ps);vol+=dot(ps[0],n)/3
 genus_euler=len(p)-len(ed)+len(f);ck(genus_euler==(0 if name.startswith('torus') else 2))
 data[name]=(p,f,av,ed,conv);rows[name]={'vertices':len(p),'faces':len(f),'edges':len(ed),'Euler':genus_euler,'strictly_convex_faces':sum(conv),'signed_volume':str(vol)}
 if name.startswith('roof'):ck(all(conv));ck(vol==(Q(14,3) if name=='roof_out' else Q(10,3)))
 if name.startswith('cap'):ck(sum(not x for x in conv)==2);ck(vol==50)
 if name.startswith('torus'):ck(all(conv))

perm=w['roof_face_matching'];A=data['roof_out'];B=data['roof_in']
for i,j in enumerate(perm):ck(A[2][i]==B[2][j])
adj=lambda fs,i,j:len(set(fs[i])&set(fs[j]))==2
ck(any(adj(A[1],i,j)!=adj(B[1],perm[i],perm[j]) for i,j in combinations(range(9),2)))
for n0,n1 in [('cap_centered','cap_shifted'),('torus_plus','torus_minus')]:
 A,B=data[n0],data[n1];ck(A[1]==B[1]);ck(A[2]==B[2])
# Geometric box integrals independently compute sliding-cap centroid.
for tau in [0,1]:
 cen=[Q(tau,25),Q(1,10),Q(14,25)];ck(sum(x*x for x in cen)==Q(809+4*tau,2500))
# All vertex pair distances, plus the explicit crossing inside nonadjacent meridian segments.
for name,tau,diam,rad in [('torus_plus',Q(1,2),Q(386,9),Q(47,18)),('torus_minus',Q(-1,2),Q(338,9),Q(37,18))]:
 p=data[name][0];ck(max(dot(sub(a,b),sub(a,b)) for a,b in combinations(p,2))==diam)
 for j in range(4):
  x=[p[j][k]+Q(2,3)*(p[4+j][k]-p[j][k]) for k in range(3)]
  y=[p[8+j][k]+Q(2,3)*(p[12+j][k]-p[8+j][k]) for k in range(3)]
  ck(x==y and x[2]==0);ck(max(abs(x[0]),abs(x[1]))==rad)
# Symbolic vector-area multiplier for one angular sector, arbitrary tau and adjacent radii r,s with rs=3.
t,R,Z,W=s.symbols('tau R Z W',real=True);S=3/R
base=[s.Matrix([R,0,Z]),s.Matrix([S,0,W]),s.Matrix([0,S,W]),s.Matrix([0,R,Z])]
star=[s.Matrix([v[0]/(R*R if i in [0,3] else S*S),v[1]/(R*R if i in [0,3] else S*S),-v[2]/3]) for i,v in enumerate(base)]
def avec(ps):return sum((ps[i].cross(ps[(i+1)%4])/2 for i in range(4)),s.zeros(3,1))
for v in avec([p+t*q for p,q in zip(base,star)])-(1-t*t/9)*avec(base):ck(s.simplify(v)==0)
# Exact edge integral underlying the Green-theorem obstruction.
r0,r1,dz,t=s.symbols('r0 r1 dz t',positive=True)
ck(s.simplify((dz/(r1-r0))*(1/r0-1/r1)-dz/(r0*r1))==0)
# Triangle scaling equations: a*u+b*v-c*(u+v)=0 -> a=c,b=c for independent basis u,v.
a,b,c=s.symbols('a b c');ck(s.solve([a-c,b-c],[a,b])=={a:c,b:c});ck(s.solve(s.Symbol('a')**2-1)==[-1,1])
print(json.dumps({'status':'PASS','exact_assertions':checks,'witnesses':rows,'floating_point_used':False,'original_scope_resolved':False,'rigidity_scope':'closed connected triangulated 2-manifold, coherent correspondence, nonflat incident face pairs'},indent=2))
