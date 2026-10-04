#!/usr/bin/env python3
"""Exact controls plus explicitly non-certifying finite numerical survey.
Python >=3.10, standard library only. No source downloads or private files.
"""
from fractions import Fraction as F
import cmath, json, math

# Rational-complex arithmetic represented by pairs, independent of float complex.
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def div(a,b):
 s=b[0]*b[0]+b[1]*b[1]
 return ((a[0]*b[0]+a[1]*b[1])/s,(a[1]*b[0]-a[0]*b[1])/s)
def norm(a):return a[0]**2+a[1]**2
one=(F(1),F(0))

def exact_controls():
 local=0
 for i in range(-8,9):
  for j in range(-8,9):
   v=(F(i,32),F(j,32))
   if norm(v)>F(1,16):continue
   for t in [F(1,1000),F(1,10),F(1,2),F(1)]:
    a=add(one,v);b=sub(a,(t,F(0)))
    assert norm(a)-norm(b)==2*t*a[0]-t*t
    assert norm(a)-norm(b)>=t/2
    assert norm(a)<=F(25,16)
    assert norm(div(b,a))<=1-F(8,25)*t
    local+=1
 conjugacy=0
 for q in [F(0),F(1,4),F(1,2),F(9,10),F(999,1000)]:
  for i in range(-3,4):
   for j in range(-3,4):
    w=(F(i,5),F(j,5))
    if norm(w)>=1:continue
    t=1-q;u=div(add(one,w),sub(one,w))
    fu=add(mul((1-t/2,F(0)),u),div((t/2,F(0)),u))
    gw=mul(w,div(add(w,(q,F(0))),add(one,mul((q,F(0)),w))))
    assert div(sub(fu,one),add(fu,one))==gw
    left=norm(add(one,mul((q,F(0)),w)))-norm(add(w,(q,F(0))))
    assert left==(1-q*q)*(1-norm(w))>0
    conjugacy+=1
 # Endpoint inequalities of linear polynomials certify |5s-1| <=1-3s.
 for s in [F(0),F(1,4)]:
  assert 1-3*s >= 5*s-1
  assert 1-3*s >= 1-5*s
  assert 1-3*s>0
 assert F(2)*F(1,2)**3/(3*F(1,2)**2-1)==-1
 assert F(1,2)*(5*F(1,2)**2-1)/(6*F(1,2)**2-2)==F(-1,4)
 # Radius formula, tested over integer degrees/multiplicities in addition to proof.
 radius=0
 for d in range(2,51):
  for m in range(1,d):
   r=F(m,4*d-3*m)
   assert 0<r<1 and (d-m)*r/(1-r)==F(m,4)
   radius+=1
 return {'local_rational_cases':local,'exact_conjugacy_cases':conjugacy,
         'radius_identity_cases':radius,'non_nesting_interval_control':'passed',
         'note':'Finite exact checks support, but do not replace, the general written proofs.'}

def label(z,h,max_iter=4000,tol=1e-9):
 for n in range(max_iter+1):
  for k,r in enumerate([-1,0,1]):
   if abs(z-r)<tol:return k,n
  if n==max_iter:return -1,n
  den=3*z*z-1
  if abs(den)<1e-28:return -1,n
  z=z-h*z*(z*z-1)/den
  if not (math.isfinite(z.real) and math.isfinite(z.imag)):return -1,n
 return -1,max_iter

def numerical_survey():
 samples=2048;params=[1,.75,.5,.25,.1];out=[]
 for radius in [3,10,100]:
  common=[0,0,0];unresolved=0;largest_iterations=0;individual=[[0,0,0] for _ in params]
  for j in range(samples):
   z=radius*cmath.exp(2j*math.pi*(j+.5)/samples)
   ll=[]
   for hi,h in enumerate(params):
    k,n=label(z,h);ll.append(k);largest_iterations=max(largest_iterations,n)
    if k<0:unresolved+=1
    else:individual[hi][k]+=1
   if len(set(ll))==1 and ll[0]>=0:common[ll[0]]+=1
  out.append({'radius':radius,'parameters':params,'samples':samples,
              'root_order':[-1,0,1],'sampled_full_basin_agreement_counts':common,
              'individual_full_basin_counts':individual,'unresolved_entries':unresolved,
              'largest_iterations':largest_iterations})
 return out

def main():
 result={'exact_controls':exact_controls(),'finite_numerical_survey':numerical_survey(),
 'numerical_limits':['No immediate-component certification','No arc or measure certificate',
 'Only a finite parameter mesh','Only three radii and one polynomial','Floating arithmetic and finite iteration limit']}
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
