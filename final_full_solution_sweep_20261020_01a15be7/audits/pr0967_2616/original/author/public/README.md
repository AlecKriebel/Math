# Countable expansive-block counterexample

`REPORT.md` contains a self-contained negative-answer proof candidate for KOU-21.107. The countable Boolean group carries the standard Mathias/free Boolean linear topology associated to an arbitrary free ultrafilter. An explicit countable dense partition and the finite-block obstruction are proved in full. Independent mathematical audit is pending; priority and publication acceptance are not claimed.

`sources.json` and `provenance.json` contain public verification metadata only. Source PDFs, source text, question records, dataset contents, and private coordination material are excluded.

Python 3.10+ and the standard library suffice:

    python3 -I -B verify.py fixtures.json
    python3 -I -B -O verify.py fixtures.json
    python3 -I -B -OO verify.py fixtures.json

The checker writes JSON to stdout and rejects invalid input with a nonzero exit code. It tests exact finite combinatorial identities, not the infinite theorem or a free ultrafilter. It also accepts `--stdin` for already-authenticated fixture bytes.

For snapshot-integrity, hostile-input and genuine nonroot read-only controls, authenticate the separate external manifest and tools against independently supplied SHA-256 pins and follow `AUDIT_INSTRUCTIONS.md`. The public manifest covers every file in this directory. The external bootstrap executes verified snapshots of the checker and input, without reading them a second time.

No files or repositories are modified by the verifier. The external test harness uses disposable temporary copies only.
