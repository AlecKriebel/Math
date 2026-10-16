#!/usr/bin/env python3
"""Exact checks for the normalization and square-complex recurrence audit.
Uses the terminating hypergeometric formula, not the submitted Laguerre code.
Finite checks do not certify the real-case analytic dependency chain.
"""
from fractions import Fraction as F
from pathlib import Path
import json

checks=[]
def check(name,value):
    assert value,name
    checks.append(name)
def moment(n):
    # E Tr(W^(1/2))/sqrt(pi), alpha=0, CMOS equation (4.11).
    term=F(1);total=term
    for k in range(n-1):
        term*=F(2*k+1,2)*F(2*k+5,2)*F(1-n+k)/((k+2)*(k+2)*(k+1))
        total+=term
    return F(n*n,2)*total
q={n:moment(n) for n in range(1,18)}
check('one_dimensional_complex',q[1]==F(1,2))
check('two_dimensional_complex',q[2]==F(11,8))
check('initial_normalized_decrease',F(11,8)**2<2**3*F(1,2)**2)
for n in range(2,17):
    check(f'square_recurrence_{n}',q[n+1]==(2+F(3,4*n*n))*q[n]-q[n-1])
for n in range(1,17):
    check(f'strict_normalized_decrease_{n}',q[n+1]**2*n**3<q[n]**2*(n+1)**3)
# The real proof's squared coefficient-ratio estimate has this expansion at N=t+3.
for t in range(0,17):
    n=t+3
    check(f'real_coefficient_polynomial_{n}',4*n**3-4*n*n-13*n+4==4*t**3+32*t*t+71*t+37)
check('real_uniform_reserve_rational',(F(4,5)**3)>F(7,10)**2)
check('real_reserve_pi_rational',F(7,10)/(32*F(22,7))>F(1,160))
result={'passed':len(checks),'failed':0,'checks':checks,'normalization':'q_n = E Tr(W^(1/2))/sqrt(pi), W=X X*, X square standard complex Gaussian. The target is sqrt(pi)*q_n/n^(3/2).','real_proof_certified':False,'scope':'Finite exact hypergeometric/recurrence and elementary-polynomial checks only; source and analytic audit in REVIEW.md.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS {len(checks)} independent exact checks')
