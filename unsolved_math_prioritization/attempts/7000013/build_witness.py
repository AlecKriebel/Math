#!/usr/bin/env python3
"""Locally authored exact rational compact-shear witness; no external executable."""
from fractions import Fraction as Q
from itertools import product
from collections import Counter,defaultdict,deque
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
checks=Counter()
def ck(cat,x):
 assert x,cat
 checks[cat]+=1
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,t):return tuple(x*t for x in a)
def cross2(a,b):return a[0]*b[1]-a[1]*b[0]
def area2(p):return sum(cross2(p[i],p[(i+1)%len(p)]) for i in range(len(p)))
def clean(p):
 q=[]
 for x in p:
  if not q or q[-1]!=x:q.append(x)
 if len(q)>1 and q[0]==q[-1]:q.pop()
 return q
# Keep L(x,y)>=0; all operations rational.
def clip(poly,L):
 out=[]
 def val(p):return L[0]*p[0]+L[1]*p[1]+L[2]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  a,b=val(p),val(q)
  if a>=0:out.append(p)
  if (a<0<b) or (b<0<a):out.append(add(p,scale(sub(q,p),a/(a-b))))
 return clean(out)
def rowval(r,p):return r[0]*p[0]+r[1]*p[1]+r[2]
H=[(None,-2,0,0),(-2,-1,1,2),(-1,1,0,1),(1,2,-1,2),(2,None,0,0)]
V=[(None,-5,0,0),(-5,-4,4,20),(-4,4,0,4),(4,5,-4,20),(5,None,0,0)]
xs=[Q(-10),Q(-1,2),Q(1,2),Q(10)];ys=[Q(-8),Q(-1,2),Q(1,2),Q(8)]
cells=[]
for i,j in product(range(3),repeat=2):
 poly=[(xs[i],ys[j]),(xs[i+1],ys[j]),(xs[i+1],ys[j+1]),(xs[i],ys[j+1])]
 cells.append((poly,[(Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0))],i==j==1))
# F=H o V o H^-1 o V^-1, read right to left.
for axis,bands,sgn in [(1,V,-1),(0,H,-1),(1,V,1),(0,H,1)]:
 new=[];arg=1-axis
 for poly,A,inside in cells:
  for lo,hi,m,b in bands:
   p=poly
   if lo is not None:p=clip(p,add(A[arg],(Q(0),Q(0),-Q(lo))))
   if p and hi is not None:p=clip(p,add(scale(A[arg],-1),(Q(0),Q(0),Q(hi))))
   if len(p)<3 or area2(p)==0:continue
   ck('positive_cell_orientation',area2(p)>0)
   B=A.copy();B[axis]=add(B[axis],add(scale(A[arg],Q(sgn*m)),(Q(0),Q(0),Q(sgn*b))))
   ck('unit_determinant_pieces',B[0][0]*B[1][1]-B[0][1]*B[1][0]==1)
   new.append((p,B,inside))
 cells=new
# Exact direct evaluation of the compact shear map.
def hh(y):return max(Q(0),min(Q(1),Q(2)-abs(y)))
def vv(x):return 4*max(Q(0),min(Q(1),Q(5)-abs(x)))
def F(p):
 x,y=p;y-=vv(x);x-=hh(y);y+=vv(x);x+=hh(y);return x,y
allpts=set(p for poly,_,_ in cells for p in poly)
def onsegment(p,a,b):return cross2(sub(p,a),sub(b,a))==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])
def refine(poly):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  pts=[p for p in allpts if onsegment(p,a,b)]
  k=0 if a[0]!=b[0] else 1
  pts.sort(key=lambda p:(p[k]-a[k])/(b[k]-a[k]))
  out.extend(pts[:-1])
 return out
cells=[(refine(p),A,inside) for p,A,inside in cells]
verts=[];images=[];lookup={};faces=[]
def vertex(p):
 if p not in lookup:
  lookup[p]=len(verts);verts.append(p)
  images.append(p if p[2]==0 else (*F(p[:2]),p[2]))
 return lookup[p]
def triangle(a,b,c):faces.append([vertex(a),vertex(b),vertex(c)])
# Top annulus: each cell lies within one affine piece and outside the bump footprint.
for poly,A,inside in cells:
 for p in poly:
  ck('affine_map_matches_shears',tuple(rowval(row,p) for row in A)==F(p))
  if inside:ck('bump_translation',F(p)==(p[0]+1,p[1]))
 if inside:continue
 center=tuple(sum(p[k] for p in poly)/len(poly) for k in range(2))
 ck('cell_area_preserved',area2([F(p) for p in poly])==area2(poly))
 for a,b in zip(poly,poly[1:]+poly[:1]):triangle((*center,Q(1)),(*a,Q(1)),(*b,Q(1)))
