#!/usr/bin/env python3
"""Independent finite audit: no imports from the candidate implementation.

Orbit dimensions are obtained by solving the commuting-endomorphism equations
for explicit normal-form matrices, using union-find on scalar variables. Gaussian
polynomials are enumerated by Schubert subset weights. This checks formulas and
bounded cases; it does not compute general intersection cohomology.
"""
import argparse
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path


def plus(a, b):
    c = [0] * max(len(a), len(b))
    for i, v in enumerate(a): c[i] += v
    for i, v in enumerate(b): c[i] += v
    while len(c) > 1 and c[-1] == 0: c.pop()
    return tuple(c)


def times(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): c[i+j] += x*y
    return tuple(c)


@lru_cache(None)
def grassmann(N, a):
    assert 0 <= a <= N
    p = [0] * (a*(N-a) + 1)
    for cells in combinations(range(N), a):
        p[sum(cells)-a*(a-1)//2] += 1
    return tuple(p)


def adjacent(x):
    y = (0,) + tuple(x) + (0,)
    return tuple(zip(y[:-1], y[1:]))


def vertex_dimensions(r, h):
    return tuple(x+a+b for x,(a,b) in zip(h,adjacent(r)))


@lru_cache(None)
def commuting_dimension(d, s):
    """Dimension of solutions of f_i X_i = X_{i+1} f_i.

    Vertex blocks are incoming, homology, outgoing. Each normal-form arrow
    identifies its outgoing block with the next vertex's incoming block.
    Every scalar equation equates two variables, or sets a variable to zero.
    """
    offsets = [0]
    for x in d: offsets.append(offsets[-1]+x*x)
    zero = offsets[-1]
    parent = list(range(zero+1))
    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def unite(x, y):
        x, y = root(x), root(y)
        if x != y: parent[x] = y
    def var(i, a, b): return offsets[i]+a*d[i]+b
    for i, rank in enumerate(s):
        start = d[i]-rank
        for a in range(d[i+1]):
            for b in range(d[i]):
                left = var(i,start+a,b) if a < rank else zero
                right = var(i+1,a,b-start) if b >= start else zero
                unite(left,right)
    return len({root(v) for v in range(zero+1)})-1


def orbit_dimension(d, s):
    return sum(x*x for x in d)-commuting_dimension(d,s)


def image_fiber(d, s, r):
    # U_i / Im(f_{i-1}) lies in Ker(f_i) / Im(f_{i-1}).
    sizes = []
    for D,(sp,sn),(rp,rn) in zip(d,adjacent(s),adjacent(r)):
        sizes.append((D-sp-sn,rp-sp))
    return tuple(sizes)


def fiber_dimension(sizes): return sum(a*(N-a) for N,a in sizes)


def fiber_polynomial(sizes):
    p = (1,)
    for N,a in sizes: p = times(p,grassmann(N,a))
    return p


def intervals(r):
    for start in range(len(r)):
        for end in range(start,len(r)):
            if r[end] == 0: break
            yield start,end


def level_components(k):
    out = []
    for m in range(1,max(k,default=0)+1):
        active = [j for j,x in enumerate(k) if x >= m]
        while active:
            start = end = active.pop(0)
            while active and active[0] == end+1: end = active.pop(0)
            out.append((start,end))
    return out


def sparse_source(h, k):
    pairs = adjacent(k)
    omega = [i for i,x in enumerate(h) if x]
    p = (0,)
    for choices in product(*(range(min(pairs[i])+1) for i in omega)):
        shift = sum((h[i]+t)*t for i,t in zip(omega,choices))
        term = (0,)*shift+(1,)
        selected = dict(zip(omega,choices))
        for i,(a,b) in enumerate(pairs):
            if i in selected:
                t = selected[i]
                term = times(term,times(grassmann(b,b-t),grassmann(a,t)))
            else: term = times(term,grassmann(a+b,b))
        p = plus(p,term)
    return p


def main():
    counts = dict(profiles=0,rank_drop_cases=0,semismall_profiles=0,
                  relevant_path_checks=0,small_formula_degree_checks=0,
                  sparse_source_small_chamber_comparisons=0)
    for n in range(1,5):
        for r in product(range(3),repeat=n-1):
            for h in product(range(3),repeat=n):
                counts['profiles'] += 1
                d = vertex_dimensions(r,h)
                open_dim = orbit_dimension(d,r)
                # Independent base plus vector-bundle dimension.
                assert open_dim == sum(a*(D-a)+(D-a)*b
                                       for D,(a,b) in zip(d,adjacent(r)))
                rows = []
                for k in product(*(range(x+1) for x in r)):
                    counts['rank_drop_cases'] += 1
                    s = tuple(a-b for a,b in zip(r,k))
                    c = open_dim-orbit_dimension(d,s)
                    sizes = image_fiber(d,s,r)
                    f = fiber_dimension(sizes)
                    formula_c = sum(b*b+a*b+x*(a+b)
                                    for x,(a,b) in zip(h,adjacent(k)))
                    assert c == formula_c
                    qform = sum((a-b)**2 for a,b in adjacent(k))//2
                    delta = sum(t*(h[j+1]-h[j]) for j,t in enumerate(k))
                    assert c-2*f == qform-delta
                    levels = level_components(k)
                    assert delta == sum(h[b+1]-h[a] for a,b in levels)
                    assert 2*len(levels) == sum(abs(a-b) for a,b in adjacent(k))
                    rows.append((k,c,f,sizes))
                small = all(c > 2*f for k,c,f,_ in rows if any(k))
                semi = all(c >= 2*f for _,c,f,_ in rows)
                assert small == all(h[j] >= h[j+1] for j,x in enumerate(r) if x)
                assert semi == all(h[b+1]-h[a] <= 1 for a,b in intervals(r))
                counts['semismall_profiles'] += semi
                # Dual reversal is checked through actual dimensions, too.
                reverse_d,reverse_r = tuple(reversed(d)),tuple(reversed(r))
                kernel_small = all(h[j] <= h[j+1] for j,x in enumerate(r) if x)
                assert kernel_small == all(c > 2*fiber_dimension(image_fiber(
                    reverse_d,tuple(reversed(tuple(a-b for a,b in zip(r,k)))),reverse_r))
                    for k,c,_,_ in rows if any(k))
                for k,c,f,sizes in rows:
                    if semi:
                        predicted = (all(abs(a-b) <= 1 for a,b in adjacent(k)) and
                                     all(h[b+1]-h[a] == 1 for a,b in level_components(k)))
                        assert (c == 2*f) == predicted
                        counts['relevant_path_checks'] += 1
                    if small:
                        p = fiber_polynomial(sizes)
                        assert len(p)-1 == f
                        assert not any(k) or 2*(len(p)-1) < c
                        counts['small_formula_degree_checks'] += 1
                    sparse = all(not(h[j] and h[j+1]) for j in range(n-1))
                    if sparse and (small or kernel_small):
                        if small: p = fiber_polynomial(sizes)
                        else:
                            s = tuple(a-b for a,b in zip(r,k))
                            p = fiber_polynomial(image_fiber(reverse_d,tuple(reversed(s)),reverse_r))
                        assert p == sparse_source(h,k)
                        counts['sparse_source_small_chamber_comparisons'] += 1
    assert counts['profiles'] == 2460
    assert counts['rank_drop_cases'] == 18525
    assert counts['semismall_profiles'] == 1864
    assert counts['relevant_path_checks'] == 12580
    assert counts['small_formula_degree_checks'] == 5665

    h=(1,2,1); r=(1,1); d=vertex_dimensions(r,h)
    example = {}
    relevant_image = []
    relevant_kernel = []
    for k in product(range(2),repeat=2):
        s=tuple(a-b for a,b in zip(r,k))
        c=orbit_dimension(d,r)-orbit_dimension(d,s)
        im=image_fiber(d,s,r)
        ker=image_fiber(tuple(reversed(d)),tuple(reversed(s)),tuple(reversed(r)))
        if c == 2*fiber_dimension(im): relevant_image.append(k)
        if c == 2*fiber_dimension(ker): relevant_kernel.append(k)
        p=fiber_polynomial(im)
        if k[0]: p=plus(p,(0,0)+tuple(-x for x in grassmann(k[1]+1,k[1])))
        dual=fiber_polynomial(ker)
        if k[1]: dual=plus(dual,(0,0)+tuple(-x for x in grassmann(k[0]+1,k[0])))
        assert p == dual
        example[str(k)] = list(p)
    assert relevant_image == [(0,0),(1,0)]
    assert relevant_kernel == [(0,0),(0,1)]
    assert example['(1, 1)'] == [1,2,1,1,1]
    assert grassmann(2,1) != sparse_source((1,1),(1,))
    return dict(status='PASS',scope='Independent bounded algebraic checks, not a general IC computation',
                counts=counts,origin_example_image_and_kernel_agree=True,
                example_polynomials_low_degree_first=example,
                implementation_independence='No candidate imports; matrix commuting equations and Schubert subset enumeration')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    out=json.dumps(main(),indent=2,sort_keys=True)+'\n'
    if args.output: args.output.write_text(out)
    print(out,end='')
