#!/usr/bin/env python3
"""Small mutation suite for the fail-closed readiness state machine."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location(
    "submission_validator", HERE / "validate_submission_packages.py"
)
if SPEC is None or SPEC.loader is None:
    raise SystemExit("could not load submission validator")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def main() -> int:
    cases = [
        ([], [], ("READY", 0)),
        ([], ["unresolved token"], ("NOT_READY", 2)),
        (["bad manifest"], [], ("INVALID", 1)),
        (["bad manifest"], ["unresolved token"], ("INVALID", 1)),
    ]
    for errors, blockers, expected in cases:
        actual = MODULE.package_status(errors, blockers)
        if actual != expected:
            raise SystemExit(f"state-machine mutation failed: {errors}, {blockers}: {actual}")

    text = "@@REAL_RELEASE_FIELD@@ @@TOKEN@@ @@UPPER_CASE_TOKEN@@"
    tokens = [
        token for token in MODULE.TOKEN_RE.findall(text)
        if token not in MODULE.DOCUMENTATION_TOKENS
    ]
    if tokens != ["REAL_RELEASE_FIELD"]:
        raise SystemExit(f"placeholder grammar mutation failed: {tokens}")

    if MODULE.latex_word_count(r"One two \(x\) three-four") != 4:
        raise SystemExit("LaTeX word-count mutation failed")

    errors: list[str] = []
    blockers: list[str] = []
    MODULE.validate_upload({
        "filename": "missing.pdf", "present": True,
        "path": "submission/does-not-exist.pdf", "sha256": "0" * 64, "bytes": 1,
    }, "fixture", errors, blockers)
    if not any("missing" in value for value in errors):
        raise SystemExit(f"present-but-missing upload mutation survived: {errors}")

    with tempfile.TemporaryDirectory(prefix="validator-fixture-", dir=HERE) as directory:
        root = Path(directory)
        artifact = root / "artifact.txt"
        artifact.write_text("actual\n")
        relative = artifact.relative_to(MODULE.PROJECT).as_posix()
        errors = []
        MODULE.validate_upload({
            "filename": "artifact.txt", "present": True, "path": relative,
            "sha256": "0" * 64, "bytes": artifact.stat().st_size,
        }, "fixture", errors, [])
        if not any("SHA-256 mismatch" in value for value in errors):
            raise SystemExit(f"wrong upload hash mutation survived: {errors}")

        manifest = root / "MANIFEST.json"
        manifest.write_text(json.dumps({
            "schema_version": 1,
            "package": "fixture",
            "status": "DRAFT_NOT_READY",
            "source_map": [{
                "source": relative, "destination": "artifact.txt", "mode": "copy_file",
            }],
            "initial_portal_uploads": [{"filename": "artifact.pdf", "present": False}],
            "release_blockers": ["fixture"],
        }))
        manifest_errors: list[str] = []
        manifest_blockers: list[str] = []
        MODULE.validate_manifest(manifest, manifest_errors, manifest_blockers)
        if manifest_errors or not any("manifest remains" in value for value in manifest_blockers):
            raise SystemExit(
                f"draft-manifest readiness mutation survived: {manifest_errors}, "
                f"{manifest_blockers}"
            )

        unsafe_manifest = root / "UNSAFE_MANIFEST.json"
        unsafe_manifest.write_text(json.dumps({
            "schema_version": 1,
            "package": "fixture",
            "status": "READY",
            "source_map": [{
                "source": "/etc/hosts", "destination": "hosts", "mode": "copy_file",
            }],
            "initial_portal_uploads": [{"filename": "artifact.pdf", "present": False}],
            "release_blockers": [],
        }))
        unsafe_errors: list[str] = []
        MODULE.validate_manifest(unsafe_manifest, unsafe_errors, [])
        if not any("unsafe manifest source" in value for value in unsafe_errors):
            raise SystemExit(f"absolute source-map mutation survived: {unsafe_errors}")

        wrong_mode_manifest = root / "WRONG_MODE_MANIFEST.json"
        wrong_mode_manifest.write_text(json.dumps({
            "schema_version": 1,
            "package": "fixture",
            "status": "READY",
            "source_map": [{
                "source": root.relative_to(MODULE.PROJECT).as_posix(),
                "destination": "not-a-file", "mode": "copy_file",
            }],
            "initial_portal_uploads": [{"filename": "artifact.pdf", "present": False}],
            "release_blockers": [],
        }))
        wrong_mode_errors: list[str] = []
        MODULE.validate_manifest(wrong_mode_manifest, wrong_mode_errors, [])
        if not any("copy_file source is not a regular file" in value
                   for value in wrong_mode_errors):
            raise SystemExit(f"source-map mode/type mutation survived: {wrong_mode_errors}")

        shared = root / "shared.tex"
        shared.write_text("@@TOKEN_IN_SHARED_SOURCE@@\n")
        locations = MODULE.collect_token_locations({shared})
        if "TOKEN_IN_SHARED_SOURCE" not in locations:
            raise SystemExit(f"shared-source token mutation survived: {locations}")

    print("PASS: 12 fail-closed validator mutations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
