#!/usr/bin/env bash
set -euo pipefail

HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO="$(CDPATH= cd -- "$HERE/../.." && pwd)"

exec python3 "$HERE/cleanroom_verify.py" \
  --repo "$REPO" \
  --family n3 \
  --output "$HERE/certificates/n3_full_replay.json" \
  --mutation-output "$HERE/certificates/n3_mutation_replay.json" \
  --manifest-output "$HERE/certificates/n3_manifest.json"

