#!/usr/bin/env python3
"""Independent byte/mode binding of the v2.0.2 source archive to Git."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile


PACKAGE = Path(sys.argv[1]).resolve()
REPO = Path(sys.argv[2]).resolve()
ARCHIVE = PACKAGE / (
    "simultaneous_amplifier_beyond_three_halves_"
    "source_and_certificates.tar.gz"
)
TAG = "simultaneous-amplification-beyond-three-halves-v2.0.2"
TAG_OBJECT = "be3946c051c7f7e2073d6adf81bca31ae750251a"
COMMIT = "03e94e877ce10d9d459fd284bd652934cde08bb3"
SYNTHETIC = {"BUNDLE_METADATA.txt", "MANIFEST.sha256"}


class Failure(RuntimeError):
    pass


def require(condition: object, message: str) -> None:
    if not bool(condition):
        raise Failure(message)


def git(*arguments: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(REPO), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(
        result.returncode == 0,
        f"git {' '.join(arguments)} failed: "
        f"{result.stderr.decode(errors='replace').strip()}",
    )
    return result.stdout


def main() -> None:
    require(sys.flags.optimize == 0, "independent Git audit refuses optimized Python")
    require(
        Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve() == REPO,
        "supplied repository path is not its root",
    )
    require(git("cat-file", "-t", TAG).decode().strip() == "tag", "tag is not annotated")
    require(git("rev-parse", TAG).decode().strip() == TAG_OBJECT, "tag object differs")
    require(git("rev-parse", f"{TAG}^{{commit}}").decode().strip() == COMMIT, "tag peel differs")
    tag_payload = git("cat-file", "-p", TAG_OBJECT).decode("utf-8")
    require(tag_payload.startswith(f"object {COMMIT}\ntype commit\n"), "tag payload differs")

    with tarfile.open(ARCHIVE, "r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        require(len(names) == len(set(names)), "archive names are not unique")
        checked = 0
        for member in members:
            if member.name in SYNTHETIC:
                continue
            name = PurePosixPath(member.name)
            require(
                not name.is_absolute() and ".." not in name.parts and name.as_posix() == member.name,
                f"unsafe name: {member.name}",
            )
            rows = git("ls-tree", COMMIT, "--", member.name).decode("utf-8").splitlines()
            require(len(rows) == 1, f"Git lacks unique tree row: {member.name}")
            metadata, returned_name = rows[0].split("\t", 1)
            mode, kind, object_id = metadata.split(" ", 2)
            require(returned_name == member.name, f"Git path differs: {member.name}")
            require(kind == "blob", f"Git object is not a blob: {member.name}")
            require(mode == ("100755" if member.mode == 0o755 else "100644"), f"mode differs: {member.name}")
            stream = archive.extractfile(member)
            require(stream is not None, f"archive member unreadable: {member.name}")
            archive_bytes = stream.read()
            git_bytes = git("cat-file", "blob", object_id)
            require(archive_bytes == git_bytes, f"blob bytes differ: {member.name}")
            checked += 1
    require(checked == 21, f"expected 21 repository-backed blobs; checked {checked}")
    print(
        "PASS independent Git binding: annotated tag object "
        f"{TAG_OBJECT}, commit {COMMIT}, {checked} exact blobs/modes"
    )
    print("LIMITATION unsigned tag/checkouts do not authenticate authorship")


if __name__ == "__main__":
    main()
