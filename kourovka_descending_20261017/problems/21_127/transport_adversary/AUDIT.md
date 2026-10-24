# Fresh adversarial review: fixed coordinate transport and the P4 example

Review begun 2026-10-24T20:54 UTC; mathematical and independent finite checks completed 2026-10-24T20:58 UTC; clarification delta accepted 2026-10-24T21:00 UTC. Reviewer did not author the construction. Estimated review completion: **100%**, with no outstanding substantive objection to the scoped claims. Estimated completion toward a solution of original Kourovka 21.127 from this route remains **7%**: the review establishes bounded partials, not general rationality. No originality claim or publication recommendation.

## Verdict and scope

The mathematical claims survive this review **with rewiring restricted to compatible ends of the same edge in the graph of groups**. The source setup already imposes that condition. The author has now explicitly repeated it in the P4 paragraph formerly saying “arbitrary” b/c pairings. This is an accepted presentation repair, not a new mathematical hypothesis.

Accepted partials:

1. The integral winding-transport criterion for fixed polygon blocks and fixed paired turns.
2. Its exact finite hitting-set optimization, including the Euler-characteristic count for the stated simple relative surfaces.
3. A P4 family with minimum four non-disks among sixteen blocks, relative Euler characteristic −4, and relative objective 2 within the fixed family.
4. Positive-density loss for compatible rewirings of unchanged copies and for the stated graph covers. The proof does not extend this loss to annular covers that change block shapes.
5. Two actual commutator-subgroup exterior elements and the bounds
   \[
   1\leq \operatorname{scl}_{A(P_4)}(g_1+g_2)\leq2.
   \]

No accepted statement determines the exact absolute chain value. No accepted statement answers elementwise rationality in arbitrary RAAGs. In particular, the exact relative cost 2 is not a certified sharp absolute value.

## Custody and independent reproduction

`independent_check.py` imports no author code and does not execute the author's checker. The initial run independently checked all eleven SHA-256/size entries in `graph_decomposition/FROZEN_MANIFEST.json`; all matched the version frozen at 20:53:36 UTC. The final run accepts exactly the reviewed two-file delta recorded in `REVIEW_DELTA_MANIFEST.json`: the P4 wording and its research-log entry. Every other frozen hash remains unchanged. The original and final checked claims, exact inputs and reconstructed outputs are recorded in `FROZEN_INITIAL_RESULTS.json` and `INDEPENDENT_RESULTS.json` respectively.

The independent reconstruction uses disjoint-set union for coordinate components, checks **all 65,536 subsets** of the sixteen pieces, and finds exactly two transversals of minimum size four: the even M pieces and the odd M pieces. The full histogram is retained. It then applies the supplied integer currents directly to independently reconstructed charges and finds exactly

\[
M_1:(2,2),\quad M_3:(2,2),\quad M_5:(-2,2),\quad M_7:(-2,-6).
\]

All other twelve winding vectors vanish. The four displayed vectors sum to zero.

It separately reconstructs the two exterior boundary cycles by ribbon permutations: each block has two turn ports; exchanging ports gives the vertex permutation, pairing ports gives the edge involution, and their composition gives the two boundary faces. Both face cycles have length sixteen and recover the exact recorded words. Thus the check does not merely retype or assume the two words.

The checker also verifies every exponent sum, nonempty projections to F(a,d), both projections to F(a,c), the actual free commutator identity, and cyclic rotation. It checks the surface/cap Euler characteristics and monodromy arithmetic for every degree 1 through 64. The all-degree proofs follow below; finite checks alone are not their justification.

## Integral transport: necessity, sufficiency and limitations

For a coordinate x the equations are those of an oriented graph incidence matrix, restricted to rows indexed by required disk pieces. A connected component with every row constrained has column sums zero, so its total prescribed charge must vanish. This proves necessity, including isolated vertices and loops.

