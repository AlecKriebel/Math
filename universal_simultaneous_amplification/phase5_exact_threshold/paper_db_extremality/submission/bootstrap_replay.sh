#!/bin/sh
set -eu

case ${PYTHONOPTIMIZE-} in
  ""|0) ;;
  *)
    echo "Refusing inherited PYTHONOPTIMIZE=${PYTHONOPTIMIZE}" >&2
    exit 2
    ;;
esac
unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME PYTHONSTARTUP PYTHONINSPECT \
  PYTHONWARNINGS PYTHONPYCACHEPREFIX PYTHONCASEOK PYTHONPLATLIBDIR \
  PYTHONUSERBASE PYTHONEXECUTABLE MAKEFLAGS MFLAGS GNUMAKEFLAGS MAKEOVERRIDES
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1

submission_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
paper_dir=$(CDPATH= cd -- "$submission_dir/.." && pwd)
project_root=$(CDPATH= cd -- "$paper_dir/../.." && pwd)
bootstrap_python=${BOOTSTRAP_PYTHON:-python3}
venv="$project_root/.venv-paper1"
safety="$submission_dir/verify_execution_safety.py"

if [ "${1-}" = "--negative-control" ] && [ "$#" -eq 1 ]; then
  exec "$bootstrap_python" -I "$safety" --intentional-failure
fi
if [ "$#" -ne 0 ]; then
  echo "Usage: bootstrap_replay.sh [--negative-control]" >&2
  exit 2
fi

"$bootstrap_python" -I "$safety" --runtime
"$bootstrap_python" -I -m venv --clear "$venv"

"$venv/bin/python" -I -m pip install \
  --disable-pip-version-check \
  --no-deps \
  --only-binary=:all: \
  --require-hashes \
  --requirement "$paper_dir/requirements-lock.txt"

"$venv/bin/python" -I "$safety" \
  --runtime --dependencies --audit-sources

PYTHON="$venv/bin/python" "$paper_dir/replay.sh"
