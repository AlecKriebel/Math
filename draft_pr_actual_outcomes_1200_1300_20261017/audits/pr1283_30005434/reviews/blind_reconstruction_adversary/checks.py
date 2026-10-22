#!/usr/bin/env python3
"""Independent adversarial diagnostics, not a replacement for universal proof.

Only the original source and the authorized sealed reconstruction are inputs.
No assertions or filesystem writes are used. Run with python3, -O, and -OO.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


class AuditFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise AuditFailure(message)


def reject(function, fragment):
    try:
        function()
    except AuditFailure as error:
        require(fragment in str(error), f"wrong injected-failure reason: {error}")
        return str(error)
    raise AuditFailure("injected failure was accepted")


MANIFEST_HASH = "cfde3d99a4443c04a056271f3d6c944c04ec0ccdb6f279b6c091721036624159"
SOURCE_HASH = "0ba13c573755289bb62e119df381d19e03a31cb3fff8e1ff3e240dce8dfeeefc"
MEMBERS = {"PROOF.md", "REPORT.md", "RESEARCH_LOG.md", "checks.py", "checks.out"}


def manifest_schema(value):
    require(isinstance(value, dict) and set(value) == {"files"}, "manifest root schema")
    require(isinstance(value["files"], list), "files must be a list")
    require(len(value["files"]) == 5, "manifest member count")
    names = []
    for item in value["files"]:
        require(isinstance(item, dict) and set(item) == {"relative_path", "bytes", "sha256"},
                "manifest record schema")
        require(isinstance(item["relative_path"], str), "relative_path type")
        require(type(item["bytes"]) is int and item["bytes"] >= 0, "bytes type")
        digest = item["sha256"]
        require(isinstance(digest, str) and len(digest) == 64 and
                all(c in "0123456789abcdef" for c in digest), "sha256 syntax")
        names.append(item["relative_path"])
    require(len(set(names)) == len(names) and set(names) == MEMBERS, "exact authored membership")


def content_check(data, size, digest, name):
    require(len(data) == size, f"member byte length: {name}")
    require(sha256(data).hexdigest() == digest, f"member SHA-256: {name}")


def authenticate():
    audit = Path(__file__).resolve().parents[2]
    family = audit / "reviews" / "blind_source_reconstruction"
    manifest_data = (family / "MANIFEST.json").read_bytes()
    require(len(manifest_data) == 791 and sha256(manifest_data).hexdigest() == MANIFEST_HASH,
            "anchored manifest mismatch")
    manifest = json.loads(manifest_data)
    manifest_schema(manifest)
    for member in manifest["files"]:
        name = member["relative_path"]
        content_check((family / name).read_bytes(), member["bytes"], member["sha256"], name)
        print(f"AUTH member {name}: bytes={member['bytes']} SHA-256={member['sha256']}")
    source = (audit / "_local" / "root_sources" / "workshop.pdf").read_bytes()
    content_check(source, 286244, SOURCE_HASH, "original workshop PDF")
    seal_data = (family / "INITIAL_SEAL.json").read_bytes()
    seal = json.loads(seal_data)
    expected = {
        "candidate_exposure_before_seal": False,
        "completion_estimate_percent": 100,
        "manifest_bytes": 791,
        "manifest_sha256": MANIFEST_HASH,
        "sealed_utc": "2026-10-18 03:56:55 UTC",
        "source_pdf_bytes": 286244,
        "source_pdf_sha256": SOURCE_HASH,
        "stage": "INITIAL_SOURCE_ONLY",
        "statement": "Full classification under the printed axioms; no remaining mathematical gap. No priority assessment.",
    }
    require(seal == expected and set(seal) == set(expected), "initial seal literal schema/value mismatch")
    require(type(seal["candidate_exposure_before_seal"]) is bool and
            type(seal["completion_estimate_percent"]) is int and
            type(seal["manifest_bytes"]) is int and type(seal["source_pdf_bytes"]) is int,
            "initial seal strict scalar types")
    print(f"AUTH initial seal: bytes={len(seal_data)} SHA-256={sha256(seal_data).hexdigest()}")
    print(f"AUTH original source: bytes={len(source)} SHA-256={SOURCE_HASH}")
    print("INJECTION schema:", reject(lambda: manifest_schema({"files": {}}), "files must be a list"))
    first = manifest["files"][0]
    actual = (family / first["relative_path"]).read_bytes()
    corrupt = bytes([actual[0] ^ 1]) + actual[1:]
    print("INJECTION content:", reject(lambda: content_check(corrupt, first["bytes"],
          first["sha256"], first["relative_path"]), "member SHA-256"))


def meet_axioms(meet):
    n = len(meet)
    for x, y, z in product(range(n), repeat=3):
        require(meet[x][x] == x, "meet idempotence")
        require(meet[x][y] == meet[y][x], "meet commutativity")
        require(meet[meet[x][y]][z] == meet[x][meet[y][z]], "meet associativity")


def semilattices(n):
    """Enumerate symmetric idempotent operation tables, then test associativity.

    This uses operation tables, unlike the reconstruction's relation enumeration.
    """
    slots = list(combinations(range(n), 2))
    for entries in product(range(n), repeat=len(slots)):
        meet = [[x if x == y else None for y in range(n)] for x in range(n)]
        for (x, y), value in zip(slots, entries):
            meet[x][y] = meet[y][x] = value
        if all(meet[meet[x][y]][z] == meet[x][meet[y][z]]
               for x, y, z in product(range(n), repeat=3)):
            yield meet


def top_product(meet, e):
    return [[e if meet[x][y] == x else meet[x][y] for y in range(len(meet))]
            for x in range(len(meet))]


def units(op, e, diagonal=False):
    n = len(op)
    require(type(e) is int and 0 <= e < n, "absent distinguished point")
    for x in range(n):
        require(op[e][x] == x, f"left unit {x}")
        require(op[x][e] == e, f"right absorption {x}")
        if diagonal:
            require(op[x][x] == e, f"diagonal {x}")


def separation(op, e):
    for x, y in product(range(len(op)), repeat=2):
        require(((op[x][y] == e and op[y][x] == e) == (x == y)),
                f"separation {x,y}")


def mixed(meet, op):
    for x, y, z in product(range(len(meet)), repeat=3):
        require(op[meet[x][y]][z] == op[op[x][y]][op[x][z]], f"mixed identity {x,y,z}")


def semibrace(meet, op, e):
    units(op, e)
    mixed(meet, op)
    preservation(meet, op)


def preservation(meet, op):
    for x, y, z in product(range(len(meet)), repeat=3):
        require(op[x][meet[y][z]] == meet[op[x][y]][op[x][z]], f"meet preservation {x,y,z}")


def lalgebra(op, e):
    units(op, e, diagonal=True)
    separation(op, e)
    for x, y, z in product(range(len(op)), repeat=3):
        require(op[op[x][y]][op[x][z]] == op[op[y][x]][op[y][z]], f"cycloid {x,y,z}")


def constructed_check(meet, e):
    op = top_product(meet, e)
    semibrace(meet, op, e)
    lalgebra(op, e)
    for x, y in product(range(len(meet)), repeat=2):
        require((op[x][y] == e) == (meet[x][y] == x), "constructed order coincidence")


def partitions(length, prefix=(0,)):
    """Restricted growth words enumerate every set partition exactly once."""
    if len(prefix) == length:
        yield prefix
        return
    for value in range(max(prefix) + 2):
        yield from partitions(length, prefix + (value,))


def quotient_diagnostics():
    # F3 consists of the subsets of three generators. Meet is union; top is 0.
    # Every triple in a bounded meet-semilattice is the image of this algebra.
    seen = congruences = 0
    histogram = Counter()
    for labels in partitions(8):
        seen += 1
        if any(labels[i] == labels[j] and labels[i | k] != labels[j | k]
               for i, j, k in product(range(8), repeat=3)):
            continue
        congruences += 1
        n = max(labels) + 1
        representatives = [labels.index(a) for a in range(n)]
        meet = [[labels[representatives[a] | representatives[b]] for b in range(n)]
                for a in range(n)]
        meet_axioms(meet)
        constructed_check(meet, labels[0])
        histogram[n] += 1
    require(seen == 4140, f"partition enumeration incomplete: {seen}")
    print(f"F3 quotient diagnostics: partitions={seen}; congruences={congruences}; "
          f"quotient-size histogram={dict(sorted(histogram.items()))}: PASS")


def small_structure_search():
    # Every operation with the printed units and diagonal has exactly these free slots.
    tested = weak_accepted = simultaneous_accepted = non_top_tested = 0
    for n in range(1, 4):
        for meet in semilattices(n):
            for e in range(n):
                slots = [(x, y) for x, y in product(range(n), repeat=2)
                         if x != e and y != e and x != y]
                is_top = all(meet[x][e] == x for x in range(n))
                for values in product(range(n), repeat=len(slots)):
                    op = [[e for _ in range(n)] for _ in range(n)]
                    op[e] = list(range(n))
                    for (x, y), value in zip(slots, values):
                        op[x][y] = value
                    tested += 1
                    non_top_tested += not is_top
                    units(op, e, diagonal=True)
                    try:
                        separation(op, e)
                        mixed(meet, op)
                    except AuditFailure:
                        continue
                    weak_accepted += 1
                    require(is_top, "local necessity countermodel found")
                    # Check the direct local substitutions, separately from row comparisons.
                    for x in range(n):
                        a = meet[x][e]
                        require(op[a][x] == e and op[x][a] == e and a == x,
                                "direct local substitution discrepancy")
                    try:
                        semibrace(meet, op, e)
                        lalgebra(op, e)
                    except AuditFailure:
                        continue
                    simultaneous_accepted += 1
    print(f"Exhaustive n<=3 forced-unit/diagonal operation search: tables={tested}; "
          f"non-top tables={non_top_tested}; mixed+separation accepted={weak_accepted}; "
          f"full simultaneous accepted={simultaneous_accepted}; non-top accepted=0: PASS")


def independent_finite_constructions():
    counts = []
    projection_points = top_points = 0
    for n in range(1, 5):
        count = 0
        for meet in semilattices(n):
            count += 1
            meet_axioms(meet)
            for e in range(n):
                semibrace(meet, [list(range(n)) for _ in range(n)], e)
                projection_points += 1
                if all(meet[x][e] == x for x in range(n)):
                    constructed_check(meet, e)
                    top_points += 1
        counts.append(count)
    require(counts == [1, 2, 9, 76], f"independent meet enumeration counts: {counts}")
    require(projection_points == 336 and top_points == 45, "construction coverage totals")
    print(f"Independent meet-table enumeration: counts={counts}; projection points={projection_points}; "
          f"top constructions={top_points}: PASS")


def hypothesis_and_fault_checks():
    meet2 = [[0, 0], [0, 1]]
    op2 = top_product(meet2, 1)
    constructed_check(meet2, 1)
    require(op2[0][0] == op2[0][1] and op2[0] != op2[1],
            "index injectivity versus individual map injectivity witness")
    print("Hypothesis witness: valid two-point simultaneous structure has noninjective L_0; distinct rows.")
    require(len({op2[0][x] for x in range(2) if meet2[x][0] == x}) < 2,
            "self-similarity counterwitness")
    print("Hypothesis witness: same structure is not self-similar (principal ideal at 0 has size 1).")
    semibrace(meet2, [[0, 1], [0, 1]], 0)
    print("Hypothesis witness: projection semibrace permits prescribed bottom as distinguished point.")
    meet_m3 = [[x if x == y else (y if x == 4 else (x if y == 4 else 0))
                for y in range(5)] for x in range(5)]
    meet_axioms(meet_m3)
    constructed_check(meet_m3, 4)
    order_only = [[4 if meet_m3[x][y] == x else y for y in range(5)] for x in range(5)]
    print("INJECTION replace meet output by y:", reject(
        lambda: preservation(meet_m3, order_only), "meet preservation"))
    corrupt = [row[:] for row in op2]
    corrupt[1][0] = 1
    print("INJECTION corrupt unit:", reject(lambda: semibrace(meet2, corrupt, 1), "left unit"))
    print("INJECTION absent point:", reject(lambda: semibrace([], [], 0), "absent distinguished point"))
    print("INJECTION falsely promote projection to L:", reject(
        lambda: lalgebra([[0, 1], [0, 1]], 1), "diagonal"))


def main():
    print("Independent adversarial checker; finite diagnostics do not replace the written proof.")
    authenticate()
    independent_finite_constructions()
    quotient_diagnostics()
    small_structure_search()
    hypothesis_and_fault_checks()
    print("ALL ADVERSARIAL CHECKS PASSED")


if __name__ == "__main__":
    main()
