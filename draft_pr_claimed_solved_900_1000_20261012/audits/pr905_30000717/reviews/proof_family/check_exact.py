#!/usr/bin/env python3
"""Independent exact finite controls; only Python standard library.

No author/audit program or output is imported. All polynomial coefficients and
matrix operations are integers or Fractions. Universal SOS impossibility is a
written deduction in AUDIT.md, not the output of a bounded search.
"""
from fractions import Fraction as F
from itertools import permutations, product
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ARCHIVE_PACKET = ROOT / "original_packet"
ORIGINAL = (ARCHIVE_PACKET if ARCHIVE_PACKET.is_dir() else
            ROOT / "original" / "unsolved_math_prioritization" / "attempts" / "30000717")
EXPECTED_PROOF_SHA256 = "a2e2109d45f7776103fc43cff554c7f49de1b9290b92dc62b3d3db5ad23050c1"
checks = []


def check(label, truth):
    if not truth:
        raise RuntimeError("FAILED: " + label)
    checks.append(label)


PROOF_PATH = ORIGINAL / "author" / "PROOF.md"
check("fixed candidate proof file exists", PROOF_PATH.is_file())
PROOF_SHA256 = hashlib.sha256(PROOF_PATH.read_bytes()).hexdigest()
check("fixed candidate proof hash matches", PROOF_SHA256 == EXPECTED_PROOF_SHA256)


def clean(p):
    return {tuple(k): F(v) for k, v in p.items() if v}


def add(*ps):
    out = {}
    for p in ps:
        for k, v in p.items():
            out[k] = out.get(k, F(0)) + v
    return clean(out)


def scale(p, c):
    return clean({k: v * c for k, v in p.items()})


def mul(p, q):
    out = {}
    for k, v in p.items():
        for l, w in q.items():
            e = tuple(a + b for a, b in zip(k, l))
            out[e] = out.get(e, F(0)) + v * w
    return clean(out)


def const(c, n):
    return clean({(0,) * n: c})


def var(i, n):
    return {tuple(int(j == i) for j in range(n)): F(1)}


def power(p, n):
    if not p:
        return {} if n else {(0, 0, 0): F(1)}
    ans = const(1, len(next(iter(p))))
    for _ in range(n):
        ans = mul(ans, p)
    return ans


def diff(p, i):
    out = {}
    for k, v in p.items():
        if k[i]:
            e = list(k)
            e[i] -= 1
            out[tuple(e)] = v * k[i]
    return clean(out)


def evaluate(p, v):
    return sum((c * product_scalar([F(a) ** e for a, e in zip(v, k)])
                for k, c in p.items()), F(0))


def product_scalar(items):
    ans = F(1)
    for item in items:
        ans *= item
    return ans


def restrict_line(p, v):
    out = {}
    for k, c in p.items():
        d = sum(k)
        out[d] = out.get(d, F(0)) + c * product_scalar([F(a) ** e for a, e in zip(v, k)])
    return {d: c for d, c in out.items() if c}


def laurent_xy(p):
    # Exact substitution x=t^(-1), y=t. Exponents may be negative.
    out = {}
    for (a, b), c in p.items():
        d = b - a
        out[d] = out.get(d, F(0)) + c
    return {d: c for d, c in out.items() if c}


def permute(p, perm):
    out = {}
    for k, c in p.items():
        e = [0] * len(k)
        for i, d in enumerate(k):
            e[perm[i]] = d
        out[tuple(e)] = c
    return clean(out)


def exponents(n, d):
    if n == 1:
        return [(d,)]
    return [(i,) + e for i in range(d + 1) for e in exponents(n - 1, d - i)]


