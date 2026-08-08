#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$here/../../.." && pwd)
bootstrap_python=${BOOTSTRAP_PYTHON:-python3}

if [ ! -x "$root/.venv/bin/python" ]; then
  "$bootstrap_python" -m venv "$root/.venv"
fi

"$root/.venv/bin/python" -m pip install \
  --disable-pip-version-check \
  --requirement "$here/requirements.txt"

PYTHON="$root/.venv/bin/python" "$here/replay.sh"
