#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$HERE/../../../../.." && pwd)

"$ROOT/.venv/bin/python" "$HERE/verify_clique_satellites.py"
OPENBLAS_NUM_THREADS=1 "$ROOT/.venv/bin/python" "$HERE/certify_unweighted_gadgets.py"
