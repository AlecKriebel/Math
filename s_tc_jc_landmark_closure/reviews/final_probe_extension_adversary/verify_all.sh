#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../.." && pwd)
cd "$ROOT"

python3 reviews/final_probe_extension_adversary/make_fixture.py
python3 reviews/final_probe_extension_adversary/produce_probe_extension.py \
  reviews/final_probe_extension_adversary/certificates/fixture_seeds.json \
  reviews/final_probe_extension_adversary/certificates/fixture_produced.json
python3 reviews/final_probe_extension_adversary/verify_probe_extension.py \
  reviews/final_probe_extension_adversary/certificates/fixture.json
python3 reviews/final_probe_extension_adversary/verify_probe_extension.py \
  reviews/final_probe_extension_adversary/certificates/fixture_produced.json
python3 reviews/final_probe_extension_adversary/mutation_tests.py
shasum -a 256 -c reviews/final_probe_extension_adversary/MANIFEST.sha256

echo "EXACT REVIEW IMPLEMENTATION PASSES; FINAL N3+N4 STREAM AUDIT PENDING"
