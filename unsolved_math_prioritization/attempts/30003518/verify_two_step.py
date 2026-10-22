#!/usr/bin/env python3
"""Exact Sturm and rational-interval Hurwitz certificate, not floating eigenvalues."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,permutations
from collections import Counter
import sympy as s,json,math
C=Counter()
def ck(cat,test):
 assert test,cat
 C[cat]+=1
class I:
 def __init__(self,lo,hi=None):self.lo=F(lo);self.hi=F(lo if hi is None else hi);assert self.lo<=self.hi
 def __add__(self,other):
  o=other if isinstance(other,I) else I(other);return I(self.lo+o.lo,self.hi+o.hi)
 __radd__=__add__
 def __neg__(self):return I(-self.hi,-self.lo)
 def __sub__(self,other):return self+-asI(other)
 def __rsub__(self,other):return asI(other)+-self
 def __mul__(self,other):
  o=asI(other);v=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi];return I(min(v),max(v))
 __rmul__=__mul__
 def __truediv__(self,other):
  o=asI(other);assert o.lo*o.hi>0;return self*I(1/o.hi,1/o.lo)
 def __rtruediv__(self,other):return asI(other)/self
 def endpoints(self):return [str(self.lo),str(self.hi)]
def asI(v):return v if isinstance(v,I) else I(v)
def det(A):
 n=len(A);total=I(0)
 for p in permutations(range(n)):
  term=I((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
  for i in range(n):term=term*A[i][p[i]]
  total=total+term
 return total
def minor(A,inds):return [[A[i][j] for j in inds] for i in inds]
x=s.symbols('e');Q=4+4*x;g=2*Q+s.Rational(1,64)*4*x;h=Q+4*x+2048*x*x+x*g
raw=s.expand((256*x*g-(8-x)*h)**2-(2+4*x)*(8-x)*Q*x*g)
P=s.Poly(raw,x).clear_denoms()[1].primitive()[1]
coeff=[1082212609,-15125744400,54877391424,-14188516224,1182559232,-31653888,262144]
ck('exact_polynomial',P.all_coeffs()==coeff)
ck('degree_six',P.degree()==6)
ck('positive_clearing_factor',s.expand(256*raw-P.as_expr())==0)
# Derive the reduced original ODE Jacobian, rather than assuming the displayed matrix.
c0s,c1s,c2s,b0s,b1s=s.symbols('c0 c1 c2 b0 b1');vs=s.Matrix([c0s,c1s,c2s,b0s,b1s]);rr=256-sum(vs);ee=8-b0s-b1s;zz=-2*rr
ODE=s.Matrix([rr**2-2*c0s-8*c0s*ee+2*b0s,2*b0s-4*c1s-8*c1s*ee+256*b1s,256*b1s-c2s/128,8*c0s*ee-4*b0s,8*c1s*ee-512*b1s])
Jexact=s.Matrix([[zz-2-8*ee,zz,zz,zz+8*c0s+2,zz+8*c0s],[0,-4-8*ee,0,2+8*c1s,8*c1s+256],[0,0,-s.Rational(1,128),0,256],[8*ee,0,0,-8*c0s-4,-8*c0s],[0,8*ee,0,-8*c1s,-8*c1s-512]])
for v in ODE.jacobian(vs)-Jexact:ck('original_ODE_jacobian',s.expand(v)==0)
ck('all_six_roots_real',P.count_roots(-s.oo,s.oo)==6)
ck('all_roots_in_enzyme_interval',P.count_roots(0,8)==6)
ck('all_roots_simple',s.gcd(P,P.diff()).degree()==0)
intervals=s.polys.polytools.intervals(P,eps=s.Rational(1,10**18));rows=[];physical=[]
for idx,((lo,hi),mult) in enumerate(intervals,1):
 ck('sturm_isolated_root',P.count_roots(lo,hi)==1 and mult==1)
 e=I(F(lo),F(hi));gg=8+F(129,16)*e
 c0=(8-e)*(4+4*e)/(e*gg);c1=(8-e)*4/gg;c2=(8-e)*2048*e/gg
 b0=2*e*c0;b1=F(1,64)*e*c1;r=256-c0-c1-c2-b0-b1
 for val in [e,8-e,c0,c1,c2,b0,b1]:ck('strict_positive_bound_species',val.lo>0)
 good=r.lo>0
 ck('physical_filter_decided',good or r.hi<0)
 row={'index':idx,'enzyme_interval':[str(lo),str(hi)],'physical':good,'free_receptor_interval':r.endpoints()}
 if good:
  physical.append(idx);z=-2*r
  J=[[z-2-8*e,z,z,z+8*c0+2,z+8*c0],
     [I(0),-4-8*e,I(0),2+8*c1,8*c1+256],
     [I(0),I(0),I(-F(1,128)),I(0),I(256)],
     [8*e,I(0),I(0),-8*c0-4,-8*c0],
     [I(0),8*e,I(0),-8*c1,-8*c1-512]]
  a=[I(1)]
  for size in range(1,6):a.append(sum((det(minor([[-v for v in line] for line in J],inds)) for inds in combinations(range(5),size)),I(0)))
  H=[[a[2*j-i+1] if 0<=2*j-i+1<=5 else I(0) for j in range(5)] for i in range(5)]
  ds=[det(minor(H,list(range(k)))) for k in range(1,6)]
  stable=all(v.lo>0 for v in ds)
  if idx in [2,6]:
   for v in ds:ck('stable_Hurwitz_positive',v.lo>0)
   row['dynamics']='hyperbolic sink by all five Hurwitz determinants'
  else:
   ck('unstable_positive_real_eigenvalue',a[5].hi<0)
   for v in ds[:4]:ck('index_one_Routh_positive_prefix',v.lo>0)
   row['dynamics']='hyperbolic index-one saddle by nonzero Routh first column with exactly one sign change'
  # Rounded outward integer enclosures are smaller, still exact certificates.
  row['characteristic_coefficient_integer_enclosures']=[[math.floor(v.lo),math.ceil(v.hi)] for v in a]
  row['Hurwitz_determinant_integer_enclosures']=[[math.floor(v.lo),math.ceil(v.hi)] for v in ds]
 rows.append(row)
ck('exactly_three_physical_equilibria',physical==[2,3,6])
out={'status':'PASS_EXACT','assertions':sum(C.values()),'categories':dict(C),'polynomial_coefficients_descending':coeff,'all_original_rates':{'binding':1,'d0':2,'d1':4,'d2':'1/128','association0':8,'dissociation0':2,'catalysis0':2,'association1':8,'dissociation1':256,'catalysis1':256},'totals':{'receptor':256,'ligand':256,'enzyme':8},'root_certificates':rows,'physical_indices':physical,'stable_indices':[2,6],'floating_point_used':False,'scope':'Exactly three physical positive equilibria, two hyperbolic sinks; no global basin classification'}
Path(__file__).with_name('two_step_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='root_certificates'},indent=2))
