# Fresh small-graph synthesis and source delta audit

Verdict: **PASS as a scoped partial proposition**: every finitely presented subgroup of a RAAG with at most five defining vertices has intrinsic Dehn function ≼n^18. This is not either required witness or a full negative answer to21.126. No literature-originality claim is certified.

## Current abelian-edge note

I reread the current ABELIAN_EDGE_FILLING.md in full. Its SHA matches the previous mathematical review receipt, f76ce56e929fbde43f6f95ea7c52b16a90d11d1b7c1129729587c6c84df36623. It already contains the stronger fixed-token multiplicative interval argument, block preservation, and unconditional conclusion; the earlier audit's editorial suggestion has been marked implemented. The abelian-edge mathematical verdict remains PASS. Its chordal-priority paragraph is checked below rather than treated as an unverified lead.

## Coherent-RAAG primary theorem

I inspected actual Definition9.2, its following paragraph, and Lemma9.5 in the cached arXiv2009.01899v2, printed pp40–41. Geometric coherence supplies a compact locally CAT(0) core for every covering with finitely generated fundamental group. The following paragraph explicitly concludes that finitely generated subgroups are finitely presented and CAT(0). Lemma9.5 gives geometric coherence for the Salvetti complex of a coherent RAAG. Thus the deduction for coherent/chordal RAAGs is directly supported. The chordal-to-coherent link is standard and also follows here from a finite tree-of-cliques decomposition and the already reviewed finite-generation argument for abelian vertex and edge stabilizers. The CAT(0) conclusion supplies a quadratic isoperimetric upper bound, not an assertion that a free subgroup has exact quadratic growth.

## Classification of the five remaining graphs

The independently reproduced expanded census covers29 of the34 five-vertex isomorphism classes and all smaller graphs. I checked the five exact leftover masks using the specified ten-edge ordering.

- Masks59,185,187 have the displayed perfect elimination orders. I checked every deleted vertex's remaining neighborhood is a clique. The independent script records all15 deletion checks, including the final singleton cases. Their chordal RAAGs therefore have the prior quadratic subgroup bound.
- Mask221 is exactly the union of square01,12,23,03 and triangle01,04,14 along edge01. Thus its standard RAAG presentation is precisely A(C4)*_(Z²) Z³. The separately reviewed abelian-edge lemma applies to every finitely presented subgroup, with quadratic vertex bounds and undistorted free-abelian edge groups. It gives degree5. The vertex-fixing boundary case needs only the quadratic bound.
- Mask254 has all six cross edges from independent pair{0,1} to{2,3,4}, together with edge23 and no other edges. Its group is F2×(Z²*Z). The complete product decomposition, rather than a vague similarity to two free factors, is essential.

## Limit-group argument and primary filling bound

For Z²*Z, the stated maps u↦p^k,v↦p^(k²),w↦q discriminate any finite set of nontrivial elements. After putting those elements in reduced free-product normal form, each nonzero abelian syllable has image exponent ak+bk², a nonzero polynomial because(a,b)≠(0,0). Finitely many such polynomials exclude finitely many integer k. Nonzero remaining p-powers alternate with nonzero q-powers, so there is no cross-factor cancellation. Finite-set injectivity follows by applying this to pairwise differences of distinct input elements. Thus the finitely generated group is fully residually free and is a limit group. The argument does not claim one homomorphism is injective on the entire rank-two abelian factor.

Actual Corollary4.8 of cached products2406.19860v2, printed p24, explicitly includes every finitely presented subgroup of a direct product of at most three limit groups and gives upper degree18. Hence it applies to these two limit factors. The degree9 theorem for free-factor products is not misapplied to Z²*Z. No unverified passage from fully residually free to polynomially filling arbitrary products is needed beyond this explicit theorem.

## Independent exhaustive reconciliation

`independent_small_graph_classification.py` imports only this reviewer's prior independent graph code, not the author census modules. It regenerates the expanded seed/closure grammar up to five vertices, enumerates permutation orbits by adjacent transpositions, verifies all three elimination orders and the two remaining graph decompositions, and assigns one justified bound to every orbit. All1024 labelled graphs at five vertices are accounted for:754 by the expanded class(degree9),180 by the three chordal classes(degree2),60 by the house class(degree5),30 by the two-limit-group class(degree18). There are exactly34 orbits and no unaccounted orbit. All graphs with at most four vertices belong to the earlier expanded class.

The maximum of these valid exponents is18; presentation-dependent constants may vary with the subgroup, as the proposition allows. The result bounds the number of ambient defining vertices, not the number of intrinsic subgroup generators. Embedding in an RAAG with more vertices is outside this proposition even if the subgroup is generated by five elements. These boundaries are correctly retained in the synthesis.

No substantive objection remains. The exact result is a finite ambient-class exclusion, and the original unrestricted Kourovka problem remains open within this research effort.

Audit completed 2026-10-24T21:31:36.388508+00:00.
