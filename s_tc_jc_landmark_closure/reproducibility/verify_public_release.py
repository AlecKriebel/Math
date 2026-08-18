#!/usr/bin/env python3
"""Download and verify the published v1.1.4 GitHub Release fail-closed."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile


REPO_SLUG = "AlecKriebel/Math"
TAG = "stc-jc-sharp-boundary-v1.1.4"
ARCHIVE = "stc_jc_sharp_boundary_reproducibility.tar.gz"
PREFIX = "stc_jc_sharp_boundary_reproducibility"
MANIFEST = "RELEASE_ASSET_SHA256SUMS"
EXPECTED_ASSETS = frozenset({
    ARCHIVE,
    f"{ARCHIVE}.sha256",
    "RELEASE_ENVELOPE.json",
    MANIFEST,
    "FINAL_RELEASE_ENGINEERING_REPORT.md",
    "verify_quick.log",
    "verify_full.log",
    "verify_regenerate_all.log",
})
PROJECT_PREFIX = "s_tc_jc_landmark_closure/"
TRANSCRIPTS = (
    "verify_quick.log", "verify_full.log", "verify_regenerate_all.log"
)
ADDED_ARCHIVE_MEMBERS = frozenset({
    "ARCHIVE_SOURCE_COMMIT.txt",
    *(f"{PROJECT_PREFIX}release/final_biorxiv/transcripts/{name}"
      for name in TRANSCRIPTS),
})


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def gh_json(*args: str):
    output = subprocess.check_output(["gh", *args], text=True)
    return json.loads(output)


def peel_annotated_tag(ref: dict, tag: dict) -> str:
    """Return the commit only for a genuine annotated tag object."""
    obj = ref["object"]
    require(obj["type"] == "tag", "public release tag is not annotated")
    require(tag["object"]["type"] == "commit",
            "annotated tag does not peel directly to a commit")
    return tag["object"]["sha"]


def resolve_public_tag() -> str:
    ref = gh_json("api", f"repos/{REPO_SLUG}/git/ref/tags/{TAG}")
    obj = ref["object"]
    require(obj["type"] == "tag", "public release tag is not annotated")
    tag = gh_json("api", f"repos/{REPO_SLUG}/git/tags/{obj['sha']}")
    return peel_annotated_tag(ref, tag)


def public_result(release_url: str, source_commit: str, manifest_path: Path) -> dict:
    return {
        "status": "PUBLIC_RELEASE_VERIFIED",
        "release_url": release_url,
        "tag": TAG,
        "source_commit": source_commit,
        "assets": len(EXPECTED_ASSETS),
        "release_asset_manifest_sha256": digest(manifest_path),
    }


def validate_result_manifest(result: dict, manifest_path: Path) -> None:
    require(result.get("release_asset_manifest_sha256") == digest(manifest_path),
            "public verdict does not record the downloaded manifest digest")


def parse_manifest(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", line)
        require(match is not None, f"malformed/non-flat public manifest row: {line}")
        value, name = match.groups()
        require(name not in rows, f"duplicate public manifest row: {name}")
        rows[name] = value
    require(set(rows) == EXPECTED_ASSETS - {MANIFEST},
            "public manifest must cover exactly the other seven assets")
    return rows


def archive_bytes(archive: Path, member: str) -> bytes:
    with tarfile.open(archive, "r:gz") as bundle:
        stream = bundle.extractfile(f"{PREFIX}/{member}")
        require(stream is not None, f"archive member missing: {member}")
        return stream.read()


def git_blob_sha(data: bytes) -> str:
    """Return the SHA-1 object id used by the public Git repository."""
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def public_project_blobs(commit: str) -> dict[str, tuple[str, str]]:
    """Read every tracked project blob and mode from the tagged Git tree."""
    tree = gh_json(
        "api", f"repos/{REPO_SLUG}/git/trees/{commit}?recursive=1"
    )
    require(not tree.get("truncated"), "public recursive Git tree was truncated")
    records: dict[str, tuple[str, str]] = {}
    for item in tree["tree"]:
        path = item["path"]
        if not path.startswith(PROJECT_PREFIX) or item["type"] == "tree":
            continue
        require(item["type"] == "blob",
                f"unsupported tracked object in project tree: {path}")
        require(path not in records, f"duplicate public Git-tree path: {path}")
        records[path] = (item["sha"], item["mode"])
    require(records, "public tagged project tree is empty")
    return records


def archive_project_blobs(archive_path: Path) -> dict[str, tuple[bytes, str]]:
    """Read tracked-looking files and reject every unapproved archive extra."""
    records: dict[str, tuple[bytes, str]] = {}
    prefix = f"{PREFIX}/"
    with tarfile.open(archive_path, "r:gz") as bundle:
        for member in bundle.getmembers():
            if member.isdir():
                continue
            require(member.name.startswith(prefix),
                    f"archive member outside release prefix: {member.name}")
            relative = member.name[len(prefix):]
            if relative in ADDED_ARCHIVE_MEMBERS:
                continue
            require(relative.startswith(PROJECT_PREFIX),
                    f"unapproved nonproject archive member: {relative}")
            require(relative not in records,
                    f"duplicate archive project member: {relative}")
            if member.issym():
                data = member.linkname.encode("utf-8")
                mode = "120000"
            else:
                require(member.isfile(),
                        f"unsupported archive member type: {relative}")
                stream = bundle.extractfile(member)
                require(stream is not None, f"archive member unreadable: {relative}")
                data = stream.read()
                mode = "100755" if member.mode & 0o111 else "100644"
            records[relative] = (data, mode)
    return records


def verify_tracked_blob_records(
    expected: dict[str, tuple[str, str]],
    observed: dict[str, tuple[bytes, str]],
) -> None:
    require(set(observed) == set(expected),
            "release archive tracked-file set differs from annotated tag")
    for path, (expected_sha, expected_mode) in expected.items():
        data, observed_mode = observed[path]
        require(git_blob_sha(data) == expected_sha,
                f"release archive byte differs from annotated tag: {path}")
        require(observed_mode == expected_mode,
                f"release archive mode differs from annotated tag: {path}")


def mutation_test_tag_binding() -> None:
    """A correct marker must not hide one altered tagged source file."""
    path = f"{PROJECT_PREFIX}STATUS.md"
    good = b"tagged bytes\n"
    expected = {path: (git_blob_sha(good), "100644")}
    verify_tracked_blob_records(expected, {path: (good, "100644")})
    try:
        verify_tracked_blob_records(
            expected, {path: (b"altered archive bytes\n", "100644")}
        )
    except AssertionError:
        return
    raise AssertionError("tag-binding source-byte mutation escaped")


def main() -> None:
    release = gh_json(
        "release", "view", TAG, "--repo", REPO_SLUG,
        "--json", "tagName,isDraft,isPrerelease,url,assets",
    )
    require(release["tagName"] == TAG, "public release tag name changed")
    require(not release["isDraft"] and not release["isPrerelease"],
            "public release is draft or prerelease")
    public_names = {asset["name"] for asset in release["assets"]}
    require(public_names == EXPECTED_ASSETS,
            f"public release asset set differs: {sorted(public_names ^ EXPECTED_ASSETS)}")
    tag_commit = resolve_public_tag()

    with tempfile.TemporaryDirectory(prefix="stc-jc-public-release-") as name:
        root = Path(name)
        subprocess.run(
            ["gh", "release", "download", TAG, "--repo", REPO_SLUG,
             "--dir", str(root)],
            check=True,
        )
        require({path.name for path in root.iterdir()} == EXPECTED_ASSETS,
                "downloaded public release is incomplete")
        manifest_path = root / MANIFEST
        manifest = parse_manifest(manifest_path)
        for asset_name, expected in manifest.items():
            require(digest(root / asset_name) == expected,
                    f"public asset hash mismatch: {asset_name}")

        envelope = json.loads((root / "RELEASE_ENVELOPE.json").read_text(encoding="utf-8"))
        require(envelope["schema"] == "stc-jc-external-release-envelope-v1",
                "public envelope schema changed")
        require(envelope["status"] == "SEALED" and envelope["outcome"] == "A",
                "public envelope is not sealed Outcome A")
        require(envelope["source_commit"] == tag_commit,
                "public tag and envelope source commit differ")
        expected_external = {
            Path(record["path"]).name: record["sha256"]
            for record in envelope["external_artifacts"].values()
        }
        require(len(expected_external) == len(envelope["external_artifacts"]),
                "public envelope has colliding asset basenames")
        require(expected_external == {
            key: value for key, value in manifest.items()
            if key != "RELEASE_ENVELOPE.json"
        }, "public envelope and flat manifest disagree")

        sidecar_hash, sidecar_name = (root / f"{ARCHIVE}.sha256").read_text(
            encoding="utf-8"
        ).split()
        require(sidecar_name == ARCHIVE and sidecar_hash == digest(root / ARCHIVE),
                "public archive sidecar mismatch")
        marker = archive_bytes(root / ARCHIVE, "ARCHIVE_SOURCE_COMMIT.txt").decode().strip()
        require(marker == tag_commit, "archive marker and public tag differ")
        verify_tracked_blob_records(
            public_project_blobs(tag_commit), archive_project_blobs(root / ARCHIVE)
        )
        mutation_test_tag_binding()
        metadata_bytes = archive_bytes(
            root / ARCHIVE, "s_tc_jc_landmark_closure/RELEASE_METADATA.json"
        )
        final_bytes = archive_bytes(
            root / ARCHIVE, "s_tc_jc_landmark_closure/FINAL_OUTCOME.json"
        )
        metadata = json.loads(metadata_bytes)
        require(metadata["release_revision"] == TAG,
                "archive metadata release revision changed")
        require(hashlib.sha256(metadata_bytes).hexdigest() == envelope["core_metadata_sha256"],
                "archive metadata and public envelope disagree")
        require(hashlib.sha256(final_bytes).hexdigest() == envelope["final_outcome_sha256"],
                "archive final outcome and public envelope disagree")
        for transcript in TRANSCRIPTS:
            content = (root / transcript).read_text(encoding="utf-8", errors="replace")
            for needle in (
                f"commit={tag_commit}", "CLEAN_BEFORE=yes", "exit_status=0",
                "CLEAN_AFTER=yes",
            ):
                require(needle in content, f"{transcript}: missing {needle}")

        subprocess.run(
            [sys.executable,
             str(Path(__file__).with_name("verify_extracted_archive.py")),
             str(root / ARCHIVE)],
            check=True,
        )

        result = public_result(release["url"], tag_commit, manifest_path)
        validate_result_manifest(result, manifest_path)

    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
