# Exact mathematical dependencies of the fourth edition

## Preserved third mathematical edition

The complete [third mathematical edition](third_edition/README.md) is preserved byte-for-byte once, including its existing second- and first-edition dependencies. This retains its relative links without a second parallel copy of the earlier editions. Its [manifest](third_edition/CONTENT_MANIFEST.json) and the new [manifest](CONTENT_MANIFEST.json) identify the exact mathematical texts. A file identity specifies a text; it does not prove the text's claims.

The third edition's original publication-status and then-current three-pass wording are historical. This fourth edition neither revises those bytes nor asserts a separate published third-edition revision. The auxiliary seed omitted from that edition gains a new finite audit here rather than retroactive third-pass acceptance.

## Immutable published baseline

The second edition is available at the immutable revision [03de8676c83d933e95fb612d170ec5d0f39c700b](https://github.com/AlecKriebel/Math/tree/03de8676c83d933e95fb612d170ec5d0f39c700b/unsolved_math_prioritization/attempts/30002861/second_edition), associated with [PR 1328](https://github.com/AlecKriebel/Math/pull/1328). The [second-edition guide](https://github.com/AlecKriebel/Math/blob/03de8676c83d933e95fb612d170ec5d0f39c700b/unsolved_math_prioritization/attempts/30002861/second_edition/README.md) provides the published scope. The retained local copies also supply these mathematical dependencies without relying on mutable branch links.

## Dependencies used in the new proofs

- [Quartic reduction](third_edition/second_edition/first_edition/QUARTIC_REDUCTION.md) and [quartic audit](third_edition/second_edition/first_edition/QUARTIC_AUDIT.md): exact equivalence Rm=Hj, even nonsingular interior rows, unconstrained boundary fan elimination, full-row-rank sufficiency and active-component closure.
- [Convex support](third_edition/second_edition/first_edition/CONVEX_SUPPORT.md): induced convexity; even strict-corner and odd straight-boundary degrees; at least three original nonsingular degree-four interior vertices and the full original star of each. Degree in an arbitrary auxiliary subcomplex is insufficient.
- [Second-pass theory](third_edition/second_edition/SECOND_PASS_THEORY.md) and [its audit](third_edition/second_edition/THEORY_AUDIT.md): normalized nonzero weights U_v=x_v(v_x,v_y,1)^T, the exact homogeneous balance equation with no division by x_v+x_w, and the obstruction implication for a genuinely closed balanced component.
- [Second-pass constructions](third_edition/second_edition/SECOND_PASS_CONSTRUCTIONS.md) and [their audit](third_edition/second_edition/CONSTRUCTION_AUDIT.md): feasible actual exterior attachments, at least five strict support corners and the complete eighteen-vertex topology.
- [Third-pass pencil proof](third_edition/THIRD_PASS_CEVA_OBSTRUCTION.md), Section 1, and [its audit](third_edition/INDEPENDENT_RING_ACCEPTANCE.md): boundary positivity on an unsubdivided side with its actual exterior opposite vertex. Sections 2 onward give the twelve-vertex pencil and complete eighteen-vertex interpolation result, used here as the earlier theorem's precise scope.
- [Third-pass nested-ring proof](third_edition/THIRD_PASS_NESTED_RING_EXTENSION.md) and [its audit](third_edition/INDEPENDENT_NESTED_RING_ACCEPTANCE.md): complete nested-core exclusion for any finite sequence of the specified forward/reverse annuli. The new fan extension changes this incidence pattern. Arbitrary proper components in larger full meshes were not excluded.

The corrected [cofactor normal form](third_edition/COFACTOR_NORMAL_FORM.md), [its acceptance](third_edition/INDEPENDENT_COFACTOR_ACCEPTANCE.md) and [correction note](third_edition/CORRECTION_NOTE.md) are preserved as part of the frozen preceding edition. Their incident-segment distinction is unchanged. The new color-pencil theorem does not require a whole-supporting-line identity for a piecewise function.

## New acceptance boundary

The [global incidence acceptance](INDEPENDENT_GLOBAL_INCIDENCE_ACCEPTANCE.md) covers the global coloring argument, boundary restrictions, interior-edge connectivity, conditional pencil normalization and exclusion, sufficient propagation rules and the exact eight-vertex control.

The [extension acceptance](INDEPENDENT_NONPENCIL_EXTENSION_ACCEPTANCE.md) covers the exact twelve-vertex seed, twelve-vertex reflex-ear intermediate and fifteen-vertex nonpencil extension. It supplies finite geometry and reduced-rank verification, not a convex closed completion or a universal quartic conclusion.

The [new reproduction guide](REPRODUCTION.md) fixes the fourth-pass certificate's own row scaling and column ordering. Earlier certificates are preserved with their original conventions. No new literature search, historical novelty determination or claim of worldwide openness is made by this edition.
