#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
checker="$here/verify_coverage.py"
scratch=$(mktemp -d "${TMPDIR:-/tmp}/vertical-coverage.XXXXXX")
trap 'rm -rf "$scratch"' EXIT HUP INT TERM

/usr/bin/python3 "$checker" >"$scratch/normal.log" 2>&1
cat "$scratch/normal.log"
if ! tail -n 1 "$scratch/normal.log" |
    grep -Fqx 'TRIPLE_VERTICAL_COVERAGE_PASS_4E7B19'
then
    echo "FAIL: coverage sentinel missing" >&2
    exit 1
fi

for mutation in drop_a0_w0_nonzero overlap_nonvertical
do
    if VERTICAL_COVERAGE_MUTATION="$mutation" \
        /usr/bin/python3 "$checker" >"$scratch/$mutation.log" 2>&1
    then
        echo "FAIL: coverage mutation escaped: $mutation" >&2
        exit 1
    fi
    grep -Fq 'FAIL:' "$scratch/$mutation.log"
done

if /usr/bin/python3 -O "$checker" >"$scratch/optimized.log" 2>&1
then
    echo "FAIL: optimized Python escaped" >&2
    exit 1
fi
grep -Fq 'refusing optimized Python' "$scratch/optimized.log"

echo 'TRIPLE_VERTICAL_COVERAGE_STRICT_PASS_85C2D0'
