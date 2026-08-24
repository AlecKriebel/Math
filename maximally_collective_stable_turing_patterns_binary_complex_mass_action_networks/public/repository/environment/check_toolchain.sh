#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOCK_FILE="${TOOLCHAIN_LOCK_FILE:-$ROOT/environment/texlive-2022.04.lock.txt}"
QUIET=0
if [[ "${1:-}" == "--quiet" ]]; then QUIET=1; fi

for command_name in python pdflatex biber kpsewhich mktemp grep; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'TOOLCHAIN_FAIL missing command: %s\n' "$command_name" >&2
    exit 2
  fi
done

python - "$ROOT/requirements-tested.txt" <<'PY'
import importlib
import platform
import sys
from pathlib import Path

if sys.flags.optimize:
    raise SystemExit("TOOLCHAIN_FAIL Python assertions are disabled")
if platform.python_version() != "3.9.6":
    raise SystemExit(
        f"TOOLCHAIN_FAIL CPython 3.9.6 required; found {platform.python_version()}"
    )
expected = {}
for raw in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    line = raw.strip()
    if not line or line.startswith("#"):
        continue
    name, version = line.split("==", 1)
    expected[name] = version
for name, version in expected.items():
    actual = importlib.import_module(name).__version__
    if actual != version:
        raise SystemExit(
            f"TOOLCHAIN_FAIL {name}=={version} required; found {actual}"
        )
PY

lock_value() {
  local name="$1"
  awk -F'|' -v target="$name" '$1 == target {print substr($0, index($0, "|") + 1)}' "$LOCK_FILE"
}
for required_lock in ENGINE FORMAT LATEX BIBER; do
  [[ -n "$(lock_value "$required_lock")" ]] || {
    printf 'TOOLCHAIN_FAIL missing special lock field: %s\n' "$required_lock" >&2
    exit 2
  }
done

pdflatex_banner="$(pdflatex --version | head -n 1)"
engine_expected="$(lock_value ENGINE)"
case "$pdflatex_banner" in
  *"$engine_expected"*) ;;
  *) printf 'TOOLCHAIN_FAIL unexpected pdfLaTeX: expected %s; found %s\n' \
       "$engine_expected" "$pdflatex_banner" >&2; exit 2 ;;
esac
biber_banner="$(biber --version | head -n 1)"
biber_expected="$(lock_value BIBER)"
case "$biber_banner" in
  *"$biber_expected"*) ;;
  *) printf 'TOOLCHAIN_FAIL unexpected Biber: expected %s; found %s\n' \
       "$biber_expected" "$biber_banner" >&2; exit 2 ;;
esac

probe_root="$(mktemp -d "${TMPDIR:-/tmp}/exact-diffusion-toolchain.XXXXXX")"
trap 'rm -rf "$probe_root"' EXIT
cat > "$probe_root/packages.tex" <<'EOF'
\listfiles
\documentclass{article}
\usepackage{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb,amsthm,mathtools}
\usepackage{booktabs,longtable,array,enumitem,microtype,graphicx,float}
\usepackage[mathlines]{lineno}
\usepackage{tikz}
\usepackage[hidelinks]{hyperref}
\usepackage[nameinlink,capitalise]{cleveref}
\usepackage[backend=biber,style=numeric]{biblatex}
\begin{document}release toolchain probe\end{document}
EOF
cat > "$probe_root/standalone_probe.tex" <<'EOF'
\listfiles
\documentclass[tikz,border=5pt]{standalone}
\usepackage{amsmath}
\begin{document}\begin{tikzpicture}\node {probe};\end{tikzpicture}\end{document}
EOF
(cd "$probe_root" && pdflatex -interaction=nonstopmode -halt-on-error packages.tex >/dev/null)
(cd "$probe_root" && pdflatex -interaction=nonstopmode -halt-on-error standalone_probe.tex >/dev/null)

while IFS='|' read -r lock_name expected; do
  case "$lock_name" in ''|'#'*) continue ;; ENGINE|BIBER) continue ;; esac
  if ! grep -Fq "$expected" "$probe_root/packages.log" \
      && ! grep -Fq "$expected" "$probe_root/standalone_probe.log"; then
    printf 'TOOLCHAIN_FAIL package lock mismatch: %s | %s\n' "$lock_name" "$expected" >&2
    exit 2
  fi
done < "$LOCK_FILE"

if ((QUIET == 0)); then
  printf '%s\n' 'TOOLCHAIN_LOCK_PASS'
  printf 'PYTHON=%s\n' "$(python -c 'import platform; print(platform.python_version())')"
  printf 'PDFLATEX=%s\n' "$pdflatex_banner"
  printf 'BIBER=%s\n' "$biber_banner"
fi
