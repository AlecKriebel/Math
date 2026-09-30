"""Independent exact controls for the restricted NLS diagnostics.

Requires SymPy. This is not a simulation or an existence/recurrence certificate.
Run from any directory; outputs independent_results.json beside this script.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import itertools
import json
import sympy as s

ROOT = Path(__file__).resolve().parent
EXPECTED = 'f92528750685bd135da7d7e09e57edd1f3c28c66439abdd6b43e153f5862124e'
artifact = ROOT / 'author_replay' / 'PARTIAL_RESULT.md'
assert hashlib.sha256(artifact.read_bytes()).hexdigest() == EXPECTED
counts = {'symbolic_generator_and_flow': 0, 'rational_phase_controls': 0,
          'integral_additivity_controls': 0, 'finite_markov_controls': 0}

def check(value, category):
    assert bool(value)
    counts[category] += 1

# An arbitrary 5x4 diffusion matrix with zero middle-action row.
a, r, b, u, v = s.symbols('a r b u v', real=True)
coords = [a, r, b, u, v]
F = s.Function('F')(r)
sig = s.Matrix(5, 4, lambda i,j: 0 if i == 1 else s.Symbol(f'z{i}{j}'))
cov = sig * sig.T
H = s.hessian(F, coords)
drift = s.Matrix([s.Symbol('ba'), -2*r*(a*s.sin(u)+b*s.sin(v)),
                  s.Symbol('bb'), s.Symbol('bu'), s.Symbol('bv')])
second = sum(cov[i,j]*H[i,j] for i in range(5) for j in range(5))/2
first = sum(drift[i]*s.diff(F, coords[i]) for i in range(5))
cat = 'symbolic_generator_and_flow'
check(s.simplify(second) == 0, cat)
check(s.simplify(first + 2*r*s.diff(F,r)*(a*s.sin(u)+b*s.sin(v))) == 0, cat)
check(s.simplify(first.subs({u:-s.pi/2,v:-s.pi/2}) - 2*r*(a+b)*s.diff(F,r)) == 0, cat)
check(s.simplify(first.subs({u:s.pi/2,v:s.pi/2}) + 2*r*(a+b)*s.diff(F,r)) == 0, cat)
t, c0, c1, c2, initial = s.symbols('t c0 c1 c2 initial', real=True)
A = c0+c1*t+c2*t*t
sol = initial*s.exp(-2*(c0*t+c1*t*t/2+c2*t**3/3))
check(s.simplify(s.diff(sol,t)+2*A*sol)==0, cat)
check(sol.subs(t,0)==initial, cat)
check(sol.subs(initial,0)==0, cat)

for aa, rr, bb, dd in itertools.product([Q(1,7),Q(1),Q(11,3)],
        [Q(1,100),Q(1),Q(100)], [Q(1,11),Q(2),Q(17)],
        [Q(-5),Q(-1,9),Q(0),Q(1,9),Q(5)]):
    phase_values = [-2*rr*dd*(aa*su+bb*sv)
                    for su,sv in itertools.product([-1,0,1], repeat=2)]
    check(min(phase_values) <= 0 <= max(phase_values), 'rational_phase_controls')
    check(max(phase_values) == 2*rr*abs(dd)*(aa+bb), 'rational_phase_controls')
    check(min(phase_values) == -max(phase_values), 'rational_phase_controls')
    check((max(phase_values)>0) == (dd!=0), 'rational_phase_controls')

# Logarithms of the integrating factor add under arbitrary partitions.
for coefficients in itertools.product(range(-2,3), repeat=3):
    lengths = [Q(1,3),Q(2,5),Q(7,11)]
    whole = -2*sum(Q(x)*h for x,h in zip(coefficients,lengths))
    split = sum(-2*Q(x)*(h/3)-2*Q(x)*(2*h/3)
                for x,h in zip(coefficients,lengths))
    check(whole == split, 'integral_additivity_controls')
    check(-whole == -2*sum(Q(-x)*h for x,h in zip(coefficients,lengths)),
          'integral_additivity_controls')

# Exact finite-state controls for the bounded-convergence uniqueness implication.
# Refresh kernels P(q)=q*Id+(1-q)*1*pi, where q=exp(-t).
def kernel(pi,q):
    return [[q*(i==j)+(1-q)*pi[j] for j in range(len(pi))]
            for i in range(len(pi))]
def matmul(A,B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def rowmul(v,P):
    return [sum(v[i]*P[i][j] for i in range(len(v))) for j in range(len(v))]
for weights in [(1,1),(1,2,3),(1,3,5,7)]:
    pi = [Q(w,sum(weights)) for w in weights]
    n = len(pi)
    for q in [Q(0),Q(1,3),Q(4,5)]:
        P = kernel(pi,q)
        check(all(sum(row)==1 and min(row)>=0 for row in P), 'finite_markov_controls')
        check(rowmul(pi,P)==pi, 'finite_markov_controls')
        for j in range(n):
            nu = [Q(i==j) for i in range(n)]
            residual = [x-y for x,y in zip(rowmul(nu,P),nu)]
            check(residual == [(1-q)*(p-x) for p,x in zip(pi,nu)], 'finite_markov_controls')
        for q2 in [Q(0),Q(2,7),Q(1)]:
            check(matmul(P,kernel(pi,q2))==kernel(pi,q*q2), 'finite_markov_controls')

result = {'all_pass':True,'assertions':sum(counts.values()),'counts':counts,
          'artifact_sha256':EXPECTED,
          'scope':'Exact restricted generator, phase, integrating-factor and finite Markov controls; no SDE existence, recurrence, regularity or model-transfer certificate.'}
(ROOT/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
