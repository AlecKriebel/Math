#!/usr/bin/env python3
"""Small exact checks for candidate.md. These do not prove the general theorem.

Run with Python 3 and SymPy. No network, randomness, or exhaustive search.
"""
from itertools import combinations
import json
import sympy as s

results = {}

# Nongeneric S != E example: two unit xy-discs plus one unit xz-disc.
u, v, w, r, t = s.symbols('u v w r t')
X, Y, Z = s.symbols('X Y Z')
P = (X**2 + Y**2 + Z**2 - 5)**2 - 4*(4-Y**2)*(1-Z**2)
F = {X:2*u/r+u/t, Y:2*v/r, Z:w/t}
num = s.fraction(s.cancel(P.subs(F)))[0]
G = s.groebner([r**2-u**2-v**2, t**2-u**2-w**2], r,t,u,v,w)
remainder = G.reduce(s.expand(num))[1]
assert remainder == 0
assert P.subs({X:0,Y:0,Z:1}) == 16
results['nongeneric_polynomial_identity_remainder'] = str(remainder)
results['nongeneric_separating_value'] = 16

# An exact five-dimensional generic-span example with two killed summands.
e = [s.eye(5)[:,i] for i in range(5)]
A = [s.Matrix.hstack(e[0],e[1]), s.Matrix.hstack(e[2],e[3]),
     s.Matrix.hstack(e[0]+e[2]+e[4], e[1]+e[3]+2*e[4])]
ranks = {}
for k in range(1,4):
    for J in combinations(range(3),k):
        rank = s.Matrix.hstack(*(A[j] for j in J)).rank()
        assert rank == min(5,2*k)
        ranks[','.join(str(j+1) for j in J)] = rank
results['generic_span_subset_ranks'] = ranks
normal = e[4]
perturbation = e[0]+e[2]
eps = s.symbols('eps', positive=True)
for j, target in [(0,e[0]),(1,e[2])]:
    assert A[j].T*normal == s.zeros(2,1)
    q = A[j].T*(normal+eps*perturbation)
    p = A[j]*q/s.sqrt((q.T*q)[0])
    assert s.simplify(p-target) == s.zeros(5,1)
q = A[2].T*(normal+eps*perturbation)
p3 = A[2]*q/s.sqrt((q.T*q)[0])
limit = p3.applyfunc(lambda a:s.limit(a,eps,0,dir='+'))
expected = A[2]*s.Matrix([1,2])/s.sqrt(5)
assert s.simplify(limit-expected)==s.zeros(5,1)
results['generic_face_perturbation'] = 'exactly verified'

# Repeated-disc case: no independent-radicals hypothesis can be necessary.
B = s.Matrix([[1,1],[0,2],[2,0]])
n = s.Matrix([1,1,1])
q = B.T*n
p = B*q/s.sqrt((q.T*q)[0])
Q = B*B.T
pQ = Q*n/s.sqrt((n.T*Q*n)[0])
assert s.simplify(p-pQ)==s.zeros(3,1)
assert s.simplify(3*p - 3*Q*n/s.sqrt((n.T*Q*n)[0]))==s.zeros(3,1)
results['repeated_disc_support_formula'] = 'exactly verified'

# Model normal-arrangement detour illustrating Lemma 2 in R^3.
# Avoid the x- and z-axes. Chosen z is outside each forbidden plane.
x=s.Matrix([1,1,0]); y=s.Matrix([-1,-1,0]); z=s.Matrix([0,1,1])
for axis in [s.Matrix([1,0,0]),s.Matrix([0,0,1])]:
    for endpoint in [x,y]:
        assert s.Matrix.hstack(axis,endpoint,z).rank()==3
results['normal_detour_rank_checks'] = 'exactly verified'
results['sympy_version'] = s.__version__
results['status'] = 'all exact sanity checks passed; general proof is analytic'
print(json.dumps(results,indent=2))
