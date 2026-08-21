#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$ROOT/run}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
read -r COMPILER CANONICALIZER < <("$PYTHON_BIN" - "$ROOT" <<'PY'
import hashlib, importlib.util, inspect, pathlib, sys
root=pathlib.Path(sys.argv[1]); p=root/'atlas'/'k2p_atlas_core.py'
spec=importlib.util.spec_from_file_location('k2p_atlas_core',p); m=importlib.util.module_from_spec(spec);sys.modules['k2p_atlas_core']=m;spec.loader.exec_module(m)
compiler=hashlib.sha256(p.read_bytes()).hexdigest()
src='\n'.join(inspect.getsource(getattr(m,n)) for n in ('mixed_incidence_graph','mixed_exact_isomorphic','mixed_relation_exact'))
canon=hashlib.sha256(src.encode()).hexdigest()
print(compiler,canon)
PY
)
mkdir -p "$OUT/logs"
for source in 0 1 2 3 4 5; do
  echo "Starting source $source" >&2
  "$PYTHON_BIN" "$ROOT/resumable_four_port_driver.py" \
    --package-root "$ROOT" \
    --source-index "$source" \
    --output-root "$OUT" \
    --expected-compiler-sha256 "$COMPILER" \
    --expected-canonicalizer-sha256 "$CANONICALIZER" \
    2>&1 | tee "$OUT/logs/source_${source}.log"
done
"$PYTHON_BIN" "$ROOT/merge_manifests.py" --run-root "$OUT"
