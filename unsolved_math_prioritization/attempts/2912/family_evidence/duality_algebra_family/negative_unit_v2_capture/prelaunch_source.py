#!/usr/bin/env python3
"""Own exact arithmetic audit using b^j a^i and t^n a^i normal forms.
No candidate or historical-review source is imported, compiled or executed.
Finite controls accompany the written all-support proof; they do not certify
Poincare-Lefschetz duality, a geometric meridian or homotopy classification.
"""
from itertools import permutations, product
import json, sys
counts={}
def require(p, category):
    if not p: raise AssertionError(category)
    counts[category]=counts.get(category,0)+1

def determinant(rows):
    n=len(rows); total=0
    for p in permutations(range(n)):
        odd=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2
        value=-1 if odd else 1
        for i in range(n): value*=rows[i][p[i]]
        total+=value
    return total

# A uses independently written normal words b^j a^i.
def multiply_A(x,y):
    j,i=x; k,l=y
    return ((j+pow(2,i,7)*k)%7,(i+l)%3)
A=list(product(range(7),range(3)))
unit=(0,0); a=(0,1); b=(1,0)
require(len(set(A))==21,'A_normal_forms')
for x,y,z in product(A,repeat=3):
    require(multiply_A(multiply_A(x,y),z)==multiply_A(x,multiply_A(y,z)),
            'A_associativity')
for x,y in product(A,repeat=2):
    require(multiply_A(x,y) in A,'A_closure')
require(multiply_A(multiply_A(a,a),a)==unit,'A_relations')
p=unit
for unused in range(7): p=multiply_A(p,b)
require(p==unit and b!=unit,'A_relations')
require(multiply_A(multiply_A(a,b),(0,2))==multiply_A(b,b),'A_relations')

# Left A/C cosets b^j C; calculate actions from the group law.
def perm(x): return tuple(multiply_A(x,(j,0))[0] for j in range(7))
for x,y in product(A,repeat=2):
    require(tuple(perm(x)[perm(y)[j]] for j in range(7))==perm(multiply_A(x,y)),
            'A_coset_action')
require(perm(a)==tuple(2*j%7 for j in range(7)),'A_coset_action')
require(perm(b)==tuple((j+1)%7 for j in range(7)),'A_coset_action')

# Choose the representative with coordinate ZERO equal to zero, differing
# from the candidate's final-coordinate convention.
def Q(v): return tuple(v[j]-v[0] for j in range(1,7))
def lift_Q(v): return (0,)+tuple(v)
def action7(p,v):
    out=[0]*7
    for j in range(7): out[p[j]]=v[j]
    return tuple(out)
def q_action(p,v): return Q(action7(p,lift_Q(v)))
E=[tuple(int(i==j) for i in range(6)) for j in range(6)]
def matrix_from_action(p,action):
    columns=[action(p,e) for e in E]
    return [[columns[j][i] for j in range(6)] for i in range(6)]
M_a=matrix_from_action(perm(a),q_action)
M_b=matrix_from_action(perm(b),q_action)
I=[[int(i==j) for j in range(6)] for i in range(6)]
for x,y,e in product(A,A,E):
    require(q_action(perm(x),q_action(perm(y),e))==q_action(perm(multiply_A(x,y)),e),
            'Q_representation')
for v in product((-1,0,1),repeat=7):
    require((Q(v)==(0,)*6)==all(c==v[0] for c in v),'Q_primitive_diagonal')
