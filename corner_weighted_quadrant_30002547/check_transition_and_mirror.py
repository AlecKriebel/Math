#!/usr/bin/env python3
"""Independent exact finite controls; not proofs of limits or operator assertions.

Uses integer/Fraction arithmetic only. No network, source documents, or third-party
packages. In particular, no truncated matrix eigenvalue is used to infer a radius.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import comb
import json


def clean(v):
    return {p: x for p, x in v.items() if x}


def add(*terms):
    result = defaultdict(F)
    for factor, vector in terms:
        for p, value in vector.items():
            result[p] += factor * value
    return clean(result)


def shift(v, dx, dy):
    return {(i+dx, j+dy): value for (i, j), value in v.items()
            if i+dx >= 0 and j+dy >= 0}


def C(v):
    return add((1, shift(v, 1, 0)), (1, shift(v, 0, 1)))


def Cs(v):
    return add((1, shift(v, -1, 0)), (1, shift(v, 0, -1)))


def A(v):
    return add((1, C(v)), (1, Cs(v)))


def B(v):
    return add((1, shift(v, -1, 1)), (1, shift(v, 1, -1)))


def K(v, c, t):
    return add((1, v), (-t, A(v)), (c*t*t, B(v)))


def T(v, alpha):
    return add((1, C(v)), (-alpha, v))


def Ts(v, alpha):
    return add((1, Cs(v)), (-alpha, v))


def dot(v, w):
    return sum(x*w.get(p, 0) for p, x in v.items())


def operator_checks():
    samples = [{(0, 0): F(1)}]
    for seed in range(1, 8):
        samples.append(clean({(i, j): F(((i+2*j+seed)*seed) % 7-3, seed+1)
                              for i in range(4) for j in range(4)}))
    parameters = [(F(3,2), F(1,3)), (F(17,9), F(6,17)),
                  (F(1), F(1,7)), (F(5,4), F(1,4)), (F(2), F(2,7))]
    for v in samples:
        assert Cs(C(v)) == add((2, v), (1, B(v)))
        for c, t in parameters:
            alpha = 1/(c*t)
            eta = 1-1/c-2*c*t*t
            factored = add((c*t*t, Ts(T(v, alpha), alpha)), (eta, v))
            assert K(v, c, t) == factored
            derivative_numerator = add((1, A(v)), (-2*c*t, B(v)))
            rearranged = add((1/t, v), (-c*t, B(v)), (-1/t, K(v,c,t)))
            assert derivative_numerator == rearranged
            # The exact quadratic-form inequality used in the derivative bound.
            lhs = dot(v, add((1, v), (-c*t*t, B(v))))
            rhs = (1-2*c*t*t)*dot(v,v)
            assert lhs >= rhs
        c, t = F(3,2), F(1,3)
        assert K(v,c,t) == add((F(1,6), Ts(T(v,F(2)),F(2))))
        # A rational upper-branch critical point: t=3/10, c=10/9, alpha=3.
        c, t, alpha = F(10,9), F(3,10), F(3)
        d = c*t*t
        laplacian = add((4, v), (-1, A(v)))
        square = Ts(T(v,F(2)),F(2))
        assert K(v,c,t) == add((d*(alpha-2), laplacian), (d, square))
        assert dot(v,square) <= 2*dot(v,laplacian)
    for n in range(81):
        coefficients = [comb(n,j) for j in range(n+1)]
        assert sum(x*x for x in coefficients) == comb(2*n,n)
        assert F(comb(2*n,n),4**n) >= F(1,2*n+1)
    delta = {(0,0): F(1)}
    for cutoff in range(21):
        formal = {(j,n-j): F(3,2)*F(comb(n,j),2**n)
                  for n in range(cutoff+1) for j in range(n+1)}
        residual = add((1, T(formal,F(2))), (3, delta))
        assert set(i+j for i,j in residual) == {cutoff+1}
        assert all(value == F(3,2)*F(comb(cutoff+1,i),2**cutoff)
                   for (i,j),value in residual.items())
        critical_residual = add((1,K(formal,F(3,2),F(1,3))),(-1,delta))
        assert all(i+j >= cutoff for i,j in critical_residual)
    return {'sparse_test_vectors':len(samples), 'factorization_parameters':len(parameters),
            'norm_binomial_degrees':list(range(81)), 'formal_recurrence_cutoffs':list(range(21)),
            'arithmetic':'exact rational and integer; no floating point'}


def mirror_checks():
    directions = 'ENWS'
    shifts = dict(zip(directions, ((1,0),(0,1),(-1,0),(0,-1))))
    opposite = dict(zip(directions, 'WSEN'))
    def vertices(word):
        x=y=0
        result=[(x,y)]
        for d in word:
            dx,dy=shifts[d]; x+=dx; y+=dy
            result.append((x,y))
        return result
    def rn(word):
        return ''.join(opposite[d] for d in reversed(word))
    def corners(word):
        return sum(a+b in ('NW','ES') for a,b in zip(word,word[1:]))
    pair_counts=[]
    for n in range(1,7):
        H=1
        while H**3 < n*n:
            H+=1
        classes=defaultdict(list)
        for steps in product(directions,repeat=n):
            word=''.join(steps)
            path=vertices(word)
            if all(max(abs(x),abs(y)) <= H for x,y in path):
                classes[(path[-1],word[0],word[-1])].append(word)
        count=0
        for (_,first,_),words in classes.items():
            prefix=('N'*H+'E'*H) if first=='W' else ('E'*H+'N'*H)
            images=set()
            for p in words:
                assert corners(p)==corners(rn(p))
                for q in words:
                    image=prefix+p+rn(q)+rn(prefix)
                    path=vertices(image)
                    assert len(image)==2*n+4*H and path[-1]==(0,0)
                    assert all(x>=0 and y>=0 for x,y in path)
                    assert corners(image)==corners(p)+corners(q)
                    assert image not in images
                    images.add(image); count+=1
        pair_counts.append(count)
    assert pair_counts == [4,16,64,572,6304,78248]
    return {'H':'smallest integer with H^3 >= n^2', 'maximum_word_length':6,
            'ordered_pairs_by_length':pair_counts,'total_ordered_pairs':sum(pair_counts)}


def blocking_checks():
    directions='ENWS'
    corners={('N','W'),('E','S')}
    M=[[(0,1) if (i,j) in corners else (1,0) for j in directions] for i in directions]
    expected=[[(3,1),(3,1),(2,2),(2,2)],
              [(3,1),(3,1),(2,2),(2,2)],
              [(4,0),(4,0),(3,1),(3,1)],
              [(4,0),(4,0),(3,1),(3,1)]]
    for i in range(4):
        for j in range(4):
            polynomial=[0,0,0]
            for k in range(4):
                for left,x in enumerate(M[i][k]):
                    for right,y in enumerate(M[k][j]):
                        polynomial[left+right]+=x*y
            assert tuple(polynomial[:2])==expected[i][j] and polynomial[2]==0
    for k in range(1,41):
        histogram=defaultdict(int)
        for position in range(k+1):
            word='N'*position+'W'+'N'*(k-position)
            count=sum(a+b=='NW' for a,b in zip(word,word[1:]))
            histogram[count]+=1
        assert dict(histogram)=={0:1,1:k}
    arbitrary=[1,4]
    for n in range(2,81):
        arbitrary.append(4*arbitrary[-1]-4*arbitrary[-2])
    assert arbitrary==[(n+1)*2**n for n in range(81)]
    return {'M_squared_entries':16,'no_initial_seam_lengths':list(range(2,42)),
            'a_minus_one_arbitrary_word_coefficients_through_length':80}


if __name__=='__main__':
    print(json.dumps({'operator_checks':operator_checks(), 'mirror_checks':mirror_checks(),
                      'blocking_checks':blocking_checks(),
                      'status':'PASS', 'scope':'Finite exact normalization controls only.'},
                     indent=2,sort_keys=True))
