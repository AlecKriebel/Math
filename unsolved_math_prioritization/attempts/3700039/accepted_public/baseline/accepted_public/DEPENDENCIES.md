# Mathematical dependencies and version boundaries

## Frozen accepted baseline

The [corrected third-pass reader manifest](baseline/corrected_public/MANIFEST.json) has SHA-256 ec9c982a8b77bf6d5b4fd973c06d0081b19f6a31645f1d7b3a0d57168ebe9626. The [third-reader acceptance supplement](baseline/public/REVIEW_MANIFEST.json) has SHA-256 34291c112d95265d3e0066c654248fe5582b243f38d8e639eab5bd2b4a7926d2. These two adjacent trees preserve their original navigation and exactly one copy of each inherited public file. The supplement's author-certificate destination correction remains applied. The prior erroneous destination is not the active baseline.

The [complete baseline acceptance](baseline/public/reader_edition_acceptance.md) describes the corrected self-contained reproduction and the older missing-input repair. Reproduction of this fourth edition reconstructs that accepted closure exactly before replaying its original and corrected mathematical readers. Historical objects retain their historical three-pass or two-pass labels; this edition itself contains four documented substantive passes, with lifetime prior count unknown.

## Relative-phase branch

The [new theorem](proofs/relative_phase.md) uses the [third-pass cyclic proof](baseline/corrected_public/proofs/cyclic_two_harmonic.md) and [corrected audit](baseline/corrected_public/audits/cyclic_acceptance.md) for context and the legitimate full-cover helical averaging construction. Its own proof restates the scalar positivity argument and derives the exact complex-amplitude median identity directly, rather than importing it from a different parameter regime.

The positive periodic scalar inverse is also established in the [second-pass periodic proof](baseline/corrected_public/baseline/two_pass/proofs/second_pass_periodic.md). Its kernel has the backward phase shift s-omega t. The [earlier finite-torus-point obstruction](baseline/corrected_public/baseline/two_pass/proofs/second_pass_periodic.md) does not apply to smooth full-phase averaging followed by evaluation of the resulting smooth polynomial. Neither this distinction nor the new coefficient tests authorize singular measure pairings.

The full [relative-phase audit](audits/relative_phase_acceptance.md) supplies explicit boundary quartic factorization, continuous distributional examples, both failures of nonlinear averaging, the dominance counterexample and an admissible nonrigid-first-axis cancellation example. These are scope controls, not counterexamples to the original question.

## Critical-layer and embedding branches

The [critical-layer report](proofs/packets/REPORT.md) proves its radial defect estimate directly by variation of constants and the median's order/Lipschitz properties. Its harmonic boundary median is recomputed from an exact ordering sector; the same first-pass identity appears in the [first-pass theory](baseline/corrected_public/baseline/two_pass/proofs/first_pass_theory.md). The report keeps numerator and actual maximum separate.

The example of a radially stationary normalized shape with noncompact negative parts refers to the [third-pass concentration construction](baseline/corrected_public/proofs/concentration.md), fully covered by its [independent audit](baseline/corrected_public/audits/concentration_acceptance.md). This example illustrates the radial criterion's independence from angular compactness; it is not used to infer compactness or automatic small defect.

The [fixed harmonic embedding](proofs/packets/HARMONIC_EMBEDDING.md) uses the cutoffs, annular repair and exponential tail architecture of the adjacent [critical-layer report](proofs/packets/REPORT.md). It independently proves a positive record slope from the actual harmonic maximum's convexity and strict increase. It does not replace that maximum by the sum of coefficient amplitudes. Its complete audit is [here](audits/harmonic_packet_acceptance.md).

Sharpness transfer uses exactly the finite harmonic-polynomial Fejer construction in the [first-pass proof](baseline/corrected_public/baseline/two_pass/proofs/first_pass_theory.md) and [first-pass acceptance](baseline/corrected_public/baseline/two_pass/audits/first_theory_acceptance.md). Each epsilon chooses a fixed finite polynomial triple before embedding. There is no exchange of an unbounded polynomial degree with the packet limit and no assertion of a single input attaining -pi. The universal upper endpoint 2pi and positivity of the radial gaps give the exact supremum of the constructed examples.

## Authored certificate roles

The [embedding report](proofs/packets/HARMONIC_EMBEDDING.md) and its [author certificate](certificates/embedding_author.json) retain exact authored bytes. The packet [main report](proofs/packets/REPORT.md) differs only by indentation of two mathematical displays that would otherwise render as broken Markdown links. Its [main certificate](certificates/packet_author.json) preserves every mathematical field and rebinds only the report hash to that included proof. The packet audit certificate likewise rebinds that proof and omits the separate operational inventory hash. Exact originals and reversible changes are retained for reconstruction; the [display correction account](changes/README.md) specifies the changes. The [relative author certificate](certificates/relative_author.json), [relative audit certificate](certificates/relative_audit.json), [packet audit certificate](certificates/packet_audit.json), and [independent fourth-reader reconstruction](certificates/fourth_reader_exact.json) remain distinct. No author certificate is relabeled as an independent audit.
