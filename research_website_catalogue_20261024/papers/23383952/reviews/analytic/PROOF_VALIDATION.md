# Analytic closure after the independent initial seal

This note closes the attacks in INITIAL_LEDGER.md using direct derivations, exact arithmetic and actual primary interfaces. No old support audit or sibling scientific conclusion was used. The independent initial objects remain unchanged.

## Geometry and normalization

The smooth step's denominator is positive in all three regions x≤0, 0<x<1 and x≥1. Its endpoint flatness follows from every derivative of exp(−1/x) tending to zero as x↓0, while the other denominator term is smooth and positive near that endpoint. Consequently all derivatives of χ at0 and of1−χ at1 vanish. Composition with log cosh gives the claimed all-order seams. The corner of |s| occurs in a neighborhood on which q<0 and u≡1, so no derivative singularity reaches u.

At each missing pole put ρ=exp(−|s|). Then `ds²+gS²=ρ^-2(dρ²+ρ²gS²)` and `sech²(|s|−L/2)=4e^Lρ²/(1+e^Lρ²)²`. The resulting metric factor and its ratio to the round metric are positive smooth functions of ρ². Thus these are ordinary Cartesian smooth poles, not conical or merely weak extensions. There is no limit L→∞ in the proof: e^10000 is finite and the compact smooth metric and conformal multiplier have bounded derivatives, positive minima and finite maxima.

On each cap q∈[0,1], u≤1; on q≥1, u³≤8e^-3q. Hence its integral is `<1+8/(3e³)<2`. The central cylinder contributes exactly L to the radial integral. This proves the volume inequality, and `a^(3/2)=2π²/VL` proves the normalization. The time is positive and finite even though the exact positive integral VL has not been numerically evaluated.

## Closed forms and all-index min–max

The actual Ammann–Jammes8Dec2008 author manuscript, Eq.(6) on PDF4 and its conformal-Laplacian example on PDF5–6, has order-two conformal bidegree ((n−2)/2,(n+2)/2) under metric change f²g. Substituting f=√W and n=3 gives exactly the note's covariance exponents. The original OWR problem independently states the equivalence of the weighted fixed-space operator and the geometric conformal Laplacian. Thus neither a W versus W² substitution nor a volume-measure mismatch is hidden in the transfer.

U=W^(3/4) preserves L² norms under dVh=W^(3/2)dV0. Its smooth positive multiplier and inverse preserve H¹. Pullback of the positive closed round form gives the stated weighted form and the bound `qW[f]≥3/(4 maxW)||f||²`. Smooth compact ellipticity supplies compact resolvent, an orthonormal eigenbasis and positive-time trace finiteness. These are standard compact elliptic facts, not numerical assumptions. Negative transition scalar curvature cannot create a negative eigenvalue of the conformally identified positive operator.

For completeness, the required min–max inequality can be proved directly from that eigenbasis. For any k-dimensional trial space S, S contains a nonzero vector orthogonal to the first k−1 eigenfunctions. Its Rayleigh quotient is at least λk. If every quotient in S is ≤μk, then λk≤μk. The extended sine functions define just such a space: their zero function traces remove the boundary term in their distributional first derivatives. Their derivatives are square integrable, so they are in H¹; no assertion of H² membership is required. Because the metric and potential on their entire supports are exactly cylindrical, their norm and form pairings are the usual diagonal sine pairings. The possible derivative jump is irrelevant for the form calculation.

The trial bounds hold for every positive integer k and the full eigenvalue list including multiplicity. Exponentials are decreasing, giving a heat-trace lower bound for every finite initial sum. Passing to the monotone limit does not require a uniform-in-k error estimate. The Gaussian integral comparison then gives the entire infinite lower sum. Extra nonconstant S² modes need not be counted; omission only weakens this lower bound.

The constant rescaling sends Yg to a^-1Yg because both the positive Laplacian and scalar curvature scale that way. At t*=4a, the correct prefactor is `8a^(3/2)=16π²/VL`. Keeping this factor yields precisely `√π/e (L−4√π)/(L+4)`. Each rational substitution preserves its inequality direction because all factors are positive. The independent Fraction calculation verifies the exact displayed lower rational and its positive margin over13/20.

## Round spectrum, Poisson identity and complete time partition

For S³, restrictions of homogeneous harmonic polynomials of degree l have eigenvalue l(l+2). Their dimension is `binom(l+3,3)−binom(l+1,3)=(l+1)²` (with the second term zero for l<2). This derives the full `j²−1/4` Yamabe spectrum and j² multiplicities used in the note.

The theta identity can be obtained without treating it as an opaque numerical import. Periodize exp(−t x²) over the integers. Its Fourier coefficients, by the Gaussian Fourier integral with frequency2πm, are `√(π/t)exp(−π²m²/t)`. Gaussian absolute convergence gives its Fourier series and evaluation at zero. On any compact positive-time interval, differentiation term by term is uniform. Differentiating the theta identity and using evenness gives

