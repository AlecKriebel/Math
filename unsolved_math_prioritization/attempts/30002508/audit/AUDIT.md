# Independent adversarial audit: Nyman–Beurling cutoff distances

Problem 30002508 / OWR-12866-018 / campaign rank 624. Audit date: 2026-10-04 UTC.

## Verdict

**Accept as a correct partial-results packet, with a minor source-provenance clarification. The full target remains unsolved.**

No substantive mathematical error was found in the frozen proofs. In particular, the Möbius witness genuinely separates the target from every finite-cutoff closed span. It does not prove a strictly decreasing distance between arbitrary cutoffs. The controls independently reproduce the claimed exact constants. Neither computation nor the fixed-tuple literature bridges the infinite-dimensional gaps.

The audit additionally proves right-continuity at the endpoint 1. This small strengthening does not settle right-continuity at any arbitrary interior cutoff or strict decrease between arbitrary cutoffs greater than 1.

The original PROOF.md was bound, before reading, to SHA256

`6a2176d75e5bd5c53ccb75fd085674f272fefabf95046b56de82d9f79fe289d3`.

All seven entries of the original SHA256SUMS passed. Frozen originals were not changed; copied inputs are included for portable reproduction. No remote writes were made.

## 1. Target and source checks

[Oberwolfach Report 06/2014](https://ems.press/journals/owr/articles/12866), printed p. 390, section 8, was checked in the existing publisher web-text extraction. It concerns the distance from χ to dilates with the real interval of parameters 1 ≤ α ≤ λ in L²((0,∞),dt/t²), and asks continuity and strict decrease. Closing the span leaves its infimum distance unchanged.

There is one provenance qualification. The publisher extraction renders the lower domain endpoint as λ > 1, while an unsolicited search-result extract of a repository copy renders λ ≥ 1. It similarly differs on the immaterial point value χ(1). A cached-page screenshot failed with cache miss. No source PDF was downloaded, no alternate copy was opened, and no download-denial workaround was attempted. Exact printed relation-sign/overline typography was therefore not visually verified. The supplied target λ > 1 is clear; the endpoint is handled separately below. See CORRECTIONS.md.

[Jousse 2005](https://aif.centre-mersenne.org/item/10.5802/aif.2127.pdf) was checked at Definitions 18–19 (p. 1400), the setup and Mellin identity (p. 1402), and Theorem 7/Corollary 1 (pp. 1404–1405). Admissibility means continuity of the projection for each fixed finite tuple, including collisions. The corollary attains the optimum for n terms with parameters in [0,1] and strictly improves it for n+1 terms. Under t=1/x, θ=1/a, this supports fixed-n continuity in the packet. It does not state the full cutoff conclusion.

Targeted current searches did not identify a verified resolution of the two exact cutoff questions. This is a bounded search, not a comprehensive literature-status theorem. No claim in the verdict depends on treating the 2005 paper or a different discretized Nyman–Beurling problem as the target.

## 2. Claim-by-claim attack

### Strong parameter continuity, left continuity, and right limits: pass

For a in a compact positive interval, min(t/a₀,1) is a valid square-integrable majorant in dt/t². The exceptional integer-multiple set has measure zero, so dominated convergence proves norm-continuity of e_a.

The equality E_λ = closure(union over 1<r<λ of E_r) is valid for λ>1. It includes the endpoint generator by an increasing sequence of smaller parameters. Consequently D is nonincreasing and left-continuous. It can only have downward right jumps, and at most countably many of them.

For decreasing closed subspaces V_n, the projection identity ||p_n-p_m||²=||p_n||²-||p_m||² for m≥n proves strong convergence to the projection onto the intersection. Applying it to E_(λ+1/n) validates formula (1). In particular the exact necessary-and-sufficient condition for this target's right continuity is

P_(E_(λ+) ∩ E_λ^⊥) χ = 0.

Equality of the two subspaces is sufficient but stronger. Individual-generator continuity proves neither assertion. As an independent negative control, in R² the continuous family g_a=(1,max(0,a-2)) has one-dimensional span through cutoff 2 and full two-dimensional span after every cutoff 2+h. Its distance from (0,1) has a right jump. This example is not claimed to satisfy Jousse's stronger fixed-tuple theorem.

### Local Möbius transform and closure: pass

C(f)=∫₀¹ f(t)dt/t is bounded, with norm 1. For every vector of E_λ, the restriction below 1 equals C(f)t, because restriction is bounded and that one-dimensional restriction space is closed.

Put F(t)=C(f)t-f(t) for t≥1 and F(t)=0 below 1. Then the packet's T is exactly the finite dilation convolution

Tf(t)=Σ_(n≤t) μ(n)F(t/n).

On [1,R], its norm is bounded by

||f|| Σ_(n≤R) |μ(n)| [sqrt(R-n)/n + n^(-1/2)].

This is a local bound only, which is all the proof requires. For a generator the elementary divisor identity gives Te_a=1_[a,∞), almost everywhere. For finite sums with parameters at most λ it is constant after λ. Local boundedness of T and closedness of the constant functions on each finite tail interval pass that property to the closed span. Constants agree on overlapping intervals. The packet does not assume a nonexistent global bound for T.

If a>λ, Te_a has a nonconstant step inside (λ,∞); hence e_a is outside E_λ. This proves strict space inclusion for every λ<ν. Separately, Tχ=-M(t) has a nonzero jump at every prime, so it is not eventually constant. Therefore χ is outside every finite-cutoff E_λ. Closedness then gives a strictly positive distance. All these conclusions are unconditional.

### Formula (5), rational witnesses, and the exact range: pass

Expand L before changing variables:

L(f)=C(f) Σ_n μ(n)/n ∫_n^∞ tψ(t)dt − Σ_n μ(n)∫_n^∞ ψ(t)f(t/n)dt.

The substitution t=nu in the second term supplies the factor n and restricts u≥1. Converting Lebesgue integration to the H inner product supplies u². Thus the sign, factor n, lower cutoff, and below-1 term A in (5) are all correct. The witness is in H and is the Riesz vector for L on the entire H, not just the generator span.

One useful independent exact identity is, for every real a≥1,

⟨e_a,h⟩ = max(0, 1 − |a−q|/ε).

It follows directly by integrating ψ against Te_a=1_[a,∞). This confirms zero pairing throughout a≤q−ε, unit pairing at q, and nonzero pairing immediately after q−ε. It also confirms the exact boundary of the claimed cutoff range; one cannot extend that range to q.

For an integer center m with ε<1, ⟨χ,h⟩=−μ(m). Prime centers give +1. A squarefree composite can give −1 with the same valid squared lower-bound mechanism; a squareful center can give zero. A noninteger center with no integer in the support also has zero target pairing despite separating its center generator. This is an explicit obstruction to converting the witness's generator separation into target improvement.

The q=2, ε=1/4 norm is exactly 32155/768, so the displayed bound 768/32155 is correct. The other four original prime-centered constants agree exactly. Rationality follows from a finite rational partition and integration of quadratic pieces, not from numerical approximation.

### N_λ, local versus global approximation: pass, with an extra endpoint result

N_λ is closed: it is the intersection of the closed below-1 restriction condition and the preimages of closed constant-function spaces under each finite restriction of T. E_λ⊆N_λ and intersection_(ε>0) N_(λ+ε)=N_λ are valid. Hence E_(λ+)⊆N_λ. No proof of E_λ=N_λ for general λ is present or inferred.

For clarity, local inversion recovers values on a fixed finite interval. It does not bound the H norm of reconstructed approximants on the full half-line. Compact parameter support, bounded Hilbert norm, and local convergence of recovered coefficients do not by themselves supply that missing global estimate.

At λ=1, however, the necessary condition is sufficient. Here is a complete extra proof.

For f∈N₁ write Tf=K almost everywhere on (1,∞). Finite divisor inversion gives

Σ_(n≤t) Tf(t/n) = F(t),

because the coefficient of F(t/k) on the left is Σ_(d|k) μ(d), which vanishes except at k=1. Countably many dilation preimages of exceptional null sets remain null. Thus F(t)=K floor(t) almost everywhere above 1 and

f(t)=(C(f)−K)t + K{t}.

If C(f)−K were nonzero, the bounded fractional-part term could not cancel its linear growth; the H norm would diverge on the tail. Therefore C(f)=K. The below-1 restriction now gives f=Ke₁ on the whole half-line, so N₁=E₁. Since E₁⊆E_(1+)⊆N₁, equality follows and D is right-continuous at 1. This addresses only that endpoint.

### Plateau and dilation identities: pass

For nested closed subspaces, the orthogonal decomposition E_ν=E_λ ⊕ (E_ν∩E_λ^⊥) validates (8). The residual r=χ−P_(E_λ)χ is already orthogonal to E_λ. Equality of distances is equivalent to r being orthogonal to all added generators, as in (9). With v=(I−P_(E_λ))e_a, (10) follows by the rank-one projection formula. Strict inclusion proves ||v||>0; it gives no nonzero numerator.

The dilation U_a f(t)=sqrt(a) f(t/a) is unitary for dt/t², and U_aE_λ is the span of the parameter interval [a,aλ]. Projection of 1_(1/a,1) onto E_λ equals (log a)P_(E_λ)z, with the inner-product convention used in the packet. Expanding the square proves (11), including the sign and factor e^(−s).

The derivative at zero is 2B−Q. Since |B|≤D and Q=1−D², it is negative if D<sqrt(2)−1. This correctly blocks that proposed sufficient condition as a universal strategy. It does not prove a plateau or preclude improvement after adjoining the shifted space to the original space.

### Fixed tuple versus full closure: pass

The cited fixed-tuple projection continuity, compact parametrization a_i=1+(λ−1)x_i, and uniform continuity on a compact neighborhood establish continuity of each d_n. Allowing repeated parameters causes no gap because the cited continuity includes collisions.

D=inf_n d_n is correct. The displayed b_n scalar family is continuous and nonincreasing in both its cutoff variable and n, yet has a right-discontinuous infimum. Thus the proposed limit passage is genuinely invalid without additional uniformity.

If a right jump exists and finite-sum approximation errors tend to its lower right-limit value, neither a bounded term count nor a bounded coefficient total variation can occur along a subsequence. The first contradicts fixed-d_n continuity; the second permits clipping all parameters above λ to λ with vanishing error. The normalized generator differences do show why bounded H norm alone gives no coefficient-total-variation bound. These are restrictions on a hypothetical jump, not exclusion of one.

### Mellin reduction and endpoint strict drop: pass

With s=1/2+iτ, the stated Mellin transform has Plancherel measure dτ/(2π) for this H. Scaling gives M e_a=−a^(−s)ζ(s)/s and Mχ=1/s. This validates (13). Absorbing a^(−1/2) into unrestricted coefficients identifies the exponential frequencies as [0,log λ]. The target −1/ζ belongs to the weighted space because its squared weighted norm equals 1; isolated zeros have measure zero. No unweighted Paley–Wiener conclusion follows by discarding the weight.

Direct interval integration confirms ⟨χ,e_a⟩=(log a+1−γ)/a and ||e_a||²=(log(2π)−γ)/a. The printed partial-sum expression for the norm also checks. The one-generator projection gain increases strictly for log a<1+γ, and choosing a=min(λ,exp(1+γ)) proves D(λ)<D(1) for every λ>1. This proves only comparisons involving 1; it does not compare any prescribed pair 1<λ<ν.

## 3. Reproduction and adversarial controls

Run `python3 independent_controls.py` from this audit directory, or use its absolute path from any working directory. Only the Python standard library is required. It hashes copied frozen inputs, runs the unmodified author script in a temporary directory, compares its generated JSON byte for byte, and creates independent_results.json. It does not write to the original author directory.

Results:

- Original replay: all 701 generator checks, with byte-identical output.
- Independent Möbius identity checks: 4,000.
- Independently rebuilt witness pairings: 3,080, including 2,249 cutoff annihilations.
- Independent Riesz identities on polynomial test functions: 234.
- Finite divisor-inversion checks: 800.
- Exact compact-polynomial dilation checks: 18.
- Prime, composite-squarefree, squareful, and noninteger centers, including supports crossing multiple integers.
- Wrong-Jacobian, omitted-below-1-term, overextended-cutoff, and separation-implies-gain mutations are rejected.
- Proper-space plateau, nonzero rank-one gain, continuous-generator right jump, and continuous-infimum right jump negative controls pass.
- Floating one-generator integration sanity checks pass with a mathematical tail bound; floating results are not presented as rigorous interval certificates.

The independent implementation uses divisor recursion for μ, midpoint evaluation on a common partition for h, and a global primitive of the fractional part for generator pairings. These differ from the author's factorization, event sweep, and generator-jump subdivision. The continuum results rest on the proofs above, not the finite samples.

## 4. Precise remaining gap and disposition

Right continuity at an arbitrary λ>1 still requires proving P_(E_(λ+)∩E_λ^⊥)χ=0. A sufficient stronger route would identify E_λ=N_λ, but no global density theorem is established for λ>1.

Strict decrease still requires, for every 1<λ<ν, some a∈(λ,ν] with ⟨χ−P_(E_λ)χ,e_a⟩≠0. The positivity of D(λ), strict growth of E_λ, separating witnesses, finite-term strict improvement, and endpoint result do not prove it.

The five reported approaches are distinct and properly recorded as partial or blocked. The subjective completion percentage is not an audited mathematical metric. Keep full_resolution=false, novelty_claim=false, and status=unsolved. The additional endpoint result may be appended as an explicitly labeled audit strengthening; do not silently rewrite the frozen proof.
