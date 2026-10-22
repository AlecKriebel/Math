#!/usr/bin/env python3
"""Independent length-eight controls: canonical recursion and border commutators.
Does not import, execute, or reuse the author's verifier or saved answers.
Python standard library only. No source or dataset contents are emitted.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from math import comb
import json


def step(a, i, delta=1):
    return a[:i] + (a[i]+delta,) + a[i+1:]


def canonical_lower_sets(n, target=8):
    """Every lower set has one path: insert its elements in lexicographic order."""
    counts = [1] + [0]*target
    final = []
    def grow(D, border):
        size=len(D)
        counts[size]+=1
        if size == target:
            final.append(frozenset(D)); return
        last=max(D)
        eligible=[]
        for a in border:
            if a > last and all(step(a,i,-1) in D for i in range(n) if a[i]):
                eligible.append(a)
        for a in sorted(eligible):
            E = D | {a}
            new_border = (border | {step(a,i) for i in range(n)}) - E
            grow(E,new_border)
    if target:
        z=(0,)*n
        grow({z},{step(z,i) for i in range(n)})
    assert len(final)==len(set(final))
    return final,counts


def rational_rank(rows):
    piv={}
    for original in rows:
        row={c:Fraction(v) for c,v in original.items() if v}
        while row:
            c=min(row)
            if c not in piv:
                lead=row[c]; piv[c]={j:v/lead for j,v in row.items()}; break
            v=row[c]
            for j,x in piv[c].items():
                row[j]=row.get(j,Fraction(0))-v*x
                if not row[j]: del row[j]
    return len(piv)


def border_tangent(D,n):
    """Linearize all multiplication-matrix commutators in the border basis chart."""
    B=sorted(D); idx={a:i for i,a in enumerate(B)}; d=len(B)
    border=sorted({step(a,i) for a in B for i in range(n)} - set(B))
    bidx={a:i for i,a in enumerate(border)}
    # A variable c[border monomial, basis monomial] changes the corresponding
    # multiplication column in every occurrence of that border monomial.
    constant={}; perturb={}
    for i in range(n):
        for col,a in enumerate(B):
            out=step(a,i)
            if out in idx: constant[i,col]=idx[out]
            else: perturb[i,col]=bidx[out]
    rows=[]
    for i,j in combinations(range(n),2):
        for col in range(d):
            block=[Counter() for _ in range(d)]
            # M_i^0 delta M_j - M_j^0 delta M_i
            for left,right,sign in [(i,j,1),(j,i,-1)]:
                beta=perturb.get((right,col))
                if beta is not None:
                    for k in range(d):
                        out=constant.get((left,k))
                        if out is not None: block[out][beta*d+k]+=sign
            # delta M_i M_j^0 - delta M_j M_i^0
            for left,right,sign in [(i,j,1),(j,i,-1)]:
                mid=constant.get((right,col))
                beta=perturb.get((left,mid)) if mid is not None else None
                if beta is not None:
                    for k in range(d): block[k][beta*d+k]+=sign
            rows.extend(dict(r) for r in block if any(r.values()))
    rank=rational_rank(rows); unknowns=d*len(border)
    return {'border_monomials':len(border),'unknowns':unknowns,'rank_Q':rank,'tangent_dimension_Q':unknowns-rank}


def audit_flat(e,Q):
    used=set(sum((list(a) for a in Q),[]))
    core=sorted(used | set([i for i in range(e) if i not in used][:4-len(used)]))
    assert len(core)==4
    extra=sorted(set(range(e))-set(core))
    selected=[a for a in combinations_with_replacement(core,2) if a not in Q][:e-4]
    basis_quadratics={a:1+e+j for j,a in enumerate(Q)}
    promotions={a:1+w for a,w in zip(selected,extra)}
    def multiply_basis(a,b):
        if a==0:return {(b,0):1}
        if b==0:return {(a,0):1}
        pair=tuple(sorted((a-1,b-1)))
        if pair in basis_quadratics:return {(basis_quadratics[pair],0):1}
        if pair in promotions:return {(promotions[pair],1):1}
        return {}
    def multiply(A,B):
        out=Counter()
        for (a,p),x in A.items():
            for (b,q),y in B.items():
                for (c,r),z in multiply_basis(a,b).items():out[c,p+q+r]+=x*y*z
        return {a:v for a,v in out.items() if v}
    basis=[{(a,0):1} for a in range(8)]
    for a,b,c in product(basis,repeat=3):
        assert multiply(multiply(a,b),c)==multiply(a,multiply(b,c))
    # At parameter zero the complete 8x8 product table equals the monomial
    # quotient, not just its rank or its Hilbert function.
    zeros=(0,)*e
    labels=[zeros]+[step(zeros,i) for i in range(e)]
    labels += [step(step(zeros,a),b) for a,b in Q]
    inv={v:i for i,v in enumerate(labels)}
    for a,b in product(range(8),repeat=2):
        exponent=tuple(x+y for x,y in zip(labels[a],labels[b]))
        expected={} if exponent not in inv else {inv[exponent]:1}
        observed={c:v for (c,t),v in multiply_basis(a,b).items() if t==0}
        assert expected==observed
    outputs=[next(iter(multiply_basis(a,b)))[0] for a,b in combinations_with_replacement(range(1,8),2) if multiply_basis(a,b)]
    assert len(set(outputs))==3
    assert set(outputs)==set(basis_quadratics.values())|set(promotions.values())
    assert len(set(basis_quadratics.values()))==7-e
    # The only coefficients are 1 or t, so these ranks hold in every field.
    assert set(basis_quadratics)==set(Q)
    return True


def homogeneous_exponents(n,d):
    if n==1:
        yield (d,);return
    for i in range(d+1):
        for rest in homogeneous_exponents(n-1,d-i):yield (i,)+rest


def projective_hilbert_series():
    # Independently use inclusion-exclusion over all subsets of generators.
    G=[(0,1,0,1),(0,0,1,1),(2,1,0,0),(2,0,1,0)]
    numerator=Counter({0:1})
    for mask in range(1,1<<len(G)):
        selected=[G[i] for i in range(len(G)) if mask>>i&1]
        lcm=tuple(max(v[i] for v in selected) for i in range(4))
        numerator[sum(lcm)]+=(-1)**len(selected)
    numerator={k:v for k,v in sorted(numerator.items()) if v}
    values={}
    for d in range(33):
        h=sum(v*comb(d-k+3,3) for k,v in numerator.items() if d>=k)
        brute=sum(not any(all(a>=b for a,b in zip(m,g)) for g in G) for m in homogeneous_exponents(4,d))
        assert h==brute
        if d>=1:assert h==3*d+2 if d>=2 else h==4
        values[d]=h
    # Hilbert series (1+2z+z^2-z^3)/(1-z)^2 has polynomial 3d+2.
    alternate=Counter()
    for i,a in enumerate([1,2,1,-1]):
        for j,b in enumerate([1,-2,1]):alternate[i+j]+=a*b
    assert {i:v for i,v in alternate.items() if v}==numerator
    return {'hilbert_numerator_over_one_minus_z_power_4':numerator,'hilbert_values_degrees_0_to_32':values,'polynomial':'3d+2 for all d>=2'}


def main():
    enumeration=[]
    for n in range(1,8):
        sets,counts=canonical_lower_sets(n)
        hist=Counter()
        for D in sets:
            e=sum(sum(a)==1 for a in D)
            if max(map(sum,D))<=2 and e>=4:hist[e]+=1
        expected={e:comb(n,e)*comb(e*(e+1)//2,7-e) for e in range(4,min(n,7)+1)}
        assert dict(hist)==expected
        enumeration.append({'n':n,'counts_d0_to_d8':counts,'signature_by_embedding_dimension':dict(sorted(hist.items())),'signature_total':sum(hist.values())})
    flat_counts={}
    for e in range(4,8):
        flat_counts[e]=0
        for Q in combinations(list(combinations_with_replacement(range(e),2)),7-e):
            assert audit_flat(e,Q);flat_counts[e]+=1
    collision=frozenset([(0,0,0,0),(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,0),(0,1,0,1),(0,0,1,1)])
    collision_result=border_tangent(collision,4)
    anchor_result=border_tangent({(i,0,0,0) for i in range(8)},4)
    assert collision_result['tangent_dimension_Q']==33
    assert anchor_result['tangent_dimension_Q']==32
    z=(0,)*4;core={z}|{step(z,i) for i in range(4)}
    quadrics=[step(step(z,i),j) for i,j in combinations_with_replacement(range(4),2)]
    tangent_hist=Counter()
    for Q in combinations(quadrics,3):
        result=border_tangent(core|set(Q),4)
        tangent_hist[result['tangent_dimension_Q']]+=1
    out={'status':'PASS','method':'canonical lex insertion; independent border-commutator linearization; integer polynomial multiplication; Hilbert-series inclusion-exclusion','enumeration':enumeration,'flat_models_by_embedding_dimension':flat_counts,'flat_models_total':sum(flat_counts.values()),'associativity_checks_per_model':512,'complete_special_fiber_product_checks_per_model':64,'collision_border_tangent':collision_result,'anchor_border_tangent':anchor_result,'h143_tangent_histogram_Q':dict(sorted(tangent_hist.items())),'projective_hilbert_series':projective_hilbert_series(),'limitations':['Finite controls do not prove the universal geometric incidence or imported component classification.','Tangent ranks are over the rationals.']}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
