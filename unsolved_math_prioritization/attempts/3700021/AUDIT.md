# Independent AI-assisted audit of the bounded logarithmic well criterion

## Verdict

**The conditional construction is mathematically valid. Eremenko's Problem 2 remains unresolved.** The proof in the examined report establishes a sufficient criterion; it neither constructs a family satisfying the all-height condition nor proves that no such family exists. No material mathematical gap was found in the conditional implication. One narrow inequality correction was identified in the earlier exposition’s discussion of containment of an open smaller disk and is incorporated in the companion statement; it does not change the theorem or the unresolved disposition.

This audit spells out the pointwise representative argument, the component separation argument, and the roles of local finiteness and strict inequalities. It also gives an explicit one-disk example showing that the affine upper bound, a nonnegative plateau, and positive circle mass are compatible for arbitrarily small error. This example covers only a small interval of heights and is not a solution of the original problem.

The companion `CONDITIONAL_PROPOSITION.md` gives a self-contained statement and proof suitable for retaining as an authored mathematical result. Acceptance in this audit means acceptance of that conditional result only. It must not be encoded as acceptance or resolution of Problem 2.

## Scope and review status

The reviewed authored result concerns problem 3700021 / AMR-036-0021. This public edition retains the mathematical checks, complete one-disk example, and qualified mass discussion. The companion conditional proposition is preserved byte for byte from the accepted mathematical review. Public source identities and inspection limits are recorded separately in `SOURCE_METADATA.json`.

This is independent AI-assisted mathematical review of an AI-assisted, unrefereed result. It is not human peer review or a machine-checked formal proof. Acceptance is restricted to the stated conditional implication and explicitly scoped partial results. Hashes identify exact files; they do not establish mathematical truth. No novelty, priority, or comprehensive current-literature claim is made.

## Target and source separation

The target is Problem 2 on the first page of A. Eremenko's [2008 problem note](https://www.math.purdue.edu/~eremenko/dvi/potvd.pdf). It asks about subharmonic functions on the open unit square converging uniformly there to the horizontal coordinate, and whether negative components other than the component containing the point −1/2 can collectively meet every horizontal height. The natural substantial interpretation concerns a sequence, or a subsequence reindexed as a sequence, with that geometry. The square's boundary endpoints do not count as intersections.

