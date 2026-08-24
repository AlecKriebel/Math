#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
MANIFEST=release/sha256_manifest.txt

if [[ "${1:-}" == "--check" ]]; then
  sha256sum -c "$MANIFEST" >/dev/null
  grep -Fq '  ./RESEARCH_LOG.md' "$MANIFEST"
  printf 'RELEASE_MANIFEST_PASS entries=%s\n' "$(wc -l < "$MANIFEST")"
  exit 0
fi

temporary_manifest="$(mktemp "$ROOT/release/.sha256_manifest.XXXXXX")"
trap 'rm -f "$temporary_manifest"' EXIT
# The immutable release is a Git snapshot.  Enumerating the working directory
# would let ignored referee scratch files contaminate the manifest with paths
# that are absent from the tag.  `git ls-files` is NUL-delimited, includes
# staged additions, and restricts the baseline to the exact tracked project.
while IFS= read -r -d '' tracked_path; do
  [[ "$tracked_path" == "$MANIFEST" ]] && continue
  [[ -f "$tracked_path" ]] || {
    printf 'tracked release file is absent: %s\n' "$tracked_path" >&2
    exit 2
  }
  printf './%s\0' "$tracked_path"
done < <(git ls-files -z -- .) \
  | sort -z \
  | xargs -0 sha256sum > "$temporary_manifest"
grep -Fq '  ./RESEARCH_LOG.md' "$temporary_manifest"
mv "$temporary_manifest" "$MANIFEST"
trap - EXIT
sha256sum -c "$MANIFEST" >/dev/null
printf 'RELEASE_MANIFEST_CREATED entries=%s\n' "$(wc -l < "$MANIFEST")"
