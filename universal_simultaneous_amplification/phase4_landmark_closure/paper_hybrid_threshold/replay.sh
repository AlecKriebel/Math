#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
cd "$root"

./universal_simultaneous_amplification/phase4_landmark_closure/threshold/dilute_pair_leaf_hybrid/replay.sh
./universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_affine_global_v2/replay.sh
