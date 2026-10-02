"""Exact checks of averaged thinning, full-refit corrections, and an actual Delta_h control."""
from fractions import Fraction as F
from itertools import product
from math import comb
from collections import Counter
import json
import sympy as sp
C=Counter()
def ck(v,k):assert v,k;C[k]+=1
def points(y):return product(*(range(t+1) for t in y))
def mass(u,y,a):return sp.prod([F(comb(t,k))*a**k*(1-a)**(t-k) for k,t in zip(u,y)])
def fit(u,kind):
 # Generic functions satisfying the proved envelope, for finite algebra controls.
 # These are not claimed to be the source family, except n=1 controls below.
 m=max(u);n=len(u)
 if kind==0:return tuple(F(t,2) for t in u)
 if kind==1:return (F(sum(u),n),)*n
 return tuple(F(m) if (sum(u)+i)%2 else F(0) for i in range(n))
for n in [1,2,3]:
 for y in product(range(3),repeat=n):
  S=sum(y);m=max(y)
  for a,kind in product([F(1,3),F(2,3),F(4,5)],range(3)):
   eta=1-a
   direct=F(0);center=F(0)
   for u in points(y):
    f=fit(u,kind);v=tuple(t-k for k,t in zip(u,y));p=mass(u,y,a)
    direct+=p*sum((f[i]-a*v[i]/eta)**2 for i in range(n))/n
    center+=p*sum(f[i]**2-2*a*v[i]*f[i]/eta for i in range(n))/n
   noise=a**3*S/(eta*n)+a*a*sum(t*t for t in y)/n
   ck(direct-noise==center,'exact_score_noise_centering')
   first=sum(mass(u,y,a)*sum(t*t for t in fit(u,kind))/n for u in points(y))
   cross=F(0)
   for i in range(n):
    if not y[i]:continue
    ym=tuple(t-(j==i) for j,t in enumerate(y))
    rhs=sum(mass(u,ym,a)*fit(u,kind)[i] for u in points(ym))
    lhs=sum(mass(u,y,a)*(y[i]-u[i])*fit(u,kind)[i] for u in points(y))
    ck(lhs==eta*y[i]*rhs,'binomial_delete_one_identity')
    cross+=2*a*y[i]*rhs/n
   ck(first-cross==center,'finite_centered_score_formula')
   f=fit(y,kind);limit=sum(t*t for t in f)/n
   for i in range(n):
    if y[i]:
     ym=tuple(t-(j==i) for j,t in enumerate(y));limit-=2*F(y[i],n)*fit(ym,kind)[i]
   bound=eta*(m*m*S+F(2*m*S*S,n))
   ck(abs(center-limit)<=bound,'uniform_envelope_comparison')
# Original n=1 family: F_h(y)=y(1-exp(-h)); at h=log2 it is exactly y/2.
# Check the exact averaged CV choice, the fitted deletion switch and optimism integrand.
for a in [F(2,5),F(1,2),F(9,10),F(99,100)]:
 for y in range(41):
  eta=1-a;c=F(1,2)
  delta=c*c*(a*eta*y+a*a*y*y)-2*c*a*a*y*(y-1)
  ck(delta==a*y*F(1,4)*(1-3*a*(y-1)),'actual_two_candidate_score_difference')
  pick=int(delta<0)
  ck(pick==int(y>=2),'actual_averaged_CV_threshold')
  # Fixed tie rule favors zero at y=0.
  prev=int(y-1>=2)
  optimism=2*y*(c*(y-1)*pick-c*(y-1)*prev) if y else F(0)
  ck(optimism==(2 if y==2 else 0),'exact_deletion_optimism_integrand')
  g=c*y*pick
  fixed_plugin=g*g-2*y*c*(y-1)*pick+y*(y-1)
  selected_URE=g*g-2*y*c*(y-1)*prev+y*(y-1)
  ck(selected_URE-fixed_plugin==optimism,'selected_algorithm_PURE_correction')
# Exact Poisson factorial-moment consequences for that actual source selector.
l,e=sp.symbols('lambda exp_minus_lambda')
Eg=(l-l*e)/2;Eg2=(l*l+l-l*e)/4
risk=sp.expand(Eg2-2*l*Eg+l*l);plugin=Eg2
ck(sp.expand(risk-plugin-l*l*e)==0,'closed_form_expected_optimism')
ck(sp.expand(risk-((l*l+l)/4+(l*l-l/4)*e))==0,'closed_form_selected_risk')
ck(sp.expand(risk.subs(l,1)-(sp.Rational(1,2)+sp.Rational(3,4)*e))==0,'exact_excess_over_best_fixed_at_one')
# Samplewise oracle inequality algebra when centered scores are uniformly close.
for base1,base2,d,e1,e2 in product(range(-2,3),range(-2,3),[F(0),F(1,3),F(1)],[F(-1),F(0),F(1)],[F(-1),F(0),F(1)]):
 U=[F(base1),F(base2)];CC=[U[0]+d*e1,U[1]+d*e2];j=min(range(2),key=lambda k:(CC[k],k))
 ck(U[j]<=min(U)+2*d,'criterion_minimizer_transfer')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Finite exact score/deletion/envelope identities, plus exact original-family n=1 countercontrol. No large-n regret conclusion is inferred.'},sort_keys=True,indent=2))
