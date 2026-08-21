#!/usr/bin/env python3
"""Independent regression for prepared-stage/source binding.

This does not rebuild the mathematical payload.  It attacks the exact
byte/mode comparison used by the release builder and fails unless all four
relevant staging mutations are rejected.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "reproducibility/build_certificate_bundle.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("certificate_builder_under_test", BUILDER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_commitment(root: Path) -> str:
    records: list[tuple[str, int, int, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name in {"ACTIVE_MANIFEST.json", "SHA256SUMS"}:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        records.append((
            path.relative_to(root).as_posix(),
            path.stat().st_size,
            path.stat().st_mode & 0o111,
            digest,
        ))
    commitment = hashlib.sha256()
    for relative, size, executable_bits, digest in records:
        commitment.update(relative.encode("utf-8") + b"\0")
        commitment.update(str(size).encode("ascii") + b"\0")
        commitment.update(f"{executable_bits:o}".encode("ascii") + b"\0")
        commitment.update(digest.encode("ascii") + b"\n")
    return commitment.hexdigest()


def expect_rejection(builder, candidate: Path, fresh: Path, name: str) -> None:
    try:
        builder.require_identical_payload(candidate, fresh)
    except AssertionError:
        return
    raise AssertionError(f"stage mutation accepted: {name}")


def reset(candidate: Path, pristine: Path) -> None:
    shutil.rmtree(candidate)
    shutil.copytree(pristine, candidate, copy_function=shutil.copy2)


def main() -> None:
    builder = load_builder()
    with tempfile.TemporaryDirectory(prefix="stc-jc-stage-binding-") as raw:
        base = Path(raw)
        pristine = base / "pristine"
        fresh = base / "fresh"
        candidate = base / "candidate"
        for root in (pristine, fresh):
            (root / "nested").mkdir(parents=True)
            (root / "payload.txt").write_bytes(b"exact payload\n")
            script = root / "nested/verify.sh"
            script.write_bytes(b"#!/bin/sh\nexit 0\n")
            script.chmod(0o755)
        shutil.copytree(pristine, candidate, copy_function=shutil.copy2)

        observed = builder.require_identical_payload(candidate, fresh)
        assert observed == independent_commitment(fresh), "commitment formula mismatch"

        (candidate / "payload.txt").write_bytes(b"altered payload\n")
        expect_rejection(builder, candidate, fresh, "changed bytes")
        reset(candidate, pristine)

        (candidate / "payload.txt").unlink()
        expect_rejection(builder, candidate, fresh, "missing file")
        reset(candidate, pristine)

        (candidate / "extra.txt").write_bytes(b"extra\n")
        expect_rejection(builder, candidate, fresh, "extra file")
        reset(candidate, pristine)

        script = candidate / "nested/verify.sh"
        script.chmod(script.stat().st_mode & ~0o111)
        expect_rejection(builder, candidate, fresh, "executable-bit change")

        # The release builder must consume the recorded Git object, not ignored
        # or untracked bytes in the ambient working tree.
        repository = base / "git-fixture"
        project = repository / "fixture_project"
        project.mkdir(parents=True)
        (repository / ".gitignore").write_text(
            "fixture_project/ignored_injection.py\n", encoding="utf-8"
        )
        (project / "tracked.py").write_text("TRACKED = True\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
        subprocess.run(["git", "config", "user.name", "Stage Test"],
                       cwd=repository, check=True)
        subprocess.run(["git", "config", "user.email", "stage@test.invalid"],
                       cwd=repository, check=True)
        subprocess.run(["git", "add", "."], cwd=repository, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repository,
                       check=True)
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repository, text=True
        ).strip()
        (project / "ignored_injection.py").write_text(
            "INJECTED = True\n", encoding="utf-8"
        )
        original_project = builder.PROJECT
        try:
            builder.PROJECT = project
            exported = builder.export_project_commit(commit, base / "export")
        finally:
            builder.PROJECT = original_project
        assert (exported / "tracked.py").is_file(), "tracked source omitted"
        assert not (exported / "ignored_injection.py").exists(), (
            "ignored working-tree injection entered commit export"
        )

        committed_builder = project / "reproducibility/build_certificate_bundle.py"
        committed_builder.parent.mkdir()
        committed_builder.write_text(
            """#!/usr/bin/env python3
import argparse
from pathlib import Path
import shutil

p = argparse.ArgumentParser()
p.add_argument('command')
p.add_argument('--stage', type=Path, required=True)
a = p.parse_args()
if a.command != 'prepare':
    raise SystemExit(2)
if a.stage.exists():
    shutil.rmtree(a.stage)
a.stage.mkdir(parents=True)
shutil.copy2(Path(__file__).resolve().parents[1] / 'tracked.py',
             a.stage / 'tracked.py')
""",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "fixture_project/reproducibility"],
                       cwd=repository, check=True)
        subprocess.run(["git", "commit", "-qm", "add committed builder"],
                       cwd=repository, check=True)
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repository, text=True
        ).strip()
        hook = base / "startup-hook"
        hook.mkdir()
        (hook / "sitecustomize.py").write_text(
            """import atexit
from pathlib import Path
import sys

def inject():
    if '--stage' in sys.argv:
        stage = Path(sys.argv[sys.argv.index('--stage') + 1])
        stage.mkdir(parents=True, exist_ok=True)
        (stage / 'injected_from_pythonpath.py').write_text('INJECTED = True\\n')

atexit.register(inject)
""",
            encoding="utf-8",
        )
        old_pythonpath = os.environ.get("PYTHONPATH")
        original_project = builder.PROJECT
        try:
            os.environ["PYTHONPATH"] = str(hook)
            builder.PROJECT = project
            isolated_stage = base / "isolated-stage"
            builder.prepare_from_commit(commit, isolated_stage,
                                        base / "isolated-scratch")
        finally:
            builder.PROJECT = original_project
            if old_pythonpath is None:
                os.environ.pop("PYTHONPATH", None)
            else:
                os.environ["PYTHONPATH"] = old_pythonpath
        assert (isolated_stage / "tracked.py").is_file(), "committed builder failed"
        assert not (isolated_stage / "injected_from_pythonpath.py").exists(), (
            "PYTHONPATH/sitecustomize entered detached preparation"
        )

        nonisolated = subprocess.run(
            [sys.executable, str(BUILDER), "prepare", "--stage",
             str(base / "nonisolated-stage")],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert nonisolated.returncode != 0, "nonisolated outer builder was accepted"
        assert "require isolated Python" in nonisolated.stderr, (
            "nonisolated rejection did not state the release requirement"
        )

    print(json.dumps({
        "accepted_identical_stage": True,
        "mutations_rejected": 7,
        "ignored_source_injection_excluded": True,
        "python_startup_injection_excluded": True,
        "nonisolated_outer_invocation_rejected": True,
        "binding_fields": ["path", "bytes", "executable_bits", "sha256"],
        "status": "VERIFIED",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
