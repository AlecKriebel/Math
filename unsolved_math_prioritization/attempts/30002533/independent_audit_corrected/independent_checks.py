#!/usr/bin/env python3
"""Independent bounded audit controls. No theorem prover and no network access.

The external digest below binds the original author submission. Source files are
optional, privately obtained inputs; neither their contents nor their paths enter
the output. All mutation tests operate only on disposable copies.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

EXPECTED_MANIFEST = "e4a387aec4351158d9b723f72122831696b4901ee4f721f94239bff5a4bde7fe"
EXPECTED_FILES = {
    "APPROACH_LOG.md", "AUTHOR_VALIDATION.json", "MATH_RECEIPT.json",
    "PROOF.md", "README.md", "SOURCE_SCOPE.md", "SOURCE_VERIFICATION.json",
    "STATUS.json", "verify.py",
}


def digest(path):
    state = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            state.update(block)
    return state.hexdigest()


def bind(root):
    for p in root.rglob("*"):
        if p.is_symlink():
            raise ValueError("symlink forbidden")
    m = root / "MANIFEST.json"
    if digest(m) != EXPECTED_MANIFEST:
        raise ValueError("externally bound manifest digest differs")
    entries = json.loads(m.read_text())["files"]
    names = [e["path"] for e in entries]
    if len(names) != len(set(names)) or set(names) != EXPECTED_FILES:
        raise ValueError("manifest payload identity differs")
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    if actual != EXPECTED_FILES | {"MANIFEST.json"}:
        raise ValueError("actual file set differs")
    for e in entries:
        p = root / e["path"]
        if p.stat().st_size != e["bytes"] or digest(p) != e["sha256"]:
            raise ValueError("payload content differs")
    return {"result": "PASS", "externally_bound_manifest_sha256": EXPECTED_MANIFEST,
            "payload_count": len(entries), "files": entries}


def arithmetic():
    q = Fraction
    S = (q(1), q(1, 2), q(1, 3), q(1, 5), q(1, 7))
    L = q(3, 13)
    rows = []

    def check(name, truth):
        if not truth:
            raise ValueError(name)
        rows.append({"check": name, "result": "PASS"})

    gaps = {str(s): str(abs(L-s)) for s in S}
    check("minimum separation derived from old set", min(abs(L-s) for s in S) == q(2, 65))
    radius = min(abs(L-s) for s in S) / 2
    low, high = L-radius, L+radius
    check("independently derived interval endpoints", (low, high) == (q(14, 65), q(16, 65)))
    check("interval excludes every old value", all(not low < s < high for s in S))
    check("interval is strictly normalized", 0 < low < L < high < 1)
    check("limit differs from every old value", L not in S)
    check("reciprocal would violate normalization", 1/L > 1)

    for x in (q(1, 4), L):
        w = (x-q(1, 5))/(q(1, 3)-q(1, 5))
        check("new average can consist only of old values: "+str(x),
              0 < w < 1 and w*q(1, 3)+(1-w)*q(1, 5) == x and x not in S)
    check("one quarter mixing weight", (q(1, 4)-q(1, 5))/(q(1, 3)-q(1, 5)) == q(3, 8))
    check("limit mixing weight", (L-q(1, 5))/(q(1, 3)-q(1, 5)) == q(3, 13))
    # An abstract non-attaining sequence, not a sequence of geometric examples.
    check("convergence does not force a term to equal the limit",
          all(L+q(1, n+100) != L for n in range(1, 65)))
    check("abstract convergent sequence eventually lies in interval",
          all(low < L+q(1, n+100) < high for n in range(1, 65)))
    # All possible dimension/rank/relative-dimension pairs under the two separate hypotheses.
    proper = [(r, rel, 2*r+rel) for r in range(1, 3) for rel in range(3)
              if 2*r+rel < 4 and rel == 0]
    check("rank and rel arithmetic leaves only dimension two", proper == [(1, 0, 2)])
    without_rel_zero = [(r, rel, 2*r+rel) for r in range(1, 3) for rel in range(3)
                        if 2*r+rel < 4]
    check("dimension-three obstruction survives without rel zero", (1, 1, 3) in without_rel_zero)
    check("rel zero without symplectic parity would allow dimension three", 3 in range(2, 4))
    for d, e in ((2, 7), (5, 3), (18, 11)):
        # Model two different curve covering degrees with a common upstairs degree pair.
        u, v = q(11, 15), q(7, 2)
        check("common-cover ratio survives unequal degrees: %s,%s" % (d, e),
              (u/d)/(v/d) == (u/e)/(v/e) == u/v)
    check("Prym label is not the sorted full second exponent",
          sorted([q(1), q(1, 2), q(2, 5), L], reverse=True)[1] != L)
    check("changing block labels can preserve a full spectrum",
          sorted([q(1), q(1, 2), q(1, 3), q(1, 5)]) ==
          sorted([q(1), q(1, 3), q(1, 2), q(1, 5)]))
    return {"result": "PASS_EXACT_ABSTRACT_CONTROLS", "count": len(rows),
            "checks": rows, "distances": gaps, "interval": [str(low), str(high)],
            "formal_theorem_verification": False, "geometric_examples_generated": False}


def sources(root, source_dir):
    entries = json.loads((root/"SOURCE_VERIFICATION.json").read_text())["sources"]
    if source_dir is None:
        return {"result": "NOT_RUN_MISSING_SOURCES", "source_count": len(entries)}
    if any(not (source_dir/e["local_basename"]).exists() for e in entries):
        return {"result": "NOT_RUN_MISSING_SOURCES", "source_count": len(entries)}
    rows = []
    for e in entries:
        p = source_dir/e["local_basename"]
        if p.is_symlink() or p.stat().st_size != e["bytes"] or digest(p) != e["sha256"]:
            raise ValueError("independent source integrity mismatch")
        with p.open("rb") as f:
            if f.read(5) != b"%PDF-":
                raise ValueError("source is not a PDF")
        rows.append({"key": e["key"], "bytes": p.stat().st_size, "sha256": digest(p)})
    return {"result": "PASS_EXACT_SOURCE_BYTES", "source_count": len(rows), "sources": rows,
            "formal_theorem_verification": False}


def replay(root, args=()):
    p = subprocess.run([sys.executable, "-B", str(root/"verify.py"), *map(str, args)],
                       capture_output=True, text=True)
    try:
        result = json.loads(p.stdout)
    except json.JSONDecodeError:
        result = {"result": "NON_JSON_OUTPUT"}
    return {"exit_code": p.returncode, "output": result}


def mutation_controls(root, source_dir):
    rows = []
    with tempfile.TemporaryDirectory(prefix="gothic-audit-controls-") as tmp:
        tmp = Path(tmp)
        def candidate_case(name, mutator, author_exit=1):
            c = tmp/name
            shutil.copytree(root, c)
            mutator(c)
            rejected = False
            try:
                bind(c)
            except (ValueError, OSError, KeyError, json.JSONDecodeError):
                rejected = True
            if not rejected:
                raise ValueError("negative candidate accepted: "+name)
            actual = replay(c)["exit_code"]
            if actual != author_exit:
                raise ValueError("unexpected author-checker exit: "+name)
            rows.append({"control": name, "independent_binding": "REJECTED_AS_REQUIRED",
                         "author_checker_exit": actual})

        def flip(p):
            b = p.read_bytes()
            p.write_bytes(bytes([b[0] ^ 1])+b[1:])

        candidate_case("same_size_payload_mutation", lambda c: flip(c/"PROOF.md"))
        candidate_case("unexpected_payload", lambda c: (c/"UNEXPECTED.txt").write_text("control\n"))
        candidate_case("missing_payload", lambda c: (c/"README.md").unlink())
        candidate_case("renamed_payload", lambda c: (c/"README.md").rename(c/"RENAMED.md"))
        def symlink_payload(c):
            (c/"README.md").unlink()
            (c/"README.md").symlink_to(root/"README.md")
        candidate_case("symlink_payload", symlink_payload)
        candidate_case("extra_directory_symlink", lambda c: (c/"LINK").symlink_to(root, target_is_directory=True))
        candidate_case("manifest_whitespace_change", lambda c: (c/"MANIFEST.json").write_bytes(
            (c/"MANIFEST.json").read_bytes()+b"\n"), 2)
        def coordinated(c):
            flip(c/"PROOF.md")
            m = json.loads((c/"MANIFEST.json").read_text())
            for e in m["files"]:
                if e["path"] == "PROOF.md": e["sha256"] = digest(c/"PROOF.md")
            (c/"MANIFEST.json").write_text(json.dumps(m, indent=2)+"\n")
        candidate_case("coordinated_payload_manifest_change", coordinated, 2)
        if source_dir is not None:
            meta = json.loads((root/"SOURCE_VERIFICATION.json").read_text())["sources"]
            def source_case(name, mutator, expected_exit, expected_result):
                d = tmp/name
                d.mkdir()
                for e in meta: shutil.copyfile(source_dir/e["local_basename"], d/e["local_basename"])
                mutator(d, meta[0]["local_basename"])
                r = replay(root, ("--sources-dir", d))
                if r["exit_code"] != expected_exit:
                    raise ValueError("unexpected source-control exit: "+name)
                output = r["output"]
                result = output.get("sources", output).get("result")
                if result != expected_result:
                    raise ValueError("unexpected source-control result: "+name)
                rows.append({"control": name, "author_checker_exit": expected_exit, "result": result})
            source_case("source_same_size_mutation", lambda d,n: flip(d/n), 1, "FAIL")
            source_case("source_missing_one", lambda d,n: (d/n).unlink(), 2, "NOT_RUN_MISSING_SOURCES")
            def source_link(d, n):
                (d/n).unlink(); (d/n).symlink_to(source_dir/n)
            source_case("source_symlink", source_link, 1, "FAIL")
    return {"result": "PASS", "count": len(rows), "controls": rows,
            "all_mutations_used_disposable_copies": True,
            "self_consistent_manifest_requires_external_binding": True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate-dir", type=Path, required=True)
    ap.add_argument("--sources-dir", type=Path)
    ap.add_argument("--mutations", action="store_true")
    args = ap.parse_args()
    root = args.candidate_dir.resolve()
    result = {"binding": bind(root), "arithmetic": arithmetic(),
              "independent_source_bytes": sources(root, args.sources_dir)}
    result["author_math_only_replay"] = replay(root, ("--math-only",))
    result["author_portable_replay"] = replay(root)
    if result["author_math_only_replay"]["exit_code"] != 0:
        raise ValueError("math-only replay failed")
    if result["author_portable_replay"]["exit_code"] != 2:
        raise ValueError("source-free replay did not preserve NOT_RUN semantics")
    if args.sources_dir is not None:
        result["author_full_source_replay"] = replay(root, ("--sources-dir", args.sources_dir))
        if result["author_full_source_replay"]["exit_code"] != 0:
            raise ValueError("full-source replay failed")
    if args.mutations:
        result["adversarial_mutations"] = mutation_controls(root, args.sources_dir)
    result["final_candidate_binding"] = bind(root)
    result["mathematical_proof_established_by_script"] = False
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["independent_source_bytes"]["result"] == "PASS_EXACT_SOURCE_BYTES" else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        print(json.dumps({"result": "FAIL", "error": str(error)}, sort_keys=True))
        sys.exit(1)
