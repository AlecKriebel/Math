#!/usr/bin/env python3
"""Portable exact checks for the five attempts. No numerical optimizer or network.
The general results are proved in the markdown; bounded tests are sanity checks.
Run: python3 verify_claims.py
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from random import Random


def normal(H):
    return {tuple(sorted(e)): c for e, c in H.items()}


def analyze(n, r, H):
    H = normal(H)
    assert all(len(set(e)) == r - 1 and set(e) <= set(range(n)) and c in (1,2,3)
               for e,c in H.items())
    good = {}
    for S in combinations(range(n), r):
        faces = [e for e in combinations(S,r-1) if e in H]
        cc = Counter(H[e] for e in faces)
        if all(cc[c] for c in (1,2,3)):
            good[S] = (faces, tuple(cc[c] for c in (1,2,3)))
    counts = tuple(list(H.values()).count(c) for c in (1,2,3))
    return counts, good


def shadow(F):
    return {p for e in F for p in combinations(e,len(e)-1)}


def check_complement(n,r,H,good):
    V = set(range(n))
    families = [[tuple(sorted(V-set(e))) for e,c in H.items() if c == color]
                for color in (1,2,3)]
    common = set.intersection(*(shadow(F) for F in families))
    expected = {tuple(sorted(V-set(S))) for S in good}
    assert common == expected


def shift(H,i,j):
    result = {}
    for e,c in H.items():
        target = tuple(sorted((set(e)-{j})|{i})) if j in e and i not in e else e
        target = target if target not in H else e
        assert target not in result
        result[target] = c
    assert Counter(H.values()) == Counter(result.values())
    return result


def cone(q,r):
    # Four classes of q vertices plus a fixed (r-3)-core.
    colors = {(0,1):1,(2,3):1,(0,2):2,(1,3):2,(0,3):3,(1,2):3}
    core = tuple(range(4*q,4*q+r-3))
    H = {}
    for (i,j),c in colors.items():
        for u in range(i*q,(i+1)*q):
            for v in range(j*q,(j+1)*q):
                H[tuple(sorted(core+(u,v)))] = c
    return 4*q+r-3, H


def main():
    report = {'arithmetic':'exact integers and fractions', 'limitations':
              'Bounded examples are sanity checks; the written proofs carry the general claims.'}
    cone_tests = 0
    for q in (1,2,3):
        for r in range(3,8):
            n,H = cone(q,r)
            counts,good = analyze(n,r,H)
            assert counts == (2*q*q,)*3 and len(good) == 4*q**3
            assert len(good)**2 == 2*counts[0]*counts[1]*counts[2]
            cone_tests += 1
    report['sharp_cones'] = cone_tests

    H = {tuple(map(int,e)):c for c,edges in [(1,['012','013','014','023','123','234']),
              (2,['024','134']),(3,['034','124'])] for e in edges}
    counts,good = analyze(5,4,H)
    assert counts == (6,2,2) and set(good) == {(0,1,2,4),(0,1,3,4),(0,2,3,4),(1,2,3,4)}
    links=[]
    for v in range(5):
        link={tuple(x for x in e if x!=v):c for e,c in H.items() if v in e}
        lc,lg=analyze(5,3,link)
        links.append({'core':v,'counts':lc,'rainbow_triangles':len(lg)})
    assert [x['counts'] for x in links] == [(4,1,1)]*4+[(2,2,2)]
    assert [x['rainbow_triangles'] for x in links] == [1,1,1,1,4]
    assert sum(x['rainbow_triangles'] for x in links) == sum(a*b*c for _,(a,b,c) in good.values()) == 8
    reds=[e for e,c in H.items() if c==1]
    degrees=[sum(e in faces for faces,cc in good.values()) for e in reds]
    assert degrees == [1,1,2,1,1,2]
    assert sum(d*d for d in degrees)==12>2*counts[1]*counts[2]
    loads={e:Fraction(0) for e in reds}
    shared={(0,1,4),(2,3,4)}
    for faces,cc in good.values():
        options=[e for e in faces if H[e]==1]
        total=Fraction(0)
        for e in options:
            p=Fraction(1,3) if e in shared else Fraction(2,3)
            loads[e]+=p;total+=p
        assert total==1
    assert set(loads.values())=={Fraction(2,3)}
    energy=sum(x*x for x in loads.values())
    assert energy==Fraction(8,3)==Fraction(len(good)**2,len(reds))
    # All 729 nonnegative integer weight vectors in {0,1,2}^6 obey the certified dual bound.
    for y in product(range(3),repeat=6):
        weights=dict(zip(reds,y))
        A=sum(min(weights[e] for e in faces if H[e]==1) for faces,cc in good.values())
        B=sum(t*t for t in y)
        assert 2*A-B<=energy
    report['five_vertex_obstruction']={'counts':counts,'T':len(good),'links':links,
       'raw_red_square_sum':12,'optimal_fractional_energy':str(energy),'dual_weight_tests':729}

    shift_tests=0
    for r in range(3,9):
        A=tuple(range(4,4+r-3))
        before={tuple(sorted(A+e)):c for e,c in { (0,2):1,(1,3):1,(1,2):2,(2,3):3}.items()}
        after=shift(before,0,1)
        bc,bg=analyze(r+1,r,before);ac,ag=analyze(r+1,r,after)
        assert bc==ac==(2,1,1) and len(bg)==1 and len(ag)==0
        shift_tests+=1
    report['compression_counterexamples']=shift_tests

    # A sharp instance of the two-three-triple lemma, from deleting one block on each side of a Pasch trade.
    F={(0,1,2),(0,3,4),(1,3,5)}
    G={(0,1,3),(0,2,4),(1,2,5)}
    assert not F&G and len(shadow(F)&shadow(G))==7
    full_F=F|{(2,4,5)};full_G=G|{(3,4,5)}
    P=shadow(full_F)
    assert not full_F&full_G and P==shadow(full_G) and len(P)==12
    triangles={e for e in combinations(range(6),3) if set(combinations(e,2))<=P}
    assert len(triangles)==8 and triangles==full_F|full_G
    report['small_trade_witnesses']={'three_triples_common_pairs':7,'pasch_pairs':12,'available_triangles':8}

    # Modest complete check: disjoint pairs of three-triple families on five vertices only.
    triples=list(combinations(range(5),3))
    families=[(frozenset(F),shadow(F)) for F in combinations(triples,3)]
    checks=0;mx=0
    for i,(F,SF) in enumerate(families):
        for G,SG in families[i+1:]:
            if F&G:continue
            common=len(SF&SG);assert common<=7
            mx=max(mx,common);checks+=1
    assert checks==2100
    report['five_vertex_disjoint_family_pairs']={'checked':checks,'max_common_pairs':mx}

    rng=Random(478)
    sampled=0
    for n in range(5,9):
        for r in range(n-2,n+1):
            es=list(combinations(range(n),r-1))
            for _ in range(200):
                H={e:c for e in es if (c:=rng.randrange(4))}
                counts,good=analyze(n,r,H)
                check_complement(n,r,H,good)
                R,G,B=counts;T=len(good)
                assert T*T<=2*R*G*B
                assert T<=min(R*G,R*B,G*B)
                assert T<=(n-r+1)*min(counts)
                sampled+=1
    assert sampled==2400
    report['complement_bijection_and_d_le_3_samples']={'seed':478,'checked':sampled}
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
