# Turn 3: reduction to prime hyperbolic branch links

**2676 / KP-1.17. Author turn 3/5, scoped classical-consequence reduction. The original problem is unresolved.**

## 1. Result and distinction between the two geometries

Using classical prime decomposition and the source-checked Boyer–Gordon–Hu results, this turn proves:

**Reduction theorem.** If KP-1.17 has a mixed alternating/non-alternating pair of links, it has such a pair in which both links are nontrivial, nonsplit, prime and have hyperbolic exteriors. Their common double branched cover is an irreducible rational homology sphere and an L-space.

This says that the **link exteriors** are hyperbolic. It does not assert that their closed common branched cover is hyperbolic. For example, a hyperbolic Montesinos link can have a Seifert-fibered double cover. The finite isometry-group arguments of Turn 1 apply only when the cover itself is hyperbolic.

The reduction is not claimed new. It combines credited results, with elementary graph calculations supplying the small-determinant exception check. It does not equate the existence of an L-space cover with alternation.

## 2. Removing split and connected-sum factors

The relevant classical input is recorded with proof in Hedden–Ni, `Manifolds with small Heegaard Floer ranks`, Proposition 5.1 (complete arXiv:0906.4771 reading copy, pp.15–16): branched double covers respect connected sums; a split union introduces an additional S^1×S^2 summand; the cover of a nonsplit prime link is irreducible; and the cover of a nonsplit link has no S^1×S^2 summand. The proof uses the equivariant sphere theorem. It is not legitimate merely to infer primeness of a branch set from nonequivariant homology.

Every link can be decomposed by splitting spheres and by spheres meeting it in two points into nonsplit prime factors, ignoring trivial connected-sum unknot factors. We need no uniqueness theorem for this **link** factorization. Kneser–Milnor uniqueness for the resulting **three-manifold** factors is sufficient.

An alternating link has a factorization of this kind all of whose factors are alternating. Indeed, Menasco's 1984 Theorem 1 makes splitting and connected-sum decompositions visible in a reduced alternating diagram. Cutting along such a diagrammatic decomposition preserves alternation and decreases the diagram complexity until the nonsplit factors are prime. Conversely, split union and componentwise connected sum of alternating diagrams preserve alternation.

Now let A be alternating, B non-alternating, with Sigma(A) homeomorphic to Sigma(B). Choose the displayed all-alternating prime decomposition of A and any prime decomposition of B. At least one prime nonsplit factor B_0 of B is non-alternating: otherwise the original B would be assembled from alternating diagrams and would be alternating.

Sigma(B_0) is irreducible. It cannot be S^3. One way to use the classical unknot-detection fact here is Dinkelbach–Leeb's Theorem E: a smooth involution of S^3 is conjugate to an orthogonal one. An orientation-preserving nontrivial involution with nonempty one-dimensional fixed set then has an unknotted fixed circle, and its quotient branch link is the unknot. It also cannot be S^1×S^2, since that manifold is not irreducible.

Consequently Sigma(B_0) is a genuine non-S^3 irreducible factor in the common cover. Three-manifold prime-decomposition uniqueness matches it with Sigma(A_0) for one of the nonsplit prime alternating factors of A. S^1×S^2 factors introduced by split unions cannot absorb it. If an orientation reversal occurs, mirror A_0 as necessary; alternation is preserved. We have obtained a mixed pair A_0,B_0 with irreducible common cover.

Because A_0 is nonsplit alternating, its cover has finite first homology and is an L-space, by Ozsvath–Szabo's branched-cover theorem. This supplies the additional properties claimed in the reduction theorem.

## 3. A small-determinant graph lemma

We will need to know which alternating covers can have homology order at most four. The following proof applies to links, including the connected-sum possibility, without importing a knot-only crossing bound.

**Lemma.** For every finite connected loopless bridgeless multigraph G with at least one edge,

    number of spanning trees tau(G) >= number of edges |E(G)|.

**Proof.** First suppose G is one vertex-biconnected block. It has an open-ear decomposition beginning with a cycle; a pair of parallel edges counts as a two-edge cycle, and an added edge counts as an ear of length one. This elementary decomposition is obtained by extending a cycle through unused edges and vertices, using the absence of a cut vertex to ensure two distinct old endpoints.

Suppose an ear with ell edges and ell-1 new interior vertices is added to H. Every spanning tree of H extends in ell distinct ways by deleting one of the ear's edges. There is at least one additional spanning tree containing the entire ear: add the whole ear to an old tree, then delete an old edge from the path between the two endpoints. Hence

    tau(H plus ear) >= ell*tau(H)+1 >= tau(H)+ell,

since `(ell-1)(tau(H)-1)>=0`. A cycle starts with equality tau=|E|, so induction proves the bound for a block.

For general G, its blocks have no bridges and at least two edges. A spanning tree of G is exactly a choice of a spanning tree in each block. Thus tau(G) is the product of the block tree counts. If their edge numbers are e_i>=2, their product is at least their sum (when there is one block this is equality). This proves the result. ∎

For a connected reduced alternating diagram, its Tait graph is connected, loopless and bridgeless, and the link determinant equals tau(G). Thus determinant at most four implies a diagram with at most four crossings. The complete graph possibilities are easily listed. Up to abstract graph isomorphism the nonempty ones with tau<=4 are:

- two vertices joined by 2, 3 or 4 parallel edges
- a 3-cycle or a 4-cycle
- two 2-edge cycles meeting in one vertex

Here is a direct check of completeness once the edge bound is known. Minimum degree is at least two. With four vertices and at most four edges one gets the 4-cycle. With three vertices, three edges give the triangle; four edges give either the two digons or a triangle with one doubled edge, and the latter has five spanning trees and is excluded. With two vertices the graph is parallel edges. There are no further nonempty cases.

