#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$paper_dir"

if command -v tectonic >/dev/null 2>&1; then
    for source in main review; do
        tectonic "$source.tex" --keep-logs
        if grep -Eiq \
            'warning:|invalid utf|undefined (citation|reference|control sequence)|overfull|underfull' \
            "$source.log"; then
            printf '%s\n' "LaTeX warning found in $source.log:" >&2
            grep -Ein \
                'warning:|invalid utf|undefined (citation|reference|control sequence)|overfull|underfull' \
                "$source.log" >&2
            exit 1
        fi
    done
    printf '%s\n' 'Built warning-free main.pdf and review.pdf.'
    exit 0
fi

printf '%s\n' "Install Tectonic to build paper/main.pdf and paper/review.pdf." >&2
exit 1
