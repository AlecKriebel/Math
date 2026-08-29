#!/usr/bin/env python3
"""Build a self-contained exact partial Git checkout for one project subtree."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile


SOURCE = Path("/Users/alec/Documents/Math")
DESTINATION = Path(
    "/Users/alec/Documents/Math/"
    "k3p_level2_second_revision_referee_2026-08-28/"
    "execution/release_engineering_5a6d/repo_exact"
)
RUNTIME = DESTINATION.parent
GIT = "/opt/homebrew/bin/git"
COMMIT = "5a6d64cb2a76e890d7baaef3ba5ac9861c1d029f"
PREFIX = "k3p_level2_identifiability_final"


class BuildFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise BuildFailure(message)


def environment() -> dict[str, str]:
    return {
        "PATH": "/opt/homebrew/bin:/usr/bin:/bin",
        "HOME": "/var/empty",
        "LC_ALL": "C",
        "LANG": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_TERMINAL_PROMPT": "0",
    }


def git(repository: Path, arguments: list[str], *, input_bytes: bytes | None = None,
        check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [GIT, "-C", str(repository), *arguments],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=environment(),
        check=check,
        timeout=300,
    )


def text(repository: Path, arguments: list[str]) -> str:
    return git(repository, arguments).stdout.decode("utf-8", errors="strict")


def selected_object_ids() -> set[str]:
    commit_id = text(SOURCE, ["rev-parse", f"{COMMIT}^{{commit}}"]).strip()
    root_tree = text(SOURCE, ["show", "-s", "--format=%T", COMMIT]).strip()
    listing = git(SOURCE, ["ls-tree", "-r", "-t", "-z", COMMIT, "--", PREFIX]).stdout
    objects = {COMMIT, commit_id, root_tree}
    for record in listing.split(b"\x00"):
        if not record:
            continue
        metadata, _path = record.split(b"\t", 1)
        _mode, _kind, object_id = metadata.decode("ascii").split(" ")
        objects.add(object_id)
    require(len(objects) == 679, ("unexpected selected object census", len(objects)))
    return objects


def main() -> int:
    require(not DESTINATION.exists(), ("destination already exists", DESTINATION))
    require(text(SOURCE, ["cat-file", "-t", COMMIT]).strip() == "commit", "source commit")
    objects = selected_object_ids()
    DESTINATION.mkdir(parents=True, exist_ok=False)
    git(DESTINATION, ["init", "-q"])

    descriptor, raw_pack = tempfile.mkstemp(prefix="selected-objects-", suffix=".pack", dir=RUNTIME)
    os.close(descriptor)
    raw_pack_path = Path(raw_pack)
    try:
        with raw_pack_path.open("wb") as output:
            packed = subprocess.run(
                [
                    GIT, "-C", str(SOURCE), "pack-objects", "--stdout",
                    "--no-reuse-delta", "--no-reuse-object", "--window=0",
                ],
                input=("\n".join(sorted(objects)) + "\n").encode("ascii"),
                stdout=output,
                stderr=subprocess.PIPE,
                env=environment(),
                check=False,
                timeout=600,
            )
        require(packed.returncode == 0, ("pack-objects", packed.stderr[-2000:]))
        with raw_pack_path.open("rb") as source:
            indexed = subprocess.run(
                [GIT, "-C", str(DESTINATION), "index-pack", "--stdin"],
                stdin=source,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=environment(),
                check=False,
                timeout=600,
            )
        require(indexed.returncode == 0, ("index-pack", indexed.stderr[-2000:]))
        pack_hash = indexed.stdout.decode("ascii").strip()
        require(len(pack_hash) == 40, ("pack hash", pack_hash))
        promisor = DESTINATION / f".git/objects/pack/pack-{pack_hash}.promisor"
        promisor.write_bytes(b"")
    finally:
        raw_pack_path.unlink(missing_ok=True)

    git(DESTINATION, ["config", "core.repositoryFormatVersion", "1"])
    git(DESTINATION, ["config", "extensions.partialClone", "origin"])
    git(DESTINATION, ["config", "remote.origin.url", "file:///nonexistent"])
    git(DESTINATION, ["config", "remote.origin.promisor", "true"])
    git(DESTINATION, ["config", "remote.origin.partialCloneFilter", "blob:none"])
    git(DESTINATION, ["config", "core.sparseCheckout", "true"])
    git(DESTINATION, ["config", "core.sparseCheckoutCone", "false"])
    (DESTINATION / ".git/shallow").write_text(COMMIT + "\n", encoding="ascii")
    sparse = DESTINATION / ".git/info/sparse-checkout"
    sparse.parent.mkdir(parents=True, exist_ok=True)
    sparse.write_text(f"/{PREFIX}/\n", encoding="utf-8")
    git(DESTINATION, ["update-ref", "--no-deref", "HEAD", COMMIT])
    git(DESTINATION, ["read-tree", "-mu", "HEAD"])

    require(text(DESTINATION, ["rev-parse", "HEAD"]).strip() == COMMIT, "checkout HEAD")
    require(text(DESTINATION, ["status", "--porcelain=v1", "--untracked-files=all"]) == "",
            "checkout status")
    symbolic = git(DESTINATION, ["symbolic-ref", "-q", "HEAD"], check=False)
    require(symbolic.returncode == 1, "checkout is not detached")
    paths = [path for path in DESTINATION.iterdir() if path.name != ".git"]
    require(paths == [DESTINATION / PREFIX], ("unexpected checked-out roots", paths))
    tracked = text(DESTINATION, ["ls-tree", "-r", "--name-only", "HEAD", "--", PREFIX])
    require(len(tracked.splitlines()) == 621, "tracked project census")
    local_objects = set(text(DESTINATION, [
        "cat-file", "--batch-all-objects", "--batch-check=%(objectname)"
    ]).splitlines())
    require(local_objects == objects,
            ("partial object set mismatch", len(objects), len(local_objects)))
    require(not (DESTINATION / ".git/objects/info/alternates").exists(), "unexpected alternate")
    require(not any(
        path.resolve() == (SOURCE / ".git/objects").resolve()
        for path in (DESTINATION / ".git/objects").rglob("alternates")
    ), "source object exposure")
    print(f"EXACT_PARTIAL_CHECKOUT_PASS objects={len(objects)} pack={pack_hash} files=621")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
