#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s [--with-pdf]\n' "$(basename "$0")" >&2
}

with_pdf=0
if [[ $# -eq 1 && "$1" == "--with-pdf" ]]; then
  with_pdf=1
elif [[ $# -ne 0 ]]; then
  usage
  exit 2
fi

packet_dir="$(cd "$(dirname "$0")" && pwd -P)"
materials_dir="$packet_dir/materials"
manifest="$packet_dir/PACKET_SHA256SUMS"

if [[ ! -d "$materials_dir" || ! -f "$manifest" ]]; then
  printf 'Packet is incomplete: materials/ or PACKET_SHA256SUMS is missing.\n' >&2
  exit 1
fi

unset PYTHONPATH PYTHONHOME PYTHONOPTIMIZE
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0

if ! command -v python3 >/dev/null 2>&1; then
  printf 'Python 3 is required.\n' >&2
  exit 1
fi

python3 - <<'PY'
import sys
if sys.version_info < (3, 10):
    raise SystemExit("Python 3.10 or newer is required")
print(f"Python {sys.version.split()[0]}")
PY

verify_packet_integrity() {
  PACKET_ROOT="$packet_dir" python3 - <<'PY'
from hashlib import sha256
from pathlib import Path
import os
import stat

root = Path(os.environ["PACKET_ROOT"])
manifest_path = root / "PACKET_SHA256SUMS"
try:
    manifest_mode = manifest_path.lstat().st_mode
except OSError as exc:
    raise SystemExit(f"Cannot inspect integrity manifest: {exc}") from exc
if not stat.S_ISREG(manifest_mode):
    raise SystemExit("Integrity manifest must be a regular file, not a link or special file")
entries = {}
for number, line in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), 1):
    if not line:
        continue
    try:
        digest, rel = line.split("  ", 1)
    except ValueError as exc:
        raise SystemExit(f"Malformed manifest line {number}") from exc
    path = Path(rel)
    if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise SystemExit(f"Malformed SHA-256 on manifest line {number}")
    if path.is_absolute() or ".." in path.parts or rel == "PACKET_SHA256SUMS":
        raise SystemExit(f"Unsafe or self-referential path on manifest line {number}: {rel}")
    if rel in entries:
        raise SystemExit(f"Duplicate manifest path: {rel}")
    entries[rel] = digest

actual_files = set()
actual_dirs = {"."}

def walk_error(exc):
    raise exc

try:
    for directory, dirnames, filenames in os.walk(
        root, topdown=True, followlinks=False, onerror=walk_error
    ):
        directory_path = Path(directory)
        directory_rel = directory_path.relative_to(root).as_posix()
        if directory_rel != ".":
            actual_dirs.add(directory_rel)
        for name in [*dirnames, *filenames]:
            item = directory_path / name
            rel = item.relative_to(root).as_posix()
            mode = item.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise SystemExit(f"Symbolic link rejected: {rel}")
            if stat.S_ISDIR(mode):
                actual_dirs.add(rel)
            elif stat.S_ISREG(mode):
                if item != manifest_path:
                    actual_files.add(rel)
            else:
                raise SystemExit(f"Nonregular packet entry rejected: {rel}")
except OSError as exc:
    raise SystemExit(f"Packet traversal failed closed: {exc}") from exc

expected = set(entries)
if actual_files != expected:
    missing = sorted(expected - actual_files)
    extra = sorted(actual_files - expected)
    raise SystemExit(f"Packet path-set mismatch; missing={missing}; extra={extra}")

expected_dirs = {"."}
for rel in expected | {"PACKET_SHA256SUMS"}:
    parent = Path(rel).parent
    while parent.as_posix() != ".":
        expected_dirs.add(parent.as_posix())
        parent = parent.parent
if actual_dirs != expected_dirs:
    missing = sorted(expected_dirs - actual_dirs)
    extra = sorted(actual_dirs - expected_dirs)
    raise SystemExit(f"Packet directory-set mismatch; missing={missing}; extra={extra}")

for rel in sorted(expected):
    path = root / rel
    if path.is_symlink():
        raise SystemExit(f"Symbolic link rejected: {rel}")
    digest = sha256(path.read_bytes()).hexdigest()
    if digest != entries[rel]:
        raise SystemExit(f"SHA-256 mismatch: {rel}")
print(f"Packet integrity PASS ({len(entries)} manifest-listed files plus manifest)")
PY
}

compare_output() {
  label="$1"
  expected="$2"
  observed="$3"
  if ! cmp -s "$expected" "$observed"; then
    printf '%s output differs from %s\n' "$label" "${expected#$packet_dir/}" >&2
    diff -u "$expected" "$observed" >&2 || true
    exit 1
  fi
  printf '%s transcript PASS\n' "$label"
}

tmp_base="${TMPDIR:-/tmp}"
tmp_base="$(cd "$tmp_base" && pwd -P)"
work_dir="$(mktemp -d "$tmp_base/k2p-referee-replay.XXXXXX")"
case "$work_dir" in
  "$tmp_base"/k2p-referee-replay.*) ;;
  *) printf 'Refusing unexpected temporary path: %s\n' "$work_dir" >&2; exit 1 ;;
esac
cleanup() {
  rm -rf -- "$work_dir"
}
trap cleanup EXIT INT TERM

