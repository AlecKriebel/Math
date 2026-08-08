#!/usr/bin/env bash
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../../../../.." && pwd)"
python="$repo/.venv/bin/python"

"$python" "$here/verify_integrated_lumping.py"
"$python" "$here/verify_far_field_algebra.py"
"$python" "$here/verify_portal_clone_obstruction.py"
