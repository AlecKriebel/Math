#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
zenodo_dir="$project_dir/submission/zenodo-v1.2.0"
pra_dir="$project_dir/submission/pra-v1.2.0"
website_dir="$project_dir/submission/website-v1.2.0-draft"
release_version=1.2.0

standard_pdf="$zenodo_dir/publication/kriebel-2026-minimum-bell-setting-complexity-v${release_version}.pdf"
review_pdf="$zenodo_dir/publication/kriebel-2026-minimum-bell-setting-complexity-review-v${release_version}.pdf"
source_archive="$zenodo_dir/publication/kriebel-2026-minimum-bell-setting-complexity-source-v${release_version}.tar.gz"
publication_manifest="$zenodo_dir/publication/kriebel-2026-minimum-bell-setting-complexity-SHA256SUMS-v${release_version}.txt"
software_archive="$zenodo_dir/software/kriebel-qubit-povm-pvm-reproducibility-v${release_version}.zip"

"$project_dir/paper/build.sh"
"$pra_dir/build.sh"

test -f "$project_dir/paper/main.pdf"
test -f "$project_dir/paper/review.pdf"
test -f "$project_dir/paper/pra.pdf"
test -f "$project_dir/paper/main.bbl"
test -f "$project_dir/reports/verifier_report.txt"
test -d "$project_dir/submission/zenodo-v1.1.0"

cp "$project_dir/paper/main.pdf" "$website_dir/paper.pdf"
cp "$project_dir/paper/review.pdf" "$website_dir/review.pdf"
(
    cd "$website_dir"
    shasum -a 256 paper.pdf review.pdf > SHA256SUMS.txt
)

"$project_dir/submission/generate_core_manifest.sh"

mkdir -p "$zenodo_dir/publication" "$zenodo_dir/software"
mkdir -p "$pra_dir/source"

cp "$project_dir/paper/main.pdf" "$standard_pdf"
cp "$project_dir/paper/review.pdf" "$review_pdf"
cp "$project_dir/CITATION.cff" "$zenodo_dir/CITATION.cff"
cp "$project_dir/CHANGELOG.md" "$zenodo_dir/CHANGELOG.md"
cp "$project_dir/reports/verifier_report.txt" "$zenodo_dir/VERIFICATION_REPORT.txt"

build_tmp=$(mktemp -d "${TMPDIR:-/tmp}/qubit-povm-pvm-v120.XXXXXX")
trap 'rm -rf "$build_tmp"' EXIT HUP INT TERM

source_top="kriebel-minimum-bell-setting-complexity-source-v${release_version}"
source_root="$build_tmp/$source_top"
mkdir -p "$source_root/figures"
for source_file in main.tex abstract.tex appendices.tex references.bib main.bbl pra.bbl review.tex pra.tex lineno.sty build.sh SOURCE_README.md; do
    cp "$project_dir/paper/$source_file" "$source_root/$source_file"
done
for figure_file in five_ray_circuit.tex rank_trichotomy.tex threshold.tex; do
    cp "$project_dir/paper/figures/$figure_file" "$source_root/figures/$figure_file"
done
cp "$project_dir/LICENSE" "$source_root/LICENSE"
mkdir -p "$source_root/vendor/revtex-4.2f/tex/latex" \
    "$source_root/vendor/revtex-4.2f/bibtex/bst" \
    "$source_root/vendor/revtex-4.2f/doc/latex/revtex"
cp -R "$project_dir/paper/vendor/revtex-4.2f/tex/latex/revtex" \
    "$source_root/vendor/revtex-4.2f/tex/latex/"
cp -R "$project_dir/paper/vendor/revtex-4.2f/bibtex/bst/revtex" \
    "$source_root/vendor/revtex-4.2f/bibtex/bst/"
cp "$project_dir/paper/vendor/revtex-4.2f/NOTICE.md" \
    "$source_root/vendor/revtex-4.2f/NOTICE.md"
cp "$project_dir/paper/vendor/revtex-4.2f/doc/latex/revtex/README" \
    "$source_root/vendor/revtex-4.2f/doc/latex/revtex/README"

COPYFILE_DISABLE=1 tar -czf "$source_archive" -C "$build_tmp" "$source_top"
COPYFILE_DISABLE=1 tar -czf "$project_dir/submission/arxiv_source.tar.gz" -C "$source_root" .
cp "$source_archive" "$pra_dir/kriebel-minimum-bell-setting-complexity-source-v${release_version}.tar.gz"

software_top="qubit-povm-pvm-minimum-settings-v${release_version}"
software_root="$build_tmp/$software_top"
mkdir -p "$software_root/paper"
for root_file in LICENSE RESEARCH_LOG.md VERSION.txt CHANGELOG.md CORRECTIONS.md AI_PROVENANCE.md .python-version requirements.txt run_all.sh; do
    cp "$project_dir/$root_file" "$software_root/$root_file"
