# Independent adversarial review: Toda stopping time, 8000011 / AMR-079-0011

Review date: 2026-10-03 UTC. Scope: the frozen five-author-turn packet only, with local independent verification and adversarial controls. No sixth author search/proof turn, remote mutation, novelty assertion, publication, or human-peer-review claim is made.

## Verdict

**PASS for the scoped partial theorems, with one minor computational-reporting correction. The original general-dimension, positive-tolerance expected-time problem remains unresolved, at 5/5 author turns.**

No mathematical blocker was found in the deterministic envelopes, the fixed-n two-term expectation asymptotic, the exact n=2 quadrature, or the fixed-positive-tolerance bounds and all-positive-moment theorem. The proofs concern the first simultaneous all-coupling crossing throughout. They do not establish a general-n finite-tolerance mean formula or a uniform growing-dimension result.

The exact reviewed packet is `../random_toda_lattice_8000011/packet`. Its `FROZEN_MANIFEST.json` has SHA-256

`f14c8548f3e51fafedb80b4af3149979b283d513f572a91b2c521434f4131a24`.

All 24 bound files and all five per-turn manifests verify. All four supplied scripts replay with byte-identical stdout in this environment. The original packet has not been edited. The companion `REVIEW_MANIFEST.json` binds this report, the independent checks, their recorded outputs, the replay receipt, the source-inventory hashes, and the review verifier.

## Required correction and presentation advice

1. **Required reporting correction, not a theorem correction:** the author packet's “2,559 assertions” are 2,559 exact equality/inequality comparisons, represented by 2,238 executed Python `assert` statements. Turn 1 counts each side of a chained inequality separately: its 642 comparisons occupy 321 executed assertions. Turns 3 and 5 contribute 55 and 1,862 assertions/comparisons. Future summaries should say “2,559 exact finite comparisons” or explain that counting convention. No test failure or mathematical consequence follows.
2. **Recommended citation precision:** for independence and the spectral weights, cite Dumitriu–Edelman Corollary 2.2 and Theorem 2.12, alongside Theorem 2.1 for the GOE tridiagonal construction. The existing attribution is broadly correct but less precise than it could be.
3. **Recommended disclosure:** keep the precise theorem statements rather than percentage estimates such as “25% toward the full target.” Such percentages have no mathematically calibrated interpretation.
4. Retain all present scope qualifications: fixed n for the two-term expansion; n=2 for the quadrature; fixed epsilon>0 for the moment claim; no unverified priority claim; and no identification of first crossing with eventual permanence. The frozen packet may be retained with this review as an erratum rather than rewritten.

## Source and model audit

The local primary reading copies and extracted target were inspected. The source inventory records their hashes; it does not redistribute PDFs. This was a source-verification audit of supplied material, not a new literature search.

- Deift, *Some Open Problems in Random Matrix Theory and the Theory of Integrable Systems* (2007), Problem 11, printed pp. 8–9, explicitly starts with average random-matrix diagonalization complexity, specifies Gaussian diagonals and chi_(n−j) off-diagonals, gives J'=[B,J] with positive upper off-diagonal B entries, and asks for all couplings below a specified positive tolerance. It additionally suggests one-end deflation. The imported exact problem chooses the all-coupling stopping rule. Neither source supplies the claimed two-term asymptotic or specifies that a fixed-n small-tolerance answer would complete the general request.
- The source does not specify the diagonal variance in that passage. The packet correctly declares, rather than quotes, the convention a_i~N(0,2), b_i~chi_(n−i), independently.
- Dumitriu–Edelman's supplied arXiv text, Theorem 2.1, Corollary 2.2, and Theorem 2.12 support the tridiagonal construction and the independent first-row spectral weights. Their convention has diagonal variance 1 and off-diagonals chi/sqrt(2). Multiplication by sqrt(2) gives the packet's exp(−sum lambda²/4) density. Squaring normalized independent chi_1 coordinates gives Dirichlet(1/2,...,1/2). Ordering the eigenvalues does not destroy independence or exchangeability of those weights.
- The supplied Deift–Trogdon paper defines first-row 1-deflation through a squared row norm and gives its large-N distributional theorem in the stated log(epsilon^−1)/log N >= 5/3+sigma/2 region. It is not a theorem about all-coupling first-crossing means. Neither a different stopping rule nor convergence in distribution determines the current mean.
- The imported prior report is qualitative and explicitly limited. Its lack-of-literature statement is not a novelty certificate. This review does not independently recertify every remote repository search or the full 2025 monograph, which is not supplied in full. The packet itself already limits those claims appropriately.

