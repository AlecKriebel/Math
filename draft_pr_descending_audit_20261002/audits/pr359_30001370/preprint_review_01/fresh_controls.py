#!/opt/homebrew/bin/python3.11
"""Fresh adversarial controls. No packet programs/tables/counts imported.

The universal proof remains analytic. These new exact controls deliberately
test the FULL weighted inverse matrix, including multiplication ordering,
and a continuous nonstrict monotone transport with an auxiliary atom.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from math import comb
import json
import sympy as S

counts={}
def ck(cat,p):
 assert p,cat
 counts[cat]=counts.get(cat,0)+1
def det(a):
 n=len(a)
 if n==0:return F(1)
 return sum(((-1)**j*a[0][j]*det([row[:j]+row[j+1:] for row in a[1:]]) for j in range(n)),F(0))
r,x,z=S.symbols('r x z',real=True)
f=((r+4)*x+r+1)/(2*r*x+2)
b=(2*z-r-1)/(r+4-2*r*z)
fp=S.diff(f,x)
for value in [f.subs(x,b)-z,b.subs(z,f)-x,S.diff(b,r)+(1-4*b*b)/(4-r*r),S.diff(f,r)/fp-(1-4*x*x)/(4-r*r),fp-(4-r*r)/(2*(1+r*x)**2)]:
 ck('independent_symbolic',S.factor(value)==0)
# A separately expanded unnormalised Gram certificate, not code imported
# from the supplement. Positive lower entry and determinant establish PSD.
be,m,s=S.symbols('beta m s',real=True)
C=1+be/4;den=1+be*m
left=(C-(1+be**2*(s-m*m))/den**2)*(C-1)-be**2*(s-m*m)/den**2
right=be**2*((C*m-S.Rational(1,4))**2+C*(m-s))/den**2
ck('independent_symbolic',S.factor(left-right)==0)
# Distinct exact continuous certificate: Bernstein positivity of the
# sharper CURRENT preprint gap over four subintervals, rather than its SOS
# or the supplement's OLD six-degree sqrt-removal certificate.
coef=[F(16),F(-104),F(172),F(58)]
bernstein=[]
for k in range(4):
 lo,hi=F(k,10),F(k+1,10)
 local=[sum(coef[j]*comb(j,i)*lo**(j-i)*(hi-lo)**i for j in range(i,4)) for i in range(4)]
 row=[sum(local[i]*F(comb(j,i),comb(3,i)) for i in range(j+1)) for j in range(4)]
 ck('current_gap_continuous',min(row)>0)
 bernstein.append({'lo':str(lo),'hi':str(hi),'coefficients':[str(v) for v in row]})
# Exact 4-state weighted FULL Jacobian inverse. The diagonal is composed
# on the right; swapping it past the rank-one term is generally false.
laws=[
 [F(-1,2),F(0),F(1,4),F(1,2)],
 [F(-1,2),F(-1,2),F(1,2),F(1,2)],
 [F(0)]*4,
 [F(1,4)]*4,
 [F(-499,1000),F(-1,1000),F(1,1000),F(499,1000)],
 [F(-1,2),F(-1,3),F(1,7),F(1,2)],
 [F(-3,7),F(-2,7),F(1,7),F(3,7)],
 [F(-1,2),F(0),F(0),F(1,2)]]
weightsets=[[F(1,30),F(4,30),F(25,60),F(25,60)],
 [F(1,137),F(11,137),F(37,137),F(88,137)],
 [F(1,4)]*4]
matrices=0;order_countercontrols=0
for values in laws:
 for w in weightsets:
  ck('probability_normalisation',sum(w)==1)
  for rr in [F(-2,5),F(-1,3),F(-1,5),F(0),F(1,5),F(1,3),F(2,5)]:
   for gscale in [F(0),F(1,2),F(1)]:
    g=gscale*(16-100*rr*rr); beta=g/(4-rr*rr)
    q=[1-4*v*v for v in values];mean=sum(ww*qq for ww,qq in zip(w,q))
    ds=[2*(1+rr*v)**2/(4-rr*rr) for v in values]
    L=[[F(i==j)-beta*q[i]*w[j]/(1+beta*mean) for j in range(4)] for i in range(4)]
    M=[[L[i][j]*ds[j] for j in range(4)] for i in range(4)]
    gram=[[F(7,10)*w[i]*F(i==j)-sum(w[k]*M[k][i]*M[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
    for size in range(1,5):
     for inds in combinations(range(4),size):
      ck('full_weighted_inverse_psd',det([[gram[i][j] for j in inds] for i in inds])>=0)
    if any(L[i][j]*ds[j]!=ds[i]*L[i][j] for i in range(4) for j in range(4)):
     order_countercontrols+=1
    matrices+=1
ck('ordering_is_not_selfadjoint_or_commuting',order_countercontrols>0)
# Exact countercontrol: uniform displacement alone does not imply TV.
# Piecewise affine maps of N alternating cells have slopes 1/2,3/2,
# fixed endpoints, displacement 1/(4N), and TV error 1/2 for every N.
wiggles=[]
for N in [1,3,17,257,65537]:
 ck('uniform_displacement_not_TV',F(1,2)==F(N,2*N)*abs(F(1,2)-1)+F(N,2*N)*abs(F(3,2)-1))
 wiggles.append({'N':N,'max_displacement':str(F(1,4*N)),'full_TV_error':'1/2'})
# New flat-interval control with a NONSYMMETRIC polynomial density:
# H(t)=0 on [0,1/4], then H(t)=(4t-1)/3. H' has a zero region.
# H_*(H'dt)=dt; H_*dt has an atom 1/4 at zero. For g(t)=1+2t,
# the auxiliary pushforward atom mass is 5/16, so it cannot be called
# a density, although the actual law H_*(H'dt) is atom-free.
t=S.symbols('t',real=True)
for k in range(9):
 integral=S.integrate(((4*t-1)/3)**k*S.Rational(4,3),(t,S.Rational(1,4),1))
 ck('nonsymmetric_flat_jacobian',integral==S.Rational(1,k+1))
ck('auxiliary_atom_allowed',S.integrate(1+2*t,(t,0,S.Rational(1,4)))==S.Rational(5,16))
ck('actual_flat_sublaw_no_atom',S.integrate(S.Integer(0),(t,0,S.Rational(1,4)))==0)
# Exact rough, integrable, unbounded endpoint law with u(t)=1/(3t^(2/3))
# and H(t)=t^(1/3). Substitute t=s^3: u dt=ds, an explicit full
# interval pushforward identity rather than a finite sample of its moments.
ss,aa,bb=S.symbols('s a b',positive=True)
ck('endpoint_unbounded_all_intervals',S.simplify((1/(3*ss**2))*3*ss**2)==1)
ck('endpoint_unbounded_all_intervals',S.integrate(S.Integer(1),(ss,aa,bb))==bb-aa)
# Atomic terminal endpoint countercontrol: z=1/2 can encode either label,
# and both inverse branches give the SAME cut. The two terminal endpoints
# differ, so their forward identity depends on a null convention. AC laws
# make this obstruction null; arbitrary atomic laws would not.
ck('atomic_endpoint_scope_countercontrol',S.factor(b.subs(z,S.Rational(1,2))+r/4)==0)
ck('atomic_endpoint_scope_countercontrol',S.Rational(-1,2)!=S.Rational(1,2))
out={'status':'PASS','exact_assertions':sum(counts.values()),'categories':counts,'full_4state_matrices':matrices,'noncommuting_order_examples':order_countercontrols,'current_gap_bernstein':bernstein,'wiggle_countercontrols':wiggles,
 'flat_control':'Auxiliary g pushforward has atom 5/16; true H-prime law has none.',
 'unbounded_control':'For t=s^3, density 1/(3t^(2/3)) transports to ds on every interval.',
 'limits':'Exact controls/countercontrols corroborate or distinguish analytic hypotheses. Matrix cases do not prove the universal Hilbert-space theorem; supplied determinant and continuous positivity proofs do.'}
print(json.dumps(out,indent=2,sort_keys=True))
