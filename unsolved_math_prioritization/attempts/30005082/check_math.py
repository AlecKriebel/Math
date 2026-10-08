#!/usr/bin/env python3
"""Exact, source-free finite controls for scoped mutation-comparison obstructions.
Uses only the Python standard library. No file writes or network access.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import json

class CheckFailure(Exception):
    pass

def require(condition, message):
    if not condition:
        raise CheckFailure(message)

def add(a, b):
    return tuple(x+y for x,y in zip(a,b))

def rank(rows):
    a=[list(map(Q,r)) for r in rows]
    if not a: return 0
    i=0
    for j in range(len(a[0])):
        p=next((r for r in range(i,len(a)) if a[r][j]),None)
        if p is None: continue
        a[i],a[p]=a[p],a[i]
        t=a[i][j];a[i]=[x/t for x in a[i]]
        for r in range(len(a)):
            if r != i and a[r][j]:
                t=a[r][j];a[r]=[x-t*y for x,y in zip(a[r],a[i])]
        i+=1
        if i==len(a): break
    return i

def columns_to_rows(cols):
    return [tuple(v[r] for v in cols) for r in range(len(cols[0]))]

TRIPLES=list(combinations(range(1,7),3))
RECTANGLES=[(r,c) for r in range(1,4) for c in range(1,4)]

def exponent(ordered):
    return tuple(int(c==ordered[r]) for r in range(3) for c in range(1,7))

def block_order(I, ell):
    a=list(I)
    if sum(j<=ell for j in I)==1:
        a[0],a[1]=a[1],a[0]
    return tuple(a)

def block_matrix(ell):
    return [[0]*6,list(range(ell,0,-1))+list(range(6,ell,-1)),list(range(12,0,-2))]

def leading_order(I, matrix):
    scores=[(sum(matrix[r][a[r]-1] for r in range(3)),a) for a in permutations(I)]
    scores.sort()
    require(scores[0][0]<scores[1][0], 'Non-unique determinant minimum')
    return scores[0][1]

def hilbert_counts(cols, maximum=4):
    values={(0,)*18};answer=[1]
    for d in range(1,maximum+1):
        values={add(v,e) for v in values for e in cols}
        answer.append(len(values))
    return answer

def grassmannian_hilbert(d):
    out=Q(1)
    for i in range(1,4):
        for j in range(4,7):
            out*=Q(d+j-i,j-i)
    require(out.denominator==1,'Hilbert dimension not integral')
    return int(out)

def rectangle_valuation(I):
    mu=[3+i-j for i,j in enumerate(I,1)]
    return tuple(max(sum(1 for i in range(1,r+1) for j in range(1,c+1)
                         if j>mu[i-1] and j-i==d) for d in range(-2,3))
                 for r,c in RECTANGLES)

def mutate(v, mode='min'):
    a=v[1]+v[3];b=v[4]
    out=list(v);out[0]=-v[0]+(min(a,b) if mode=='min' else max(a,b))
    return tuple(out)

def reflection(v):
    return (-v[0],)+tuple(v[1:])

def phi(v, direction=-1, factor_sign=1):
    """w=direction*e_0, factor endpoints sign*(e_1+e_3), sign*e_4."""
    m=min(factor_sign*(v[1]+v[3]),factor_sign*v[4])
    out=list(v);out[0]-=direction*m;return tuple(out)

def difference_phi(v):
    # w=-e_0 and F-F=conv{0, +/-((e_1+e_3)-e_4)}.
    d=v[1]+v[3]-v[4]
    out=list(v);out[0]+=min(0,d,-d);return tuple(out)

def minor(I):
    terms={}
    for p in permutations(I):
        parity=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        terms[exponent(p)]=(-1)**parity
    return terms

def poly_mul(a,b):
    out={}
    for x,c in a.items():
        for y,d in b.items():
            key=add(x,y);out[key]=out.get(key,0)+c*d
    return {x:c for x,c in out.items() if c}

def plucker_identity():
    total={}
    for sign,I,J in [(1,(2,3,6),(4,5,6)),(1,(2,5,6),(3,4,6)),(-1,(2,4,6),(3,5,6))]:
        for monomial,coefficient in poly_mul(minor(I),minor(J)).items():
            total[monomial]=total.get(monomial,0)+sign*coefficient
    require(not any(total.values()),'Square exchange polynomial identity failed')

def main():
    blocks=[];expected=[grassmannian_hilbert(d) for d in range(5)]
    require(expected==[1,20,175,980,4116],'Unexpected Grassmannian Hilbert values')
    for ell in range(7):
        matrix=block_matrix(ell)
        orders=[block_order(I,ell) for I in TRIPLES]
        require(all(leading_order(I,matrix)==a for I,a in zip(TRIPLES,orders)), 'Block coherence failed')
        cols=[exponent(a) for a in orders]
        require(hilbert_counts(cols)==expected,'Block Hilbert regression failed')
        blocks.append(cols)
    a,b=blocks[:2]
    indices=[TRIPLES.index(I) for I in [(1,3,4),(2,4,5),(1,4,5),(2,3,4)]]
    i,j,k,l=indices
    require(add(a[i],a[j])==add(a[k],a[l]),'Source relation missing')
    require(add(b[i],b[j])!=add(b[k],b[l]),'Target relation unexpectedly holds')
    ranks=[rank(columns_to_rows(c)) for c in blocks]
    joint=rank(columns_to_rows(a)+columns_to_rows(b))
    require(ranks==[10]*7 and joint==12,'Rank certificate failed')
    intersection=ranks[0]+ranks[1]-joint
    require(intersection==8 and intersection<9,'Adjacency obstruction failed')
    hex_matrix=[[0]*6,[18,3,15,6,9,12],[42,35,28,21,14,7]]
    hex_cols=[exponent(leading_order(I,hex_matrix)) for I in TRIPLES]
    hex_counts=hilbert_counts(hex_cols)
    require(hex_counts==[1,20,174,968,4040],'Hexagonal Hilbert regression failed')
    vals={I:rectangle_valuation(I) for I in TRIPLES}
    require(all(x>=0 for v in vals.values() for x in v),'Negative rectangle value')
    require(vals[(1,4,5)]==(0,0,0,0,1,1,0,1,2),'First rectangle witness changed')
    require(vals[(3,5,6)]==(0,1,1,1,1,2,1,2,2),'Second rectangle witness changed')
    u,v=vals[(1,4,5)],vals[(3,5,6)]
    images=[mutate(u,'max'),mutate(v,'max')]
    midpoint=tuple(Q(x+y,2) for x,y in zip(*images))
    preimage=mutate(midpoint,'max')
    require(preimage[0]==Q(-1,2),'Convexity separator failed')
    require(mutate(preimage,'max')==midpoint,'Max map involution failed')
    require(phi(reflection(u),1,1)[0]==0 and mutate(u,'max')[0]==1,'ArXiv v2 counterexample failed')
    samples=0
    for t,a1,a2,b1 in product(range(-3,4),repeat=4):
        x=(Q(t,2),Q(a1,2),0,Q(a2,2),Q(b1,2),0,0,0,0)
        require(phi(reflection(x),-1,1)==mutate(x,'min'),'Min factorization failed')
        require(phi(reflection(x),1,-1)==mutate(x,'max'),'Corrected max factorization failed')
        require(difference_phi(mutate(x,'max'))==mutate(x,'min'),'Difference-body relation failed')
        require(mutate(mutate(x,'max'),'max')==x,'Max involution failed')
        require(mutate(mutate(x,'min'),'min')==x,'Min involution failed')
        require(phi(phi(x,-1,1),1,1)==x,'Mutation inverse failed')
        samples+=1
    plucker_identity()
    # Fail-closed corruption controls: the guards must remain effective under -O/-OO.
    rejected=0
    for test in [lambda:require(174==175,'bad Hilbert claim'),lambda:require(intersection==9,'bad adjacency'),lambda:require(preimage[0]>=0,'bad convexity')]:
        try:test()
        except CheckFailure:rejected+=1
    require(rejected==3,'Fail-closed guard self-test failed')
    return {'status':'PASS','scope':'Exact finite controls and counterexamples; not a proof of the global characterization',
            'block_coherence_cases':140,'block_hilbert_degrees_0_to_4':expected,
            'hexagonal_hilbert_degrees_0_to_4':hex_counts,
            'source_label_relation':['134+245','145+234'],'source_relation_equal':True,'target_relation_equal':False,
            'block_ranks':ranks,'B0_B1_stacked_rank':joint,'span_intersection_dimension':intersection,
            'adjacent_prime_cones_need_common_dimension':9,
            'rectangle_coordinate_order':RECTANGLES,
            'nonconvexity_Plucker_labels':['145','356'],'max_image_midpoint':list(map(str,midpoint)),
            'unique_max_preimage':list(map(str,preimage)),
            'arxiv_v2_formula_left_coordinate':1,'arxiv_v2_formula_right_coordinate':0,
            'corrected_formula_exact_rational_samples':samples,
            'square_exchange_symbolic_polynomial_identity':True,'rejected_false_controls':rejected}

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
