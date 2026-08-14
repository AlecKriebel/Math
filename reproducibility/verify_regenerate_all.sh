#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec bash "$REPO/s_tc_jc_landmark_closure/reproducibility/verify_regenerate_all.sh"
