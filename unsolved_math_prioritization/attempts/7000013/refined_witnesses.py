#!/usr/bin/env python3
"""Exact rational controls for the three refined polyhedral categories."""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
import json
C=Counter();root=Path(__file__).resolve().parent

def ck(k,b):assert b,k;C[k]+=1
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def vecarea(ps):return tuple(sum(cross(ps[i],ps[(i+1)%len(ps)])[j] for i in range(len(ps)))/2 for j in range(3))
def normal(ps):return cross(sub(ps[1],ps[0]),sub(ps[2],ps[1]))
def oriented(ps,n):
 return ps if dot(vecarea(ps),n)>0 else list(reversed(ps))
def pack(faces):
 points=[];ids={};fs=[]
 for face in faces:
  row=[]
  for p in face:
   p=tuple(map(F,p))
   if p not in ids:ids[p]=len(points);points.append(p)
   row.append(ids[p])
  fs.append(row)
 return points,fs

def analyze(points,faces,prefix):
 ed=defaultdict(list);areas=[];convex=[]
 for k,f in enumerate(faces):
  ps=[points[i] for i in f];n=vecarea(ps);areas.append(n)
  ck(prefix+'_positive_area',dot(n,n)>0)
  for p in ps:ck(prefix+'_planarity',dot(n,sub(p,ps[0]))==0)
  signs=[dot(n,cross(sub(ps[(j+1)%len(ps)],ps[j]),sub(ps[(j+2)%len(ps)],ps[(j+1)%len(ps)]))) for j in range(len(ps))]
  convex.append(all(s>0 for s in signs))
  for a,b in zip(f,f[1:]+f[:1]):ed[tuple(sorted((a,b)))].append((a,b,k))
 for uses in ed.values():
  ck(prefix+'_oriented_manifold_edge',len(uses)==2 and uses[0][:2]==uses[1][:2][::-1])
  ck(prefix+'_nonflat_adjacent_faces',cross(areas[uses[0][2]],areas[uses[1][2]])!=(0,0,0))
 return areas,convex,ed

def mass(points,faces):
 V=F(0);M=[F(0)]*3
 for f in faces:
  for k in range(1,len(f)-1):
   a,b,c=[points[i] for i in [f[0],f[k],f[k+1]]];d=dot(a,cross(b,c));V+=d/6
   for j in range(3):M[j]+=d*(a[j]+b[j]+c[j])/24
 return V,tuple(x/V for x in M) if V else None

def roof(height):
 b=[(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0)];t=[(x,y,1) for x,y,z in b];ap=(0,0,1+height)
 faces=[list(reversed(b))]
 for i in range(4):j=(i+1)%4;faces.append([b[i],b[j],t[j],t[i]])
 for i in range(4):j=(i+1)%4;faces.append([t[i],t[j],ap])
 return pack(faces)
A,fa=roof(F(1,2));B,fb=roof(F(-1,2));aa,ca,ea=analyze(A,fa,'roof');ab,cb,eb=analyze(B,fb,'dent')
perm=list(range(5))+[7,8,5,6]
for i,j in enumerate(perm):ck('roof_dent_cooriented_area_match',aa[i]==ab[j])
ck('roof_dent_convex_maximal_faces',all(ca+cb))
va,_=mass(A,fa);vb,_=mass(B,fb);ck('roof_dent_noncongruent_volumes',va==F(14,3) and vb==F(10,3))
def adjacent(faces,i,j):return len(set(faces[i])&set(faces[j]))>=2
ck('normal_match_not_incidence_preserving',any(adjacent(fa,i,j)!=adjacent(fb,perm[i],perm[j]) for i,j in combinations(range(9),2)))

# Edge-attached cap: maximum planar faces, two simple nonconvex faces.
def cap(t):
 l=t-F(1,2);r=t+F(1,2)
 faces=[]
 def face(ps,n):faces.append(oriented(ps,n))
 face([(-4,-3,0),(4,-3,0),(4,3,0),(-4,3,0)],(0,0,-1))
 face([(-4,-3,0),(4,-3,0),(4,-3,1),(-4,-3,1)],(0,-1,0))
 face([(-4,-3,0),(-4,3,0),(-4,3,1),(-4,-3,1)],(-1,0,0))
 face([(4,-3,0),(4,3,0),(4,3,1),(4,-3,1)],(1,0,0))
 face([(-4,3,0),(4,3,0),(4,3,1),(r,3,1),(r,3,3),(l,3,3),(l,3,1),(-4,3,1)],(0,1,0))
 face([(-4,-3,1),(4,-3,1),(4,3,1),(r,3,1),(r,2,1),(l,2,1),(l,3,1),(-4,3,1)],(0,0,1))
 face([(l,2,1),(r,2,1),(r,2,3),(l,2,3)],(0,-1,0))
 face([(l,2,1),(l,3,1),(l,3,3),(l,2,3)],(-1,0,0))
 face([(r,2,1),(r,3,1),(r,3,3),(r,2,3)],(1,0,0))
 face([(l,2,3),(r,2,3),(r,3,3),(l,3,3)],(0,0,1))
 return pack(faces)
