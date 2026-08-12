#!/bin/sh
set -eu

supplement_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$supplement_dir"

tectonic supplement.tex --keep-logs
if grep -Eiq 'warning:|invalid utf|undefined|overfull|underfull' supplement.log; then
    grep -Ein 'warning:|invalid utf|undefined|overfull|underfull' supplement.log >&2
    exit 1
fi
mv supplement.pdf kriebel-minimum-bell-setting-complexity-supplement-v1.2.0.pdf
printf '%s\n' 'Built warning-free Supplemental Material PDF.'