verify_packet_integrity

printf '\nRunning complete exact replay...\n'
(cd "$materials_dir" && python3 verify.py) >"$work_dir/complete.normal.txt"
compare_output "Complete normal replay" \
  "$materials_dir/verification_report_complete.txt" \
  "$work_dir/complete.normal.txt"

(cd "$materials_dir" && PYTHONOPTIMIZE=1 python3 verify.py) \
  >"$work_dir/complete.optimized.txt"
compare_output "Complete optimized replay" \
  "$materials_dir/verification_report_complete.txt" \
  "$work_dir/complete.optimized.txt"

printf '\nRunning focused transcript replays...\n'
(cd "$materials_dir" && python3 verify_k2p_simple.py) >"$work_dir/simple.txt"
compare_output "Focused compact K2P replay" \
  "$materials_dir/verification_report_simple.txt" "$work_dir/simple.txt"

(cd "$materials_dir" && python3 verify_k2p_displayed_trees.py) \
  >"$work_dir/displayed.txt"
compare_output "Focused displayed-tree replay" \
  "$materials_dir/verification_report_displayed_trees.txt" \
  "$work_dir/displayed.txt"

(cd "$materials_dir" && python3 src/verify_source_conventions.py) \
  >"$work_dir/source.txt"
compare_output "Focused source-convention replay" \
  "$materials_dir/verification_report_source_conventions.txt" \
  "$work_dir/source.txt"

(cd "$materials_dir" && python3 src/verify_k2p_four_leaf_graft.py) \
  >"$work_dir/four-leaf.txt"
compare_output "Focused four-leaf graft replay" \
  "$materials_dir/verification_report_four_leaf_graft.txt" \
  "$work_dir/four-leaf.txt"

(cd "$materials_dir" && PYTHONOPTIMIZE=1 python3 src/verify_k2p_four_leaf_graft.py) \
  >"$work_dir/four-leaf.optimized.txt"
compare_output "Optimized four-leaf graft replay" \
  "$materials_dir/verification_report_four_leaf_graft.txt" \
  "$work_dir/four-leaf.optimized.txt"

printf '\nRunning individual supporting entry points...\n'
(cd "$materials_dir" && python3 src/verify_k2p_extended.py) \
  >"$work_dir/k2p-extended.txt"
(cd "$materials_dir" && python3 src/verify_k2p_rank_family.py) \
  >"$work_dir/k2p-rank-family.txt"
(cd "$materials_dir" && python3 src/verify_k3p.py) \
  >"$work_dir/k3p.txt"
(cd "$materials_dir" && python3 src/test_k3p_semantic_mutations.py) \
  >"$work_dir/k3p-semantic-mutations.txt"
printf 'Individual supporting entry points PASS\n'

printf '\nRegenerating the compact certificate in a disposable copy...\n'
cp -R "$materials_dir" "$work_dir/certificate-replay"
python3 "$work_dir/certificate-replay/src/generate_k2p_simple_certificate.py" \
  >"$work_dir/generator.txt"
if ! cmp -s "$materials_dir/certificate_k2p_simple.json" \
  "$work_dir/certificate-replay/certificate_k2p_simple.json"; then
  printf 'Regenerated compact certificate differs from the supplied certificate.\n' >&2
  exit 1
fi
printf 'Compact certificate regeneration PASS\n'

if [[ "$with_pdf" -eq 1 ]]; then
  printf '\nRebuilding all PDFs in a disposable copy...\n'
  if ! command -v pdftotext >/dev/null 2>&1; then
    printf 'pdftotext is required for --with-pdf.\n' >&2
    exit 1
  fi
  if ! command -v latexmk >/dev/null 2>&1 && ! command -v tectonic >/dev/null 2>&1; then
    printf 'latexmk or tectonic is required for --with-pdf.\n' >&2
    exit 1
  fi
  cp -R "$materials_dir" "$work_dir/pdf-replay"
  rm -f -- \
    "$work_dir/pdf-replay/combined-paper-clarified.pdf" \
    "$work_dir/pdf-replay/technical-summary-clarified.pdf" \
    "$work_dir/pdf-replay/k2p_displayed_tree_clarification.pdf"
  bash "$work_dir/pdf-replay/src/build_pdfs.sh" >"$work_dir/pdf-build.txt" 2>&1
  for stem in combined-paper-clarified technical-summary-clarified k2p_displayed_tree_clarification; do
    pdftotext -layout "$materials_dir/$stem.pdf" "$work_dir/$stem.supplied.txt"
    pdftotext -layout "$work_dir/pdf-replay/$stem.pdf" "$work_dir/$stem.rebuilt.txt"
    if ! cmp -s "$work_dir/$stem.supplied.txt" "$work_dir/$stem.rebuilt.txt"; then
      printf 'Rebuilt PDF text differs for %s.pdf\n' "$stem" >&2
      diff -u "$work_dir/$stem.supplied.txt" "$work_dir/$stem.rebuilt.txt" >&2 || true
      exit 1
    fi
  done
  printf 'Disposable PDF rebuild and extracted-text comparison PASS\n'
fi

verify_packet_integrity
printf '\nALL REFEREE REPLAY CHECKS PASSED\n'
