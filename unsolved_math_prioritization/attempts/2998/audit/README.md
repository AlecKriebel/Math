# Independent audit packet

Verdict: the frozen partial results pass mathematical review in the stated exact-locus, locally flat category. The original problem is not solved. Recommended status: **unsolved 5/5**. A nonblocking defect in the historical author verifier is documented and superseded by the strict release check below.

- `AUDIT.md`: authored proof review, source/category checks, limitations, five-approach disposition, and exact verifier finding.
- `AUDIT_BINDING.json`: exact original-author binding plus seven rejected integrity mutations.
- `binding_checks.py`: **controlling author release verifier**, pinned to the reviewed manifest; rejects unexpected nested manifests, symlinks, missing files, and altered bytes.
- `independent_controls.py`, `INDEPENDENT_CONTROL_RESULTS.json`: independently implemented exact controls and ten mathematical negative controls.
- `AUTHOR_REPLAY.json`: byte-identical replay of the author's controls in a temporary directory.
- `SOURCE_RETRIEVAL_CHECKS.json`: six fresh public PDF retrievals with hashes and sizes, all matching.
- `VERIFIER_HARDENING_CHECK.json`: exact nested-file case accepted by the historical verifier and rejected by the controlling checker.
- `AUDIT_SUMMARY.json`: machine-readable verdict and scope.
- `AUDIT_MANIFEST.json`, `verify_audit.py`: audit-payload binding and release verification.

From this audit directory:

    python verify_audit.py --author ../author
    python binding_checks.py --author ../author --negative-controls
    python independent_controls.py

These commands do not modify the original author files or the frozen audit files. The first verifies both packets' bytes; the remaining two replay integrity attacks on temporary copies and arithmetic controls. Standard-library Python suffices. Do not use Python's `-O` option, which disables assertions.

The original author verifier is preserved unchanged for historical reproducibility; its acceptance alone is not a release gate. The entire author directory must retain its nine exact reviewed files. If its location changes, pass the new directory using `--author`.

Only authored analysis/code and public verification metadata are distributed here. There are no source PDFs, source-text extracts, page images, raw dataset records, or private coordination material. Computation verifies finite bookkeeping, not topology or geometric realization.
