#!/usr/bin/env python3
"""Exact algebra diagnostics for the partial surface-isotopy package.
This does not implement the imported PL/JSJ or free-group decision algorithms.
"""
from pathlib import Path
from itertools import permutations, product
import hashlib, json
import sympy as s

counts={}
def check(name, condition):
    assert condition, name
    counts[name]=counts.get(name,0)+1

def comp(a,b): return tuple(a[b[i]] for i in range(len(a)))
def inv(a): return tuple(a.index(i) for i in range(len(a)))
G=list(permutations(range(3)));e=tuple(range(3))
def generated(gens):
    seen={e};todo=[e]
    while todo:
        u=todo.pop()
        for g in gens:
            v=comp(u,g)
            if v not in seen: seen.add(v);todo.append(v)
    return frozenset(seen)
subs={generated(())}
for a,b in product(G,repeat=2):subs.add(generated((a,b)))
check('all_S3_subgroups',len(subs)==6)
for A,B in product(subs,repeat=2):
    AB={comp(x,y) for x in A for y in B}
    for a,b in product(G,repeat=2):
        c=comp(a,inv(b))
        intersects=bool({comp(x,a) for x in A}&{comp(y,b) for y in B})
        extends=any(comp(x,c) in B for x in A)
        check('boundary_coset_conventions',intersects==extends==(c in AB))
        # Changing initial side maps changes c by left A and right B factors.
        x=sorted(A)[-1];y=sorted(B)[-1]
        new_c=comp(comp(x,c),inv(y))
        check('reference_map_independence',(new_c in AB)==(c in AB))

# Trefoil's braid presentation maps onto the nonabelian group S3.
x=(1,0,2);y=(0,2,1)
check('trefoil_relation',comp(comp(x,y),x)==comp(comp(y,x),y))
check('trefoil_nonabelian',comp(x,y)!=comp(y,x))
check('trefoil_surjection',generated((x,y))==frozenset(G))

P=s.Matrix([[1,1],[0,1]]);Q=s.Matrix([[1,0],[-1,1]])
m,n=s.symbols('m n',integer=True)
Pm=s.Matrix([[1,m],[0,1]]);Qn=s.Matrix([[1,0],[-n,1]])
formula=s.Matrix([[1-m*n,m],[-n,1]])
check('universal_ordered_power_formula',Pm*Qn==formula)
R=P*Q*P.inv()
check('conjugate_matrix',R==s.Matrix([[0,1],[-1,2]]))
check('universal_obstruction_entry',R[1,1]!=formula[1,1])
check('twists_noncommute',P*Q!=Q*P)
J=s.Matrix([[0,1],[-1,0]])
for a,b in product(range(-5,6),repeat=2):
    check('signed_power_formula',P**a*Q**b==formula.subs({m:a,n:b}))
    check('not_two_power_product',R!=P**a*Q**b)
    check('symplectic_twist',((P**a*Q**b).T*J*(P**a*Q**b))==J)
pairedP=s.diag(P,P.inv());pairedQ=s.diag(Q,Q.inv())
J4=s.diag(J,J)
check('paired_twists_symplectic',pairedP.T*J4*pairedP==J4 and pairedQ.T*J4*pairedQ==J4)
check('paired_twists_noncommute',pairedP*pairedQ!=pairedQ*pairedP)
check('paired_conjugate_first_block',(pairedP*pairedQ*pairedP.inv())[:2,:2]==R)
# Disjoint-curve multitwists do permit exponent vectors. These independent-block
# transvections are algebraic controls, not a reconstruction of a JSJ surface.
for a,b,c,d in product(range(-2,3),repeat=4):
    U=s.diag(P**a,P**b);V=s.diag(P**c,P**d)
    check('commuting_multitwist_addition',U*V==s.diag(P**(a+c),P**(b+d)))
    check('orientation_reversal_exponents',U.inv()==s.diag(P**(-a),P**(-b)))

# Word-nullity must not be replaced by an abelianized exponent-sum test.
def reduce_word(w):
    st=[]
    for t in w:
        if st and st[-1]==-t:st.pop()
        else:st.append(t)
    return tuple(st)
commutator=(1,2,-1,-2)
check('homology_is_insufficient',reduce_word(commutator)!=() and
      sum(1 if t==1 else -1 if t==-1 else 0 for t in commutator)==0 and
      sum(1 if t==2 else -1 if t==-2 else 0 for t in commutator)==0)
for k in range(-10,11):
    word=(1,)*k if k>=0 else (-1,)*(-k)
    opposite=tuple(-t for t in reversed(word))
    check('free_word_signed_inverse',reduce_word(word+opposite)==())

p=Path(__file__).parent
result={'problem_id':2830,'status':'PASS_FINITE_ALGEBRA_DIAGNOSTICS','assertions':sum(counts.values()),'groups':counts,
        'artifact_sha256':hashlib.sha256((p/'PARTIAL_RESULT.md').read_bytes()).hexdigest(),
        'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'Exact coset formulas, trefoil finite quotient and matrix/word diagnostics only; no implemented surface-isotopy, JSJ or imported general free-group algorithm.'}
print(json.dumps(result,indent=2,sort_keys=True))
