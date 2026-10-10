# Pointed pseudotriangulation counts: accepted exposure-witness partial

Problem 5500040 / AMR-054-0040 (TOPP 40).

**Accepted partial only. The universal per-set comparison remains unresolved.**
The question asks whether every finite planar point set in general position
has at least as many pointed pseudotriangulations as triangulations, always
on the same full vertex set and without Steiner points.

## Results preserved in full

- If each interior point p becomes extreme after removing at least one original hull vertex, an explicit injection proves ppt(S) >= (product over p of |E(p)|) t(S).
- Every chosen exposure edge belongs to every triangulation. Recovering T=P union F and D=F minus P proves injectivity including the witness choices.
- A displayed six-point wheel contains no pointed pseudotriangulation. This refutes universal containment-only maps and containment-only Hall arguments, but does not refute the counting inequality.
- The audit gives an independent analytic count t=11 and ppt=25 for that example.
- With one interior point, unique refinement gives ppt(S)=sum_T d_p(T). The full positive Catalan difference is credited to Randall, Rote, Santos and Snoeyink (2001).
- The general weighted-refinement identity is proved, while the needed global compensation lower bound remains unproved.

The embedding-specific characterization is credited to Rote, Santos and
Streinu's survey and its attribution to Streinu. Earlier family results are
credited to Aichholzer, Orden, Santos and Speckmann. The prior existence of
containment obstructions is acknowledged through TOPP 50 and O'Rourke's
2002 column. The author correction for arXiv:1210.7126 is retained:
Ben-Ner, Schulz and Sheffer, not Sharir and Sheffer.
No novelty or bibliographic priority is established or claimed.

## Files and review meaning

- [PROOF_PARTIAL.md](PROOF_PARTIAL.md): complete analytic proofs, coordinate example, exact target and remaining gap
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): complete mathematical audit, independent analytic count, and recorded supporting checks
- [ACCEPTANCE.json](ACCEPTANCE.json): exact public proof/audit identities, accepted claims and historical aggregate checks
- [STATUS.json](STATUS.json): unresolved full target and accepted partial scope
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): source credit and historical inspection boundaries
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public bibliography, recorded source identities and retrieval/inspection history
- [MANIFEST.json](MANIFEST.json): exact eight-member inventory and seven non-manifest identities

The manuscript and independent audit are AI-assisted and unrefereed.
Acceptance is a mathematical audit verdict; no external human peer review,
journal acceptance, or formal proof-assistant certification is claimed.
A bounded earlier source check located no universal resolution. This is
not an exhaustive or current worldwide literature-status certification.

## Editorial and distribution boundary

All analytic arguments and mathematical qualifications remain. Changes
reconcile completed acceptance, bind public document identities, remove
private provenance and stale review state, and clearly label earlier
computational/source observations as historical. The analytic verdict
depends on no omitted program, generated detailed result, or fixture dataset.
The displayed six-point coordinates and small determinant lists belong to
the authored analytic proof; prior finite enumeration tables are aggregate
verification metadata only.

No programs, generated detailed certificates/results, copied source bodies,
PDFs/images, fixture datasets, or private coordination are distributed.
This edition makes no packaged computational reproducibility claim.
Edition preparation reran no mathematical checks and performed no new
scholarly-source retrieval, source-file rehash, source inspection, or
literature search.

QUEUE.md and all unrelated repository content remain unchanged. No merge,
release, DOI, journal submission, or external outreach is implied.
