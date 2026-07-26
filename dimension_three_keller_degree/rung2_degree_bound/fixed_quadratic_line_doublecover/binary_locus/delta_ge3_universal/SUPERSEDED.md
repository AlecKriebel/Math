# Superseded primary freeze

This directory is the primary atlas exactly as it was frozen at
2026-07-26T01:10:52Z.  It is retained as evidence of an independent
derivation, not as the canonical denominator.

The subsequent blinded reconstruction and line-by-line reconciliation
found:

1. two branch-square orbit-type splits, changing the stable-ID count from
   \(17+6+1\) to \(19+6+1\);
2. two missing guard factors in `D3-DN-L3`, which made its stated
   exact-\(\delta=3\) locus overlap an exact-\(\delta=4\) orbit; and
3. an invalid reciprocal quotient in `D3-SF-2C`, which omitted the genuine
   exact-\(\delta=3\) orbit at \(z=-1/5\).

Therefore `NOTE.md` and `denominator.json` in this directory must not be
used as the final classification.  The canonical ledger is
`../../audit_delta_ge3_denominator/DENOMINATOR.json`, and the complete
comparison is in `../../delta_ge3_reconciliation/RECONCILIATION.md`.

This warning was added after the primary freeze.  The files and hashes
listed in `FREEZE.json` remain unchanged.
