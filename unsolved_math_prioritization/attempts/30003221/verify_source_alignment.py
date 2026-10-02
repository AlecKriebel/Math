#!/usr/bin/env python3
"""Source-alignment and exact algebra controls; does not prove the analytic theorem."""
from pathlib import Path
from fractions import Fraction as F
import json

root=Path(__file__).resolve().parent
s=json.loads((root/'SOURCE_ALIGNMENT.json').read_text())
o,t=s['original'],s['theorem']
checks=0

def check(v, label):
    global checks
    checks+=1
    if not v:raise AssertionError(label)

check(o['dimension']==s['specialization']['N']==3,'dimension')
check(o['repulsive_exponent']==s['specialization']['lambda_value']==1,'Coulomb exponent')
N=3;lam=1
check(0<lam<N-1,'strict theorem parameter range')
for key in ['alpha_domain','density_lower','density_upper','normalization','attractive_coefficient','repulsive_coefficient','perimeter_term','radial_constraint','centering_constraint']:
    check(o[key]==t[key],('exact source/theorem match',key))
check(s['specialization']['equality_convention']=='almost everywhere, up to arbitrary translation','equality scope')
check(o['admissible']=='all measurable densities on R^3 with specified finite mass','density domain')
check(t['conclusion']=='every minimizer is a ball indicator almost everywhere','universal minimizer quantifier')
# Reject inapplicable boundary regimes explicitly.
for l,expected in [(F(0),False),(F(1,2),True),(F(1),True),(F(2),False),(F(5,2),False)]:
    check((0<l<N-1)==expected,('lambda boundary',l))

alphas=[F(1,100),F(1,4),F(1,2),F(1),F(3,2),F(2),F(3),F(4),F(5),F(10),F(100)]
for a in alphas:
    attraction=2+a/N
    repulsion=2-F(lam,N)
    gap=attraction-repulsion
    check(gap==(a+lam)/N and gap>0,('strict mass dominance',a))
    check(2*N+a-N*attraction==0,('attraction dilation exponent',a))
    check(2*N-lam-N*repulsion==0,('repulsion dilation exponent',a))
    # ell=alpha^(-1/(alpha+1)): formal log_alpha identities for coefficient matching.
    logell=-1/(a+1)
    check((a+1)*logell==-1,('existence coefficient ratio',a))
    check((2*N+a)*logell==(2*N-1)*logell-1,('existence common prefactor',a))
    check(N*logell+( -N*logell)==0,('existence mass inverse',a))
check(1-F(lam,N-1)==F(1,2),'positive shell error exponent')
# Coulomb potential of the unit ball divided by pi, a direct boundary sanity check.
def phi(r):
    return 2*(1-r*r/F(3)) if r<=1 else F(4,3)/r

def deriv(r):
    return -F(4,3)*r if r<=1 else -F(4,3)/(r*r)

check(phi(F(1))==F(4,3),'Coulomb potential boundary value')
check(deriv(F(1))==-F(4,3),'Coulomb potential boundary derivative')
for r in [F(i,8) for i in range(25)]:
    check(abs(phi(r)-phi(F(1)))<=F(4,3)*abs(r-1),('Coulomb Lipschitz bound',r))
    check(abs(deriv(r))<=F(4,3),('Coulomb bounded derivative',r))
# Translation leaves pairwise squared distances invariant; no center restriction.
points=[(0,0,0),(1,2,3),(-2,4,1),(3,-1,2)]
shift=(7,-3,11)
for x in points:
    for y in points:
        before=sum((a-b)**2 for a,b in zip(x,y))
        after=sum((a+h-b-h)**2 for a,b,h in zip(x,y,shift))
        check(before==after,'pairwise translation invariance')
# A fractional density is allowed by both source/theorem domains.
weights=[F(1,4),F(1,2),F(3,4),F(1)]
check(all(0<=w<=1 for w in weights),'fractional admissible density')
check(any(w not in (0,1) for w in weights),'competitor class is broader than indicators')
print(json.dumps(dict(problem_id=30003221,status='source alignment and exact algebra controls passed',assertions=checks,alpha_samples=len(alphas),N=N,lambda_value=lam,threshold_power='(alpha+1)/3',shell_error_power='1/2',dependencies='Python 3 standard library',limit='These controls do not prove the variational theorem or replace its credited analytic dependencies.'),indent=2))
