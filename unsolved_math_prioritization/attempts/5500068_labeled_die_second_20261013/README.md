# Labeled rolling die paths second mathematical edition

TOPP Problem 68, row 1758, identifier 5500068 / AMR-054-0068. Date: 2026-10-13.

The complexity classification of the fully labeled, hole-free rectangular rolling-die Hamiltonian-path problem remains unresolved. This second edition records an accepted exact cycle-rank algorithm and four accepted no-hole gadget statements. Across the first and second editions there are exactly **two newly documented substantive passes**; the lifetime number of earlier attempts is **unknown**. Preparing this edition and its certificates is editorial verification, not another mathematical pass.

## The exact problem

The die has fixed chirality, with reference orientation `(top,bottom,north,south,east,west)=(1,6,2,5,3,4)`. Every cell of a finite rectangle is labeled in `{1,...,6}`. The path starts at a specified corner, matches the initial top and every landed-on top, and uses every cell exactly once. There are no holes, free cells, rotations in place, excursions, revisits, or closing return. Fixed and selectable initial orientation are distinct variants.

## What is established

1. **Exact cycle-rank algorithm.** After endpoint/state conditioning and sound propagation, forced-chain contraction preserves the surviving cycle rank `k=|E|−N+1`. Every unresolved branch has a port- and full-state-tagged multigraph with at most `2k` nodes and `3k−1` optional edges. At most `2^k` affine parity candidates, each checked for exact degrees, physical chain ports, full-state agreement and selected connectedness, decide the branch in polynomial preprocessing plus `O(k 2^k)` time and polynomial decision space.
2. **Adjacent neutral detours leak endpoints.** A nontrivial fully covered neutral replacement between adjacent ports always has an alternative traversal from the same starting state that ends at the original second cell. It assigns the same full states to all cells.
3. **Exact rigid ribbons.** Every even-width rectangle of height `4r+3` with the stated periodic labels has exactly one bottom-left-rooted path, including selectable initial orientation. Width divisible by four gives neutrality for the longer horizontal displacement between the nonadjacent ports. External boundary isolation remains a condition, not an implemented reduction.
4. **Pair-copy collars obstruct coverage.** An adjacent same/opposite-pair collar beside a straight rail of at least four cells leaves two compulsory noncorner cells with phase-degree at most one in the rail's intended phase.
5. **Compatible eight-cycles force the endpoint.** Every compatible simple eight-cycle in a solution's simultaneous orientation field is a 3-by-3 perimeter and forces its center to be the final endpoint. There is at most one. The endpoint-free gadget corollary requires the gadget to contain the enclosed center as well as the ring.

The graph contraction and binary-cycle-space methods are general methods, with no novelty claim. No general bound on `k` is proved that would make this a polynomial algorithm on arbitrary rectangles. No hardness proof, global uniqueness theorem, worldwide novelty claim, or complete hole-elimination reduction is established.

## Reading the edition

- [FOUNDATIONS.md](FOUNDATIONS.md): the accepted orientation parity, unique-edge and checkerboard-area facts used here
- [CYCLE_RANK_KERNEL.md](CYCLE_RANK_KERNEL.md): full propagation, size, completeness, soundness and complexity proofs
- [NO_HOLE_GADGETS.md](NO_HOLE_GADGETS.md): complete proofs of the four gadget statements and their interface limitations
- [INDEPENDENT_MATHEMATICAL_ACCEPTANCE.md](INDEPENDENT_MATHEMATICAL_ACCEPTANCE.md): the independent mathematical proof challenge and acceptance of the underlying results
- [EXACT_AUTHORED_CERTIFICATE.json](EXACT_AUTHORED_CERTIFICATE.json) and [CERTIFICATE_GUIDE.md](CERTIFICATE_GUIDE.md): exact small authored data and program-independent validation instructions
- [VERIFICATION_SUMMARY.json](VERIFICATION_SUMMARY.json): attributed aggregate outcomes and their bounded scopes
- [SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json): prior public-source identities, retrieval metadata and date-qualified status
- [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json): file byte lengths and SHA-256 identities

The [first edition](../5500068_labeled_die_first_20261013/README.md) remains unchanged. It supplies the full earlier structural investigation, obstructions, source-model audit and independent reviews. Mathematical proofs needed by this edition are included here; the sibling links supply fuller provenance and context.

## Evidence and source limits

Arbitrary-size results rest on the complete proofs. Exact small certificates support inspection, while bounded exhaustive and regression checks establish only their stated finite outcomes. Abstract tagged multigraph examples are not claimed to be realizable die-board kernels, and no surviving ambiguous-state rectangle is asserted.

The 270-cell source regression uses the two already known witnesses of De Biasi's May 2012 Version 0.03, Figure 4. Its aggregate count is for one shared endpoint/initial/final-state branch. It is neither a count across other branches nor a newly discovered nonuniqueness construction. The edition contains no source board arrays, routes, orientation tables, copied third-party text or source documents. It also contains no software implementation; the mathematical algorithm and exact authored certificates can be checked independently from the descriptions.
