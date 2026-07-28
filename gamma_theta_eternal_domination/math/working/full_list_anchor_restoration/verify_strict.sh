#!/bin/sh
set -eu

anchor_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
anchor_tmp=$(mktemp -d)
trap 'rm -rf -- "$anchor_tmp"' EXIT HUP INT TERM

python3 -I -B -W error "$anchor_dir/verify_control.py" \
  > "$anchor_tmp/result.json"

actual_sha=$(
  shasum -a 256 "$anchor_tmp/result.json" | awk '{print $1}'
)
expected_sha=$(
  python3 -I -B -W error -c \
    'import json,sys; stream=open(sys.argv[1], encoding="utf-8"); data=json.load(stream); stream.close(); print(data["verifier_stdout_sha256"])' \
    "$anchor_dir/expected_result.json"
)

if [ "$actual_sha" != "$expected_sha" ]; then
  echo "strict replay mismatch: $actual_sha != $expected_sha" >&2
  exit 1
fi

echo "PASS full-list anchor-restoration strict replay $actual_sha"
