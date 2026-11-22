#!/bin/sh
# Build both manuscript PDFs. Use --submission to also refresh the source tarball.
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
case "${1:-}" in
    '') package=no ;;
    --submission) package=yes ;;
    *) echo "Usage: $0 [--submission]" >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then
    echo "Usage: $0 [--submission]" >&2
    exit 2
fi
if ! command -v tectonic >/dev/null 2>&1; then
    echo 'Install Tectonic to build the manuscript PDFs.' >&2
    exit 1
fi

# Resolve a local TeX resource bundle before changing to the fresh source tree.
set --
if [ -n "${TECTONIC_BUNDLE:-}" ]; then
    case "$TECTONIC_BUNDLE" in
        /*|*://*) set -- --bundle "$TECTONIC_BUNDLE" ;;
        *) set -- --bundle "$(pwd)/$TECTONIC_BUNDLE" ;;
    esac
fi

build_dir=$(mktemp -d "${TMPDIR:-/tmp}/qubit-paper.XXXXXXXX")
trap 'rm -rf "$build_dir"' EXIT
mkdir "$build_dir/figures"
cp "$paper_dir/main.tex" "$paper_dir/appendices.tex" "$paper_dir/references.bib" \
    "$paper_dir/review.tex" "$paper_dir/lineno.sty" "$build_dir/"
cp "$paper_dir"/figures/*.tex "$build_dir/figures/"
cd "$build_dir"

for source in main review; do
    tectonic "$@" --keep-logs --keep-intermediates "$source.tex"
    if grep -Eiq 'warning:|invalid utf|undefined (citation|reference|control sequence)|overfull|underfull' "$source.log" ||
       grep -Eiq 'warning--|error message' "$source.blg"; then
        echo "TeX or BibTeX warnings in $source:" >&2
        grep -Ein 'warning:|warning--|error message|invalid utf|undefined (citation|reference|control sequence)|overfull|underfull' "$source.log" "$source.blg" >&2
        exit 1
    fi
done

if [ "$package" = yes ]; then
    python3 - <<'PY'
import gzip
from pathlib import Path
import tarfile

members = [Path(name) for name in ("main.tex", "appendices.tex", "references.bib", "main.bbl")]
members.extend(sorted(Path("figures").glob("*.tex")))
with open("arxiv_source.tar.gz", "wb") as output:
    with gzip.GzipFile(filename="", fileobj=output, mode="wb", mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w", format=tarfile.USTAR_FORMAT) as archive:
            for path in members:
                member = tarfile.TarInfo(path.as_posix())
                member.size = path.stat().st_size
                member.mode = 0o644
                with path.open("rb") as source:
                    archive.addfile(member, source)
PY
    mv arxiv_source.tar.gz "$paper_dir/../submission/"
fi

for source in main review; do
    mv "$source.pdf" "$source.log" "$source.blg" "$paper_dir/"
done
echo 'Built warning-free main.pdf and review.pdf.'
