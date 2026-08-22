#!/bin/zsh

set -eu

delivery_manifest="/Users/alec/Documents/Math/complete_graph_extremality_r2_rereview_2026-08-22/work/package/source_and_certificates/MANIFEST.sha256"
source_repo="/Users/alec/Documents/Math-universal-amplification"
source_commit="e63cc44748e4084ade67c5ff7dc5d1bf2a872f7c"
checked=0

git -C "$source_repo" cat-file -e "$source_commit^{commit}"

while read -r expected member; do
  if [[ "$member" == "BUNDLE_METADATA.txt" ]]; then
    continue
  fi
  actual=$(git -C "$source_repo" show "$source_commit:$member" | shasum -a 256 | awk '{print $1}')
  if [[ "$actual" != "$expected" ]]; then
    print -u2 -- "MISMATCH $member expected=$expected actual=$actual"
    exit 1
  fi
  (( checked += 1 ))
  print -- "OK $member"
done < "$delivery_manifest"

[[ "$checked" -eq 69 ]]
print -- "PASS: $checked archive payload files match source commit $source_commit"
