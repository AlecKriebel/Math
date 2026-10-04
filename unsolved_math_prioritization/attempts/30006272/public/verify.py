#!/usr/bin/env python3
"""Bounded exact checks for the partial incidence results, standard library only.

This is not an intersection-cohomology implementation. All polynomial comparisons
below test explicitly proved formulas, and finite tests do not prove the theorems.
"""
from functools import lru_cache
from itertools import product
from math import comb
import argparse
import json
from pathlib import Path


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    z = [0] * max(len(p), len(q))
    for i, x in enumerate(p): z[i] += x
    for i, x in enumerate(q): z[i] += x
    return trim(z)


def mul(p, q):
    z = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q): z[i+j] += a*b
    return trim(z)


def shift(p, n):
    return (0,)*n + p


@lru_cache(None)
def gaussian(n, a):
    if not 0 <= a <= n: return (0,)
    if a == 0 or a == n: return (1,)
    return add(gaussian(n-1, a), shift(gaussian(n-1, a-1), n-a))


def partition_polynomial(a, b):
    out = [0] * (a*b+1)
    def visit(left, cap, total):
        if left == 0:
            out[total] += 1
            return
        for x in range(cap+1): visit(left-1, x, total+x)
    visit(a, b, 0)
    return trim(out)


def ends(k): return (0,)+tuple(k)+(0,)


def dimensions(r, h):
    z = ends(r)
    return tuple(h[i]+z[i]+z[i+1] for i in range(len(h)))


def shifted_h(h, k):
    z = ends(k)
    return tuple(h[i]+z[i]+z[i+1] for i in range(len(h)))


def end_dim_formula(r, h):
    z = ends(r)
    return sum(h[i]**2+h[i]*z[i+1]+z[i+1]**2+h[i]*z[i]+z[i]*z[i+1]
               for i in range(len(h)))


def end_dim_interval_count(r, h):
    intervals = [(i, i, x) for i,x in enumerate(h) if x]
    intervals += [(i, i+1, x) for i,x in enumerate(r) if x]
    return sum(x*y for a,b,x in intervals for c,d,y in intervals
               if c <= a <= d <= b)


def codim(h, k):
    z = ends(k)
    return sum(z[i+1]**2+z[i]*z[i+1]+h[i]*(z[i]+z[i+1])
               for i in range(len(h)))


def quad(k):
    z = ends(k)
    return sum(x*x for x in k)-sum(z[i]*z[i+1] for i in range(len(z)-1))


def fim(h, k):
    z = ends(k)
    return sum(z[i]*(h[i]+z[i+1]) for i in range(len(h)))


def fker(h, k):
    z = ends(k)
    return sum(z[i+1]*(h[i]+z[i]) for i in range(len(h)))


def fflag(h, k):
    z = ends(k)
    return sum(h[i]*(z[i]+z[i+1])+z[i]*z[i+1] for i in range(len(h)))


def interval_rises(r, h):
    for a in range(len(r)):
        for b in range(a, len(r)):
            if r[b] == 0: break
            yield h[b+1]-h[a]


def level_intervals(k):
    ans = []
    for level in range(1, max(k, default=0)+1):
        a = None
        for i in range(len(k)+1):
            high = i < len(k) and k[i] >= level
            if high and a is None: a = i
            if not high and a is not None:
                ans.append((level,a,i-1))
                a = None
    return ans


def path_relevant(h, k):
    z = ends(k)
    return (all(abs(z[i+1]-z[i]) <= 1 for i in range(len(z)-1))
            and all(h[b+1]-h[a] == 1 for _,a,b in level_intervals(k)))


def fiber_poly(h, k, kernel=False):
    z = ends(k)
    p = (1,)
    for i, x in enumerate(h):
        p = mul(p, gaussian(x+z[i]+z[i+1], z[i+1] if kernel else z[i]))
    return p


