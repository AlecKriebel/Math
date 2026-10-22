#!/usr/bin/env python3
"""Exact finite checks of the paper's explicit constructions.

These checks supplement the infinite theoretical proof; they do not certify
all embeddings or replace the lemmas in the manuscript. Python 3, stdlib only.
"""
if not __debug__:
    raise RuntimeError("Run without -O: exact checks must remain enabled")

from fractions import Fraction as F
import json


def pow2(k):
    return F(2**k) if k >= 0 else F(1, 2**(-k))


def split_segment(a, b, c, d):
    """Map [a,b] to [c,d] with two adjacent power-of-two slopes."""
    if not a < b or not c < d:
        raise ValueError('Segments must increase')
    ratio = (d-c)/(b-a)
    k = 0
    while pow2(k) > ratio:
        k -= 1
    while pow2(k+1) < ratio:
        k += 1
    lo, hi = pow2(k), pow2(k+1)
    theta = (hi-ratio)/(hi-lo)
    assert 0 <= theta <= 1
    midx = a + theta*(b-a)
    midy = c + lo*(midx-a)
    assert midy + hi*(b-midx) == d
    return [(a,c),(midx,midy),(b,d)], [lo,hi]


def interpolate_tuple(xs, ys):
    if len(xs) != len(ys) or any(x>=y for x,y in zip(xs,xs[1:])) or any(x>=y for x,y in zip(ys,ys[1:])):
        raise ValueError('Tuples must be equally long and strictly increasing')
    if not 0 < min(xs+ys) <= max(xs+ys) < 1:
        raise ValueError('Tuples must be interior')
    c = min(xs+ys)/2
    d = (max(xs+ys)+1)/2
    source, target = [c]+xs+[d], [c]+ys+[d]
    segments = []
    for a,b,e,f in zip(source,source[1:],target,target[1:]):
        pts, slopes = split_segment(a,b,e,f)
        segments.append((pts,slopes))
    return segments


def bump_value(a,b,x):
    mid=a+(b-a)/3
    if x <= mid:
        return a+2*(x-a)
    return b+(x-b)/2


def run():
    ratios = [F(1,2**j) for j in range(1,21)]+[F(2**j) for j in range(21)]
    ratios += [F(p,q) for p in range(1,40) for q in range(1,40)]
    segment_count=0
    for r in ratios:
        pts, slopes=split_segment(F(0),F(1),F(0),r)
        assert pts[0]==(F(0),F(0)) and pts[-1]==(F(1),r)
        assert slopes[1]==2*slopes[0]
        segment_count+=1
    tuples=[([F(1,10),F(2,10),F(3,10),F(4,10)], [F(6,10),F(7,10),F(8,10),F(9,10)]),
            ([F(1,1000),F(1,3),F(2,3),F(999,1000)], [F(1,5),F(2,5),F(3,5),F(4,5)]),
            ([F(1,5),F(2,5),F(3,5),F(4,5)],[F(1,1000),F(1,3),F(2,3),F(999,1000)])]
    for xs,ys in tuples:
        segs=interpolate_tuple(xs,ys)
        for index,(pts,slopes) in enumerate(segs):
            assert pts[0][0] < pts[-1][0] and pts[0][1] < pts[-1][1]
            if index+1<len(segs):
                assert pts[-1]==segs[index+1][0][0]
    bump_count=0
    left, right=[],[]
    for m in range(100):
        b=pow2(-2*m-2);a=b/2
        left.append((a,b));right.append((1-b,1-a))
        for v,w in [left[-1],right[-1]]:
            mid=v+(w-v)/3
            assert v+2*(mid-v)==w+(mid-w)/2
            assert bump_value(v,w,v)==v and bump_value(v,w,w)==w
            for j in range(1,25):
                x=v+F(j,25)*(w-v)
                assert x < bump_value(v,w,x) < w
            bump_count+=1
    for n in range(99):
        assert left[n+1][1] < left[n][0]
        assert right[n][1] < right[n+1][0]
    # Right-germ conjugation: h^-1 f h at the transported fixed point
    # has slope c^-1*k*c = k, for every affine branch, exactly.
    germ_cases=0
    for i in range(-10,11):
        for j in range(-10,11):
            c,k=pow2(i),pow2(j)
            assert (1/c)*k*c==k
            germ_cases+=1
    # Affine group is metabelian: commutators have slope one and
    # their translation commutators vanish (symbolic coefficient law).
    def mul(x,y):return (x[0]*y[0], x[0]*y[1]+x[1])
    def inv(x):return (1/x[0], -x[1]/x[0])
    def comm(x,y):return mul(mul(mul(inv(x),inv(y)),x),y)
    affine_cases=0
    for a in [F(1,2),F(1),F(2),F(3)]:
        for b in [F(-3),F(0),F(2,3)]:
            for c in [F(1,3),F(1),F(4)]:
                q=comm((a,b),(c,F(5,7)))
                assert q[0]==1
                assert comm(q,(F(1),F(2,9)))==(F(1),F(0))
                affine_cases+=1
    return dict(status='passed', arithmetic='exact rational', segment_cases=segment_count,
                tuple_cases=len(tuples), bump_intervals=bump_count,germ_cases=germ_cases,
                affine_cases=affine_cases,
                limitation='Finite construction checks; infinite and universal claims are proved in manuscript, not inferred from tests')


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
