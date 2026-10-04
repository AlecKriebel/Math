# Kirby Problem 4.119: audited-candidate partial analysis, not a solution

## Exact target and verdict

Catalogue ID 2995, KP-4.119, asks: **Is every topological 4-manifold homeomorphic to a CW complex?** The target is homeomorphism of underlying spaces, not homotopy equivalence. A CW structure need not be regular. We use the usual Hausdorff, second-countable manifold convention. The obstruction examples below are closed, connected, oriented, simply connected manifolds, so do not depend on whether the full question also permits boundary. The unrestricted target remains **unsolved** in this investigation; no counterexample to an arbitrary CW structure is proved.

The K3 preliminary volume, Problem 4.119, printed pp. 289–290, is the exact source [K3]. Smoothable manifolds, and each connected noncompact topological 4-manifold, have CW structures. The finite-homotopy-type theorem is weaker than the target. These known positive cases do not close the compact nonsmoothable case. No newly discovered theorem is claimed.

## 1. Compactness and the homotopy-model approach

**Lemma 1 (compact subsets see finitely many cells).** A compact subset A of a CW complex X meets only finitely many open cells. Consequently a compact space carrying a CW structure carries a finite CW structure.

**Proof.** If A met infinitely many cells, select points x_i in pairwise distinct open cells. Let S be their set. Closure-finiteness says that each closed cell meets only finitely many open cells, hence meets S in a finite set. For every T contained in S, the inverse image of T under each characteristic map is closed: it is the inverse image of a finite set in the Hausdorff space X. The weak topology therefore makes every T closed in X. Thus S is a closed discrete subspace of A, and is compact because A is compact. An infinite discrete space is not compact, a contradiction. Apply this to A=X. QED.

Known existence of a finite CW complex K homotopy equivalent to a compact manifold M [FNOP, Theorem 3.16] removes homological finiteness as a candidate obstruction. It supplies neither an injective map K to M nor characteristic maps for cells in M.

**Explicit failure of this implication for a supplied model.** The finite CW complex K=S^4 union_p [0,1], attaching the interval at its endpoint 0 to p, deformation retracts onto S^4. Nevertheless K is not a 4-manifold: an interior point of the appended interval has an open interval neighborhood. Its local homology is Z in degree 1 and zero in degree 4; an interior point of a 4-manifold has the opposite nonzero degree. This does not assert that S^4 lacks another CW model homeomorphic to itself. It shows exactly why a homotopy equivalence of a supplied finite model cannot be promoted to a homeomorphism.

**Approach 1 gap.** Construct a finite cellular partition of the actual manifold and the requisite characteristic maps, or prove an obstruction to every such partition. Algebraic finiteness and simple homotopy type alone do neither.

## 2. Regular CW decompositions and triangulation

**Lemma 2.** A finite regular CW complex is homeomorphic to a finite simplicial complex.

**Proof.** Induct on the skeleton. Triangulate the zero-skeleton. For each successive closed cell, its boundary is a subcomplex already triangulated and is homeomorphic to a sphere. Cone that boundary triangulation from a new vertex. The boundary homeomorphism extends across the corresponding topological balls by coning a chosen spherical parametrization. Glue this extension to the already constructed homeomorphism on the lower skeleton. Distinct cells have disjoint interiors and meet along lower cells, so the maps agree on intersections. The resulting continuous bijection between compact Hausdorff spaces is a homeomorphism. There are finitely many cells, so the resulting triangulation is finite. QED.

For closed 4-manifolds, triangulability implies a PL structure, and a PL structure implies smoothability [FNOP, Proposition 3.11 and Theorem 3.5]. Thus any nonsmoothable closed 4-manifold has no finite regular CW structure.

For a concrete example, let E be Freedman's closed simply connected oriented manifold with positive definite E8 intersection form. Its existence is classical [Fre; also B et al., Theorem 2.1]. Donaldson's definite-form theorem rules out a smooth structure [Don]: E8 is even and positive definite, whereas the standard positive diagonal form is odd. Hence E has no regular CW structure, by Lemmas 1–2. This is a negative result for a strictly stronger target.

