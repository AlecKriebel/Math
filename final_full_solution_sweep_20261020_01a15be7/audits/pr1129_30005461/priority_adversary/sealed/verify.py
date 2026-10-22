#!/usr/bin/env python3
"""Read-only offline integrity/arithmetic checks; no network or captured-code execution.

Run a disposable copy, passing an externally retained manifest SHA256:
    python3 verify.py --manifest-sha256 HEX
This verifies finite evidence, not the imported literature theorem or historical priority.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def guard(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def poly(rows):
    out = {}
    for u, v, c, coeff in rows:
        key = (u, v, c)
        out[key] = out.get(key, 0) + coeff
    return {key: value for key, value in out.items() if value}


def blowup(p):
    # u=a*v, divide by v^2; c remains a symbolic indeterminate.
    out = {}
    for (u, v, c), coeff in p.items():
        guard(u + v >= 2, "cannot divide transformed polynomial by exceptional square")
        key = (u, u + v - 2, c)
        out[key] = out.get(key, 0) + coeff
    return {key: value for key, value in out.items() if value}


def homogeneous_min(p):
    m = min(u + v for u, v, c in p)
    return m, {key: val for key, val in p.items() if key[0] + key[1] == m}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest-sha256", required=True)
    args = ap.parse_args()
    base = Path(__file__).resolve().parent
    guard(len(args.manifest_sha256) == 64, "external digest is malformed")
    manifest_path = base / "MANIFEST.json"
    guard(not manifest_path.is_symlink(), "manifest must not be symlink")
    manifest_bytes = manifest_path.read_bytes()
    guard(digest(manifest_bytes) == args.manifest_sha256.lower(), "external manifest digest mismatch")
    manifest = json.loads(manifest_bytes)
    guard(manifest.get("schema") == 1, "unsupported manifest schema")
    files = manifest["files"]
    guard(isinstance(files, dict) and files, "empty inventory")
    observed = set()
    for path in base.rglob("*"):
        guard(not path.is_symlink(), "symlinks are forbidden")
        if path.is_file():
            observed.add(path.relative_to(base).as_posix())
    guard(observed == set(files) | {"MANIFEST.json"}, "inventory missing or unexpected files")
    for relative, record in files.items():
        pure = PurePosixPath(relative)
        guard(not pure.is_absolute() and ".." not in pure.parts and str(pure) == relative,
              "unsafe manifest path")
        data = (base / relative).read_bytes()
        guard(len(data) == record["bytes"], "size mismatch: " + relative)
        guard(digest(data) == record["sha256"], "hash mismatch: " + relative)
        if relative.endswith(".pdf"):
            guard(data.startswith(b"%PDF-"), "invalid captured PDF header")

    checks = json.loads((base / "CHECKS.json").read_text())
    guard(checks["head"] == "26fed29c1130e539ba018a37200f133870f0e036", "wrong immutable candidate")
    guard(checks["disposition"] == "prior_literature_covers_both_target_conclusions", "disposition changed")
    guard(checks["prior_theorem"] == "arxiv:2602.01191v1 Theorem6.4", "wrong prior theorem")
    for relative, anchors in checks["source_anchors"].items():
        guard(relative in files, "unbound source anchor")
        source = " ".join((base / relative).read_text().split())
        for anchor in anchors:
            guard(" ".join(anchor.split()) in source, "missing source anchor: " + anchor)

    expected_start = {(2, 0, 0): 1, (4, 0, 0): 1, (0, 6, 0): 1, (2, 2, 1): -1}
    recorded = [poly(rows) for rows in checks["blowup_polynomials"]]
    guard(len(recorded) == 4 and recorded[0] == expected_start, "wrong local starting polynomial")
    for index in range(3):
        guard(blowup(recorded[index]) == recorded[index + 1], "blow-up identity fails")
    expected_tangents = [
        {(2, 0, 0): 1},
        {(2, 0, 0): 1},
        {(2, 0, 0): 1, (0, 2, 0): 1},
    ]
    multiplicities = []
    for p, expected_tangent in zip(recorded[:3], expected_tangents):
        m, tangent = homogeneous_min(p)
        guard(m == 2 and tangent == expected_tangent, "incorrect multiplicity or tangent cone")
        multiplicities.append(m)
    # Positive definite final tangent has no projective real zero.
    final_degree, final_leading = homogeneous_min(recorded[3])
    guard(final_degree == 0 and final_leading == {(0, 0, 0): 1}, "real resolution does not terminate")
    exceptional = {key: val for key, val in recorded[3].items() if key[1] == 0}
    guard(exceptional == {(0, 0, 0): 1, (2, 0, 0): 1}, "wrong exceptional restriction")
    local_delta = sum(m * (m - 1) // 2 for m in multiplicities)
    guard(local_delta == 3 and checks["local_delta"] == local_delta, "wrong local delta")
    guard(checks["total_real_delta"] == 2 * local_delta == 6, "wrong total real delta")
    guard(checks["prior_theorem_cutoff"] == 8 and 2 * local_delta <= 8, "prior theorem does not apply")
    guard(checks["range"] == "0<c<3", "parameter range changed")

    # Half-Newton triangle: x+y+z=3, y<=2x, x<=2y, x,y,z>=0.
    roots = sorted((x, y, 3 - x - y) for x in range(4) for y in range(4 - x)
                   if y <= 2 * x and x <= 2 * y)
    guard(roots == [(0, 0, 3), (1, 1, 1), (1, 2, 0), (2, 1, 0)], "unexpected lattice points")
    guard(checks["newton_roots"] == [list(root) for root in roots], "recorded lattice roots changed")
    pairs = [(a, b) for a in roots for b in roots if tuple(a[i] + b[i] for i in range(3)) == (2, 2, 2)]
    guard(pairs == [((1, 1, 1), (1, 1, 1))], "non-SOS coefficient obstruction fails")
    for j in range(10):
        for k in range(j, 12):
            guard((2 * j + 1) + 2 * (k - j) == 2 * k + 1, "odd exponent propagation identity fails")

    # Fetch records and captured bytes agree; failures remain explicitly recorded.
    for record in json.loads((base / "SOURCE_FETCH.json").read_text()):
        if "sha256" in record:
            path = "private/" + record["name"]
            guard(path in files, "fetched input absent from manifest")
            guard(files[path]["sha256"] == record["sha256"], "fetch binding differs from captured bytes")
    print(json.dumps({"result": "PASS", "files_bound": len(files),
                      "local_delta": local_delta, "total_real_delta": 2 * local_delta,
                      "meaning": "integrity, exact symbolic local calculation and finite support checks; imported theorem remains trusted"}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, TypeError, json.JSONDecodeError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
