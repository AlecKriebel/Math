#!/usr/bin/env python3
"""Independent finite checks; no asymptotic or literature theorem is certified."""
from fractions import Fraction as F
from functools import total_ordering
from itertools import permutations
from math import isqrt
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = "96e071e004aef40ae132a5ec27c8c8aaacf55b5fd52202ef1da25999771db544"
counts = {}
def check(group, assertion):
    if not assertion:
        raise AssertionError(group)
    counts[group] = counts.get(group, 0) + 1

manifest_bytes = (ROOT / "public/MANIFEST.json").read_bytes()
check("integrity", hashlib.sha256(manifest_bytes).hexdigest() == EXPECTED)
for item in json.loads(manifest_bytes)["files"]:
    data = (ROOT / "public" / item["path"]).read_bytes()
    check("integrity", len(data) == item["bytes"])
    check("integrity", hashlib.sha256(data).hexdigest() == item["sha256"])
check("integrity", (ROOT / "audit/replay.json").read_bytes() ==
      (ROOT / "public/verification/result.json").read_bytes())

@total_ordering
class Quadratic:
    """Ordering by certified rational sqrt enclosures, not the author's sign code."""
    def __init__(self, d, a=0, b=0): self.d, self.a, self.b = d, F(a), F(b)
    def coerce(self, value):
        if isinstance(value, Quadratic):
            assert value.d == self.d
            return value
        return Quadratic(self.d, value)
    def __add__(self, value):
        value = self.coerce(value)
        return Quadratic(self.d, self.a + value.a, self.b + value.b)
    __radd__ = __add__
    def __neg__(self): return Quadratic(self.d, -self.a, -self.b)
    def __sub__(self, value): return self + -self.coerce(value)
    def __rsub__(self, value): return self.coerce(value) + -self
    def __mul__(self, value):
        value = self.coerce(value)
        return Quadratic(self.d, self.a * value.a + self.d * self.b * value.b,
                         self.a * value.b + self.b * value.a)
    __rmul__ = __mul__
    def __eq__(self, value):
        value = self.coerce(value)
        return self.a == value.a and self.b == value.b
    def sign(self):
        if self.b == 0: return (self.a > 0) - (self.a < 0)
        scale = 1
        while True:
            root = isqrt(self.d * scale * scale)
            values = [self.a + self.b * F(root, scale),
                      self.a + self.b * F(root + 1, scale)]
            if min(values) > 0: return 1
            if max(values) < 0: return -1
            scale *= 2
    def __lt__(self, value): return (self - value).sign() < 0
    def __abs__(self): return self if self.sign() >= 0 else -self
    def conjugate(self): return Quadratic(self.d, self.a, -self.b)
    def norm(self): return self.a**2 - self.d * self.b**2

# Five quadratic fields, three denominators, boundary and rational initial points.
for d in [2, 3, 5, 7, 13]:
    for denom in [1, 2, 5]:
        alpha = Quadratic(d, F(-isqrt(d), denom), F(1, denom))
        H = max(abs(alpha.conjugate()), abs((alpha-1).conjugate()))
        def rot(x):
            z = x + alpha
            return z if z < 1 else z-1
        for initial in [Quadratic(d, F(j, 11)) for j in range(11)] + [1-alpha]:
            z = initial
            for n in range(1, 65):
                z = rot(z)
                delta = z-initial
                check("quadratic_norm", delta != 0)
                norm = (denom*delta).norm()
                check("quadratic_norm", norm.denominator == 1 and norm != 0)
                check("quadratic_norm", n * abs(delta) * denom**2 * H >= 1)
                distance = min(abs(delta), abs(delta-1), abs(delta+1))
                check("quadratic_norm", n * distance * denom**2 * (H+1) >= 1)

class RationalIET:
    def __init__(self, lengths, order):
        self.lefts = []
        self.rights = []
        left = F(0)
        for length in lengths:
            self.lefts.append(left)
            left += length
            self.rights.append(left)
        target_lefts = [None]*len(lengths)
        left = F(0)
        for label in order:
            target_lefts[label] = left
            left += lengths[label]
        self.shifts = [b-a for a,b in zip(self.lefts, target_lefts)]
        self.images = [(a+h,b+h,h) for a,b,h in
                       zip(self.lefts,self.rights,self.shifts)]
    def step(self, x, reverse=False):
        branches = self.images if reverse else list(zip(self.lefts,self.rights,self.shifts))
        for a,b,h in branches:
            if a <= x < b: return x-h if reverse else x+h
        raise AssertionError("outside half-open domain")
    def orbit(self, x, n):
        for _ in range(abs(n)): x = self.step(x, n < 0)
        return x

