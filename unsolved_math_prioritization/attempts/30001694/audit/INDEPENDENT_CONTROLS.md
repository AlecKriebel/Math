# Independent controls and implementation separation

This audit's third implementation computes results before optionally importing the two historical modules for comparison. The controlling strict validator never imports either historical module.

- Admissibility: cell union-find, full cubical-complex Euler characteristic and alternating local-link exclusion. Historical implementations instead use exposed-boundary cycles or complementary-region flood fill. Cell connectivity and local corner topology are intrinsic conditions and necessarily recur.
- Boundary points: direct neighbor-absence construction of oriented exposed cell edges.
- Interior-square side: exact inclusion of every precomputed filled-block bit mask.
- Boundary squares: enumerate all 12,650 four-subsets of the 25 available lattice points, then check the six squared distances and the two maximal-distance pairs' equal midpoint and perpendicularity. Exactly 50 four-subsets pass. Filter these fixed geometric configurations by boundary membership for each polyomino. No geometric tolerance, side-pair rotation generator, diagonal-pair completion, or random sample is used.
- Full replay: all 65,535 nonempty masks, with all 9,349 original rows checked for exact maxima and both witnesses. All three admissibility predicates additionally agree at the empty mask.
- Chord surgery: direct oriented cycle extraction, both arc-plus-chord polygons, and exact integer ray casting at cell centers. All 53,072 chord occurrences are inspected. The controls check shorter cycles, subset boundary vertices, partition or nesting, and the monotonicity required by the proof.
- Symmetry: all eight dihedral images of every admitted mask; every rectangular mask; and every admitted quarter-turn-invariant mask detected from its bounding-box center.
- Rounding: exact rational arithmetic, with negative and integral parameters, floor and ceiling endpoint construction, containing-edge endpoint membership, shape, side comparison and degeneracy tracking. This is an algebraic stress test, not a finite substitute for the proof.
- Release controls: the strict validator pins exact original archive and certificate hashes and sizes, enforces a literal package inventory, rejects duplicate archive member names and duplicate JSON keys, reconstructs the complete intended CSV key set, checks exact field structure, rejects out-of-domain or duplicate masks, and checks all maxima and witnesses. The controlling checks survive python -O.

The Euler predicate is justified by planar topology: the occupied-cell union is a finite connected planar cubical complex; its Euler characteristic is one minus the number of bounded complementary components. With the diagonal nonmanifold patterns excluded, no local pinch remains. Euler characteristic one therefore leaves a single boundary component. The original two predicates were also inspected directly, rather than accepted only from finite agreement.

Reproducibility controls establish the packet's stated finite computation and detect validation blind spots. They do not establish the universal conjecture, novel mathematics, or correctness of an uninspected source.
