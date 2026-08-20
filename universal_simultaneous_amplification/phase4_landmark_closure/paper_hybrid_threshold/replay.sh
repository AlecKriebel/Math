#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project=$(CDPATH= cd -- "$paper_dir/../.." && pwd)
python=${PYTHON:-"$project/.venv/bin/python"}

if [ ! -x "$python" ]; then
  python=${PYTHON:-python3}
fi

export PYTHONDONTWRITEBYTECODE=1

"$python" "$paper_dir/certificates/verify_leading_algebra.py"
"$python" "$paper_dir/certificates/verify_hybrid_lumping.py"
"$python" "$paper_dir/certificates/verify_hybrid_coefficients.py"
"$python" "$paper_dir/verify_paper_claims.py"
