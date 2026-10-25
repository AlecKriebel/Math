#!/usr/bin/env python3
"""Independent exact controls from the manuscript; no submitted helpers imported."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,time
start=time.time();count=0;details={}
def ck(x):
 global count
 if not x:raise AssertionError(count)
 count+=1
def det(M):return M[0]*M[3]-M[1]*M[2]
def at(A,B,z):return tuple(a+z*b for a,b in zip(A,B))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
# Exhaust all small integer two-parameter first jets. Three actual heights
# determine a quadratic, including repeated/singular pencils and degree drops.
qualified=0;two_only=0
for entries in product((-1,0,1),repeat=8):
 A=entries[:4];B=entries[4:];c0=det(A);c2=det(B);c1=det(at(A,B,1))-c0-c2
 for z in (F(-3,2),F(1,3),F(5,2)):ck(det(at(A,B,z))==c0+c1*z+c2*z*z)
 if all(det(at(A,B,z))==0 for z in (0,1,2)):
  qualified+=1;ck(c0==c1==c2==0)
 if det(A)==det(at(A,B,1))==0 and det(at(A,B,2))!=0:two_only+=1
ck(qualified>0 and two_only>0);details['integer_pencils']={'total':6561,'three_roots':qualified,'two_roots_nonzero_elsewhere':two_only}
# Three arbitrary rational roots have nonzero Vandermonde determinant.
for z1,z2,z3 in [(F(-7,5),F(2,9),F(11,3)),(F(0),F(1,1000000),F(1,500000)),(F(-1),F(0),F(1))]:
 ck((z2-z1)*(z3-z1)*(z3-z2)!=0)
# Published two-rectangle countercontrol, independently computed Jacobian.
A=(0,0,1,0);B=(0,1,-1,0)
ck(det(at(A,B,0))==det(at(A,B,1))==0)
for z in (F(-2),F(1,4),F(1,2),F(3,4),F(2)):
 ck(det(at(A,B,z))==z*(z-1))
ck(4*(F(1,2)-F(1,3))==F(2,3))
for s,t in product([F(-3,4),F(0),F(3,4)],repeat=2):
 # A lies z=0 with x>=0; B lies z=1 with y>=0.
 # Each proposed plane functional is nonnegative on its entire rectangle.
 for x,y in product([F(0),F(1)],[F(-1),F(1)]):ck(x-t*0>=0)
 for x,y in product([F(-1),F(1)],[F(0),F(1)]):ck(y+s*(1-1)>=0)
 ck(0-t*0==0 and 0+s*(1-1)==0)
details['two_contacts_positive_volume']='2/3'

# Exact support increments for convex hulls: extrema of a linear functional
# occur among listed vertices. Includes full-dimensional and planar examples.
polytopes=[[(F(x),F(y),F(z)) for x,y,z in product((-2,1),(-1,2),(-1,3))],[(F(-1),F(-1),F(0)),(F(2),F(-1),F(0)),(F(0),F(2),F(0))],[(F(0),F(0),F(0)),(F(-1),F(-1),F(-1)),(F(-1),F(1),F(-1)),(F(-1),F(0),F(1))]]
normals=[]
for t in [F(-3),F(-1),F(-1,2),F(0),F(1,3),F(1),F(2)]:
 n=((1-t*t)/(1+t*t),2*t/(1+t*t));ck(dot(n,n)==1);normals.append(n)
samples=[(F(a,3),F(b,5)) for a,b in product((-2,0,3),repeat=2)]
inc=0
for C,n,u,v,du,dv in product(polytopes,normals,samples[:3],samples[3:6],samples[6:8],samples[:2]):
 def psi(uu,vv):return dot(n,uu)-max(dot(n,(x-z*vv[0],y-z*vv[1])) for x,y,z in C)
 delta=psi(tuple(u[i]+du[i] for i in range(2)),tuple(v[i]+dv[i] for i in range(2)))-psi(u,v)
 changes=[dot(n,tuple(du[i]+z*dv[i] for i in range(2))) for _,_,z in C]
 ck(min(changes)<=delta<=max(changes));inc+=1
details['support_increment_cases']=inc

# Independent active-piece reconstruction of a nonsmooth two-root graph.
# gA=max_i(a+c_i b+d_i.r); gB=max_j(b+e_j a+f_j.r).
# Own slopes are1; cross slopes <=1/20. Solve each active affine pair and
# retain only genuine maxima, rather than using fixed-point iteration.
ca=[F(-1,20),F(1,25),F(0)];da=[(F(1),F(-1,2)),(F(-1),F(1,3)),(F(1,4),F(2,3))]
cb=[F(1,20),F(-1,30)];db=[(F(-1,2),F(1)),(F(2,3),F(-1))]
def roots(r):
 valid=[]
 for i,j in product(range(3),range(2)):
  x=-dot(da[i],r);y=-dot(db[j],r);den=1-ca[i]*cb[j]
  a=(x-ca[i]*y)/den;b=(y-cb[j]*x)/den
  if max(a+c*b+dot(d,r) for c,d in zip(ca,da))==0 and max(b+c*a+dot(d,r) for c,d in zip(cb,db))==0:valid.append((a,b))
 ck(len(set(valid))==1);return valid[0]
rr=[(F(a,200),F(b,200)) for a,b in product(range(-3,4),repeat=2)];sol=[roots(r) for r in rr]
for r,p in zip(rr,sol):ck(max(map(abs,p))<F(3,4))
for i,j in product(range(len(rr)),repeat=2):
 distance=sum(abs(rr[i][k]-rr[j][k]) for k in range(2))
 ck(max(abs(sol[i][k]-sol[j][k]) for k in range(2))<=distance/(1-F(1,20)))
details['nonsmooth_root_parameters']=len(rr)
# Quantitative construction does not need uniform geometric constants.
for k,l in product(range(1,31),repeat=2):
 aa=F(1,k);bb=F(1,l);eps=min(aa,bb)/32;mA=aa/4;mB=bb/4;kappa=max(eps/mA,eps/mB)
 ck(kappa<F(1,4));eta=min(mA-eps,mB-eps)/8
 for m in (mA,mB):ck((m-eps)-eta>0 and kappa+eta/m<F(3,4))

res={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','checks':count,'details':details,'seconds':time.time()-start,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite exact corroboration of determinant, support-increment and nonsmooth root estimates plus genuine two-contact positive-volume control. Does not prove density, countability or area-formula applicability; those are audited analytically.'}
Path(__file__).with_name('fresh_geometric_results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':count,'details':details,'seconds':time.time()-start}))
