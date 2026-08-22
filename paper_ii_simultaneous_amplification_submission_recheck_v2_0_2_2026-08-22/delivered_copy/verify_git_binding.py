#!/usr/bin/env python3
"""Optionally compare every archived source blob and mode with a Git checkout."""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile


PACKAGE = Path(__file__).resolve().parent
ARCHIVE = PACKAGE / (
    "simultaneous_amplifier_beyond_three_halves_"
    "source_and_certificates.tar.gz"
)
COMMIT = "03e94e877ce10d9d459fd284bd652934cde08bb3"
TAG_OBJECT = "be3946c051c7f7e2073d6adf81bca31ae750251a"
TAG = "simultaneous-amplification-beyond-three-halves-v2.0.2"
SYNTHETIC = frozenset(
    {PurePosixPath("BUNDLE_METADATA.txt"), PurePosixPath("MANIFEST.sha256")}
)
SOURCE_EXECUTABLES = frozenset(
    {
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/all.sh"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/bootstrap_replay.sh"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/build.sh"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/bundle_manifest.py"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/release_bundle.sh"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/replay.sh"
        ),
        PurePosixPath(
            "universal_simultaneous_amplification/phase4_landmark_closure/"
            "paper_hybrid_threshold/verify_paper_claims.py"
        ),
    }
)


class VerificationError(RuntimeError):
    """Raised when the supplied Git checkout does not match the handoff."""


def require(condition: object, message: str) -> None:
    if not bool(condition):
        raise VerificationError(message)


def reject_optimized_python() -> None:
    if sys.flags.optimize != 0:
        raise SystemExit(
            "ERROR: optimized Python is unsupported for Git-binding verification"
        )


def expected_source_mode(name: PurePosixPath) -> int:
    return 0o755 if name in SOURCE_EXECUTABLES else 0o644


def git(repo: Path, *arguments: str) -> bytes:
    process = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        detail = process.stderr.decode("utf-8", errors="replace").strip()
        raise VerificationError(
            f"git {' '.join(arguments)} failed with status "
            f"{process.returncode}: {detail}"
        )
    return process.stdout


def archive_payloads() -> tuple[dict[PurePosixPath, bytes], dict[PurePosixPath, int]]:
    payloads: dict[PurePosixPath, bytes] = {}
    modes: dict[PurePosixPath, int] = {}
    with tarfile.open(ARCHIVE, mode="r:gz") as archive:
        members = archive.getmembers()
        member_names = [member.name for member in members]
        require(
            member_names == sorted(member_names),
            "source archive members are not sorted",
        )
        require(
            len(member_names) == len(set(member_names)),
            "source archive contains duplicate member names",
        )
        for member in members:
            require(member.isfile(), f"non-regular source member: {member.name}")
            name = PurePosixPath(member.name)
            require(
                not name.is_absolute()
                and ".." not in name.parts
                and name.as_posix() == member.name,
                f"unsafe or noncanonical source member: {member.name}",
            )
            require(name not in payloads, f"duplicate source member: {member.name}")
            require(
                member.mode == expected_source_mode(name),
                f"unexpected source mode {member.mode:#06o}: {member.name}",
            )
            stream = archive.extractfile(member)
            require(stream is not None, f"unreadable source member: {member.name}")
            payloads[name] = stream.read()
            modes[name] = member.mode
    return payloads, modes


def verify(repo: Path) -> int:
    root = Path(git(repo, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    require(root == repo.resolve(), f"not a repository root: {repo}")
    require(
        git(repo, "cat-file", "-t", TAG).decode().strip() == "tag",
        f"{TAG} is not an annotated tag object",
    )
    require(
        git(repo, "rev-parse", TAG).decode().strip() == TAG_OBJECT,
        "annotated tag object does not match the frozen record",
    )
    require(
        git(repo, "rev-parse", f"{TAG}^{{commit}}").decode().strip() == COMMIT,
        "annotated tag does not peel to the frozen scientific commit",
    )
    tag_text = git(repo, "cat-file", "-p", TAG_OBJECT).decode(
        "utf-8", errors="strict"
    )
    require(
        tag_text.startswith(f"object {COMMIT}\ntype commit\n"),
        "annotated tag payload names a different object",
    )

    payloads, archive_modes = archive_payloads()
    repository_payloads = sorted(set(payloads) - SYNTHETIC, key=lambda p: p.as_posix())
    require(repository_payloads, "source archive has no repository-backed payloads")
    for name in repository_payloads:
        raw_tree = git(repo, "ls-tree", COMMIT, "--", name.as_posix()).decode(
            "utf-8", errors="strict"
        )
        rows = raw_tree.splitlines()
        require(len(rows) == 1, f"Git tree lacks a unique entry for {name}")
        metadata, tree_name = rows[0].split("\t", 1)
        mode, object_type, _object_id = metadata.split(" ", 2)
        require(tree_name == name.as_posix(), f"Git returned a different path for {name}")
        require(object_type == "blob", f"Git entry is not a blob: {name}")
        expected_mode = "100755" if archive_modes[name] == 0o755 else "100644"
        require(mode == expected_mode, f"Git/archive mode mismatch for {name}")
        repository_bytes = git(repo, "show", f"{COMMIT}:{name.as_posix()}")
        require(
            repository_bytes == payloads[name],
            f"Git/archive byte mismatch for {name}",
        )
    return len(repository_payloads)


def main() -> None:
    reject_optimized_python()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        required=True,
        type=Path,
        help="independently obtained repository root containing the frozen tag",
    )
    arguments = parser.parse_args()
    count = verify(arguments.repo.resolve())
    print(
        f"PASS: annotated unsigned tag and {count} archived source blobs/modes "
        "match the supplied Git checkout"
    )
    print(
        "LIMITATION: this comparison does not authenticate the unsigned tag, "
        "the checkout, or repository authorship"
    )


if __name__ == "__main__":
    main()
