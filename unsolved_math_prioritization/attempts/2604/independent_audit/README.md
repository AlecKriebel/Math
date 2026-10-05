# Independent partial-results audit for Kourovka 21.95

Verdict: PASS at the frozen packet's limited scope. No mathematical correction was found. The original problem remains unresolved, 5/5 approaches; no novelty claim or complete solution is certified.

Read AUDIT_REPORT.md for the proof-by-proof review, literature limits, computational coverage, and optional presentation improvements. CORRECTIONS.json gives the machine-readable disposition. SOURCE_AUDIT.json records checked public source metadata without reproducing source content.

## Replay

Run `python3 verify_audit_manifest.py`, then `python3 independent_checks.py`. Both use only the Python standard library, are offline, and do not rewrite files. The second command independently regenerates AUDIT_CHECK_RESULTS.json and checks exact equality.

For comparison against an available frozen author packet, run `python3 independent_checks.py --author-dir /path/to/author/safe_output`. This reads CHECK_RESULTS.json only, checks all 183 original maps and compares the overlapping exact element-order histograms. It imports no author code. REPLAY_SUMMARY.json records that comparison from the audit.

The rebuild uses faithful permutation cycle orders instead of the author's matrix powers and affine norm sums, concrete binary linear algebra instead of merely substituting into a fixed-dimension formula, generated projective actions over prime and extension fields, and a second independently chosen set of 183 collision witnesses. Finite tests support the written proofs; they do not solve the overall existence question.

The author freeze is identified by SHA-256 `6d51c5e2467b119245a6b8ef2e1444f6ffb07decc0822522ea240106a6a02f91`. Frozen originals were not modified. This audit archive is independently manifested and contains no source PDFs, raw source text, datasets or private coordination files.
