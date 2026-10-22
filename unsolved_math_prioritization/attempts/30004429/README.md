# Schonmann two-sided continuity: audited partial results

Problem 30004429 (OWR-17474-001), rank 751. **Unsolved, 5/5. No resolution or novelty claim.**

The target is the singleton almost-Gibbs question for the horizontal-line marginal of the extremal plus phase of the finite-temperature, zero-field two-dimensional nearest-neighbor ferromagnetic Ising model above beta_c. The exact almost-sure two-sided annulus-influence limit remains unproved.

The [frozen authored proofs](author/PROOFS.md) retain an essential-oscillation criterion, an extremal-annulus reduction, a sufficient summable-variation transfer, and exact countercontrols. The [independent adversarial audit](independent_audit/AUDIT_REPORT.md) passes these partial results, with no blocking corrections. It is an internal AI audit, not peer review or exhaustive literature/priority certification.

## Controlling clarifications

These clarifications govern interpretation without rewriting either historical freeze:

- In author Section 6.2, the strict essential range is the two-point set {1/4,3/4}. Its smallest containing interval, or essential-infimum/supremum interval, is [1/4,3/4]. The oscillation is 1/2.
- In author Section 6.3, X and Y are plus indicators valued in {0,1}. The displayed covariances are lambda(1-lambda)/4 and 1/16. For {-1,+1} spins multiply both by four, obtaining lambda(1-lambda) and 1/4.
- The singleton criterion does not automatically construct an everywhere consistent full specification or an unsupported common-null-set extension.
- The later sufficiently-low-temperature regular-g theorem is one-sided. No one-sided-to-two-sided conclusion for the target is claimed. The summable-variation sufficient criterion retains its hypothesis, which is not established for the target.
- The appended catalog long-range clause is mis-extracted or under-specified: the primary report's adjacent long-range question concerns Aizenman-Higuchi. Canonical continuity for the original summable Dyson interaction is a separate control, not a resolution of that clause or a transformed-model statement.

The author archive and eight files, and the independent audit archive and six files, are unchanged. Historical statements that an audit is pending or that no remote writes were made describe their original snapshots. This wrapper records the subsequent scoped acceptance and publication.

## Reproduce

Run `python3 verify_publication.py` from this folder, or invoke it by absolute path from another working directory. Python's standard library suffices. It checks the exact file/directory allowlist, hashes and archive membership, immutable scope, both original manifests, author replay, and independent exact controls. Replay output is written only to a temporary directory. `python3 -O verify_publication.py` also keeps delivery checks active; the underlying scientific scripts are explicitly replayed with assertions enabled.

Finite controls include the 32,768-state author Ising box and independent row-transfer calculations at three temperatures. Finite checks establish neither an infinite-volume limit nor almost-sure target continuity. See the audit for source-inspection limits.

Only the target row's Status and Turns change in QUEUE.md. Its embedded historical header, every other row, and the target Findings, Chat and DOI remain byte-for-byte unchanged. Source PDFs, source extracts, raw datasets and private coordination files are excluded. No merge or release is part of this draft.