For the chosen clock, the first component q_j of an eigenvector evolves as q_j'=(lambda_j−a_1)q_j. Thus w_j'=2(lambda_j−a_1)w_j and the weights are proportional to w_j(0)exp(2lambda_j t). This verifies the factor 2 in the tau functions directly from the Lax equation. The entrywise equations are a_i'=2(b_i²−b_(i−1)²) and b_i'=b_i(a_(i+1)−a_i), so the long-time coupling exponent is the adjacent gap d_k, not 2d_k or d_k/2. The independent exact checks verify these identities against Gram determinants and reconstructed characteristic polynomials.

## Turn 1: deterministic envelope and stopping rule

**Pass.** The Hankel determinant formula is the Cauchy–Binet expansion of the finite discrete moment matrix. Every term is positive. For t>=0 the subset of the k largest eigenvalues is the unique maximizing exponent, including k=n. Therefore A_k exp(2S_k t) <= tau_k <= tau_k(0)exp(2S_k t), and M_k>=1 with M_0=M_n=1.

Substitution into b_k²=tau_(k−1)tau_(k+1)/tau_k² gives exactly L_k exp(−d_k t) <= b_k <= U_k exp(−d_k t). Every time in the stopping set satisfies the lower bound; every time strictly above the stated upper bound lies in the stopping set. Taking infima handles the strict inequality and does not require the stopping infimum itself to belong to the open set. The bound |T−ell/d|<=H/d for epsilon<=1 follows by choosing a smallest-gap index for the lower side and d_k>=d for the upper side.

The formulas involving d exclude n=1, which the packet handles separately. Positivity of b_k and simple spectrum hold almost surely. Initial-below-threshold trajectories can have T=0 and rise above threshold later, so fixed-time survival indicators are invalid. The supplied n=2 negative control is correct.

## Turn 2: collision and weight-tail integrability

**Pass.** Partitioning the ordered chamber by a minimizing adjacent gap cancels exactly one Vandermonde factor against 1/d. On each cell the remaining factors have polynomial growth. In coordinates g=lambda_(j+1)−lambda_j and c=(lambda_(j+1)+lambda_j)/2, the Gaussian contribution from the pair is exp(−c²/2−g²/8), with Jacobian magnitude 1. On 0<g<1, the remaining product is bounded by a polynomial in c and the other coordinates, uniformly in g. Dropping ordering constraints gives an integrable Gaussian-polynomial majorant times integral_0^1 |log g| dg.

This covers multiple collisions: uncancelled Vandermonde factors vanish, and create no inverse factors. On d>=1 the collision logarithm vanishes. Gaussian growth control also handles log(2R). Independence permits E[W/d]=E[W]E[1/d], and each Beta marginal has a finite absolute logarithmic moment at both endpoints.

The algebraic envelope is valid: all pairwise differences lie between d0 and 2R; |log A_k|<=K; tau_k(0)<=binomial(n,k)(2R)^(k(k−1)); log M_k<=n log 2+2K; |log c_k|<=2K; and H<=4K+n log 2. Thus the deterministic error has an integrable majorant and the claimed bounded mean-error theorem follows. No unproved uniform integrability is hidden here.

The optional inverse-gap moment remark is also correct. On an isolated collision the density behaves as a positive constant times g dg, so the inverse p-th gap moment has local integral g^(1−p)dg: finite for p<2, divergent for p>=2. This is an eigenvalue-gap statement, not a moment statement for a fixed-tolerance first crossing.

