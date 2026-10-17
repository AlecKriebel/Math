# Independent acceptance: ambient block refinement

Problem 30003527 / OWR-15575-006, queue row 1767. Audited 13 October 2026 as supporting verification within the shared pass 4/5 investigation. This is not a further substantive problem-solving pass.

## Verdict and exact input

**ACCEPTED as three partial results.** The complementary-component bound, the stationary Hawaiian-earring realization, and the finite-component block refinement are valid. The modified surface argument genuinely avoids a finite-rank hypothesis on first cohomology and genuinely lifts to isolating blocks. No essential mathematical gap was found.

This acceptance does not establish movability for all isolated invariant compacta, or the original invariant-enlargement assertion. It does not claim novelty or a comprehensive literature result.

Audited input: `AMBIENT_BLOCK_REFINEMENT.md`, 13,237 bytes, SHA-256 `f1632f10df477bf10fbb79dea753ad5716154ed9697810e2d8b4c6e33c3b380d`. The file was read in full, and its hash was checked before and after the audit. The audited file was not edited. No remote mutation was made. This report contains authored verification, public bibliographic links, and verification metadata, with no copied source document or private coordination material.

## 1. Complementary-component bound

Let K be nonempty. A component of its complement is invariant under every time map: the full orbit is a connected path in the complement, because hitting K at any finite time would put its initial point in K by invertibility. The argument does not require components of K to be finite, and does not confuse connectedness of the complement with connectedness of K.

If a complementary component were contained in the compact isolating neighborhood N, every one of its points would have a full orbit in N. Thus each bounded complementary component reaches outside N. Its boundary is nonempty and contained in K, so it also has points at distance less than the chosen positive delta from K. Being an open connected subset of Euclidean space, it is path connected; a path between these two points contains a point at distance exactly delta.

An open ball of radius delta/2 centered there lies in the same complementary component. Different components give disjoint balls. All bounded components lie within the ball containing K: the exterior of that ball is connected and disjoint from K, so any component reaching it is the unique unbounded component. Consequently every selected ball is within the stated enlarged ball. The volume bound can be applied to every finite collection, so there cannot be infinitely many components; countability need not be assumed in advance.

Adding the point at infinity leaves the component count unchanged. Alexander duality gives the claimed finite-rank free integral second Cech cohomology. For K empty the result is immediate and the distance construction is unnecessary. The same argument in dimension at least two is valid.

## 2. Infinite first cohomology is realized

The distance function is 1-Lipschitz, as is truncation at 1; multiplying by the constant vertical unit vector preserves that bound. The resulting bounded globally Lipschitz field has a unique complete flow. Its zero set is exactly C.

For fixed horizontal coordinates a, compactness of C gives two cases. If a is outside the planar copy of C, its planar distance from C is positive and the scalar vertical speed has a positive lower bound. Its full orbit is the entire vertical line. If a belongs to C, the scalar speed is min(1,|z|). The origin on that fiber is stationary and each nonzero full orbit is one of the two half-lines. Uniqueness excludes crossing or reaching zero in finite time. Each nonstationary full orbit is unbounded in at least one time direction. Therefore no such orbit can be contained in a compact neighborhood, proving Inv(N)=C for every compact neighborhood N of C.

For the Hawaiian earring, the collapse to the first m circles is continuous, including at the common point, because the diameters of the omitted circles tend to zero. Compatible inverse-limit coordinates either all equal the common point or, at the first non-basepoint coordinate, determine one particular circle and a point on it which all subsequent coordinates retain. This verifies the claimed inverse-limit identification.

The finite-bouquet sequence is a polyhedral shape expansion. On integral first cohomology its bonding maps induce coordinate inclusions, yielding a direct sum of countably many copies of Z, not a product. The inclusion of the first m circles into any later bouquet is a section of the corresponding collapse. Taking j=m in the inverse-system movability criterion verifies movability. No inference from cohomology alone is used.

The planar Cantor-set observation is also sound: the same field isolates it, while arbitrarily large finite clopen partitions give infinite-dimensional degree-zero Cech cohomology over a field.

## 3. Finite relative rank is the correct resource

Write M=S minus L. Surface duality transfers the lemma's assumptions to H2(M,partial S;F2)=0 and finite dimension r of H1(M,partial S;F2).