def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = a[r][c]
        a[r] = [v / z for v in a[r]]
        for i in range(len(a)):
            if i != r:
                z = a[i][c]
                a[i] = [u - z * v for u, v in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def determinant(matrix):
    a = [[F(x) for x in row] for row in matrix]
    ans = F(1)
    for c in range(len(a)):
        pivot = next((i for i in range(c, len(a)) if a[i][c]), None)
        if pivot is None:
            return F(0)
        if pivot != c:
            a[c], a[pivot] = a[pivot], a[c]
            ans *= -1
        z = a[c][c]
        ans *= z
        for i in range(c + 1, len(a)):
            factor = a[i][c] / z
            a[i] = [u - factor * v for u, v in zip(a[i], a[c])]
    return ans


def evaluation_matrix(z, monos):
    return [[product_scalar([F(a) ** e for a, e in zip(v, k)]) for k in monos] for v in z]


x, y, z = [var(i, 3) for i in range(3)]
vs = [x, y, z]
R = add(*(power(v, 6) for v in vs),
        *(scale(mul(power(vs[i], 4), power(vs[j], 2)), -1)
          for i in range(3) for j in range(3) if i != j),
        scale(mul(mul(power(x, 2), power(y, 2)), power(z, 2)), 3))
check("sextic support has ten terms", len(R) == 10)
check("all Robinson monomials degree six", all(sum(k) == 6 for k in R))
for perm in permutations(range(3)):
    check("coordinate symmetry " + str(perm), permute(R, perm) == R)
for signs in product((-1, 1), repeat=3):
    signed = clean({k: c * product_scalar([F(s) ** e for s, e in zip(signs, k)]) for k, c in R.items()})
    check("sign symmetry " + str(signs), signed == R)

# Same polynomial operations, with x,y,z now standing for a,b,c.
Fabc = add(*(power(v, 3) for v in vs),
           *(scale(mul(power(vs[i], 2), vs[j]), -1)
             for i in range(3) for j in range(3) if i != j),
           scale(mul(mul(x, y), z), 3))
decomp = add(mul(power(add(x, scale(y, -1)), 2), add(x, y, scale(z, -1))),
             mul(mul(z, add(x, scale(z, -1))), add(y, scale(z, -1))))
check("Schur decomposition exact", Fabc == decomp)
check("substitution a=x^2,b=y^2,c=z^2", {(2*a, 2*b, 2*c): q for (a,b,c), q in Fabc.items()} == R)

grad = [diff(R, i) for i in range(3)]
gx_formula = scale(mul(x, add(scale(power(x, 4), 3),
    scale(mul(power(x, 2), power(y, 2)), -2), scale(power(y, 4), -1),
    scale(mul(power(x, 2), power(z, 2)), -2), scale(power(z, 4), -1),
    scale(mul(power(y, 2), power(z, 2)), 3))), 2)
check("explicit x derivative", grad[0] == gx_formula)
check("Euler identity", add(*(mul(vs[i], grad[i]) for i in range(3))) == scale(R, 6))
K = [mul(vs[j], grad[i]) for i in range(3) for j in range(3) if i != j]
J = [add(mul(vs[j], grad[i]), scale(mul(vs[i], grad[j]), -1))
     for i in range(3) for j in range(i + 1, 3)]

# Derive the directions independently from the 13 sign-normalized cube directions.
cube_directions = []
for v in product((-1, 0, 1), repeat=3):
    if v != (0, 0, 0) and next(c for c in v if c) == 1:
        cube_directions.append(v)
zero_directions = [v for v in cube_directions if evaluate(R, v) == 0]
author_Z = [(1,1,1), (1,1,-1), (1,-1,1), (1,-1,-1),
            (1,1,0), (1,-1,0), (1,0,1), (1,0,-1), (0,1,1), (0,1,-1)]
check("13 normalized cube directions", len(cube_directions) == 13)
check("ten zero directions independently recovered", set(zero_directions) == set(author_Z))
for v in zero_directions:
    check("entire zero line R " + str(v), restrict_line(R, v) == {})
    for i, g in enumerate(grad):
        check("entire zero line derivative " + str((v, i)), restrict_line(g, v) == {})
    for name, gens in (("J", J), ("K", K)):
        check("all ideal generators on line " + name + str(v), all(restrict_line(g, v) == {} for g in gens))
axis = (1, 0, 0)
check("axis R=t^6", restrict_line(R, axis) == {6: F(1)})
check("axis gradient", [restrict_line(g, axis) for g in grad] == [{5: F(6)}, {}, {}])
check("axis in J variety", all(restrict_line(g, axis) == {} for g in J))
check("axis in K variety", all(restrict_line(g, axis) == {} for g in K))

rank_results = []
for d in range(5):
    monos = exponents(3, d)
    r = rank(evaluation_matrix(zero_directions, monos))
    rank_results.append({"degree": d, "dimension": len(monos), "rank": r})
    check("evaluation rank degree " + str(d), r == [1, 3, 6, 10, 10][d])
author_monos = [(0,0,3), (0,1,2), (0,2,1), (0,3,0), (1,0,2),
                (1,1,1), (1,2,0), (2,0,1), (2,1,0), (3,0,0)]
det = determinant(evaluation_matrix(author_Z, author_monos))
check("author ordered determinant is -128", det == -128)

pair_Z = [v for v in zero_directions if 0 in v]
kernel_basis = [mul(vs[i], add(power(vs[i], 2),
    *(scale(power(vs[j], 2), -1) for j in range(3) if j != i))) for i in range(3)]
kernel_basis.append(mul(mul(x, y), z))
check("six paired directions have cubic rank six", rank(evaluation_matrix(pair_Z, author_monos)) == 6)
check("four proposed cubics vanish at paired directions", all(evaluate(p,v)==0 for p in kernel_basis for v in pair_Z))
coefficient_columns = [[p.get(k, F(0)) for p in kernel_basis] for k in author_monos]
check("four cubic kernel vectors independent", rank(coefficient_columns) == 4)
full_Z = [v for v in zero_directions if 0 not in v]
check("remaining sign-character evaluation invertible", rank([[evaluate(p,v) for p in kernel_basis] for v in full_Z]) == 4)

# Independent stencil: axis evaluation for degrees <=3 uses only eight lines.
# The two representatives with x=0 have zero weights.
axis_weights = [F(-1,4)] * 4 + [F(1,2)] * 4 + [F(0)] * 2
for d in range(4):
    for k in exponents(3, d):
        stencil = sum((w * product_scalar([F(a)**e for a,e in zip(vv,k)])
                       for w,vv in zip(axis_weights,author_Z)), F(0))
        axis_eval = product_scalar([F(a)**e for a,e in zip(axis,k)])
        check("independent axis interpolation monomial " + str(k), stencil == axis_eval)

# Counterfactual controls: these pass by demonstrating why shortcuts fail.
quartic = mul(add(power(x,2), scale(power(y,2), -1)),
              add(power(x,2), power(y,2), scale(power(z,2), -1)))
check("degree-four nonzero witness vanishes at ten directions", quartic != {} and all(evaluate(quartic,v)==0 for v in zero_directions))
check("degree-four witness has t^4 axis trace", restrict_line(quartic, axis) == {4:F(1)})
sample_only = mul(add(x, const(-1,3)), add(y, const(-1,3)))
check("finite representatives admit nonhomogeneous quadratic", all(evaluate(sample_only,v)==0 for v in author_Z))
check("quadratic fails whole-line vanishing", restrict_line(sample_only,(1,1,1)) == {2:F(1),1:F(-2),0:F(1)})

# Q is checked with an independent two-variable construction.
u, v = [var(i,2) for i in range(2)]
one_minus_uv = add(const(1,2), scale(mul(u,v),-1))
Q = add(power(one_minus_uv,2), power(v,2), const(F(-1,2),2))
Qx, Qy = diff(Q,0), diff(Q,1)
A, B = mul(v,Qx), mul(u,Qy)
check("Q first literal generator", A == scale(mul(power(v,2),add(mul(u,v),const(-1,2))),2))
check("Q second literal generator", B == scale(mul(u,add(mul(u,add(mul(u,v),const(-1,2))),v)),2))
check("Q origin value", evaluate(Q,(0,0)) == F(1,2))
check("Q negative rational value", evaluate(Q,(2,F(1,2))) == F(-1,4))
check("literal y=0 branch second generator=-2x^2", restrict_line(B,(1,0)) == {2:F(-2)})
check("literal xy=1 branch second generator=2", laurent_xy(B) == {0:F(2)})
check("nonattaining path exact", laurent_xy(Q) == {2:F(1),0:F(-1,2)})
check("Q+1/2 squares identity", add(Q,const(F(1,2),2)) == add(power(one_minus_uv,2),power(v,2)))

# A negative tangency value makes the separation from the product example explicit.
# x^2=44/15, y=x/4, so xy=11/15 and y^2=11/60.
aa, bb, uv = F(44,15), F(11,60), F(11,15)
check("negative tangent witness coordinate consistency", aa*bb == uv**2 and bb == aa/F(16))
check("negative tangent witness minors zero", (bb-aa)*(uv-1)-uv == 0)
q_tangent = (1-uv)**2 + bb - F(1,2)
check("Q tangent negative value", q_tangent == F(-221,900))

results = {
    "verdict": "all independent finite exact controls passed",
    "checked_candidate_proof_sha256": PROOF_SHA256,
    "check_count": len(checks),
    "arithmetic": "Python standard-library exact integers and fractions; no floating point",
    "imports_candidate_programs_or_results": False,
    "degree_ranks": rank_results,
    "author_ordered_cubic_determinant": int(det),
    "independent_axis_interpolation_weights_author_Z_order": [str(w) for w in axis_weights],
    "independently_recovered_zero_directions": zero_directions,
    "sharpness_witness": "(x^2-y^2)(x^2+y^2-z^2): zero on ten lines and t^4 on the extra axis",
    "representatives_only_witness": "(x-1)(y-1): zero at ten representatives, nonconstant on their lines",
    "Q_negative_tangency_value": str(q_tangent),
    "universal_argument_location": "AUDIT.md",
    "finite_checks_are_not_universal_SOS_search": True,
    "checks": checks,
}
(HERE / "RESULTS.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps({"checks":len(checks), "determinant":int(det), "ranks":rank_results,
                  "result":"PASS", "output":str(HERE / "RESULTS.json")}, indent=2))
