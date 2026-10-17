#!/usr/bin/env python3
"""Exact rational PL braid-representative intersection experiment."""
from fractions import Fraction as F
from itertools import permutations
import json

def add(a,b):return(a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def mul(a,t):return(a[0]*t,a[1]*t)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def orient(a,b,c):return cross(sub(b,a),sub(c,a))
def interp(a,b,t):return add(a,mul(sub(b,a),t))

def directions():
 q=[]
 for k in range(8):
  t=F(k,8);q.append(((1-t*t)/(1+t*t),2*t/(1+t*t)))
 out=[]
 for turns in range(4):
  for p in q:
   for _ in range(turns):p=(-p[1],p[0])
   out.append(p)
 return out

def half_twist(center):
 ds=directions();rads=[F(11,20)+F(17,320)*i for i in range(17)]
 rings=[[add(center,mul(v,r)) for v in ds] for r in rads]
 images=[[add(center,mul(ds[(j+16-i)%32],r)) for j in range(32)] for i,r in enumerate(rads)]
 triangles=[]
 for j in range(32):triangles.append(((center,rings[0][j],rings[0][(j+1)%32]),(center,images[0][j],images[0][(j+1)%32])))
 for i in range(16):
  for j in range(32):
   k=(j+1)%32
   triangles.append(((rings[i][j],rings[i+1][j],rings[i+1][k]),(images[i][j],images[i+1][j],images[i+1][k])))
   triangles.append(((rings[i][j],rings[i+1][k],rings[i][k]),(images[i][j],images[i+1][k],images[i][k])))
 for a,b in triangles:
  if orient(*a)<=0 or orient(*b)<=0:raise ArithmeticError('Triangle orientation failure')
 edges=set()
 for tri,_ in triangles:
  for i in range(3):edges.add(tuple(sorted([tri[i],tri[(i+1)%3]])))
 return triangles,edges

def intersections(a,b,c,d):
 """Closed segment intersection parameters on ab; split collinear overlaps."""
 v,w=sub(b,a),sub(d,c);den=cross(v,w)
 if den:
  t=cross(sub(c,a),w)/den;s=cross(sub(c,a),v)/den
  return [t] if 0<=t<=1 and 0<=s<=1 else []
 if cross(sub(c,a),v):return []
 axis=0 if v[0] else 1
 if not v[axis]:return []
 return [t for t in [(c[axis]-a[axis])/v[axis],(d[axis]-a[axis])/v[axis]] if 0<=t<=1]

def image_at(p,triangles):
 for tri,img in triangles:
  a,b,c=tri;den=orient(a,b,c)
  vb=cross(sub(p,a),sub(c,a))/den;vc=cross(sub(b,a),sub(p,a))/den
  if vb>=0 and vc>=0 and vb+vc<=1:
   return add(img[0],add(mul(sub(img[1],img[0]),vb),mul(sub(img[2],img[0]),vc)))
 return p

def transform(poly,triangles,edges):
 out=[]
 for a,b in zip(poly,poly[1:]):
  ts={F(0),F(1)}
  for c,d in edges:ts.update(intersections(a,b,c,d))
  for t in sorted(ts):
   p=image_at(interp(a,b,t),triangles)
   if not out or p!=out[-1]:out.append(p)
 # Remove redundant collinear points.
 compact=[]
 for p in out:
  while len(compact)>=2 and orient(compact[-2],compact[-1],p)==0:compact.pop()
  compact.append(p)
 return compact

def arc(r):return [(F(-r),F(0)),(F(-r),F(-r)),(F(r),F(-r)),(F(r),F(0))]
def circle(r):
 e=F(1,40);r=F(r)
 return [(-r-e,-e),(-r+e,-e),(-r+e,r-e),(r-e,r-e),(r-e,-e),(r+e,-e),(r+e,r+e),(-r-e,r+e),(-r-e,-e)]

def count(poly,loop):
 pts=set();bad=[]
 for a,b in zip(poly,poly[1:]):
  for c,d in zip(loop,loop[1:]):
   ts=intersections(a,b,c,d)
   if not ts:continue
   if cross(sub(b,a),sub(d,c))==0:bad.append('collinear')
   for t in ts:
    p=interp(a,b,t);pts.add(p)
    if p in [a,b,c,d]:bad.append('vertex')
 if bad:raise ArithmeticError(('Not transverse in segment interiors',bad))
 return len(pts),pts

def experiment(n,word):
 aa=[arc(n-i+1) for i in range(1,n+1)]
 for sigma in word:
  center=(F(-(n+1-sigma))-F(1,2),F(0))
  triangles,edges=half_twist(center)
  aa=[transform(p,triangles,edges) for p in aa]
  print('Applied',n,sigma,'segments',[len(p)-1 for p in aa],flush=True)
 mm=[[count(p,circle(n-j+1))[0] for j in range(1,n+1)] for p in aa]
 gen=sum(__import__('math').prod(mm[i][p[i]] for i in range(n)) for p in permutations(range(n)))
 return {'n':n,'braid_word':word,'intersection_matrix':mm,'generator_count':gen,'PL_homeomorphism_verified':'Every source and target triangle has strictly positive rational signed area; boundary map is identity.'}

def on_segment(p,a,b):
 return orient(a,b,p)==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])
