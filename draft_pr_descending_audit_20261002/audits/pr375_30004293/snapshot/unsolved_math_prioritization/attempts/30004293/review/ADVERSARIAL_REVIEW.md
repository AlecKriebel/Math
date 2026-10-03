# Independent full-packet review: logarithmic random sets, 30004293

**Verdict: PASS for the stated scoped results. Original broader growth question and explicit sharp finite-prefix interpretation remain unresolved, 5/5 author turns. No mandatory mathematical correction.**

This is a separate AI-assisted mathematical audit, not a peer-reviewed publication or a certification of priority. It covers all five frozen turns and their precise probability modes. It does not certify the entire long primary entropy framework or the recent preprint's proof.

## Binding and source scope

The reviewed 42-file author packet has FINAL_AUTHOR_MANIFEST.json SHA-256 ab2d9369a444b49e913abf32420b1c08f701149dc2df631278ad03e69feb5218. Every raw Git blob agrees at commit cd4f8dc65cd68c002e2cf85c9df60ce962f33c0d, folder unsolved_math_prioritization/attempts/30004293 in AlecKriebel/Math. The remote binding is recorded separately. No author file was changed.

The full Green contribution, OWR 50/2019 printed 3164–3167, and the rendered model page 3165 were checked. It really displays an unrestricted maximum for an infinite logarithmic random set, following a finite-prefix motivation; its following annular question is different. Official source: https://ems.press/content/serial-article-files/46829 . The EMS publication date is 19 November 2020, distinct from the 2019 report year.

The precise distinct-subset model, convergence-in-probability definition of beta_k, Theorem 2/Corollary 1, Lemma 2.1 and its finite-prefix remark, and the known beta_2 discussion were checked in FGK v3, https://arxiv.org/pdf/1908.00378v3 , and compared with the published source bound by the author manifest (https://doi.org/10.1007/s00222-022-01177-y). The primary lower bound and tensor/flag ideas receive explicit credit. The entire 94-page lower-bound proof was not independently reconstructed here; it is a clearly cited published input.

The 27 September 2026 Mao–Song v2 metadata and introductory fixed-threshold claims were checked against https://arxiv.org/abs/2609.22296 and the bound local PDF. They are explicitly recent preprint claims, not a premise of the sharp prefix result. The dated divisor-powers manuscript concerns a different quantity; no automatic transfer of its exponent is used. No exhaustive literature or novelty certification is made.

For each fixed x, only finitely many subsets can represent x. Published prefix divergence in probability implies that the unrestricted supremum is infinite almost surely by monotonicity and countable intersection. This literal correction is correct and does not resolve the substantive growth interpretation. The packet's normalization log M(D)/log log D is explicitly chosen and supported by FGK's prefix remark, not falsely quoted as an exact normalization in the OWR display.

## Turn 1: amplification and tail structure

The half-open endpoint change costs at most D^{-c}; positive c is fixed before the limit. Downward closure of the threshold set justifies every rational c below beta_k. The crude largest-entry union bound uses independence only for distinct valid supports and correctly obtains D^{2-3c}.

The independent geometric-log annuli are disjoint. Their success probabilities tending to one need no uniform convergence rate: the variance bound on square-index subsequences is summable, and monotonicity fills the gaps. The subset unions remain distinguishable by restriction to the annuli. The passage from endpoints D_n to all D loses only n/(n+1). Countably many fixed k and rational c yield the asserted almost-sure liminf.

The power inequality beta_{k^r}>=beta_k^r fixes r before taking D to infinity, so its identification of the supremum with the large-k limsup introduces no hidden growing-parameter assumption. Finite changes alter log M by a bounded amount, making extended liminf and limsup tail-measurable and deterministic. This does not imply their finiteness or equality. The sum-cutoff squeeze is valid because positivity bounds every representing element by its sum, while every subset of [1,D] has sum at most D(D+1)/2. Fixed-power rescaling preserves the log-log leading limits.

## Turn 2: relation-support estimates

After cancellation, all support entries are distinct and both signs occur. Orienting the largest entry positively and exposing the second largest gives n>=m/(ell-1); the remaining entries and signs determine n uniquely. The probability bound therefore has m^{-2}, without an erroneous additional free summation over n. Elementary symmetric polynomials are bounded by harmonic powers divided by a factorial.

