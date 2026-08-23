#!/bin/sh
set -eu

if [ "${PYTHON+x}" = x ]; then
  echo "PYTHON overrides are forbidden for the Paper I bootstrap stage" >&2
  exit 2
fi
case ${PYTHONOPTIMIZE-} in
  ""|0) ;;
  *)
    echo "Refusing inherited PYTHONOPTIMIZE=${PYTHONOPTIMIZE}" >&2
    exit 2
    ;;
esac
unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME PYTHONSTARTUP PYTHONINSPECT \
  PYTHONWARNINGS PYTHONPYCACHEPREFIX PYTHONCASEOK PYTHONPLATLIBDIR \
  PYTHONUSERBASE PYTHONEXECUTABLE PYTHON MAKEFLAGS MFLAGS GNUMAKEFLAGS \
  MAKEOVERRIDES
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1

submission_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
paper_dir=$(CDPATH= cd -- "$submission_dir/.." && pwd)
project_root=$(CDPATH= cd -- "$paper_dir/../.." && pwd)
bundle_root=$(CDPATH= cd -- "$project_root/.." && pwd)
bootstrap_python=${BOOTSTRAP_PYTHON:-python3}
safety="$submission_dir/verify_execution_safety.py"

if [ "${1-}" = "--negative-control" ] && [ "$#" -eq 1 ]; then
  exec "$bootstrap_python" -I "$safety" --intentional-failure
fi
if [ "$#" -ne 1 ]; then
  echo "Usage: bootstrap_replay.sh {--certified-package-stage|--development|--negative-control}" >&2
  exit 2
fi
mode=$1
case "$mode" in
  --certified-package-stage|--development) ;;
  *)
    echo "Usage: bootstrap_replay.sh {--certified-package-stage|--development|--negative-control}" >&2
    exit 2
    ;;
esac

if [ "$mode" = "--certified-package-stage" ]; then
  "$bootstrap_python" -I "$safety" \
    --runtime --bundle-root "$bundle_root" --audit-sources
else
  "$bootstrap_python" -I "$safety" --runtime
  echo "NOTICE: development bootstrap; only the enclosing package launcher is certified"
fi

tmp_base=${TMPDIR:-/tmp}
tmp_base=${tmp_base%/}
runtime_dir=$(mktemp -d "$tmp_base/paper1-runtime.XXXXXX")
case "$runtime_dir" in
  "$tmp_base"/paper1-runtime.*) ;;
  *)
    echo "Unexpected Paper I runtime directory: $runtime_dir" >&2
    exit 2
    ;;
esac
chmod 700 "$runtime_dir"
cleanup() {
  case "$runtime_dir" in
    "$tmp_base"/paper1-runtime.*) rm -rf -- "$runtime_dir" ;;
    *) echo "Refusing to remove unexpected runtime directory: $runtime_dir" >&2 ;;
  esac
}
trap cleanup EXIT HUP INT TERM
venv="$runtime_dir/venv"
cache="$runtime_dir/pycache"
setup_cache="$runtime_dir/setup-pycache"
mkdir -m 700 "$setup_cache"

"$bootstrap_python" -I -B -X "pycache_prefix=$setup_cache" -m venv "$venv"

"$venv/bin/python" -I -B -X "pycache_prefix=$setup_cache" -m pip install \
  --disable-pip-version-check \
  --no-deps \
  --only-binary=:all: \
  --require-hashes \
  --requirement "$paper_dir/requirements-lock.txt"

mkdir -m 700 "$cache"
if [ "$mode" = "--certified-package-stage" ]; then
  "$venv/bin/python" -I -B -X "pycache_prefix=$cache" "$safety" \
    --runtime --dependencies --bundle-root "$bundle_root" --audit-sources \
    --expected-cache-prefix "$cache"
else
  "$venv/bin/python" -I -B -X "pycache_prefix=$cache" "$safety" \
    --runtime --dependencies --audit-sources --expected-cache-prefix "$cache"
fi

"$paper_dir/replay.sh" --internal-from-bootstrap "$runtime_dir"
