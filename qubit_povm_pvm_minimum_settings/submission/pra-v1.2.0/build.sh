#!/bin/sh
set -eu

pra_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$pra_dir"

./supplement/build.sh
tectonic theorem_comparison.tex --keep-logs
if grep -Eiq 'warning:|invalid utf|undefined|overfull|underfull' theorem_comparison.log; then
    grep -Ein 'warning:|invalid utf|undefined|overfull|underfull' theorem_comparison.log >&2
    exit 1
fi
mv theorem_comparison.pdf kriebel-zcw-theorem-comparison-v1.2.0.pdf
printf '%s\n' 'Built warning-free PRA supplement and theorem comparison.'