**Approach 2 gap.** An arbitrary CW characteristic map can identify boundary points. No valid regularization theorem for CW 4-manifolds was obtained. Assuming regularity here would assume the central missing implication. The fact that a manifold has nonregular CW decompositions is already visible for S^4 with one 0-cell and one 4-cell.

## 3. Puncturing, triangulating, and compactifying

Let M be a closed connected 4-manifold and p in M. The punctured manifold M minus p is smoothable [FNOP, Theorem 9.1], hence triangulable.

**Lemma 3 (the old cells cannot simply be retained).** No infinite CW decomposition of M minus p can be extended to a CW decomposition of M merely by retaining all its open cells and adding p as a 0-cell.

**Proof.** Such an extension would be an infinite CW decomposition of a compact space, contradicting Lemma 1. A triangulation of M minus p is necessarily infinite: a finite simplicial complex is compact whereas M minus p is not. QED.

For a locally finite triangulation the failure is visible in the zero-skeleton. Infinitely many vertices have no accumulation in M minus p, by local finiteness and compactness of compact subsets. In the compact metrizable space M they have a subsequence converging to p. After adding p, the proposed zero-skeleton is not discrete, whereas every CW zero-skeleton is discrete.

**Lemma 4 (a smooth product end would smooth the compactification).** Suppose a smoothing of M minus p has a cofinal end neighborhood diffeomorphic to S^3 times [0,infinity), with compact complement and smooth boundary at S^3 times {0}. Then M is smoothable.

**Proof.** Truncate the product end to obtain a compact smooth manifold N with boundary the standard smooth S^3. Cap it by a standard smooth 4-ball using the end parametrization. The resulting smooth manifold is topologically the one-point compactification of M minus p: radially compactifying the S^3-product end adds a ball about the missing point. One-point compactification is unique for a locally compact noncompact Hausdorff space. Therefore this smooth manifold is homeomorphic to M. QED.

In particular, no smoothing of E minus p has such a product end. Its end is topologically standard; the obstruction here is to the stated smooth product condition, not to the topology of the end.

**Approach 3 gap.** A successful compactification must replace infinitely many old cells by a finite nonregular arrangement, with globally continuous attaching maps at the missing point. Neither punctured smoothing nor end homology gives this arrangement.

## 4. Finite Kirby encodings and the contractible-cap approach

Bastl et al. [B et al., Definition 3.5 and Theorem 3.6] represent every closed oriented simply connected topological 4-manifold as W union_Y C, where W is a smooth 0/2-handlebody, Y is an integral homology 3-sphere, and C is a compact contractible topological 4-manifold with boundary Y. This is a finite encoding, not a handle decomposition or CW decomposition of the entire manifold.

**Lemma 5 (a genuine gluing sufficient condition).** Suppose W and C have finite CW structures for which Y is a subcomplex on each side, and the gluing homeomorphism is cellular in both directions. Then W union_Y C has a finite CW structure.

**Proof.** Identify the cells in the common boundary and retain the remaining cells on both sides. Cellular compatibility puts the boundary of each n-cell in the resulting (n-1)-skeleton. The characteristic maps remain homeomorphisms on interiors. Their finite disjoint union is a quotient map onto the glued space: it is a continuous surjection from a compact space to the Hausdorff manifold W union_Y C. This proves the weak topology, and finiteness proves closure-finiteness. QED.

This condition is not supplied by the fact that C is contractible. Contractibility gives the homotopy type of a point, not a CW decomposition of the actual C or of the pair (C,Y).

**Lemma 6 (the cone is the wrong cap).** Let Y be a closed connected 3-manifold with nontrivial fundamental group. Its cone cY is not a topological 4-manifold at its cone vertex, even if Y is an integral homology sphere.

**Proof.** The punctured conical neighborhoods U_epsilon minus vertex retract to Y, and inclusions between any two such neighborhoods induce isomorphisms on fundamental groups. If the vertex had a Euclidean 4-ball neighborhood B, choose U_delta contained in B contained in U_epsilon. The induced isomorphism pi_1(Y) to pi_1(Y) would factor through pi_1(B minus vertex)=0. This contradicts pi_1(Y) nontrivial. QED.

Thus replacing C by the finite CW cone cY preserves contractibility but need not preserve local manifold structure or the homeomorphism type after gluing. The failure persists despite correct local homology when Y is a homology sphere.

