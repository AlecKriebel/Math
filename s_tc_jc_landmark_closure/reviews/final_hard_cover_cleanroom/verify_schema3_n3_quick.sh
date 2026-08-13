#!/usr/bin/env bash
set -euo pipefail

review_dir="$(cd "$(dirname "$0")" && pwd)"
repo_dir="$(cd "$review_dir/../.." && pwd)"
cd "$repo_dir"

/usr/bin/python3 reviews/final_hard_cover_cleanroom/verify_schema3_n3_path_certificate.py
