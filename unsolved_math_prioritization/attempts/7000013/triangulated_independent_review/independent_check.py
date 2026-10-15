#!/usr/bin/env python3
"""Independent witness validation; rational projected-area and overlap checks.
Reads only frozen witness data, not the author's generator.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict,deque
from itertools import combinations
import json
SRC=Path('/workspace/shared/math-7000013-audit/unsolved_math_prioritization/attempts/7000013/witness.json')
data=json.loads(SRC.read_text());faces=data['oriented_triangles'];sets=[[[Q(x) for x in p] for p in data[n]] for n in ['vertices','image_vertices']];checks=0

def ck(x):
 global checks
 assert x;checks+=1

def minus(a,b):return [x-y for x,y in zip(a,b)]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def cv(points,tri):a,b,c=[points[i] for i in tri];return cross(minus(b,a),minus(c,a))
def twice_area(poly):return sum(det(p,poly[(i+1)%len(poly)]) for i,p in enumerate(poly)) if len(poly)>=3 else Q(0)
def clip(poly,axis,cut,positive):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  va=(a[axis]-cut)*(1 if positive else -1);vb=(b[axis]-cut)*(1 if positive else -1)
  if va>=0:out.append(a)
  if va*vb<0:out.append([a[k]+va/(va-vb)*(b[k]-a[k]) for k in range(2)])
 return out

def disjoint_interiors(a,b):
 for poly in [a,b]:
  for u,v in zip(poly,poly[1:]+poly[:1]):
   dx,dy=minus(v,u);vals1=[-dy*p[0]+dx*p[1] for p in a];vals2=[-dy*p[0]+dx*p[1] for p in b]
   if max(vals1)<=min(vals2) or max(vals2)<=min(vals1):return True
 return False

ck(len(faces)==530);ck(len(sets[0])==len(sets[1])==267)
for tri in faces:
 ck(len(set(tri))==3);a=cv(sets[0],tri);b=cv(sets[1],tri);ck(a==b and a!=[0,0,0])
edges=defaultdict(list);links=defaultdict(list)
for tri in faces:
 for i,j in zip(tri,tri[1:]+tri[:1]):edges[tuple(sorted((i,j)))].append((i,j))
 for i in tri:links[i].append([j for j in tri if j!=i])
for uses in edges.values():ck(len(uses)==2 and uses[0]==tuple(reversed(uses[1])))
ck(len(edges)==795 and 267-795+530==2)
for i,pairs in links.items():
 adj=defaultdict(set)
 for a,b in pairs:adj[a].add(b);adj[b].add(a)
 ck(all(len(v)==2 for v in adj.values()))
 seen={next(iter(adj))};queue=deque(seen)
 while queue:
  for v in adj[queue.popleft()]:
   if v not in seen:seen.add(v);queue.append(v)
 ck(len(seen)==len(adj))
receipts=[]
for kind,points in enumerate(sets):
 ck(len(set(map(tuple,points)))==267)
 bumpx=(Q(-1,2)+kind,Q(1,2)+kind);groups=defaultdict(list);areas=defaultdict(Q);vol=Q(0);moment=[Q(0)]*3
 for tri in faces:
  p=[points[i] for i in tri];normal=cv(points,tri);axis=next(i for i in range(3) if normal[i]);ck(sum(v!=0 for v in normal)==1)
  value=p[0][axis];ck(all(v[axis]==value for v in p));project=[[v[j] for j in range(3) if j!=axis] for v in p]
  groups[(axis,value)].append(project);areas[(axis,value)]+=abs(normal[axis])/2
  if axis==2:
   ck(value in [0,1,3]);ck((normal[2]>0)==(value!=0))
   bounds=[[-10,10],[-8,8]] if value!=3 else [bumpx,[Q(-1,2),Q(1,2)]]
   for v in p:ck(all(bounds[j][0]<=v[j]<=bounds[j][1] for j in range(2)))
   if value==1:
    clipped=[v[:2] for v in p]
    for ax,lo,hi in [(0,*bumpx),(1,Q(-1,2),Q(1,2))]:
     if clipped:clipped=clip(clipped,ax,lo,True)
     if clipped:clipped=clip(clipped,ax,hi,False)
    ck(twice_area(clipped)==0)
   area=normal[2]/2;vol+=area*value
   for j in range(2):moment[j]+=area*value*sum(v[j] for v in p)/3
   moment[2]+=area*value*value/2
  else:
   other=1-axis
   if max(v[2] for v in p)<=1:
    bound=10 if axis==0 else 8;ck(abs(value)==bound);ck((normal[axis]>0)==(value>0))
    for v in p:ck(0<=v[2]<=1 and abs(v[other])<=(8 if axis==0 else 10))
   else:
    ends=bumpx if axis==0 else(Q(-1,2),Q(1,2));ck(value in ends);ck((normal[axis]>0)==(value==ends[1]))
    bounds=(Q(-1,2),Q(1,2)) if axis==0 else bumpx
    for v in p:ck(1<=v[2]<=3 and bounds[0]<=v[other]<=bounds[1])
 # Each planar patch is independently checked free of overlapping triangle interiors.
 pairchecks=0
 for group in groups.values():
  for a,b in combinations(group,2):ck(disjoint_interiors(a,b));pairchecks+=1
 ck(areas[(2,Q(0))]==320);ck(areas[(2,Q(1))]==319);ck(areas[(2,Q(3))]==1)
 ck(sorted(areas.values())==[1,2,2,2,2,16,16,20,20,319,320]);ck(vol==322)
 centroid=[a/vol for a in moment];ck(centroid==[Q(kind,161),Q(0),Q(82,161)])
 receipts.append({'triangles_nonoverlapping_coplanar_pairs':pairchecks,'patch_areas':sorted(map(str,areas.values())),'volume':str(vol),'centroid':list(map(str,centroid)),'bottom_center_distance_squared':str(sum(z*z for z in centroid))})
ck(receipts[0]['bottom_center_distance_squared']!=receipts[1]['bottom_center_distance_squared'])
print(json.dumps({'status':'PASS','exact_assertions':checks,'surfaces':receipts,'floating_point_used':False,'category':'finite triangulated embedded PL sphere; coplanar adjacent faces allowed'},indent=2))
