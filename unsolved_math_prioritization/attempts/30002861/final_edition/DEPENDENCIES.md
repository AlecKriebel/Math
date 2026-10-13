# Exact dependencies and edition boundaries

## Preserved mathematical editions

The corrected [fourth mathematical edition](fourth_edition/README.md) is retained exactly once, with its [public manifest](fourth_edition/CONTENT_MANIFEST.json). It contains the [third edition](fourth_edition/third_edition/README.md), which contains the [second edition](fourth_edition/third_edition/second_edition/README.md) and [first edition](fourth_edition/third_edition/second_edition/first_edition/README.md). Their internal proof, audit, source and reproduction links remain intact. No parallel copy of a baseline edition is added.

The first through fourth editions' pass counts and preparation-status descriptions are historical statements about those editions. The final count is five newly documented shared substantive passes, with an unknown lifetime total. The corrected fourth edition differs from its frozen predecessor only in one public phrase and the corresponding public manifest record; the exact correction is described in [CORRECTIONS_AND_SCOPE.md](CORRECTIONS_AND_SCOPE.md).

The immutable published second-edition baseline is revision [03de8676c83d933e95fb612d170ec5d0f39c700b](https://github.com/AlecKriebel/Math/tree/03de8676c83d933e95fb612d170ec5d0f39c700b/unsolved_math_prioritization/attempts/30002861/second_edition), associated with [PR 1328](https://github.com/AlecKriebel/Math/pull/1328). Its [reader guide](https://github.com/AlecKriebel/Math/blob/03de8676c83d933e95fb612d170ec5d0f39c700b/unsolved_math_prioritization/attempts/30002861/second_edition/README.md) fixes that published scope. This checkpoint asserts no separate remote publication of the third, fourth or final editions.

## Dependencies of the final theory

- [Quartic reduction](fourth_edition/third_edition/second_edition/first_edition/QUARTIC_REDUCTION.md) and [quartic audit](fourth_edition/third_edition/second_edition/first_edition/QUARTIC_AUDIT.md): exact equivalence Rm=Hj; even nonsingular interior rows; no boundary fan compatibility row; zero-ray row criterion; closed-component characterization.
- [Convex support](fourth_edition/third_edition/second_edition/first_edition/CONVEX_SUPPORT.md): induced convexity; strict/straight boundary parity and degree restrictions; full original stars and at least three nonsingular degree-four interior support vertices.
- [Second-pass theory](fourth_edition/third_edition/second_edition/SECOND_PASS_THEORY.md) and [theory audit](fourth_edition/third_edition/second_edition/THEORY_AUDIT.md): normalized full-support weighting; exact homogeneous magnitude balance; automatic pure-gradient obstruction; one-way compact C1 quadratic construction.
- [Second-pass constructions](fourth_edition/third_edition/second_edition/SECOND_PASS_CONSTRUCTIONS.md) and [construction audit](fourth_edition/third_edition/second_edition/CONSTRUCTION_AUDIT.md): forced exterior attachments and strict adjacent-turn necessities; at least five strict corners; exact integer sign-balanced but magnitude-unbalanced control.
- [Corrected cofactor normal form](fourth_edition/third_edition/COFACTOR_NORMAL_FORM.md), [acceptance](fourth_edition/third_edition/INDEPENDENT_COFACTOR_ACCEPTANCE.md), and [incident-segment correction](fourth_edition/third_edition/CORRECTION_NOTE.md): local polynomial form on actual full fans; agreement on each incident segment, with no invalid whole-line statement for a piecewise function.
- [Global incidence theorem](fourth_edition/FOURTH_PASS_GLOBAL_INCIDENCE.md) and [acceptance](fourth_edition/INDEPENDENT_GLOBAL_INCIDENCE_ACCEPTANCE.md): proper coloring, boundary parity, refined degree-four count, interior-edge connectivity under the required boundary degrees, and conditional exclusion of three distinct concurrent color lines.

The final [boundary-completion theorem](FIFTH_PASS_BOUNDARY_COMPLETION.md) proves the sufficiency of the forced collar, the exact finite completion interface and the boundary-chord restriction. These conclusions were not already supplied by the older necessary exterior tests. Its [independent acceptance](INDEPENDENT_BOUNDARY_COMPLETION_ACCEPTANCE.md) states the accepted proof and finite-check scope.

## Dependencies of the final construction obstruction

The [fourth-pass extension](fourth_edition/FOURTH_PASS_NONPENCIL_EXTENSION.md), [independent acceptance](fourth_edition/INDEPENDENT_NONPENCIL_EXTENSION_ACCEPTANCE.md), [exact certificate](fourth_edition/FOURTH_PASS_CERTIFICATES.json) and [short rank certificates](fourth_edition/EXACT_RANK_CERTIFICATES.json) specify the exact fifteen-vertex, twenty-one-face candidate. All twenty-eight interior edges balance, its same-color triple 2,5,13 is noncollinear, and the actual reduced matrix has full row rank eight. The disk is nonconvex and has reflex vertices 12 and 14.

The final [additive obstruction](FIFTH_PASS_ADDITIVE_OBSTRUCTION.md) adds a rank-fourteen rigidity proof for its old weights and whole-sector separation at both reflex vertices. Its [independent acceptance](INDEPENDENT_ADDITIVE_OBSTRUCTION_ACCEPTANCE.md) preserves every old-face, old-coordinate and nonzero-weight qualification. Replacing old faces, subdividing them, moving old vertices and choosing other disks are not excluded.

The final proof does not depend on a claim that all convex nonpencil disks fail. The general collar theorem does not depend on completing this nonconvex candidate. The two branches belong to the same final fifth pass.

## Quantifiers that remain separate

The [full eighteen-vertex theorem](fourth_edition/third_edition/THIRD_PASS_CEVA_OBSTRUCTION.md) covers every admissible realization of that full topology because every prospective closed component is forced to contain the entire core. The [nested-ring theorem](fourth_edition/third_edition/THIRD_PASS_NESTED_RING_EXTENSION.md) excludes complete specified cores with any finite sequence of whole annuli. It does not exclude irregular proper components in all larger full meshes.

The fourth-pass color-pencil exclusion assumes actual containment on three distinct concurrent projective lines. The sufficient propagation rules do not prove every support satisfies it. The nonpencil control changes triangulation incidence while the underlying space remains a disk. Its new fan is outside the complete-annulus hypotheses.

The finite collar controls do not themselves satisfy all conditions for a balanced closed support. The existing integer support remains magnitude-unbalanced. An arbitrary compact C1 quadratic remains insufficient for the quartic proportionality requirement. The final sharp unresolved statement is in the [reader guide](README.md).

## Attribution and source limits

The cubic counterexample is credited to Qiu's [versioned September 2026 preprint](https://arxiv.org/abs/2609.06364v1), with the inherited exact proof and audit linked above. Source coordinate arrays and copied source documents are not included. The [bounded source review](fourth_edition/third_edition/second_edition/first_edition/SOURCES.md), [PDF metadata](fourth_edition/third_edition/second_edition/first_edition/SOURCE_METADATA.json), and [third-edition Morgan–Scott context](fourth_edition/third_edition/SOURCE_METADATA.json) retain their dated inspection limits. No new source retrieval, fresh literature-status survey, worldwide-openness or historical-priority conclusion is claimed.