## Turn 3: two-term mean asymptotic

**Pass.** T(epsilon) tends to infinity for every fixed positive Jacobi sample as epsilon decreases to zero, because the maximum coupling has a strictly positive minimum on every compact time interval. Factoring the dominant terms of the finite exponential sums yields both b_k~c_k exp(−d_k t) and b_k'/b_k→−d_k. The derivative statement is justified directly and does not differentiate an arbitrary little-o.

Distinct adjacent gaps tie only on a finite union of proper linear hypersurfaces. Hence the slowest coupling is unique almost surely, eventually strictly maximal, and eventually strictly decreasing. For sufficiently small sample-dependent epsilon, no earlier crossing is possible and the first simultaneous crossing is the scalar outgoing crossing in that eventual regime. This gives T−ell/d→log(c_(k*))/d.

The same integrable envelope from Turn 2 dominates the centered stopping time for every epsilon<=1, so dominated convergence is legitimate. The sample-dependent time needed to separate nearly tied gaps need not itself have an integrable bound; it is not used as the dominating variable. Thus near-tie events are not a missing singularity.

Cancellation of the dominant Vandermonde factors gives exactly

c_(n−r)=d sqrt(w_r/w_(r+1)) product_(j=r+2)^n (lambda_j−lambda_r)/(lambda_j−lambda_(r+1)).

The minimizing index r depends only on the eigenvalues. The log weight ratio divided by d is absolutely integrable, and its conditional expectation is zero by exchangeability and independence. The stated eigenvalue-only B_n is therefore justified. For n=2 the radial density d exp(−d²/8)/4 gives C_2=sqrt(pi/8) and the logarithmic Mellin derivative gives B_2=C_2(log 2−EulerGamma)/2. Both factors agree with the chosen clock.

This is a fixed-dimension theorem. It does not license any simultaneous dimension limit, any exchange with second moments, or a finite-epsilon equality for n>=3.

## Turn 4: exact n=2 quadrature and boundaries

**Pass.** Put u=(a_1−a_2)/2 and v=b_1. Then u is standard normal and v an independent absolute standard normal. The radial coordinate R=sqrt(u²+v²) is Rayleigh, d=2R, and the angle is uniform on a half-circle. For x=u/R=tanh s this gives density sech(s)/pi, independent of d. The ODE x'=d(1−x²) gives b(t)=(d/2)sech(dt+s).

For d>2epsilon, set A=arcosh(d/(2epsilon)). Initial coupling below epsilon is precisely |s|>A, where the first-crossing infimum is 0. If |s|<A, the first crossing has infimum (A−s)/d. Integration over the symmetric truncated s interval cancels the odd term. The resulting factor P(|s|<A)=2 arccos(2epsilon/d)/pi yields the packet's integral with coefficient 1/(2pi).

The measure-zero equality cases deserve explicit distinction if this is ever stated as an all-initial-data trajectory formula: at s=−A with A>0, b(0)=epsilon and initially increases, so the strict first crossing has infimum 2A/d; at s=A the infimum is 0. If d=2epsilon, including s=0, the infimum is 0. The packet already excludes the boundary in (11), so this is not a defect in the expectation theorem.

Endpoint convergence is rigorous. With h=d−2epsilon down to zero, each inverse function is asymptotic to sqrt(h/epsilon), so their product is h/epsilon+O(h²) for fixed epsilon>0. The integrand vanishes linearly at its lower endpoint. At infinity it is bounded by a constant times exp(−d²/8)(1+log d), which is integrable. No principal-value interpretation or cancellation of divergent integrals is needed.

The independent original-Gaussian-coordinate double integral agrees numerically with the radial quadrature at epsilon=0.1, 1, and 3. These calculations and the small-epsilon residuals are diagnostics, not validated quadrature error certificates.

## Turn 5: Lyapunov budget, all moments, and bounds

