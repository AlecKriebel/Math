# Labeled die rolling on a complete rectangle

First mathematical edition for row 1758 / 5500068 / AMR-054-0068. Date: 2026-10-13.

**Status: unresolved.** This edition records exactly one newly documented substantive pass. The prior lifetime attempt count is unknown. Neither a polynomial-time algorithm nor an NP-hardness proof for the exact target has been obtained.

## The precise question

Every cell of a nonempty finite rectangle is labeled with one of 1–6. A fixed-chirality die, with opposite labels summing to seven, begins at a specified corner with its top matching that cell. It rolls to adjacent cells, matching the label on top after landing, and must visit every cell exactly once. There are no free cells, blocked cells, holes, outside excursions, lifts, or rotations in place. The solution is a path, with no closing return. Fixed initial orientation and selectable initial orientation are separate variants; the results state which is meant.

## Results of this pass

1. A physical adjacency fixes at most one full-state transition and belongs to at most one invariant parity phase. The rectangular edge budget lets at most one phase meet the spanning-path edge-count requirement.
2. A three-color potential characterizes the phase projection. It excludes four-cycles and imposes a checkerboard-area congruence on every simple projected cycle. Projected six-cycles can occur and need not be physically rollable.
3. Once the initial state, other endpoint, and final state are fixed, exhaustive sound degree/state/forced-edge propagation leaves ambiguous cells only as singletons or side-adjacent dominoes, with no diagonal contacts. The proof uses full rectangular coverage and the corner start. Attainment of the ambiguity bound is not claimed.
4. One Boolean variable per singleton or domino, together with fixed-state edge variables, exact degree equations, and connectedness of the selected edges, gives an equivalent formulation. The global selection problem remains unresolved.
5. An explicit authored 4 × 5 board has a connected candidate graph and feasible local orientation/degree constraints but no complete path from its prescribed corner, even with selectable initial orientation.
6. An orientation-preserving 2 × 5 cap admits an unintended full traversal ending inside the cap. Correct net orientation alone does not justify eliminating holes from a hardness reduction.

## Complete proofs and certificates

- [Residual orientation structure](ORIENTATION_STRUCTURE.md): conventions, phase/color lemmas, propagation, singleton/domino theorem, and exact Boolean formulation.
- [Global-connectivity obstruction](CONNECTIVITY_OBSTRUCTION.md): the 4 × 5 board and full nonexistence proof.
- [Hole-filler obstruction](FILLER_OBSTRUCTION.md): two explicit cap traversals and the boundary-parity identity.
- [Certificate guide](CERTIFICATE_GUIDE.md) and [exact authored certificate](EXACT_AUTHORED_CERTIFICATE.json): complete small-board data and how to check them from the roll permutations.
- [Independent structural review](INDEPENDENT_STRUCTURE_REVIEW.md) and [verification summary](VERIFICATION_SUMMARY.json).
- [Source and model audit](SOURCE_MODEL_AUDIT.md), [source identities](SOURCE_IDENTITIES.json), and [integration and acceptance](INTEGRATION_AND_ACCEPTANCE.md).

## Prior literature and the remaining gap

Buchin and coauthors' parity/state-graph framework is credited. Their free-cell and prescribed-cycle-length hardness results concern different targets. De Biasi's Figure 4 is an older 2012 nonuniqueness construction: its two 270-cell cycles were independently replayed, and all 270 dash annotations in each drawing point opposite the manuscript's stated reference-face direction. The board labels and cycles remain valid. This is verification and annotation correction of prior literature, not a new nonuniqueness theorem. The full source-status qualifications are retained in the audit.

The next mathematical gap is global connected edge selection, or a valid no-hole reduction with exact path and corner/start-state interfaces. No second pass is part of this edition. [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) identifies every public file; this edition has no unpublished dependency needed to check its authored mathematical proofs or small-board certificate.