**Approach 4 gap.** Produce compatible finite CW structures on the actual topological cap and its boundary, or a different finite cellular construction of the glued manifold. A finite link description and an algorithm comparing manifold encodings do not provide those structures. This route only addresses simply connected closed manifolds even if its cap gap is repaired.

## 5. Stable smoothing and handle cancellation

A classical stable-smoothing theorem gives a smooth M # k(S^2 times S^2) for some k whenever a compact connected 4-manifold M has vanishing Kirby–Siebenmann invariant [FNOP, Theorem 9.9; attributed there to Freedman–Quinn]. One might try to triangulate this stabilization and then cancel the added summands.

**Proposition 7 (smooth/PL cancellation cannot be automatic).** There is a closed simply connected oriented topological 4-manifold F with ks(F)=0 which becomes smooth after enough S^2 times S^2 stabilizations but is itself nonsmoothable.

**Proof.** Let F=E#E. Its intersection form is E8 direct-sum E8, even, positive definite, unimodular, and of signature 16. For an even form Freedman's classification gives ks(F)=signature(F)/8 mod 2=0 [Fre; B et al., Theorem 2.1]. Thus stable smoothing applies. Were F smooth, Donaldson's theorem would force its form to be the positive diagonal identity form, which is odd. Evenness is invariant under integral change of basis, contradiction. QED.

This is also a direct refutation of the assertion that vanishing Kirby–Siebenmann invariant alone implies smoothability in dimension four. The exact matrix checks below verify parity, definiteness and unimodularity, but do not computationally prove Freedman's, Donaldson's, or the smoothing theorem.

Any cancellation procedure which stays within smooth or PL handle structures cannot recover F, because those structures would smooth F. It could still be possible to cancel topologically into nonregular CW cells; this investigation provides no obstruction to that weaker possibility. For E itself, the invariant remains 1 under S^2 times S^2 stabilization, so even the stated stable-smoothing premise fails.

**Approach 5 gap.** Supply a topological descent procedure for finite CW structures under the requisite destabilization, permitting nonregular attaching maps and proving the weak topology. Smooth/PL cancellation is too strong; algebraic removal of hyperbolic summands alone is not such a procedure.

## Exact status

Five distinct approaches were investigated. Their partial statements concern compactness, regular structures, fixed punctured decompositions, controlled smooth ends, compatible gluing, singular cone caps, and smooth stabilization. None settles the existence of an arbitrary finite CW structure on E, F, or on all compact topological 4-manifolds. Status: **unsolved, 5/5 substantive approaches**. Discovery completion estimate: **0% of the missing general homeomorphism proof**, despite completing this bounded investigation. These estimates are bookkeeping, not probabilities.

## References and checked theorem locators

- [K3] R. I. Baykur, R. C. Kirby, D. Ruberman (eds.), K3: A New Problem List in Low-Dimensional Topology, AMS 2026, preliminary author PDF, Problem 4.119, pp. 289–290. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [FNOP] S. Friedl, M. Nagel, P. Orson, M. Powell, A survey of the foundations of four-manifold theory in the topological category, arXiv:1910.07372v3, 2 January 2024. Questions 3.14–3.15; Theorems 3.5, 3.16, 9.1, 9.9; Proposition 3.11. https://arxiv.org/abs/1910.07372v3
- [B et al.] S. Bastl et al., Algorithms in 4-manifold topology, arXiv:2411.08775v2, 28 September 2025, Section 1.1, Theorem 2.1, Definition 3.5, Theorem 3.6. https://arxiv.org/abs/2411.08775v2
- [Fre] M. H. Freedman, The topology of four-dimensional manifolds, J. Differential Geometry 17 (1982), 357–453. https://doi.org/10.4310/jdg/1214437136 . Classification is invoked as an established theorem, with precise formulation checked in [B et al.]; its full proof is not reproduced or reverified here.
- [Don] S. K. Donaldson, An application of gauge theory to four-dimensional topology, J. Differential Geometry 18 (1983), 279–315. https://doi.org/10.4310/jdg/1214437665 . The definite-form statement and E8 direct-sum E8 application were cross-checked in C. Manolescu's author survey, Theorem 3.4: https://web.stanford.edu/~cm5/4D.pdf . No reproof of gauge theory is claimed.
