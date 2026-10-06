"""Fresh exact PR126 algebra audit; no prior verifier code used.

All guards remain enabled under -O. Writes only this script's directory.
Finite checks are corroboration; INDEPENDENT_PROOF.md supplies the proof.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import itertools

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT.parent / "original_head_authentication_20261006" / "original_attempt"
A = ((3, 1), (2, 1))
B = ((1, -2), (-1, 3))
C = ((8, -11), (3, -4))
I = ((1, 0), (0, 1))
X = ((0, 1), (-1, 0))
Y = ((-2, -1), (3, 1))

def require(value, reason):
    if not value:
        raise RuntimeError(reason)

def mul(m, n, p=None):
    out = tuple(tuple(sum(m[i][k] * n[k][j] for k in range(2))
                      for j in range(2)) for i in range(2))
    return out if p is None else tuple(tuple(z % p for z in r) for r in out)

def det(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]

def inv(m, p=None):
    require(det(m) == 1 if p is None else det(m) % p == 1, "SL2 inverse requires determinant one")
    out = ((m[1][1], -m[0][1]), (-m[1][0], m[0][0]))
    return out if p is None else tuple(tuple(z % p for z in r) for r in out)

def triple(m, n, p=None):
    return mul(mul(m, n, p), m, p)

def qadd(a, b):
    return (a[0] + b[0], a[1] + b[1])

def qmul(a, b):
    return (a[0] * b[0] + 3 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])

def qscale(a, z):
    return (a[0] * z, a[1] * z)

def row_mul(v, m):
    return tuple(qadd(qscale(v[0], m[0][j]), qscale(v[1], m[1][j])) for j in range(2))

def column_mul(m, v):
    return tuple(qadd(qscale(v[0], m[i][0]), qscale(v[1], m[i][1])) for i in range(2))

def original_hashes():
    return [{"path": str(f.relative_to(ORIGINAL)), "bytes": f.stat().st_size,
             "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
            for f in sorted(ORIGINAL.rglob("*")) if f.is_file()]

before = original_hashes()
require(len(before) == 16, "immutable original file count must be 16")
records = {}
matrices = {"A": A, "B": B, "C": C}
require(len(set(matrices.values())) == 3, "matrices must be distinct")
lam = (2, 1)
lam_inv = (2, -1)
require(qmul(lam, lam_inv) == (1, 0), "exact reciprocal eigenvalues")
for name, m in matrices.items():
    require(det(m) == 1, name + " determinant")
    require(m[0][0] + m[1][1] == 4, name + " trace")
    require(mul(m, inv(m)) == I and mul(inv(m), m) == I, name + " integral two-sided inverse")
    a, b = m[0]
    v_expand = ((b, 0), (2 - a, 1))
    v_contract = ((b, 0), (2 - a, -1))
    ell_s = ((2 - a, -1), (-b, 0))
    ell_u = ((2 - a, 1), (-b, 0))
    require(column_mul(m, v_expand) == tuple(qmul(lam, v) for v in v_expand), name + " expanding eigenvector")
    require(column_mul(m, v_contract) == tuple(qmul(lam_inv, v) for v in v_contract), name + " contracting eigenvector")
    require(row_mul(ell_s, m) == tuple(qmul(lam, v) for v in ell_s), name + " expanding transverse covector")
    require(row_mul(ell_u, m) == tuple(qmul(lam_inv, v) for v in ell_u), name + " contracting transverse covector")
    require(qadd(qmul(ell_s[0], v_contract[0]), qmul(ell_s[1], v_contract[1])) == (0, 0), name + " stable covector annihilation")
    require(qadd(qmul(ell_u[0], v_expand[0]), qmul(ell_u[1], v_expand[1])) == (0, 0), name + " unstable covector annihilation")
    records[name] = {"matrix": m, "determinant": det(m), "trace": 4,
                     "expanding_eigenvector_Qsqrt3": v_expand,
                     "contracting_eigenvector_Qsqrt3": v_contract,
                     "stable_foliation_transverse_covector_Qsqrt3": ell_s,
                     "unstable_foliation_transverse_covector_Qsqrt3": ell_u}

require(mul(mul(A, B), inv(A)) == C, "C=A B A^-1")
require(mul(mul(inv(B), A), B) == C, "C=B^-1 A B")
pair_products = {}
for left, right in itertools.combinations(matrices, 2):
    m, n = matrices[left], matrices[right]
    require(triple(m, n) == triple(n, m), left + right + " braid")
    require(mul(m, n) != mul(n, m), left + right + " noncommutation")
    pair_products[left + right] = {"braid_common": triple(m, n), "left_product": mul(m, n), "right_product": mul(n, m)}
require(mul(X, X) == ((-1, 0), (0, -1)), "X^2=-I")
require(mul(mul(Y, Y), Y) == I, "Y^3=I")
require(mul(X, Y) == A and mul(Y, X) == B, "source pair mechanism")

finite_torus_points = 0
for q in (2, 3, 5, 7, 11, 13):
    for point in itertools.product(range(q), repeat=2):
        def action(m, point):
            return tuple(sum(m[i][j] * point[j] for j in range(2)) % q for i in range(2))
        for m, n in itertools.combinations(matrices.values(), 2):
            require(action(m, action(n, action(m, point))) == action(n, action(m, action(n, point))), "finite torus braid")
        finite_torus_points += 1

finite_group_records = []
for p in (2, 3, 5):
    group = [((a, b), (c, d)) for a, b, c, d in itertools.product(range(p), repeat=4) if (a * d - b * c) % p == 1]
    require(len(group) == p * (p * p - 1), "SL2 finite group cardinality")
    distinct_braid_pairs = 0
    commuting_braid_pairs = 0
    for a, b in itertools.product(group, repeat=2):
        if triple(a, b, p) != triple(b, a, p):
            continue
        if mul(a, b, p) == mul(b, a, p):
            commuting_braid_pairs += 1
            require(a == b, "commuting braid pair must coincide")
        if a == b:
            continue
        distinct_braid_pairs += 1
        c = mul(mul(a, b, p), inv(a, p), p)
        require(c == mul(mul(inv(b, p), a, p), b, p), "finite group conjugacy formula")
        require(len({a, b, c}) == 3, "finite group triple distinctness")
        for u, v in itertools.combinations((a, b, c), 2):
            require(triple(u, v, p) == triple(v, u, p), "finite group triple braid")
            require(mul(u, v, p) != mul(v, u, p), "finite group triple noncommutation")
    finite_group_records.append({"prime": p, "group_order": len(group),
                                 "ordered_pairs_examined": len(group) ** 2,
                                 "distinct_braid_pairs": distinct_braid_pairs,
                                 "commuting_braid_pairs": commuting_braid_pairs})

mutated_C = ((8, -11), (4, -4))
require(det(mutated_C) != 1, "negative control catches perturbed determinant")
require(triple(A, mutated_C) != triple(mutated_C, A), "negative control catches perturbed braid")
require(triple(B, mutated_C) != triple(mutated_C, B), "second negative control catches perturbed braid")
guard_rejected = False
try:
    require(False, "deliberate false guard")
except RuntimeError:
    guard_rejected = True
require(guard_rejected, "explicit guard must reject false claim")
after = original_hashes()
require(before == after, "original artifacts must remain unchanged")
result = {"schema": "pr126-independent-algebra-audit/v1",
          "UTC": datetime.now(timezone.utc).isoformat(), "actual_operator_PID": os.getpid(),
          "immutable_submitted_head": "a1df84a64fa96d53f3a8c6fec9db8bc48bd1533c",
          "original_budget": "1/5", "new_central_proof_search_turns": 0,
          "PASS": True, "matrices": records, "pair_products": pair_products,
          "finite_torus_points_all_three_pairs": finite_torus_points,
          "finite_group_tests": finite_group_records,
          "negative_control_rejection": True,
          "original_hashes_before_after_equal": True,
          "original_file_hashes": before,
          "scope": "exact group and matrix identities; measured-foliation covectors; corroborating finite checks; proof in INDEPENDENT_PROOF.md; primary source acceptance and historical priority remain separate"}
(ROOT / "independent_result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"PASS": True, "UTC": result["UTC"], "PID": os.getpid(), "finite_torus_points": finite_torus_points, "finite_group_tests": finite_group_records}))