def main():
    counts = {"gaussian_partition_checks":0, "profiles":0,
              "rank_drop_cases":0, "semismall_profiles":0,
              "relevant_path_checks":0, "small_formula_degree_checks":0}
    for n in range(10):
        for a in range(n+1):
            p = gaussian(n,a)
            assert p == partition_polynomial(a,n-a)
            assert sum(p) == comb(n,a)
            assert p == gaussian(n,n-a)
            counts["gaussian_partition_checks"] += 1

    # Modest exhaustive profiles: n<=4, all r_i,h_i in {0,1,2}.
    for n in range(1,5):
        for r in product(range(3), repeat=n-1):
            for h in product(range(3), repeat=n):
                counts["profiles"] += 1
                d = dimensions(r,h)
                e = end_dim_formula(r,h)
                assert e == end_dim_interval_count(r,h)
                # Smooth bundle dimension versus direct orbit dimension.
                z = ends(r)
                base = sum(z[i]*(d[i]-z[i]) for i in range(n))
                bundle = sum((d[i]-z[i])*z[i+1] for i in range(n))
                assert base+bundle == sum(x*x for x in d)-e
                ks = list(product(*(range(x+1) for x in r)))
                actual_small = all(codim(h,k)>2*fim(h,k) for k in ks if any(k))
                criterion_small = all(h[i]>=h[i+1] for i,x in enumerate(r) if x)
                assert actual_small == criterion_small
                actual_semi = all(codim(h,k)>=2*fim(h,k) for k in ks)
                criterion_semi = all(x<=1 for x in interval_rises(r,h))
                assert actual_semi == criterion_semi
                kernel_small = all(h[i]<=h[i+1] for i,x in enumerate(r) if x)
                assert kernel_small == all(codim(h,k)>2*fker(h,k)
                                           for k in ks if any(k))
                counts["semismall_profiles"] += int(actual_semi)
                for k in ks:
                    counts["rank_drop_cases"] += 1
                    hp = shifted_h(h,k)
                    rp = tuple(a-b for a,b in zip(r,k))
                    assert dimensions(rp,hp) == d
                    assert codim(h,k) == end_dim_interval_count(rp,hp)-e
                    zz = ends(k)
                    assert 2*quad(k) == sum((zz[i+1]-zz[i])**2 for i in range(n))
                    delta = sum((h[i+1]-h[i])*k[i] for i in range(n-1))
                    assert codim(h,k)-2*fim(h,k) == quad(k)-delta
                    levels = level_intervals(k)
                    assert delta == sum(h[b+1]-h[a] for _,a,b in levels)
                    assert 2*len(levels) == sum(abs(zz[i+1]-zz[i]) for i in range(n))
                    assert quad(k) >= len(levels)
                    if actual_semi:
                        assert (codim(h,k)==2*fim(h,k)) == path_relevant(h,k)
                        counts["relevant_path_checks"] += 1
                    if actual_small:
                        p = fiber_poly(h,k)
                        assert len(p)-1 == fim(h,k)
                        if any(k): assert 2*(len(p)-1) < codim(h,k)
                        counts["small_formula_degree_checks"] += 1

    # Determinantal case, both chambers and every lower rank.
    det_cases = 0
    for a,b,k in product(range(6),range(6),range(5)):
        p = fiber_poly((a,b),(k,),kernel=a<b)
        assert p == gaussian(k+min(a,b),k)
        det_cases += 1
    assert gaussian(2,1) == (1,1)  # Sparse extrapolation would give (1,).

    # Complete four-stratum semismall example, with the one supported summand.
    h=(1,2,1); r=(1,1)
    relevant=[k for k in product(range(2),repeat=2)
              if codim(h,k)==2*fim(h,k)]
    assert relevant == [(0,0),(1,0)]
    example = {}
    for k in product(range(2),repeat=2):
        p=fiber_poly(h,k)
        if k[0] == 1:
            support=gaussian(k[1]+1,k[1])
            p=add(p,tuple(-x for x in shift(support,2)))
        assert all(x>=0 for x in p)
        if any(k): assert 2*(len(p)-1)<codim(h,k)
        example[str(k)]=list(p)
    assert example["(1, 1)"] == [1,2,1,1,1]
    assert example["(1, 0)"] == example["(0, 1)"] == [1,1]

    # The image-semismall class is not closed under its relevant supports.
    rr=(2,2,2); hh=(0,1,0,1); t=(1,1,1)
    assert all(x<=1 for x in interval_rises(rr,hh))
    assert codim(hh,t)==2*fim(hh,t)
    hnew=shifted_h(hh,t); rnew=tuple(a-b for a,b in zip(rr,t))
    assert hnew==(1,3,2,2)
    assert not all(x<=1 for x in interval_rises(rnew,hnew))

    # Three named incidence maps fail in the high-rise example.
    hh=(1,3,1)
    assert (codim(hh,(1,0)),fim(hh,(1,0)),fflag(hh,(1,0)))==(5,3,4)
    assert (codim(hh,(0,1)),fker(hh,(0,1)))==(5,3)

    result={"status":"PASS", "scope":"bounded exact checks, not a general IC algorithm",
            "counts":counts, "determinantal_cases":det_cases,
            "n3_example_polynomials_low_degree_first":example,
            "counterexample_to_naive_sparse_extension":{"r":[1],"h":[1,1],
                "true_polynomial":[1,1],"naive_polynomial":[1]},
            "unresolved":"uniform Catalan formula for all canonical-basis elements of complexes"}
    return result


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    out=json.dumps(main(),indent=2,sort_keys=True)+"\n"
    if args.output: args.output.write_text(out)
    print(out,end="")