done
cp "$zenodo_dir/metadata/SOFTWARE_ARCHIVE_README.md" "$software_root/README.md"
cp "$zenodo_dir/metadata/SOFTWARE_ARCHIVE_CITATION.cff" "$software_root/CITATION.cff"
cp -R "$project_dir/artifacts" "$software_root/artifacts"
cp -R "$project_dir/reports" "$software_root/reports"
cp -R "$project_dir/review_packet" "$software_root/review_packet"
mkdir -p "$software_root/paper/figures"
for paper_file in main.pdf review.pdf pra.pdf main.tex abstract.tex appendices.tex references.bib main.bbl pra.bbl review.tex pra.tex lineno.sty build.sh SOURCE_README.md; do
    cp "$project_dir/paper/$paper_file" "$software_root/paper/$paper_file"
done
for figure_file in five_ray_circuit.tex rank_trichotomy.tex threshold.tex; do
    cp "$project_dir/paper/figures/$figure_file" "$software_root/paper/figures/$figure_file"
done
mkdir -p "$software_root/paper/vendor/revtex-4.2f/tex/latex" \
    "$software_root/paper/vendor/revtex-4.2f/bibtex/bst" \
    "$software_root/paper/vendor/revtex-4.2f/doc/latex/revtex"
cp -R "$project_dir/paper/vendor/revtex-4.2f/tex/latex/revtex" \
    "$software_root/paper/vendor/revtex-4.2f/tex/latex/"
cp -R "$project_dir/paper/vendor/revtex-4.2f/bibtex/bst/revtex" \
    "$software_root/paper/vendor/revtex-4.2f/bibtex/bst/"
cp "$project_dir/paper/vendor/revtex-4.2f/NOTICE.md" \
    "$software_root/paper/vendor/revtex-4.2f/NOTICE.md"
cp "$project_dir/paper/vendor/revtex-4.2f/doc/latex/revtex/README" \
    "$software_root/paper/vendor/revtex-4.2f/doc/latex/revtex/README"
(
    cd "$software_root"
    find . -type f ! -path './SHA256SUMS.txt' -print | LC_ALL=C sort |
        while IFS= read -r release_file; do
            shasum -a 256 "$release_file"
        done > SHA256SUMS.txt
)
(
    cd "$build_tmp"
    COPYFILE_DISABLE=1 zip -X -q -r "$software_archive" "$software_top"
)

verifier_top="kriebel-qubit-povm-pvm-verifier-v${release_version}"
verifier_root="$build_tmp/$verifier_top"
mkdir -p "$verifier_root"
for root_file in LICENSE VERSION.txt AI_PROVENANCE.md .python-version requirements.txt run_all.sh; do
    cp "$project_dir/$root_file" "$verifier_root/$root_file"
done
cp "$pra_dir/verifier_README.md" "$verifier_root/README.md"
cp "$zenodo_dir/metadata/SOFTWARE_ARCHIVE_CITATION.cff" "$verifier_root/CITATION.cff"
cp -R "$project_dir/artifacts" "$verifier_root/artifacts"
cp "$project_dir/review_packet/theorem_to_artifact_map.md" "$verifier_root/theorem_to_artifact_map.md"
cp "$project_dir/reports/verifier_report.txt" "$verifier_root/verifier_report.txt"
(
    cd "$verifier_root"
    find . -type f ! -path './SHA256SUMS.txt' -print | LC_ALL=C sort |
        while IFS= read -r release_file; do
            shasum -a 256 "$release_file"
        done > SHA256SUMS.txt
)
(
    cd "$build_tmp"
    COPYFILE_DISABLE=1 zip -X -q -r \
        "$pra_dir/kriebel-minimum-bell-setting-complexity-verifier-v${release_version}.zip" \
        "$verifier_top"
)

cp "$project_dir/paper/pra.pdf" \
    "$pra_dir/kriebel-minimum-bell-setting-complexity-pra-v${release_version}.pdf"
cp "$project_dir/paper/review.pdf" \
    "$pra_dir/kriebel-minimum-bell-setting-complexity-review-v${release_version}.pdf"

(
    cd "$zenodo_dir/publication"
    for release_file in \
        "$(basename "$standard_pdf")" \
        "$(basename "$review_pdf")" \
        "$(basename "$source_archive")"; do
        shasum -a 256 "$release_file"
    done > "$(basename "$publication_manifest")"
)

(
    cd "$zenodo_dir"
    find . -type f ! -path './SHA256SUMS.txt' -print | LC_ALL=C sort |
        while IFS= read -r release_file; do
            shasum -a 256 "$release_file"
        done > SHA256SUMS.txt
)

(
    cd "$pra_dir"
    find . -type f \
        ! -path './SHA256SUMS.txt' \
        ! -name '*.aux' \
        ! -name '*.blg' \
        ! -name '*.log' \
        ! -name '*.out' \
        ! -name '*.synctex.gz' \
        -print | LC_ALL=C sort |
        while IFS= read -r release_file; do
            shasum -a 256 "$release_file"
    done > SHA256SUMS.txt
)

# The core manifest includes all public source/prose metadata, including the
# PRA manifest above, so it must be generated last.
"$project_dir/submission/generate_core_manifest.sh"

printf '%s\n' 'Built whitelisted v1.2.0 Zenodo, arXiv, and PRA archives.'
