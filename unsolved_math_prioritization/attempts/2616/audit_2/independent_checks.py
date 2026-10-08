#!/usr/bin/env python3
"""Independent set-based finite checks and frozen-packet execution controls.

This does not import the candidate verifier, simulate a free ultrafilter, or
mechanize the infinite proof. Supply the frozen public and external directories.
"""
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


PINS = {
    "MANIFEST.json": "31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c",
    "bootstrap.py": "054dbe643ad4f78f13ea0595e4cab5379d438a33ab2fd2f6aed9f5125d9dcb57",
    "test_harness.py": "5c6d1056179a95c647db5cc11028059c64c5abcdcabd69790cef892948c9ca27",
    "PINS.json": "cbf61f7d4163f50d15eb264e779bb79c9fc8a0566b571f0d9d9a3bf3fd96634d",
}
PUBLIC = {
    "README.md": (1575, "98a106326df13cdab1b46094dab21565dd86519546246c34d943156a7f67f5a5"),
    "REPORT.md": (9338, "ddde58f03f320c881b78e59b60a40f315e1811c7c88aaa25ce620c427afbb6ca"),
    "fixtures.json": (276, "cc8769655ddc787fe8446f78f24afd3d27dac6c4e393932418b0846e2eba1581"),
    "provenance.json": (1065, "d16faf5c48ca84bff4df008c8c9a7df40da8b8b43c025b6edc900ed1448392bb"),
    "sources.json": (2647, "3fd2c18b83be32c4579c63917c1907b2970508b805dace66e2eadfb818cc43d8"),
    "verify.py": (6773, "b805650e49c5096f0fe368653122989c1087f59447871a5cb6fc32843d6983d1"),
}
EXPECTED_COUNTS = {
    "group_and_coset_cases": 16 ** 3,
    "maximum_fibers": 13,
    "dense_coloring_extensions": 256 * 6 * sum(range(1, 6)),
    "finite_disjoint_block_assignments": 4 ** 7,
}


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def finite_subsets(n):
    return [frozenset(c) for k in range(n + 1)
            for c in itertools.combinations(range(n), k)]