The fixed-length tail constant is allowed to depend on length. For growing lengths the separate factorial calculation is genuinely uniform: L=c log D+O(1), c<1, and its dyadic exponent is -1+c log(2e/c)<0. Borel–Cantelli needs no event independence here. Fixed-cardinality equal-sum fibers share their outside part after their short relations are confined to a finite core, proving a finite random bound and eventual stabilization. A common large entry does not count as a large differing support element.

## Turns 3–4: self-contained flag exposure and uniformity

Reading entries in decreasing order builds a rational flag with one new dimension per recorded vector. Distinct witness subsets force distinct coordinate patterns, hence k<=2^t. Upward rounding of recorded magnitudes is safe: a residual entry above the next rounded endpoint cannot have a type outside the current flag space. Tied bins are empty and are handled without a strict-bin assumption.

For a fixed residual set and flag data, diagonal coset assignments determine residual quotient sums. Choices inside one coset add no quotient multiplicity. Injectivity of the recorded vectors modulo constants makes each residual sum determine at most one recorded tuple. Invalid, repeated or residual recovered entries are discarded. The exact probability ratio is product 1/(K_j-1), not product 1/K_j; summing probabilities of all residual sets is at most one, and does not assume that deletion preserves their distribution.

Turn 3 discretizes all empirical frequencies for fixed k, so its unspecified C_k is harmless in its fixed-parameter proof. Turn 4 removes those frequencies from the union bound and uses the explicit count [2^k(L+3)]^t. A (j+1)-dimensional cube section has at most 2^{j+1} vertices, and zero and one identify modulo constants, giving at most 2^{j+1}-1 classes.

The upper cumulative-count regularity bound also holds for every residual subset. Summation by parts has nonnegative entropy increments and accumulates the error only as (u+2)h_t. The first coefficient h_1-1=log 3-1 is positive, while all later increments minus one are negative; maximizing them at their correct opposite endpoints gives a-c(t+a). All constants in R and the geometric sum are explicit. Thus substituting k=floor(L/(log L)^3), u=sqrt(L)log L and c=(a+epsilon)/ceil(log_2 k) is valid. In particular t_0 R=o(L), the first term decays exponentially in L, and the regularity failure is summable along dyadic D. The count law applies to the deterministic growing cutoff D^c. The final constant (log 3-1)(log 2)^2 follows with the correct two factors of log 2.

The recovered beta_2 upper boundary is already known and is credited. No inference of a finite log-log upper exponent is made from the much larger exp(O(log D/log log D)) scale.

## Turn 5: annealed moments and rare events

The tilted measure includes the surely selected first indicator and has exactly p_i=lambda/(i+lambda-1). The pigeonhole count uses S+1 possible nonnegative sums. Jensen applies to the convex decreasing function x^{-q}; the upper bound on the tilted mean of S therefore yields a lower bound in the stated direction. At q=2 the exact product gives the coefficient 1/96.

The rare-event argument intersects a high-probability tilted count event with a Markov bound on S, producing tilted probability at least one half. Since lambda>1, the upper bound on N gives the required lower likelihood-ratio bound. Parameters are fixed before the n limit and then approach the boundary. A strictly larger exponent handles real-D flooring before continuity is invoked.

For logarithmic moments, the pointwise annular failure probability is available for all sufficiently large D, rather than merely an almost-sure asymptotic statement. Bernoulli factorial moments control every fixed moment; variance and a strictly higher moment give uniform integrability. Cauchy–Schwarz kills the exceptional contribution because its probability decays faster than any power of log L. This justifies the stated limsup of all fixed logarithmic moments. Raw polynomial moments, vanishing rare-event probabilities and almost-sure typical growth are consistently distinguished.

## Reproduction and limitations

All 150,925 author assertions replay byte-exactly. All 120 historical manifest entries, all 41 final entries and all five source PDFs match their hashes. All 42 remote raw blob IDs and sizes match. The separate independent checker passes 8,390 exact rational controls covering every binary-generated constant-containing subspace in dimensions at most four, 574 equal-sum pair/triple flags, rounded support and injectivity, exact tilted finite laws, relation first moments and coefficient optimization.

Finite controls support the analytic audit and do not prove infinite probability statements. The sharp prefix exponent, convergence on the log-log scale, finite limsup and original broader growth question remain unproved. The recommended disposition is unsolved, five turns completed, with the proved partial results preserved and credited.
