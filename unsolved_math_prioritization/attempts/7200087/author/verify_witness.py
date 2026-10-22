#!/usr/bin/env python3
"""Independent exact checks of Mizhaev's 2026 integer realization.

Input mathematical data: R. Mizhaev, arXiv:2609.17700v1, Tables 1--2
and Section 4. Code is newly written; it does not execute source-paper code.
Only Python standard-library Fraction arithmetic is used.
"""
from fractions import Fraction as Q
from itertools import combinations
from collections import defaultdict, Counter
import json

VERTICES = [
 (-72,84,18),(-36,112,102),(72,-84,18),(36,-112,102),
 (0,300,234),(-84,48,-18),(9,147,207),(0,-300,234),
 (84,-48,-18),(-112,-36,-102),(48,84,18),(-147,9,-207),
 (-9,-147,207),(84,72,-18),(112,36,-102),(-48,-84,18),
 (147,-9,-207),(-18,126,144),(-126,-18,-144),(-300,0,-234),
 (-84,-72,-18),(18,-126,144),(126,18,-144),(300,0,-234)]
FACES = [
 [6,10,16,22,18,7,5,1,2], [9,15,11,18,22,13,8,3,4],
 [7,5,8,3,17,23,9,15,14], [13,8,5,1,12,19,6,10,21],
 [1,2,11,18,7,14,24,20,12], [3,4,16,22,13,21,20,24,17],
 [14,24,17,23,19,6,2,11,15], [10,21,20,12,19,23,9,4,16]]
# (a,b,c,d) denotes ax+by+cz=d.
PLANES = [(21,3,-10,-1440),(21,3,10,1440),(3,0,1,234),
 (3,0,-1,-234),(0,3,-1,234),(0,3,1,-234),
 (3,-21,10,-1440),(3,-21,-10,1440)]
ORIENTATIONS = [1,1,-1,-1,-1,-1,1,1]

def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def edges(c): return list(zip(c,c[1:]+c[:1]))
def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def on_segment(p,a,b):
 return orient(a,b,p)==0 and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in range(2))
def segments_meet(a,b,c,d):
 o1,o2,o3,o4=orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
 return (o1*o2<0 and o3*o4<0) or any((o==0 and on_segment(p,u,v)) for o,p,u,v in [(o1,c,a,b),(o2,d,a,b),(o3,a,c,d),(o4,b,c,d)])
def project(p,plane):
 drop=max(range(3),key=lambda k:abs(plane[k]))
 return tuple(p[k] for k in range(3) if k!=drop)
def inside_closed(p,poly):
 """Exact even-odd rule, with boundary included and half-open y intervals."""
 if any(on_segment(p,a,b) for a,b in edges(poly)): return True
 count=0
 for a,b in edges(poly):
  if (a[1]>p[1]) != (b[1]>p[1]):
   x=a[0]+Q(p[1]-a[1],b[1]-a[1])*(b[0]-a[0])
   if x>p[0]: count+=1
 return bool(count%2)
def normalize(intervals):
 out=[]
 for a,b in sorted(tuple(sorted(x)) for x in intervals):
  if out and a<=out[-1][1]: out[-1]=(out[-1][0],max(b,out[-1][1]))
  else: out.append((a,b))
 return out
def intersect(a,b):
 return normalize([(max(x,u),min(y,v)) for x,y in a for u,v in b if max(x,u)<=min(y,v)])
def line(p,q):
 """Return k, origin, direction with origin[k]=0, direction[k]=1."""
 d=cross(p[:3],q[:3]); assert any(d), 'parallel planes'
 k=next(k for k in range(3) if d[k])
 i,j=[u for u in range(3) if u!=k]
 det=p[i]*q[j]-p[j]*q[i]; assert det
 o=[Q(0)]*3
 o[i]=Q(p[3]*q[j]-p[j]*q[3],det)
 o[j]=Q(p[i]*q[3]-p[3]*q[i],det)
 v=tuple(Q(t,d[k]) for t in d)
 assert dot(p[:3],o)==p[3] and dot(q[:3],o)==q[3]
 return k,tuple(o),v

def section(poly, own_plane, other_plane, line_data):
 """Closed polygon intersect line: sample every boundary-delimited open interval.

Every membership change is on the polygon boundary. A boundary segment has
linear signed distance to the other plane, so all breakpoints are exact.
Outside the extreme breakpoints the compact polygon has no points.
"""
 k,o,d=line_data
 cuts=set()
 for a,b in edges(poly):
  fa=dot(other_plane[:3],a)-other_plane[3]
  fb=dot(other_plane[:3],b)-other_plane[3]
  if fa==0: cuts.add(Q(a[k]))
  if fb==0: cuts.add(Q(b[k]))
  if fa*fb<0:
   t=Q(fa,fa-fb)
   cuts.add(a[k]+t*(b[k]-a[k]))
 cuts=sorted(cuts)
 projected=[project(a,own_plane) for a in poly]
 def contained(t):
  pt=tuple(o[i]+t*d[i] for i in range(3))
  return inside_closed(project(pt,own_plane),projected)
 intervals=[(t,t) for t in cuts if contained(t)]
 intervals += [(a,b) for a,b in zip(cuts,cuts[1:]) if contained((a+b)/2)]
 return normalize(intervals)

