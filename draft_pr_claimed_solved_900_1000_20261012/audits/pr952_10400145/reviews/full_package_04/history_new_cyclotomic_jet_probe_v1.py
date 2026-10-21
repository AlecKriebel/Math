"""Independent full04 boundary design: parity-local jets at q=-1.
Exact finite controls corroborate the accompanying general finite-coordinate proof.
No candidate or earlier checker implementation is imported.
"""
import sys,json,math,datetime
from fractions import Fraction
def need(x,m):
 if not x:raise RuntimeError(m)
def binom(z,d):
 v=1
 for k in range(d):v=v*(z-k)//(k+1)
 return v
def coeff(e,j,n,d,sign):return (sign**(e+j*n))*binom(e+j*n,d)
def diff(v):return [b-a for a,b in zip(v,v[1:])]
checks=0
for sign in (1,-1):
 step=1 if sign==1 else 2
 for e in range(-7,8):
  for j in range(8):
   for d in range(6):
    for initial in range(1,9):
     v=[coeff(e,j,initial+step*k,d,sign) for k in range(d+2)]
     for _ in range(d+1):v=diff(v)
     need(v==[0], 'degree bound within root residue');checks+=1
# Genuine negative control: global affinity at -1 is false already for P=t.
slopes=[int(coeff(0,1,n,1,-1)) for n in (1,2,3)]
need(slopes==[-1,2,-3] and slopes[2]-2*slopes[1]+slopes[0]==-8,'global affine false at -1')
# General cubic actual invariant at q=1 is excluded with and without size1.
need([n*(n*n-1)*(-1) for n in (1,2,3)]==[0,-6,-24],'counterexample calibration')
# New residue/valuation counter-model: first jet t itself is compatible, hence
# any stronger claim that q=-1 slopes must be globally affine would be false.
print(json.dumps({'status':'PASS_NEW_CYCLOTOMIC_BOUNDARY_CONTROLS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_optimization':sys.flags.optimize,'basis_difference_checks':checks,'negative_global_affine_slopes_at_minus1':slopes,'negative_second_difference':-8,'scope':'Finite exact Laurent-monomial corroboration; general proof in MATH_REVIEW.md. No new topology calculation or predecessor claim.'},sort_keys=True))
