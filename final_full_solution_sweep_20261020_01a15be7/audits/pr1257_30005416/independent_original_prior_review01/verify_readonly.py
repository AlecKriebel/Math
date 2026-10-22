#!/usr/bin/env python3
"""Reviewer-authored, exact Q-linear algebra; no source code is executed.
Reads this folder only, writes no files, and performs no network/subprocess call.
Finite checks supplement the written all-weight arguments and primary theorems.
"""
from pathlib import Path
from functools import lru_cache
from collections import defaultdict
from math import gcd
import json
import hashlib

ROOT = Path(__file__).resolve().parent
P = ROOT / "private_sources"
N = 10
GUARDS = 0


def need(ok, why):
    global GUARDS
    GUARDS += 1
    if not ok:
        raise RuntimeError(why)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def wt(m):
    return sum(i // 3 + 1 for i in m)


@lru_cache(None)
def monomials(w, minimum=0):
    if w == 0:
        return ((),)
    return tuple((i,) + tail for i in range(minimum, 3 * w)
                 for tail in monomials(w - i // 3 - 1, i))


def pmul(a, b):
    c = defaultdict(int)
    for u, x in a.items():
        for v, y in b.items():
            m = tuple(sorted(u + v))
            if wt(m) <= N:
                c[m] += x * y
    return {m: v for m, v in c.items() if v}


def coefficient_equations(terms):
    """Terms are integer coefficient and three ordinary polynomial exponents."""
    F = defaultdict(int)
    variables = [{(3 * (j - 1) + a,): 1 for j in range(1, N + 1)} for a in range(3)]
    for c, powers in terms:
        r = {(): c}
        for a, e in enumerate(powers):
            for _ in range(e):
                r = pmul(r, variables[a])
        for m, v in r.items():
            F[m] += v
    out = {j: {} for j in range(1, N + 1)}
    for m, c in F.items():
        if c:
            need(wt(m) > 0, "centered equation has no constant")
            out[wt(m)][m] = c
    return out


def primitive(row):
    row = {i: a for i, a in row.items() if a}
    g = 0
    for a in row.values():
        g = gcd(g, a)
    if g:
        sign = 1 if row[min(row)] > 0 else -1
        row = {i: a // g * sign for i, a in row.items()}
    return row


def reduce_row(row, basis):
    row = primitive(row)
    while row and min(row) in basis:
        i = min(row)
        old = basis[i]
        a, b = old[i], row[i]
        row = primitive({j: a * row.get(j, 0) - b * old.get(j, 0)
                         for j in row.keys() | old.keys()})
    return row


def ideal_basis(equations, w, last=N):
    cols = {m: i for i, m in enumerate(monomials(w))}
    basis = {}
    for j, F in equations.items():
        if j > w or j > last:
            continue
        for m in monomials(w - j):
            row = {cols[tuple(sorted(m + u))]: c for u, c in F.items()}
            row = reduce_row(row, basis)
            if row:
                basis[min(row)] = row
    return cols, basis


def belongs(poly, w, equations, last=N):
    cols, basis = ideal_basis(equations, w, last)
    return not reduce_row({cols[m]: c for m, c in poly.items()}, basis)


def hilbert(equations):
    out = []
    for w in range(N + 1):
        cols, basis = ideal_basis(equations, w)
        out.append(len(cols) - len(basis))
    return out


def conv(a, b):
    return [sum(a[j] * b[i - j] for j in range(i + 1)) for i in range(N + 1)]


def euler(multiplicity):
    a = [1] + [0] * N
    for j in range(1, N + 1):
        for _ in range(multiplicity(j)):
            for w in range(j, N + 1):
                a[w] += a[w - j]
    return a


def authenticate():
    seal_path = ROOT / "MANIFEST.json"
    if seal_path.exists():
        seal = json.loads(seal_path.read_text())
        expected = {e["path"] for e in seal["files"]}
        actual = {str(f.relative_to(ROOT)) for f in ROOT.rglob("*") if f.is_file() and f != seal_path}
        need(expected == actual, "closed manifest membership")
        for e in seal["files"]:
            f = ROOT / e["path"]
            need(not f.is_symlink(), "no symlink")
            b = f.read_bytes()
            need(len(b) == e["bytes"] and digest(b) == e["sha256"], "sealed bytes: " + e["path"])
            need(e["private"] == e["path"].startswith("private_sources/"), "raw body privacy")
    for f in ROOT.glob("FETCH_RECEIPTS_*.json"):
        for r in json.loads(f.read_text()):
            if r.get("status") == 200:
                b = (P / r["file"]).read_bytes()
                need(len(b) == r["bytes"] and digest(b) == r["sha256"], "primary capture receipt")
    pr = json.loads((P / "pr.json").read_text())
    need(pr["number"] == 1257 and pr["head"]["sha"] == "e81d140d4aabfa35adb01d12a1677035fd3fa1f2", "immutable PR head")
    comparison = json.loads((P / "compare.json").read_text())
    need(len(comparison["files"]) == 8, "eight PR changes")
    for e in comparison["files"]:
        need(e["filename"].startswith("unsolved_math_prioritization/attempts/30005416/") and e["status"] == "added", "scoped no-QUEUE changes")
        b = (P / ("pr_" + e["filename"].split("/")[-1])).read_bytes()
        need(hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest() == e["sha"], "Git source blob")
    nested = json.loads((P / "pr_MANIFEST.json").read_text())
    for e in nested["entries"]:
        b = (P / ("pr_" + e["file"])).read_bytes()
        need(len(b) == e["bytes"] and digest(b) == e["sha256"], "nested PR manifest")
    for name, raw in [("INITIAL_LEDGER_CHECK.json", "ledger_initial.json"), ("FINAL_LEDGER_CHECK.json", "ledger_final.json")]:
        if (ROOT / name).exists():
            j = json.loads((ROOT / name).read_text())
            b = (P / raw).read_bytes()
            values = json.loads(b)["valueRanges"][0]["valueRange"]["values"]
            need(j["request"]["dataFilters"][0]["gridRange"] ==
                 {"sheetId": 1254632077, "startColumnIndex": 0, "endColumnIndex": 43}, "full numeric sheet request")
            need(digest(b) == j["sha256"] and len(values) == j["rows"], "ledger capture")
    if (ROOT / "PROPOSED_ROW.json").exists():
        j = json.loads((ROOT / "PROPOSED_ROW.json").read_text())
        need(len(j["cells"]) == 4 and all(isinstance(c, str) for c in j["cells"]), "four literal strings")
        need(j["cells"][1] == "" and j["cells"][2] == "https://doi.org/10.1007/s11139-012-9401-y", "blank B / authenticated prior DOI")
        need(not j["ready_for_external_write"] and j["covers_normal_converse"] is False, "scope and adoption gate")


def main():
    authenticate()
    target = euler(lambda j: 3 if j == 1 else 2)
    free = euler(lambda j: 3)
    product_formula = free[:]
    for j in range(2, N + 1):
        product_formula = [product_formula[w] - (product_formula[w - j] if w >= j else 0) for w in range(N + 1)]
    need(target == product_formula, "independent Euler-product expansions")
    need(target == [1, 3, 8, 18, 38, 74, 139, 249, 434, 734, 1215], "target coefficients")
    for w in range(N + 1):
        M = monomials(w)
        need(len(M) == len(set(M)) == free[w] and all(wt(m) == w for m in M), "monomial basis weight/count")
    cases = {
        "crossing": [(1, (1, 1, 0))],
        "pinch": [(1, (2, 0, 0)), (-1, (0, 2, 1))],
        "D4": [(1, (2, 0, 0)), (-1, (0, 2, 1)), (-1, (0, 0, 3))],
        "anisotropic_A1": [(1, (2, 0, 0)), (1, (0, 2, 0)), (1, (0, 0, 2))],
        "doubled_plane": [(1, (2, 0, 0))],
        "isolated_candidate_236": [(1, (2, 0, 0)), (1, (0, 3, 0)), (1, (0, 0, 6))],
    }
    equations = {k: coefficient_equations(v) for k, v in cases.items()}
    results = {k: hilbert(F) for k, F in equations.items()}
    for k in ["crossing", "pinch", "D4", "anisotropic_A1"]:
        need(results[k] == target, "positive exact series control " + k)
    need(results["doubled_plane"][:4] == target[:4] and results["doubled_plane"][4] == 39, "early nonregular control")
    need(results["isolated_candidate_236"][:10] == target[:10] and results["isolated_candidate_236"][10] == 1216, "late attempted normal counterexample rejected")
    cross = equations["crossing"]
    need(not belongs({(0, 4): 1}, 3, cross), "cross nilpotent nonzero")
    need(belongs({(0, 0, 4, 4): 1}, 6, cross), "cross nilpotent square zero")
    pinch = equations["pinch"]
    need(not belongs({(0,): 1}, 1, pinch) and belongs({(0, 0): 1}, 2, pinch), "pinch nonzero square-zero class")
    H = euler(lambda j: 1)
    reduced = [2 * c - h for c, h in zip(conv(H, H), H)]
    need(reduced[3] == 17 != target[3], "reduction changes invariant")
    bad = equations["isolated_candidate_236"]
    y5 = (1,) * 5
    annihilator = {tuple(sorted(y5 + u)): c for u, c in bad[5].items()}
    need(not belongs({y5: 1}, 5, bad, last=4), "annihilator witness is nonzero")
    need(belongs(annihilator, 10, bad, last=4), "annihilator kills fifth equation")
    y4product = {tuple(sorted((1,) * 4 + u)): c for u, c in bad[5].items()}
    need(not belongs(y4product, 9, bad, last=4), "weaker claimed annihilator rejected")
    # Finite-weight stability tests equations, rather than guessing series changes.
    for bound in range(2, N):
        late = coefficient_equations(cases["pinch"] + [(-1, (0, 0, bound + 1))])
        early = coefficient_equations(cases["pinch"] + [(-1, (0, 0, bound))])
        need(all(late[j] == pinch[j] for j in range(1, bound + 1)), "high-order perturbation invisible")
        need(early[bound] != pinch[bound], "threshold perturbation detected")
    # Monic normal-form basis under x=uv,y=u,z=v^2: parity proves
    # injectivity in every degree; these exact finite indices are controls.
    images = {(a + c, 2 * b + c) for a in range(7) for b in range(7) for c in range(2)}
    need(len(images) == 98, "pinch normal-form monomials have distinct images")
    # Test normalization: S=k[a,b], quotient by a^2,ab,b^2.
    P3 = [1] + [0] * N
    for _ in range(3):
        P3 = [P3[i] - (P3[i - 2] if i >= 2 else 0) for i in range(N + 1)]
    inverse = [1] + [0] * N
    for _ in range(3):
        for i in range(2, N + 1):
            inverse[i] += inverse[i - 2]
    normalized = conv([1, 2] + [0] * (N - 1), inverse)
    normalized_defect = [normalized[i] - (i + 1) for i in range(N + 1)]
    need(all(c >= 0 for c in normalized_defect) and any(c > 0 for c in normalized_defect), "normalized zero-divisor defect cannot cancel")
    naive = conv([i + 1 for i in range(N + 1)], P3)
    need(any(c < 0 for c in naive), "unnormalized alternating product is unsafe")
    print(json.dumps({"status": "PASS", "guards": GUARDS, "max_weight": N,
                      "target": target, "series": results, "reduced_crossing": reduced,
                      "normal_candidate_annihilator_verified": True,
                      "source_author_code_executed": False,
                      "scope": "exact finite controls and source bytes; all-weight deductions and standard imported theorems reviewed in REPORT"}, sort_keys=True))


if __name__ == "__main__":
    main()
