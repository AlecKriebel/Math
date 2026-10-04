# Mathematical verdict, sealed before implementation or prior review

Materials read since the source-first seal: candidate SOURCE_GATE.md, TURN_1.md and PRIOR_RESOLUTION.md, plus the independently downloaded original sources. No candidate checker/code, CHECKS JSON, STATE, FINAL_RESULT, publication/author manifests, review output, root/sibling findings, or queue was read before this verdict. Original OWR printed page 2257 was rendered locally and visually inspected. The web screenshot attempt for this page timed out; this is preserved as an acquisition failure, not mathematical evidence.

## Verdict

PASS for the precisely qualified pair of results: (1) the original nonnegative-scalar-curvature and empty/minimal-boundary class has a credited prior resolution, and (2) the broader sentence interpreted as an assertion about all AF metrics admits the supplied counterexample. No gap was found in TURN_1's proof. It establishes a strict lower bound for the supremum, not the exact capacity–volume mass. No novelty or priority is verified.

The original full-paper conjecture is not falsified by this example. This is a mandatory interpretation constraint, already observed explicitly by the candidate. A final or queue disposition that collapsed the two claims into a purported new solution of the original conjecture would fail this review.

## Reconstruction of the example

Take any smooth χ with values in [0,1], χ=0 on [0,2], χ=1 on [3,∞), and put `u=1−χ(r)/r`, `g=u^4δ` on R3. The quotient is defined as zero near the origin. The metric is smooth because χ vanishes on a neighborhood of the only radial-coordinate singularity. `1/2≤u≤1`; hence `(1/16)δ≤g≤δ` and completeness follows from Euclidean completeness. The end is exactly Schwarzschild with parameter −2 and has one AF end, no boundary, O2(r−1) decay and scalar curvature supported in [2,3].

For a radial conformal metric the ADM flux is `−2r²u³u_r`; exterior `u_r=r−2` gives −2. The scalar curvature identity `R_g=−8u^(−5)Δu` is appropriate in dimension three. More explicitly `Δu=−χ''(r)/r` in the transition. Since χ increases from 0 to 1 while χ' vanishes at both endpoints, χ'' is negative somewhere; therefore R_g is negative somewhere. This makes the counterexample's exclusion from the physical hypotheses explicit and checkable, even though the candidate does not need a pointwise location.

The family `K_R=B((R/2)e1,R)`, R≥6, is nested: center displacement between R and S is `(S−R)/2`, and adding the smaller radius gives at most S. It contains `B(0,R/2)`, so every fixed compact set is eventually contained. Its exterior is wholly in r≥3. Thus the interior smoothing contributes to volume only, and cannot change the exterior capacity calculation.

Let `f=1−R/|x−(R/2)e1|` outside K_R. Both f and u are Euclidean harmonic there; direct differentiation yields

`div(u²∇(f/u))=uΔf−fΔu=0`.

In this dimension `Δ_gφ=u^(−6)div(u²∇φ)` and the metric energy density is `u²|∇φ|² dx`. The quotient f/u has the required boundary and infinity values, finite energy, and is the unique capacitary potential by the exterior maximum principle. At infinity its coefficient of 1/r is `−(R−1)`; the normalized metric flux tends to R−1 because u²→1. Therefore `cap_g(K_R)=R−1` exactly. The negative sign of ADM mass does not invalidate this transformation: Jauregui equation (41) precedes the subsequent imposition of nonnegative mass for the volume estimate.

The separate variational upper estimate is also correct: shells of radius ρ≥R about the displaced center have the mean of 1/r equal to 1/ρ, giving the first two terms R−1. The remaining `r−2` term has energy at most `4/(3R)` by `r≥ρ/2`. It is consistent with the exact result and uses the actual metric energy.

Outside the fixed core, `u^6=1−6/r+O(r−2)`. Extending `1−6/r` through the core changes its integral by a finite fixed constant because 1/r is locally integrable. The entire K_R lies in `B(0,3R/2)`; the integral of r−2 over that containing ball is 6πR. Thus the remainder in total volume is O(R), with a constant independent of R. The Newton potential of a solid ball at distance d<R from the origin is

