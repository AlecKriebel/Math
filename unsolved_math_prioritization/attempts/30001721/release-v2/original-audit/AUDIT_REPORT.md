# Independent adversarial audit: acyclic-quiver tree modules

Date: 2026-10-04. Problem: 30001721 / OWR-4800-012, queue rank 621.

## Decision

**Mathematical claims pass; one minor machine-readable metadata correction is required before publication.** Retain `unsolved`, five substantive approaches, no full proof, no counterexample to the original conjecture, and no novelty claim. No substantive mathematical correction was identified. This audit does not certify exhaustive literature coverage.

The audited frozen author manifest is SHA-256
`407db7c0739ad6ec9fb9417fac74cb60f35924c1e04623f0938b772d7acab070`.
All seven file hashes match it before and after the audit. Originals were not edited. `AUDIT_BINDING.json` binds the individual author files and the separate audit artifacts; `SHA256SUMS` binds the audit packet.

## Required correction C1: mislabeled cache counts

Location: `verify_tree_controls.py`, `enumerate_trees`, return value at line 121; corresponding fields in `control_results.json`.

The key `tested_basis_permutation_orbits` is assigned `len(cache)` even when `quotient=False`. Thus it reports 32 for Kronecker and 12 for D4, although these are counts of tested labelled supports. Independent Burnside counts give **8** and **6** actual basis-permutation orbits. For the affine case, where the quotient is enabled, the reported **485** is correct. The A2 value 1 happens to agree under both interpretations.

Minimum safe correction: replace the key by `algebra_cases_evaluated` in the script and regenerate the JSON. Prefer also adding `basis_permutation_quotient_used: quotient`. If retaining an orbit-count field, report it only when a quotient has actually been computed, or calculate all four actual totals separately. Do not simply replace 32/12 by 8/6 while leaving a field that purports to count the cases the original run actually evaluated.

This is a labeling defect only. All support totals, indecomposable counts, endomorphism dimensions, trace ranks, and affine orbit count pass. The narrative REPORT does not mistake these small-case cache counts for mathematical orbit totals. The frozen packet should remain unchanged; a corrected release can incorporate C1 and regenerate its own manifest.

## Independent verification method and reproducibility

The author's complete extended control script was replayed without modification. Its generated JSON is byte-identical to the frozen `control_results.json`.

The separate `independent_controls.py` never imports the author's script. Differences reduce common-mode implementation risk:

- Enumerates every labelled candidate directly, including all 8,748 affine trees; no orbit cache is used.
- Tests connectivity by breadth/depth-first reachability rather than union-find. With N vertices and N−1 edges, connectivity is equivalent to being a tree, including the parallel-edge convention.
- Builds endomorphism equations using column-major Kronecker products, rather than the author's entrywise row-major assembly.
- Uses exact rational DomainMatrix nullspaces.
- Computes the trace pairing on the faithful underlying vector space, rather than forming the author's left-regular multiplication matrices.
- Separately verifies all 32 Kronecker candidates by invertible-pencil discriminants.

The faithful-module test is valid here: for the finite-dimensional C-algebra A=End(M), its Jacobson radical acts nilpotently and lies in the kernel of (x,y)↦tr_V(xy). A semisimple complement acts faithfully on V and each matrix block occurs with positive multiplicity. In characteristic zero, the induced weighted matrix-trace pairing is nondegenerate. Consequently this pairing has rank dim(A/rad A), just as the regular trace pairing does. Rank one is equivalent to A being local. This alternate implementation shares the correct algebraic principle but not the multiplication code.

`orbit_control.py` independently counts basis-permutation orbits by Burnside's lemma on support bitmasks, rather than selecting lexicographically minimal orbit representatives.

Reproduction, Python 3 with SymPy 1.14.0:

    python independent_controls.py --output independent_results.json
    python orbit_control.py
    python ../author/verify_tree_controls.py --extended-control --output author_replay.json
    cmp author_replay.json ../author/control_results.json

The full independent labelled affine test took approximately 28 seconds in the audit environment. Timing is not part of the mathematical claim. No source documents, network, remote writes, or publication are needed for these computations.

## Exhaustive results

The independent totals exactly match the author:

- 2-Kronecker, (2,2): 32 trees, 8 indecomposable, 24 decomposable. Histogram (dim End, trace rank): (2,1):8; (2,2):16; (4,4):8.
- D4 inward three-subspace quiver, (2;1,1,1): 12 trees, 6 indecomposable, 6 decomposable. Histogram (1,1):6; (2,2):6.
- A2, (2,1): one tree, decomposable, pair (3,2).
- Affine D4 inward four-subspace quiver, (3;2,2,1,1): 8,748 trees, 96 indecomposable, 8,652 decomposable. Every indecomposable has pair (2,1).

The complete affine histogram is (2,1):96; (2,2):1728; (3,2):1776; (3,3):576; (4,3):2592; (5,3):1056; (5,4):336; (6,4):456; (7,5):54; (7,6):60; (8,4):12; (9,5):6.

Burnside orbit totals are respectively 8, 6, 1, and 485. In the affine case the acting group has order 3!·2!·2!=24, and the sum of its fixed-support counts is 11,640, giving 11,640/24=485. All count claims refer to labelled supports, or explicitly specified permutation orbits; neither is an isomorphism-class count.

Combinatorial totals are also correct: the Kronecker supports are four spanning trees of K₂,₂ with 2³ arrow colorings each; the affine position graph is K₃,₆, yielding 3⁵6²=8,748. D4 gives 3·2²=12.

## Affine-D4 witness, coefficients, roots and local algebra

