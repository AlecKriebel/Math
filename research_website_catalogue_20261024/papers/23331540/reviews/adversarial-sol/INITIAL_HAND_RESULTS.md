# Independent hand falsification before support/primary bodies

These are actual source-first deductions from the native definitions and displayed formulas. They are not prior AI reviews or execution results, and do not assert the original-question interface has yet been verified.

## 1. Is the collapsed-edge observable really invariant under the stated homeomorphism?

Let e={i,j} be a native coordinate. The vector with w_e=1 and all other coordinates0 satisfies equilibrium iff p_i=p_j: the only possibly nonzero forces are ±(p_j−p_i). In particular the exact sign pattern (+ at e,0 everywhere else) occurs iff the edge collapses. A sign-coordinate-preserving homeomorphism is a bijection, so its image preserves existence of this pattern; its inverse does too. It need not be linear or map the vector1 to itself, but it must map the positive singleton-support ray to vectors with the same pattern. This suffices. The all-zero vector is the unique all-zero sign pattern. The argument therefore does not assume linearity of an arbitrary fibre equivalence.

It follows that a same-G equivalence class either lies in Δ_ij or avoids it when e is an edge. Every connected component of each class has the same property, so the diagonal is a union of full strata even if a class is disconnected. This direction requires no unstated implication “equal dimension ⇒ equivalent” and no topology finer than the defined partition.

## 2. Nonedge witness: signs, orientation and connectedness

For a nonedge{i,j}, choose a≠0. Set x_i=t, x_j=0, x_k=k+1 for all other native labels k and −1/2≤t≤1/2; put p_k=x_k a. Every fixed x_k is at least2 and distinct. Thus the only potential collision is i with j at0. Every actual edge difference δ_e(t)=x_v−x_u is nonzero throughout the closed interval, with a fixed sign. It has a positive lower bound because there are finitely many edges and a compact interval. Nonedges elsewhere are irrelevant to equilibrium, and no actual collapsed edge has been introduced.

With B initial+1/final−1, (BD_tw)_u sums w_e(x_v−x_u) with precisely the equilibrium sign at each endpoint. Equilibrium in R^d is the scalar equation BD_tw=0 times a; since a≠0 the equivalence is exact for every d≥1. Reversing an orientation changes BOTH its B column and its diagonal entry by−1; BD_t and D_t^−1D_0 therefore do not change. This addresses an orientation-sign trap.

The transport T_t=D_t^−1D_0 has strictly positive diagonal entries δ_e(0)/δ_e(t). Direct multiplication gives BD_tT_t=BD_0, and its inverse is D_0^−1D_t. Consequently it maps the complete kernel bijectively, preserves every positive/negative/zero coordinate, and is a linear homeomorphism of the stress subspaces. The empty edge set is the zero-dimensional exception with the unique zero-space map, not an inversion of a nonempty singular matrix.

All P(t) belong to the SAME equivalence class, not merely classes with equal rank. The map t↦P(t) is continuous, so its connected image is contained in one connected component of that class. There is no need to infer that the entire equivalence class is connected or that all equivalent points can be joined. This particular connected set contains P(0)∈Δ_ij and P(1/4)∉Δ_ij. A partition block crossing a set proves it is not a union of whole blocks. The quantifiers in this converse are therefore adequate for each nonedge, with a witness in the full space rather than a replacement collinear-only theorem.

## 3. A nontrivial rational cycle control

Take the C4 edges12,23,34,14 and the missing pair13. Use i=1,j=3 with x=(t,3,0,5), and orient the cycle1→2→3→4→1. Then

    D_t=diag(3−t,−3,5,t−5),
    ker(B)=span(1,1,1,1),
    W(P(t))=span(1/(3−t),−1/3,1/5,1/(t−5)).

At t=0 this generator is (1/3,−1/3,1/5,−1/5), and at t=1/4 it is (4/11,−1/3,1/5,−4/19). The positive coordinate transport is diag(12/11,1,1,20/19). Both fibres have exactly the two nonzero full-support sign patterns (+,−,+,−) and its opposite plus0, and the actual positive diagonal map gives topology, not just an assertion from sign patterns. The nonedge13 collision disappears without changing the stratum along the explicit path. This tests a nonzero stress space rather than relying only on edgeless/forest examples.

## 4. Dimension-only and sign-forgetting attacks

For K3 collinear coordinates(0,1,2), the stress space in edge order12,23,13 is span(2,2,−1). At the collapsed configuration(0,0,1), equilibrium forces w13=w23=0 and allows arbitrary w12, so the stress space is span(1,0,0). Both have dimension1 and are abstractly homeomorphic lines. They are not coordinate-sign equivalent: the positive singleton12 pattern is absent from the first. Thus merely classifying stress dimensions or forgetting labels/signs would invalidate the detector, but the native definition retains the needed data. The chosen placements are valid for every d≥1 by multiplication by a≠0.

