#!/usr/bin/env python3
"""Self-contained exact arithmetic; complete pair-line incidence certificates.

No floating point, external packages, numerical LP, or candidate code is used.
An exhaustive finite check supplements, rather than replaces, the all-n proof.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
from collections import Counter
import json
import sys


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def padd(a, b):
    r = [Q(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        r[i] += x
    for i, x in enumerate(b):
        r[i] += x
    return trim(r)


def pneg(a):
    return [-x for x in a]


def pmul(a, b):
    if not a or not b:
        return []
    r = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i+j] += x*y
    return trim(r)


def pdiv(a, b):
    a, b = trim(a), trim(b)
    if not b:
        raise ZeroDivisionError
    r = [Q(0)] * max(0, len(a)-len(b)+1)
    while len(a) >= len(b):
        k, t = len(a)-len(b), a[-1]/b[-1]
        r[k] += t
        for j, x in enumerate(b):
            a[k+j] -= t*x
        a = trim(a)
    return trim(r), a


@lru_cache(None)
def cyclotomic(n):
    p = [Q(-1)] + [Q(0)]*(n-1) + [Q(1)]
    for d in range(1, n):
        if n % d == 0:
            p, rem = pdiv(p, cyclotomic(d))
            assert not rem
    return tuple(p)


class Field:
    def __init__(self, n):
        self.n = n
        self.mod = cyclotomic(n)
        self.d = len(self.mod)-1
        self.zero = (Q(0),)*self.d
        self.one = (Q(1),)+(Q(0),)*(self.d-1)
        self.zeta = self.reduce([Q(0),Q(1)])

    def reduce(self, p):
        r = pdiv(p, self.mod)[1]
        return tuple(r+[Q(0)]*(self.d-len(r)))

    def add(self, a, b):
        return tuple(x+y for x,y in zip(a,b))

    def neg(self, a):
        return tuple(-x for x in a)

    def sub(self, a, b):
        return tuple(x-y for x,y in zip(a,b))

    @lru_cache(None)
    def mul(self, a, b):
        if a == self.zero or b == self.zero:
            return self.zero
        if a == self.one:
            return b
        if b == self.one:
            return a
        return self.reduce(pmul(a,b))

    @lru_cache(None)
    def inv(self, a):
        if a == self.zero:
            raise ZeroDivisionError
        r0,r1 = list(self.mod),trim(a)
        s0,s1 = [],[Q(1)]
        while r1:
            quo,r2 = pdiv(r0,r1)
            r0,r1 = r1,r2
            s0,s1 = s1,padd(s0,pneg(pmul(quo,s1)))
        assert len(r0) == 1
        ans = self.reduce([x/r0[0] for x in s0])
        assert self.mul(a,ans) == self.one
        return ans

    def norm(self, v):
        assert any(x != self.zero for x in v)
        t = self.inv(next(x for x in v if x != self.zero))
        return tuple(self.mul(x,t) for x in v)

    def cross(self, a, b):
        return (self.sub(self.mul(a[1],b[2]),self.mul(a[2],b[1])),
                self.sub(self.mul(a[2],b[0]),self.mul(a[0],b[2])),
                self.sub(self.mul(a[0],b[1]),self.mul(a[1],b[0])))


def qs(x):
    return str(x)


def check(n):
    F = Field(n)
    z,o = F.zero,F.one
    roots = [o]
    for _ in range(1,n):
        roots.append(F.mul(roots[-1],F.zeta))
    assert len(set(roots)) == n and F.mul(roots[-1],F.zeta) == o
    comps = {F.norm(v) for a in roots for v in
             ((o,F.neg(a),z),(z,o,F.neg(a)),(o,z,F.neg(a)))}
    assert len(comps) == 3*n
    actual = {F.norm(F.cross(a,b)) for a,b in combinations(comps,2)}
    grid = {F.norm((a,b,o)) for a in roots for b in roots}
    vertices = {F.norm(v) for v in ((o,z,z),(z,o,z),(z,z,o))}
    expected = grid | (vertices if n>=2 else set())
    assert actual == expected
    points = sorted(actual)
    index = {p:i for i,p in enumerate(points)}
    line_points = {}
    for i,j in combinations(range(len(points)),2):
        M = F.norm(F.cross(points[i],points[j]))
        line_points.setdefault(M,set()).update((i,j))
    if len(points)==1:
        line_points = {next(iter(comps)):{0}}
    # Complete pair enumeration proves all support columns with >=2 points.
    # Singleton columns never improve a cover, and dual feasibility there is y<=1.
    K = max(map(len,line_points.values()))
    comp_support = {M:{i for i,p in enumerate(points)
                        if F.add(F.add(F.mul(M[0],p[0]),F.mul(M[1],p[1])),
                                 F.mul(M[2],p[2]))==z} for M in comps}
    for M,S in comp_support.items():
        if len(S)>=2:
            assert line_points[M] == S
    multiplicities = Counter(sum(i in S for S in comp_support.values())
                             for i in range(len(points)))
    if n>=3:
        assert K == n+1
        assert all(len(S)==n+1 for S in comp_support.values())
        assert max((len(S) for M,S in line_points.items() if M not in comps),
                   default=0)<=2
        primal = {M:Q(1,3) for M in comps}
        dual = {i:(Q(1,n) if p in grid else Q(0)) for i,p in enumerate(points)}
        comp_dual = dual
        comp_primal = primal
        optimum = Q(n)
        comp_optimum = Q(n)
    elif n==2:
        assert K==3
        axes = {F.norm(v) for v in ((o,z,z),(z,o,z),(z,z,o))}
        assert all(len(line_points[M])==2 for M in axes)
        primal = {M:Q(1,3) for M in comps}
        primal.update({M:Q(1,6) for M in axes})
        dual = {i:(Q(1,4) if p in grid else Q(1,2)) for i,p in enumerate(points)}
        comp_primal = {M:Q(1,2) for M in comps}
        comp_dual = {i:(Q(0) if p in grid else Q(1)) for i,p in enumerate(points)}
        optimum,comp_optimum = Q(5,2),Q(3)
    else:
        assert K==1 and len(points)==1
        primal = {next(iter(comps)):Q(1)}
        dual = {0:Q(1)}
        comp_primal,comp_dual = primal,dual
        optimum=comp_optimum=Q(1)

    def verify_primal(weights,total):
        assert sum(weights.values())==total
        cov = [sum(w for M,w in weights.items() if i in
                   (line_points.get(M) or comp_support[M]))
               for i in range(len(points))]
        assert min(cov)>=1
        return min(cov),max(cov)

    def verify_dual(weights,support,total):
        assert sum(weights.values())==total
        assert min(weights.values())>=0 and max(weights.values())<=1
        loads = [sum(weights[i] for i in S) for S in support.values()]
        assert max(loads)<=1
        return max(loads)

    pcov=verify_primal(primal,optimum)
    ccov=verify_primal(comp_primal,comp_optimum)
    dload=verify_dual(dual,line_points,optimum)
    cload=verify_dual(comp_dual,comp_support,comp_optimum)
    result={
        "n":n,"q_if_9q_family":n//3 if n%3==0 else None,
        "cyclotomic_modulus_low_to_high":[qs(c) for c in F.mod],
        "component_count":len(comps),"singular_count":len(actual),
        "singular_multiplicity_histogram":dict(sorted(multiplicities.items())),
        "all_pair_line_count":len(line_points),
        "all_pair_line_support_histogram":dict(sorted(Counter(map(len,line_points.values())).items())),
        "K_all_lines":K,"tau_components":qs(comp_optimum),
        "tau_all_lines":qs(optimum),"all_primal_coverage_range":list(map(qs,pcov)),
        "component_primal_coverage_range":list(map(qs,ccov)),
        "all_dual_max_line_load":qs(dload),"component_dual_max_line_load":qs(cload),
        "epsilon_by_proved_cover_criterion":qs(Q(1,K)),
        "exact_verifications":"PASS"
    }
    print(json.dumps(result,sort_keys=True),flush=True)
    F.mul.cache_clear()
    F.inv.cache_clear()
    return result


if __name__=="__main__":
    requested=list(map(int,sys.argv[1:])) or [1,2,3,6,9]
    assert all(n>=1 for n in requested)
    for n in requested:
        check(n)
    print("ALL EXACT CHECKS PASSED",flush=True)