def self_test():
 s=[(Q(0),Q(0)),(Q(2),Q(0)),(Q(2),Q(2)),(Q(0),Q(2))]
 assert inside_closed((1,1),s) and inside_closed((0,1),s) and not inside_closed((3,1),s)
 assert segments_meet((0,0),(2,2),(0,2),(2,0))
 assert segments_meet((0,0),(2,0),(1,0),(3,0))
 assert not segments_meet((0,0),(1,0),(2,0),(3,0))
 p=(0,0,1,0); poly=[(x,y,Q(0)) for x,y in s]
 for q,expected in [((1,0,0,1),[(Q(0),Q(2))]),((1,0,0,0),[(Q(0),Q(2))]),((1,1,0,0),[(Q(0),Q(0))]),((1,0,0,3),[])]:
  assert section(poly,p,q,line(p,q))==expected
 # Concave polygon cut in two disconnected components.
 u=[(0,0,0),(3,0,0),(3,3,0),(2,3,0),(2,1,0),(1,1,0),(1,3,0),(0,3,0)]
 q=(0,1,0,2)
 assert section(u,p,q,line(p,q))==[(Q(0),Q(1)),(Q(2),Q(3))]
 return 11

def verify(vertices=VERTICES,faces=FACES,planes=PLANES):
 verts=[tuple(map(Q,v)) for v in vertices]
 assert len(verts)==len(set(verts))==24
 assert len(faces)==len(planes)==8
 incidence=defaultdict(list); face_edges=[]; reflex=[]; area2=[]
 for fi,face in enumerate(faces):
  assert len(face)==len(set(face))==9
  poly=[verts[v-1] for v in face]; pl=planes[fi]
  assert all(dot(pl[:3],v)==pl[3] for v in poly), ('planarity',fi+1)
  proj=[project(v,pl) for v in poly]
  area=sum(a[0]*b[1]-a[1]*b[0] for a,b in edges(proj)); assert area
  turns=[orient(proj[i-1],proj[i],proj[(i+1)%9]) for i in range(9)]
  assert all(turns), ('collinear consecutive edges',fi+1)
  for i,j in combinations(range(9),2):
   if (i-j)%9 in (1,8): continue
   assert not segments_meet(proj[i],proj[(i+1)%9],proj[j],proj[(j+1)%9]), ('non-simple',fi+1,i,j)
  reflex.append(sum(t*area<0 for t in turns)); assert reflex[-1]>0
  area2.append(str(area))
  es={tuple(sorted(e)) for e in edges(face)}; assert len(es)==9; face_edges.append(es)
  for a,b in edges(face): incidence[tuple(sorted((a,b)))].append((fi,1 if a<b else -1))
 assert len(incidence)==36 and all(len(x)==2 for x in incidence.values())
 assert all(ORIENTATIONS[i]*s == -ORIENTATIONS[j]*t for (i,s),(j,t) in incidence.values())
 # Each vertex link is a connected simple cycle, rather than a pinch point.
 neighbors=defaultdict(set)
 for a,b in incidence: neighbors[a].add(b); neighbors[b].add(a)
 for v in range(1,25):
  incident=[f for f in faces if v in f]; assert len(incident)==3
  link=defaultdict(set)
  for f in incident:
   i=f.index(v); a,b=f[i-1],f[(i+1)%len(f)]
   link[a].add(b); link[b].add(a)
  assert set(link)==neighbors[v] and len(link)==3 and all(len(x)==2 for x in link.values())
 seen={1}; todo=[1]
 while todo:
  for v in neighbors[todo.pop()]-seen: seen.add(v); todo.append(v)
 assert len(seen)==24
 pairs=[]; mult=Counter()
 for i,j in combinations(range(8),2):
  ld=line(planes[i],planes[j]); k=ld[0]
  left=section([verts[v-1] for v in faces[i]],planes[i],planes[j],ld)
  right=section([verts[v-1] for v in faces[j]],planes[j],planes[i],ld)
  actual=intersect(left,right)
  common_edges=sorted(face_edges[i]&face_edges[j]); assert common_edges
  common_vertices=sorted(set(faces[i])&set(faces[j]))
  expected=normalize([(verts[a-1][k],verts[b-1][k]) for a,b in common_edges]+[(verts[v-1][k],verts[v-1][k]) for v in common_vertices])
  assert actual==expected, ('unexpected intersection',i+1,j+1,actual,expected)
  # No extra isolated shared vertex outside the shared edges.
  edge_union=normalize([(verts[a-1][k],verts[b-1][k]) for a,b in common_edges])
  assert actual==edge_union
  assert len(actual)==len(common_edges) # Doubled edges are disconnected.
  mult[len(common_edges)]+=1
  pairs.append({'faces':[i+1,j+1],'shared_edges':common_edges,'parameter_coordinate':'xyz'[k],
   'intersection_intervals':[[str(a),str(b)] for a,b in actual]})
 assert mult=={1:20,2:8}
 chi=24-36+8; assert chi==-4
 # A closed embedded orientable genus-3 surface cannot bound a convex body.
 # Stronger local check: every planar face itself has reflex corners.
 return {'verification':'PASS','arithmetic':'fractions.Fraction; no tolerance',
  'source':'https://arxiv.org/html/2609.17700v1',
  'vertices':24,'edges':36,'faces':8,'euler_characteristic':chi,'genus':3,
  'vertex_links':'24 connected triangles','orientable':True,'connected':True,
  'all_faces_simple_planar_disks':True,'reflex_corners_by_face':reflex,
  'pairwise_face_intersections_checked':28,'unexpected_intersections':0,
  'edge_adjacency_multiplicities':dict(mult),'face_pair_intersections':pairs}

if __name__=='__main__':
 if not __debug__: raise RuntimeError('Run without -O; assertions are certificate checks')
 result=verify(); result['primitive_self_tests']=self_test()
 # A corrupted input is required to fail; a smoke test for active assertions.
 corrupted=list(VERTICES); corrupted[0]=(VERTICES[0][0]+1,*VERTICES[0][1:])
 try: verify(corrupted)
 except AssertionError: result['coordinate_mutation_rejected']=True
 else: raise AssertionError('corruption was not detected')
 print(json.dumps(result,indent=2))
