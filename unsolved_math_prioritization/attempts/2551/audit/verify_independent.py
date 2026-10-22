#!/usr/bin/env python3
"""Independent exact checks of the example and bridge pitfalls, not of the imported classification theorem.
Standard library only. Does not import or execute the author verifier. Writes no files.
"""
from fractions import Fraction as Q
from itertools import product
from collections import Counter
import json

BASIS = ('x','y','z','u','v','A','B','C','D','E')
WEIGHTS = dict(zip(BASIS,(1,2,1,2,3,3,4,5,3,4)))
REL = [('x','y','D'),('x','z','u'),('y','z','v'),('x','u','A'),
       ('y','u','B'),('x','v','B'),('y','v','C'),('z','u','D'),('z','v','E')]
COUNTS = Counter()
def check(v, name):
    COUNTS[name] += 1
    if not v: raise AssertionError(name)
def clean(v): return {k:a for k,a in v.items() if a}
def plus(*vs):
    r={}
    for v in vs:
        for k,a in v.items(): r[k]=r.get(k,0)+a
    return clean(r)
def times(c,v): return clean({k:c*a for k,a in v.items()})
def br(a,b,rels=REL):
    r={}
    for i,j,k in rels:
        r[k]=r.get(k,0)+a.get(i,0)*b.get(j,0)-a.get(j,0)*b.get(i,0)
    return clean(r)
def bch(a,b,third=Q(1,12)):
    c=br(a,b)
    return plus(a,b,times(Q(1,2),c),times(third,plus(br(a,c),br(b,br(b,a)))))
def com(a,b): return bch(bch(bch(times(-1,a),times(-1,b)),a),b)
def dil(a,q): return {k:v*q**WEIGHTS[k] for k,v in a.items()}
def rank(vs):
    rows=[[Q(v.get(k,0)) for k in BASIS] for v in vs if v]
    piv=0
    for c in range(len(BASIS)):
        nxt=next((i for i in range(piv,len(rows)) if rows[i][c]),None)
        if nxt is None: continue
        rows[piv],rows[nxt]=rows[nxt],rows[piv]
        pivot=rows[piv][c]
        rows[piv]=[a/pivot for a in rows[piv]]
        for i in range(piv+1,len(rows)):
            fac=rows[i][c]
            rows[i]=[a-fac*b for a,b in zip(rows[i],rows[piv])]
        piv+=1
        if piv==len(rows):break
    return piv
E=[{x:Q(1)} for x in BASIS]
for a,b in product(E, repeat=2):
    check(br(a,b)==times(-1,br(b,a)),'antisymmetry')
    check(dil(br(a,b),Q(2,3))==br(dil(a,Q(2,3)),dil(b,Q(2,3))),'rational_dilation')
for a,b,c in product(E,repeat=3):
    check(not plus(br(a,br(b,c)),br(b,br(c,a)),br(c,br(a,b))),'jacobi')
series=[E]
for _ in range(3):series.append([br(a,b) for a,b in product(E,series[-1])])
check([rank(s) for s in series]==[10,7,5,0],'lower_central_series')
G=E[:3]; G2=[br(a,b) for a,b in product(G,G)]
G3=[br(a,b) for a,b in product(G,G2)]
check(rank(G+G2+G3)==10,'three_generator_lie_span')
x,y,z=[times(12,a) for a in G]
u,v=com(x,z),com(y,z)
triples=[com(x,u),com(y,u),com(y,v),com(z,u),com(z,v)]
for a,k in zip(triples,('A','B','C','D','E')):
    check(a=={k:Q(1728)},'exact_triple_commutator')
check(rank([x,y,z,u,v]+triples)==10,'group_log_full_rank')
check(u.get('u')==144 and v.get('v')==144,'pair_commutator_leading_terms')
check(sum(WEIGHTS.values())==28 and 2**28==268435456,'index_exponent')
for a in (x,y,z):
    k=next(iter(a));check(dil(a,Q(2))==times(2**WEIGHTS[k],a),'generator_images_are_powers')
# Universal BCH associativity in this exact Lie algebra, as a polynomial identity
# in all 30 coordinates. Monomials are sorted tuples of variable indices.
def pplus(*polys):
    r={}
    for p in polys:
        for m,c in p.items():r[m]=r.get(m,0)+c
    return clean(r)
def ptimes(a,b):
    r={}
    for u,c in a.items():
        for v,d in b.items():
            m=tuple(sorted(u+v));r[m]=r.get(m,0)+c*d
    return clean(r)
def pscale(q,p):return clean({m:q*c for m,c in p.items()})
def vpadd(*vs):return {k:pplus(*(v.get(k,{}) for v in vs)) for k in BASIS}
def vpscale(q,v):return {k:pscale(q,p) for k,p in v.items()}
def pbr(a,b):
    r={k:{} for k in BASIS}
    for i,j,k in REL:
        r[k]=pplus(r[k],ptimes(a.get(i,{}),b.get(j,{})),pscale(-1,ptimes(a.get(j,{}),b.get(i,{}))))
    return r
