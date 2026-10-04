#!/usr/bin/env python3
"""Independent exact audit controls. Does not import the author's verifier.

Usage: python3 independent_controls.py [--source-tex downloaded-paper.tex]
The optional file is the arXiv:2609.08774v1 TeX source, obtained separately.
Source documents are not redistributed by this audit.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import re

PUBLIC = Path(__file__).resolve().parent.parent / "public"
EXPECTED_MANIFEST = "f1ee1233c24da05dddadcc1d8fa23501bad503eb7801caac083eddeb46917e18"
counts = Counter()

def check(condition, category):
    if not condition:
        raise AssertionError(category)
    counts[category] += 1

def add(p, q):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, F(0)) + v
    return {k: v for k, v in out.items() if v}

def multiply(p, q):
    out = {}
    for k, v in p.items():
        for l, w in q.items():
            out[k+l] = out.get(k+l, F(0)) + v*w
    return {k: v for k, v in out.items() if v}

def shift(p, n, factor=F(1)):
    return {k+n: factor*v for k, v in p.items() if factor*v}

def radial_integral(p):
    # Integral_0^1 p(r) r dr. Our products have nonnegative exponents.
    assert all(k >= 0 for k in p)
    return sum((v/F(k+2) for k, v in p.items()), F(0))

def polynomial(m, coefficients):
    out, basis = {}, {m: F(1)}
    for c in coefficients:
        out = add(out, {k: c*v for k, v in basis.items()})
        basis = multiply(basis, {0: F(1), 2: F(-1)})
    return out

def tex_number(s):
    s = s.strip()
    s = re.sub(r"\\frac\{(\d+)\}\{(\d+)\}", r"\1/\2", s)
    s = re.sub(r"\\frac(\d)(\d)", r"\1/\2", s)
    return F(s)

def source_compare(source, rows):
    tex = source.read_text()
    tables = re.findall(r"\\begin\{longtblr\}.*?\\end\{longtblr\}", tex, re.S)
    interval_table = next(t for t in tables if "label=tab:intervaltable" in t)
    coefficient_table = next(t for t in tables if "label=tab:mandvec" in t)
    defect_table = next(t for t in tables if "label=tab:results" in t)
    intervals = {
        int(m): [int(a), int(b)]
        for m, a, b in re.findall(
            r"\\\(\s*(\d+)\\\)\s*&\s*\\\(\[\s*(\d+)\s*,\s*(\d+)\s*\]\\\)",
            interval_table,
        )
    }
    vectors = {
        int(m): [tex_number(v) for v in c.split(",")]
        for m, c in re.findall(r"(\d+)\s*&\s*\(([^()]*)\)\s*\\\\", coefficient_table)
    }
    defects = {
        int(m): [tex_number(a), tex_number(b)]
        for m, a, b in re.findall(r"(\d+)\s*&\s*(-\\frac\{\d+\}\{\d+\})\s*&\s*(-\\frac\{\d+\}\{\d+\})\s*\\\\", defect_table)
    }
    check(len(intervals) == len(vectors) == len(defects) == 30, "source_table_dimensions")
    for row in rows:
        m = row["m"]
        check(intervals[m] == row["interval"], "source_interval_equality")
        check(vectors[m] == list(map(F, row["coefficients"])), "source_vector_equality")
        for actual, recorded in zip(defects[m], row["source_disk_defects"]):
            check(actual == F(recorded), "source_defect_equality")
    return {"source": "https://arxiv.org/src/2609.08774v1", "tex_sha256": sha256(source.read_bytes()).hexdigest(), "matched_interval_rows": 30, "matched_coefficient_vectors": 30, "matched_endpoint_defects": 60}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-tex", type=Path)
    args = parser.parse_args()
    manifest_bytes = (PUBLIC/"MANIFEST.json").read_bytes()
    check(sha256(manifest_bytes).hexdigest() == EXPECTED_MANIFEST, "frozen_manifest")
    for entry in json.loads(manifest_bytes)["files"]:
        data = (PUBLIC/entry["path"]).read_bytes()
        check(len(data) == entry["bytes"] and sha256(data).hexdigest() == entry["sha256"], "frozen_payload")
    data = json.loads((PUBLIC/"witnesses.json").read_text())
    rows = sorted(data["witnesses"], key=lambda r: r["interval"][0])
    check(len(rows) == 30, "witness_count")
    theta, kappa = F(5901, 10000), F(20201, 20200)
    check(F(data["threshold"]) == theta, "threshold")
    check((F(101,100)+F(100,101))/2 == kappa, "affine_anisotropy")
    check(kappa/2 < theta, "small_field_overlap")
    check(F("0.590106124587") > F("0.590106124") > theta, "published_threshold_comparison")
    right = F(3)
    ratios = []
    records = []
    replay = json.loads((PUBLIC/"verification.json").read_text())
    by_m = {r["m"]:r for r in replay["records"]}
    for row in rows:
        m = row["m"]
        c = list(map(F, row["coefficients"]))
        a, b = map(F, row["interval"])
        check(a <= right and a < b, "closed_interval_coverage")
        right = max(right,b)
        check(m >= 1 and len(c) == 9 and c[0] == 1, "polynomial_admissibility")
        g = polynomial(m,c)
        dg = {k-1:k*v for k,v in g.items() if k}
        gg = multiply(g,g)
        N = radial_integral(gg)
        K = radial_integral(multiply(dg,dg)) + radial_integral(shift(gg,-2,F(m*m)))
        V = radial_integral(shift(gg,2,F(1,4)))
        check((N,K,V) == tuple(F(by_m[m][key]) for key in ("mass","kinetic","potential")), "independent_polynomial_integrals")
        check(N > 0 and K > 0 and V > 0, "positive_integrals")
        check(4*K*V > m*m*N*N, "positive_energy_for_all_real_fields")
        row_out = {"m":m,"interval":[str(a),str(b)],"mass":str(N),"kinetic":str(K),"potential":str(V),"ellipse_margins":[]}
        for i,s in enumerate((a,b)):
            angular = add(shift(g,-1,F(m)), shift(g,1,-s/2))
            q = radial_integral(multiply(dg,dg)) + radial_integral(multiply(angular,angular))
            check(q == K-m*s*N+s*s*V, "direct_covariant_energy")
            disk = q-theta*s*N
            ellipse = kappa*q-theta*s*N
            check(disk < 0, "disk_endpoint_sign")
            check(disk == F(row["source_disk_defects"][i]), "recorded_endpoint_equality")
            check(ellipse < 0, "ellipse_endpoint_sign")
            check(K+m*s*N+s*s*V-theta*s*N > 0, "wrong_angular_sign_rejected")
            ratios.append((q/(s*N),m,s))
            row_out["ellipse_margins"].append(str(-ellipse/(s*N)))
        records.append(row_out)
    check(right == 131 and F(rows[0]["interval"][0]) == 3, "complete_coverage")
    worst,m,s = max(ratios)
    margin = theta-kappa*worst
    check(margin > 0, "uniform_endpoint_ratio_margin")
    # The ratio K/(sN)-m+sV/N has positive second derivative on s>0,
    # so its endpoint maximum also controls the complete real intervals.
    out = {"status":"PASS","author_manifest_sha256":EXPECTED_MANIFEST,"assertions":sum(counts.values()),"counts":dict(sorted(counts.items())),"largest_ratio":str(worst),"largest_ratio_at":{"m":m,"s":str(s)},"uniform_margin_below_5901_over_10000":str(margin),"uniform_margin_decimal_for_orientation_only":float(margin),"records":records,"scope":"Finite exact checks only; written analytic proofs and the external half-line theorem remain separate inputs."}
    if args.source_tex:
        out["source_table_comparison"] = source_compare(args.source_tex,rows)
        out["counts"] = dict(sorted(counts.items()))
        out["assertions"] = sum(counts.values())
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
