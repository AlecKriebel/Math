#!/usr/bin/env python3
"""Independent exact audit controls. No imports from the author verifier.
These are finite algebraic controls, not a computation of a manifold skein module.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from collections import Counter
import json
C = Counter()
def check(x, group):
    if not x: raise AssertionError(group)
    C[group] += 1
# A different sparse Laurent representation: dict exponent -> rational coefficient.
def clean(p): return {e:Q(c) for e,c in p.items() if c}
def plus(p,q):
    r=dict(p)
    for e,c in q.items(): r[e]=r.get(e,0)+c
    return clean(r)
def scale(p,c): return clean({e:c*v for e,v in p.items()})
def times(p,q):
    r={}
    for e,c in p.items():
        for f,d in q.items(): r[e+f]=r.get(e+f,0)+c*d
    return clean(r)
def mon(e,c=1): return clean({e:c})
def evaluate(p,a): return sum(c*Q(a)**e for e,c in p.items())
def evaluate_mod(p,a,prime):
    return sum((c.numerator*pow(c.denominator,-1,prime)%prime)*pow(a,e,prime)
               for e,c in p.items())%prime
A=mon(1); ONE=mon(0)
# Direct geometric-series certificates, not a cyclotomic-polynomial implementation.
# (A-c)G=A^n-c^n; modulo A^n-1 this supplies a Bezout inverse over Q.
for c in (-5,-3,-2,2,3,5):
    f=plus(A,mon(0,-c))
    for n in range(1,129):
        G={i:Q(c)**(n-1-i) for i in range(n)}
        check(times(f,G)==plus(mon(n),mon(0,-Q(c)**n)), 'geometric_series_identity')
        check(1-Q(c)**n != 0, 'no_root_of_unity_support')
    # All tested Laurent representatives evaluate compatibly in Z[1/c].
    for e in range(-12,13):
        check(evaluate(times(f,mon(e)),c)==0,'localized_integer_evaluation')
# Arithmetic torsion can be invisible in all characteristic-zero fibers.
# R/(p,A-a) = F_p for nonzero a; test Laurent, not just ordinary polynomials.
for prime in (2,3,5,7,11):
    for a in range(1,prime):
        check(evaluate_mod(ONE,a,prime)==1, 'nonzero_arithmetic_residue')
        f=plus(A,mon(0,-a))
        for e in range(-9,10):
            check(evaluate_mod(times(f,mon(e)),a,prime)==0,'laurent_residue_polynomial_relation')
            check(evaluate_mod(mon(e,prime),a,prime)==0,'laurent_residue_integer_relation')
# Nilpotents in a fiber are compatible with a free family:
# rank-two algebra basis 1,x, x^2=A+1. Multiplication closes without denominators.
u=plus(A,ONE)
def algmul(v,w):
    return (plus(times(v[0],w[0]),times(u,times(v[1],w[1]))),
            plus(times(v[0],w[1]),times(v[1],w[0])))
X=({},ONE)
check(algmul(X,X)==(u,{}),'free_deformation_nonreduced_fiber')
check(evaluate(u,-1)==0 and X!=( {},{}),'nonzero_nilpotent_at_minus_one')
# Independent general rectangular determinantal controls over Z.
def matvec(B,x): return [sum(Q(v)*w for v,w in zip(row,x)) for row in B]
def det2(M): return M[0][0]*M[1][1]-M[0][1]*M[1][0]
def adj_apply(M,v):
    a,b=M[0]; c,d=M[1]
    return [d*v[0]-b*v[1],-c*v[0]+a*v[1]]
for aa,bb,cc,dd in product(range(-2,3), repeat=4):
    if aa*dd-bb*cc == 0: continue
    # Three row and column choices, including a redundant third column.
    B=[[aa,bb,aa+bb],[cc,dd,cc+dd],[aa+2*cc,bb+2*dd,aa+bb+2*(cc+dd)]]
    for den in (2,3):
        for num in ((1,0),(0,1),(1,1),(-2,3)):
            v=matvec(B,[Q(num[0],den),Q(num[1],den),0])
            if any(t.denominator!=1 for t in v): continue
            for cols in combinations(range(3),2):
                D=[[row[j] for j in cols] for row in B]
                for rows in combinations(range(3),2):
                    square=[D[i] for i in rows]; delta=det2(square)
                    if not delta: continue
                    coeff=adj_apply(square,[v[i] for i in rows])
                    check(all(t.denominator==1 for t in coeff),'integer_adjugate_coefficients')
                    check(matvec(D,coeff)==[delta*t for t in v], 'all_rectangular_minor_annihilators')
# Explicit polynomial rectangular example with actual integer torsion.
p=plus(A,mon(0,-1))
B=[[mon(0,2),{}],[{},p],[mon(0,2),p]]
v=[ONE,{},ONE]
for rows in combinations(range(3),2):
    a,b=B[rows[0]]; c,d=B[rows[1]]
    delta=plus(times(a,d),scale(times(b,c),-1))
    if not delta: continue
    coeff=[plus(times(d,v[rows[0]]),scale(times(b,v[rows[1]]),-1)),
           plus(scale(times(c,v[rows[0]]),-1),times(a,v[rows[1]]))]
    lhs=[plus(times(row[0],coeff[0]),times(row[1],coeff[1])) for row in B]
    check(lhs==[times(delta,t) for t in v],'polynomial_rectangular_minor_annihilators')
check(evaluate_mod(v[0],1,2)==1 and all(evaluate_mod(t,1,2)==0 for t in B[0])
      and [scale(t,2) for t in v]==[row[0] for row in B],
      'polynomial_example_torsion_is_nonzero')
# Nonunit-minor ideal but torsion-free cokernel R^2/R(A-1,2).
# Multiples of the column map to zero under (x,y) -> 2x-(A-1)y.
for e in range(-20,21):
    t=mon(e)
    x=times(p,t); y=scale(t,2)
    check(plus(scale(x,2),scale(times(p,y),-1))=={},'nonprincipal_ideal_syzygy')
check(evaluate_mod(p,1,2)==0 and evaluate_mod(mon(0,2),1,2)==0,
      'minor_ideal_proper_residue_witness')
# Reduction coefficient is a nonunit even though it is invertible in Q(A).
check(evaluate(plus(A,mon(0,-2)),2)==0 and evaluate(ONE,2)==1,
      'nonmonic_rewrite_cannot_kill_generator_integrally')
print(json.dumps({'status':'PASS','total_assertions':sum(C.values()),
  'assertions_by_group':dict(sorted(C.items())),
  'independence':'Standard library only; no author-verifier imports or execution.',
  'scope':'Finite exact adversarial module and matrix controls; no manifold counterexample.'},
  indent=2,sort_keys=True))
