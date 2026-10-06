# Connected sum ropelength audit

Problem ID 2733, KP-1.74, rank 907. Assessment date: 2026-10-06.

**Outcome: partial formulation audit; intended problem unresolved.** The constant
4π−4 cannot hold when an unknot summand is permitted, under the stated
radius/reach normalization. This is a missing-scope issue, not a resolution of
the intended connected-sum conjecture for nontrivial summands. No proof or
counterexample for the intended version of part (a), or for part (b), is claimed.

- `PROOF.md`: exact unknot calculation, split-link cancellation, and the
  quantitative condition a thickness-losing splice must satisfy.
- `REPORT.md`: source reconciliation, interpretation, and the unresolved gap.
- `APPROACH_LOG.md`: two bounded approaches and their stopping reason.
- `STATUS.json`: machine-readable scope and outcome.
- `SOURCE_AUDIT.json`: public source identifiers, inspection history, hashes,
  and bounded repository-search results.
- `ARITHMETIC_CERTIFICATE.json`: exact symbolic arithmetic inputs.
- `verify.py`: integrity and arithmetic checks; these are not a formal
  verification of geometric or topological theorems.
- `MANIFEST.json`: hashes and byte counts of all other package members.

Run `python3 verify.py` or `python3 -O verify.py` from this directory. Both modes
enforce the same explicit checks. Unexpected, missing, modified, symlinked,
or malformed members cause failure. An external manifest binds this package
to a particular ZIP hash. No source PDFs, extracts, datasets, or private
coordination records are included.
