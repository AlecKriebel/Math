#!/usr/bin/env python3
"""Exact supplemental controls and strict file-integrity checks, Python stdlib only.

This does not formally prove any cited theorem, curve existence, equidistribution,
or Lyapunov continuity. Source verification checks PDF bytes, not their truth.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def math_checks():
    checks = []

    def require(label, value):
        if not value:
            raise AssertionError(label)
        checks.append(label)

    old = [F(1), F(1, 2), F(1, 3), F(1, 5), F(1, 7)]
    limit, radius = F(3, 13), F(1, 65)
    lo, hi = limit-radius, limit+radius
    distances = [abs(limit-v) for v in old]
    require("exact distances", distances == [F(10,13), F(7,26), F(4,39), F(2,65), F(8,91)])
    require("minimum separation", min(distances) == 2*radius)
    require("exact interval", (lo,hi) == (F(14,65),F(16,65)))
    require("positive normalized interval", 0 < lo < limit < hi < 1)
    for v in old:
        require("old value excluded " + str(v), not lo < v < hi)
        require("old value farther than radius " + str(v), abs(v-limit) > radius)

    # Pure degree arithmetic. No example below represents a claimed Gothic curve.
    for a,b in [(1,3),(3,13),(7,29),(19,83)]:
        for d in [1,2,3,6,24,101]:
            require(f"cover ratio {a}/{b} degree {d}", F(d*a,d*b) == F(a,b))
    # A commensurable-cover comparison uses two possibly unequal cover degrees.
    for d,e in [(2,3),(6,24),(17,31)]:
        a,b=F(7,10),F(31,6)
        require(f"common cover {d},{e}", (d*a)/(d*b) == (e*a)/(e*b))

    # Negative controls reject plausible but invalid shortcut implications.
    avg = F(3,8)*F(1,3) + F(5,8)*F(1,5)
    require("negative control new average need not be new component", avg == F(1,4) and avg not in old and F(1,3) in old and F(1,5) in old)
    avg_limit = F(3,13)*F(1,3) + F(10,13)*F(1,5)
    require("negative control even limit can average old values", avg_limit == limit)
    require("negative control reciprocal normalization", 1/limit == F(13,3) and 1/limit > 1)
    abstract_spectrum = sorted([F(1), F(3,5), F(2,5), limit], reverse=True)
    require("negative control block label is not sorted full label", abstract_spectrum[1] != limit)
    for n in range(1,101):
        x = limit + F(1,n+10)
        require(f"negative control limit not attained at term {n}", x != limit)
    # Nonsquare examples satisfying the published congruence requirement.
    for d in [12,24,28,33,40,48,52,60]:
        require(f"admissible sample discriminant {d}", d % 24 in {0,1,4,9,12,16} and d % 4 in {0,1} and isqrt(d)**2 != d)
    require("negative control volume-theorem condition is not target condition", 12 % 8 != 5 and 12 % 24 in {0,1,4,9,12,16})
    require("rank2 rel0 dimension", 4-2*2 == 0)
    require("proper positive even dimension", [d for d in range(2,4) if d % 2 == 0] == [2])
    return {"result":"PASS_EXACT_SUPPLEMENTAL_CONTROLS", "assertion_count":len(checks),
            "negative_control_families":5,
            "limit":str(limit), "interval":[str(lo),str(hi)],
            "minimum_old_set_distance":str(min(distances)),
            "formal_mathematical_proof_verification":False,
            "abstract_controls_are_geometric_examples":False}


def verify_manifest(root):
    manifest_path = root / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    expected = {item["path"]:item for item in manifest["files"]}
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    if actual != set(expected) | {"MANIFEST.json"}:
        raise ValueError("manifest file-set mismatch")
    for name,item in expected.items():
        p=root/name
        if p.is_symlink() or not p.is_file():
            raise ValueError("invalid artifact type: " + name)
        if p.stat().st_size != item["bytes"] or sha256(p) != item["sha256"]:
            raise ValueError("artifact integrity mismatch: " + name)
    for p in root.rglob("*"):
        if p.is_symlink():
            raise ValueError("symlink rejected")
    return {"result":"PASS", "files":len(expected), "manifest_sha256":sha256(manifest_path)}


def verify_sources(root, source_dir):
    metadata = json.loads((root/"SOURCE_VERIFICATION.json").read_text())
    sources=metadata["sources"]
    if source_dir is None:
        return {"result":"NOT_RUN_MISSING_SOURCES", "source_verification_run":False,
                "required_pdf_count":len(sources)}
    missing=[s["local_basename"] for s in sources if not (source_dir/s["local_basename"]).is_file()]
    if missing:
        return {"result":"NOT_RUN_MISSING_SOURCES", "source_verification_run":False,
                "missing":missing}
    for s in sources:
        p=source_dir/s["local_basename"]
        if p.is_symlink() or p.stat().st_size != s["bytes"] or sha256(p) != s["sha256"]:
            raise ValueError("source byte mismatch: " + s["local_basename"])
        if not p.read_bytes().startswith(b"%PDF-"):
            raise ValueError("not a PDF: " + s["local_basename"])
    return {"result":"PASS_EXACT_PDF_BYTES", "source_verification_run":True,
            "verified_pdf_count":len(sources), "source_theorems_formally_verified":False}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--sources-dir",type=Path)
    ap.add_argument("--math-only",action="store_true",help="Only the explicitly supplemental rational controls")
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    result={"mathematics":math_checks()}
    if not args.math_only:
        result["artifacts"]=verify_manifest(root)
        result["sources"]=verify_sources(root,args.sources_dir)
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if args.math_only or result["sources"]["source_verification_run"] else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AssertionError, ValueError, OSError, KeyError) as exc:
        print(json.dumps({"result":"FAIL", "error":str(exc)},sort_keys=True))
        sys.exit(1)
