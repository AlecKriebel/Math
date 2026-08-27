#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' \
    'Usage: bash submission/build_release.sh --output-dir DIR [--commit REF] [--version VERSION]' \
    '' \
    'Build deterministic ZIP and tar.gz archives of the committed canonical' \
    'package. REF defaults to HEAD. VERSION defaults to the version recorded' \
    'in CITATION.cff. The version, citation metadata, and annotated release tag' \
    'k2p-k3p-theta-v<VERSION> must all identify the same commit.' \
    'DIR must not already contain target filenames. The canonical subtree must' \
    'have no tracked or nonignored untracked changes. Author-only submission/biorxiv files' \
    'are excluded from the release archives.'
}

output_dir=''
commit_ref='HEAD'
release_version=''
while (($#)); do
  case "$1" in
    --output-dir)
      (($# >= 2)) || { usage >&2; exit 2; }
      output_dir=$2
      shift 2
      ;;
    --commit)
      (($# >= 2)) || { usage >&2; exit 2; }
      commit_ref=$2
      shift 2
      ;;
    --version)
      (($# >= 2)) || { usage >&2; exit 2; }
      release_version=$2
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ -n "$output_dir" ]] || { usage >&2; exit 2; }

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
package_dir=$(cd -- "$script_dir/.." && pwd -P)
repo_root=$(git -C "$package_dir" rev-parse --show-toplevel)
case "$package_dir" in
  "$repo_root"/*) package_rel=${package_dir#"$repo_root"/} ;;
  *) printf 'Canonical package is not inside the Git worktree.\n' >&2; exit 1 ;;
esac

dirty=$(git -C "$repo_root" status --porcelain=v1 --untracked-files=all -- "$package_rel")
if [[ -n "$dirty" ]]; then
  printf 'Refusing to archive a modified canonical subtree:\n%s\n' "$dirty" >&2
  exit 1
fi

full_commit=$(git -C "$repo_root" rev-parse --verify "${commit_ref}^{commit}")
short_commit=${full_commit:0:12}

citation_path="${package_rel}/CITATION.cff"
citation_version=$(
  git -C "$repo_root" show "${full_commit}:${citation_path}" |
    awk '
      /^version:[[:space:]]*/ {
        value=$0
        sub(/^version:[[:space:]]*/, "", value)
        gsub(/^[[:space:]\"]+|[[:space:]\"]+$/, "", value)
        print value
        exit
      }
    '
) || {
  printf 'Could not read CITATION.cff at %s.\n' "$short_commit" >&2
  exit 1
}
[[ -n "$citation_version" ]] || {
  printf 'CITATION.cff has no top-level release version at %s.\n' "$short_commit" >&2
  exit 1
}
if [[ -z "$release_version" ]]; then
  release_version=$citation_version
elif [[ "$release_version" != "$citation_version" ]]; then
  printf 'Requested version %s does not match CITATION.cff version %s at %s.\n' \
    "$release_version" "$citation_version" "$short_commit" >&2
  exit 1
fi

release_tag="k2p-k3p-theta-v${release_version}"
tag_type=$(git -C "$repo_root" cat-file -t "refs/tags/${release_tag}" 2>/dev/null) || {
  printf 'Required release tag is absent: %s\n' "$release_tag" >&2
  exit 1
}
if [[ "$tag_type" != tag ]]; then
  printf 'Required release tag is not annotated: %s\n' "$release_tag" >&2
  exit 1
fi
tag_commit=$(git -C "$repo_root" rev-parse --verify "${release_tag}^{commit}" 2>/dev/null) || {
  printf 'Required release tag is absent: %s\n' "$release_tag" >&2
  exit 1
}
if [[ "$tag_commit" != "$full_commit" ]]; then
  printf 'Release tag %s identifies %s, not requested commit %s.\n' \
    "$release_tag" "$tag_commit" "$full_commit" >&2
  exit 1
fi

required=(
  README.md
  PROVENANCE.md
  CHANGELOG.md
  RESEARCH_LOG.md
  ADVERSARIAL_REVIEW_DISPOSITION.md
  CERTIFICATE_FIELD_COVERAGE.md
  combined-paper-clarified.tex
  combined-paper-clarified.pdf
  technical-summary-clarified.tex
  technical-summary-clarified.pdf
  k2p_displayed_tree_clarification.tex
  k2p_displayed_tree_clarification.pdf
  verify.py
  verification_report_complete.txt
  verification_report_simple.txt
  verification_report_displayed_trees.txt
  verification_report_four_leaf_graft.txt
  verification_report_source_conventions.txt
  CITATION.cff
  manifest.sha256
  LICENSE-CODE
  LICENSES.md
  src/verify_k2p_four_leaf_graft.py
  submission/build_release.sh
)
for rel in "${required[@]}"; do
  if ! git -C "$repo_root" cat-file -e "${full_commit}:${package_rel}/${rel}"; then
    printf 'Required release file is absent at %s: %s\n' "$short_commit" "$rel" >&2
    exit 1
  fi
done

excluded_prefix="${package_rel}/submission/biorxiv/"
archive_repo_paths=()
archive_paths=()
while IFS= read -r repo_path; do
  [[ "$repo_path" == "$excluded_prefix"* ]] && continue
  archive_repo_paths+=("$repo_path")
  archive_paths+=("${repo_path#"$package_rel"/}")
done < <(git -C "$repo_root" ls-tree -r --name-only "$full_commit" -- "$package_rel")
if ((${#archive_paths[@]} == 0)); then
  printf 'No committed release files remain after applying exclusions.\n' >&2
  exit 1
fi
if printf '%s\n' "${archive_paths[@]}" | grep -Eq '(^|/)(__pycache__/|[^/]*\.py[co]$)'; then
  printf 'Refusing to archive tracked Python cache/bytecode files.\n' >&2
  exit 1
fi

output_dir=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$output_dir")
case "$output_dir" in
  "$package_dir"|"$package_dir"/*)
    printf 'Output directory must be outside the canonical package: %s\n' "$output_dir" >&2
    exit 1
    ;;
esac
mkdir -p -- "$output_dir"
stem="k2p-k3p-theta-collision-${short_commit}"
zip_name="${stem}.zip"
tgz_name="${stem}.tar.gz"
sums_name="SHA256SUMS-${short_commit}"
zip_sidecar="${zip_name}.sha256"
tgz_sidecar="${tgz_name}.sha256"
for name in "$zip_name" "$tgz_name" "$sums_name" "$zip_sidecar" "$tgz_sidecar"; do
  [[ ! -e "$output_dir/$name" ]] || {
    printf 'Refusing to overwrite existing release output: %s\n' "$output_dir/$name" >&2
    exit 1
  }
done

tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/k2p-release.XXXXXX")
trap 'rm -rf -- "$tmp_dir"' EXIT

git -C "$repo_root" show "${full_commit}:${package_rel}/manifest.sha256" >"$tmp_dir/canonical-manifest.sha256"
if ! awk '
  length($1) != 64 || $1 !~ /^[0-9a-fA-F]+$/ || substr($0,65,2) != "  " || length(substr($0,67)) == 0 { exit 1 }
' "$tmp_dir/canonical-manifest.sha256"; then
  printf 'Malformed canonical manifest at %s.\n' "$short_commit" >&2
  exit 1
fi
printf '%s\n' "${archive_paths[@]}" | awk '$0 != "manifest.sha256"' | LC_ALL=C sort >"$tmp_dir/expected-manifest-paths"
awk '{ print substr($0,67) }' "$tmp_dir/canonical-manifest.sha256" | LC_ALL=C sort >"$tmp_dir/actual-manifest-paths"
if ! cmp -s "$tmp_dir/expected-manifest-paths" "$tmp_dir/actual-manifest-paths"; then
  printf 'Canonical manifest path set does not match the release file set at %s.\n' "$short_commit" >&2
  exit 1
fi

sha256_value() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  else
    shasum -a 256 "$1" | awk '{print $1}'
  fi
}

# Hash exactly the committed files selected for the release archive. The two
# generated metadata files are intentionally not self-listed; the provenance
# record binds this manifest, and the external sidecars bind complete archives.
for repo_path in "${archive_repo_paths[@]}"; do
  archive_path=${repo_path#"$package_rel"/}
  blob_file="$tmp_dir/blob"
  git -C "$repo_root" cat-file blob "${full_commit}:${repo_path}" >"$blob_file"
  printf '%s  %s\n' "$(sha256_value "$blob_file")" "$archive_path"
done >"$tmp_dir/FILE_SHA256SUMS"
file_manifest_sha256=$(sha256_value "$tmp_dir/FILE_SHA256SUMS")
file_manifest=$(<"$tmp_dir/FILE_SHA256SUMS")
file_manifest+=$'\n'
provenance=$(printf '%s\n' \
  'format-version: 1' \
  "release-version: ${release_version}" \
  "git-commit: ${full_commit}" \
  'repository-url: https://github.com/AlecKriebel/Math' \
  "canonical-subtree: ${package_rel}" \
  "excluded-path: ${excluded_prefix}" \
  'file-sha256-manifest: FILE_SHA256SUMS' \
  "file-sha256-manifest-sha256: ${file_manifest_sha256}" \
  'builder: submission/build_release.sh')
provenance+=$'\n'
printf '%s' "$provenance" >"$tmp_dir/RELEASE_PROVENANCE.txt"

archive_common=(
  --prefix="${stem}/"
  --add-virtual-file="${stem}/RELEASE_PROVENANCE.txt:${provenance}"
  --add-virtual-file="${stem}/FILE_SHA256SUMS:${file_manifest}"
)

git -C "$repo_root" archive \
  --format=zip \
  "${archive_common[@]}" \
  "${full_commit}:${package_rel}" "${archive_paths[@]}" >"$tmp_dir/$zip_name"
git -C "$repo_root" archive \
  --format=tar \
  "${archive_common[@]}" \
  "${full_commit}:${package_rel}" "${archive_paths[@]}" | gzip -n -9 >"$tmp_dir/$tgz_name"

# Rebuild both forms once and compare them before publishing any output.
git -C "$repo_root" archive \
  --format=zip \
  "${archive_common[@]}" \
  "${full_commit}:${package_rel}" "${archive_paths[@]}" >"$tmp_dir/recheck.zip"
git -C "$repo_root" archive \
  --format=tar \
  "${archive_common[@]}" \
  "${full_commit}:${package_rel}" "${archive_paths[@]}" | gzip -n -9 >"$tmp_dir/recheck.tar.gz"
cmp -s "$tmp_dir/$zip_name" "$tmp_dir/recheck.zip" || {
  printf 'ZIP determinism self-check failed.\n' >&2
  exit 1
}
cmp -s "$tmp_dir/$tgz_name" "$tmp_dir/recheck.tar.gz" || {
  printf 'tar.gz determinism self-check failed.\n' >&2
  exit 1
}

unzip -tq "$tmp_dir/$zip_name" >/dev/null
gzip -t "$tmp_dir/$tgz_name"
unzip -p "$tmp_dir/$zip_name" "${stem}/RELEASE_PROVENANCE.txt" >"$tmp_dir/zip-provenance"
cmp -s "$tmp_dir/RELEASE_PROVENANCE.txt" "$tmp_dir/zip-provenance" || {
  printf 'ZIP internal provenance check failed.\n' >&2
  exit 1
}
tar -xOzf "$tmp_dir/$tgz_name" "${stem}/RELEASE_PROVENANCE.txt" >"$tmp_dir/tar-provenance"
cmp -s "$tmp_dir/RELEASE_PROVENANCE.txt" "$tmp_dir/tar-provenance" || {
  printf 'tar.gz internal provenance check failed.\n' >&2
  exit 1
}
unzip -p "$tmp_dir/$zip_name" "${stem}/FILE_SHA256SUMS" >"$tmp_dir/zip-file-manifest"
cmp -s "$tmp_dir/FILE_SHA256SUMS" "$tmp_dir/zip-file-manifest" || {
  printf 'ZIP internal file-manifest check failed.\n' >&2
  exit 1
}
tar -xOzf "$tmp_dir/$tgz_name" "${stem}/FILE_SHA256SUMS" >"$tmp_dir/tar-file-manifest"
cmp -s "$tmp_dir/FILE_SHA256SUMS" "$tmp_dir/tar-file-manifest" || {
  printf 'tar.gz internal file-manifest check failed.\n' >&2
  exit 1
}

extract_dir="$tmp_dir/extracted"
mkdir -p "$extract_dir"
unzip -q "$tmp_dir/$zip_name" -d "$extract_dir"
if command -v sha256sum >/dev/null 2>&1; then
  (cd "$extract_dir/$stem" && sha256sum -c FILE_SHA256SUMS >/dev/null)
  (cd "$extract_dir/$stem" && sha256sum -c manifest.sha256 >/dev/null)
else
  (cd "$extract_dir/$stem" && shasum -a 256 -c FILE_SHA256SUMS >/dev/null)
  (cd "$extract_dir/$stem" && shasum -a 256 -c manifest.sha256 >/dev/null)
fi

tar_extract_dir="$tmp_dir/extracted-tar"
mkdir -p "$tar_extract_dir"
tar -xzf "$tmp_dir/$tgz_name" -C "$tar_extract_dir"
diff -qr "$extract_dir/$stem" "$tar_extract_dir/$stem" >/dev/null || {
  printf 'ZIP and tar.gz extracted contents differ.\n' >&2
  exit 1
}

release_tree="$extract_dir/$stem"
(cd "$release_tree" && python3 verify.py) >"$tmp_dir/verification-normal.txt"
cmp -s "$release_tree/verification_report_complete.txt" "$tmp_dir/verification-normal.txt" || {
  printf 'Stored complete verification report is stale.\n' >&2
  exit 1
}
(cd "$release_tree" && PYTHONOPTIMIZE=1 python3 verify.py) >"$tmp_dir/verification-optimized.txt"
cmp -s "$release_tree/verification_report_complete.txt" "$tmp_dir/verification-optimized.txt" || {
  printf 'Optimized verification output differs from the stored complete report.\n' >&2
  exit 1
}
(cd "$release_tree" && python3 verify_k2p_simple.py) >"$tmp_dir/verification-simple.txt"
cmp -s "$release_tree/verification_report_simple.txt" "$tmp_dir/verification-simple.txt" || {
  printf 'Stored simple verification report is stale.\n' >&2
  exit 1
}
(cd "$release_tree" && python3 verify_k2p_displayed_trees.py) >"$tmp_dir/verification-displayed.txt"
cmp -s "$release_tree/verification_report_displayed_trees.txt" "$tmp_dir/verification-displayed.txt" || {
  printf 'Stored displayed-tree verification report is stale.\n' >&2
  exit 1
}
(cd "$release_tree" && python3 src/verify_source_conventions.py) >"$tmp_dir/verification-conventions.txt"
cmp -s "$release_tree/verification_report_source_conventions.txt" "$tmp_dir/verification-conventions.txt" || {
  printf 'Stored source-convention verification report is stale.\n' >&2
  exit 1
}
(cd "$release_tree" && python3 src/verify_k2p_four_leaf_graft.py) >"$tmp_dir/verification-four-leaf.txt"
cmp -s "$release_tree/verification_report_four_leaf_graft.txt" "$tmp_dir/verification-four-leaf.txt" || {
  printf 'Stored four-leaf graft verification report is stale.\n' >&2
  exit 1
}
(cd "$release_tree" && PYTHONOPTIMIZE=1 python3 src/verify_k2p_four_leaf_graft.py) >"$tmp_dir/verification-four-leaf-optimized.txt"
cmp -s "$release_tree/verification_report_four_leaf_graft.txt" "$tmp_dir/verification-four-leaf-optimized.txt" || {
  printf 'Optimized four-leaf graft output differs from the stored focused report.\n' >&2
  exit 1
}

for command_name in pdftotext pdftoppm; do
  command -v "$command_name" >/dev/null 2>&1 || {
    printf 'Required PDF validation command is unavailable: %s\n' "$command_name" >&2
    exit 1
  }
done
original_pdf_dir="$tmp_dir/original-pdfs"
mkdir -p "$original_pdf_dir"
pdf_stems=(
  combined-paper-clarified
  technical-summary-clarified
  k2p_displayed_tree_clarification
)
for pdf_stem in "${pdf_stems[@]}"; do
  cp "$release_tree/${pdf_stem}.pdf" "$original_pdf_dir/${pdf_stem}.pdf"
done
(cd "$release_tree" && bash src/build_pdfs.sh) >"$tmp_dir/pdf-build.txt" 2>&1 || {
  printf 'Clean-extraction PDF build failed; log follows.\n' >&2
  cat "$tmp_dir/pdf-build.txt" >&2
  exit 1
}
if grep -Eiq 'LaTeX Warning|Package [^ ]+ Warning|Overfull|Underfull|undefined (citation|reference)|^!' "$release_tree"/*.log; then
  printf 'Clean-extraction PDF build produced a TeX warning or error.\n' >&2
  exit 1
fi
for pdf_stem in "${pdf_stems[@]}"; do
  pdftotext -layout "$original_pdf_dir/${pdf_stem}.pdf" "$tmp_dir/${pdf_stem}-original.txt"
  pdftotext -layout "$release_tree/${pdf_stem}.pdf" "$tmp_dir/${pdf_stem}-rebuilt.txt"
  cmp -s "$tmp_dir/${pdf_stem}-original.txt" "$tmp_dir/${pdf_stem}-rebuilt.txt" || {
    printf 'Committed PDF text is stale for %s.pdf.\n' "$pdf_stem" >&2
    exit 1
  }
  mkdir -p "$tmp_dir/${pdf_stem}-original-pages" "$tmp_dir/${pdf_stem}-rebuilt-pages"
  pdftoppm -png -r 144 "$original_pdf_dir/${pdf_stem}.pdf" "$tmp_dir/${pdf_stem}-original-pages/page" >/dev/null 2>&1
  pdftoppm -png -r 144 "$release_tree/${pdf_stem}.pdf" "$tmp_dir/${pdf_stem}-rebuilt-pages/page" >/dev/null 2>&1
  diff -qr "$tmp_dir/${pdf_stem}-original-pages" "$tmp_dir/${pdf_stem}-rebuilt-pages" >/dev/null || {
    printf 'Committed PDF rendering is stale for %s.pdf.\n' "$pdf_stem" >&2
    exit 1
  }
done

{
  printf '%s  %s\n' "$(sha256_value "$tmp_dir/$zip_name")" "$zip_name"
  printf '%s  %s\n' "$(sha256_value "$tmp_dir/$tgz_name")" "$tgz_name"
} >"$tmp_dir/$sums_name"
printf '%s  %s\n' "$(sha256_value "$tmp_dir/$zip_name")" "$zip_name" \
  >"$tmp_dir/$zip_sidecar"
printf '%s  %s\n' "$(sha256_value "$tmp_dir/$tgz_name")" "$tgz_name" \
  >"$tmp_dir/$tgz_sidecar"

mv -- "$tmp_dir/$zip_name" "$output_dir/$zip_name"
mv -- "$tmp_dir/$tgz_name" "$output_dir/$tgz_name"
mv -- "$tmp_dir/$sums_name" "$output_dir/$sums_name"
mv -- "$tmp_dir/$zip_sidecar" "$output_dir/$zip_sidecar"
mv -- "$tmp_dir/$tgz_sidecar" "$output_dir/$tgz_sidecar"

printf 'Release commit: %s\n' "$full_commit"
printf 'Release version: %s\n' "$release_version"
printf 'Release tag: %s\n' "$release_tag"
printf 'Canonical subtree: %s\n' "$package_rel"
printf 'Excluded author-only path: %s\n' "$excluded_prefix"
printf 'Created:\n  %s\n  %s\n  %s\n  %s\n  %s\n' \
  "$output_dir/$zip_name" \
  "$output_dir/$tgz_name" \
  "$output_dir/$sums_name" \
  "$output_dir/$zip_sidecar" \
  "$output_dir/$tgz_sidecar"
