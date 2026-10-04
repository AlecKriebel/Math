#!/usr/bin/env python3
"""Exact controls for review of KP-2.17; not a test of all current length functions.

Run: python independent_checks.py > independent_results.json
Python standard library plus SymPy are used. All checks are exact.
"""
from collections import Counter, deque
from itertools import product
import json
import sympy as sp

counts = Counter()
def check(condition, category):
    assert bool(condition), category
    counts[category] += 1

I = (1, 0, 0, 1)
S = (0, -1, 1, 0)
T = (1, 1, 0, 1)
A = (1, 2, 0, 1)
B = (1, 0, 2, 1)
def mul(x,y):
    a,b,c,d=x; e,f,g,h=y
    return (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)
def inv(x):
    a,b,c,d=x
    return (d,-b,-c,a)
def det(x):
    a,b,c,d=x
    return a*d-b*c
def tr(x):
    return x[0]+x[3]
def mod2(x):
    return tuple(z%2 for z in x)
def power(x,k):
    out=I
    for _ in range(k): out=mul(out,x)
    return out
def cycles(permutation):
    remaining=set(permutation)
    result=[]
    while remaining:
        start=min(remaining); c=[]; at=start
        while at not in c:
            c.append(at); remaining.remove(at); at=permutation[at]
        check(at==start, 'permutation_cycles_close')
        result.append(c)
    return result

# Independently construct SL(2,F_2), rather than assuming Gamma(2)'s index.
group={mod2(I)}; queue=deque(group)
while queue:
    x=queue.popleft()
    for y in [S,T]:
        z=mod2(mul(x,y))
        if z not in group:
            group.add(z); queue.append(z)
all_sl2={x for x in product(range(2),repeat=4) if det(x)%2==1}
check(group==all_sl2, 'mod_two_quotient_generated')
check(len(group)==6, 'principal_level_two_index')
for x in group:
    check(mod2(mul(x,inv(x)))==I, 'mod_two_group_inverses')
perms=[]
for generator in [S,mul(S,T),T]:
    perm={x:mod2(mul(x,generator)) for x in group}
    check(set(perm.values())==group, 'regular_coset_permutations')
    perms.append(cycles(perm))
check(sorted(map(len,perms[0]))==[2,2,2], 'no_order_two_elliptic_fixed_cosets')
check(sorted(map(len,perms[1]))==[3,3], 'no_order_three_elliptic_fixed_cosets')
check(sorted(map(len,perms[2]))==[2,2,2], 'three_cusps_width_two')
index=len(group); cusps=len(perms[2])
orbifold_area_over_pi=sp.Rational(index,3)
genus=(orbifold_area_over_pi/2 + 2 - cusps)/2
check(orbifold_area_over_pi==2 and genus==0, 'thrice_punctured_sphere_signature')
check(6*genus-6+2*cusps==0, 'finite_area_teichmuller_dimension_only')
check(6*genus-6+3*cusps==3, 'variable_geodesic_boundary_dimension_control')

# Matrices belonging to Gamma(2), with the three different cusp fixed points.
C=mul(A,inv(B)); H=mul(A,B)
for x in [A,B,C,H]:
    check(det(x)==1, 'exact_determinants')
    check(mod2(x)==I, 'exact_level_two_membership')
check(tr(A)==2 and tr(B)==2 and tr(C)==-2, 'parabolic_cusp_traces')
for matrix,point in [(A,(1,0)),(B,(0,1)),(C,(1,1))]:
    a,b,c,d=matrix; p,q=point
    check((a*p+b*q)*q-(c*p+d*q)*p==0, 'projective_cusp_fixed_points')
check(len({(1,0),(0,1),(1,1)})==3, 'distinct_mod_two_cusp_classes')
check(H==(5,2,2,1) and tr(H)==6, 'closed_geodesic_matrix')
z=sp.symbols('z')
check(z*z-tr(H)*z+det(H)==z*z-6*z+1, 'closed_geodesic_characteristic_polynomial')
lam=3+2*sp.sqrt(2)
check(sp.expand(lam**2-6*lam+1)==0, 'exact_expanding_eigenvalue')
check(lam>1 and sp.simplify(lam*(3-2*sp.sqrt(2)))==1, 'positive_hyperbolic_translation_length')
trace_sequence=[tr(power(H,k)) for k in range(10)]
for k in range(2,10):
    check(trace_sequence[k]==6*trace_sequence[k-1]-trace_sequence[k-2], 'closed_word_powers_recurrence')
    check(trace_sequence[k]>trace_sequence[k-1]>2, 'closed_word_powers_hyperbolic')

# Universal polynomial control in eight unconstrained matrix entries.
# This differs from testing a generic diagonal SL2 pair.
entries=sp.symbols('a b c d e f g h')
M=sp.Matrix(2,2,entries[:4]); N=sp.Matrix(2,2,entries[4:])
word='aababb'; reverse=word[::-1]
def evaluate(w,first,second):
    out=sp.eye(2)
    for letter in w:
        out=out*{'a':first,'b':second}[letter]
    return out
difference=sp.expand(sp.trace(evaluate(word,M,N))-sp.trace(evaluate(reverse,M,N)))
check(difference==0, 'universal_two_matrix_trace_reversal_polynomial')
def rotations(w):
    return {w[k:]+w[:k] for k in range(len(w))}
inverse=''.join(c.swapcase() for c in word[::-1])
check(reverse not in rotations(word), 'distinct_free_conjugacy_classes')
check(reverse not in rotations(inverse), 'distinct_unoriented_free_conjugacy_classes')
for w in [word,reverse]:
    for period in [1,2,3]:
        check(w != w[:period]*(len(w)//period), 'primitive_free_words')
# Demonstrate that reversal cannot just be substituted with an arbitrary word.
other='aaabbb'
check(sp.expand(sp.trace(evaluate(word,M,N))-sp.trace(evaluate(other,M,N)))!=0,
      'nonidentity_trace_negative_control')

# The finite angle factor in the local Liouville self-intersection integral.
theta,phi=sp.symbols('theta phi',real=True)
angle_factor=2*sp.integrate(sp.integrate(sp.sin(theta-phi)**2,(phi,0,theta)),(theta,0,sp.pi))
check(sp.simplify(angle_factor-2*sp.pi)==0, 'positive_finite_liouville_angle_factor')
# Gauss--Bonnet and oriented unit tangent volume; no arbitrary normalization fixed.
chi=2-2*genus-cusps
check(chi==-1, 'surface_euler_characteristic')
check(-2*sp.pi*chi==2*sp.pi, 'finite_area_gauss_bonnet')
check(2*sp.pi*(-2*sp.pi*chi)==4*sp.pi**2, 'oriented_unit_tangent_liouville_volume')

print(json.dumps({
    'status':'PASS',
    'sympy_version':sp.__version__,
    'assertions':sum(counts.values()),
    'checks':dict(counts),
    'mod_two_quotient_order':len(group),
    'cusp_widths':sorted(map(len,perms[2])),
    'closed_word_matrix':list(H),
    'closed_word_trace':tr(H),
    'trace_control_words':[word,reverse],
    'scope':'Finite exact quotient, matrix, word, polynomial and normalization controls. '
            'They do not prove compactness, relative filling, the current/flow correspondence, '
            'or equality against all hyperbolic metrics. Those are audited in REVIEW.md.'
},indent=2))
