# Five substantive attempts on Kirby Problem 4.21

Research date: 2026-10-03. These are distinct mathematical approaches, not five repetitions of a literature search. Complete arguments and dependencies are in PROOF.md. The count does not mean the problem is exhausted.

## 1. Local-ball construction and connected-sum reduction

**Goal.** Produce the acyclic piece by removing or retaining a coordinate ball, then enlarge the positive class by connected sums.

**Work.** Proved the smoothable case, the integral-homology-4-sphere case, connected-sum closure by joining the acyclic pieces with a 1-handle, and the precise characterization of an S3 interface as a connected sum of a smoothable closed manifold with a homology sphere.

**Result.** Full proofs for these classes. In the simply-connected setting, an S3 interface forces smoothability, so the E8-manifold rules out using S3 in every successful decomposition.

**Gap.** No general connected-sum reduction exists in the argument. This does not handle every non-simply-connected manifold.

## 2. Form realization, topological capping, and classification

**Goal.** Realize the required manifold as a smooth 2-handlebody plus a contractible cap.

**Work.** Checked Freedman's construction, including unimodularity of the boundary surgery matrix, the contractible cap, van Kampen, and the change in boundary Rokhlin invariant needed to obtain both odd-form Kirby–Siebenmann types. Applied the actual simple-connectivity hypothesis rather than ordinary homology alone. Checked the separate known nonorientable star-RP4 construction in Ruberman–Stern.

**Result.** The simply-connected positive answer and a known nonorientable example, with explicit source locations.

**Gap.** Ordinary intersection-form realization does not control arbitrary fundamental groups and their equivariant forms. The star-RP4 construction does not generalize automatically.

## 3. Punctured smoothing and finite end cross-sections

**Goal.** Turn Quinn's almost-smoothness into a compact smoothable complement.

**Work.** Proved the homology and boundary-map statements for a punctured acyclic manifold, and the converse under the required linking-sphere generator condition. Compared smooth exhaustion levels with topological coordinate spheres.

**Result.** A precise sufficient missing statement: a smooth finite cross-section with end-side homology S3 and the correct local H3 generator.

**Gap.** A smooth exhaustion need not supply those homology groups or maps; the coordinate sphere need not be smooth in the punctured smoothing. Neither theorem was silently assumed.

## 4. Homology restrictions and definite cyclic-cover lattices

**Goal.** Find an obstruction that survives arbitrary acyclic pieces.

**Work.** Derived the H1/H2 and oriented H3/intersection-form restrictions from Mayer–Vietoris. Reproduced the FHMT characteristic-vector calculation: in rank 4n the vector has norm 4n−8 for n≥3, obstructing a standard positive lattice. Checked symmetry, unimodularity, positive definiteness and characteristic parity exactly for n=1,…,12. Analyzed the restrictions of cyclic covers to an acyclic piece and its homology-sphere boundary.

**Result.** A valid nonsmoothability test and an explicit reason it fails to refute the requested weaker decomposition.

**Gap.** The smooth lifted complement has boundary. Its natural acyclic caps are only topological, so closed smooth diagonalization cannot be invoked. Acyclicity does not supply smooth caps or trivial fundamental group.

## 5. Compact slice-disk obstruction and attempted closed promotion

**Goal.** Promote the known compact-with-boundary obstruction to a closed counterexample.

**Work.** Used the published FHMT knot theorem; proved the compact obstruction with two dual 2-handle attachments, all homology maps, correct gluing orientation, and the resulting slice cocore. Then computed the double's homology and performed surgery on a primitive loop in its second half, leaving the first half embedded.

**Result.** The compact counterexample embeds in a closed integral homology 4-sphere, which satisfies the desired closed decomposition by Attempt 1. This rigorously demonstrates failure of the proposed inheritance shortcut.

**Gap.** A closed decomposition may cross the chosen compact submanifold's boundary. There is no theorem here controlling every possible interface.

## Final assessment

All five approaches yield proved special cases, exact reductions, or rigorously identified failures. No general proof or closed counterexample was found. No new paper, DOI, novelty claim, or solved status is warranted by this work.
