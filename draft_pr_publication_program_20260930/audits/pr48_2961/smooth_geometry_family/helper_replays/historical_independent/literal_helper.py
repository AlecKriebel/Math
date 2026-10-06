#!/usr/bin/env python3
"""Independent exact free-group, matrix, differential and averaging controls.
Run: python independent_checks.py > independent_results.json
These diagnostics do not prove smooth perfectness or resolve KP-4.85.
"""
from collections import Counter
from itertools import permutations
from fractions import Fraction as Q
import json
import sympy as s

counts=Counter()
def check(ok,name):
    assert bool(ok),name
    counts[name]+=1

# The restricted wreath product of a free group with Z.
# Elements are (finitely supported coordinate dictionary, shift exponent).
# Coordinate words are freely reduced tuples of nonzero signed letters.
def reduced(word):
    out=[]
    for x in word:
        if out and out[-1]==-x: out.pop()
        else: out.append(x)
    return tuple(out)
def inverse_word(w):
    return tuple(-x for x in reversed(w))
def mul(g,h):
    a,n=g; b,k=h
    out=dict(a)
    for j,w in b.items():
        i=j+n
        v=reduced(out.get(i,())+w)
        if v: out[i]=v
        elif i in out: del out[i]
    return out,n+k
def inv(g):
    a,n=g
    return {i-n:inverse_word(w) for i,w in a.items()},-n
def product(seq):
    out=({},0)
    for g in seq: out=mul(out,g)
    return out
def comm(g,h):
    return product([g,h,inv(g),inv(h)])
def base(letter):
    return {0:(letter,)},0
def translate(g,n):
    return {j+n:w for j,w in g[0].items()},g[1]
F=({},1); one=({},0)
for m in range(1,10):
    aa=[base(2*i+1) for i in range(m)]
    bb=[base(2*i+2) for i in range(m)]
    cc=[comm(a,b) for a,b in zip(aa,bb)]
    h=product(cc)
    A=product(translate(a,i+1) for i,a in enumerate(aa))
    B=product(translate(b,i+1) for i,b in enumerate(bb))
    C=product(translate(product(cc[i:]),i) for i in range(m))
    transported=product(translate(c,i+1) for i,c in enumerate(cc))
    check(comm(A,B)==transported,'free_wreath_parallel_commutator')
    check(comm(C,F)==mul(h,inv(transported)),'free_wreath_suffix_identity')
    check(mul(comm(C,F),comm(A,B))==h,'free_wreath_two_commutator_identity')
    check(h!=one,'nontrivial_free_word_control')
    check(mul(comm(F,C),comm(A,B))!=h,'reversed_commutator_negative_control')
    if m>=2:
        check(mul(cc[0],cc[1])!=mul(cc[1],cc[0]),'noncommuting_input_commutators')
        wrong_C=product(translate(product(cc[:i+1]),i) for i in range(m))
        check(mul(comm(wrong_C,F),comm(A,B))!=h,'prefix_instead_of_suffix_negative_control')
    # Adjacent transported subgroups commute independently of their internal words.
    check(comm(translate(aa[0],0),translate(bb[0],m))==one,'different_coordinates_commute')

# A smooth determinant-one family which is not a one-parameter subgroup.
t,u,chi=s.symbols('t u chi',real=True)
def family(t):
    return s.Matrix([[1,t],[t*t,1+t**3]])
M=family(t); f=family(1)
check(s.expand(M.det())==1,'smooth_family_invertibility')
check(family(0)==s.eye(2),'smooth_family_initial_identity')
check(s.simplify(family(t+u)-family(t)*family(u))!=s.zeros(2),
      'non_one_parameter_family_control')
a=family(t*chi); b=family(t)*a.inv()
check(s.simplify(b*a-family(t))==s.zeros(2),'parameter_dependent_factorization')
check(a.subs(chi,0)==s.eye(2),'first_factor_cutoff_zero')
check(s.simplify(b.subs(chi,1))==s.eye(2),'second_factor_cutoff_one')
check(s.simplify(b.subs(t,0))==s.eye(2),'second_factor_isotopy_initial_identity')
check(s.simplify(b.det())==1,'second_factor_invertibility')

# Exact smooth point-dependent-time singularity on the sphere.
x,y,z=s.symbols('x y z',real=True)
tau=(1+2*x*y)/2
mapF=s.Matrix([x*s.cos(tau)-y*s.sin(tau),x*s.sin(tau)+y*s.cos(tau),z])
J=mapF.jacobian([x,y,z]).subs({x:0,y:1,z:0})
v=s.Matrix([-1,0,0]); other=s.Matrix([0,0,1])
check(J*v==s.zeros(3,1),'singular_tangent_direction')
check(J*other==other,'nonzero_other_tangent_direction')
check(s.Matrix.hstack(J*v,J*other).rank()==1,'sphere_tangent_rank_one')
check(tau.subs({x:0,y:1,z:0})==Q(1,2),'cutoff_time_is_interior')
# |2xy| <= x^2+y^2 <= 1 on the unit sphere follows from (x +/- y)^2 >= 0.
check(s.expand((x+y)**2+(x-y)**2)==2*(x*x+y*y),'global_cutoff_range_certificate')

# Direct cocycle pushforward calculations on a finite action.
# c(f,x)=h(f(x))-h(x) is an exact additive cocycle; target defect is zero.
perms=list(permutations(range(3)))
def compose(p,q): return tuple(p[q[i]] for i in range(3))
measures=[(Q(1),Q(0),Q(0)),(Q(1,2),Q(1,3),Q(1,6)),(Q(1,3),)*3]
height=(0,1,100)
nonzero=0
for mu in measures:
    def average(f):
        return sum((mu[i]*(height[f[i]]-height[i]) for i in range(3)),Q(0))
    for f in perms:
        for g in perms:
            defect=average(compose(f,g))-average(f)-average(g)
            push=[Q(0)]*3
            for i in range(3): push[g[i]]+=mu[i]
            extra=sum(((push[i]-mu[i])*(height[f[i]]-height[i]) for i in range(3)),Q(0))
            check(defect==extra,'noninvariant_measure_exact_defect')
            if mu==(Q(1,3),)*3:
                check(defect==0,'invariant_measure_defect_control')
            elif defect: nonzero+=1
check(nonzero>0,'noninvariance_obstruction_is_nonvacuous')

print(json.dumps({
 'status':'PASS','assertions':sum(counts.values()),'checks':dict(counts),
 'sympy_version':s.__version__,'free_group_cases':9,
 'maximum_input_commutators':9,'finite_cocycle_action_pairs':108,
 'nonzero_noninvariant_defects':nonzero,
 'scope':'Exact free-word and symbolic smooth-parameter controls, plus finite cocycle calculations. '
         'The support constructions and imported smooth perfectness theorem require the written audit. '
         'The full four-manifold problem remains unresolved.'
},indent=2))
