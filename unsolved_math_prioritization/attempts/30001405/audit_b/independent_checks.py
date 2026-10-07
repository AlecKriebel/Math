#!/usr/bin/env python3
"""Independent exact diagnostics only. No network, source access, or file writes."""
from fractions import Fraction
from itertools import combinations, product
import json
import math
import sympy as s

checks = []
def require(name, condition):
    ok = bool(condition)
    checks.append({'name': name, 'passed': ok})
    if not ok:
        raise AssertionError(name)

def zero(a):
    return s.cancel(a) == 0

x, y, z, t, u, v, h = s.symbols('x y z t u v h')
rho = x*x+y*y
w = 1-z
a = 1-t
D = w*w+a*a*rho
H = (2*a*x*w/D, 2*a*y*w/D, (a*a*rho-w*w)/D)
f = z*z+x*x+y*y-1

def sphere_zero(expression):
    numerator = s.fraction(s.cancel(expression))[0]
    return s.rem(numerator, f, z) == 0

require('direct contraction norm identity without sphere reduction', zero(sum(c*c for c in H)-1))
require('direct contraction north-pole exclusion identity', zero(1-H[2]-2*w*w/D))
require('direct contraction start x coordinate modulo sphere', sphere_zero(H[0].subs(t,0)-x))
require('direct contraction start y coordinate modulo sphere', sphere_zero(H[1].subs(t,0)-y))
require('direct contraction start z coordinate modulo sphere', sphere_zero(H[2].subs(t,0)-z))
require('direct contraction endpoint', all(zero(c.subs(t,1)-q) for c,q in zip(H,(0,0,-1))))
require('direct contraction fixes south pole', all(zero(c.subs({x:0,y:0,z:-1})-q) for c,q in zip(H,(0,0,-1))))
require('initial denominator is twice 1-z modulo sphere', sphere_zero(D.subs(t,0)-2*w))
R = u*u+v*v
Q = (2*u/(1+R), 2*v/(1+R), (R-1)/(1+R))
require('inverse chart has sphere norm', zero(sum(c*c for c in Q)-1))
require('inverse chart avoids north pole identity', zero(1-Q[2]-2/(1+R)))
require('plane chart inverse first coordinate', zero(Q[0]/(1-Q[2])-u))
require('plane chart inverse second coordinate', zero(Q[1]/(1-Q[2])-v))
H_chart = tuple(c.subs({x:Q[0],y:Q[1],z:Q[2]}, simultaneous=True) for c in H)
Q_scaled = tuple(c.subs({u:a*u,v:a*v}, simultaneous=True) for c in Q)
require('direct contraction agrees with stereographic conjugation', all(zero(c-d) for c,d in zip(H_chart,Q_scaled)))
curve = (2*h/(1+h*h), s.Integer(0), (1-h*h)/(1+h*h))
require('accumulation curve has sphere norm', zero(sum(c*c for c in curve)-1))
require('accumulation curve begins at north pole', tuple(c.subs(h,0) for c in curve)==(0,0,1))
require('accumulation distance squared exact identity', zero(sum((c-q)**2 for c,q in zip(curve,(0,0,1)))-4*h*h/(1+h*h)))

vertices = tuple(range(4))
edges = tuple(combinations(vertices,2))
faces = tuple(combinations(vertices,3))
B1 = s.Matrix([[int(v==j)-int(v==i) for i,j in edges] for v in vertices])
# Independently fill each boundary column using the explicit triangle formula.
B2 = s.zeros(6,4)
for col,(i,j,k) in enumerate(faces):
    for edge,coefficient in [((j,k),1),((i,k),-1),((i,j),1)]:
        B2[edges.index(edge),col] = coefficient
c0,c1,c2,c3 = s.symbols('c0:4')
solution = s.linsolve(list(B2*s.Matrix([c0,c1,c2,c3])), (c0,c1,c2,c3))
generator = s.Matrix([-1,1,-1,1])
require('simplicial boundary of boundary is zero', B1*B2==s.zeros(4,4))
require('exact kernel equations have one displayed parameter', solution==s.FiniteSet((-c3,c3,-c3,c3)))
require('degree two boundary matrix has rank three', B2.rank()==3)
require('displayed integral cycle is nonzero and killed', generator!=s.zeros(4,1) and B2*generator==s.zeros(6,1))
require('displayed integral generator is primitive', math.gcd(*map(int,generator))==1)
require('last coordinate gives an integral kernel parameter', generator[3]==1)
require('boundary complex contains no tetrahedral three-simplex', all(len(face)<=3 for face in faces))

# Symbolic class labels test finite equivalence-relation combinatorics only.
labels = (False,True)
E = lambda i,j: i==j
require('equivalence relation reflexive', all(E(i,i) for i in labels))
require('equivalence relation symmetric', all(E(i,j)==E(j,i) for i,j in product(labels,repeat=2)))
require('equivalence relation transitive', all(not(E(i,j) and E(j,k)) or E(i,k) for i,j,k in product(labels,repeat=3)))
subsets = [set(comb) for n in range(3) for comb in combinations(labels,n)]
require('two-point powerset has all four subsets', len(subsets)==4 and len({frozenset(q) for q in subsets})==4)
require('logic candidate topology closed under intersections', all(i&j in subsets for i,j in product(subsets,repeat=2)))
require('logic candidate topology closed under unions', all(i|j in subsets for i,j in product(subsets,repeat=2)))

# Supplemental finite rational witnesses. These do not establish a universal claim.
examples = 0
for U,V,T in product(range(-2,3),range(-2,3),(Fraction(0),Fraction(1,3),Fraction(1))):
    aa = 1-T; rr = aa*aa*(U*U+V*V)
    p = (2*aa*U/(1+rr),2*aa*V/(1+rr),(rr-1)/(1+rr))
    assert sum(q*q for q in p)==1 and p[2]!=1
    examples += 1
require('75 exact rational contraction witnesses', examples==75)

result = {
    'all_passed': all(x['passed'] for x in checks),
    'check_count': len(checks),
    'sympy_version': s.__version__,
    'checks': checks,
    'tetrahedron_boundary_matrix': [[int(c) for c in row] for row in B2.tolist()],
    'integer_kernel_generator': [int(c) for c in generator],
    'integer_kernel_parameter': 'last coefficient, hence an integer on integer chains',
    'degree_three_chain_group_rank': 0,
    'supplemental_exact_rational_witness_count': examples,
    'limits': [
        'Rational identities require nonzero denominators; their strict positivity on the mathematical domains is checked by ordered-field reasoning in REVIEW.md.',
        'Finite class-label tests do not mechanize logic topology, definability, or the infinite sphere.',
        'Model-theoretic saturation, first-order transfer, continuity, and foundational homology theorems are not formalized by this script.',
        'No numerical approximation, large exhaustive search, or formal proof checker is used.'
    ]
}
print(json.dumps(result,indent=2))
