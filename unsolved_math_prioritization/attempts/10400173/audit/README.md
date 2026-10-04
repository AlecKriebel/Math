# Portable independent audit: rank 637

Verdict: **PASS WITH NONBLOCKING CORRECTIONS**; whole target remains **unsolved**, five approach families. See `AUDIT_REPORT.md` for the mathematical and source-boundary review.

The original 283 checks pass normally and with optimization. An independent integer-only seventh-cyclotomic Kirby-color implementation passes 81 runtime checks. Sokolov's 1997 primary paper was newly retrieved and visually inspected: it already separates the target pair for the full SU(2) TV theory. The historical and normalization implications are explained in the report.

## Reproduce with Python 3.8+

    python3 verify_audit.py
    python3 independent_verify.py > /tmp/rank637-independent.json
    diff -u INDEPENDENT_RESULTS.json /tmp/rank637-independent.json
    python3 -O independent_verify.py > /tmp/rank637-independent-optimized.json
    diff -u INDEPENDENT_RESULTS.json /tmp/rank637-independent-optimized.json

To recheck the separately supplied frozen author packet:

    python3 hardened_author_manifest.py /path/to/author-packet
    python3 /path/to/author-packet/verify.py > /tmp/rank637-author.json
    diff -u REPLAY_NORMAL.json /tmp/rank637-author.json

`REPLAY_NORMAL.json` and `REPLAY_OPTIMIZED.json` record successful author replays. `AUTHOR_BINDING_RECHECK.json` pins the exact reviewed version. `SOURCE_HASH_RECHECK.json` checks all ten original source PDF hashes without redistributing their bytes. `NEW_SOURCE_METADATA.json` records only public metadata for newly inspected papers. `PACKAGING_NEGATIVE_CONTROL.json` documents the nonblocking original allowlist weakness and its correction.

This package is dependency-free and requires no network. It preserves the author packet, contains no source PDFs, extracted text, datasets, or private coordination records, and makes no novelty or complete-resolution claim. Algebraic controls do not replace the cited category-realization and topology theorems.
