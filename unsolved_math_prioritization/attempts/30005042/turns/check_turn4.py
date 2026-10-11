#!/usr/bin/env python3
"""Exact controls for endpoint scalar estimates and the true geometric coupling."""
from fractions import Fraction as F
from collections import Counter,defaultdict
from itertools import product
from pathlib import Path
import hashlib,json
import sympy as S
C=Counter()
def ck(p,k):
    assert p,k
    C[k]+=1

# Exact infinite variance-series bound for arbitrary rational lambda>=a>1.
for a,lam in [(F(3,2),F(3,2)),(F(3,2),F(2)),(F(2),F(3)),(F(5,4),F(7,4))]:
    for n,y in product(range(1,18),range(0,80)):
        k=n
        while lam**k<y:k+=1
        lhs=F(y*y)*lam**(-k)/(1-1/lam)
        rhs=a/(a-1)*min(F(y*y)/a**n,F(y))
        ck(lhs<=rhs,'uniform_scalar_variance_series')

# Conditional martingale differences, directly convolving a finite offspring law.
X={0:F(1,4),2:F(1,2),4:F(1,4)};mean=F(2)
def convolution(A,B):
    d=defaultdict(F)
    for x,p in A.items():
        for y,q in B.items():d[x+y]+=p*q
    return d
for k in range(1,5):
    trunc={};u=defaultdict(F)
    for x,p in X.items():u[x if x<=mean**k else 0]+=p
    mu=sum(x*p for x,p in u.items());var=sum((x-mu)**2*p for x,p in u.items())
    law={0:F(1)}
    for pop in range(17):
        dmean=sum((x-pop*mu)*p for x,p in law.items())
        second=sum((x-pop*mu)**2*p for x,p in law.items())
        ck(dmean==0,'conditional_temporal_centering')
        ck(second==pop*var,'conditional_temporal_variance')
        ck(second<=pop*sum(x*x*p for x,p in u.items()),'no_population_second_moment_needed')
        law=convolution(law,u)

for lam,mu,n in product([F(5,4),F(3,2),F(2)],[F(5,2),F(3),F(4)],range(1,25)):
    if mu<=lam:continue
    ck(2*(1-(lam/mu)**n)<=2*n*(mu-lam)/lam,'monotone_generation_L1_modulus')
for x,y,K in product(range(12),range(12),range(1,6)):
    ck(x*int(x>2*K)<=2*abs(x-y)+2*y*int(y>K),'uniform_integrability_tail_inequality')

# Symbolically derive the source geometric factorial moments and joint equations.
l,m,z=S.symbols('l m z',positive=True)
G=1/(1+l*(1-z));inc=(1+l*(1-z))/(1+m*(1-z))
for k in range(1,5):ck(S.simplify(S.diff(G,z,k).subs(z,1)-S.factorial(k)*l**k)==0,'geometric_factorial_moment')
ck(S.simplify(S.diff(inc,z).subs(z,1)-(m-l))==0,'geometric_increment_mean')
m20=2*l/(l-1);m02=2*m/(m-1);m11=(l+m)/(m-1)
m21=2*l*(2*l*l*m+l*m*m-l-2*m)/((l-1)*(m-1)*(l*m-1))
ck(S.factor((l*l*m-l)*m21-(2*l*l*(m20+2*m11)+6*l**3+(m-l)*(l*m20+2*l*l)))==0,'common_descendant_m21_expansion')
candidate=2*l*(2*l+m)/((l-1)*(m-1))
ck(S.factor(m21-candidate-2*l*(l-m)/((l-1)*(m-1)*(l*m-1)))==0,'independent_increment_moment_defect')
ck(S.factor((l-1)*(m-1)*(m11-1)-(l*l-1))==0,'matching_covariance_is_insufficient')

# Exact rational continued-fraction certificates and candidate comparisons.
def phi(r,t):return (r-1+t)/(r-1+r*t)
def coefficient(l,m,t):return phi(m,t)*(1+l*(1-phi(m,t/m)))
def bounds(l,m,s,t,n):
    q=1-s/l**n-t/m**n
    ck(0<=q<=1,'mean_corrected_terminal_range')
    for k in reversed(range(n)):
        x=t/m**k;c=coefficient(l,m,x)
        ck(0<c<=1,'continued_fraction_coefficient')
        ck(c==(1+l*(1-phi(m,x/m)))/(1+m*(1-phi(m,x/m))),'coefficient_source_identity')
        q=c/(1+l-l*q)
        ck(0<=q<=1,'continued_fraction_range')
    a=2*l/(l-1);b=2*m/(m-1);d=(l+m)/(m-1)
    err=l**n*(s*s/l**(2*n)*a+2*s*t/(l*m)**n*d+t*t/m**(2*n)*b)/2
    return q,q+err
examples=[]
for l0,m0 in [(F(2),F(3)),(F(3,2),F(5,2)),(F(3),F(4))]:
    for s,t in product([F(0),F(1,2),F(1),F(2)],repeat=2):
        intervals=[]
        for n in [8,12,16]:
            lo,hi=bounds(l0,m0,s,t,n);intervals.append((lo,hi))
            if t==0:ck(lo<=phi(l0,s)<=hi,'known_first_marginal_enclosed')
            if s==0:ck(lo<=phi(m0,t)<=hi,'known_second_marginal_enclosed')
        ck(max(x[0] for x in intervals)<=min(x[1] for x in intervals),'rational_enclosure_compatibility')
lo,hi=bounds(F(2),F(3),F(1),F(1),8)
ck(lo>F(1,2),'exact_transform_separates_subordinator_candidate')
ck(m21.subs({l:2,m:3})==S.Rational(68,5),'exact_true_third_moment')
ck(candidate.subs({l:2,m:3})==14,'exact_false_candidate_third_moment')
examples.append({'lambda':'2','mu':'3','s':'1','t':'1','depth':8,'lower':str(lo),'upper':str(hi),'false_candidate_value':'1/2'})

out={'problem_id':30005042,'author_turn':4,'exact_assertions':sum(C.values()),'by_kind':dict(sorted(C.items())),
     'rational_certificates':examples,'scope':'Exact finite controls. The temporal maximum estimate keeps the parameter supremum outside expectation. The geometric result is bivariate; the full source endpoint and simple-process questions remain unresolved.',
     'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,indent=2,sort_keys=True))
