# Independent audit of the Robin dimension dichotomy

## Decision and exact scope

**ACCEPT for the mathematical claims stated in the reviewed proof.** No unresolved mathematical error was found. In particular, the explicit smooth nonzero compact graph in ambient dimension four, with Robin parameter β=1, has no spectrum below −1. It is a counterexample to the dimension-unrestricted universal binding question. The all-coupling binding theorem for connected smooth compact perturbations in dimensions two and three also passes this audit.

This AI-assisted, unrefereed independent mathematical audit is not external human peer review, journal acceptance, formal proof-assistant verification, or a certificate of literature novelty. The review was performed on 10 October 2026. The distributed [mathematical report](MATHEMATICAL_REPORT.md) has 14,666 bytes and SHA-256 `9db488c626bad1367229603fc45eeff92be5f613c79418f0249dd25032ffe3e5`. This edition preserves all accepted analytic arguments and mathematical qualifications.

The audit recomputed the analytic identities and inequalities, inspected the domain and topology arguments, and checked the exact explicit constants separately from the authored proof. Two minor presentation issues were identified and corrected before the accepted version: the support ball is closed, and the Lipschitz-graph identity is derived directly using the weak chain rule and vertical-fiber integration. Neither changed the mathematical result.

## Original problem and quantifiers

