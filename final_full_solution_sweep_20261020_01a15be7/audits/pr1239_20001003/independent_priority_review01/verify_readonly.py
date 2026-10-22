#!/usr/bin/env python3
"""Independent exact checks; reads this audit only, writes nothing, uses no network.

This is reviewer-authored code, not a source author's program.  It corroborates
the explicit priority bridge and finite controls; it does not certify novelty.
All guards survive python -O and -OO. Run from any directory.
"""
from pathlib import Path
from itertools import product, permutations, combinations
from math import gcd, prod
import hashlib
import json

ROOT = Path(__file__).resolve().parent
P = ROOT / "private_sources"
CHECKS = 0


def need(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def egcd(a, b):
    if b == 0:
        return abs(a), (1 if a >= 0 else -1), 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def det(A):
    n = len(A)
    out = 0
    for q in permutations(range(n)):
        inversions = sum(q[i] > q[j] for i in range(n) for j in range(i + 1, n))
        out += (-1 if inversions % 2 else 1) * prod(A[i][q[i]] for i in range(n))
    return out


def bareiss(A):
    B = [list(r) for r in A]
    n, sign, old = len(B), 1, 1
    for k in range(n - 1):
        if B[k][k] == 0:
            j = next((j for j in range(k + 1, n) if B[j][k]), None)
            if j is None:
                return 0
            B[k], B[j] = B[j], B[k]
            sign *= -1
        pivot = B[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = B[i][j] * pivot - B[i][k] * B[k][j]
                need(numerator % old == 0, "Bareiss exact division")
                B[i][j] = numerator // old
            B[i][k] = 0
        old = pivot
    return sign * B[-1][-1]


def hnf(B):
    (a, b), (c, d) = B
    D = abs(a * d - b * c)
    need(D > 0, "HNF input rank")
    k, u, v = egcd(b, d)
    need(k > 0 and D % k == 0, "HNF projection index")
    h = D // k
    return h, (u * a + v * c) % h, k


def member(v, H):
    h, r, k = H
    x, y = v
    return y % k == 0 and (x - y // k * r) % h == 0


def member_adjugate(v, B):
    (a, b), (c, d) = B
    x, y = v
    D = a * d - b * c
    return (x * d - y * c) % D == 0 and (-x * b + y * a) % D == 0


def triple_lattice(t):
    a, b, c = t
    return ((a + c, -c), (-c, b + c))


def triples_cube(D):
    return {t for t in product(range(D + 1), repeat=3)
            if t[0] * t[1] + t[0] * t[2] + t[1] * t[2] == D}


def triples_division(D):
    out = set()
    for a, b in product(range(D + 1), repeat=2):
        if a + b and D >= a * b and (D - a * b) % (a + b) == 0:
            c = (D - a * b) // (a + b)
            if c <= D:
                out.add((a, b, c))
    return out


def connected(n, edges, weights):
    reached = {n}
    while True:
        new = reached | {v for (u, v), w in zip(edges, weights) if w and u in reached}
        new |= {u for (u, v), w in zip(edges, weights) if w and v in reached}
        if new == reached:
            return len(reached) == n + 1
        reached = new


def matrix(n, edges, weights):
    L = [[0] * n for _ in range(n)]
    for (u, v), w in zip(edges, weights):
        if u < n:
            L[u][u] += w
        if v < n:
            L[v][v] += w
        if u < n and v < n:
            L[u][v] -= w
            L[v][u] -= w
    return L


def tree_count(n, edges, weights):
    total = 0
    for ids in combinations(range(len(edges)), n):
        w = prod(weights[i] for i in ids)
        if w and connected(n, [edges[i] for i in ids], [1] * n):
            total += w
    return total


def validate_inventory():
    seal_path = ROOT / "MANIFEST.json"
    if seal_path.exists():
        seal = json.loads(seal_path.read_text())
        entries = seal["files"]
        expected = {e["path"] for e in entries}
        actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
                  if p.is_file() and p != seal_path}
        need(expected == actual, "closed inventory exact file membership")
        for e in entries:
            p = ROOT / e["path"]
            need(not p.is_symlink(), "no symlinks")
            b = p.read_bytes()
            need(len(b) == e["bytes"] and sha(b) == e["sha256"], "sealed bytes " + e["path"])
            need(e["private"] == e["path"].startswith("private_sources/"), "privacy flag")
    for receipt in sorted(ROOT.glob("FETCH_RECEIPTS_*.json")):
        for r in json.loads(receipt.read_text()):
            if r.get("status") == 200:
                b = (P / r["file"]).read_bytes()
                need(len(b) == r["bytes"] and sha(b) == r["sha256"], "capture receipt")
    pr = json.loads((P / "pr.json").read_text())
    need(pr["number"] == 1239 and pr["head"]["sha"] == "d31329ef92ab27b9d5a314ecc0313bd2b4e113b9", "PR head")
    comp = json.loads((P / "compare.json").read_text())
    need(comp["base_commit"]["sha"] == "4b27092a448d53b61408355ce44ec38d103a1ce4", "PR base")
    need(len(comp["files"]) == 8, "eight PR paths")
    for e in comp["files"]:
        need(e["filename"].startswith("unsolved_math_prioritization/attempts/20001003/")
             and e["status"] == "added", "scoped added path")
        b = (P / ("pr_" + e["filename"].split("/")[-1])).read_bytes()
        need(hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest() == e["sha"], "immutable Git blob")
    nested = json.loads((P / "pr_MANIFEST.json").read_text())
    need(set(nested["members"]) == {e["filename"].split("/")[-1] for e in comp["files"]}, "nested manifest members")
    for e in nested["entries"]:
        b = (P / ("pr_" + e["file"])).read_bytes()
        need(len(b) == e["bytes"] and sha(b) == e["sha256"], "nested manifest payload")
    for name in ["INITIAL_LEDGER_CHECK.json", "FINAL_LEDGER_CHECK.json"]:
        f = ROOT / name
        if f.exists():
            j = json.loads(f.read_text())
            need(j["request"]["dataFilters"][0]["gridRange"] ==
                 {"sheetId": 1254632077, "startColumnIndex": 0, "endColumnIndex": 43}, "full numeric-gid request")
            raw_name = "ledger_initial.json" if name.startswith("INITIAL") else "ledger_final.json"
            raw = (P / raw_name).read_bytes()
            values = json.loads(raw)["valueRanges"][0]["valueRange"]["values"]
            need(sha(raw) == j["sha256"] and len(values) == j["rows"], "ledger capture identity/count")
            need(values[0][:4] == ["Original Problem", "Solution Chat URL", "DOI", "Notes"], "ledger schema")
    for n in ["zenodo_target.json", "zenodo_ferudun10.json", "zenodo_title10.json"]:
        j = json.loads((P / n).read_text())
        need(j["hits"]["total"] == 0 and j["hits"]["hits"] == [], "bounded exact registry search zero")
    exact = json.loads((P / "datacite_lattice_exact.json").read_text())
    need(exact["meta"]["total"] == 26 == len(exact["data"]), "entire exact-phrase DataCite response inspected")
    pages = [json.loads((P / n).read_text()) for n in ["datacite_row.json", "datacite_row2.json"]]
    need(sum(len(j["data"]) for j in pages) == 31 and all(j["meta"]["total"] == 31 for j in pages), "both reduced-Laplacian result pages")
    index = (P / "eulersolve_index.html").read_text().casefold()
    need("aim-combinatorics-0128" not in index and "undirected reduced laplacian" not in index,
         "false public-index lead explicitly rejected")
    hold_path = ROOT / "ACCOUNTING_HOLD.json"
    if hold_path.exists():
        hold = json.loads(hold_path.read_text())
        need(hold["four_cell_row"] is None and not hold["ready_for_external_write"], "no partial-prior DOI promoted to full row")
    return True


def main():
    validate_inventory()
    prior_B = ((2, -2, 0), (-1, 3, -2))
    orbit = []
    for q in permutations(range(3)):
        B = tuple(tuple(r[i] for i in q[:2]) for r in prior_B)
        H = hnf(B)
        need(H[0] * H[2] == 4, "prior family index four")
        orbit.append({"permutation": q, "reduced_basis": B, "hnf": H})
        for v in product(range(-4, 5), repeat=2):
            need(member(v, H) == member_adjugate(v, B), "independent prior bridge membership")
    bad = {(2, 1, 2), (4, 1, 1), (4, 2, 1)}
    need({tuple(e["hnf"]) for e in orbit} == bad, "exact prior orbit equals all PR obstructions")
    # The (0,2,1) projection is the PR's chosen bad lattice, with an explicit
    # unimodular row operation: (2,0),(-1,-2) -> (2,0),(1,2).
    need(hnf(((2, 0), (-1, -2))) == hnf(((2, 0), (1, 2))), "exact chosen lattice equality")
    counts = []
    for D in range(1, 21):
        T = triples_cube(D)
        need(T == triples_division(D), "two independent exact triple enumerations")
        forms = [(h, r, D // h) for h in range(1, D + 1) if D % h == 0 for r in range(h)]
        images = {hnf(triple_lattice(t)) for t in T}
        recognized = set()
        for H in forms:
            for t in T:
                B = triple_lattice(t)
                inside = all(member(v, H) for v in B)
                need(inside == (hnf(B) == H), "inclusion/index and normal form recognition agree")
                if inside:
                    recognized.add(H)
        need(recognized == images, "rank-two recognition completeness within finite bound")
        if D < 4:
            need(recognized == set(forms), "all rank-two forms below four graphical")
        if D == 4:
            need(set(forms) - recognized == bad, "exact three obstructions")
            need(len(T) == 9, "nine determinant-four triples")
        counts.append({"D": D, "forms": len(forms), "graphical": len(recognized), "triples": len(T)})
    need(hnf(triple_lattice((1, 0, 4))) == (1, 0, 4), "graphical cyclic-four comparison")
    need(gcd(2, gcd(1, 2)) == gcd(1, 4) == 1, "Smith first invariant one in both cases")
    graph_counts = []
    for n, cap in [(1, 2), (2, 2), (3, 2), (4, 1)]:
        edges = list(combinations(range(n + 1), 2))
        total = positive = 0
        for W in product(range(cap + 1), repeat=len(edges)):
            L = matrix(n, edges, W)
            d = det(L)
            need(d == bareiss(L), "independent determinant algorithms")
            need(d == tree_count(n, edges, W), "weighted matrix-tree identity")
            need((d > 0) == connected(n, edges, W), "connectivity/determinant equivalence")
            if d:
                need(all(w <= d for w in W), "all edge multiplicities bounded by tree count")
                need(all(0 < L[i][i] <= n * d for i in range(n)), "correct diagonal bound")
                positive += 1
            total += 1
        graph_counts.append({"rank": n, "weight_cap": cap, "assignments": total, "connected": positive})
    controls = {
        "same_determinant_alone_unsound": hnf(((2, 0), (1, 2))) != hnf(((1, 0), (0, 4))),
        "transpose_changes_embedding": member_adjugate((1, 2), ((2, 0), (1, 2))) and
                                      not member_adjugate((1, 2), ((2, 1), (0, 2))),
        "inclusion_without_equal_index_unsound": all(member(v, (2, 1, 2)) for v in ((4, 0), (0, 4))) and det(((4, 0), (0, 4))) != 4,
        "corrupt_prior_bridge_rejected": hnf(((2, 0), (-1, -3))) not in bad,
        "diagonal_D_bound_false": max(triple_lattice((1, 0, 4))[i][i] for i in range(2)) > 4,
    }
    for k, v in controls.items():
        need(v, "negative semantic control " + k)
    print(json.dumps({"status": "PASS", "guards": CHECKS, "prior_orbit": orbit,
                      "rank_two_counts": counts, "graph_controls": graph_counts,
                      "negative_controls": controls,
                      "limit": "finite exact controls and byte authentication; no global novelty certificate"}, sort_keys=True))


if __name__ == "__main__":
    main()
