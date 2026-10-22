#!/usr/bin/env python3
"""Portable exact auxiliary checks and pin verification; not a theorem prover.

Default: verify this safe audit package. Optional paths independently check the
frozen author directory, its ZIP, or the six locally available public PDFs.
No network calls, source extraction, or writes are performed.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def check_bytes(data, record):
    require(len(data) == record["bytes"], "Byte-count mismatch: " + record["name"])
    require(digest(data) == record["sha256"], "SHA-256 mismatch: " + record["name"])


def verify_directory(directory, records, additional=()):
    names = [r["name"] for r in records]
    require(len(names) == len(set(names)), "Duplicate manifest entry")
    require(all(Path(n).name == n and n not in (".", "..") for n in names), "Unsafe manifest name")
    require({p.name for p in directory.iterdir()} == set(names) | set(additional), "Unexpected or missing package entry")
    require(all(p.is_file() and not p.is_symlink() for p in directory.iterdir()), "Nonregular package entry")
    for record in records:
        check_bytes((directory / record["name"]).read_bytes(), record)
    return len(records)


def compute_checks():
    swap = lambda n: {0: 1, 1: 0}.get(n, n)
    pairs = 0
    extrema = set()
    for x, y in combinations(range(-128, 129), 2):
        ratio = Q(abs(swap(x) - swap(y)), y - x)
        require(Q(1, 2) <= ratio <= 2, "Adjacent-swap distortion")
        require(swap(swap(x)) == x and swap(swap(y)) == y, "Adjacent-swap inverse")
        extrema.add(ratio)
        pairs += 1
    require(min(extrema) == Q(1, 2) and max(extrema) == 2, "Adjacent-swap extrema")
    require((swap(-1), swap(0), swap(1)) == (-1, 1, 0), "Nonmonotonicity witness")

    bd_cases = 0
    for q in range(1601):
        bound = Q(q, 16)
        n = bound.numerator // bound.denominator + 1
        targets = (2 * n + 1) ** 2
        radius = (n + bound) / 2
        preimages = (2 * (radius.numerator // radius.denominator) + 1) ** 2
        require(preimages <= (n + bound + 1) ** 2 < targets, "Density counting obstruction")
        bd_cases += 1

    grid = list(product(range(-4, 5), repeat=2))
    translations = [(Q(0), Q(0)), (Q(1, 2), Q(0)), (Q(-2, 3), Q(5, 7))]
    affine_cases = inverse_points = affine_pairs = 0
    for scale, orientation, shift in product([Q(1, 2), Q(1), Q(2)], [-1, 1], translations):
        mapped = []
        for z in grid:
            d = (scale * orientation * z[0] + shift[0], scale * z[1] + shift[1])
            restored = (orientation * (d[0] - shift[0]) / scale, (d[1] - shift[1]) / scale)
            require(restored == z, "Affine inverse reduction")
            mapped.append((z, d))
            inverse_points += 1
        for (z, d), (w, e) in combinations(mapped, 2):
            require(sum((a-b)**2 for a,b in zip(d,e)) == scale**2 * sum((a-b)**2 for a,b in zip(z,w)), "Affine exact squared distance")
            affine_pairs += 1
        affine_cases += 1
    require(Q(-1, 2).denominator != 1, "Origin-exclusion witness")
    require(1 % 2 != 0, "Unit-equivariance parity witness")

    exponent_10 = 84 + 52 * 39 + 54 * 200 + 30 * 41
    exponent_L = 52 * 15 + 54 * 77 + 30 * 16
    require((exponent_10, exponent_L) == (14142, 5418), "Published substitution arithmetic")
    require(exponent_10 <= 20000 and exponent_L <= 6000, "Published upper-bound slack")
    ceiling_cases = 0
    for n in range(8, 65):
        L = Q(n, 8)
        value = 10**40 * L**16
        ceiling = -(-value.numerator // value.denominator)
        require(ceiling <= 10**41 * L**16, "Ceiling bound")
        ceiling_cases += 1
    return {
        "adjacent_swap_pairs": pairs,
        "adjacent_swap_min_ratio": "1/2",
        "adjacent_swap_max_ratio": "2",
        "rational_bounded_displacement_cases": bd_cases,
        "affine_orientation_translation_scale_cases": affine_cases,
        "affine_inverse_points": inverse_points,
        "affine_squared_distance_pairs": affine_pairs,
        "ceiling_bound_cases": ceiling_cases,
        "substitution_base_10_exponent": exponent_10,
        "substitution_L_exponent": exponent_L,
        "universal_mathematical_proof_by_sampling": False,
    }


def verify_sources(directory, sources):
    for record in sources:
        path = directory / record["local_filename"]
        require(path.is_file() and not path.is_symlink(), "Missing regular source PDF")
        check_bytes(path.read_bytes(), {"name": record["local_filename"], "bytes": record["bytes"], "sha256": record["sha256"]})
    return len(sources)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author-dir", type=Path)
    parser.add_argument("--author-archive", type=Path)
    parser.add_argument("--source-dir", type=Path)
    args = parser.parse_args()
    verified = {"audit_payload_files": verify_directory(ROOT, read_json("MANIFEST.json")["files"], ("MANIFEST.json",))}
    checks = compute_checks()
    require(checks == read_json("INDEPENDENT_CHECKS.json")["computed_checks"], "Computed-check result changed")
    pins = read_json("FROZEN_PAYLOAD_PINS.json")
    require(pins["archive"]["sha256"] == "2511a95f32681a85c337393c1c0ac2f7ad5525247f3e484c00d6150423c477cb", "Wrong author freeze")
    if args.author_dir:
        verified["author_files"] = verify_directory(args.author_dir, pins["files"])
    if args.author_archive:
        data = args.author_archive.read_bytes()
        check_bytes(data, pins["archive"])
        with zipfile.ZipFile(args.author_archive) as archive:
            require(len(archive.namelist()) == len(set(archive.namelist())), "Duplicate ZIP entry")
            require(set(archive.namelist()) == {r["name"] for r in pins["files"]}, "ZIP inventory mismatch")
            for record in pins["files"]:
                check_bytes(archive.read(record["name"]), record)
        verified["author_archive"] = "PASS"
    source_records = read_json("INDEPENDENT_SOURCE_VERIFICATION.json")["sources"]
    require(len(source_records) == 6, "Expected six PDF pins")
    require(all(r["fresh_matches_retained"] and r["fresh_bytes"] == r["bytes"] and r["fresh_sha256"] == r["sha256"] and r["fresh_pages"] == r["pages"] for r in source_records), "Fresh source receipt mismatch")
    if args.source_dir:
        verified["source_pdf_pins"] = verify_sources(args.source_dir, source_records)
    print(json.dumps({"result": "PASS", "verified": verified, "computed_checks": checks}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
