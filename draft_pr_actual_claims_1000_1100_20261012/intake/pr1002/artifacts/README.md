# Iwahori restriction: corrected partial analysis and audit

Read ACCEPTANCE.md, PARTIAL_ANALYSIS.md and AUDIT.md. The full problem remains
unresolved in this work; proof-search budget 5/5 is exhausted. The negative
independence example applies Prasad 1993 and carries no novelty claim.

This directory contains authored analysis, a public edition of the independent
audit and acceptance, contextual corrections, exact code, public bibliographic
metadata, and validation evidence. Source bodies, the full superseded original
report and archive, dataset contents, and the queue are excluded.

Authenticate BOOTSTRAP.py using the SHA-256 published outside this directory,
for example in the draft PR description. It pins the full publication manifest,
verifier and controls harness. The manifest binds every other delivered file,
including acceptance, references and preparation receipts. A substituted internal
manifest cannot replace that external trust anchor.

For portable verification, use a directory owned by UID 1000, with every file
mode 0444 and the directory mode 0555. Execute as UID=EUID=1000:

    python -I -S -B BOOTSTRAP.py .
    python -I -S -B -O BOOTSTRAP.py .
    python -I -S -B -OO BOOTSTRAP.py .

For integrity, schema, direct-comparator and hostile-environment negative controls:

    python -I -S -B BOOTSTRAP.py --controls .
    python -I -S -B -O BOOTSTRAP.py --controls .
    python -I -S -B -OO BOOTSTRAP.py --controls .

The verifier attempts actual append/create operations and requires EACCES.
Temporary mutation fixtures do not alter the delivered snapshot. Every fresh
complete stdout/stderr is compared byte-for-byte with its mode-specific pinned
reference, and parsed JSON types and values are compared recursively. Identical
checker outputs may legitimately have identical references across modes; the
semantic runner additionally records the actual optimization mode.

PREPARATION_CONTROLS files are explicitly historical pre-seal receipts. Their
recorded pins describe that earlier stage. Final sealing binds them, and the
final all-mode validation evidence is recorded and pinned outside this packet
to avoid circular self-hashes. CHECK_RUNS.json records full reference capture.

Original-report replay, original-archive replay, historical patch application,
source-body replay, dataset replay and formal proof-assistant verification are
NOT_RUN by the portable validator. Source metadata describes previous inspection.