The four matrices in REPORT are exactly the stored witness. Their nonzero-entry counts are 3,2,2,1, totaling eight edges on nine basis vertices. Their graph is connected. All four maps are injective.

Directly preserving the image planes and lines gives the center endomorphism aI+zE₃₁. At the four leaves its blocks are aI₂+zE₂₁, aI₂+zE₂₁, a, a. Thus the whole-quiver nilpotent generator is

    N = (E31, E21, E21, 0, 0),    N² = 0,    N ≠ 0.

The independent equation solver gives End dimension two and trace rank one. The exhibited identity and N are independent, so they are a complete basis, and End=C[ε]/(ε²). The only idempotents are 0 and 1; indecomposability is therefore proved. The nonzero nilpotent rules out the Schur property of this representative.

The dimension vector has q(d)=9+4+4+1+1−3(2+2+1+1)=1. More importantly, real-root status is independently certified by the complete reflection sequence:

    (3;2,2,1,1) → (3;1,2,1,1) → (3;1,1,1,1)
    → (1;1,1,1,1) → (1;0,1,1,1) → (1;0,0,1,1)
    → (1;0,0,0,1) → (1;0,0,0,0).

Hence the report does not rely on an unjustified implication from q=1 alone. The intermediate center reflection is unavailable as a BGP sink/source reflection for the orientation reached after the first two leaf reflections.

The report also proves that the dimension vector itself is non-Schur, not merely that one representative has nonscalar endomorphisms. The indicated generic configuration splits V₀=L⊕U, where L is the plane intersection and U spans the two image lines. This supplies a nontrivial idempotent on a nonempty open set. A scalar-endomorphism representation anywhere would create another nonempty open set by upper semicontinuity of kernel dimension, contradicting irreducibility of the representation space. This argument is sound.

## Audit of the five approaches and countercontrols

1. **Reflections.** Lattice reflections and BGP functors have different domains. A sequence of BGP equivalences beginning at a simple representation preserves the endomorphism ring and cannot produce the demonstrated non-Schur module. The exceptional-tree theorem does not remove this obstruction. It is correct to retain real non-Schur roots among the cases needing separate constructions.

2. **Covering/thin construction.** For dimensions zero or one, a spanning tree of the connected support gives a scalar endomorphism ring. The D4 example with columns e₁,e₂,e₁+e₂ has a coefficient tree and End=C. Since the underlying base graph is already a tree, a connected universal-cover component is the same graph, so a thin lift cannot supply center dimension two. This refutes the proposed cover-thin method, not tree existence.

3. **One-edge gluing.** Under both Hom-orthogonality assumptions and the Schur hypotheses, the nonsplit extension has End=C: endomorphisms preserve X, their induced scalars agree on the nonzero extension class, and the remainder factors through Hom(Y,X)=0. If a representative cocycle has one cross coefficient, the graph joins the two trees by one edge. The existence of such decompositions and cocycles for all roots is not established. The packet explicitly states this gap.

4. **Connectivity and specialization.** The connected coefficient tree (A,B)=([[1,1],[1,0]],0) is decomposable, since A is invertible and the representation becomes (I₂,0). Independently, End has dimension and trace rank four. The family (I₂,tJ₂) has local two-dimensional End for nonzero t and matrix End at t=0. Thus an arrow-scaling limit can lose indecomposability. Stable representations are Schur by the stated kernel/image argument. None of these controls is a counterexample to the original existence problem.

5. **Finite exhaustive reformulation.** Diagonal basis scaling normalizes every nonzero tree edge to one because a tree has unique paths and no compatibility cycle. Choosing all N−1 coefficient positions and retaining connected multigraphs therefore captures every tree module up to isomorphism, with redundancy. Exact rational endomorphism equations remain exact after scalar extension to C. The regular-trace radical criterion used by the author is valid in characteristic zero, and its local-algebra/indecomposable equivalence is correct. The nonzero single-vertex case is properly addressed; the zero representation is excluded. No fixed finite enumeration proves the universal all-roots assertion.

The Kronecker positive family (Iₙ,Jₙ(0)) has a path coefficient graph and End=C[t]/(tⁿ); this is a correct general control. The 2×2 pencil test succeeds for all 32 enumerated supports and agrees with the independent trace test. It is not assumed for arbitrary singular pencils.

## Primary statement and literature

`literature_review.md` supplies the separate sourced review. The OWR existence question, complex field and no-oriented-cycle assumptions match the target. The adjacent stronger multiplicity question is correctly kept separate. Ringel's result is about exceptional modules. Weist's verified theorems cover Schur and isotropic roots; his explicit real non-Schur obstruction rules out an all-real exceptional inference. The later covering, Kac-count and normal-form results retain hypotheses or stated open questions and are not universal solutions.

Independent current searches through October 4, 2026 found no all-roots resolution. Related 2024–2026 primary papers were screened by scope, including the September 2026 tree-brick automata paper; none asserts the missing result. These last checks are abstract-level and bounded. The report's conservative literature qualification should remain.

## Optional improvements, not release blockers

- Keep the affine witness as a named standalone script control, rather than relying only on its occurrence in the exhaustive output. The independent audit does so.
- Add the independently computed Burnside counts if retaining orbit metadata, with the group explicitly restricted to basis permutations at fixed vertices and fixed arrows.
- Record the current related-paper check in SOURCES if updating the bibliography, without claiming comprehensive coverage.

There is no basis here for a full-solution claim or for changing the original problem to `already_solved`. After C1, the packet is suitable as a conservative, reproducible five-approach unsuccessful investigation with valid auxiliary results.
