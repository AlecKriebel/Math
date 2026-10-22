#!/usr/bin/env python3
"""Verify this review in its workspace or a standalone distribution package.

Validation uses explicit exceptions and remains active under -O and -OO.
Directory entries are inspected without following symlinks. Known FIFOs and
other special entries are rejected before any attempt to open their content.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import re
import stat

EXPECTED_HEAD = "32eaecaa8907dbf674e65b138b000cdcc49004ae"
EXPECTED_PROOF_SHA256 = "2634e714b9a06a1770ae39b0201031c7d2a7ce6e97f3330f8745d0e2453d4fef"
EXPECTED_SNAPSHOT_SHA256 = "ce16b1c496f0c69d7a8582f658dddbb1049c3125733bddcadcd394a875922661"
EXPECTED_PACKET_HASH_MAP_SHA256 = "c1eebcc56d07f9143947f0a51f3e7e3b5a1165296e8f93d924c2f3c2056967c6"
EXPECTED_CONTROL_RESULTS_SHA256 = "e022ef5834ae41f135a308818af975d612c59af0fc4e836ee397a4e451b02783"
EXPECTED_INITIAL_MANIFEST_SHA256 = "85a206b16b8eb007ec225b0f033da8fba53713c240720ad7c4da6c1fd3b27ad8"
SNAPSHOT_PREFIX = "unsolved_math_prioritization/attempts/30006419/"
INITIAL_FILES = {
    ".gitignore", "AUDIT.md", "RESULT.json", "INDEPENDENT_DERIVATIONS.md",
    "RESEARCH_LOG.md", "independent_controls.py", "CONTROL_RESULTS.json",
    "SOURCE_INSPECTION.json", "verify_manifest.py",
}
ACTIVE_FILES = INITIAL_FILES | {
    "UTILITY_REPAIR.md", "UTILITY_REPAIR_RESULTS.json", "utility_repair_checks.py",
}
EXPECTED_PUBLIC_FILES = ACTIVE_FILES | {
    f"history/initial_revision/{name}" for name in INITIAL_FILES | {"MANIFEST.json"}
}
IGNORED_TOP_LEVEL_DIRS = {"private_sources", "private_tmp", "__pycache__"}
EXPECTED_EXCLUDED_GLOBS = [
    "private_sources/*", "private_sources/**", "private_tmp/*", "private_tmp/**",
    "__pycache__/*", "__pycache__/**",
]


class VerificationFailure(ValueError):
    """A validation failure whose execution is independent of optimization."""


def require(condition, message):
    if not condition:
        raise VerificationFailure(message)


def valid_relative_name(name):
    require(isinstance(name, str) and name != "", "Invalid empty/non-string file name")
    path = PurePosixPath(name)
    require(not path.is_absolute() and ".." not in path.parts and "." not in path.parts,
            f"Unsafe relative name: {name}")
    require(path.as_posix() == name and "\\" not in name, f"Noncanonical relative name: {name}")


def read_regular(path):
    """Read a regular file only, rejecting known special entries before open."""
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode), f"Non-regular file rejected before open: {path.name}")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        require(stat.S_ISREG(opened.st_mode), f"Non-regular opened descriptor rejected: {path.name}")
        require((opened.st_dev, opened.st_ino) == (info.st_dev, info.st_ino),
                f"File changed between inspection and open: {path.name}")
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            return stream.read()
    finally:
        os.close(descriptor)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def scan_closed_tree(root, allowed_files, ignored_top_level=()):
    """Reject unlisted files/directories, symlinks and specials without reads."""
    require(stat.S_ISDIR(root.lstat().st_mode), f"Tree root is not a regular directory: {root.name}")
    allowed_dirs = set()
    for name in allowed_files:
        valid_relative_name(name)
        allowed_dirs.update(p.as_posix() for p in PurePosixPath(name).parents
                            if p.as_posix() != ".")
    observed = set()

    def walk(directory, prefix=""):
        with os.scandir(directory) as entries:
            for entry in entries:
                name = f"{prefix}/{entry.name}" if prefix else entry.name
                info = entry.stat(follow_symlinks=False)
                if stat.S_ISLNK(info.st_mode):
                    raise VerificationFailure(f"Symlink rejected: {name}")
                if stat.S_ISDIR(info.st_mode):
                    if not prefix and entry.name in ignored_top_level:
                        continue
                    require(name in allowed_dirs, f"Unlisted directory rejected: {name}")
                    walk(Path(entry.path), name)
                elif stat.S_ISREG(info.st_mode):
                    require(name in allowed_files, f"Unlisted file rejected: {name}")
                    observed.add(name)
                else:
                    raise VerificationFailure(f"Special entry rejected before open: {name}")

    walk(root)
    require(observed == set(allowed_files),
            f"Missing public files: {sorted(set(allowed_files) - observed)}")


def check_metadata_file(root, name, expected):
    valid_relative_name(name)
    require(isinstance(expected, dict) and set(expected) == {"bytes", "sha256"},
            f"Invalid metadata keys for {name}")
    require(type(expected["bytes"]) is int and expected["bytes"] >= 0,
            f"Invalid byte count for {name}")
    require(isinstance(expected["sha256"], str) and
            re.fullmatch(r"[0-9a-f]{64}", expected["sha256"]) is not None,
            f"Invalid digest for {name}")
    data = read_regular(root / name)
    require(len(data) == expected["bytes"], f"Size mismatch: {name}")
    require(digest(data) == expected["sha256"], f"Hash mismatch: {name}")


def locate_audit_root(root, explicit=None):
    if explicit is not None:
        candidate = explicit.absolute()
        require(os.path.lexists(candidate / "ORIGINAL_SNAPSHOT.json"),
                "Explicit audit root lacks ORIGINAL_SNAPSHOT.json")
        return candidate
    for candidate in (root, *root.parents):
        if os.path.lexists(candidate / "ORIGINAL_SNAPSHOT.json"):
            return candidate
    raise VerificationFailure("No ancestor package root contains ORIGINAL_SNAPSHOT.json")


def verify(audit_root=None):
    root = Path(__file__).absolute().parent
    manifest = json.loads(read_regular(root / "MANIFEST.json"))
    require(isinstance(manifest, dict), "Manifest must be a JSON object")
    require(manifest.get("schema") == "intentional-public-files-sha256-allowlist-v2",
            "Unexpected active manifest schema")
    require(manifest.get("audit_id") == "pr906_30006419_reshetnyak_proof_family",
            "Wrong review identity")
    require(manifest.get("original_head") == EXPECTED_HEAD, "Wrong manifest original head")
    require(manifest.get("manifest_self_path") == "MANIFEST.json", "Wrong manifest self path")
    require(manifest.get("excluded_globs") == EXPECTED_EXCLUDED_GLOBS,
            "Manifest exclusions differ from the fixed private-only list")
    intentional = manifest.get("intentional_public_files")
    require(isinstance(intentional, dict) and set(intentional) == EXPECTED_PUBLIC_FILES,
            "Manifest public list differs from the fixed closed review list")
    scan_closed_tree(root, EXPECTED_PUBLIC_FILES | {"MANIFEST.json"}, IGNORED_TOP_LEVEL_DIRS)
    for name, expected in intentional.items():
        check_metadata_file(root, name, expected)
    require(digest(read_regular(root / "CONTROL_RESULTS.json")) == EXPECTED_CONTROL_RESULTS_SHA256,
            "Active analytic control result differs from fixed initial result")

    history = root / "history" / "initial_revision"
    history_raw = read_regular(history / "MANIFEST.json")
    require(digest(history_raw) == EXPECTED_INITIAL_MANIFEST_SHA256,
            "Initial revision manifest differs from fixed history pin")
    historical = json.loads(history_raw)
    require(set(historical["intentional_public_files"]) == INITIAL_FILES,
            "Initial history allowlist has changed")
    for name, expected in historical["intentional_public_files"].items():
        check_metadata_file(history, name, expected)

    package_root = locate_audit_root(root, audit_root)
    snapshot_raw = read_regular(package_root / "ORIGINAL_SNAPSHOT.json")
    require(digest(snapshot_raw) == EXPECTED_SNAPSHOT_SHA256,
            "Original snapshot differs from fixed packet snapshot pin")
    snapshot = json.loads(snapshot_raw)
    require(snapshot["head"] == EXPECTED_HEAD, "Wrong original snapshot head")
    files = snapshot["files"]
    require(isinstance(files, dict) and len(files) == 30, "Wrong original packet file count")
    canonical_map = json.dumps(files, sort_keys=True, separators=(",", ":")).encode()
    require(digest(canonical_map) == EXPECTED_PACKET_HASH_MAP_SHA256,
            "Original packet hash map differs from fixed pin")
    require(files[SNAPSHOT_PREFIX + "author/PROOF.md"] == EXPECTED_PROOF_SHA256,
            "Original proof hash differs from fixed proof pin")
    for name in files:
        valid_relative_name(name)
        require(name.startswith(SNAPSHOT_PREFIX), "Unexpected original packet prefix")
    layouts = [name for name in ("original", "original_packet")
               if os.path.lexists(package_root / name)]
    require(len(layouts) == 1, "Exactly one supported original-packet layout is required")
    layout = layouts[0]
    packet_root = package_root / layout
    packet_files = ({name: value for name, value in files.items()} if layout == "original"
                    else {name.removeprefix(SNAPSHOT_PREFIX): value for name, value in files.items()})
    scan_closed_tree(packet_root, set(packet_files))
    for name, expected_hash in packet_files.items():
        require(digest(read_regular(packet_root / name)) == expected_hash,
                f"Original packet changed: {name}")
    return {
        "public_allowlist_passed": True,
        "public_hashed_file_count": len(intentional),
        "initial_revision_unchanged": True,
        "original_snapshot_unchanged": True,
        "original_file_count": len(files),
        "raw_sources_excluded": True,
        "layout": "workspace" if layout == "original" else "standalone",
        "verification_guards_active_without_assert": True,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-root", type=Path, help="Optional package/audit root override")
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.audit_root), indent=2))
    except (VerificationFailure, OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"Verification failure: {exc}\n")