The independent audit examined the two-page problem note as text and reconfirmed the target through the public PDF. The [author's public problem index](https://www.math.purdue.edu/~eremenko/uns1.html), checked on 2026-10-11, marks Problem 1 of that note solved; it does not mark Problem 2 solved. This observation is not a comprehensive literature-status theorem.

The neighboring paper is A. Eremenko and T. Zhang, [A counterexample to Fuchs's conjecture, arXiv 2609.28443v1](https://arxiv.org/abs/2609.28443v1). Its exact supplied PDF has 529,022 bytes and SHA256 `6ac2b7a095fe289fcc2a7033ed8865ef66be5dfcec17c70abe25b16b17db7eb8`. This audit inspected its relevant statements and proof passages in Proposition 5.1, Lemma 5.2, and Lemma 6.1. These passages provide flat disks, a positive Riesz measure, dyadic scaling, radial coverage by shrunken disks, and logarithmic drilling. They do not provide the affine envelope or horizontal negative-core coverage required here. During the independent mathematical audit, a fresh web request for the versioned abstract returned a cache error; the source comparison rests on the hash-verified PDF and its extracted text, not on a claimed successful fresh arXiv retrieval.

There is a useful terminology refinement: call the source potential a **logarithmic potential with positive Riesz measure**, rather than a “positive logarithmic potential” if the latter could suggest that its values are everywhere nonnegative. Proposition 5.1 calls its plateau constants real; the conditional criterion separately assumes the selected plateau values are nonnegative. No conclusion about the source paper's later entire-function construction, journal acceptance, or complete proof correctness is made in this audit.

## Detailed mathematical checks

### Distributional identity and normalization

For a disk B(a,R), put G(z)=log(|z−a|/R) on its interior and G=0 on its complement, with the logarithmic value −∞ at a. Let λ_R be normalized arclength on its boundary, so dλ_R=ds/(2πR). Then

    (2π)^(-1) ΔG = δ_a − λ_R.

The center atom is positive. The circle term is negative: the radial normal derivative changes from 1/R on the inner side to zero on the outer side. For a smooth compactly supported test function φ, integration by parts over a punctured disk gives

    ⟨ΔG,φ⟩ = 2π φ(a) − (1/R) ∫_{∂B(a,R)} φ ds.

Thus the report's sign and its factors of 2π and R are correct. The boundary-mass assumption μ|_{∂B_j}≥γ_j λ_{R_j} pays for precisely the negative circle term introduced by γ_jG_j. Because the circles are disjoint, these lower bounds can be subtracted simultaneously. The center atoms add positive measure.

### Local finiteness and local integrability

On every relatively compact part of the ambient open set, local finiteness reduces the distributional calculation to finitely many logarithmic patches. Each patch is locally integrable. Consequently W is a well-defined locally integrable function, with the indicated pointwise values, and

    (2π)^(-1) ΔW = μ − Σ_j γ_j λ_{R_j} + Σ_j γ_j δ_{a_j} ≥ 0.

There is no unproved convergence of an infinite series in this argument. Pairwise disjoint disks even imply that at a given point at most one patch is nonzero, but that pointwise observation alone would not justify distributional sums near an interior accumulation. The stated local-finiteness assumption correctly excludes such an accumulation. Accumulation at the boundary of Q is harmless if it lies outside the ambient open set; otherwise local finiteness must still hold there. The phrase “open neighborhood of Q” does not itself mean an open neighborhood of the closed square.

The Riesz-measure notation uses the usual nontrivial locally integrable subharmonic representative. If an ambient open set has irrelevant components on which V is identically −∞, one can discard those components or work on the component containing Q. This is a routine convention rather than a gap in the construction.

For the cleanest statement, take closed disks compactly contained in the ambient open set. If an open disk is contained in that set but its circle touches the ambient boundary, the same proof holds on the ambient set after restricting all circle measures to it. Requiring compact containment merely removes a notational ambiguity about the original boundary restriction.

### Pointwise values of the subharmonic representative

Distributional positivity alone yields an almost-everywhere class with a subharmonic representative; it would not justify arbitrary pointwise upward alterations. The report does not need such alterations.

Away from a disk center, the added locally finite sum is continuous in a neighborhood of the point. Its averages over shrinking disks converge to its value. The corresponding averages of a subharmonic V converge to V at every point, including points with value −∞. Therefore the shrinking-disk averages of W converge to its stated value at every noncenter point. At a center a_j, V is constant nearby and no other patch is present, so W=c_j+γ_j log(|z−a_j|/R_j); its disk averages tend to −∞. These pointwise limits identify W everywhere with the canonical subharmonic representative of its distributional class.

This also shows why no boundary values are silently changed by regularization. The finite family case is included, and the same argument is local for a locally finite family.

### The affine maximum and the whole-square bound

Every patch is nonpositive, so W≤V≤x+δ throughout Q. The function x−δ is harmonic. The maximum

    u=max(W,x−δ)

is subharmonic, is finite, and obeys x−δ≤u≤x+δ at every point of the entire open square. In particular, the centers where W=−∞ cause no problem: u takes the finite value x−δ there. No continuity assumption on V is needed.

The estimate is a global supremum estimate on Q, not merely a compact-subset bound. Choosing δ_k→0 would immediately give sup_Q |u_k−x|≤δ_k→0. No convergence or uniform bound for the original potentials V_k, apart from their respective envelopes, is additionally required.

### Exact negative cores

Because c_j≥0, the radius r_j=R_j exp(−c_j/γ_j) satisfies 0<r_j≤R_j. Within B_j, the other patches vanish, and

    W(z)=c_j+γ_j log(|z−a_j|/R_j).

Hence W<0 exactly when |z−a_j|<r_j, including the center. Since a maximum is negative exactly when both entries are negative,

    {u<0} ∩ B_j = Q ∩ B(a_j,r_j) ∩ {x<δ} = N_j.

The strict inequality x<δ is essential. Points with x=δ have u≥0. The case c_j=0 is correctly included: r_j=R_j, and the boundary circle remains outside the negative core. Empty N_j are simply irrelevant.

### Boundary barriers and full components

At any b∈∂B_j∩Q, upper semicontinuity and the constant values approaching b from inside the disk give V(b)≥c_j≥0. Each patch is zero at b: its own patch is zero by definition, and pairwise disjoint closures exclude any other patch there. Thus u(b)≥0.

The set D={u<0} is open because u is upper semicontinuous. A nonempty N_j is an intersection of convex open sets, hence is connected. Inside D there is no boundary point of B_j. Therefore D∩B_j is both open and closed relative to D: its relative complement is D∩(C\overline{B_j}), which is open in D. Any connected component of D meeting B_j must remain in B_j. As D∩B_j=N_j is connected, N_j is exactly one whole component. This argument works even when B_j extends beyond Q; the missing portions of its circle outside Q do not create a route within Q.

No global connectedness of the complement of the disks is assumed or needed.

### Separation from the main component

For x<−δ, the global upper bound gives u≤x+δ<0. Thus the entire connected left subrectangle of Q lies in one negative component, and it contains −1/2 because δ<1/2.

A point in B_j∩Q cannot have x<−δ, since the plateau value c_j≥0 would contradict V≤x+δ<0. Consequently N_j contains no point of that left subrectangle. Since N_j is already a whole component, it is different from the component containing −1/2. This proves the claimed non-main status without assuming that every other negative component has been classified.

### Coverage and its limitations

If the vertical projections of the N_j cover (−1,1), then for each height there is a point in one of these non-main negative components. This is exactly the required horizontal intersection. The projection hypothesis concerns the negative cores after the affine clipping; coverage by the larger plateau disks is not sufficient.

The condition is sufficient, not necessary: the construction might produce additional non-main components outside the specified disks. A failure of the displayed sufficient conditions would not settle Problem 2 negatively.

### Correction to the open smaller disk threshold

The examined report says that keeping a prescribed smaller disk B(a_j,qR_j), with 0<q<1, negative before clipping needs c_j<γ_j log(1/q). When B denotes an **open** disk, the exact condition is instead

    B(a_j,qR_j)⊆{W<0} if and only if c_j≤γ_j log(1/q).

Indeed, the exact negative radius is r_j=R_j exp(−c_j/γ_j), so inclusion of the open disk means qR_j≤r_j. Equality leaves every point of the smaller open disk negative and its boundary at level zero. The strict inequality is the condition for the **closed** smaller disk to be negative, or for a positive radial margin. This is a correction to the claim of necessity in the explanatory paragraph, not a defect in the exact radius formula or the conditional theorem.

### Finite capping

For L>0, replacing the logarithm inside a disk by max(log(|z−a|/R),−L) gives a continuous finite patch whose normalized Laplacian is

    λ_{R exp(−L)} − λ_R.

The derivative is zero inside the inner circle, 1/r between the two circles, and zero outside the outer circle; this gives a positive normalized mass on the inner circle and a negative one on the outer circle. If L>c_j/γ_j, the capped value at the bottom is strictly negative, and the negative set within B_j is the same radius-r_j disk as before. If equality holds, the entire patch plus c_j is nonnegative, so the strict hypothesis cannot be weakened. Capping does not increase the core radius. Capping by itself does not supply a lower affine bound for V; the final maximum still supplies that bound.

## An explicit compatible local example

The analytic hypotheses do not already contradict one another. Fix any 0<δ<1/2. Choose R>0 sufficiently small that

    R<δ and R+3R log(√2/R)≤δ.

Such R exist because R log(1/R) tends to zero. On the entire plane, define

    V_R(z)=0,                                             |z|≤R,
    V_R(z)=x(1−R²/|z|²)+3R log(|z|/R),                    |z|>R.

This function is continuous. It is harmonic in the disk and in the exterior. In polar coordinates the exterior formula is

    (r−R²/r) cos θ + 3R log(r/R).

Its outward radial derivative at r=R is 2 cos θ+3, while the derivative on the interior side is zero. Therefore

    (2π)^(-1) ΔV_R = ((3+2 cos θ)/(2π)) ds|_{|z|=R}
                   ≥ (1/(2π)) ds|_{|z|=R}
                   = R λ_R ≥0.

There is no center atom, because the function is constant in a neighborhood of the center. Thus V_R is subharmonic and supports the drilling coefficient γ=R on its zero plateau.

On Q∩{|z|≤R}, V_R−x=−x≤R. On Q∩{|z|>R},

    V_R−x=−R² x/|z|²+3R log(|z|/R)
          ≤R+3R log(√2/R)≤δ.

The conditional construction therefore applies. Here c=0, r=R, and R<δ ensures that the entire disk survives the clipping. It becomes a non-main negative component of a finite subharmonic u with sup_Q|u−x|≤δ.

Its vertical projection is only (−R,R). This example establishes no all-height coverage and supplies no compatible multiple-disk family. Directly adding copies of V_R would generally destroy each copy's constant plateau because the other copies are nonconstant there. The missing simultaneous construction has not been replaced by a superposition claim.

## Local mass convergence and the limit of a radius heuristic

For any proposed solution sequence with sup_Q|u_k−x|≤δ_k→0, put μ_k=(2π)^(-1)Δu_k. For every smooth compactly supported test function φ on Q,

    |∫ φ dμ_k| = |(2π)^(-1) ∫_Q (u_k−x)Δφ dA|
                 ≤δ_k (2π)^(-1) ∫_Q |Δφ| dA.

Thus μ_k tends to zero locally as a measure. In particular, choosing a nonnegative test function at least one on a fixed compact set K gives μ_k(K)=O_K(δ_k).

This fact concerns the **final functions u_k**. The criterion gives only an upper bound for V_k, so the same argument does not yield local vanishing of their Riesz measures. Where W_k is strictly below the affine floor on an open set, the maximum equals a harmonic function there and discards its previous mass. A valid mass-based obstruction would have to control mass that survives in u_k.

Nor do the hypotheses imply a universal bound γ_j≥C r_j with an absolute C>0. In the explicit one-disk example above, keep V_R fixed and choose **any** 0<γ≤R as the drilling coefficient. The plateau constant is zero, so the core radius remains r=R while γ/R can be arbitrarily small.

More precisely, near the interior side of the radius-R circle, u=γ log(|z|/R): its value tends to zero, whereas the affine floor on that circle is at most R−δ<0. By flux through a slightly smaller concentric circle lying in this collar, the Riesz mass inside B(0,R) is exactly γ. On the outer circle the remaining mass is 3R−γ, since the total boundary mass of V_R is 3R. Consequently this example’s total mass on the closed disk is 3R, independently of γ. It has a background cost proportional to R, but its negative component’s interior mass can be arbitrarily smaller than R.

These observations rule out the simplest universal lower bound on drilling mass per core radius. They do not prove or disprove a universal estimate for the total surviving mass of arbitrary admissible backgrounds or families. No such estimate, and no resulting all-height obstruction, is asserted here.

## Disposition and recommended retained statement

Retain the upper-envelope drilling criterion as an authored conditional proposition. The requested proof can be made fully explicit without changing its mathematical mechanism. Use the companion statement's standard compact-containment convention and representative argument when a standalone theorem is desired. Correct the explanatory open-disk threshold to a nonstrict inequality, as recorded above.

Keep the original problem status **UNRESOLVED**. No all-height family satisfying the affine envelope and paid-for nonnegative plateaus has been constructed here. The neighboring source has not been shown to supply that family. No impossibility theorem for the original question follows from this audit.
