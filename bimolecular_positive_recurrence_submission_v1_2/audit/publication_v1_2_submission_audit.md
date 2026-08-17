# Version 1.2 adversarial submission audit

**Audit date:** 16 August 2026
**Target:** Version 1.2 manuscript, verifier, PDFs, archive, and submission
metadata
**Outcome:** no theorem blocker found; release-hardening changes incorporated

## Mathematical replay

The following load-bearing interfaces were independently reconstructed from
the displayed argument rather than accepted from the test suite:

1. fixed-residual lifting of complex return paths and symmetry/closure of
   population accessibility under weak reversibility;
2. marked labelled-channel augmentation and irreducibility;
3. exact residual-factorial and source-entropy identities;
4. target-following episode recursion and scalar-envelope induction;
5. normalized-log subsequence extraction, including zero-weight divergent
   coordinates;
6. every molecularity-at-most-two top-complex branch and the signed-invariant
   obstruction;
7. finiteness and nonemptiness of the exceptional set;
8. stopped random-time Foster, finite trace, embedded-return, physical-time,
   nonexplosion, and regenerative-occupation interfaces; and
9. the exact Anderson--Cappelletti--Kim Example 4.1 comparison and the
   rate-degeneration example.

No circularity, invalid boundary branch, missing finiteness premise, or
computational dependence of the universal proof was found. Version 1.2 makes
three non-substantive hardening edits: it scopes the abstract closure claim
explicitly by weak reversibility, states `n >= 2` for the ACK display involving
`log(n-1)`, and spells out finiteness, normalization, and regeneration for the
stationary occupation formula.

## Independent computational stress

In addition to the packaged 57-test verifier, the audit exhaustively checked
1,687 small weakly reversible directed graphs, 149,058 enabled-edge return
witnesses, and 366,324 population transitions. It also checked 7,168 ACK
episode cases over 1,024 positive rate vectors. No counterexample was found.
These finite checks remain falsification aids, not proof of the theorem.

## Release and submission hardening

- The canonical PDF builder now requires Tectonic 0.16.9, an explicit bundle,
  deterministic mode, and a package-fixed epoch.
- The regular-wheel builder and its tests require byte-identical repeated
  output, canonical timestamps and modes, and the frozen wheel digest.
- A standard-library archive builder documents canonical membership,
  timestamp, permissions, ordering, and storage format and supports `--check`.
- A complete manifest covers every durable package file except its two
  byte-identical copies.
- A clean-checkout replay prints the actual commit/tag and toolchain, reruns
  all checks and builds, verifies every duplicate and archive byte, and
  requires no resulting package-tree change.
- The former Markdown-only reviewer appendices are represented by a polished,
  standalone PDF supplement.
- bioRxiv metadata is primary; arXiv metadata is clearly a mutually exclusive
  fallback. Applied Probability/JAP is recommended for later journal
  submission, with SPA-specific gaps recorded separately.

## Residual limits

No independent human expert review or journal/preprint screening has occurred.
bioRxiv may determine that a purely mathematical result is outside its scope
despite the direct stochastic-biochemical-model relevance. Submission-day
platform fields, licensing, policy text, and live preprint status must be
rechecked by the human author. A Zenodo DOI must not be cited until an actual
deposit is minted.