The corresponding alternating diagrams are the (2,m)-torus links for m=2,3,4, up to mirror and planar duality, and a connected sum of two Hopf links. An empty connected diagram is the unknot. Their covers are respectively lens spaces of order m, RP^3#RP^3, and S^3. Equivalently, the cycle graph has a chain Goeritz form with diagonal entries 2, while the parallel-edge graph has form [m]; these give the standard lens-space surgery descriptions. The two-digon cut vertex is a diagrammatic connected sum.

**Consequence.** An alternating link whose cover has finite first homology of order at most four has cover S^3, a lens space, or RP^3#RP^3. In particular its cover cannot have a noncyclic finite fundamental group. For a prime nonsplit alternating link, the connected-sum alternative does not occur.

## 4. Excluding Seifert branch exteriors with the exact 2025 hypothesis

Boyer–Gordon–Hu's `Cyclic branched covers of Seifert links and properties related to the ADE link conjecture`, Theorem 1.1, applies to a **prime Seifert link that is not an ADE link as an unoriented link**. It proves that every cyclic branched cover is a non-L-space. No fiberedness or strong-quasipositivity assumption is required in this theorem; those occur in other statements in the same paper. The published article is JLMS 111 (2025), e70178. The complete arXiv v1 reading copy is dated February 2024, and its theorem has been checked against the publisher's indexed statement.

Apply this to the non-alternating prime B_0 above. Its double cover is an L-space, so if its exterior were Seifert-fibered, B_0 would have to be ADE up to orientation and mirror. The A_m links are (2,m+1)-torus links and are alternating, which already excludes them.

For the remaining D_m and E_6,E_7,E_8 links, the two-fold covers have finite noncyclic fundamental groups: binary dihedral, binary tetrahedral, binary octahedral and binary icosahedral respectively. This is the geometric group statement in the paper's Proposition 2.1. Their homology orders are at most four, as can be checked independently without trusting a numerical table:

- D_m: order 4 for every m>=4
- E_6: order 3
- E_7: order 2
- E_8: order 1

For example, the canonical Hopf-band plumbing has symmetrized Seifert form equal, up to basis signs, to the Cartan matrix of the associated tree, and the stated numbers are its determinants. The D_m number also follows directly from the three-strand pretzel Goeritz determinant for P(-2,2,m-2): its absolute value is `|-4-2(m-2)+2(m-2)|=4`. These determinant computations are independent of component orientations at the double-cover level.

Section 3 now rules out an alternating link with any of these covers: the finite noncyclic fundamental group cannot be that of S^3 or a lens space, and RP^3#RP^3 has infinite fundamental group. Therefore B_0 cannot have a Seifert exterior.

**Edition-specific numerical caveat.** The arXiv v1 p.8 table prints order 2 for odd D_m. That specific entry is not used. The independent Cartan and pretzel computations give 4 for all m. The binary-dihedral presentation also has abelianization of order 4: it is C4 for odd rotation parameter and C2×C2 for even parameter. The printed entry was visually checked; the published PDF was not accessible in this environment, so this note is confined to the verified v1 entry. The argument only needs the bound <=4, which holds with the independently computed value.

## 5. Excluding toroidal branch exteriors at degree two

The relevant original result is Boyer–Gordon–Hu, `Slope detection and toroidal 3-manifolds`, arXiv:2106.14378v5, 13 April 2026, Theorem 2.13 on p.10. It states that if L is a prime toroidal link in an integer homology sphere with irreducible exterior, its **double** branched cover is not an L-space. Its broader degree statement includes powers of two and three times powers of two. The proof is in Section 10.5, pp.58–59. The article is listed by the author as published in Advances in Mathematics 495 (2026), 110956.

All hypotheses apply to a nontrivial nonsplit prime link in S^3 whose exterior contains an essential torus. Hence B_0 cannot be toroidal, because its cover is the L-space Sigma(A_0). The same reasoning rules out a toroidal exterior for A_0, although Menasco already gives that case.

This uses the **proved non-L-space assertion at n=2**, not the general L-space conjecture and not the still-conjectural all-degrees toroidal statement. The distinctions between satellite and general toroidal links, and between degree two and arbitrary cyclic degree, are material; the exact Theorem 2.13 closes the degree-two case needed here.

## 6. Completion of the reduction and the remaining target

A nontrivial nonsplit prime link exterior in S^3 has incompressible torus boundary. After excluding Seifert and toroidal cases, geometrization makes it hyperbolic. Thus B_0 has hyperbolic exterior.

For A_0, Menasco gives hyperbolicity unless it is a (2,m)-torus link. The latter has a lens-space cover. Hodgson–Rubinstein's lens-space branched-cover classification, Corollary 4.12, says that any branch link with a lens-space double cover is two-bridge, hence alternating. This contradicts B_0's choice. The precise lens-space consequence is also explicitly recorded in Greene's 2011 follow-up questions and in Mecchia–Reni's 2002 introduction; the full 1985 chapter has not been recovered locally and is not represented as a directly read PDF. Therefore A_0 also has hyperbolic exterior, proving the reduction theorem.

A useful additional classical consequence of the same factor argument is that a manifold all of whose irreducible summands are lens spaces, together with any number of S^1×S^2 summands, cannot support a mixed pair. All its prime branch factors are two-bridge or trivial; their split and connected sums are alternating. This is a known-result consequence, not a new lens-space classification.

The main obstacle survives: two hyperbolic link exteriors can produce the same closed branched cover through different branching involutions. L-space data do not determine the branch link's alternation, and the common closed cover may still be Seifert-fibered or toroidal. No actual mixed pair or theorem transporting alternation between all such involutions has been constructed.

Two substantive turns remain. No full solution, general equivariant extension theorem, or novelty claim follows from this reduction.
