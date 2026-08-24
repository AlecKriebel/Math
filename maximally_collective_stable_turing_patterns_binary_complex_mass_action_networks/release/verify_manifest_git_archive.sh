#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(git -C "$ROOT" rev-parse --show-toplevel)"
PROJECT_PREFIX="$(git -C "$ROOT" rev-parse --show-prefix)"
REF="${1:-HEAD}"

archive_root="$(mktemp -d "${TMPDIR:-/tmp}/exact-diffusion-manifest-archive.XXXXXX")"
trap 'rm -rf "$archive_root"' EXIT

git -C "$REPO_ROOT" archive "$REF" "$PROJECT_PREFIX" | tar -x -C "$archive_root"
snapshot="$archive_root/${PROJECT_PREFIX%/}"
(
  cd "$snapshot"
  bash release/create_release_manifest.sh --check >/dev/null
  listed="$(wc -l < release/sha256_manifest.txt | tr -d ' ')"
  present="$(find . -type f ! -path './release/sha256_manifest.txt' | wc -l | tr -d ' ')"
  [[ "$listed" == "$present" ]] || {
    printf 'release manifest/archive file-count mismatch: listed=%s present=%s\n' \
      "$listed" "$present" >&2
    exit 2
  }
  printf 'RELEASE_MANIFEST_GIT_ARCHIVE_PASS ref=%s entries=%s\n' "$REF" "$listed"
)
