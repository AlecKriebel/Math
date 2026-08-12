#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$paper_dir"

if command -v tectonic >/dev/null 2>&1; then
    for source in main review; do
        tectonic "$source.tex" --keep-logs --keep-intermediates
        if grep -Eiq \
            'warning:|invalid utf|undefined (citation|reference|control sequence)|overfull|underfull' \
            "$source.log"; then
            printf '%s\n' "LaTeX warning found in $source.log:" >&2
            grep -Ein \
                'warning:|invalid utf|undefined (citation|reference|control sequence)|overfull|underfull' \
                "$source.log" >&2
            exit 1
        fi
        if grep -Eiq 'warning--|there (was|were) [1-9][0-9]* warning' \
            "$source.blg"; then
            printf '%s\n' "BibTeX warning found in $source.blg:" >&2
            cat "$source.blg" >&2
            exit 1
        fi
    done
    # The current APS bibliography is shipped as a generated .bbl so the
    # reproducible PDF build does not invoke BibTeX's known REVTeX control-file
    # warning. Regenerate pra.bbl explicitly whenever citations change.
    rm -f pra.blg praNotes.bib
    tectonic \
        -Z search-path=vendor/revtex-4.2f/tex/latex/revtex \
        -Z search-path=vendor/revtex-4.2f/bibtex/bst/revtex \
        pra.tex --keep-logs --keep-intermediates
    if grep -Eiq \
        'warning:|invalid utf|undefined (citation|reference|control sequence)|overfull|underfull|stuck' \
        pra.log; then
        printf '%s\n' 'LaTeX warning found in pra.log:' >&2
        grep -Ein \
            'warning:|invalid utf|undefined (citation|reference|control sequence)|overfull|underfull|stuck' \
            pra.log >&2
        exit 1
    fi
    if test -f pra.blg && grep -Eiq 'warning--|there (was|were) [1-9][0-9]* warning' pra.blg; then
        printf '%s\n' 'BibTeX warning found in pra.blg:' >&2
        cat pra.blg >&2
        exit 1
    fi
    printf '%s\n' 'Built warning-free main.pdf, review.pdf, and one-column PRA PDF.'
    exit 0
fi

printf '%s\n' "Install Tectonic to build paper/main.pdf, paper/review.pdf, and paper/pra.pdf." >&2
exit 1