D,fd=cap(F(0));E,fe=cap(F(1));ad,cd,ed=analyze(D,fd,'cap0');ae,ce,ee=analyze(E,fe,'cap1')
for i in range(10):ck('cap_cooriented_area_match',ad[i]==ae[i])
ck('cap_incidence_same',fd==fe)
ck('cap_two_nonconvex_faces',sum(not x for x in cd)==sum(not x for x in ce)==2)
vd,gd=mass(D,fd);ve,ge=mass(E,fe)
ck('cap_equal_volumes',vd==ve==50)
ck('cap_centroid0',gd==(0,F(1,10),F(14,25)))
ck('cap_centroid1',ge==(F(1,25),F(1,10),F(14,25)))
ck('cap_noncongruence_invariant',dot(gd,gd)==F(809,2500) and dot(ge,ge)==F(813,2500))
ck('cap_unique_largest_bottom',[sum(abs(q) for q in n) for n in ad]==[48,8,6,6,10,47,2,2,2,1])

# Four-ring immersed quadrilateral tori, all maximal faces convex and nonflat.
prof=[(F(1),F(-2)),(F(3),F(1)),(F(1),F(2)),(F(3),F(-1))];dirs=[(1,0),(0,1),(-1,0),(0,-1)]
def torus(sign):
 tau=F(sign,2);points=[]
 for r,z in prof:
  for x,y in dirs:points.append(((r+tau/r)*x,(r+tau/r)*y,z*(1-tau/3)))
 faces=[]
 for i in range(4):
  for j in range(4):faces.append([4*i+j,4*((i+1)%4)+j,4*((i+1)%4)+(j+1)%4,4*i+(j+1)%4])
 return points,faces
T,ft=torus(1);U,fu=torus(-1);at,ct,et=analyze(T,ft,'torus_plus');au,cu,eu=analyze(U,fu,'torus_minus')
O,fo=torus(0)
for i in range(16):
 ck('torus_cooriented_area_match',at[i]==au[i])
 ck('torus_exact_area_scaling',at[i]==tuple(F(35,36)*x for x in vecarea([O[j] for j in fo[i]])))
ck('torus_strictly_convex_faces',all(ct+cu));ck('torus_incidence_same',ft==fu)
ck('torus_Euler_zero',len(T)-len(et)+len(ft)==len(U)-len(eu)+len(fu)==0)
dt=max(dot(sub(p,q),sub(p,q)) for p,q in combinations(T,2));du=max(dot(sub(p,q),sub(p,q)) for p,q in combinations(U,2))
ck('torus_distinct_exact_diameters',dt==F(386,9) and du==F(338,9))
ck('dual_closure',sum((prof[(i+1)%4][1]-prof[i][1])/(prof[i][0]*prof[(i+1)%4][0]) for i in range(4))==0)
# Exact transverse profile self-intersection at radius7/3,z0 before the affine radial changes.
for sign in [1,-1]:
 tau=F(sign,2);k=1-tau/3;d=4*tau/3;pt=(k*F(7,3)+d,F(0))
 p0=(k*prof[0][0]+d,k*prof[0][1]);p1=(k*prof[1][0]+d,k*prof[1][1]);p2=(k*prof[2][0]+d,k*prof[2][1]);p3=(k*prof[3][0]+d,k*prof[3][1])
 ck('torus_self_intersection_explicit',all(pt[j]==p0[j]+F(2,3)*(p1[j]-p0[j])==p2[j]+F(2,3)*(p3[j]-p2[j]) for j in range(2)))

def record(points,faces):return {'vertices':[[str(x) for x in p] for p in points],'faces':faces}
witness={'roof_out':record(A,fa),'roof_in':record(B,fb),'roof_face_matching':perm,'cap_centered':record(D,fd),'cap_shifted':record(E,fe),'torus_plus':record(T,ft),'torus_minus':record(U,fu)}
(root/'refined_witnesses.json').write_text(json.dumps(witness,indent=2)+'\n')
out={'status':'PASS_EXACT','assertions':sum(C.values()),'categories':dict(C),'roof_dent':{'faces':9,'volume_values':[str(va),str(vb)],'incidence_preserved_by_normal_matching':False},'sliding_cap':{'faces':10,'convex_faces':8,'nonconvex_faces':2,'incidence_preserved':True,'embedded':True,'volume':str(vd)},'immersed_torus':{'vertices':16,'faces':16,'all_faces_strictly_convex':True,'adjacent_faces_nonflat':True,'incidence_preserved':True,'embedded':False,'diameter_squared':[str(dt),str(du)]},'all_arithmetic':'exact rational'}
(root/'refined_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
