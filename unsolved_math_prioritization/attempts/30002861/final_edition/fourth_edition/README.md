# Cubic and quartic spline interpolation fourth mathematical edition

Row 1761, problem 30002861 / OWR-13678-002. Prepared 13 October 2026 UTC.

## Result and status

Every balanced closed active support has a proper vertex three-coloring. Its boundary word obeys exact parity restrictions. If its three color classes additionally lie on three distinct concurrent projective lines, it is impossible. The line-containment hypothesis is essential to this theorem; this edition does not prove it for arbitrary closed supports.

An exact rational construction extends the earlier auxiliary twelve-vertex seed to a conforming fifteen-vertex disk outside the color-pencil class. All 28 interior edges satisfy the magnitude balance equations. The disk remains nonconvex and its actual reduced quartic matrix has full row rank eight. A separate eight-vertex control has nine balanced interior edges and actual reduced rank two. Both controls admit arbitrary quartic vertex first jets. Neither is a closed balanced support or a counterexample.

The unrestricted quartic interpolation assertion remains unresolved by this work. The cubic vertex-value assertion has a negative answer credited in the unchanged [first edition](third_edition/second_edition/first_edition/README.md). **The bundled row remains unsolved.** No novelty, priority, worldwide-openness or external-peer-review claim is made.

There are **four newly documented substantive passes** in this sequence; the lifetime total is unknown. The global incidence proof, seed extension, audits and editorial preparation are branches of the same fourth pass and add no separate passes.

## Fixed mathematical model

A mesh is a finite conforming straight-line triangulation of a polygonal disk. Distinct vertices have distinct positions and every original triangle is nondegenerate. Values and both first derivatives are independently prescribed at all vertices, including boundary vertices. The interpolant is globally C1 and piecewise polynomial of degree at most four on the original triangles. There is no refinement, vertex movement or imposed boundary condition.

The accepted reduction is Rm=Hj. A prospective nonzero left dependency is supported on a closed balanced active component. Its induced support K is convex; every induced edge is active; interior degrees are even; strict boundary corners have even induced degree at least four; straight boundary vertices have odd induced degree at least five. At least five boundary vertices are strict corners. Every closed component contains at least three original nonsingular degree-four interior mesh vertices, with their full original stars.

The degree-four count below concerns vertices interior to the induced support, where the full original star is present. It is not permission to replace original-mesh nonsingularity and full-star closure by a degree count in an arbitrary subcomplex. Actual exterior triangles are retained whenever boundary balance or exterior attachment is invoked.

## Reading guide

1. [Global incidence proof](FOURTH_PASS_GLOBAL_INCIDENCE.md) establishes global three-coloring, boundary parity, the refined degree-four count, common-base normalization from color-pencil containment, the conditional global exclusion and two sufficient propagation rules. [Its independent acceptance](INDEPENDENT_GLOBAL_INCIDENCE_ACCEPTANCE.md) checks the arguments and eight-vertex control.
2. [Nonpencil extension](FOURTH_PASS_NONPENCIL_EXTENSION.md) independently reconstructs the twelve-vertex seed, fills one reflex ear and adds a three-vertex fan. [Its independent acceptance](INDEPENDENT_NONPENCIL_EXTENSION_ACCEPTANCE.md) covers all three finite disks, their embedding, balances and actual reduced ranks.
3. [Exact finite certificates](FOURTH_PASS_CERTIFICATES.json) give authored rational coordinates, weights, faces, exact boundary turns, endpoint balance coefficients, sparse reduced rows and nonzero maximal minors. The independent [short triangular rank certificates](EXACT_RANK_CERTIFICATES.json) give normalized determinant-one witnesses for the seed and extensions. The [reproduction guide](REPRODUCTION.md) specifies every indexing and normalization convention without requiring a particular program.
4. [Accepted dependencies](DEPENDENCIES.md) identifies immutable second-edition references and the preserved third mathematical edition. [Edition boundaries](EDITION_BOUNDARIES.md) separates new acceptance from the frozen historical scope. The [content manifest](CONTENT_MANIFEST.json) identifies all public files except itself.

## Boundary consequences and conditional scope

Let k be the number of strict boundary corners, s the number of straight boundary vertices and N4 the number of degree-four interior support vertices. Then s is even and N4 is at least 3+s/2. If s=0, k is a multiple of three and k is at least six. If k=5, then s is at least two, the total boundary size is at least seven and N4 is at least four.

The color-pencil hypothesis forces at most six boundary vertices. The preceding restrictions then force exactly six strict corners and no straight subdivisions. Opposite same-color diagonals meet at a finite interior point. Their weights must have opposite signs, whereas the accepted positivity lemma, using the actual exterior triangle on each unsubdivided boundary side, forces one common boundary sign. This contradiction does not extend positivity to individual subedges of a subdivided straight side.

The line/base rules certify consequences of exact fixed-base patches on arbitrary incidence patterns. They are sufficient rules. No assertion is made that they reach every vertex, that a single four-star starts a complete certificate, or that a new closed topology has passed the rules.

## What remains

The remaining problem is to find an admissible balanced closed support outside the excluded classes, or prove that none exists. Convexity, legal boundary degrees, feasible original exterior attachments and all full closed-component equations remain necessary. Interior balance alone is insufficient. Boundary vertices 12 and 14 of the fifteen-vertex control have induced degree three and reflex turns; they cannot be treated as legal straight support vertices.

The third-edition theorem for every admissible realization of the specified full eighteen-vertex topology remains separate from its all-size exclusion of complete nested-ring cores. Irregular proper components in larger full meshes remain unresolved. The fourth-pass extension escapes the complete-annulus incidence hypotheses and does not contradict either theorem.

This edition contains authored mathematical proofs, independent mathematical audits, exact authored finite certificates and public references. Earlier editions are retained once, byte-for-byte, with their relative-link structure. No earlier theorem or source-inspection limit is silently enlarged.
