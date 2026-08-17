#!/usr/bin/env python3
"""Download and verify the published v1.1.2 GitHub Release fail-closed."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile


REPO_SLUG = "AlecKriebel/Math"
TAG = "stc-jc-sharp-boundary-v1.1.2"
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
        for transcript in (
            "verify_quick.log", "verify_full.log", "verify_regenerate_all.log"
        ):
            content = (root / transcript).read_text(encoding="utf-8", errors="replace")
            for needle in (
                f"commit={tag_commit}", "CLEAN_BEFORE=yes", "exit_status=0",
                "CLEAN_AFTER=yes",
            ):
                require(needle in content, f"{transcript}: missing {needle}")

        result = public_result(release["url"], tag_commit, manifest_path)
        validate_result_manifest(result, manifest_path)

    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
