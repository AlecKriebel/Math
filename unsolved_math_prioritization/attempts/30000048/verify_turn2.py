"""Exact finite classification in the explicitly specified SU(3) character span."""
from fractions import Fraction as F
from itertools import permutations,product
import hashlib,json
checks=0

def ck(x):
 global checks
 assert x
 checks+=1

def add(a,b):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,0)+v
 return {k:v for k,v in c.items() if v}

def scale(a,s):return {k:s*v for k,v in a.items() if s*v}

def mul(a,b):
 c={}
 for (i,j),v in a.items():
  for (k,l),w in b.items():c[i+k,j+l]=c.get((i+k,j+l),0)+v*w
 return {k:v for k,v in c.items() if v}

def conj(a):return {(-i,-j):v for (i,j),v in a.items()}

def power(a,n):
 out={(0,0):1}
 for _ in range(n):out=mul(out,a)
 return out

def alt(exps):
 eig=[(1,0),(0,1),(-1,-1)];out={}
 for perm in permutations(range(3)):
  sign=(-1 if sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))%2 else 1)
  e=tuple(sum(exps[i]*eig[perm[i]][j] for i in range(3)) for j in range(2))
  out[e]=out.get(e,0)+sign
 return {k:v for k,v in out.items() if v}
unit={(0,0):1};u={(1,0):1,(0,1):1,(-1,-1):1};v=conj(u);x=mul(u,v);y=add(power(u,3),power(v,3))
chi8=add(x,scale(unit,-1));chi6=add(power(u,2),scale(v,-1));chi10=add(add(power(u,3),scale(x,-2)),unit);chi27=add(power(x,2),scale(y,-1))
Den=alt((2,1,0))
for (a,b),ch,dim in [((1,0),u,3),((2,0),chi6,6),((1,1),chi8,8),((3,0),chi10,10),((0,3),conj(chi10),10),((2,2),chi27,27)]:
 ck(mul(Den,ch)==alt((a+b+2,b+1,0)))
 ck(sum(ch.values())==dim)
 ck((a+1)*(b+1)*(a+b+2)==2*dim)
# Exact normalized Weyl-constant inner products for the chosen characters.
weight=mul(Den,conj(Den))
cs=[unit,chi8,chi10,conj(chi10),chi27]
for i,a in enumerate(cs):
 for j,b in enumerate(cs):ck(F(mul(mul(a,conj(b)),weight).get((0,0),0),6)==(1 if i==j else 0))
# Every sample is an actual diagonal SU3 trace, not an arbitrary plane point.
points=[]
for j in range(31):
 t=F(j,10);points.append(('real',t,t*t,2*t**3));ck(-1<=t<=3)
 if t<=1:points.append(('real',-t,t*t,-2*t**3));ck(-1<=-t<=3)
for j in range(10,91):
 xx=F(j,10);z=F(xx-5,4);yy=(xx*xx+18*xx-27)/4
 ck(-1<=z<=1);ck(yy==4*z*z+28*z+22)
 points.append(('double_eigenvalue',xx,xx,yy))
expected={(0,0,0),(1,0,0),(1,0,1),(2,1,1)}
survivors=[];witnesses=[];family_counts={};total=0
for a in range(-8,9):
 for b in range(-10,11):
  for c in range(-27,28):
   total+=1;A=1-a+2*b;B=a-4*b;C=c;D=b-c
   found=None
   for idx,(family,param,xx,yy) in enumerate(points):
    value=A+B*xx+C*xx*xx+D*yy
    if value<0:
     found=[a,b,c,idx,str(value)];ck(value<0);family_counts[family]=family_counts.get(family,0)+1;break
   if found is None:survivors.append((a,b,c))
   else:witnesses.append(found)
ck(total==17*21*55==19635)
ck(set(survivors)==expected)
# Global sufficiency is an exact character-square identity, never the sample grid.
for (a,b,c),root in [((0,0,0),unit),((1,0,0),u),((1,0,1),chi6),((2,1,1),chi8)]:
 f=add(add(add(unit,scale(chi8,a)),scale(add(chi10,conj(chi10)),b)),scale(chi27,c))
 ck(f==mul(root,conj(root)))
 ck(F(mul(f,weight).get((0,0),0),6)==1)
ck(len(witnesses)==19631)
digest=hashlib.sha256(json.dumps(witnesses,separators=(',',':')).encode()).hexdigest()
print(json.dumps({'status':'PASS_EXACT_FINITE_SPAN_CLASSIFICATION','exact_assertions':checks,'integer_triples':total,'excluded_by_exact_negative_witness':len(witnesses),'witness_family_counts':family_counts,'witness_stream_sha256':digest,'actual_group_test_points':len(points),'surviving_triples':survivors,'survivor_square_root_dimensions':[1,3,6,8],'scope':'Complete classification only for 1+a chi_(1,1)+b(chi_(3,0)+chi_(0,3))+c chi_(2,2), a,b,c integers. Character coefficient bounds and actual diagonal realizations are proved in TURN_2.md. Global positivity of survivors is certified by exact irreducible-square identities.','original_status':'unresolved','completed_substantive_author_turns':2},indent=2,sort_keys=True))
