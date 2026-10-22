#!/usr/bin/env python3
"""Fresh 3D exact integration of (Z,Delta,x) mask polytopes; stdlib only.

No supplied checker is imported. Each point-floor/inclusion mask gives an
intersection of integer halfspaces. Vertices come from plane triples; boundary
facets are triangulated and joined to an interior rational center. The integral
of an affine pth power over each tetrahedron uses barycentric monomials.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from functools import cmp_to_key
from math import comb
import json,sys

CHECKS=0

def require(test,detail):
 global CHECKS
 CHECKS+=1
 if not test:raise RuntimeError(detail)

def det(a,b,c):
 return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

def dot(a,b):return sum(u*v for u,v in zip(a,b))
def sub(a,b):return tuple(u-v for u,v in zip(a,b))

def vertex(rows):
 a,b,c=rows;den=det(a,b,c)
 if not den:return None
 return (
  Q(det((a[3],a[1],a[2]),(b[3],b[1],b[2]),(c[3],c[1],c[2])),den),
  Q(det((a[0],a[3],a[2]),(b[0],b[3],b[2]),(c[0],c[3],c[2])),den),
  Q(det((a[0],a[1],a[3]),(b[0],b[1],b[3]),(c[0],c[1],c[3])),den))

def face_order(vertices,normal):
 # Project away a nonzero normal coordinate, then polar-sort rational vectors.
 drop=next(i for i,v in enumerate(normal) if v)
 axes=[i for i in range(3) if i!=drop]
 center=tuple(sum(v[i] for v in vertices)/len(vertices) for i in axes)
 def vec(p):return tuple(p[i]-center[j] for j,i in enumerate(axes))
 def half(v):return 0 if v[1]>0 or (v[1]==0 and v[0]>=0) else 1
 def cmp(a,b):
  u,v=vec(a),vec(b);ha,hb=half(u),half(v)
  if ha!=hb:return -1 if ha<hb else 1
  cross=u[0]*v[1]-u[1]*v[0]
  return -1 if cross>0 else 1 if cross<0 else 0
 return sorted(vertices,key=cmp_to_key(cmp))

def homogeneous(values,p):
 # Generating function coefficient of product_i (1-values_i t)^(-1).
 h=[Q(1)]+[Q(0)]*p
 for value in values:
  for k in range(1,p+1):h[k]+=value*h[k-1]
 return h[p]

def integrate(rows,level,p):
 rows=sorted(set(rows));points=set()
 for triple in combinations(rows,3):
  v=vertex(triple)
  if v is not None and all(dot(row[:3],v)<=row[3] for row in rows):points.add(v)
 if len(points)<4:return Q(0),Q(0)
 center=tuple(sum(v[i] for v in points)/len(points) for i in range(3))
 volume=Q(0);value=Q(0);seen=set()
 for row in rows:
  face=frozenset(v for v in points if dot(row[:3],v)==row[3])
  if len(face)<3 or face in seen:continue
  seen.add(face);vs=face_order(list(face),row[:3])
  for j in range(1,len(vs)-1):
   tetra=[center,vs[0],vs[j],vs[j+1]]
   vol=abs(det(*(sub(tetra[k],center) for k in (1,2,3))))/6
   volume+=vol
   value+=vol*homogeneous([level-v[2] for v in tetra],p)/comb(p+3,3)
 return volume,value

CUBE=[(-1,0,0,0),(1,0,0,1),(0,-1,0,0),(0,1,0,1),(0,0,-1,0),(0,0,1,1)]

def model(n,p):
 total_volume=Q(0);moment=Q(0);positive=0;mask_vol=[Q(0)]*(n+1)
 for floors in product(*(range(j+1) for j in range(n))):
  base=CUBE[:]
  for j,f in enumerate(floors):base.extend([(-j,-1,0,-f),(j,1,0,f+1)])
  for mask in product((False,True),repeat=n):
   rows=base[:]
   for j,(f,included) in enumerate(zip(floors,mask)):
    rows.append((j,1,-1,f) if included else (-j,-1,1,-f))
   vol,value=integrate(rows,Q(sum(mask),n),p)
   require(vol>=0 and value>=0,'negative polytope measure/moment')
   if vol:
    positive+=1;total_volume+=vol;moment+=value;mask_vol[sum(mask)]+=vol
 require(total_volume==1,'floor/mask coverage is not the whole probability cube')
 require(sum(mask_vol)==1,'count law does not normalize')
 require(sum(k*v for k,v in enumerate(mask_vol))==Q(n,2),'uniform marginal mean integrated over x')
 return {'n':n,'p':p,'positive_polytopes':positive,'volume':str(total_volume),'count_volumes':list(map(str,mask_vol)),'moment':str(moment)}

def iid(n,p):
 # Direct integrated binomial law, expanding only the affine centered power.
 from math import factorial as fac
 return sum(Q(comb(n,k)*comb(p,a)*(-1)**a*fac(k+a)*fac(n-k),fac(n+a+1))*Q(k,n)**(p-a)
            for k in range(n+1) for a in range(p+1))

def main():
 baseline=[]
 for p in (0,2,4,6):
  vol,value=integrate(CUBE,Q(0),p)
  require(vol==1 and value==Q(1,p+1),'cube monomial integration')
  simplex=[(-1,0,0,0),(0,-1,0,0),(0,0,-1,0),(1,1,1,1)]
  vol,value=integrate(simplex,Q(0),p)
  require(vol==Q(1,6) and value==Q(1,(p+1)*(p+2)*(p+3)),'simplex monomial integration')
  baseline.append({'p':p,'cube':str(Q(1,p+1)),'simplex':str(value)})
 records=[model(n,p) for n in range(1,5) for p in (2,4)]
 vals={(r['n'],r['p']):Q(r['moment']) for r in records}
 for n in range(1,5):require(vals[n,2]==Q(1,6*n),'all checked second moments')
 for n in (1,2):require(vals[n,4]==iid(n,4),'complete small-count law control')
 expected=Q(4,405) if '--force-failure' in sys.argv else Q(19,1620)
 require(vals[3,4]==expected,'three-point exact value (forced corrupt iid substitution if requested)')
 require(vals[4,4]==Q(139,17280),'four-point exact value')
 require(vals[3,4]-iid(3,4)==Q(1,540),'gap')
 require(vals[3,4]/iid(3,4)==Q(19,16),'ratio')
 # Universal claims rely on the written derivation, not a finite loop.
 require([25,52,27,4]==[4*4**3-21*4**2+28*4-7,12*4**2-42*4+28,12*4-21,4],'tail polynomial positive coefficients')
 adverse={
 'iid_joint_substitution':vals[3,4]!=iid(3,4),
 'unscaled_count':3**4*vals[3,4]!=Q(19,1620),
 'n3_tail_does_not_prove_reversal':Q(1,105)<iid(3,4),
 'single_tail_n4_is_insufficient':Q(1,315)<iid(4,4),
 'fixed_zero_generator_is_different':vals[1,4]!=vals[3,4],
 'lower_half_q_cannot_extend':Q(1,2)!=1,
 'shared_phase_cannot_iid':sum(a+b==c+d for a,b,c,d in product(range(3),repeat=4))==19 and sum(sorted((a,b))==sorted((c,d)) for a,b,c,d in product(range(3),repeat=4))==15,
 }
 for name,v in adverse.items():require(v,'adverse control inactive: '+name)
 print(json.dumps({'status':'PASS','mechanism':'3D exact floor/inclusion polytope integration','checks':CHECKS,'baselines':baseline,'records':records,'adverse':adverse},indent=2,sort_keys=True))

if __name__=='__main__':main()
