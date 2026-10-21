#!/usr/bin/env python3
"""Private-copy boundary probes of the previously read PR 883 checkers.

An 'accepted' result on a named probe is deliberately retained; this program
does not equate every accepted probe with an incorrect mathematical claim.
"""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
BASELINE = HERE / "private_replay" / "baseline path with spaces"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def import_read_code(path, name):
    # These two complete code bodies were inspected before execution. Import
    # executes their definitions but their main guards prevent CLI side effects.
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    publication = import_read_code(BASELINE / "check_publication.py", "pr883_publication")
    author = import_read_code(BASELINE / "author/verify.py", "pr883_author")
    original = json.loads((BASELINE / "author/certificate.json").read_text())
    rows = []

    def invoke(label, function, expected_accept, category):
        try:
            result = function()
        except Exception as exc:
            accepted = False
            detail = type(exc).__name__ + ": " + str(exc)
        else:
            accepted = True
            detail = result
        need(accepted is expected_accept, "unexpected probe outcome: " + label)
        rows.append({"probe": label, "category": category, "accepted": accepted, "detail": detail})

    invoke("baseline whole publication", lambda: publication.integrity(BASELINE), True, "positive")
    invoke("baseline author manifest", lambda: author.verify_manifest(BASELINE / "author"), True, "positive")
    invoke("baseline certificate", lambda: author.verify(original), True, "positive")

    with tempfile.TemporaryDirectory(prefix="boundary_", dir=HERE / "private_replay") as temporary:
        temporary = Path(temporary)
        counter = 0

        def fixture():
            nonlocal counter
            counter += 1
            directory = temporary / str(counter)
            shutil.copytree(BASELINE, directory, copy_function=shutil.copyfile)
            return directory

        mutations = [
            ("same-size proof corruption", "author/PROOF.md", "same"),
            ("appended proof", "author/PROOF.md", "append"),
            ("appended credit", "CREDIT_ADDENDUM.md", "append"),
            ("appended acceptance", "review2/ACCEPTANCE.json", "append"),
            ("appended archive", "archives/DIFFUSE_MASS_9900008_AUTHOR_SAFE_FREEZE.zip", "append"),
            ("appended second archive", "archives/DIFFUSE_MASS_9900008_FRESH_REVIEW_ACCEPTED_SAFE.zip", "append"),
            ("changed checker bytes", "check_publication.py", "append"),
            ("changed verifier bytes", "author/verify.py", "append"),
            ("missing certificate", "author/certificate.json", "delete"),
            ("unlisted root payload", "extra_payload.txt", "extra"),
        ]
        for label, name, method in mutations:
            directory = fixture()
            path = directory / name
            if method == "delete":
                path.unlink()
            elif method == "same":
                raw = path.read_bytes()
                path.write_bytes(bytes([raw[0] ^ 1]) + raw[1:])
            else:
                path.write_bytes((path.read_bytes() if method == "append" else b"") + b"changed\n")
            invoke(label, lambda directory=directory: publication.integrity(directory), False, "negative")

        directory = fixture()
        target = directory / "author/certificate.json"
        outside = temporary / "outside_certificate.json"
        outside.write_bytes(target.read_bytes())
        target.unlink()
        target.symlink_to(outside)
        invoke("whole publication rejects symlink payload", lambda: publication.integrity(directory), False, "negative")
        invoke("author-only integrity accepts same-byte symlink", lambda: author.verify_manifest(directory / "author"), True, "documented_boundary")

        directory = fixture()
        (directory / "unused-empty-directory").mkdir()
        invoke("whole publication ignores empty extra directory", lambda: publication.integrity(directory), True, "documented_boundary")

        directory = fixture()
        extra = directory / "author/unused-directory"
        extra.mkdir()
        (extra / "payload.txt").write_text("unlisted nested payload\n")
        invoke("author-only integrity ignores nested payload", lambda: author.verify_manifest(directory / "author"), True, "documented_boundary")
        invoke("whole publication detects nested payload", lambda: publication.integrity(directory), False, "negative")

        directory = fixture()
        outside_empty = temporary / "empty_target"
        outside_empty.mkdir()
        (directory / "extra-directory-link").symlink_to(outside_empty, target_is_directory=True)
        invoke("whole publication ignores symlink to empty extra directory", lambda: publication.integrity(directory), True, "documented_boundary")

        directory = fixture()
        path = directory / "PUBLICATION_MANIFEST.json"
        raw = path.read_text()
        path.write_text('{"schema":"INVALID_SHADOWED_SCHEMA",' + raw.lstrip()[1:])
        invoke("whole publication accepts duplicate manifest schema key", lambda: publication.integrity(directory), True, "documented_boundary")

        directory = fixture()
        # The outer manifest is intentionally not self-pinned. Its generic
        # checker accepts rewriting an unbound README and its corresponding
        # row. The immutable Git/source pin remains a separate trust anchor.
        path = directory / "README.md"
        path.write_bytes(path.read_bytes() + b"\ncoordinated edit\n")
        manifest_path = directory / "PUBLICATION_MANIFEST.json"
        manifest = json.loads(manifest_path.read_text())
        for row in manifest["files"]:
            if row["path"] == "README.md":
                row["bytes"] = path.stat().st_size
                row["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
        invoke("coordinated README and manifest edit passes internal layer", lambda: publication.integrity(directory), True, "expected_trust_boundary")

    semantic_mutations = [
        ("dimension boolean", "dimension", True, False),
        ("source count boolean", "source_coset_count", True, False),
        ("rational integer type", "period", 1, False),
        ("wrong probability", "shifted_heavy_root_probability", "1/3", False),
        ("equal weights", "line_weights", ["1", "1"], False),
        ("off-cell offset", "line_offsets", ["0", "1"], False),
        ("wrong covariance class", "equivariance", "almost_everywhere_unspecified", False),
        ("extra random background", "allocation_randomness", "independent_stationary_background", False),
        ("boolean labels compare equal to integer labels", "expected_preserving_target_labels", [[False, True]], True),
        ("float labels compare equal to integer labels", "expected_preserving_target_labels", [[0.0, 1.0]], True),
    ]
    for label, field, value, expected in semantic_mutations:
        variant = copy.deepcopy(original)
        variant[field] = value
        invoke(label, lambda variant=variant: author.verify(variant), expected, "documented_parser_boundary" if expected else "negative")

    # Independently exercise the actual CLI JSON parser. Duplicate JSON keys
    # are accepted by json.loads with the final value; nonfinite metadata is
    # not being used to evade any arithmetic guard in this probe.
    with tempfile.TemporaryDirectory(prefix="certificate_", dir=HERE / "private_replay") as temporary:
        path = Path(temporary) / "duplicate.json"
        raw = json.dumps(original)
        path.write_text('{"dimension":1,' + raw[1:])
        process = subprocess.run([sys.executable, "-B", "-I", "-S"] + (["-O"] if sys.flags.optimize else []) + [str(BASELINE / "author/verify.py"), "--certificate", str(path)], capture_output=True, timeout=30)
        need(process.returncode == 0 and not process.stderr, "duplicate-key CLI probe unexpected result")
        rows.append({"probe": "author CLI accepts duplicate dimension key with valid final value", "category": "documented_parser_boundary", "accepted": True, "returncode": process.returncode, "stdout_sha256": hashlib.sha256(process.stdout).hexdigest()})

    output = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "optimized": bool(sys.flags.optimize), "status": "pass", "probes": rows, "count": len(rows), "candidate_edited": False, "mathematical_refutation_claimed": False, "interpretation": "Observed wrapper/parser boundaries are distinct from the authenticated fixed baseline, external immutable pins, and universal analytic proof."}
    filename = "ADVERSARIAL_OPTIMIZED.json" if sys.flags.optimize else "ADVERSARIAL_NORMAL.json"
    (HERE / filename).write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "pass", "optimized": bool(sys.flags.optimize), "probes": len(rows)}))


if __name__ == "__main__":
    main()
