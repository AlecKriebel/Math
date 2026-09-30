#!/usr/bin/env python3
"""Independent rational Schur-jet and Q(sqrt(3)) extremal controls."""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
C=Counter()
def ck(g,v):
 assert v,g
 C[g]+=1
def add(z,w):return(z[0]+w[0],z[1]+w[1])
def mul(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def sc(a,z):return(a*z[0],a*z[1])
def norm(z):return z[0]**2+z[1]**2
def div(z,w):return sc(1/norm(w),mul(z,(w[0],-w[1])))
one=(F(1),F(0))
dirs=[(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1))]
for t in (F(1,2),F(1,3)):
 dirs.extend([( (1-t*t)/(1+t*t),2*t/(1+t*t)),(-(1-t*t)/(1+t*t),-2*t/(1+t*t))])
cases=0
for r in (F(1,10),F(1,3),F(1,2),F(2,3)):
 for h in (F(0),F(1,5),F(1,2),F(9,10),F(1)):
  rho=r*h
  for phase in dirs:
   w=sc(rho,phase);den=add(one,sc(-1,w));D=norm(den)
   ck('radial_phase',norm(w)==rho*rho)
   Q=rho*rho-(1-r*r)*rho+1-2*r*r
   lower=(1+rho)*Q/((1-r*r)*D)
   ck('completed_square',Q==(rho-(1-r*r)/2)**2+(3-6*r*r-r**4)/4)
   ck('strict_positive_lower',lower>0)
   for ampl in (F(0),F(1,2),F(1)):
    for direction in dirs:
     eta=sc(ampl,direction)
     delta=sc((r*r-rho*rho)/(1-r*r),eta)
     # delta=z*w'-w is the arbitrary admissible Schwarz-Pick jet perturbation.
     value=div(add(add(one,w),delta),den)[0]
     ck('schur_jet_positivity',value>=lower)
     ck('schur_jet_disk',norm(delta)<=(r*r-rho*rho)**2/(1-r*r)**2)
     cases+=1

class K:
 """Exact a+b sqrt(3), with exact ordered-real sign."""
 def __init__(self,a=0,b=0):
  if isinstance(a,K):self.a,self.b=a.a,a.b
  else:self.a,self.b=F(a),F(b)
 def __add__(self,x):x=K(x);return K(self.a+x.a,self.b+x.b)
 __radd__=__add__
 def __neg__(self):return K(-self.a,-self.b)
 def __sub__(self,x):return self+-K(x)
 def __rsub__(self,x):return K(x)+-self
 def __mul__(self,x):x=K(x);return K(self.a*x.a+3*self.b*x.b,self.a*x.b+self.b*x.a)
 __rmul__=__mul__
 def __truediv__(self,x):
  x=K(x);d=x.a*x.a-3*x.b*x.b
  return self*K(x.a/d,-x.b/d)
 def __eq__(self,x):x=K(x);return self.a==x.a and self.b==x.b
 def sign(self):
  sg=lambda x:(x>0)-(x<0)
  if self.b==0:return sg(self.a)
  if self.a==0:return sg(self.b)
  if sg(self.a)==sg(self.b):return sg(self.a)
  return sg(self.a)*sg(self.a*self.a-3*self.b*self.b)

rho=K(2,-1);q=K(-3,2) # q=R^2
ck('quadratic_field_radius',q*q+6*q-3==0)
ck('quadratic_field_contact',rho*rho-4*rho+1==0 and q==1-2*rho)
ck('positive_radius',q.sign()>0 and (1-q).sign()>0)
ck('positive_extremal_parameter',rho.sign()>0 and (1-rho*rho/q).sign()>0)
ck('extremal_a_squared',rho*rho/q==K(-1,F(2,3)))
coeff=[K(1),-rho,rho*rho-2*q,rho*q] # B(R*u)
ck('extremal_boundary_zero',sum(coeff,K())==0)
ck('extremal_negative_derivative',sum((i*x for i,x in enumerate(coeff)),K())==-6*rho)
for k in range(10,101):
 u=F(k+1,k)
 value=sum((x*u**i for i,x in enumerate(coeff)),K())
 denominator=(1-rho*u)*(1-2*rho*u+q*u*u)
 ck('beyond_radius_inside_disk',(1-q*u*u).sign()>0)
 ck('beyond_radius_positive_denominator',denominator.sign()>0)
 ck('beyond_radius_negative_convexity',value.sign()<0)

# Exact specialization of the published branch and its transition gate.
beta=F(1,2)
coeff4=8*beta*beta-3*beta-1
coeff2=-(8*beta*beta-2*beta+2)
coeff0=5*beta-1
ck('published_polynomial',(coeff4,coeff2,coeff0)==(F(-1,2),F(-3),F(3,2)))
published_square=K(5*beta-1)/(K(4*beta*beta-beta+1)+K(0,1))
ck('published_radius',published_square==q)
transition=lambda x:20*x**4-52*x**3+15*x*x+12*x-4
ck('published_branch_gate',transition(F(0))<0<transition(beta))

root=Path(__file__).resolve().parent
out={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(C),'admissible_rational_Schur_jets':cases,'artifact_sha256':sha256((root/'author_replay/KNOWN_RESULT.md').read_bytes()).hexdigest(),'scope':'Exact local derivative-bound and extremal arithmetic diagnostics; the all-function analytic proof and sharpness are assessed in the review.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