# Boundary loops have every induced mesh vertex, avoiding hanging edges.
def rectloop(x0,x1,y0,y1):
 corners=[(Q(x0),Q(y0)),(Q(x1),Q(y0)),(Q(x1),Q(y1)),(Q(x0),Q(y1))]
 return refine(corners)
outer=rectloop(-10,10,-8,8);inner=rectloop(Q(-1,2),Q(1,2),Q(-1,2),Q(1,2))
for p in outer:ck('outer_boundary_fixed',F(p)==p)
for loop,zlo,zhi in [(outer,Q(0),Q(1)),(inner,Q(1),Q(3))]:
 for a,b in zip(loop,loop[1:]+loop[:1]):
  triangle((*a,zlo),(*b,zlo),(*b,zhi));triangle((*a,zlo),(*b,zhi),(*a,zhi))
for a,b in zip(outer,outer[1:]+outer[:1]):triangle((Q(0),Q(0),Q(0)),(*b,Q(0)),(*a,Q(0)))
for a,b in zip(inner,inner[1:]+inner[:1]):triangle((Q(0),Q(0),Q(3)),(*a,Q(3)),(*b,Q(3)))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
edges=defaultdict(list)
for fi,tri in enumerate(faces):
 a,b,c=[verts[i] for i in tri];aa,bb,cc=[images[i] for i in tri]
 cv=cross(sub(b,a),sub(c,a));cv2=cross(sub(bb,aa),sub(cc,aa))
 ck('nondegenerate_triangular_face',cv!=(0,0,0))
 ck('identical_oriented_face_area_vector',cv==cv2)
 for i,j in zip(tri,tri[1:]+tri[:1]):edges[tuple(sorted((i,j)))].append((i,j,fi))
for uses in edges.values():ck('closed_oriented_edge',len(uses)==2 and uses[0][:2]==uses[1][:2][::-1])
ck('Euler_sphere',len(verts)-len(edges)+len(faces)==2)
adj=defaultdict(set)
for a,b in edges:adj[a].add(b);adj[b].add(a)
seen={0};q=deque([0])
while q:
 for j in adj[q.popleft()]:
  if j not in seen:seen.add(j);q.append(j)
ck('connected_surface',len(seen)==len(verts))
# Every vertex link is one cycle, so this is a closed triangulated 2-manifold.
for v in range(len(verts)):
 link=defaultdict(set)
 for tri in faces:
  if v in tri:
   a,b=[i for i in tri if i!=v];link[a].add(b);link[b].add(a)
 ck('link_degree_two',all(len(x)==2 for x in link.values()))
 st=next(iter(link));ss={st};q=deque([st])
 while q:
  for j in link[q.popleft()]:
   if j not in ss:ss.add(j);q.append(j)
 ck('link_connected',len(ss)==len(link))
def mass(points):
 vol=Q(0);mom=[Q(0)]*3
 for tri in faces:
  a,b,c=[points[i] for i in tri];d=dot(a,cross(b,c));vol+=d/6
  for k in range(3):mom[k]+=d*(a[k]+b[k]+c[k])/24
 return vol,tuple(x/vol for x in mom)
v0,c0=mass(verts);v1,c1=mass(images)
ck('exact_volumes',v0==v1==322)
ck('centroid_original',c0==(0,0,Q(82,161)))
ck('centroid_shifted',c1==(Q(1,161),0,Q(82,161)))
ck('noncongruence_invariant',dot(c0,c0)==Q(6724,25921) and dot(c1,c1)==Q(6725,25921))
# Top annulus consists of full refined cells, total area319; unique bottom area320.
ck('annulus_area',sum(area2(p)/2 for p,A,inside in cells if not inside)==319)
ck('bump_footprint_area',sum(area2(p)/2 for p,A,inside in cells if inside)==1)
ck('full_domain_area',sum(area2(p)/2 for p,A,inside in cells)==320)
witness={'vertices':[[str(x) for x in p] for p in verts],'image_vertices':[[str(x) for x in p] for p in images],'oriented_triangles':faces,'map':'H o V o H^-1 o V^-1','base_box':[['-10','10'],['-8','8'],['0','1']],'original_bump':[['-1/2','1/2'],['-1/2','1/2'],['1','3']],'image_bump':[['1/2','3/2'],['-1/2','1/2'],['1','3']]}
(root/'witness.json').write_text(json.dumps(witness,indent=2)+'\n')
out={'status':'PASS_EXACT','assertions':sum(checks.values()),'categories':dict(checks),'affine_cells':len(cells),'vertices':len(verts),'edges':len(edges),'triangles':len(faces),'Euler_characteristic':2,'volume':str(v0),'original_centroid':list(map(str,c0)),'image_centroid':list(map(str,c1)),'squared_distances_to_unique_bottom_center':['6724/25921','6725/25921'],'witness_sha256':hashlib.sha256((root/'witness.json').read_bytes()).hexdigest(),'all_arithmetic':'exact rational; no numerical geometric tolerance'}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
