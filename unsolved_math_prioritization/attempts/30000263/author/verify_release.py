#!/usr/bin/env python3
"""Fail-closed artifact checks. The human-readable proofs remain primary.

No check uses Python assert; python -O executes the same validations.
No network access and no external state changes are performed.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parent
TARGET_HASH = "41dce0de0472889e89c4936d3356ad2b0e568c1368a3cff52261db747b141f38"
CORPUS_HASHES = {
    "catalog": "891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566",
    "problems": "04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf",
    "reports": "8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pairs_hook(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def bad_constant(value):
    raise ValueError("nonfinite JSON constant: " + value)


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=pairs_hook, parse_constant=bad_constant)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_manifest():
    m = read_json(ROOT / "MANIFEST.json")
    require(m["schema"] == 1, "manifest schema")
    require(isinstance(m["files"], dict) and m["files"], "empty manifest")
    require(all(p.is_file() and not p.is_symlink() for p in ROOT.iterdir()), "unexpected directory or symlink")
    actual = {p.name for p in ROOT.iterdir() if p.is_file()}
    require(actual == set(m["files"]) | {"MANIFEST.json"}, "unexpected or missing package file")
    for name, expected in m["files"].items():
        require(Path(name).name == name and name not in (".", ".."), "invalid manifest path")
        p = ROOT / name
        require(p.is_file() and not p.is_symlink(), "missing file or symlink: " + name)
        data = p.read_bytes()
        require(len(data) == expected["bytes"], "byte count mismatch: " + name)
        require(sha(data) == expected["sha256"], "hash mismatch: " + name)
    return len(m["files"])


def line_quantities(x, u):
    n = len(x)
    require(n == len(u) and n >= 2 and len(set(x)) == n, "invalid line configuration")
    P = [sum((u[j] / abs(x[i] - x[j]) for j in range(n) if j != i), Q()) for i in range(n)]
    F = [sum((u[j] * (x[i] - x[j]) / abs(x[i] - x[j]) ** 3
              for j in range(n) if j != i), Q()) for i in range(n)]
    D = sum((u[j] ** 2 / (x[i] - x[j]) ** 2
             for i in range(n) for j in range(n) if i != j), Q())
    return P, F, D


def rank_q(matrix):
    a = [list(map(Q, row)) for row in matrix]
    rank = 0
    for c in range(len(a[0])):
        pivots = [i for i in range(rank, len(a)) if a[i][c]]
        if not pivots:
            continue
        i = pivots[0]
        a[rank], a[i] = a[i], a[rank]
        pivot = a[rank][c]
        a[rank] = [z / pivot for z in a[rank]]
        for i in range(len(a)):
            if i != rank:
                t = a[i][c]
                a[i] = [z - t * w for z, w in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def exact_checks():
    c = read_json(ROOT / "EXACT_CERTIFICATES.json")
    ball = c["min_ball"]
    points = [[Q(v) for v in row] for row in ball["points"]]
    require(len(points) == 6 and all(len(x) == 3 for x in points), "ball point dimensions")
    require(len(set(map(tuple, points))) == 6, "duplicate ball points")
    weights = list(map(Q, ball["weights_first_three"]))
    require(len(weights) == 3 and min(weights) > 0 and sum(weights) == 1, "barycentric weights")
    require(all(sum(weights[i] * points[i][k] for i in range(3)) == 0 for k in range(3)), "weighted center")
    radii = [sum(v * v for v in x) for x in points]
    require(radii == list(map(Q, ball["squared_radii"])), "squared radii")
    require(radii[:3] == [Q(1)] * 3 and max(radii[3:]) < 1, "exactly three sphere contacts")
    require(rank_q([[points[i][k] - points[0][k] for k in range(3)] for i in range(1, 6)]) == 3, "full affine span")
    require(rank_q([[points[i][k] - points[0][k] for k in range(3)] for i in [1, 2]]) == 2, "boundary noncollinearity")
    require(ball["boundary_count"] == 3 and ball["affine_dimension"] == 3, "ball metadata")

    for e in map(Q, c["spectral_family"]["epsilon_tests"]):
        require(0 < e < 1, "epsilon outside domain")
        u = [-e / (1-e), -e, Q(1)]
        P, F, D = line_quantities([Q(0), e, Q(1)], u)
        require(P == [0, 0, -2*e/(1-e)], "spectral potential formula")
        require(D == (4-4*e+4*e*e)/(1-e)**2, "spectral denominator")
        G = [-2*u[i]*F[i] for i in range(3)]
        require(G == [2, -2/(1-e)**2, 2*e*(2-e)/(1-e)**2], "spectral force formula")
        require(sum(G) == 0, "translation identity")
        require((sum(v*v for v in P)+max(map(abs, G)))/D == (4*e*e+2)/(4-4*e+4*e*e), "full spectral ratio")

    # Polynomial identity underlying the pairwise cubic argument, exact coefficients.
    polynomial = {(2, 0): Q(1)-Q(3, 2)+Q(1, 2),
                  (1, 1): Q(1)-Q(1),
                  (0, 2): Q(1)-Q(3, 2)+Q(1, 2)}
    require(all(v == 0 for v in polynomial.values()), "cubic pair polynomial")
    rng = random.Random(30000263)
    count = 0
    for n in range(2, 12):
        for unused in range(100):
            x = sorted(map(Q, rng.sample(range(-50, 50), n)))
            u = [Q(rng.randrange(-8, 9), rng.randrange(1, 6)) for i in x]
            P, F, unused_D = line_quantities(x, u)
            E = sum((u[i]*u[j]*abs(x[i]-x[j]) for i in range(n) for j in range(i+1, n)), Q())
            L = sum((u[i]*x[i]**3*F[i]-Q(3,2)*u[i]*x[i]**2*P[i] for i in range(n)), Q())
            require(L == -E/2, "cubic virial identity")
            w = u[:-1] + [-sum(u[:-1])]
            lhs = sum((w[i]*w[j]*(x[j]-x[i]) for i in range(n) for j in range(i+1,n)), Q())
            rhs = -sum(((x[k+1]-x[k])*sum(w[:k+1])**2 for k in range(n-1)), Q())
            require(lhs == rhs, "negative distance identity")
            require(lhs < 0 or all(z == 0 for z in w), "strict conditional negativity")
            # A rational inversion center chosen away from all integer points.
            a = Q(1, 2)
            radii = [abs(t-a) for t in x]
            y = [a+1/(t-a) for t in x]
            v = [u[i]/radii[i] for i in range(n)]
            Py, Fy, unused_Dy = line_quantities(y, v)
            for i in range(n):
                require(Py[i] == radii[i]*P[i], "Kelvin potential identity")
                sign = Q(1) if x[i] > a else Q(-1)
                require(Fy[i] == sign*radii[i]**2*P[i]-radii[i]**3*F[i], "Kelvin force identity")
            Ey = sum((v[i]*v[j]*abs(y[i]-y[j]) for i in range(n) for j in range(i+1,n)), Q())
            Ew = sum((u[i]*u[j]*abs(x[i]-x[j])/(radii[i]**2*radii[j]**2)
                      for i in range(n) for j in range(i+1,n)), Q())
            require(Ey == Ew, "Kelvin distance-energy identity")
            count += 1

    # Gaussian-rational version of the local complex-weight counterexample.
    def mul(a, b):
        return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
    a = mul((Q(-1,2), Q(1,2)), (Q(1), Q(-1)))
    b = mul((Q(-1,2), Q(0)), (Q(0), Q(2)))
    require((a[0]+b[0], a[1]+b[1]) == (0,0), "local complex circle identity")
    require((Q(1), Q(-1)+Q(2)) != (0,0), "local signed sum is nonzero")
    return count


def numeric_checks():
    data = read_json(ROOT / "NUMERIC_RESULTS.json")
    require(data["status"] == "FINITE_EXPLORATION_NOT_A_PROOF", "numeric scope")
    require(data["starts_per_family"] == 6 and data["evaluation_budget_per_start"] == 500, "search bounds")
    require(len(data["rows"]) == 24, "numeric row count")
    seen = set()
    minima = {}
    for row in data["rows"]:
        p, dim = row["p"], row["dimension"]
        require((p,dim) in {(6,2),(6,3),(7,3),(8,3)}, "numeric family")
        key = (p,dim,row["start"])
        require(key not in seen and 0 <= row["start"] < 6, "numeric start")
        seen.add(key)
        x, u = row["positions"], row["charges"]
        require(len(x) == p and len(u) == p and all(len(z) == dim for z in x), "numeric dimensions")
        require(all(math.isfinite(v) for z in x for v in z) and all(math.isfinite(v) for v in u), "numeric finite")
        P, G, D = [0.0]*p, [[0.0]*dim for i in range(p)], 0.0
        separation = math.inf
        for i in range(p):
            for j in range(p):
                if i == j:
                    continue
                dx = [x[i][k]-x[j][k] for k in range(dim)]
                r = math.sqrt(math.fsum(v*v for v in dx))
                require(r > 0 and math.isfinite(r), "numeric collision")
                separation = min(separation, r)
                P[i] += u[j]/r
                D += u[j]*u[j]/(r*r)
                for k in range(dim):
                    G[i][k] -= 2*u[i]*u[j]*dx[k]/r**3
        require(D > 0 and math.isfinite(D), "numeric denominator")
        ratio = (math.fsum(v*v for v in P)+max(abs(v) for z in G for v in z))/D
        require(math.isfinite(ratio) and ratio > 0, "numeric ratio")
        require(math.isclose(ratio, row["ratio_coordinate"], rel_tol=1e-8, abs_tol=1e-10), "numeric replay mismatch")
        require(math.isclose(separation, row["min_separation"], rel_tol=1e-10, abs_tol=1e-12), "numeric separation")
        require(0 < row["nfev"] <= 500 and row["optimizer_status"] in {0,1,2,3,4}, "optimizer metadata")
        label = f"p={p},dimension={dim}"
        minima[label] = min(minima.get(label, math.inf), ratio)
    return minima


def external_checks(paths, source_dir):
    status = {"corpora": "NOT_PROVIDED", "pdfs": "NOT_PROVIDED"}
    meta = read_json(ROOT / "TARGET_REVIEW.json")
    require(meta["problem_id"] == 30000263 and meta["problem_number"] == "OWR-1050-014", "target identity")
    require(meta["complete_record_review_sha256"] == TARGET_HASH, "target review hash")
    require(meta["verdict"] == "PARTIAL_NO_FULL_RESOLUTION" and meta["report_present"] is False, "target scope")
    require({x["role"]: x["sha256"] for x in meta["corpora"]} == CORPUS_HASHES, "corpus pins")
    if paths:
        parsed = {}
        for role, path in zip(["catalog","problems","reports"], paths):
            raw = path.read_bytes()
            require(sha(raw) == CORPUS_HASHES[role], "external corpus hash: " + role)
            pin = next(v for v in meta["corpora"] if v["role"] == role)
            require(len(raw) == pin["byte_count"], "external corpus size: " + role)
            parsed[role] = read_json(path)
            require(len(parsed[role]) == pin["record_count"], "external corpus count: " + role)
        records = [v for v in parsed["problems"] if v.get("id") == 30000263]
        require(len(records) == 1, "unique complete problem record")
        p = records[0]
        require(p["problem_number"] not in parsed["reports"], "expected absent research report")
        report = parsed["reports"].get(p["problem_number"], {})
        require(sha(json.dumps([p,report], sort_keys=True).encode()) == TARGET_HASH, "complete review serialization")
        require(any(str(v.get("id")) == "30000263" for v in parsed["catalog"]), "catalog identity match")
        status["corpora"] = "PASS_ALL_THREE_AND_COMPLETE_RECORD"
    if source_dir:
        for src in read_json(ROOT / "SOURCE_METADATA.json")["sources"]:
            name = src["retrieval_filename"]
            require(Path(name).name == name, "source filename")
            raw = (source_dir / name).read_bytes()
            require(raw.startswith(b"%PDF-") and len(raw) == src["byte_count"] and sha(raw) == src["sha256"], "source PDF mismatch: " + name)
        status["pdfs"] = "PASS_ALL_FIVE_PDFS"
    return status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpora", type=Path, nargs=3, metavar=("CATALOG", "PROBLEMS", "REPORTS"))
    ap.add_argument("--source-dir", type=Path)
    args = ap.parse_args()
    files = check_manifest()
    identities = exact_checks()
    minima = numeric_checks()
    external = external_checks(args.corpora, args.source_dir)
    print(json.dumps({"status":"PASS_ARTIFACT_CHECKS_NOT_GENERAL_CONJECTURE", "optimized_python":not __debug__,
                      "manifest_files":files, "exact_identity_test_configurations":identities,
                      "numeric_minima_not_bounds":minima, "external":external}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
