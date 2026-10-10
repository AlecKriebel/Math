# 30001599: uniform fat-point alpha bounds

**Unsolved, 5/5 substantive approaches used.** This draft publishes scoped rigorous partials and an independent adversarial AI audit. It does not resolve the arbitrary-support inequality, establish novelty, certify worldwide openness, or constitute human peer review.

For a nonempty finite reduced set X in projective n-space, write I=I(X), a=alpha(I), and m=n(r-1)+1. The target is alpha(I^(m)) >= r*a+(r-1)(n-1), for every integer r>=1. The OWR contribution does not state a field assumption. The differential, star-family and polar arguments here work over an algebraically closed field of characteristic zero; no arbitrary-characteristic extrapolation is intended.

## Accepted partial results

- A sharp equality proof for hyperplane point-star configurations in every projective dimension within the stated characteristic-zero scope. This recovers a known family.
- In the plane, any counterexample witness for r>=3 must have a repeated irreducible factor. This is a necessary condition, not a counterexample or a proof of the target.
- Two rational six-point supports have the same entire reduced Hilbert function but different symbolic initial degrees: their (alpha(I), alpha(I^(3)), alpha(I^(5))) triples are (3,7,11) and (3,8,12).
- Exact differentiation deficits and conditional Waldschmidt thresholds identify why those approaches fall short.

The unresolved obstruction is how repeated irreducible components contribute weighted, nonuniform point multiplicities. Removing one component does not preserve a uniform instance suitable for induction.

The Cooper–Hartke all-r update is restricted to line-count types (c_1,...,c_t) in nondecreasing order with c_i>=i, with no support point at an intersection of two supporting lines. It is not an arbitrary-support result or a consequence of the reduced Hilbert function alone.

## Evidence and preserved snapshots

- [Authored proofs](fat_points_30001599/safe/PROOFS.md)
- [Five-approach log](fat_points_30001599/safe/APPROACH_LOG.md)
- [Independent audit and exact limitations](fat_points_30001599_independent_audit/safe/AUDIT.md)
- [Audit binding](fat_points_30001599_independent_audit/safe/BINDING.json)
- [Source verification](fat_points_30001599/safe/SOURCE_VERIFICATION.json) and [independent source audit](fat_points_30001599_independent_audit/safe/SOURCE_AUDIT.json)

Both eight-file author and six-file audit snapshots are preserved byte for byte. Statements such as “audit required” and “no remote writes” inside them describe their freeze-stage state; the later audit verdict is PASS as unsolved 5/5 with scoped partials. The author archive contains only those eight safe files. Source PDFs, extracts, screenshots, raw datasets and private coordination records are excluded.

The audit independently checks eight rational ranks, 24 modular ranks, upper witnesses, nine higher-dimensional star controls and 18 rejected negative controls. Finite computations are diagnostics; universal claims rely on the written proofs. The raw datasets, catalog statement hash, exhaustive conversation history and global literature completeness were not independently reverified by that audit.

## Portable reproduction

From any directory, run Python 3.10+ with its standard library:

    python3 /path/to/30001599/verify_publication.py --expected-manifest-sha256 <SHA-256 of PUBLICATION_MANIFEST.json recorded in the PR>

The verifier checks the exact file set, byte counts, hashes, both frozen manifests, the audit-to-author binding and archive membership. It rejects deliberate corruptions before replaying the independent and author controls in a temporary relocated copy. The checked-in originals are never executed in a mode that overwrites their results. The audit output must equal the preserved result exactly.

Do not run either snapshot's command-line entry point in its frozen directory: those scripts write adjacent results files. Use the wrapper above.

This publication changes only this target's queue Status to unsolved and Turns to 5/5. Findings, Chat, DOI, all other rows, and the existing embedded queue header remain byte-identical. No queue regeneration, merge, release, DOI deposit or external outreach is part of this draft.