Even knowing the set of possible sign vectors is not silently identified here with existence of a sign-preserving homeomorphism. The edge obstruction needs only its necessity; the nonedge construction supplies an explicit linear map, stronger than sufficiency of an abstract sign-pattern assertion.

## 5. Small parameters and connected components

n=1 has one simple empty graph; the edge-pair theorem is vacuous and the reconstruction conclusion is correct. For n=2, the empty graph has W={0} at every point and one equivalence class X, which is connected. Its collision diagonal is a proper subset when d≥1, so cannot be a union of its single stratum. The one-edge graph has W=R on Δ12 and W={0} off it; Δ12 is a full class and connected.

For d=1 the complement of Δ12 has two connected components p2−p1>0 and<0. Both have the same zero stress space, so they demonstrate that an equivalence class need not itself be one stratum. The collision diagonal remains a block. For d≥2, R^d\{0} is connected, so the noncollapsed class is connected after separating root location and difference. No proof step assumes the d=1 and d≥2 numbers of components agree.

The absent d=0 hypothesis is essential: X is then a singleton and every graph induces the same singleton partition; every Δij=X would be a union even for a nonedge. This is a control outside the claimed range, not a defect. Likewise loops contribute a free coordinate at every placement and parallel edges are not reconstructed merely by the single collision observable; simplicity is an actual hypothesis, not decorative wording. For n=2 with m≥1 parallel edges, all noncollapsed fibres are the fixed hyperplane sum w_e=0 and all collapsed fibres R^m; each m has the same location partition though coordinate spaces differ across graphs. The source excludes this enlarged class.

## 6. Forests and the exact ambient-linear distinction

At a leaf of a forest, its only incident stress obeys w_e(p_j−p_i)=0. A noncollapsed leaf edge has w_e=0; a collapsed leaf edge has arbitrary w_e but contributes zero force at the neighbour as well. Removing the leaf and iterating gives W exactly the coordinate subspace supported on collapsed edges, with those coordinates independent. This works even if unrelated vertices collide, because graph leaf degree is unchanged by geometric coincidence.

Hence two placements for the same forest are sign-equivalent iff their sets of collapsed native edges agree. Necessity follows from singleton supports; sufficiency is the coordinate-subspace identity. The connected components may split further, particularly in d=1, and must be transported as components rather than counted by stress dimension.

For path G={12,23,34} and star H={12,13,14}, the native map is

    q1=p1, q2=p2, q3=p1+p3−p2, q4=p1+p4−p3.

It gives q2−q1=p2−p1, q3−q1=p3−p2, q4−q1=p4−p3. It is invertible, with

    p1=q1, p2=q2, p3=q3+q2−q1, p4=q4+q3+q2−2q1.

The scalar4×4 linear matrix has determinant1; the same invertibility holds on all d coordinates. Thus the three corresponding collapsed-edge conditions match exactly, and forest equivalence classes map bijectively. A homeomorphism maps connected components onto connected components: a larger connected image/preimage would contradict maximality. The map therefore carries the full strata, including their d=1 component splits. Degree multisets (2,2,1,1) and(3,1,1,1) differ, so the graphs are not isomorphic.

This ambient map is not a permitted fixed-label partition equality or a vertex permutation. It genuinely mixes coordinates. Literal reconstruction and this distinct ambient-equivalence example therefore do not contradict one another. The corollary for a specified label permutation follows instead because that coordinate permutation carries every equilibrium equation and every collision diagonal to the corresponding labelled one; the converse invokes the recovered pair set. No classification of arbitrary ambient maps is deduced.

## 7. Exact pending falsifiers and primary-source interface

No counterexample was found in these source-first hand controls to the displayed native theorem or forest example under their stated conventions. This is not yet a full-original pass: the claimed answer to the literal original Problem4 still requires actual primary definitions/question and attention to whether the source's “same stratifications” has any explicitly different cross-graph equivalence. It is not acceptable to silently repair a mismatch by limiting the published claim after the fact. Also pending are the actual cited singleton-detector/collinear-invariance interfaces and supporting-package relevance; archived priority conclusions will not substitute for primary reading.

Potential failure routes retained for post-resume review: an actual primary restriction excluding collisions or fixing dimension differently; strata defined by a finer/different topological comparison; a source-defined ambient/cross-graph equivalence replacing literal equality; a missed normalisation that changes coordinate-sign fibres; or support code that checks a different graph/stratum notion. Central gaps will be recorded rather than transferred to an equivalent unsupported classification. No novelty or historical exhaustiveness conclusion is inferred from the manuscript's assertions. No new follow-up is proposed.
