#!/usr/bin/env python3
"""Deterministic exact algebraic controls for rank 663 / 4000018.
No third-party package, network, source PDF, or private corpus is needed.
These controls support the written proofs; they do not solve the open problem.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

COUNTS = {}
def check(group, assertion):
    COUNTS[group] = COUNTS.get(group, 0) + 1
    if not assertion:
        raise AssertionError((group, COUNTS[group]))

def mean(p, f):
    return sum((w*x for w,x in zip(p,f)), F(0))

def generator(p, f, rate=F(2)):
    m=mean(p,f)
    return [rate*(m-x) for x in f]

def gamma(p, f, g):
    lfg=generator(p,[x*y for x,y in zip(f,g)])
    lf,lg=generator(p,f),generator(p,g)
    return [(z-x*v-y*u)/2 for z,x,y,u,v in zip(lfg,f,g,lf,lg)]

def gamma2(p,f):
    gf=gamma(p,f,f)
    lg=generator(p,gf)
    gl=gamma(p,f,generator(p,f))
    return [a/2-b for a,b in zip(lg,gl)]

# Reset Gamma and Gamma2, from the definitions rather than copied formulas.
weights=[[F(1,2),F(1,3),F(1,6)], [F(1,7),F(2,7),F(4,7)],
         [F(1,100),F(19,100),F(4,5)]]
for p in weights:
    check('probability',sum(p)==1)
    for raw in product(range(-2,3),repeat=3):
        f=list(map(F,raw)); m=mean(p,f); g=[x-m for x in f]; V=mean(p,[x*x for x in g])
        gf=gamma(p,f,f); g2=gamma2(p,f); lf=generator(p,f)
        for i in range(3):
            check('gamma_identity',gf[i]==V+g[i]**2)
            check('gamma2_identity',g2[i]==3*V+g[i]**2)
            check('BE_infinity',g2[i]-gf[i]==2*V)
            for N in [F(1,2),F(1),F(2),F(4),F(10),F(100)]:
                K=1-4/N
                check('BE_profile_sufficiency',g2[i]-K*gf[i]-lf[i]**2/N==(3-K)*V)
                check('BE_profile_nonnegative',g2[i]-K*gf[i]-lf[i]**2/N>=0)

# Indicator witnesses for every integer dimension in a fixed nontrivial range.
for N in range(1,201):
    p=F(1,N+2); g=1-p; V=p*(1-p)
    check('BE_finite_failure',2*V-4*g*g/N<0)
    K=1-F(4,N)+F(1,N+1)
    p=F(1,100*(N+1)**2); g=1-p; V=p*(1-p)
    check('BE_profile_necessity_witness',(3-K)*V+(1-K-F(4,N))*g*g<0)

# Continuous tent witnesses: exact integrals and unbounded lower bounds.
for N in range(1,201):
    e=F(1,100*(N+1)); m=e/2; V=e/3-e*e/4; g=1-m
    check('tent_positive_variance',V>0)
    check('tent_BE_failure',2*V-4*g*g/N<0)

# The universal reset coupling's sufficient algebraic bound.
# The proof supplies A >= (2t-s)/2 and B <= 2(t-s).
# Square-root times a,b are rational so these checks are fully exact.
for ia in range(21):
    for ib in range(ia,21):
        a,b=F(ia,40),F(ib,40); s,t=a*a,b*b; q=b-a
        check('reset_time_horizon',0<=s<=t<=F(1,4))
        residual=4*(2*t-s)-(a+b)**2
        check('reset_polynomial_factor',residual==(b-a)*(7*b+5*a))
        check('reset_polynomial_nonnegative',residual>=0)
        A=(2*t-s)/2; B=2*(t-s)
        check('reset_discriminant',B*B<=32*A*q*q)
        for ir in range(1,21):
            r=F(ir,20)
            check('reset_quadratic_square',(A*r+8*q*q/r)**2-32*A*q*q==(A*r-8*q*q/r)**2)
            check('reset_coupling_sufficient',A*r+8*q*q/r>=B)

# W2-to-W1 transfer controls and scaling identities.
for ia in range(21):
    for ib in range(ia,21):
        a,b=F(ia,20),F(ib,20); s,t=a*a,b*b
        tau=F(2,3)*(t+a*b+s)
        check('heat_tau_bound',tau>=2*s)
for a in [F(1,5),F(1,2),F(1),F(3),F(11)]:
    for b in [F(0),F(1,7),F(1),F(13)]:
        check('sqrt_linearization_square',(a+b/(2*a))**2-(a*a+b)==b*b/(4*a*a))
        check('sqrt_linearization_nonnegative',(a+b/(2*a))**2>=a*a+b)
for scale in [F(1,3),F(1,2),F(2),F(7)]:
    for n in [1,2,7,31]:
        K=F(3,5); G=F(9,7); H=K*G+F(16,n); L=F(4)
        check('BE_time_scaling',scale**2*H-(scale*K)*(scale*G)-(scale*L)**2/n==0)

# File integrity and claims guardrails. Sources are metadata only.
root=Path(__file__).resolve().parent
sources=json.loads((root/'SOURCE_VERIFICATION.json').read_text())
check('source_count',len(sources['sources'])==4)
for source in sources['sources']:
    check('source_sha256',len(source['sha256'])==64 and all(c in '0123456789abcdef' for c in source['sha256']))
    check('source_size',source['bytes']>0)
    check('source_pages',source['pages']>0)
    check('source_public_url',source['url'].startswith('https://'))
status=(root/'STATUS.md').read_text()
check('status_unsolved','Verdict: UNSOLVED' in status)
check('status_noncanonical','not the canonical heat generator' in status)
proof=(root/'FULL_PROOFS.md').read_text()
for token in ['Theorem 1.', 'Theorem 2.', 'Corollary 3.', 'Proposition 4.', 'Proposition 5.', 'Proposition 6.', 'Proposition 7.']:
    check('claim_sections',token in proof)
check('source_crossref','Proposition 2.22' in proof and 'Proposition 2.12' not in proof)
result={
    'target':'4000018 / AMR-039-0018',
    'status':'PASS',
    'total_assertions':sum(COUNTS.values()),
    'assertions_by_group':COUNTS,
    'arithmetic':'Python standard-library fractions.Fraction; all mathematical assertions exact rational comparisons',
    'scope':'Finite algebraic/test-family controls only. General analytic proofs are in FULL_PROOFS.md. Original problem remains unresolved.',
}
if '--write-result' in sys.argv:
    (root/'CONTROL_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
