#!/usr/bin/env python3
"""Exact independent controls supporting the literal source/mathematical gate.
No claim that finite controls prove an all-mesh theorem. All output stays here.
"""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
from hashlib import sha256
import json

root = Path(__file__).resolve().parent
checks = []
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

# Barycentric monomial integrals normalized by physical triangle area.
def normalized_integral(a, b, c):
    return Q(2 * factorial(a) * factorial(b) * factorial(c), factorial(a+b+c+2))
check('quadratic_edge_mean', 4*normalized_integral(1,1,0) == Q(1,3))
check('cubic_correction_mean', 20*normalized_integral(1,1,1) == Q(1,3))
check('mean_zero', 4*normalized_integral(1,1,0)-20*normalized_integral(1,1,1)==0)
check('edge_trace_integral', 4*(Q(1,2)-Q(1,3)) == Q(2,3))
# On AB, lambda_C=0; on AC or BC, one of lambda_A,lambda_B=0.
# The formula has these factors, establishing trace compatibility identically.

# Exact geometry and scale invariance of the chosen center-to-corner jump.
gradients = [(Q(0),Q(2)),(Q(-2),Q(0)),(Q(0),Q(-2)),(Q(2),Q(0))]
check('center_hat_energy', sum((a*a+b*b)/4 for a,b in gradients)==4)
for i in range(4):
    a,b = gradients[i],gradients[(i+1)%4]
    check(f'jump_squared_{i}',sum((a[k]-b[k])**2 for k in range(2))==8)
for n in range(1,65):
    check(f'tail_{n}',4*sum(Q(1,4**j) for j in range(1,n+1))+Q(4,3*4**n)==Q(4,3))
    check(f'selected_weight_{n}',sum(4**j*2*Q(1,4**j) for j in range(1,n+1))==2*n)
    # Two NVB generations turn the square base pattern into four child patterns:
    # filling a square with 4^j bases costs 4*(4^j-1), not an assumed leading constant.
    cost=sum(4*j+4*(4**j-1) for j in range(1,n+1))
    check(f'cost_upper_bound_{n}',cost<=8*4**n)

# Derive the global Cauchy allocation inequality by an exact nonnegative identity.
# This applies to every finite collection of positive m_i and real a_i.
for count in range(2,15):
    a=[Q((-1)**i*(i+2),4**(1+i%3)) for i in range(count)]
    m=[Q((i+1)*(i+2)) for i in range(count)]
    left=sum(m)*sum(x*x/y for x,y in zip(a,m))-sum(a)**2
    right=sum((a[i]*m[j]-a[j]*m[i])**2/(m[i]*m[j]) for i in range(count) for j in range(i+1,count))
    check(f'allocation_identity_{count}',left==right and right>=0)

candidate = root.parent/'original_submission/files/unsolved_math_prioritization/attempts/30000229/COUNTEREXAMPLE.md'
receipt = {
    'status':'PASS',
    'exact_assertions':len(checks),
    'candidate_sha256':sha256(candidate.read_bytes()).hexdigest(),
    'proof_role':'Exact mean, trace, jump, tail, geometric cost and allocation controls; the written uniform dual-test/overlay argument is the proof, not finite mesh enumeration.',
    'checks':checks,
}
(root/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='checks'},indent=2))