**Pass.** The exact telescoping identity F'=-2 sum b_i² has the stated sign. For every t<T at least one coupling is >=epsilon, even on trajectories that subsequently re-cross thresholds. Hence 2epsilon² t<=F(0)−F(t)<=F(0)−F(infinity). The latter finite budget excludes an infinite T and gives T<=[F(0)−F(infinity)]/(2epsilon²). Centering the index vector and using conservation of Frobenius norm gives F(0)−F(infinity)<=2QS, and therefore T<=QS/epsilon².

This is a deterministic finite-tolerance bound with no inverse spectral gap. Every positive moment of S is finite for the independent Gaussian/chi entries, so every positive moment of T is finite for each fixed n and epsilon>0. The conflict with E[d^−2]=infinity is only an invalid exchange of limits; the packet correctly avoids it.

For (16), E[F(0)]=0 and the descending sorted limit gives the factor 1/4 after using E[trace J]=0. These expectations are integrable by the norm bound. For (17), the coefficient vector 2j−n−1 has squared norm n(n²−1)/3; E[sum(lambda_j−mean lambda)²]=n(n+1)−2; Cauchy–Schwarz, including its expectation form, yields the displayed constant exactly.

For (18), diagonal entries are convex combinations of the spectrum, so b_i'/b_i>=−rho. Applying the inequality to an initial maximizing coupling gives the lower bound at every point of the stopping set and then at its infimum. Its expectation is finite because it is bounded by T, already proved integrable.

For (19), T vanishes on the strict initial-below-threshold event. Cauchy–Schwarz applies to S times its complementary event; it does not assume S and that event are independent. The chi-CDF product uses precisely the independent initial couplings. Equality at the deterministic epsilon has probability zero. Standard chi tails give Gaussian high-tolerance decay after taking the square root, with n-dependent polynomial factors; no asymptotic equivalence is asserted.

Finally, J_c(t)=cJ(ct) satisfies the same quadratic Lax ODE, so T_(cJ)(epsilon)=c^−1 T_J(epsilon/c). A change in generator normalization is a separate clock change. This scaling also predicts C→C/c and B→(B+C log c)/c, consistent with the spectral formulas.

## Independent verification evidence

The independent exact script uses Fraction arithmetic, direct Hankel determinants, subset tau expansions, differentiated sums, and characteristic-polynomial recurrences. It passes **2,049 exact predicates over 60 spectral samples**. Samples include mixed/negative spectra, spectral translations through widely separated locations, rational tiny gaps, exact tied smallest gaps, near ties, and weights as small as 10^−60 before normalization. Ties are valid for deterministic checks; the almost-sure uniqueness step is handled analytically. These checks support identities and signs; they do not replace the all-data arguments above.

The independent floating script passes **47 numerical predicates**. It compares quadrature in spectral coordinates with quadrature in the original independent Gaussian/half-Gaussian coordinates, checks endpoint behavior and strict incoming-boundary behavior, and compares direct ODE integration with tau evaluation. No computation here is presented as a rigorous interval certificate.

A useful n=3 negative control has a(0)=(-2,0,2), b(0)=(0.1,1), epsilon=0.5. Numerically the maximum of the individual first-crossing times is about 0.9796960323, whereas the first simultaneous crossing is about 2.7173606580. At the second coupling's first crossing the first coupling is about 1.9808281216. This strongly exposes the forbidden stopping-rule substitution; direct ODE/tau discrepancies were below 4e−12 on the sampled interval. The analytic review does not rely on this numerical example.

## Classification and stopping condition

All stated partial mathematical results survive independent audit. No unresolved mathematical correction is needed to retain them with their existing restrictions. The exact finite-epsilon expected stopping time for arbitrary n>=3, or another comparably sharp general characterization answering the original average-complexity request, has not been determined. The original remains unsolved at the exhausted five-turn cap. No further author attempt, remote publication, source-wide novelty claim, or automatic promotion to solved status is authorized or implied by this review.
