# Author approach 3: torsion symmetry and relative local-knot absorption

## Construction goal

Approach 1 leaves open the possibility that ordinary four-genus is larger than stable four-genus. This attempt tries to turn such a gap into a genuine genus-saving surface in an orientable lens-space product. The simplest target is a genus-one surface for a local K in RP³×I, with g_4(K)≥2. A finite cover or a four-manifold filling is not the desired answer: an explicit embedded product surface is required.

Two related constructions were tested. Both stop at an identified geometric obstruction. No counterexample is produced.

## Test A: quotient a surface for two copies of K

Let q:S³→RP³ be the antipodal double cover, and suppose F⊂RP³×I is a connected orientable genus-one surface with one local boundary K and nontrivial fundamental-group image. Its full preimage is connected. By the exact covering calculation, it must be a genus-one surface with two boundary components, each a copy of K in one of two antipodal disjoint balls. The deck transformation must act freely, preserve the surface orientation, exchange the two boundary components, and agree with (x,t)↦(−x,t) on the ambient product.

This gives a concrete proposed construction target:

    A smoothly embedded Σ_{1,2} in S³×I, invariant under the product antipodal action,
    with orientation-preserving free restricted action and boundary K⊔K in a ball orbit.

Its quotient would be exactly the required genus-one local-knot surface in RP³×I. The boundary ball orbit, rather than merely an invariant knot, is essential to locality downstairs.

### Why a slice #²K does not supply the target

For an order-two concordance class, #²K is slice. Splitting its connected-sum boundary by an oriented saddle gives an annulus with boundary a split union of two copies of K. This annulus has χ=0, whereas the required double-cover surface has χ=−2. More decisively, no free orientation-preserving involution of an annulus can exchange its two boundary components: its quotient would be a compact orientable surface with one boundary and Euler characteristic zero, contradicting χ=1−2g.

A free orientation-reversing involution can exchange the annulus boundaries, but then the quotient is nonorientable (a Möbius band). That is outside the problem's category. Thus the apparent direct torsion construction fails before any four-dimensional embedding details.

Adding one interior tube to the annulus gives the right topology Σ_{1,2}. It does not create the required antipodal equivariance. In particular, an orientation-reversing action on a surviving open part of the old annulus cannot become orientation-preserving merely by adding a tube elsewhere. A new global equivariant embedding is still needed. A slice disk for #²K, even a ribbon disk, does not provide it.

