#!/usr/bin/env python3
"""Independent, standard-library replay of the frozen 30003264 author packet.

Usage: python3 -I -B independent_verify.py AUTHOR_PACKET.zip
The external digest is the trust anchor. This verifies finite calculations and
package integrity, not imported theorems or general arithmetic-group homology.
"""
import ast
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ARCHIVE_BYTES = 23595
ARCHIVE_SHA256 = "7e96c5992aa3d18ae6a00a78dd9bb373126410fa6b3fabba6280bb3e20cd0c2b"
NAMES = {"CONTROL_RESULTS.json", "LITERATURE.md", "MANIFEST.json", "PROOF.md",
         "README.md", "RESEARCH_LOG.md", "SOURCE_VERIFICATION.json", "controls.py", "verify.py"}
MANIFEST_SHA256 = "00d7c6e2159fc100af50d28f933eb0be886af80551e02119bd4fca8c63275ecd"


def check(value, description):
    if not value:
        raise ValueError(description)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        check(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def archive_anchor(data):
    check(len(data) == ARCHIVE_BYTES and digest(data) == ARCHIVE_SHA256,
          "external frozen archive mismatch")


def envelope(root):
    check({p.name for p in root.iterdir()} == NAMES, "exact file inventory")
    check(all(p.is_file() and not p.is_symlink() for p in root.iterdir()), "regular files only")
    check(digest((root / "MANIFEST.json").read_bytes()) == MANIFEST_SHA256, "pinned manifest")
    manifest = json.loads((root / "MANIFEST.json").read_text(), object_pairs_hook=unique_object)
    check(type(manifest["format"]) is int and manifest["format"] == 1, "manifest format")
    check(type(manifest["problem_id"]) is int and manifest["problem_id"] == 30003264, "problem identity")
    check(set(manifest["files"]) == NAMES - {"MANIFEST.json"}, "manifest inventory")
    for name, meta in manifest["files"].items():
        content = (root / name).read_bytes()
        check(meta == {"bytes": len(content), "sha256": digest(content)}, "file digest: " + name)
    return manifest


def execute(path, optimized=False):
    p = subprocess.run([sys.executable, "-I", "-B", *(["-O"] if optimized else []), str(path)],
                       cwd=path.parent, capture_output=True, timeout=120)
    return p


def det3(a):
    return sum((-1 if perm in ((0, 2, 1), (1, 0, 2), (2, 1, 0)) else 1)
               * a[0][perm[0]] * a[1][perm[1]] * a[2][perm[2]]
               for perm in itertools.permutations(range(3)))


def lattice_coordinates(vector, basis):
    # Solve the transposed basis system by independently implemented elimination.
    m = [[Fraction(basis[col][row]) for col in range(3)] + [Fraction(vector[row])]
         for row in range(3)]
    for i in range(3):
        pivot = next(k for k in range(i, 3) if m[k][i])
        m[i], m[pivot] = m[pivot], m[i]
        scale = m[i][i]
        m[i] = [x / scale for x in m[i]]
        for k in range(3):
            if k != i:
                scale = m[k][i]
                m[k] = [x - scale * y for x, y in zip(m[k], m[i])]
    return [m[i][3] for i in range(3)]


def independent_residue():
    # Use the algebraically equivalent fourth symbol y(x-1)/(x(y-1)).
    rows = []
    for x in (2, 3, 4):
        for y in (2, 3, 4):
            if x == y:
                continue
            symbols = [x, y, y * pow(x, -1, 5) % 5,
                       y * (x - 1) * pow(x * (y - 1) % 5, -1, 5) % 5,
                       (1 - x) * pow((1 - y) % 5, -1, 5) % 5]
            row = [0, 0, 0]
            for s, sign in zip(symbols, [1, -1, 1, -1, 1]):
                check(s in (2, 3, 4), "admissible symbol")
                row[s - 2] += sign
            rows.append(row)
    basis = [rows[0], rows[1], rows[3]]
    canonical = [[0, 0, 1], [1, -2, 0], [0, 6, 0]]
    check(abs(det3(basis)) == 6, "index six")
    # Certify both inclusions of the entire integer relation lattice.
    for vector in rows:
        check(all(c.denominator == 1 for c in lattice_coordinates(vector, canonical)),
              "raw relation belongs to canonical lattice")
    for vector in canonical:
        check(all(c.denominator == 1 for c in lattice_coordinates(vector, basis)),
              "canonical relation belongs to raw lattice")
    homs = [values for values in itertools.product(range(6), repeat=3)
            if all(sum(x*y for x, y in zip(row, values)) % 6 == 0 for row in rows)]
    check(len(homs) == 6 and (2, 1, 0) in homs, "cyclic quotient certificate")
    check({(2 * a + b) % 6 for a, b in itertools.product(range(6), repeat=2)} == set(range(6)),
          "surjective quotient map")
    return {"five_term_relations": rows, "mutual_integer_lattice_inclusions": True,
            "integral_cyclic_order": 6, "half_integral_cyclic_order": 3,
            "homomorphisms_to_Z6": len(homs)}


def independent_linear_controls():
    pairs = list(itertools.product(range(3), repeat=2))
    k = [v for v in pairs if sum(v) % 3 == 0]
    res = lambda v: (v[0] - v[1]) % 3
    check(len(k) == 3 and {res(v) for v in k} == {0, 1, 2}, "small-S kernel isomorphism")
    check([v for v in k if not res(v)] == [(0, 0)], "joint kernel zero")
    check({sum(v) % 3 for v in k} == {0}, "wrong residue map fails")
    count = 0
    for n in range(1, 40, 2):
        for a, b in itertools.product(range(n), repeat=2):
            if (a + b) % n == 0:
                check((a - b) % n == (-2 * b) % n, "normalization")
                check(((a - b) % n == 0) == (b == 0), "localized kernels")
                count += 1
    check((-2) % 2 == 0, "characteristic-two control")
    stage_count = 0
    for n in range(1, 8):
        zero = (0,) * n
        old_kernel = [zero + (e,) for e in range(3)]
        transition = lambda v: v[:-1] + (0, 0)
        check(all(transition(v) == (0,) * (n + 2) for v in old_kernel), "old kernels die")
        new_kernel = (0,) * (n + 1) + (1,)
        check(new_kernel != (0,) * (n + 2), "new kernel nonzero")
        for v in itertools.product(range(3), repeat=n + 1):
            check(transition(v)[:-1] == v[:-1] + (0,), "commutative projection square")
        stage_count += 1
    return {"small_S_residue_bijection": True, "wrong_residue_rejected": True,
            "normalization_cases": count, "odd_moduli_through": 39,
            "two_primary_shortcut_rejected": True, "limit_stages": stage_count,
            "abstract_kernel_persistence_verified": True}


def independent_projectors():
    count = 0
    for rank in range(1, 6):
        order = 2 ** rank
        rows = [[(-1) ** ((g & chi).bit_count()) for g in range(order)] for chi in range(order)]
        check([sum(r[g] for r in rows) for g in range(order)] == [order] + [0]*(order - 1),
              "projectors sum to identity")
        for chi, psi, g in itertools.product(range(order), repeat=3):
            convolution = sum(rows[chi][h] * rows[psi][g ^ h] for h in range(order))
            check(convolution == (order * rows[chi][g] if chi == psi else 0),
                  "group-algebra orthogonal idempotents")
            count += 1
    # Action characters of (sign, first prime, second prime): sign acts trivially.
    source_characters = [(0, 1, 0), (0, 0, 1), (0, 1, 1)]
    target_characters = source_characters[:2]
    for chi in target_characters:
        check(source_characters.count(chi) == target_characters.count(chi), "supported comparison")
    check(source_characters.count((0, 1, 1)) == 1 and (0, 1, 1) not in target_characters,
          "mixed-character countermodel")
    return {"coefficientwise_convolution_checks": count, "largest_squareclass_rank": 5,
            "sign_generator_included_in_mixed_control": True, "target_only_test_rejected": True}


def mutation_controls(root, temporary):
    alterations = {
        "missing_proof": lambda p: (p / "PROOF.md").unlink(),
        "extra_file": lambda p: (p / "unlisted.txt").write_text("synthetic control"),
        "modified_proof": lambda p: (p / "PROOF.md").write_text("synthetic replacement"),
        "modified_verifier": lambda p: (p / "verify.py").write_text("print('false success')\n"),
        "nested_directory": lambda p: (p / "nested").mkdir(),
        "invalid_manifest": lambda p: (p / "MANIFEST.json").write_text("{"),
    }
    rejections = []
    for name, alter in alterations.items():
        p = temporary / name
        shutil.copytree(root, p)
        alter(p)
        try:
            envelope(p)
        except (ValueError, OSError, KeyError, TypeError):
            rejections.append(name)
        else:
            raise ValueError("mutation accepted: " + name)
    p = temporary / "rehashed_verifier"
    shutil.copytree(root, p)
    data = b"print('false success')\n"
    (p / "verify.py").write_bytes(data)
    m = json.loads((p / "MANIFEST.json").read_text())
    m["files"]["verify.py"] = {"bytes": len(data), "sha256": digest(data)}
    (p / "MANIFEST.json").write_text(json.dumps(m))
    try:
        envelope(p)
    except ValueError:
        rejections.append("rehashed_verifier")
    else:
        raise ValueError("rehashed verifier accepted")
    p = temporary / "symlink_proof"
    shutil.copytree(root, p)
    (p / "PROOF.md").unlink()
    (p / "PROOF.md").symlink_to(root / "PROOF.md")
    try:
        envelope(p)
    except ValueError:
        rejections.append("symlink_proof")
    else:
        raise ValueError("symlink accepted")
    # Independently trigger each substantive author arithmetic check under -O.
    original = (root / "controls.py").read_text()
    edits = {
        "bad_relation": ("expected = [[0, 0, 1]", "expected = [[0, 0, 2]"),
        "wrong_small_S_map": ("image = sorted({(x-y) % 3", "image = sorted({(x+y) % 3"),
        "wrong_normalization": ("evaluation == -2*delta % modulus", "evaluation == -delta % modulus"),
        "old_kernel_survives": ("transition = b + (0, 0)", "transition = b + (0, 1)"),
        "trivialized_characters": ("return -1 if (g & chi).bit_count() % 2 else 1", "return 1"),
    }
    math_rejections = []
    for name, (old, new) in edits.items():
        check(original.count(old) == 1, "unique mutation location")
        p = temporary / (name + ".py")
        p.write_text(original.replace(old, new))
        for optimized in (False, True):
            result = execute(p, optimized)
            check(result.returncode != 0 and b"ValueError" in result.stderr,
                  "arithmetic corruption must be rejected with and without -O")
        math_rejections.append(name)
    return {"independent_envelope_mutations_rejected": rejections,
            "arithmetic_mutations_rejected_in_both_modes": math_rejections}


def main():
    check(len(sys.argv) == 2, "supply the frozen author ZIP as the only argument")
    archive = Path(sys.argv[1]).read_bytes()
    archive_anchor(archive)
    for changed in (archive[:-1], archive + b"x", bytes([archive[0] ^ 1]) + archive[1:]):
        try:
            archive_anchor(changed)
        except ValueError:
            pass
        else:
            raise ValueError("damaged archive accepted")
    with tempfile.TemporaryDirectory(prefix="prebloch-independent-") as temporary:
        base = Path(temporary)
        root = base / "packet"
        root.mkdir()
        with zipfile.ZipFile(sys.argv[1]) as z:
            check(set(z.namelist()) == NAMES and len(z.namelist()) == len(NAMES), "ZIP inventory")
            check(z.testzip() is None, "ZIP checksums")
            for info in z.infolist():
                check(info.filename == Path(info.filename).name and not info.is_dir(), "flat safe ZIP")
                (root / info.filename).write_bytes(z.read(info))
        envelope(root)
        for name in ("controls.py", "verify.py"):
            check(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse((root / name).read_text()))),
                  "author checks must not be removable assertions")
        controls = []
        replays = []
        for optimized in (False, True):
            p = execute(root / "controls.py", optimized)
            check(p.returncode == 0 and not p.stderr and p.stdout == (root / "CONTROL_RESULTS.json").read_bytes(),
                  "author control replay")
            controls.append(p.stdout)
            p = execute(root / "verify.py", optimized)
            check(p.returncode == 0 and not p.stderr, "author verifier replay")
            replays.append(p.stdout)
        check(replays[0] == replays[1], "normal and optimized author verifier identical")
        replay = json.loads(replays[0])
        check(replay["damage_controls"]["rejected_count"] == 12, "all author damage cases")
        result = {"problem_id": 30003264, "archive_bytes": len(archive), "archive_sha256": digest(archive),
                  "frozen_inventory_count": len(NAMES), "archive_mutations_rejected": 3,
                  "author_damage_controls_rejected": 12, "normal_optimized_author_replays_identical": True,
                  "independent_residue": independent_residue(),
                  "independent_linear_controls": independent_linear_controls(),
                  "independent_projectors": independent_projectors(),
                  "mutations": mutation_controls(root, base),
                  "scope": "Integrity and finite controls only; primary problem remains unresolved."}
        print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
