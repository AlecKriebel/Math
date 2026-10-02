#!/usr/bin/env python3
"""Independent integral diagnostics, using stdlib only; no topology theorem test.

Mechanisms: tensor cellular cochains, an integral Whitney-class algebra, exact
minor gcds, and the long-exact-sequence lattice of the homogeneous frame space.
No original checker is imported. Run with --mutant ordinary_c2 for the preserved
expected-failure harness. The mathematical proof is in REPORT.md.
"""
import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from math import gcd

CHECKS = []
MUTANTS = []

def check(condition, label):
    assert condition, label
    CHECKS.append(label)

def reject(name, correct, wrong, witness):
    check(correct != wrong, "reject mutant: " + name)
    MUTANTS.append({"name": name, "correct": correct, "mutant": wrong, "witness": witness})

def det(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    a = [[Fraction(v) for v in row] for row in matrix]
    out = Fraction(1)
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[pivot], a[col] = a[col], a[pivot]
            out = -out
        v = a[col][col]
        out *= v
        for r in range(col + 1, n):
            factor = a[r][col] / v
            for j in range(col + 1, n):
                a[r][j] -= factor * a[col][j]
            a[r][col] = 0
    assert out.denominator == 1
    return int(out)

def coker(matrix, rows=None):
    """Integer invariant factors via gcd of all minors; exact, not nullspaces."""
    n = len(matrix) if rows is None else rows
    m = len(matrix[0]) if matrix else 0
    divisors = [1]
    for size in range(1, min(n, m) + 1):
        d = 0
        for rs in combinations(range(n), size):
            for cs in combinations(range(m), size):
                d = gcd(d, abs(det([[matrix[r][c] for c in cs] for r in rs])))
        if d == 0:
            break
        assert d % divisors[-1] == 0
        divisors.append(d)
    factors = [divisors[i] // divisors[i-1] for i in range(1, len(divisors))]
    return {"free_rank": n - len(factors), "torsion": [v for v in factors if v > 1]}

def tensor_rp_circle_cochains(circles, relative_last=False):
    """RP2 cellular differential 1* -> 2(2*) tensor circle complexes.

    Cell tuples carry degrees; the parameter-relative subcomplex has last=1.
    Differential signs come from the preceding tensor degrees, not a hardcoded
    presentation. Only the RP2 factor has a nonzero differential here.
    """
    cells = list(product(range(3), *([range(2)] * circles)))
    if relative_last:
        cells = [c for c in cells if c[-1] == 1]
    by_degree = {d: [c for c in cells if sum(c) == d] for d in range(circles + 3)}
    ds = {}
    for degree, src in by_degree.items():
        dst = by_degree.get(degree + 1, [])
        matrix = [[0 for _ in src] for _ in dst]
        for j, cell in enumerate(src):
            if cell[0] == 1:
                target = (2,) + cell[1:]
                matrix[dst.index(target)][j] = 2
        ds[degree] = matrix
    # In this actual differential every nonzero column has one distinct target.
    # The kernel is therefore exactly the coordinate sublattice of zero columns.
    groups = {}
    for degree, src in by_degree.items():
        d = ds[degree]
        kernel = [j for j in range(len(src)) if all(not row[j] for row in d)]
        previous = ds.get(degree - 1, [])
        relations = [previous[j] for j in kernel] if previous else [[] for _ in kernel]
        groups[degree] = coker(relations, rows=len(kernel))
        for target_j, cell in enumerate(src):
            if cell[0] == 1 and previous:
                check(all(v == 0 for v in previous[target_j]), "tensor differential squared zero at " + str(cell))
    return by_degree, ds, groups

class RPRing:
    """H*(RP2;Z) tensor exterior circle generators, truncated by actual cells.

    Monomial (b_exponent, circle_mask): b has degree2 and order2, b²=0;
    circle degree1 generators anticommute and square to zero. This ring records
    torsion integrally, independently of the cochain differential computation.
    """
    def __init__(self, circles):
        self.circles = circles

    def norm(self, a):
        out = {}
        for (b, mask), coefficient in a.items():
            if b > 1:
                continue
            coefficient = coefficient % 2 if b else coefficient
            if coefficient:
                out[(b, mask)] = coefficient
        return out

    def add(self, *args):
        out = {}
        for a in args:
            for monomial, coefficient in a.items():
                out[monomial] = out.get(monomial, 0) + coefficient
        return self.norm(out)

    def scale(self, a, n):
        return self.norm({key: n*v for key, v in a.items()})

    def mul(self, a, b):
        out = {}
        for (eb, mb), cb in a.items():
            for (ed, md), cd in b.items():
                if mb & md or eb + ed > 1:
                    continue
                inversions = sum(1 for i in range(self.circles) for j in range(self.circles)
                                 if mb >> i & 1 and md >> j & 1 and i > j)
                key = (eb + ed, mb | md)
                out[key] = out.get(key, 0) + cb*cd*(-1)**inversions
        return self.norm(out)

    def chern(self, lines):
        """Multiply total Chern polynomials, retain c1/c2 only."""
        out = [{(0,0): 1}, {}, {}]
        for root in lines:
            out = [out[0], self.add(out[1], root),
                   self.add(out[2], self.mul(out[1], root))]
        return out

    def virtual(self, numerator, denominator):
        c = self.chern(numerator)
        e = self.chern(denominator)
        # Formal inverse of 1+e1+e2 through Chern degree2, no division.
        inv = [e[0], self.scale(e[1], -1),
               self.add(self.mul(e[1], e[1]), self.scale(e[2], -1))]
        return [c[0], self.add(c[1], inv[1]),
                self.add(c[2], self.mul(c[1], inv[1]), inv[2])]

class Polynomial:
    """Sparse Z[x,y,p,q,epsilon]/epsilon²; no symbolic library or rationals.

    Epsilon represents the circle direction AFTER computing line-loop classes
    h*t (even degree2), so these line roots commute. Only epsilon coefficients
    are used. Identities proven here are integer polynomial identities, hence
    retain their coefficients under torsion specialization.
    """
    zero = (0,0,0,0,0)

    @staticmethod
    def add(*args):
        out = {}
        for a in args:
            for key, value in a.items():
                out[key] = out.get(key, 0) + value
        return {key:value for key,value in out.items() if value}

    @staticmethod
    def scale(a, n):
        return {key:n*v for key,v in a.items() if n*v}

    @staticmethod
    def mul(a, b):
        out = {}
        for key, value in a.items():
            for other, coefficient in b.items():
                combined = tuple(v+w for v,w in zip(key, other))
                if combined[4] > 1:
                    continue
                out[combined] = out.get(combined, 0) + value*coefficient
        return {key:value for key,value in out.items() if value}

    @classmethod
    def var(cls, n):
        key = list(cls.zero)
        key[n] = 1
        return {tuple(key): 1}

    @classmethod
    def chern(cls, lines):
        out = [{cls.zero:1}, {}, {}]
        for root in lines:
            out = [out[0], cls.add(out[1], root), cls.add(out[2], cls.mul(out[1], root))]
        return out

    @classmethod
    def virtual(cls, lines, base):
        v, e = cls.chern(lines), cls.chern(base)
        return [v[0], cls.add(v[1], cls.scale(e[1], -1)),
                cls.add(v[2], cls.scale(cls.mul(v[1], e[1]), -1),
                        cls.mul(e[1], e[1]), cls.scale(e[2], -1))]

    @classmethod
    def slant(cls, a):
        return {key[:4]+(0,):v for key,v in a.items() if key[4] == 1}

    @classmethod
    def evaluate(cls, a, x, y, p, q):
        return sum(coef*x**key[0]*y**key[1]*p**key[2]*q**key[3]
                   for key,coef in a.items() if key[4] == 0)

def generic_nontrivial_e(mutant=False):
    cells, ds, full = tensor_rp_circle_cochains(2)
    rcells, rds, relative = tensor_rp_circle_cochains(2, relative_last=True)
    check(full[2] == {"free_rank":1,"torsion":[2]}, "RP2 times two circles H2 integral")
    check(full[4] == {"free_rank":0,"torsion":[2]}, "RP2 times two circles H4 integral")
    check(relative[2] == {"free_rank":1,"torsion":[]}, "parameter-relative H2 is integral H1(M)")
    check(relative[4] == {"free_rank":0,"torsion":[2]}, "parameter-relative H4 is torsion H3(M)")
    top = cells[4].index((2,1,1))
    previous = ds[3][top]
    check(gcd(*previous) == 2, "b*x*t is nonzero modulo actual integral coboundaries")
    check(rcells[4] == cells[4] and gcd(*rds[3][0]) == gcd(*previous),
          "relative top cell and relation ideal agree with the absolute class")
    ring = RPRing(2)
    b, x, t = {(1,0):1}, {(0,1):1}, {(0,2):1}
    xt = ring.mul(x,t)
    numerator = [b, xt, {}]
    denominator = [b, {}, {}]
    ordinary = ring.chern(numerator)
    virtual = ring.virtual(numerator, denominator)
    check(ordinary[2] == {(1,3):1}, "actual ordinary c2(V) has the nonzero order-two term")
    check(virtual[1] == xt and virtual[2] == {}, "computed virtual Chern product cancels torsion cross term")
    check(ring.mul(xt,xt) == {}, "relative c1 square is zero because parameter-circle square is zero")
    if mutant:
        # This deliberately false assertion must exit nonzero; never label PASS.
        assert ordinary[2] == virtual[2], "EXPECTED_FAILURE: ordinary c2 is not the relative virtual coordinate on RP2 x S1"
    reject("ordinary_c2_instead_of_virtual", virtual[2], ordinary[2],
           "E=L_b+1+1; V=L_b+P_xt+1 on RP2 x S1_x x S1_parameter; H4=Z/2")
    # Both target loops and their sums have relative c1 containing t.
    plus = ring.virtual([b, ring.scale(xt, 2), {}], denominator)
    check(plus[1] == ring.scale(xt,2) and plus[2] == {}, "relative integral coordinates add, including torsion")
    return {"full_cohomology":full, "relative_cohomology":relative,
            "ordinary_c2_term":"b*x*t of order2", "virtual_c2":0}

def universal_whitney_polynomials():
    P = Polynomial
    x,y,p,q,e = [P.var(i) for i in range(5)]
    xs, hs = [x,y,P.scale(P.add(x,y),-1)], [p,q,P.scale(P.add(p,q),-1)]
    lines = [P.add(c,P.mul(h,e)) for c,h in zip(xs,hs)]
    roots = [P.add(xs[j],P.scale(xs[i],-1)) for i,j in ((0,1),(0,2),(1,2))]
    rloops = [P.add(hs[j],P.scale(hs[i],-1)) for i,j in ((0,1),(0,2),(1,2))]
    tangent = [P.add(c,P.mul(h,e)) for c,h in zip(roots,rloops)]
    a = P.scale(P.slant(P.chern(lines)[2]),-1)
    v = P.virtual(tangent,roots)
    k,b = P.slant(v[1]), P.scale(P.slant(v[2]),-1)
    expected_a = P.add(P.mul(P.add(P.scale(x,2),y),p),
                       P.mul(P.add(x,P.scale(y,2)),q))
    check(a == expected_a, "universal Whitney multiplication: SU loop coefficient")
    check(k == P.add(P.scale(p,-4),P.scale(q,-2)), "universal Whitney multiplication: determinant coefficient")
    check(b == P.scale(a,3), "universal virtual Whitney multiplication: root-index coefficient3")
    check(P.slant(P.chern(roots)[1]) == {}, "base bundle has no parameter coordinate")
    # This finite specialization is supplementary; the preceding exact identities
    # and the written proof explain why all torsion coefficients are valid.
    count = 0
    for modulus in (2,3,4,8,12):
        for xx,yy,pp,qq in product(range(-2,3),repeat=4):
            aa = P.evaluate(a,xx,yy,pp,qq)
            bb = P.evaluate(b,xx,yy,pp,qq)
            check((bb-3*aa)%modulus == 0, "torsion specialization " + str((modulus,xx,yy,pp,qq)))
            count += 1
    return {"integer_polynomial_identities":3,"supplementary_specializations":count}

def homogeneous_frame_and_action():
    # T2 -> SU3 x U3 -> (SU3 x U3)/T2.
    correct = coker([[-4,-2]])
    check(correct == {"free_rank":0,"torsion":[2]}, "homogeneous frame target fundamental group Z/2")
    check(-4*1-2*(-2) == 0 and gcd(1,2) == 1, "homogeneous frame pi2 generator (1,-2) is primitive")
    wrong_determinant = coker([[0,0],[-4,-2]])
    reject("replace_SU3_by_U3", correct, wrong_determinant,
           "M=open Mobius band x R is homotopy S1; free homotopies are conjugacy classes in pi1(frame target)")
    reject("missing_full_loop_action", correct, {"free_rank":1,"torsion":[]},
           "same M: fixed-f U3 determinant framings Z become Z/2 only after torus loops act")
    # Full coupled presentation on S2 x S1; quotient EACH coordinate separately
    # is a different and generally false operation.
    sphere = []
    for n in range(-20,21):
        original = [[0,-3*n],[-4,-2],[0,-9*n]]
        got = coker(original)
        if n:
            g = gcd(2,3*n)
            expected = {"free_rank":1,"torsion":[v for v in (g,12*abs(n)//g) if v>1]}
        else:
            expected = {"free_rank":2,"torsion":[2]}
        check(got == expected, "full coupled minors S2xS1 n="+str(n))
        # Integral row operation v -> v-3u kills BOTH image columns.
        changed = [[original[2][j]-3*original[0][j] for j in range(2)], original[1], original[0]]
        check(changed[0] == [0,0] and coker(changed) == got, "unimodular integral split n="+str(n))
        sphere.append({"n":n,**got})
    reject("independent_coordinate_quotients", coker([[0,-3],[-4,-2],[0,-9]]),
           {"free_rank":0,"torsion":[3,2,9]},
           "n=1 has a surviving free Z and Z/12; taking three separate images instead kills that free coordinate")
    reject("wrong_root_index2", coker([[0,-3],[-4,-2],[0,-9]]),
           coker([[0,-2],[-4,-2],[0,-4]]), "n=1 actual root-index3 gives Z plus Z/12, index2 gives Z plus Z/8")
    return {"circle_frame_group":correct,"sphere_product":sphere}

def existence_and_noncompact_controls():
    _,_,rp = tensor_rp_circle_cochains(1)
    check(rp[1] == {"free_rank":1,"torsion":[]} and rp[2] == {"free_rank":0,"torsion":[2]}
          and rp[3] == {"free_rank":0,"torsion":[2]}, "actual RP2xS1 cohomology has integral top torsion")
    reject("Koshkin_deRham_H3_zero", rp[3], {"free_rank":0,"torsion":[]},
           "RP2 x S1 cochain d in top degree is multiplication2, so H3=Z/2 rather than zero")
    indices = [(x,y) for x,y in product(range(2),repeat=2) if (-4*x-2*y-1)%2 == 0]
    check(indices == [], "actual RP2xS1 determinant delta=b obstructs existence")
    reject("rationalize_determinant_torsion", len(indices), 1,
           "rational B and delta vanish and falsely leave the zero label; integral delta is nonzero Z/2")
    # For an orientable lens space with p=2 the integer labels are four, while
    # rational cohomology would retain just the zero pair.
    lens = [(x,y) for x,y in product(range(2),repeat=2) if (-4*x-2*y)%2 == 0]
    reject("rationalize_primary_labels", len(lens), 1, "genuine lens space L(2,1), B=Z/2 and delta0")
    relators = ('aaaBAAAbbaaababb','aaabAAbbaaaBABAAAB')
    exps = lambda word,letter:word.count(letter)-word.count(letter.upper())
    relations = [[exps(r,c) for r in relators] for c in 'ab']
    check(coker(relations) == {"free_rank":1,"torsion":[4]}, "primary Reid relators abelianize to Z plus Z/4")
    check(all(sum(exps(r,c)*h for c,h in zip('ab',(-1,1)))==0 for r in relators), "Reid integral character (-1,1)")
    check(any(exps(r,'b') != 0 for r in relators) and all(exps(r,'b')%4==0 for r in relators),
          "Reid orientation (0,1) lifts modulo4 but is not an integral character")
    check(all(row[0] == row[1] and row[0] != 0 for row in zip(*relations)),
          "all Reid integral characters have equal generator parity, unlike orientation (0,1)")
    reid = [(x,y) for x,y in product(range(4),repeat=2) if (-4*x-2*y-2)%4 == 0]
    check(len(reid)==8 and all(y%2==1 for x,y in reid), "genuine nonzero divisible determinant delta2 admits eight labels")
    # Ordinary cohomology / homotopy type controls on noncompact actual domains.
    r3 = {"classes":1}
    mobius = {"fiber":coker([[-4,-2]]),"primary_labels":1}
    check(mobius['fiber'] == {"free_rank":0,"torsion":[2]}, "open Mobius x R retains exactly two classes")
    reject("compact_support_instead_of_ordinary", r3, {"fiber_free_rank":2},
           "R3 is contractible, while H_c^3(R3)=Z would incorrectly manufacture two Z coordinates")
    check(not any((-4*x-2*y-1)%2==0 for x,y in product(range(2),repeat=2)),
          "RP2xR noncompact nonorientable obstruction still excludes all labels")
    return {"RP2xS1":rp,"Reid_relation_matrix":relations,"Reid_labels":reid,
            "Reid_scope":"Published manifold identification and orientation character are inputs; relator algebra is independently checked. No cup table or hyperbolicity certification.",
            "R3":r3,"open_Mobius_times_R":mobius}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutant", choices=["ordinary_c2"])
    args = parser.parse_args()
    generic = generic_nontrivial_e(mutant=args.mutant == "ordinary_c2")
    universal = universal_whitney_polynomials()
    action = homogeneous_frame_and_action()
    existence = existence_and_noncompact_controls()
    # Only stringify torsion-ring dictionaries for JSON; integer computations are
    # already complete. Full labels are kept to identify every assertion.
    safe_mutants = []
    for item in MUTANTS:
        safe_mutants.append({k:repr(v) if isinstance(v,dict) and any(isinstance(j,tuple) for j in v) else v
                             for k,v in item.items()})
    result = {"pass":True,"assertions":len(CHECKS),"checks":CHECKS,
              "generic_nontrivial_E":generic,"whitney":universal,"action":action,
              "existence":existence,"rejected_mutants":safe_mutants,
              "scope":"Integral computation diagnostics supplement REPORT universal proof. No computation certifies stability, h-principle, homotopy-fiber equivalence, novelty, or future publication readiness."}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