For sufficiency, in a component with any unconstrained vertex choose it as root. Set off-tree currents to zero and move each leaf's entire integral charge across its parent edge. The operation solves that leaf's equation and changes only the parent's residual charge; every value is an integer. With all rows constrained, the final root equation holds precisely when total charge is zero. With an unconstrained root it need not hold, as allowed. Different named coordinates of a coordinate subgroup are independent, so these scalar solutions combine to a permissible winding vector. No congruence or saturation issue remains in this primitive coordinate-subgroup setting.

The result would need modification for scaled nonprimitive injections or arbitrary changes of coordinate basis. The actual theorem explicitly assumes identical named coordinate subgroups, and P4 satisfies that assumption.

The hitting-set consequence follows in both directions. Any nonzero-charge component must meet the actual non-disks. Conversely, a transversal permits all other pieces to be disks by the transport proof. If a minimum transversal produced fewer actual non-disks, those would be a smaller transversal, a contradiction. Thus the optimum number is attained, not just approached.

Each zero-winding polygon bounds a disk in its target torus because pi_1 of the torus is exactly its integral winding group. Each nonzero-winding polygon is realizable as one boundary of an annulus, with the other boundary the opposite winding loop. For these simple relative surfaces the pieces contribute 1 or 0 and each turn-interval gluing subtracts one; hence chi = V − tau − E. This is a relative construction with additional loop boundaries. An uncapped annulus is not an absolute filling.

For the explicit family the piece graph is a single cycle. A regular thickening has two exterior boundary circles and genus zero. Removing a disk from each of four disk blocks changes those blocks to annuli and adds four inner circles. It remains connected, has b=6 and chi=12−16=−4, hence genus zero. This independently excludes a hidden handle or a missing Euler-characteristic term.

## Uniform loss and the precise meaning of covers

Compatible b rewiring pairs an ab-side turn with a bc-side turn. An A block has degree two in H_b and every M block has degree one in H_b. Consequently each H_b component is one A and two distinct M leaves. With N unchanged copies there are 4N disjoint such components. Their possible total charges are 2, −2 and −6, all nonzero; one non-disk is mandatory in each. This proves the 4N lower bound irrespective of extra boundary-word pairing restrictions. The c restrictions can only add constraints; they cannot weaken it. The recorded odd-M transversal realizes equality in the displayed pairing, and disjoint copies realize equality for the duplicated family.

The incidence graph is 2-regular for all such pairings, so its components have V=E and chi=−(number of non-disks). There is no positive-Euler-characteristic component whose removal would invalidate the numerical relative objective.

If “arbitrary b pairings” were instead permitted to pair A with A and M with M, the asserted star structure would fail. Those pairings do not glue opposite ends of the b edge in the prescribed graph of groups. The accepted wording now expressly excludes such pairings. Its exact P4 SHA-256 is `d63b5ed01f04dcb1f5b3868d4360da3ff23f619e9353cdcd74a9f3c8f340df49` (8172 bytes).

A genuine graph cover duplicating unchanged blocks restricts to a covering of each H_x: all coordinate incidences remain present at every lift. A finite cover of a finite tree is a disjoint union of copies of that tree, so nonzero charge persists in every copy. This proves the graph-cover obstruction. An annular-piece cover has different local data: a connected degree-N annular cover has a polygon boundary running through N copies of the old circuit, hence a longer polygon and potentially degree 2N in its incidence description. It is outside this unchanged-block hypothesis. Confusing those two operations would invalidate the promotion argument, and the reviewed text keeps them separate.

## Actual RAAG words and absolute upper bound

The iterated amalgam of the three coordinate tori has exactly the P4 presentation, with injective coordinate inclusions. Its underlying graph is a tree, so choosing paths through the edge cylinders introduces no stable-letter generators. The exterior words recovered by the ribbon computation are the actual RAAG boundary words.

At each ab endpoint the exterior arc is a or a^-1, outside the incident subgroup <b>. At each cd endpoint it is d or d^-1, outside <c>. The middle passages use different edges. Therefore the graph-of-groups loops have no trivial backtracking and are tight/hyperbolic. Independently, the F(a,d) projections are nontrivial. All four exponent sums of each word vanish, so both words lie in the RAAG commutator subgroup.