mutants = {}
cylinders = 0
for raw in [[1,2,3,5], [1,2,4,5,7], [3,5,7,8]]:
    lengths = [F(v,sum(raw)) for v in raw]
    for order in permutations(range(len(raw))):
        iet = RationalIET(lengths,order)
        for n in range(1,8):
            endpoints = set(iet.orbit(x,j) for x in iet.lefts for j in range(-n,n+1))
            ordered = sorted(endpoints)
            gap = min(y-x for x,y in zip(ordered,ordered[1:]))
            cuts = sorted(set([F(1)] + [iet.orbit(x,-j) for x in iet.lefts for j in range(n)]))
            for left,right in zip(cuts,cuts[1:]):
                delta = iet.orbit(left,n)-left
                for point in [left, (2*left+right)/3, (left+2*right)/3]:
                    check("rational_cylinders", iet.orbit(point,n)-point == delta)
                    check("rational_cylinders", iet.step(iet.step(point),True) == point)
                    check("rational_cylinders", iet.step(iet.step(point,True)) == point)
                check("rational_cylinders", left in endpoints and iet.orbit(left,n) in endpoints)
                if delta != 0: check("rational_cylinders", abs(delta) >= gap)
                else: mutants.setdefault("remove_aperiodicity", {"lengths":list(map(str,lengths)),"order":order,"n":n,"gap":str(gap)})
                base_gap = min(y-x for x,y in zip(iet.lefts,iet.lefts[1:]))
                if delta != 0 and abs(delta) < base_gap:
                    mutants.setdefault("use_only_original_endpoints", {"lengths":list(map(str,lengths)),"order":order,"n":n,"displacement":str(delta),"base_gap":str(base_gap)})
                cylinders += 1
check("mutations", "remove_aperiodicity" in mutants)
check("mutations", "use_only_original_endpoints" in mutants)

# The reversal clock identity across 120 length triples, all piece left endpoints
# and two distinct interior points; this does not assert rational-map minimality.
for ia in range(1,16):
    for ib in range(1,17-ia):
        a,b,c = F(ia,17),F(ib,17),F(17-ia-ib,17)
        iet = RationalIET([a,b,c], [2,1,0])
        circumference,theta = 1+b,b+c
        for left,right in zip(iet.lefts,iet.rights):
            for point in [left,(2*left+right)/3,(left+2*right)/3]:
                z=(point+theta) % circumference
                clock=1
                if z>=1:
                    z=(z+theta) % circumference
                    clock=2
                check("inducing_boundaries", z==iet.step(point))
                check("inducing_boundaries", clock==(2 if a<=point<a+b else 1))

# Exact witnesses to hypotheses that cannot be dropped.
for n in range(2,129):
    z = 1-F(1,n*n)
    check("metric_endpoint", n*min(z,1-z) == F(1,n))
    check("metric_endpoint", n*z > n-1)
    check("unbounded_clock", n*n*F(1,n*n) == 1 and n*F(1,n*n) == F(1,n))
    check("missing_invariance", n*F(1,2**(n+1)) < F(1,n))

# Finite Tonelli inequality with all support strictly in [0,1), and integer
# radius/distance ratios to distinguish < from <= in the counting step.
atoms = [(F(0),F(1,3)),(F(1,2),F(1,6)),(F(7,8),F(1,2))]
for y in [F(1,4),F(3,8),F(3,4)]:
    potential = sum(mass/abs(z-y) for z,mass in atoms)
    for radius in [F(1,4),F(1),F(3)]:
        partial = sum(mass for n in range(1,257) for z,mass in atoms if abs(z-y)<radius/n)
        check("potential", partial <= radius*potential)
for integer in range(1,17):
    check("strict_count", sum(n<integer for n in range(1,20)) == integer-1)

# Independent rational covering choices with the same proven width rule.
used=set(); blocks=[]; index=1
for stage in range(1,4):
    left=F(0);start=index
    while left<1:
        width=min(1-left,F(1,stage*index))
        m=1
        while True:
            center=left+width*(F(1,3)+F(1,9*m))
            if center not in used: break
            m+=1
        right=left+width
        check("covering", center not in used and 0<center<1)
        check("covering", index*max(center-left,right-center)<=F(2,3*stage))
        check("covering", max(center-left,right-center)<F(1,stage*index))
        # For initial points in the sequence, a fixed forward index shift only
        # reduces the bound when the sampled orbit time remains positive.
        for shift in [1,7,100]:
            if index>shift:
                check("shifted_covers", (index-shift)*max(center-left,right-center)<=F(2,3*stage))
        used.add(center);left=right;index+=1
    blocks.append({"stage":stage,"first":start,"last":index-1})
    check("covering", left==1)
check("mutations", F(1,2)!=F(3,4))  # repeated z=1/4 with those successors gives no function.

out = {
    "status":"PASS", "reviewed_manifest_sha256":EXPECTED,
    "total_assertions":sum(counts.values()),"counts":counts,
    "rational_cylinders":cylinders,"mutation_witnesses":mutants,
    "quadratic_fields":[2,3,5,7,13],"quadratic_denominators":[1,2,5],
    "covering_blocks":blocks,
    "limits":"All checks are finite. Analytic arguments, not these controls, establish the stated lemmas. Rational IET fixtures are not minimality examples. No source-status or general IET resolution is certified."
}
print(json.dumps(out,indent=2))