def v2(n):
    check(type(n) is int and n > 0, "positive integer required")
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def independent_mathematics():
    universe = finite_subsets(4)
    groups = {a: frozenset(s for s in universe if s <= a) for a in universe}
    triple_count = 0
    for s, t, u in itertools.product(universe, repeat=3):
        check((s ^ t) ^ u == s ^ (t ^ u), "associativity")
        check(s ^ t == t ^ s and (s ^ t) ^ t == s, "Boolean identities")
        triple_count += 1
    intersection_count = 0
    for a, b, s, t in itertools.product(universe, repeat=4):
        coset1 = frozenset(s ^ u for u in groups[a])
        coset2 = frozenset(t ^ u for u in groups[b])
        intersection = coset1 & coset2
        if intersection:
            x = next(iter(intersection))
            check(intersection == frozenset(x ^ u for u in groups[a & b]),
                  "mixed-subgroup coset intersection")
        intersection_count += 1
    for k in range(16):
        fiber = [s | {k} for s in finite_subsets(k)]
        check(len(fiber) == 2 ** k and all(max(s) == k for s in fiber),
              "maximum fiber")
        check(len(set(fiber)) == 2 ** k, "fiber enumeration is injective")
    extension_count = 0
    for s in finite_subsets(8):
        for color in range(8):
            scale = 2 ** color
            r = max(0, (len(s) + 1 - scale + 2 * scale - 1) // (2 * scale))
            q = scale * (2 * r + 1) - 1
            check(q >= len(s) and v2(q + 1) == color, "explicit coloring size")
            for period in range(1, 8):
                for residue in range(period):
                    added = set()
                    progression = itertools.count(residue, period)
                    while len(added) < q - len(s):
                        n = next(progression)
                        if n not in s:
                            added.add(n)
                    check(not s & added and len(s ^ added) == q, "dense extension")
                    check(v2(len(s ^ added) + 1) == color, "extension color")
                    check(all((n - residue) % period == 0 for n in added),
                          "extension in prescribed progression")
                    extension_count += 1
    small_group = finite_subsets(3)  # Includes the group identity.
    block_count = 0
    for assignment in itertools.product(range(4), repeat=len(small_group)):
        blocks = [set() for _ in range(3)]
        for element, label in zip(small_group, assignment):
            if label:
                blocks[label - 1].add(element)
        for k in range(3):
            occurrences = sum(any(s and max(s) == k for s in block) for block in blocks)
            check(occurrences <= 2 ** k, "point-finite fiber bound")
        # The proof omits every index through the sole identity-containing block.
        start = 0
        for n, block in enumerate(blocks):
            if frozenset() in block:
                start = n + 1
        chosen = []
        used = set()
        for n in range(start, len(blocks)):
            maxima = {max(s) for s in blocks[n]}
            if maxima and maxima.isdisjoint(used):
                chosen.append((n, maxima))
                used |= maxima
        parity_sets = [set(), set()]
        for i, (_, maxima) in enumerate(chosen):
            parity_sets[i % 2] |= maxima
        check(parity_sets[0].isdisjoint(parity_sets[1]), "disjoint parity unions")
        for parity, excluded in enumerate(parity_sets):
            allowed = set(range(3)) - excluded
            for i, (n, _) in enumerate(chosen):
                if i % 2 == parity:
                    check(all(not s <= allowed for s in blocks[n]), "whole-block exclusion")
        block_count += 1
    return {"set_based_group_triples": triple_count,
            "mixed_subgroup_coset_intersections": intersection_count,
            "maximum_fibers": 16,
            "set_based_coloring_extensions": extension_count,
            "disjoint_block_assignments_including_identity": block_count}


def snapshot(root):
    return {p.name: (len(p.read_bytes()), sha(p.read_bytes()))
            for p in root.iterdir() if p.is_file()}


def rejection_inputs(fixture):
    obj = json.loads(fixture)
    variants = []
    for key in sorted(obj):
        for kind, bad in [("boolean", True), ("float", float(obj[key])),
                          ("negative", -1), ("off_by_one", obj[key] + 1),
                          ("string", str(obj[key])), ("null", None),
                          ("list", [obj[key]]), ("object", {"value": obj[key]})]:
            changed = dict(obj)
            changed[key] = bad
            variants.append((key + ":" + kind, json.dumps(changed).encode()))
    for label, replacement in [("positive_infinity", b"Infinity"),
                               ("negative_infinity", b"-Infinity"),
                               ("nan", b"NaN"), ("float_overflow", b"1e9999"),
                               ("huge_integer", b"9" * 10000)]:
        variants.append((label, fixture.replace(b'"problem_id": 2616',
                                               b'"problem_id": ' + replacement)))
    variants += [("duplicate_key", fixture.replace(b'"schema_version": 1',
                    b'"schema_version": 1, "schema_version": 1')),
                 ("oversized", b" " * 65537), ("empty", b""),
                 ("invalid_utf8", b"\xff"), ("trailing", fixture + b"{}"),
                 ("nonobject", b"[]")]
    return variants


def execution_checks(public, external):
    check(os.getuid() != 0 and os.geteuid() != 0, "nonroot execution required")
    check(snapshot(public) == PUBLIC, "independent frozen public pins mismatch")
    for name, expected in PINS.items():
        check(sha((external / name).read_bytes()) == expected, "external pin mismatch")
    fixture = (public / "fixtures.json").read_bytes()
    code = (public / "verify.py").read_bytes().decode()
    bad_inputs = rejection_inputs(fixture)
    output = []
    with tempfile.TemporaryDirectory(prefix="second_independent_audit_") as temp:
        work = Path(temp)
        marker = work / "hostile_import_executed"
        for module in ("sitecustomize", "usercustomize", "json", "math", "itertools"):
            (work / (module + ".py")).write_text(
                "raise RuntimeError('hostile module must never execute')\n")
        env = dict(os.environ)
        env.update(PYTHONPATH=str(work), PYTHONSTARTUP=str(work / "sitecustomize.py"),
                   TMPDIR=str(public), PYTHONDONTWRITEBYTECODE="1")
        # Probe the actual frozen directory, not just mode bits or a copied tree.
        try:
            with (public / "fixtures.json").open("ab") as stream:
                stream.write(b"")
        except PermissionError:
            pass
        else:
            raise RuntimeError("actual frozen fixture unexpectedly writable")
        probe = public / "SECOND_AUDIT_WRITE_PROBE"
        try:
            probe.touch(exist_ok=False)
        except PermissionError:
            pass
        else:
            probe.unlink()
            raise RuntimeError("actual frozen directory unexpectedly writable")
        for mode, flags in [("normal", []), ("O", ["-O"]), ("OO", ["-OO"])]:
            cmd = [sys.executable, "-I", "-B", *flags, "-c", code, "--stdin"]
            positive = subprocess.run(cmd, input=fixture, capture_output=True,
                                      cwd=work, env=env, timeout=60)
            check(positive.returncode == 0, "positive checker failed")
            result = json.loads(positive.stdout)
            check(result == {"ok": True, "problem_id": 2616, "exact_finite_checks": True,
                 "infinite_proof_mechanized": False, "free_ultrafilter_simulated": False,
                 "counts": EXPECTED_COUNTS}, "exact verifier result mismatch")
            for label, malformed in bad_inputs:
                rejected = subprocess.run(cmd, input=malformed, capture_output=True,
                                          cwd=work, env=env, timeout=60)
                check(rejected.returncode != 0, "accepted hostile fixture: " + label)
                check(json.loads(rejected.stderr)["ok"] is False,
                      "unstructured hostile rejection: " + label)
            boot = subprocess.run([sys.executable, "-I", "-B", *flags,
                 str(external / "bootstrap.py"), str(public),
                 str(external / "MANIFEST.json"), PINS["MANIFEST.json"], mode],
                 capture_output=True, cwd=work, env=env, timeout=60)
            check(boot.returncode == 0, "bootstrap failed")
            boot_result = json.loads(boot.stdout)
            check(boot_result["euid"] == os.geteuid() and boot_result["euid"] != 0,
                  "bootstrap must actually be nonroot")
            check(boot_result["verifier_result"] == result, "bootstrap result mismatch")
            output.append({"mode": mode, "positive_counts": result["counts"],
                           "malformed_variants_rejected": len(bad_inputs),
                           "snapshot_bootstrap_passed": True})
        check(not marker.exists(), "unexpected hostile marker")
    check(snapshot(public) == PUBLIC, "author freeze changed during audit")
    return {"uid": os.getuid(), "euid": os.geteuid(),
            "actual_frozen_existing_file_write_denied": True,
            "actual_frozen_directory_create_denied": True,
            "externally_pinned_author_tools": PINS,
            "author_public_files_unchanged": True, "modes": output,
            "rejected_variant_labels": [label for label, _ in bad_inputs]}


def main():
    check(len(sys.argv) == 3, "usage: independent_checks.py PUBLIC EXTERNAL")
    public, external = (Path(p).resolve() for p in sys.argv[1:])
    result = {"schema_version": 1, "ok": True, "problem_id": 2616,
              "python_version": sys.version.split()[0],
              "infinite_proof_mechanized": False, "free_ultrafilter_simulated": False,
              "independent_mathematics": independent_mathematics(),
              "independent_execution_controls": execution_checks(public, external)}
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
