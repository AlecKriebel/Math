#!/usr/bin/env bash
set -euo pipefail

review_dir="$(cd "$(dirname "$0")" && pwd)"
repo_dir="$(cd "$review_dir/../.." && pwd)"
cd "$repo_dir"

if [[ -f reviews/final_hard_cover_cleanroom/MANIFEST.sha256 ]]; then
  shasum -a 256 -c reviews/final_hard_cover_cleanroom/MANIFEST.sha256
fi

bash reviews/final_hard_cover_cleanroom/verify_schema3_n4_quick.sh
bash reviews/final_hard_cover_cleanroom/verify_schema3_n3_quick.sh

if [[ -f reviews/final_hard_cover_cleanroom/MANIFEST.sha256 ]]; then
  shasum -a 256 -c reviews/final_hard_cover_cleanroom/MANIFEST.sha256
fi

echo "VERIFIED: active schema-3 n=4 theta-2 base hard cover"
echo "VERIFIED: schema-3 n=3 graph/path layer only"
echo "WITHDRAWN: schema-3 n=3 terminal routine (two-active-label incompatibility)"
echo "UNRESOLVED: complete schema-3 n=3 hard-cover gate"
echo "UNRESOLVED: active p/q probe closure"
