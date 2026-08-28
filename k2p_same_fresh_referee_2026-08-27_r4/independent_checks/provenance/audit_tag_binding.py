#!/usr/bin/env python3
"""Compare every distributed referee member with an annotated Git tag."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path, PurePosixPath


def run(repository: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise SystemExit(result.stderr.decode("utf-8", "replace"))
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--project-path", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    tag_type = run(args.repository, "cat-file", "-t", args.tag).decode().strip()
    tag_object = run(args.repository, "rev-parse", f"{args.tag}^{{tag}}").decode().strip()
    peeled_commit = run(args.repository, "rev-parse", f"{args.tag}^{{}}").decode().strip()
    head = run(args.repository, "rev-parse", "HEAD").decode().strip()
    origin_main = run(args.repository, "rev-parse", "origin/main").decode().strip()
    changed_project_paths = run(
        args.repository,
        "diff",
        "--name-only",
        peeled_commit,
        head,
        "--",
        args.project_path,
    ).decode("utf-8").splitlines()
    tag_ancestor_of_head = subprocess.run(
        [
            "git",
            "-C",
            str(args.repository),
            "merge-base",
            "--is-ancestor",
            peeled_commit,
            head,
        ],
        check=False,
    ).returncode == 0

    mismatches: list[str] = []
    missing_at_tag: list[str] = []
    distributed: dict[str, dict[str, object]] = {}
    with zipfile.ZipFile(args.archive) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            pure = PurePosixPath(info.filename)
            relative = PurePosixPath(*pure.parts[1:]).as_posix()
            repository_relative = f"{args.project_path.rstrip('/')}/{relative}"
            result = subprocess.run(
                ["git", "-C", str(args.repository), "show", f"{args.tag}:{repository_relative}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if result.returncode:
                missing_at_tag.append(relative)
                continue
            current = archive.read(info)
            tagged = result.stdout
            if current != tagged:
                mismatches.append(relative)
            distributed[relative] = {
                "bytes": len(current),
                "sha256": hashlib.sha256(current).hexdigest(),
            }

    tree_lines = run(
        args.repository,
        "ls-tree",
        "-r",
        "--name-only",
        args.tag,
        args.project_path,
    ).decode("utf-8").splitlines()
    project_prefix = args.project_path.rstrip("/") + "/"
    tagged_project_paths = {
        path[len(project_prefix):]
        for path in tree_lines
        if path.startswith(project_prefix)
    }
    sidecar = Path(str(args.archive) + ".sha256")
    sidecar_text = sidecar.read_text(encoding="utf-8").strip() if sidecar.is_file() else None
    archive_sha256 = hashlib.sha256(args.archive.read_bytes()).hexdigest()
    sidecar_digest = sidecar_text.split()[0] if sidecar_text else None
    tagged_sidecar_path = (
        f"{args.project_path.rstrip('/')}/proof_compression_submission/output/"
        f"{sidecar.name}"
    )
    tagged_sidecar = run(
        args.repository, "show", f"{args.tag}:{tagged_sidecar_path}"
    ).decode("utf-8").strip()
    remote_lines = run(
        args.repository,
        "ls-remote",
        "--tags",
        "origin",
        f"refs/tags/{args.tag}",
        f"refs/tags/{args.tag}^{{}}",
    ).decode("utf-8").splitlines()
    remote_refs = {
        reference: object_id
        for object_id, reference in (line.split("\t", 1) for line in remote_lines)
    }
    result = {
        "tag": args.tag,
        "tag_type": tag_type,
        "tag_object": tag_object,
        "peeled_commit": peeled_commit,
        "repository_head": head,
        "head_equals_peeled_commit": head == peeled_commit,
        "origin_main": origin_main,
        "origin_main_equals_peeled_commit": origin_main == peeled_commit,
        "tag_commit_is_ancestor_of_head": tag_ancestor_of_head,
        "project_paths_changed_between_tag_and_head": changed_project_paths,
        "project_tree_unchanged_between_tag_and_head": not changed_project_paths,
        "archive_sha256": archive_sha256,
        "archive_sidecar": str(sidecar),
        "archive_sidecar_text": sidecar_text,
        "archive_sidecar_matches": sidecar_digest == archive_sha256,
        "archive_sidecar_byte_identical_to_tag": tagged_sidecar == sidecar_text,
        "remote_tag_object": remote_refs.get(f"refs/tags/{args.tag}"),
        "remote_peeled_commit": remote_refs.get(f"refs/tags/{args.tag}^{{}}"),
        "remote_tag_matches_local": (
            remote_refs.get(f"refs/tags/{args.tag}") == tag_object
            and remote_refs.get(f"refs/tags/{args.tag}^{{}}") == peeled_commit
        ),
        "distributed_file_count": len(distributed) + len(missing_at_tag),
        "byte_identical_to_tag_count": len(distributed) - len(mismatches),
        "missing_at_tag": sorted(missing_at_tag),
        "byte_mismatches": sorted(mismatches),
        "all_distributed_members_byte_identical_to_tag": not missing_at_tag and not mismatches,
        "tagged_project_file_count": len(tagged_project_paths),
        "tagged_project_files_not_distributed": sorted(tagged_project_paths - set(distributed)),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
