Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The final structural theorem is independent of a finite computer bound. Earlier through-nine and through-ten results retain their historical scope in unchanged companion editions. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Actual verification and scope

All three executions completed on 12 October 2026 UTC using Python's standard library:

- full fresh author verification under normal Python: PASS, optimization 0
- full fresh author verification under Python -O: PASS, optimization 1
- full fresh author verification under Python -OO: PASS, optimization 2

The receipts agree after removing the optimization field. They enumerate all six canonical twisted encodings at order three and all 1,296 at order nine. The generator assigns independently one of six orientation/color states to each positive cyclic distance. It checks every actual arc of the resulting twist symmetry. No random seed, external solver, timeout, or pruning incompleteness occurs in this small author test.

At order three, three encodings have exactly the failed-predecessor relation in the fixed +1 Hamilton order, and none is rainbow-free. At order nine, twelve have that exact failed-predecessor relation; all yield the actual 0->2->4->0 rainbow witness and the eighteen forced offmatching arcs. Among all order-nine encodings, 432 are rainbow-free and every one has every vertex as an outgoing source. Of these, 360 have no spanning monochromatic color and 72 are balanced in every color. These finite checks validate the implementation and fixtures; they do not establish a new general finite tournament bound.

Eight rigid-family members are checked at orders 3, 9, 15, 21, 27, 33, 45 and 81. Each has the exact failed-predecessor relation and no outgoing source, and each contains a cyclic rainbow triangle. These are positive tests of the structural premises without rainbow exclusion, not conjecture counterexamples. The all-order family has its own proof.

Every enumerated matrix and every rigid-family matrix is checked by both BFS and an independent Boolean Floyd-Warshall closure. A separately written directed-triangle enumeration verifies each reported rainbow witness. Fixed fixtures also check: a rainbow-free fully twisted tournament with every vertex a source but no spanning color; a strict-period-three Hamilton word without a globally color-permuting shift; three simultaneous choices of spanning colors in an exact-color-transitive seven-vertex tournament; and the nine-vertex four-color affine example where no color spans.

Twenty explicit rejection gates cover malformed matrices, loops, missing/duplicate pair orientations, Boolean values passed as integers, invalid palettes or distance states, wrong order, missing exact-failure/symmetry premises, nondistinct or incorrect chosen fiber colors, and confusing a predecessor failure with the reversed tournament's successor failure. Exceptions remain active under -O and -OO.

The certificate validates hypotheses and computes actual forced arcs and a rainbow triangle. It does not establish that an input is induced-minimal or search for its automorphism group. No proof assistant or unrestricted exhaustive enumeration is claimed. The independent mathematical audit and the separate finite orbit-CSP lane are different deliverables and are not premises of these author checks.