A relative singular 1-cycle has compact support. Inside a triangulated surface neighborhood of this support, subdivision and mod-2 smoothing produce a finite disjoint union of embedded circles and arcs with endpoints on the boundary. This requires no triangulation of L, no local connectedness of L, and no global finite triangulation of M. At least one constituent has nonzero relative class.

There are precisely three cases:

1. A nonzero constituent which is already a proper arc can be cut directly.
2. For a closed constituent in a component meeting partial S, choose a path from partial S to the curve and truncate it at its first intersection. A simple perturbation gives a compact embedded corridor, disjoint from L and from the rest of the curve. Remove a tiny segment of the curve at the corridor attachment and run back to the boundary along two parallel corridor sides. This produces an embedded proper arc. The old circle and the new arc differ by the boundary of the corridor together with a short boundary segment; hence their relative mod-2 classes agree.
3. If the curve's component does not meet partial S, remove a small interior disk disjoint from the curve. Removing such a disk from a connected surface leaves it connected: paths crossing the disk can be detoured around its boundary. The curve's component therefore now meets the new boundary circle, and case 2 applies.

All supports used here are compact and disjoint from L, so each can be thickened a positive amount without hitting L. The corridor construction does not assume a closed curve is already a proper arc.

## 4. Exact-sequence audit, including infinite relative H0

For an interior disk D, its relative contribution is H0(D;F2)=F2, with all positive-degree groups zero. The cut sequence gives an isomorphism on relative H2 and the segment

0 -> H1(M,partial S) -> H1(M minus Int D,partial S union partial D) -> F2 -> H0(M,partial S).

The last map sends 1 to the basis vector of the chosen component. It is injective exactly because that component had not met partial S. Therefore the two relative H1 groups are isomorphic. No subtraction of infinite dimensions and no claim that relative H0 vanishes is involved.

For a strip T around a proper arc, T meets partial S in two disjoint short sides. Thus H1(T,T intersection partial S;F2)=F2, while its H2 and H0 vanish. The relevant sequence is

0 -> H2(M,partial S) -> H2(M',partial S') -> F2 -> H1(M,partial S) -> H1(M',partial S') -> 0.

The F2 generator maps to the chosen nonzero arc class, so that arrow is injective. Relative H2 remains zero and relative H1 decreases by exactly one. Relative H0 is unaffected by a strip; it may remain infinitely generated.

After exactly r strips and at most r disk removals, relative H1 and H2 have the required values. The desired degree-zero and degree-one relative cohomology vanish by duality. This is the essential modification: an internal component is punctured only when a selected nonzero 1-class requires it. No finite number of all internal complementary components is assumed.

## 5. Actual flow blocks and the primary-source dependency