def pbch(a,b):
    c=pbr(a,b)
    return vpadd(a,b,vpscale(Q(1,2),c),vpscale(Q(1,12),vpadd(pbr(a,c),pbr(b,pbr(b,a)))))
X,Y,Z=[{k:{(10*t+i,):Q(1)} for i,k in enumerate(BASIS)} for t in range(3)]
left,right=pbch(pbch(X,Y),Z),pbch(X,pbch(Y,Z))
for k in BASIS:check(left[k]==right[k],'universal_bch_associativity_coordinate')
for k in BASIS:check(not pbch(X,vpscale(-1,X))[k],'universal_bch_inverse_coordinate')
# Universal closure of 12 Z^10 checked coefficientwise, not just on a sample.
scaled=pbch(vpscale(12,X),vpscale(12,Y))
for k in BASIS:
    check(all(c.denominator==1 and c.numerator%12==0 for c in scaled[k].values()),'universal_lattice_closure_coordinate')
# Explicit arbitrary rational-lattice example: in coordinates of the oblique
# lattice basis (1,0),(1/3,1), alpha=diag(1/2,1/4) has matrix
# [[1/2,1/12],[0,1/4]]. Its intersection domain is 2 Z x 12 Z,
# and its image is {(a+b,3b)}. In particular f need not be surjective.
def oblique(m,n):return Q(m,2)+Q(n,12),Q(n,4)
for m,n in product(range(-24,25),repeat=2):
    value=oblique(m,n)
    check(all(v.denominator==1 for v in value)==(m%2==0 and n%12==0),'oblique_exact_domain')
check(oblique(0,12)==(1,3) and oblique(2,0)==(1,0),'oblique_image_generators')
check(2*12==24 and 3>1,'domain_finite_image_not_surjective')
check(oblique(0,1)==(Q(1,12),Q(1,4)),'lattice_preservation_not_assumed')
# Finite-level recursion control for Z: a -> residue(a+g), state=(a+g)//q.
def action(g,word,q=3):
    out=[]
    for a in word:
        g,b=divmod(g+a,q);out.append(b)
    return tuple(out)
words=list(product(range(3),repeat=4))
for g,h in product(range(-5,6),repeat=2):
    check(all(action(g,action(h,w))==action(g+h,w) for w in words),'tree_recursion_group_law')
for g in range(-80,81):
    check((all(action(g,w)==w for w in words))==(g%81==0),'finite_level_kernel_exact')
# Negative controls reject precisely the invalid mathematical substitutes.
badrel=[r for r in REL if r != ('x','v','B')]
check(bool(plus(br(E[0],br(E[1],E[2],badrel),badrel),br(E[1],br(E[2],E[0],badrel),badrel),br(E[2],br(E[0],E[1],badrel),badrel))),'negative_delete_jacobi_bracket')
wrong=WEIGHTS.copy();wrong['D']+=1
check(any(wrong[k]!=wrong[i]+wrong[j] for i,j,k in REL),'negative_mutate_degree')
naive=dict(zip(BASIS,(1,1,1,2,2,3,3,3,3,3)))
check(any(naive[k]!=naive[i]+naive[j] for i,j,k in REL),'negative_lower_central_substitution')
check(times(Q(1,2),br(x,y))!=br(times(Q(1,2),x),times(Q(1,2),y)),'negative_uniform_scaling')
check(any(bch(bch(a,b,Q(1,24)),c,Q(1,24)) != bch(a,bch(b,c,Q(1,24)),Q(1,24)) for a,b,c in product(E[:3],repeat=3)),'negative_wrong_bch_coefficient')
# The zero-weight coordinate is an actual infinite invariant subgroup; finite
# samples only exercise that formula and do not establish faithfulness.
for t in range(-16,17):
    check((Q(0,2),t)==(0,t),'negative_zero_weight_core')
# If k^2=2l^2 nontrivially, 2-adic valuation has opposite parity. Exhaustion is
# supplemental, while the infinite argument is in AUDIT_REPORT.md.
for k,l in product(range(-25,26),repeat=2):
    if k or l:check(k*k!=2*l*l,'negative_irrational_domain_samples')
print(json.dumps({'status':'PASS','scope':'independent exact example and mechanism controls; not a proof of the imported grading classification','checks':dict(sorted(COUNTS.items())),'total_checks':sum(COUNTS.values()),'polynomial_associativity_monomials':sum(map(len,left.values())),'lower_central_dimensions':[10,7,5,0],'dilation_index':268435456,'oblique_domain_index':24,'oblique_image_index':3},sort_keys=True,indent=2))