`Σj≥1 j²exp(−tj²)=√π/(4t^(3/2))[1+2Σm≥1(1−2π²m²/t)exp(−π²m²/t)]`.

This verifies the coefficient and correction sign. In the small-time range all corrections are strictly negative and absolutely summable. Dropping them gives a valid upper bound over the whole open interval approaching zero, rather than a sampled estimate.

On [7/5,2], A is increasing and each term in B is decreasing. For every j≥3 and a≥7/5, the consecutive tail ratio is at most `(16/9)e^-7a`. The elementary bound e^x≥1+x already makes this `<1/2`, uniformly. Thus the full infinite j≥3 tail is bounded by twice its first term. Using A at the right endpoint and D at the left gives the six enclosing expressions. Their closed intervals cover the whole middle range, sharing endpoints without gaps. For t≥2 all full summands are nonincreasing, including the first whose derivative vanishes exactly at2, so the already-bounded value at2 controls the entire large-time range.

The independent exact checker uses a different Machin identity,30-term arctangent brackets, integer isqrt root brackets at scale10^10, degree60 reciprocal exponential bounds and degree18 positive-exponential tails. Every resulting interval bound is below the corresponding printed ceiling, not merely below the final321/500 threshold. It separately verifies the lower rational, exact margin, cap inequality and finite-time attainment comparisons. Both it and the fully read deposited pure Fraction checker passed in normal and optimized Python. No heat-trace grid, cylinder discretization or finite eigenvalue approximation is substituted for any of these universal arguments.

## Maxima and boundary cases

The original OWR problem's exact weighted-operator expansion on printed422 gives leading coefficient `(4π)^(-n/2)∫W^(n/2)`. Applied to the fixed smooth positive normalized W and to W≡1, it gives the same zero-time limit √π/4. This is also the usual leading heat coefficient of a smooth compact Laplace-type operator; the potential affects later coefficients. The scope is a fixed L and fixed smooth metric, so no uniformity in a degenerating cylinder family is being claimed.

For t≥1, termwise positivity yields the stated spectral-gap bound on the entire trace. Its product with t^(3/2) tends to zero. On compact positive-time intervals the heat series is continuous. The weighted witnessed value is strictly above its zero-time limit. The round first mode at2 is also above that limit; the independent rational bounds verify this and the alternate128>πe³ inequality. Each supremum is therefore achieved away from both endpoints on a compact positive-time interval. Neither maximizer must equal the supplied t*, and uniqueness is not asserted.

The case W≡1 remains equality with itself; L=0 or an infinite L is not part of the construction. The certificate at a shorter length such as10 fails the stated coarse lower-bound threshold, which is a diagnostic of this certificate rather than a proof that no short-cylinder counterexample exists. Dimensions n≥4 and the separate monotonicity conjecture remain outside the theorem. No nonnegative-scalar-curvature condition, singular-weight extension or numerical representability hypothesis is introduced.

## Exact primary question and bounded related results

The actual74-page OWR2009 report was read at physical PDF67–68, printed421–422, item16. It states precisely the round-sphere positive smooth W, volume-power normalization, fixed-space symmetric weighted operator and maximum-over-all-positive-times comparison for n≥3. Its next conjecture starts at n≥4. Thus the constructed n=3 counterexample addresses the literal first question and does not silently change its category. The manuscript's attribution and scope limitation are faithful.

Ammann–Jammes's actual8Dec2008 author body directly supplies the conformal formula and the established long-cylinder context; its PDF3 and7–8 also attribute the earlier Pinocchio construction. Its own theorem is about normalized first-positive-eigenvalue suprema, not this heat-trace maximum. No theorem about the present trace functional is attributed to that paper. The2007 arXivv1 and final journal/chapter are not asserted byte-identical to the actual15-page author body read here.

The accessible author-uploaded Morpurgo2002 web transcription was read at its introduction's transformed functional and Section4 Theorem4.1/Corollary4.2. The admissible Ψ is convex, continuous and subject to a specific origin-integrability condition; the functional is a Laplace-transformed trace/zeta family. A delta selecting one heat time is not in that class. These passages do not directly assert the conjectured time-maximum comparison. This is a bounded theorem-interface observation, not certification of all external proofs or proof that no other result implies the answer. The final Duke PDF was not authenticated; no byte hash or final-edition equivalence is asserted for a web transcription. Historical priority and current worldwide openness remain unknown.

Conclusion of this analytic lane: the full original finite theorem and attainment claim are supported by the explicit smooth construction, closed-form spectral argument, complete all-time enclosure and exact checks. No unresolved central analytic gap or required source repair was identified. This is a human-checkable mathematical assessment using standard imported compact elliptic facts, not formal proof certification, novelty clearance or publication authority. Root must combine the separate scientific lanes.