def insert_points(poly,points):
 out=[]
 for a,b in zip(poly,poly[1:]):
  axis=0 if b[0]!=a[0] else 1
  pp=[(F(0),a),(F(1),b)]
  for p in points:
   if on_segment(p,a,b):pp.append(((p[axis]-a[axis])/(b[axis]-a[axis]),p))
  for t,p in sorted(set(pp)):
   if not out or out[-1]!=p:out.append(p)
 return out

def path(poly,p,q,cyclic=False):
 pp=insert_points(poly,[p,q]);ip=pp.index(p);iq=pp.index(q)
 if ip<=iq:return pp[ip:iq+1]
 if cyclic:return pp[ip:-1]+pp[:iq+1]
 return list(reversed(pp[iq:ip+1]))
def ray_number(poly,z):
 out=0
 for a,b in zip(poly,poly[1:]):
  if a[1]<=0<b[1] or b[1]<=0<a[1]:
   xx=a[0]-a[1]*(b[0]-a[0])/(b[1]-a[1])
   if xx>z:out+=1 if b[1]>a[1] else -1
 return out

def winding_ray(poly,p):
 for a,b in zip(poly,poly[1:]):
  if on_segment(p,a,b):raise ArithmeticError('Path through puncture')
 return ray_number([sub(a,p) for a in poly],F(0))
def at_time(poly,t):
 N=len(poly)-1
 if t==1:return poly[-1]
 i=int(t*N);u=t*N-i
 return interp(poly[i],poly[i+1],u)
def delta_path(polys):
 times=sorted({F(i,len(p)-1) for p in polys for i in range(len(p))})
 return [sub(at_time(polys[0],t),at_time(polys[1],t)) for t in times]
def negative_axis_count(poly):
 count=0
 for a,b in zip(poly,poly[1:]):
  if a[1]<=0<b[1] or b[1]<=0<a[1]:
   xx=a[0]-a[1]*(b[0]-a[0])/(b[1]-a[1])
   if xx<0:count+=1 if b[1]<a[1] else -1
  if on_segment((F(0),F(0)),a,b):raise ArithmeticError('Particle collision')
 return count

def quantum_grade_experiment(n,word):
 from itertools import product
 aa=[arc(n-i+1) for i in range(1,n+1)]
 for sigma in word:
  mesh=half_twist((F(-(n+1-sigma))-F(1,2),F(0)))
  aa=[transform(p,*mesh) for p in aa]
 bb=[circle(n-j+1) for j in range(1,n+1)]
 pp=[[sorted(count(a,b)[1]) for b in bb] for a in aa]
 rows=[];e=F(1,40)
 for perm in permutations(range(n)):
  for pts in product(*(pp[perm[j]][j] for j in range(n))):
   S=[];winding=0;taus=[];nus=[]
   for j,p in enumerate(pts):
    i=perm[j];rj=F(n-j);ri=F(n-i);dj=(F(0),-rj);di=(F(0),-ri)
    canonical=(i==j and p==(rj,-e))
    if canonical:
     S.append(j+1);tau=[dj,(rj,-rj),(rj+2*e,-rj),(rj+2*e,-e),p]
    else:
     eta=[dj,(-rj,-rj),(-rj,-e)]
     tau=eta+path(bb[j],(-rj,-e),p,True)[1:]
    nu=path(aa[i],p,di)
    gamma=tau+nu[1:];taus.append(tau);nus.append(nu)
    winding+=sum(ray_number(gamma,F(-k))-ray_number(gamma,F(k)) for k in range(1,n+2))
   qwind=sum(winding_ray(tau+nu[1:],(F(k)+e/2,-2*e)) for tau,nu in zip(taus,nus) for k in range(1,n+2))
   if n==1:exchange=0
   elif n==2:
    dif=delta_path(taus)+delta_path(nus)[1:]
    exchange=(1 if perm==(1,0) else 0)+2*negative_axis_count(dif)
   else:raise ValueError('only n<=2')
   local_sign=1
   for j,p in enumerate(pts):
    i=perm[j]
    a,b=next((a,b) for a,b in zip(aa[i],aa[i][1:]) if on_segment(p,a,b))
    c,d=next((c,d) for c,d in zip(bb[j],bb[j][1:]) if on_segment(p,c,d))
    local_sign*=1 if cross(sub(b,a),sub(d,c))>0 else -1
   perm_sign=-1 if perm==(1,0) else 1
   coeff=(-1)**n*perm_sign*local_sign
   rows.append({'permutation':[p+1 for p in perm],'S':S,'A':winding+(len(word)+n)//2,'Q':exchange+qwind+len(word),'q_winding':qwind,'exchange_exponent':exchange,'Euler_coefficient':coeff})
 return rows


def inverse_generator_count():
 tris,_=half_twist((F(-3,2),F(0)))
 inv=[(b,a) for a,b in tris];edges=set()
 for tri,_ in inv:
  for i in range(3):edges.add(tuple(sorted([tri[i],tri[(i+1)%3]])))
 return count(transform(arc(1),inv,edges),circle(1))[0]