`∫_{B(a,R)} r−1 dx = 2π(R²−d²/3)`.

This follows from the shell mean `1/max(d,ρ)` and integrating at ρ=d, not from an assumption of concentric balls. With d=R/2 the integral equals `(11π/6)R²`. Hence volume is `(4π/3)R³−11πR²+O(R)`. Dividing by 4π/3 gives `R³−(33/4)R²+O(R)`; taking a cube root gives `R−11/4+O(R−1)`. Subtracting the exact capacity gives limit −7/4. Because the mass is a supremum, this one admissible exhaustion proves `mCV≥−7/4>−2=mADM`, with gap at least 1/4.

The general fixed λ∈(0,1) statement also checks out: center λR, normalized capacity `R+m/2`, volume-radius constant `(3m/2)(1−λ²/3)`, and deficit `m(1−λ²/2)>m` for m<0. Positivity of the compactly filled conformal factor must be maintained by placing its transition at a sufficiently large radius if m varies. This generalization is not needed for the explicit m=−2 example.

## Reconstruction of the credited original-class resolution

The three inequalities in PRIOR_RESOLUTION use distinct primary results with compatible scope. Jauregui Theorem 5 gives the lower bound; BFM23 Theorem 5.6 at p=2 gives the capacity/isoperimetric upper comparison without the H2 restriction; Jauregui Theorem 2 and the Jauregui–Lee theorem give `miso=mADM`. PMT supplies the nonnegative sign needed at the vulnerable BFM23 proof step; choosing a positive comparison parameter also covers zero mass. The later Benatti correction and JLU corroborate that qualification. Directly using BFM23 Theorem 1.3 without H2 would be invalid, but the candidate does not do so.

At p=2, BFM normalization reduces exactly to `(4π)^−1∫|Dv|²`, and its cubic mass is `(V−(4π/3)c³)/(4πc²)`. Jauregui Lemma 10 identifies its exhaustion supremum with the radius deficit. Smooth supersets may approximate any compact competitor with capacity error tending to zero; the volume term can only improve under enlargement. The nested selection described by the candidate uses a sufficiently late exhaustion term to contain the previous smooth set, so no nestedness gap remains.

The candidate asserts neither an unproved topology extension nor a new physical-class theorem. The reference to C1 improvement is supporting literature; the original target needs only the C2 theorem. Infinite mass issues do not arise in the original integrable-curvature class, while the broader references permit extended values where explicitly stated.

## Adversarial challenges resolved

* Normalized capacity versus raw energy: all constants agree, Euclidean capacity is radius.
* Smoothness/completeness versus a singular negative Schwarzschild space: compact fill is explicit and uniformly positive.
* Invalid use of negative scalar curvature as a counterexample to the physical class: scope distinction is explicit.
* Displaced balls fail exhaustion or nesting: both inclusions are proved quantitatively.
* Interior contributes an R² volume error: it contributes a fixed finite constant; the exterior remainder is O(R).
* Capacity identity relies on nonnegative ADM mass: the transformation does not; the later volume rearrangement in the source does.
* Supremum needs all exhaustions: an existential exhaustion suffices for a strict lower-bound counterexample; the credited upper comparison covers all exhaustions.
* Quantitative/numerical computations establish a universal assertion: the proof is analytic for all R≥6 and any admissible smooth χ. No sampled checker was used to reach this verdict.
* Topology or connected boundary silently omitted: BFM Theorem 5.6 avoids the H2 requirement, and the original isoperimetric identity has the necessary boundary scope.

Mandatory mathematical repairs: none in the opened candidate mathematical files. Mandatory final-claim constraint: preserve both the credited original-class equality and the unrestricted-statement counterexample, plus unverified novelty and the absence of an exact value for mCV.

Completion at mathematical checkpoint: 55%. Frozen implementation, reproduction, complete JSON, manifests, queue provenance and live/API evidence remain unreviewed. Exact-live approval is pending a later additive final_live gate.
