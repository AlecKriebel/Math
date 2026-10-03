# Release changes from the independently audited frozen package

Prepared 2026-10-03 UTC. Mathematical status is unchanged: UNSOLVED, 5/5.
These are documentation, audit packaging, and explicit check clarifications;
no sixth mathematical attempt has been undertaken.

## Three nonblocking audit recommendations

1. ATTEMPT_5.md: added the exact Haettel–Huang Theorem 5.7 citation and the
   identification chain through the proof of Corollary 4.5 to this particular Q.
2. ATTEMPT_2.md: added v=3k for a^u z^k, the explicit intrinsic expression,
   infimum/supremum normalization, and Lee–Lee Section 4 as the length-formula
   source. The statement remains intrinsic and motivational, not an ambient
   metric theorem or a coarse-Helly obstruction.
3. verify_local_obstruction.py: added direct assertions that the a^n and p^n
   images differ and that the full triple image intersection is empty, n=1,2,3.
   The existing output schema and certificate values are unchanged.

## Packaging and sanitization

- Added audit/REPORT.md with the full mathematical audit, independent controls,
  all scope cautions, and all recommendations. Nonpublic history-search
  bookkeeping was omitted; no mathematical conclusion was removed.
- Added audit/independent_controls.py and audit/independent_controls.json
  byte-for-byte from the audit. Added the original author's frozen manifest.
- SOURCE_GATE.md: omitted nonpublic history-search bookkeeping; retained exact
  original-source evidence, repository-search limits, hashes, and caveats.
- README.md: added the audit/release map and accurately distinguished the
  audited original from this clarified release awaiting narrow review.
- No source PDFs/HTML, source extracts, bulk corpus records, or private
  conversation records are included.
- ATTEMPT_1.md, ATTEMPT_3.md, ATTEMPT_4.md and checks_turn2.json are unchanged.

## Validation

Both verifiers were rerun successfully with Python 3. The author output is
structurally identical to checks_turn2.json; the independent output is
structurally identical to audit/independent_controls.json. The frozen original
nine-file package still matches every hash in its original manifest.

The release is held for a narrow independent review and the separate
publication gate. No remote writes were performed while preparing it.