The canonical [AIM Problem 1.4](http://aimpl.org/shapesurface/1/) and its preceding introduction specify an attractive Robin Laplacian on a locally perturbed half-space and ask whether there must be an eigenvalue below the flat threshold. Neither the problem sentence nor its introduction imposes an ambient dimension restriction. The geometric phrase is explained by agreement of the boundary with a hyperplane outside a bounded region.

The reviewed counterexample is a stronger, unambiguous member of that class: its domain agrees with the upper half-space outside a compact set, is connected and smooth, and has connected nonflat boundary. It therefore does not depend on counting the unchanged half-space as a deformation or on allowing disconnected domains, nonsmooth boundaries, or unusual topology.

A single such example in dimension four disproves the dimension-unrestricted universal assertion. If the intended question is instead separately restricted to dimension three, the reviewed positive theorem answers that smooth compact-perturbation version. No classification of every higher-dimensional nongraph perturbation is needed for the counterexample or claimed by this audit.

## Form domain and essential spectrum

The form is correctly defined on H¹(Ω), with a negative boundary term and outward-normal boundary convention ∂νu=βu. The local trace estimate, finitely many charts on the compact perturbed part, and the flat trace estimate imply that the boundary term is infinitesimally form bounded relative to the Dirichlet energy. Thus the form is closed and semibounded. The use of H¹ trial functions requires no Robin condition on those trial functions.

The essential-spectrum argument is valid. Its IMS partition vanishes near all geometric changes, so the exterior-localized function extends to the flat half-space without creating a jump. The flat completed-square identity bounds that exterior piece below by −β². The compactly localized remainder is bounded below by a fixed compactly supported L² error. A singular Weyl sequence below −β² would have bounded H¹ norm, tend to zero locally in L² by Rellich compactness, and contradict this estimate.

Conversely, tangential wave packets can be dilated and translated so that their entire vertical fibers lie in the unchanged half-space. Multiplication by the normalized transverse mode gives functions in the Robin operator domain. Their residuals tend to zero, and their supports escape horizontally. They give every point of [−β²,∞) in the essential spectrum, including the threshold. The proof therefore establishes exactly σess=[−β²,∞).

Theorem B's equality of spectral sets with the essential spectrum does not itself exclude embedded eigenvalues. The proof and its counterexample conclusion correctly assert absence of spectrum below the threshold; they do not claim absence of every eigenvalue at every energy.

## Ground-state identity and nongraph topology

For φ=e^(−βy), independent expansion gives

Q[φv]=∫Ω φ²|∇v|²−β∫∂Ω(1+νy)φ²|v|²,

where Q=q+β²‖·‖². The boundary sign is correct because ∂νφ=−βνyφ. In particular, 1+νy is nonnegative on every boundary component, including obstacle components, and is zero on the unperturbed lower boundary of the upper half-space.

Strict positivity of the total boundary defect is justified in the stated smooth class. If its nonnegative continuous integrand vanished identically, every outward normal would be −ey. Each connected boundary component would then lie in a horizontal hyperplane and be open in that plane. It is also closed in Euclidean space, hence in that plane, and must be the whole plane. Agreement with the half-space outside a compact set excludes every horizontal plane except y=0 and excludes any compact additional component. The smooth one-sided boundary condition, connectedness, and agreement at infinity then force Ω to be the original half-space.

The nongraph trial function φψ(x) belongs to H¹ because the domain is bounded below and the upward tail decays exponentially. Vertical truncation makes the integration-by-parts argument legitimate and has vanishing error. Where the tangential cutoff varies, every vertical fiber is exactly (0,∞); hence its kinetic contribution is exactly (2β)^(−1)∫|∇ψ|². The negative boundary contribution remains fixed and strictly negative. Linear cutoffs in one tangential dimension and logarithmic cutoffs in two have energy tending to zero. The resulting negative shifted form value, combined with the verified essential spectrum, produces a discrete eigenvalue. This covers overhangs and compact extra boundary components without a hidden graph assumption.

## Hardy estimate and weighted trace estimate

The regularized Hardy derivation is correct. With a₀=(m−2)/2 and pδ=x/(|x|²+δ²), expanding the nonnegative square and integrating its cross term produces

∫|∇a|² ≥ ∫[a₀²|x|²+a₀mδ²]/(|x|²+δ²)² |a|².

Dropping the positive δ term and applying Fatou yields the standard constant 4/(m−2)². Consequently a compact set in the closed ball of radius R obeys the local bound with A=4R²/(m−2)². The argument applies precisely when m≥3.

For ρ=e^(−2βt), vertical integration gives

T_K=2βL_K−2 Re∫_(K×R+)ρ w̄∂tw.

Cauchy–Schwarz and the tangential Hardy bound give T_K≤2βAE_x+2√(AE_xE_t). Finally 2√(E_xE_t)≤E_x+E_t yields T_K≤(2βA+√A)E. There is no missing transverse normalization, boundary Jacobian, or weight factor in this estimate.

## Flattening and the all-function lower bound

For the graph y=f(x), its outward normal is (∇f,−1)/√(1+|∇f|²), and its surface measure is √(1+|∇f|²)dx. Thus the boundary defect becomes exactly √(1+|∇f|²)−1.

With y=t+f(x) and u=e^(−β(t+f))w, the Jacobian is one, and the physical gradient of the transformed v is (∇xw−∇f∂tw, ∂tw). The report's direct vertical integration is valid for Lipschitz f and proves the same identity without importing a smooth-boundary divergence theorem.

The coercivity estimate is correct for complex-valued gradients as well as real ones. Writing a=(a−gb)+gb and using the elementary two-term square bound gives

|a|²+|b|² ≤ 2(1+G²)(|a−gb|²+|b|²).

Hence c(G)=1/[2(1+G²)] is a valid lower bound. Bounding e^(−2βf) below in the bulk and above at the boundary produces the factor e^(4βM), with the correct direction of both inequalities. Combining this with the trace estimate yields the sufficient absence criterion in equation (6.3).

The final domain extension is valid. One first works on compactly supported flattened functions. The bi-Lipschitz coordinate change and multiplication by the positive exponential, with locally bounded inverse and derivatives, give a dense form core. Passing to arbitrary H¹ functions uses continuity of q, rather than a false claim that multiplication by e^(βy) is globally bounded on ordinary H¹. Thus the result controls every admissible function, not only a separable ansatz.

For each fixed compact Lipschitz graph the left side of the sufficient criterion tends to zero with β, whereas c(G)>0. This proves a nonempty interval of weak-coupling absence for every such graph when m≥3.

## Explicit smooth counterexample and exact arithmetic

For h(x)=exp(−1/(1−|x|²)) on the open unit ball and zero elsewhere, the standard flat exponential extension proves smoothness across the sphere. The function is nonzero and compactly supported. If q=(1−r²)^(−1), then

|∇h|=2rq²e^(−q)≤2q²e^(−q)≤8/e²<2.

The maximum of q²e^(−q) on q≥1 occurs at q=2. Thus f=h/100 satisfies M<1/100, G<1/50, and D<1/5000. For m≥3 the choice R=1 gives A≤4. At β=1 the authored bound is less than 1/250, while c(G)>1/3, leaving a positive margin greater than 247/750.

An independent exact rational check gives a stronger bound: the power series implies exp(1/25)≤25/24, so the absence coefficient is below 1/480, whereas c(G)>1250/2501. The analytic proof above establishes absence of spectrum below the threshold.

The graph domain is diffeomorphic to the half-space by (x,t)↦(x,t+f(x)); its boundary is diffeomorphic to R^m. Its symmetric difference from the half-space is bounded. The dimension-four example therefore satisfies every nontriviality, smoothness, and connectedness condition needed for the claimed counterexample.

## Literature and provenance limits

The planar precedent was checked in [Exner–Minakov, arXiv:1406.7624](https://arxiv.org/abs/1406.7624), Section 5, Theorems 5.1 and 5.2. It is correctly credited. The concave asymptotic-wedge absence result does not concern a nontrivial same-line compact perturbation. The strong-coupling result in [Pankrashkin–Popoff, arXiv:1502.00877](https://arxiv.org/abs/1502.00877), Corollary 1.6, has a large-parameter quantifier and is compatible with weak-coupling absence.

The September 2026 primary abstract of [Barseghyan–Schneider–Zhang, arXiv:2609.03783](https://arxiv.org/abs/2609.03783) explicitly includes a magnetic field and does not establish the present unmagnetized counterexample.

[Lotoreichik's Trier 2017 talk](https://aamp.fjfi.cvut.cz/lotoreichik/Trier2017.pdf), printed slide 15, was also inspected visually. It records expectations about related problems, not a Robin theorem with proved hypotheses. Its previously defined β is a deformation amplitude. The higher-dimensional δ-interaction expectation in the preceding box must not be relabeled as a proved Robin absence theorem. This source neither supplies a proof of the reviewed result nor invalidates it.

The original source was read as recorded in [SOURCE_METADATA.json](SOURCE_METADATA.json). Its retained HTML was retrieved over plain HTTP after an HTTPS certificate failure was not bypassed; it was not authenticated by a new HTTPS retrieval in this audit. The recorded targeted searches were bounded and do not establish novelty or exhaust every later source. Edition preparation claims no new scholarly-source retrieval, source-file rehash, source inspection, or literature search.

## Final acceptance conditions

The distributed report is mathematically accepted for Theorems A and B and its explicit counterexample. Preserve the stated smooth compact-perturbation scope for the nongraph positive theorem, the compact Lipschitz-graph scope for the higher-dimensional absence theorem, the distinction between absence below threshold and absence of all point spectrum, and the explicit lack of a novelty certificate. Any substantive proof revision requires another hash-bound review.
