#!/usr/bin/env python3
"""Independent replay controls for the fixed EP-1133 audit bundle.

This checks identities and finite tests, never the analytic theorem.
Input source contents and input paths are not copied into the output.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

MANIFEST = "97185d9d301079510b35dcc78944f1f536c10e34f4de5222aadf474093b1b15d"
VERIFIER = "14733b9582625d2cdecc12312832a3af5b1f4737646088a54b7f4b9c8586af8d"
MODES = [("normal", []), ("-O", ["-O"]), ("-OO", ["-OO"])]
FLAGS = ["--problems", "--research", "--candidate-pdf", "--density-pdf", "--original-pdf"]


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    return {p.name: sha(p.read_bytes()) for p in root.iterdir() if p.is_file()}


def run(verifier, root, mode, sources=(), pin=MANIFEST):
    args = [sys.executable, "-B", *mode, str(verifier), "--root", str(root),
            "--manifest-sha256", pin]
    for flag, path in zip(FLAGS, sources):
        args.extend([flag, str(path)])
    return subprocess.run(args, capture_output=True, text=True, timeout=60,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


def reseal(root):
    p = root / "MANIFEST.json"
    obj = json.loads(p.read_bytes())
    for entry in obj["files"]:
        data = (root / entry["path"]).read_bytes()
        entry.update(bytes=len(data), sha256=sha(data))
    p.write_text(json.dumps(obj, indent=2) + "\n")
    return sha(p.read_bytes())


def json_change(root, filename, mutate):
    p = root / filename
    obj = json.loads(p.read_bytes())
    mutate(obj)
    p.write_text(json.dumps(obj, indent=2, allow_nan=True) + "\n")
    return reseal(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    for flag in FLAGS:
        parser.add_argument(flag, required=True, type=Path)
    args = parser.parse_args()
    root = args.bundle.absolute() / "public"
    verifier = root / "verify.py"
    sources = [getattr(args, flag[2:].replace("-", "_")).absolute() for flag in FLAGS]
    require(sha(verifier.read_bytes()) == VERIFIER, "external verifier pin mismatch")
    require(sha((root / "MANIFEST.json").read_bytes()) == MANIFEST, "external manifest pin mismatch")
    before = inventory(root)
    baseline = [run(verifier, root, mode, sources) for _, mode in MODES]
    require(all(x.returncode == 0 for x in baseline), "full-source baseline rejected")
    require(len({x.stdout for x in baseline}) == 1, "optimization mismatch")
    result = json.loads(baseline[0].stdout)
    require(result["source_replay"]["whole_file_pins_matched"] == 5, "source coverage")
    source_summary = [{"input": flag[2:], "bytes": p.stat().st_size,
                       "sha256": sha(p.read_bytes())} for flag, p in zip(FLAGS, sources)]
    tests = [
        ("boolean_claim_integer", "CLAIMS.json", lambda c: c.update(new_approaches=False)),
        ("integer_claim_boolean", "CLAIMS.json", lambda c: c.update(new_discovery_claimed=0)),
        ("float_claim_integer", "CLAIMS.json", lambda c: c.update(rank=1037.0)),
        ("extra_claim", "CLAIMS.json", lambda c: c.update(extra=True)),
        ("integer_fixture_boolean", "FIXTURES.json", lambda f: f.update(finite_evidence_only=1)),
        ("boolean_fraction_denominator", "FIXTURES.json", lambda f: f["parameters"][0].update(eta=[1, True])),
        ("negative_fraction_numerator", "FIXTURES.json", lambda f: f["parameters"][0].update(eta=[-1, 100])),
        ("float_fraction_numerator", "FIXTURES.json", lambda f: f["parameters"][0].update(eta=[1.0, 100])),
        ("boolean_threshold", "FIXTURES.json", lambda f: f["parameters"][0].update(n0=True)),
        ("negative_infinity_threshold", "FIXTURES.json", lambda f: f["parameters"][0].update(n0=float("-inf"))),
        ("boolean_dataset_bytes", "SOURCES.json", lambda s: s["dataset_pins"][0].update(bytes=True)),
        ("float_dataset_bytes", "SOURCES.json", lambda s: s["dataset_pins"][0].update(bytes=68931837.0)),
        ("nan_source_metadata", "SOURCES.json", lambda s: s.update(checked_utc=float("nan"))),
        ("uppercase_source_digest", "SOURCES.json", lambda s: s["scholarly_sources"][0].update(sha256="A" * 64)),
        ("integer_source_boolean", "SOURCES.json", lambda s: s.update(research_entry_present=0)),
        ("wrong_problem_record_digest", "SOURCES.json", lambda s: s.update(selected_record_sha256="0" * 64)),
        ("wrong_source_digest", "SOURCES.json", lambda s: s["scholarly_sources"][0].update(sha256="0" * 64)),
    ]
    rejection_rows = []
    readonly_modes = []
    with tempfile.TemporaryDirectory(prefix="ep1133-independent-") as temporary:
        tmp = Path(temporary)
        for index, (label, filename, mutate) in enumerate(tests):
            copy = tmp / str(index)
            shutil.copytree(root, copy)
            pin = json_change(copy, filename, mutate)
            for name, mode in MODES:
                replay = run(verifier, copy, mode, sources, pin)
                require(replay.returncode != 0 and replay.stderr.startswith("REJECT:"), label)
                rejection_rows.append({"label": label, "mode": name, "rejected": True})
        copy = tmp / "duplicate"
        shutil.copytree(root, copy)
        p = copy / "CLAIMS.json"
        p.write_bytes(p.read_bytes().replace(b'"new_approaches": 0', b'"new_approaches": 0, "new_approaches": 0'))
        pin = reseal(copy)
        for name, mode in MODES:
            replay = run(verifier, copy, mode, sources, pin)
            require(replay.returncode != 0 and replay.stderr.startswith("REJECT:"), "nested duplicate")
            rejection_rows.append({"label": "duplicate_claim_key", "mode": name, "rejected": True})
        badpdf = tmp / "modified.pdf"
        data = bytearray(sources[2].read_bytes())
        data[-1] ^= 1
        badpdf.write_bytes(data)
        linkedpdf = tmp / "linked.pdf"
        linkedpdf.symlink_to(sources[2])
        variants = [
            ("partial_source_group", sources[:1]),
            ("wrong_pdf_bytes_same_size", [*sources[:2], badpdf, *sources[3:]]),
            ("swapped_pdf_sources", [*sources[:2], sources[3], sources[2], sources[4]]),
            ("symlink_source", [*sources[:2], linkedpdf, *sources[3:]]),
            ("missing_source", [*sources[:2], tmp / "missing", *sources[3:]]),
            ("directory_source", [*sources[:2], tmp, *sources[3:]]),
        ]
        for label, paths in variants:
            for name, mode in MODES:
                replay = run(verifier, root, mode, paths)
                require(replay.returncode != 0 and replay.stderr.startswith("REJECT:"), label)
                rejection_rows.append({"label": label, "mode": name, "rejected": True})
        for name, mode in MODES:
            replay = run(verifier, root, mode, sources, "0" * 64)
            require(replay.returncode != 0 and replay.stderr.startswith("REJECT:"), "manifest pin")
            rejection_rows.append({"label": "wrong_external_manifest_pin", "mode": name, "rejected": True})

        # This reproduces the trust boundary without executing any mutated code.
        changed = tmp / "changed-code"
        shutil.copytree(root, changed)
        (changed / "verify.py").write_text("raise SystemExit(0)\n")
        require(sha((changed / "verify.py").read_bytes()) != VERIFIER, "verifier pin challenge")

        # Descriptive metadata is byte-authenticated by the frozen manifest;
        # it is not a complete generic schema validator after a caller repins.
        boundary = tmp / "trusted-repin-boundary"
        shutil.copytree(root, boundary)
        pin = json_change(boundary, "SOURCES.json", lambda s: s.update(checked_utc=True))
        boundary_result = run(verifier, boundary, [], (), pin)
        require(boundary_result.returncode == 0, "unexpected descriptive-schema behavior")
        fixed_boundary_result = run(verifier, boundary, [])
        require(fixed_boundary_result.returncode != 0 and fixed_boundary_result.stderr.startswith("REJECT:"),
                "descriptive mutation bypassed fixed pin")

        ro = tmp / "readonly"
        shutil.copytree(root, ro)
        inputs = tmp / "readonly-inputs"
        inputs.mkdir()
        copied_sources = []
        for index, path in enumerate(sources):
            dest = inputs / str(index)
            shutil.copyfile(path, dest)
            copied_sources.append(dest)
        before_ro = inventory(ro)
        before_inputs = inventory(inputs)
        for directory in (ro, inputs):
            for path in directory.iterdir():
                path.chmod(0o444)
            directory.chmod(0o555)
        require(os.geteuid() != 0, "readonly control requires actual nonroot")
        denied = 0
        try:
            for path in (ro / "NEW", ro / "REPORT.md", inputs / "NEW", copied_sources[0]):
                try:
                    with path.open("ab") as handle:
                        handle.write(b"x")
                except PermissionError:
                    denied += 1
                else:
                    raise RuntimeError("read-only write probe succeeded")
            for name, mode in MODES:
                replay = run(ro / "verify.py", ro, mode, copied_sources)
                require(replay.returncode == 0 and replay.stdout == baseline[0].stdout, "readonly replay")
                readonly_modes.append(name)
            require(inventory(ro) == before_ro and inventory(inputs) == before_inputs, "readonly bytes changed")
        finally:
            for directory in (ro, inputs):
                directory.chmod(0o755)
                for path in directory.iterdir():
                    path.chmod(0o644)
    require(inventory(root) == before, "frozen original changed")
    output = {
        "status": "PASS", "proof_assistant_verification": False,
        "manifest_sha256": MANIFEST, "verifier_sha256": VERIFIER,
        "baseline_modes": [name for name, _ in MODES], "optimization_outputs_identical": True,
        "finite_evidence": result["finite_evidence"], "sources": source_summary,
        "additional_hostile_cases": len(rejection_rows) // 3,
        "additional_hostile_rejections": len(rejection_rows), "rejections": rejection_rows,
        "replaced_code_detected_by_external_verifier_pin": True,
        "readonly_nonroot_euid": os.geteuid(), "readonly_write_probes_denied": denied,
        "readonly_full_source_modes": readonly_modes, "readonly_bytes_unchanged": True,
        "frozen_original_unchanged": True,
        "descriptive_mutation_rejected_under_fixed_pin": True,
        "schema_boundary": "After explicitly supplying a new trusted manifest digest, an altered descriptive checked_utc field is not semantically rejected. Under the fixed original digest, that same altered bundle is rejected by integrity verification. This is an identity verifier with selected semantic checks, not a generic full-metadata schema validator."
    }
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "rejections"}, sort_keys=True))


if __name__ == "__main__":
    main()
