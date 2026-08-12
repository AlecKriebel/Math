#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$project_dir"

find . -type f \
    ! -path './SHA256SUMS.txt' \
    ! -path './tmp/*' \
    ! -path './submission/zenodo-v1.1.0/*' \
    ! -path './submission/zenodo-v1.2.0/*' \
    ! -path './submission/arxiv_source.tar.gz' \
    ! -path './submission/pra-v1.2.0/*.pdf' \
    ! -path './submission/pra-v1.2.0/*.zip' \
    ! -path './submission/pra-v1.2.0/*.tar.gz' \
    ! -path './submission/pra-v1.2.0/SHA256SUMS.txt' \
    ! -path './submission/pra-v1.2.0/supplement/*.pdf' \
    ! -name '*.aux' \
    ! -name '*.bbl' \
    ! -name '*.blg' \
    ! -name '*.log' \
    ! -name '*.out' \
    ! -name '*.synctex.gz' \
    ! -name '.DS_Store' \
    -print | LC_ALL=C sort |
while IFS= read -r release_file; do
    shasum -a 256 "$release_file"
done > SHA256SUMS.txt

printf '%s\n' 'Regenerated the core source/prose SHA-256 manifest.'
