#!/usr/bin/env python3
"""Shared fail-closed primitives for the K3P release layer.

This module deliberately uses explicit checks rather than ``assert`` so no
certification decision changes under interpreter optimization.  Public
entrypoints nevertheless refuse optimized Python as an additional safeguard.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Iterable, Mapping


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ReleaseFailure(RuntimeError):
    """A release invariant failed."""


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ReleaseFailure(str(message))


def refuse_optimized_python() -> None:
    if not __debug__ or sys.flags.optimize:
        raise ReleaseFailure("OPTIMIZED_PYTHON_FORBIDDEN")


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def pretty_json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    require(path.is_file(), ("missing JSON artifact", str(path)))
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ReleaseFailure(("invalid JSON artifact", str(path), str(error))) from error
    require(isinstance(value, dict), ("JSON object required", str(path)))
    return value


def safe_relative_path(value: str) -> PurePosixPath:
    require(isinstance(value, str) and value != "", ("empty path", value))
    require("\\" not in value and "\x00" not in value, ("unsafe path spelling", value))
    require(not value.startswith("/"), ("absolute path forbidden", value))
    raw_parts = value.split("/")
    require(".." not in raw_parts, ("path traversal forbidden", value))
    require(all(part not in ("", ".") for part in raw_parts),
            ("noncanonical or traversing path", value))
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts,
            ("path traversal forbidden", value))
    return path


def resolve_inside(root: Path, relative: str) -> Path:
    safe_relative_path(relative)
    root = root.resolve()
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise ReleaseFailure(("path resolves outside project", relative)) from error
    return path


def verify_payload_sha256(value: Mapping[str, object], *, excluded: Iterable[str] = ()) -> str:
    claimed = value.get("payload_sha256")
    require(isinstance(claimed, str) and SHA256_RE.fullmatch(claimed) is not None,
            "missing or malformed payload_sha256")
    body = dict(value)
    body.pop("payload_sha256", None)
    for key in excluded:
        body.pop(key, None)
    observed = sha256_bytes(canonical_json_bytes(body))
    require(observed == claimed, ("stale payload SHA-256", claimed, observed))
    return observed


def parse_sha256sums(text: str, *, checksum_path: str | None = None) -> dict[str, str]:
    records: dict[str, str] = {}
    for line_number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        require(len(raw) >= 67 and raw[64:66] == "  ",
                ("malformed checksum line", line_number, raw))
        digest, relative = raw[:64], raw[66:]
        require(SHA256_RE.fullmatch(digest) is not None,
                ("malformed SHA-256", line_number, digest))
        safe_relative_path(relative)
        require(relative not in records, ("duplicate checksum path", relative))
        if checksum_path is not None:
            require(relative != checksum_path,
                    ("self-referential checksum list", checksum_path))
        records[relative] = digest
    require(bool(records), "empty checksum list")
    return records


def verify_sha256sums(project: Path, checksum_relative: str) -> dict[str, str]:
    checksum_path = resolve_inside(project, checksum_relative)
    require(checksum_path.is_file(), ("missing checksum file", checksum_relative))
    records = parse_sha256sums(
        checksum_path.read_text(encoding="utf-8"), checksum_path=checksum_relative
    )
    for relative, expected in records.items():
        path = resolve_inside(project, relative)
        require(path.is_file(), ("missing checksummed file", relative))
        observed = sha256_file(path)
        require(observed == expected, ("stale file SHA-256", relative, expected, observed))
    return records


def run_git(project: Path, arguments: list[str], *, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        ["git", *arguments], cwd=project, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    require(result.returncode == 0,
            ("git command failed", arguments, result.stderr.decode(errors="replace")[-2000:]))
    return result.stdout if binary else result.stdout.decode("utf-8", errors="strict")


def git_root(project: Path) -> Path:
    return Path(str(run_git(project, ["rev-parse", "--show-toplevel"])).strip()).resolve()


def git_project_prefix(project: Path) -> str:
    project = project.resolve()
    root = git_root(project)
    try:
        relative = project.relative_to(root)
    except ValueError as error:
        raise ReleaseFailure("project is outside its Git root") from error
    return relative.as_posix()


def head_commit(project: Path) -> str:
    value = str(run_git(project, ["rev-parse", "HEAD"])).strip()
    require(re.fullmatch(r"[0-9a-f]{40}", value) is not None, ("invalid HEAD", value))
    return value


def head_commit_epoch(project: Path) -> int:
    value = str(run_git(project, ["show", "-s", "--format=%ct", "HEAD"])).strip()
    require(value.isdigit() and int(value) >= 0, ("invalid commit epoch", value))
    return int(value)


def exact_head_tags(project: Path) -> list[str]:
    text = str(run_git(project, ["tag", "--points-at", "HEAD"]))
    return sorted(line for line in text.splitlines() if line)


def tracked_head_paths(project: Path) -> list[str]:
    prefix = git_project_prefix(project)
    root = git_root(project)
    raw = run_git(root, ["ls-tree", "-rz", "--name-only", "HEAD", "--", prefix], binary=True)
    require(isinstance(raw, bytes), "binary Git tree output required")
    result: list[str] = []
    marker = (prefix + "/").encode()
    for item in raw.split(b"\x00"):
        if not item:
            continue
        require(item.startswith(marker), ("Git tree path outside project", item))
        relative = item[len(marker):].decode("utf-8", errors="strict")
        safe_relative_path(relative)
        result.append(relative)
    require(result == sorted(result), "Git tree paths are not sorted")
    require(len(result) == len(set(result)), "duplicate Git tree path")
    return result


def tracked_head_entries(project: Path) -> dict[str, str]:
    """Return project-relative regular-blob paths mapped to Git file modes."""
    prefix = git_project_prefix(project)
    root = git_root(project)
    raw = run_git(root, ["ls-tree", "-rz", "HEAD", "--", prefix], binary=True)
    require(isinstance(raw, bytes), "binary Git tree output required")
    marker = (prefix + "/").encode()
    result: dict[str, str] = {}
    for item in raw.split(b"\x00"):
        if not item:
            continue
        metadata, full_path = item.split(b"\t", 1)
        mode, kind, object_id = metadata.decode("ascii").split(" ")
        require(kind == "blob" and mode in ("100644", "100755"),
                ("nonregular Git entry forbidden in release", mode, kind, full_path))
        require(re.fullmatch(r"[0-9a-f]{40,64}", object_id) is not None,
                ("invalid Git object id", object_id))
        require(full_path.startswith(marker), ("Git tree path outside project", full_path))
        relative = full_path[len(marker):].decode("utf-8", errors="strict")
        safe_relative_path(relative)
        require(relative not in result, ("duplicate Git tree entry", relative))
        result[relative] = mode
    require(list(result) == sorted(result), "Git tree entries are not sorted")
    return result


def read_head_blob(project: Path, relative: str) -> bytes:
    safe_relative_path(relative)
    prefix = git_project_prefix(project)
    value = run_git(git_root(project), ["show", f"HEAD:{prefix}/{relative}"], binary=True)
    require(isinstance(value, bytes), "binary Git blob output required")
    return value


def load_head_json(project: Path, relative: str) -> dict:
    try:
        value = json.loads(read_head_blob(project, relative).decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ReleaseFailure(("invalid JSON artifact at HEAD", relative, str(error))) from error
    require(isinstance(value, dict), ("JSON object required at HEAD", relative))
    return value


def tracked_worktree_fingerprint(project: Path) -> str:
    """Hash names, modes, symlink targets, and bytes of project-tracked files."""
    prefix = git_project_prefix(project)
    root = git_root(project)
    raw = run_git(root, ["ls-files", "-z", "--", prefix], binary=True)
    require(isinstance(raw, bytes), "binary Git index output required")
    digest = hashlib.sha256()
    for encoded in raw.split(b"\x00"):
        if not encoded:
            continue
        full_relative = encoded.decode("utf-8", errors="strict")
        path = root / full_relative
        digest.update(encoded)
        digest.update(b"\x00")
        require(path.exists() or path.is_symlink(), ("tracked file missing", full_relative))
        if path.is_symlink():
            digest.update(b"L")
            digest.update(os.readlink(path).encode())
        else:
            digest.update(b"F")
            digest.update(path.read_bytes())
        digest.update(b"\x00")
    return digest.hexdigest()


def scoped_status(project: Path) -> list[str]:
    prefix = git_project_prefix(project)
    root = git_root(project)
    text = str(run_git(
        root, ["status", "--porcelain=v1", "--untracked-files=all", "--", prefix]
    ))
    return [line for line in text.splitlines() if line]


FORBIDDEN_ACTIVE_PREFIXES = (
    "history/",
    "cut_recovery/pointwise_algebra/",
)

FORBIDDEN_ACTIVE_EXACT = {
    "cut_recovery/upstream_frozen/pointwise_cut_certificate.json",
    "cut_recovery/verify_cut_recovery.py",
    "cut_recovery/verification_report.json",
    "cut_recovery/primary_exact_evidence.json",
    "input_frozen/k3p_cloud_artifacts/k3p_pointwise_cut_transfer.json",
    "input_frozen/k3p_cloud_artifacts/verify_k3p_cut_transfer.py",
}


def forbidden_active_evidence(relative: str) -> bool:
    safe_relative_path(relative)
    return relative in FORBIDDEN_ACTIVE_EXACT or relative.startswith(FORBIDDEN_ACTIVE_PREFIXES)


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-release")
    temporary.write_bytes(data)
    os.replace(temporary, path)