The four inner circles of the six-holed sphere map into the same middle torus. Their oriented winding vectors are the negatives of the recorded outer annular windings; either convention has sum zero. For every positive N, send the six oriented boundary generators to 1,−1,1,−1,1,−1 in Z/N. The sum-zero sphere relation is respected, and 1 generates Z/N, so the corresponding cover is connected. Each boundary monodromy is an N-cycle, giving one boundary lift of degree N for each of the six boundaries. A monodromy of −1 changes the sheet permutation, not the positive degree of an oriented covering of the boundary circle.

The cover has chi=−4N and still six boundary components. Its four inner boundary vectors are N times the original vectors, still summing to zero. A four-holed sphere maps into the middle torus with their opposites as boundary values: choose based representatives in that torus; the product relation holds because its fundamental group is abelian. Attaching this cap subtracts two from chi and leaves precisely two outer boundaries, each of degree N over the corresponding g_i. Thus the absolute admissible surface has

\[
\chi=-4N-2,\qquad -\chi/(2N)=2+1/N.
\]

Taking the infimum proves the upper bound 2. There are no remaining unfilled loop boundaries. The normalized cap cost tends to zero, but the cover's own negative Euler characteristic has already grown by 4N. Hence no annular reservoir has been silently filled at zero total cost.

## Free-retract lower bound

Killing b,d gives a well-defined retraction to the free induced subgroup F(a,c). The independently reconstructed images are

\[
h=acacAcACCC,
\qquad h'=ACCCacacAc,
\]

and h' is a forward cyclic rotation of h, not a rotation of its inverse. Exact reduction verifies

\[
h=[acacA,cACA].
\]

The word is cyclically reduced and nonempty. The once-punctured-torus construction gives the universal scl upper bound 1/2 for a commutator. Heuer's primary Theorem 7.3 supplies the lower bound 1/2 for this nontrivial free RAAG element. Therefore scl(h)=1/2. Conjugacy invariance and homogeneity give scl(h+h')=scl(2h)=1, and monotonicity under the retraction proves the claimed lower bound for the original chain.

The exploratory turn LP is unnecessary for this proof. Its claimed topological model was not adopted as a substitute for the direct commutator argument; the original probe labels that interpretation as requiring independent review.

## Primary theorem checks and exact remaining gap

Primary versions were reopened at arXiv during this review, and cached full texts were inspected:

- [Chen, arXiv:1904.08360v2](https://arxiv.org/abs/1904.08360v2), Section 3.1 and equation (3–1): paired turns have opposite winding and matching boundary types. Theorem 3.4 requires homological injectivity on the sum of the incident edge images. Theorem 5.10 requires central, mutually commensurable images in each vertex. In P4 the middle images are the distinct rational lines <b> and <c>; they are not commensurable. Collapsing them to one abelian direction loses injectivity on that rank-two sum. Passing to finite-index lattices keeps the lines distinct.
- [Susse, arXiv:1310.2254v3](https://arxiv.org/abs/1310.2254v3), Theorems 3.4/3.5: free abelian factors amalgamated over one common shared subgroup. An iteration with a nonabelian intermediate vertex and changing edge directions is not a direct instance.
- [Heuer, arXiv:1802.01107v3](https://arxiv.org/abs/1802.01107v3), Theorem 7.3: every nontrivial commutator-subgroup element of a RAAG has scl at least 1/2. This applies to the free-group word above.

The independent derived-subgroup warning is also sound. Under G -> F(a,d), [G,G] maps onto F(a,d)', while [a,d] gives a nonzero square cycle in the universal abelian cover of a rose, which is a graph with no 2-cells. Therefore [a,d] is not in [[G,G],[G,G]] and free-derived-subgroup scl cannot simply replace ambient scl.

The remaining general problem is control of all polygon types, winding component structures and admissible pairings for an arbitrary fixed input. Fixed-data integer optimization does not supply that control. Infima of infinitely many rational optima need not be rational. No exact absolute value, extremal-surface theorem, new compactness mechanism, or irrational element has been established by this family. All such routes remain unproved; publication as a solution of 21.127 would be unjustified.