For a general cyclic d-fold lens-space cover, a genus-one quotient similarly requires a connected genus-one surface with d local boundary components and a free orientation-preserving cyclic action. The numerical inequality g_4(#^dK)≤d is only necessary; it gives neither this boundary configuration nor the action.

## Test B: cancel a nonlocal companion using an annulus

The next attempt uses local-knot absorption. Let J⊂M be any oriented knot, choose an embedded annulus R⊂M around J, and denote its two boundary components by J_+ and J_−, with their opposite annulus-induced orientations. Here J_− means an oppositely oriented parallel; it does NOT mean the classical concordance inverse, which would also mirror the ambient knot.

Tie the local knot K into J_+ in a small ball disjoint from J_−. Write

    L_K=(J_+#K)⊔J_−,       L_0=J_+⊔J_−.

There is a standard oriented pair-of-pants cobordism P_K from the local K to L_K. For K=U, take the annulus R with a small interior disk removed and use a height function to place its small boundary at the incoming end and the other two boundaries at the outgoing end. For general K, insert the same local knotted strip along an arc of this pair of pants joining its small boundary to J_+. This inserts K in exactly those two boundary components and leaves J_− unchanged. The cobordism remains embedded and has χ(P_K)=−1.

### Conditional construction lemma

If there is a smooth oriented two-component link concordance from L_K to L_0 in M×I, preserving the specified components, then

    g_{M×I}(K) ≤ 1.

Proof. Stack P_K, the two disjoint concordance annuli, and a pushed-in copy of the annulus R capping L_0. The result is a compact connected orientable properly embedded surface with sole boundary K. Its Euler characteristic is −1+0+0=−1, hence it has genus one. All pieces lie in successive portions of the same product collar; no filling or surgery trace is substituted. ∎

This is a potentially useful sufficient condition for a counterexample if g_4(K)≥2. It is stronger than ordinary concordance J#K≈J.

### Intersection-cost version

Suppose only an embedded knot concordance A from J_+#K to J_+ is available. Keep the other component as the cylinder C=J_−×I, and make A transverse to C with r intersection points. Stacking P_K, A∪C, and R now gives an immersed connected orientable genus-one surface with exactly those r transverse double points. Oriented local smoothing of each double point removes two disks and inserts an annulus, increasing the genus by one. Therefore this actual construction gives

    g_{M×I}(K) ≤ 1+r.

To beat g_4(K), one needs a concordance A and spectator C with r≤g_4(K)−2. The ordinary knot-concordance statement does not control r and does not establish r=0. In dimension four, generic two-surfaces have isolated intersections; general position does not make them disjoint.

## A verified sanity check exposes the missing hypothesis

Davis–Nagel–Park–Ray prove that all winding-one knots in S¹×S² are smoothly concordant to the standard essential core (Theorem A). Thus J#K is concordant to J for that core and every local K. The same paper proves that every local-knot surface type in S¹×S²×I already occurs classically (Theorem 2.5).

If knot concordance alone implied the two-component link concordance above, every classical knot would have four-genus at most one. Taking K as a connected sum of three equally handed trefoils contradicts its signature lower bound g_4(K)=3. More quantitatively, for this particular construction in S¹×S² any transverse absorbing annulus and the prescribed spectator cylinder must have

    r ≥ g_4(K)−1.

This inequality follows by combining the smoothing construction with the known local-genus equality. It proves that the spectator-disjointness problem is substantive, rather than a technical isotopy omitted from the construction.

## Applying the test to projective/lens-space constructions

McDonald–Miller's constructions give tangle cobordisms in punctured three-manifold products and then use gluing in Spin(M) to produce low-genus surfaces in punctured four-manifolds. In particular their RP³ construction recovers disks for strongly negative amphichiral knots in punctured Spin(RP³); their Remark 2.10 gives genus at most one in punctured RP³×S¹. Neither ambient four-manifold is RP³×I.

Attempting to replace the spinning step with the companion-cancellation lemma requires precisely the disjoint spectator concordance above. The constructions checked do not state or verify that condition. Their compression disks and bands cannot be assumed disjoint from a parallel essential companion. No intersection count sufficient for a strict genus saving was established here.

The output of this attempt is therefore a concrete geometric target, an orientability obstruction to the naive quotient, and a relative-link criterion with an explicit intersection penalty. It is not evidence that a desired equivariant surface or disjoint link concordance exists.

## Disposition and next obstacle

This is substantive author approach 3. The full orientable local-knot problem remains unresolved by it. The finite-stable-genus gap survives, but realizing it needs either:

1. an explicitly verified free equivariant Σ_{g,d} in a spherical product cover, with local boundary orbit; or
2. a link concordance satisfying the companion-disjointness condition, or an intersection bound strong enough to save genus.

Source checking and later review do not add author turns.

## Public references

- C. W. Davis, M. Nagel, J. Park, A. Ray, Concordance of knots in S¹×S², Theorems A and 2.5. https://arxiv.org/abs/1707.04542 . The institutional PDF was readable through the web tool at https://pure.mpg.de/rest/items/item_3086285_1/component/file_3136058/content ; a separate local download returned HTTP 403 and was not retried or bypassed.
- C. McDonald and A. N. Miller, Constructing knots with low rational genera, Construction 2.8, Proposition 2.9 and Remark 2.10. https://arxiv.org/abs/2511.15900 .