The source was inspected directly, including its proofs, rather than inferred from its finite-cohomology handle theorem: J. J. Sanchez-Gabites, *Using an invariant knot of a flow to find additional invariant structure*, [arXiv:2403.18805v1](https://arxiv.org/html/2403.18805v1). Definition 6 and Section 5.4 supply tame blocks and their neighborhood-basis property. Proposition 5(iii) identifies relative block and entry-pair cohomology. Propositions 11 and 12 realize the two local cuts, preserving the invariant set and the entry trace up to pair homeomorphism. Proposition 30 supplies the cut sequence; its proof needs no rank bounds. The Appendix's circle-to-arc construction uses only the selected component's access to boundary. In contrast, Theorems 10 and 13 assume finite cohomology; those theorems are not being reapplied with their hypotheses removed. The [arXiv record](https://arxiv.org/abs/2403.18805) listed v1, submitted 27 March 2024, at inspection. This audit does not infer journal publication status from that record.

For the proposed application, finite-component K has H0(K;F2)=F2^c. Starting with a finite-type block N, delete only components disjoint from K. Then H0(N)->H0(K) is injective. The long exact sequence gives H0(N,K)=0 and a finite-dimensional H1(N,K), with dimension at most c + dim H1(N). No term involving H1(K) is needed for this upper bound.

The entry surface is orientable as a subsurface of the oriented boundary of N, and its trace lies in its interior. The relative-pair isomorphism thus puts it within the finite-cut lemma. At each finite step, transport the next chosen disk or strip through the current entry-pair homeomorphism and apply the corresponding shaving operation. Compact support away from the trace excludes forward-trapped entry orbits from the removed tube. The maximal trajectory segments used in these tubes are the ones inside the current block, so possible later reentry into the block causes no ambiguity.

For strips, endpoints are allowed on tangency curves: the endpoint fibers collapse in the flow-coordinate model, and the cited strip construction specifically accounts for this. One is not treating such a tube as a nondegenerate rectangle times an interval. Convex tapering restores transverse entry/exit and exterior tangency; the local model also supplies tameness. These facts address the geometric obstruction which would invalidate an arbitrary abstract modification of the entry surface.

Only finitely many operations occur, each gives a smaller genuine block isolating the same K, and the final entry pair is homeomorphic to (P,L). Hence the claimed mod-2 relative vanishing transfers back to the actual block B. Arbitrary smallness comes from the initial block choice, not from an unproved claim that shaving an arbitrary surface neighborhood automatically removes all stable and unstable tails.

## 6. Integral vanishing and splitting

The coefficient change is valid and does not conceal a finite-rank assumption on H1(K;Z).

First, H0(P,L;F2)=0 means every component of the finite surface P meets L. Thus H0(P,L;Z)=0. The same long exact sequence and H1(P,L;F2)=0 show that H0(P;F2)->H0(L;F2) is surjective. It follows that L has finitely many connected components. For completeness, in a compact Hausdorff space components equal quasicomponents; any finite collection of distinct components can be distinguished by a finite clopen partition. Their characteristic functions give correspondingly many linearly independent degree-zero classes. Infinitely many components would therefore contradict the finite-dimensional surjection.

Because those finitely many components are clopen, H0(L;Z) is finitely generated. The integral long exact sequence now expresses H1(P,L;Z) as an extension of a quotient of H0(L;Z) by a subgroup of H1(P;Z), so it is finitely generated. The subgroup is finitely generated because H1(P;Z) is.

The quotient P/L is compact metrizable. Its reduced first integral Cech cohomology is torsion-free: present it by finite polyhedra, use the universal coefficient theorem at degree one on each polyhedron, and take the direct limit of torsion-free groups. Direct limits here remain torsion-free even when their bonding maps are not injective. Indeed, if a multiple of a represented element becomes zero at a later stage, torsion-freeness at that stage forces the element itself to become zero.

The coefficient sequence 0 -> Z --2--> Z -> F2 -> 0 gives an injection of H1(P,L;Z)/2H1(P,L;Z) into H1(P,L;F2). The target is zero. A finitely generated torsion-free abelian group with zero mod-2 reduction is zero. This establishes integral relative vanishing without assuming that an arbitrary group with zero mod-2 reduction vanishes.

Finally the long exact sequence gives H0(B;Z) isomorphic to H0(K;Z), injectivity of H1(B;Z)->H1(K;Z), and an embedding of its cokernel into H2(B,K;Z). The latter is identified with H2(P,L;Z), and oriented surface duality identifies that group with H0(P minus L,partial P;Z). For a possibly disconnected open surface, this relative H0 is free on components which do not meet partial P. Arbitrary rank is harmless. Its subgroups are free abelian, so the cokernel is free and therefore projective; the short exact sequence splits. This is a noncanonical splitting of abelian groups only.

If L is empty, the initial H0(S,L)=0 condition forces S to be empty; the surface argument is then vacuous and the relative block conclusion follows directly. The stated quotient conventions do not introduce an exceptional case.

## 7. Boundary of this acceptance

The proof has no hidden finite-H1(K) assumption, no hidden finite-relative-H0 assumption, and no purely abstract surface step being passed off as a flow operation. The remaining relative degree-two group can nevertheless be infinite, and the finite-cut construction does not eliminate it.

In particular, it supplies neither fundamental-group stabilization nor the maps and homotopies required by the quantified movability criterion. The previously accepted rank-two inverse-graph example remains a relevant warning about this distinction, not an isolated-flow counterexample. The final discussion correctly keeps the additional problem of obtaining an isolated enlargement of an arbitrary invariant compactum separate.

No mathematical correction to the frozen input is required for these three partial claims. Explicitly separating the empty-K case and spelling out the clopen-partition argument are optional expository clarifications, included above. The original problem remains unresolved by this argument.
