#!/bin/zsh

set -eu

delivery_manifest="/Users/alec/Documents/Math/complete_graph_extremality_r3_rereview_2026-08-23/work/package/source_and_certificates/MANIFEST.sha256"
source_repo="/Users/alec/Documents/Math-universal-amplification"
source_commit="b9a415f763e82d9cc45c83de96c895b109e158a4"
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

[[ "$checked" -eq 71 ]]
print -- "PASS: $checked archive payload files match source commit $source_commit"
