#!/bin/sh
set -eu

pra_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$pra_dir"

./supplement/build.sh
cp supplement/kriebel-minimum-bell-setting-complexity-supplement-v1.2.0.pdf \
    supplemental_material.pdf
cp ../../artifacts/three_by_two_separation/bell_coefficients_dense.csv \
    supplemental_artifacts/
cp ../../artifacts/three_by_two_separation/bell_coefficients_sparse.csv \
    supplemental_artifacts/
cp ../../review_packet/theorem_to_artifact_map.md supplemental_artifacts/
cp ../../artifacts/SHA256SUMS.txt \
    supplemental_artifacts/MATHEMATICAL_ARTIFACT_SHA256SUMS.txt
cp ../../reports/verifier_report.txt supplemental_artifacts/
(
    cd supplemental_artifacts
    find . -type f ! -path './SHA256SUMS.txt' -print | LC_ALL=C sort |
        while IFS= read -r supplemental_file; do
            shasum -a 256 "$supplemental_file"
        done > SHA256SUMS.txt
)
rm -f supplemental_artifacts-v1.2.0.zip
COPYFILE_DISABLE=1 zip -X -q -r \
    supplemental_artifacts-v1.2.0.zip supplemental_artifacts
tectonic theorem_comparison.tex --keep-logs
if grep -Eiq 'warning:|invalid utf|undefined|overfull|underfull' theorem_comparison.log; then
    grep -Ein 'warning:|invalid utf|undefined|overfull|underfull' theorem_comparison.log >&2
    exit 1
fi
mv theorem_comparison.pdf kriebel-zcw-theorem-comparison-v1.2.0.pdf
printf '%s\n' 'Built warning-free PRA supplement, artifact archive, and internal theorem comparison.'
