# Source and scope audit

The mathematical target for problem 4500001 / AMR-044-0001 is the arithmetic region and period classification in the originating 2015 article. The 2015 article has pages 69–73; the earlier 2012 source is a 24-page manuscript, and its leaf is genus three. The proofs use these source conventions explicitly.

## Primary sources inspected

1. Dragović–Radnović, *Periods of Pseudo-Integrable Billiards*, Arnold Mathematical Journal 1 (2015), 69–73, DOI https://doi.org/10.1007/s40598-014-0004-0 . All five pages were read, including all three questions and final remarks. The period examples and geometric figure on page 71 were visually inspected during the recorded author inspection.
2. Dragović–Radnović, *Pseudo-integrable billiards and arithmetic dynamics*, arXiv:1206.0163v1 (1 June 2012), https://arxiv.org/abs/1206.0163v1 . The complete retrieved 24-page manuscript was read, including Sections 6–8. Pages 18, 19 and 23 were additionally rendered and visually inspected. Section 1 supplies the convex/reflex corner distinction; Sections 3–5 supply the genus-3 geometry and measured-foliation decomposition; Section 7 supplies the source IET; Section 8 supplies the counterexample to sufficiency of the Cayley relation.

Metadata, public URLs, retrieval times, byte counts and reverified SHA-256 hashes are in [SOURCE_METADATA.json](SOURCE_METADATA.json). The source PDFs and extracted text are not part of this package.

## Formula discrepancy detected and resolved geometrically

The retrieved 2012 v1 PDF has a wrong sign in the second negative translation of its lower-sign case on page 19. As printed, that entry duplicates the image of a positive interval and makes the alleged IET noninjective. The exact interior witness and correct geometric formula are in [PROOF.md](PROOF.md), Section 1. The corrected entry agrees with the permutation printed on the same page. This is a statement about the inspected version only; no claim is made that every later version or the published journal article has the same typo.

The audit records that the original test suite distinguished the printed formula from its corrected version in all three parameter regimes and expected the isolated printed-entry disagreement. The self-contained interval-overlap and exact rational witness arguments establish the failure without a numeric tolerance. Historical Euclidean ray-tracing checks corroborated the independently derived geometric map; no proof depends on omitted code or output.

## Scope retained

- Opposite concentric semicircles with their two collinear connecting segments.
- Strictly interior positive circular caustic, normalized by arccos(r/R)/pi.
- Direction retained, straight-segment collisions counted, reflex singularities not artificially continued.
- Mixed periodic/nonperiodic behavior allowed and proved on the quarter-rotation line.
- Rationally dependent irrational parameters are not declared periodic merely from an integer relation.
- Generic multi-arc/radial tables and a new confocal normalization theorem are not claimed.
- The unbounded word-certificate test is not described as a terminating solution of the full arithmetic question.

## Rights and content exclusions

This separately sealed edition contains the complete corrected proof, full mathematical audit, exact correction and witness, acceptance/status, source review and public verification metadata. It distributes no programs, raw outputs, datasets, source PDFs, copied source text or images, repository/queue snapshots, private coordination material or private personal data. Mathematical formulas necessary to state and audit the model are accompanied by precise citations. Public access to a source is not treated as redistribution permission.

## Corrected acceptance and historical limits

The audit's sole required correction concerns strict exclusion of convex-corner trajectories: this can split oriented cylinders. The exact required replacement is applied in PROOF.md and recorded with its full witness in CORNER_CORRECTION.md. All main region formulas and oriented-cylinder counts use the continuous convex-corner convention. The original frozen author and audit records are unchanged.

The public proof writes out complete finite derivations of the same three examples accepted by the audit, using only its already accepted permutation, singular-strip and reversal formulas. The correction artifact also spells out the reversal pairing in its already audited witness. These editorial substitutions were checked in exact arithmetic. They are no new theorem, parameter family or region-count claim.

Edition preparation rechecked frozen byte identities and publication integrity. It did not rerun the original mathematical programs or perform new scholarly retrieval, source-text inspection or literature search. Historical finite tests supplement universal arguments; they do not replace them. This AI-assisted manuscript and audit are unrefereed, with no external human peer-review, journal-acceptance, proof-assistant-certification, novelty, priority, exhaustive-literature or current-worldwide-openness claim. The general irrational dependent classification remains unresolved.