for mat in (M_a,M_b): require(determinant(mat)==1,'Q_unimodular_action')
D=[[M_b[i][j]-I[i][j] for j in range(6)] for i in range(6)]
require(determinant(D)==7,'Q_b_minus_one_index')
# Cramer's rule exactly confirms all a-1 columns lie in the b-1 lattice.
for column in range(6):
    target=[M_a[i][column]-I[i][column] for i in range(6)]
    solution=[]
    for j in range(6):
        replace=[[target[i] if k==j else D[i][k] for k in range(6)] for i in range(6)]
        numerator=determinant(replace)
        require(numerator%7==0,'Q_coinvariants_C7')
        solution.append(numerator//7)
    require([sum(D[i][j]*solution[j] for j in range(6)) for i in range(6)]==target,
            'Q_coinvariants_C7')
for p in (perm(a),perm(b)):
    for e in E: require(sum(q_action(p,e))%7==sum(e)%7,'Q_coinvariants_C7')

# Independent augmentation lattice I_aug has basis e_j-e_0.
def lift_aug(v): return (-sum(v),)+tuple(v)
def aug_action(p,v): return action7(p,lift_aug(v))[1:]
def cyclic_charge(v): return sum((j+1)*v[j] for j in range(6))%7
for e in E:
    require(cyclic_charge(aug_action(perm(b),e))==cyclic_charge(e),
            'augmentation_coinvariant_control')
require((cyclic_charge(aug_action(perm(a),E[0]))-cyclic_charge(E[0]))%7==1,
        'augmentation_full_coinvariants_zero')

# B uses t^n a^i rather than a^i t^n. T-left-orbits have constant i.
def multiply_B(x,y):
    n,i=x; m,j=y
    return (n+m,((1 if m%2==0 else -1)*i+j)%3)
window=list(product(range(-3,4),range(3)))
for x,y,z in product(window,repeat=3):
    require(multiply_B(multiply_B(x,y),z)==multiply_B(x,multiply_B(y,z)),
            'B_associativity')
for x in window:
    for k in range(-4,5):
        require(multiply_B((k,0),x)[1]==x[1],'B_T_orbit_labels')

# Explicit finite-support ring addition and left action.
def add(p,q,scale=1):
    out=dict(p)
    for key,value in q.items(): out[key]=out.get(key,0)+scale*value
    return {key:value for key,value in out.items() if value}
def left_B(x,v): return {multiply_B(x,key):value for key,value in v.items()}
def norm_at(n): return {(n,i):1 for i in range(3)}
def derive(x,v):
    n,i=x; out={}
    for k in range(0,n) if n>=0 else range(n,0):
        out=add(out,left_B((k,0),v),1 if n>=0 else -1)
    return out
for n in range(-9,10):
    v=norm_at(n)
    require(left_B((0,1),v)==v,'C_norm_invariance')
    require(left_B((1,0),v)==norm_at(n+1),'C_norm_shift')
for v in (norm_at(0), add(norm_at(-2),norm_at(3),-1)):
    for x,y in product(window,repeat=2):
        require(derive(multiply_B(x,y),v)==add(derive(x,v),left_B(x,derive(y,v))),
                'B_explicit_cocycle')

# Every finite Laurent polynomial of total coefficient zero has an exact
# finite primitive for t-1. Prove the recurrence in AUDIT.md; check windows.
for coeff in product((-1,0,1),repeat=7):
    total=sum(coeff)
    v={}
    for n,c in zip(range(-3,4),coeff): v=add(v,norm_at(n),c)
    restricted=tuple(sum(c for (n,j),c in v.items() if j==i) for i in range(3))
    require(restricted==(total,)*3,'B_restriction_diagonal')
    require((restricted==(0,0,0))==(total==0),'B_restriction_injection_control')
    if total==0:
        partial=0; primitive={}
        for n,c in zip(range(-3,4),coeff):
            partial+=c
            primitive=add(primitive,norm_at(n),-partial)
        require(add(left_B((1,0),primitive),primitive,-1)==v,
                'B_finite_primitive_control')
require(Q((1,)*7)==(0,)*6,'negative_control_witnesses')
require(Q((0,1,0,0,0,0,0))==(1,0,0,0,0,0),'negative_control_witnesses')
if len(sys.argv)>1:
    if sys.argv[1]=='diagonal-is-augmentation':
        # Deliberately false: Q need not have representative of sum zero.
        assert sum(Q((0,1,0,0,0,0,0)))==0, 'EXPECTED FAILURE: diagonal quotient is not augmentation'
    elif sys.argv[1]=='t-minus-one-is-unit':
        # Augmentation of any (t-1)u is zero, whereas augmentation(1)=1.
        finite_u={(-3,0):2,(2,1):-5,(4,2):7}
        product_by_t_minus_one=add(left_B((1,0),finite_u),finite_u,-1)
        assert sum(product_by_t_minus_one.values())==1, 'EXPECTED FAILURE: augmentation of (t-1)u is 0, augmentation of 1 is 1'
    else: raise ValueError('Unknown deliberately failing control')
print(json.dumps({'status':'PASS_SCOPED_ARITHMETIC','counts':counts,
 'exact_controls':sum(counts.values()),'alternative_coordinate_zero':0,
 'matrix_a':M_a,'matrix_b':M_b,'det_b_minus_one':determinant(D),
 'Q_A_coinvariants':'Z/7','augmentation_A_coinvariants':'0',
 'restriction_per_regular_B_block':'Z -> Z^3, n -> (n,n,n)',
 'limits':['finite and finite-support arithmetic controls only',
 'written all-support proof is separate','no candidate or historical helper executed',
 'no proof of geometric meridian realization or original target']},indent=2))
