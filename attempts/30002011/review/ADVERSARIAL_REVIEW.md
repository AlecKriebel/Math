# Independent adversarial review: problem 30002011, all five author turns

Reviewed 2026-10-02. **Verdict: PASS for the stated scoped results; retain the original broader objective as unresolved, 5/5 author turns.** No mandatory mathematical revision was found. In particular, the positive-h comparator and shrinking-window/data-selected finite-thinning theorem are valid under the bounded iid-prior assumptions stated in Turns 4 and 5. They do not establish the original practical general-grid CV/refit guarantee.

This is an independent mathematical audit, not a formal proof-assistant certificate, human peer review, or a historical-priority certification. No sixth author search turn was performed. The review checks the frozen five-turn packet and the exact source scope.

## Frozen inputs and reproducibility

The complete author packet is bound by FINAL_FROZEN_MANIFEST.json, SHA-256

    641216d1928d9c1066a382f6cd07efcc84151eaf1e0a1940a1c8e7535e5b6866

All 40 files listed there were read and checked against their recorded byte counts and SHA-256 hashes. The manifest itself is the 41st author-package file. All five author programs were rerun; their deterministic outputs match the saved receipts byte-for-byte, totaling 68,121 assertions. The individual replay hashes are in AUTHOR_REPLAY_RECEIPT.json. The historical manifests are not rewritten by this review.

The independent program independent_checks.py imports no author code. It computes weighted isotonic fits by the max-min interval-average formula rather than PAVA. It encloses positive-h fits using reciprocal positive-series bounds for exp(h), with a geometric bound for the remaining Poisson series. It passes 116,124 exact rational assertions over 172 count histograms, supplemented by exact missing-bin multinomial and centered/anchored-score checks. The tested positive h values are 3/4, 1/32 and 1/2048. All arithmetic in these assertions is rational; no floating-point tolerance is used. These are finite falsification controls, not a proof of an asymptotic rate.

## 1. Source scope and known inputs

I checked all eight available primary PDFs against the pinned hashes and sizes. The central source pages and rate input were independently read in the extracted text, and the following pages were rendered and inspected: OWR printed p. 820, Brown–Greenshtein–Ritov author-version p. 9, and Polyanskiy–Wu pp. 4 and 30. The byte checks are in SOURCE_HASH_CHECKS.json; copyrighted PDFs, extracts and renders are excluded from this review's publication bundle.

The [OWR 14/2012 contribution](https://ems.press/content/serial-article-files/46384), printed pp. 819–821, proposes selecting a corruption parameter and discusses inbred cross-validation. It does not specify one universal grid, thinning schedule, replication count, tie rule or sharp-refit theorem. Its motivating moderate-h choices are materially different from a grid whose maximum tends rapidly to zero. Accordingly, the final packet correctly distinguishes a proved construction from the broader research objective.

The [Brown–Greenshtein–Ritov full source](https://arxiv.org/pdf/1006.4582v2), Sections 2.3–2.4 and 6, confirms empirical-multiplicity-weighted isotonic projection on the observed domain, the positive-limit gap-filling phenomenon, and the thinning score followed by proposed full-data reconstruction. Those ingredients and the already-known discontinuity must remain credited. The packet does not silently identify h=0+ with the separately defined h=0 rule.

The [Polyanskiy–Wu source](https://arxiv.org/pdf/2109.03943v2), estimator (5), Theorem 2 and Appendix C (115)–(128), is the correct fixed-sample, in-sample Robbins input. Its total-regret bound divides by n to give the average-regret benchmark used here. This avoids importing a new-observation or Poissonized-sample theorem without a transfer argument. The positive-h result uses that known rate rather than claiming to establish it anew.

I also checked the coupled-bootstrap paper's Hudson identity and infinite-bootstrap/noiseless-limit discussion, and the relevant introductory/model sections of the newer minimum-distance, ERM and heavy-tail papers supplied in the source packet. Their estimator objectives are different from this original least-squares isotonic smoothing family. This bounded scope check does not certify that no later result anywhere resolves the original question.

## 2. Turn 1: source-family envelope and single-thinning comparison

**Pass.** The shifted Poisson-convolution identity follows by splitting z+1 into (z+1-t)+t; all negative-index kernel terms vanish under the stated convention. The tail bound makes the Rao–Blackwell average finite. The auxiliary posterior tail is nondecreasing by the adjacent-kernel total-positivity inequality, including zero-support boundaries.

The suffix identity has the necessary one-step shift T+N-1. Defining the tail to be zero below the empirical minimum is essential and correctly accounts for the lost term at the smallest observed count. Its consequence bounds every weighted suffix mean by the sample maximum. The last fitted isotonic value is the largest suffix mean; block-mean identities and monotonicity then bound all fitted values in [0,m]. Multiplicities are retained throughout. The separate h=0 proof handles missing bins directly.

For the validation comparison, conditioning on U and the deterministic mean vector makes V independent with the stated Poisson means, including when the finite candidate set is U-measurable. The h-independent noise cancels only in score differences; it is not mistaken for zero. The variance bound has the factor 8 alpha^2 M/(eta n), and the subsequent square-root/Young bound gives the stated factor 4 alpha^2 M/epsilon. The random sample-maximum envelope B is legitimate after conditioning. The result concerns the realized U-trained loss; neither regret-scale adaptivity nor full-Y refitting is inferred from it.

## 3. Turn 2: centered limit, full-refit correction and optimism

**Pass.** The centering constant is the conditional second moment of a binomial deletion count, including both its variance and squared-mean parts. Reindexing that binomial mass produces the leave-one-count formula without division by eta. Every fixed-data sum is finite.

The uniform error bound D_alpha follows from the probability of any deletion and the sample-maximum envelope. It requires no h-continuity. The Poisson third-moment estimate is uniform over deterministic vectors in [0,M]^n, and eta=n^-5 indeed makes its expectation O_M(n^-2).

Hudson's identity must be applied to the whole selected-and-refitted rule. Doing so gives the displayed Omega with the stated sign: the held-fixed selected parameter in the plug-in expression is compared with the parameter reselected at Y-e_i. The switch-indicator bound is valid but remains a hypothesis for the unrestricted selector. Fixed-h unbiasedness alone does not cancel Omega.

For n=1 the source formula gives F_h(y)=y(1-exp(-h)). With h=log 2, the exact averaged-score difference is alpha*y*[1-3 alpha(y-1)]/4. For alpha>1/3, selection changes at y=2. The correction integrand is exactly 2 at y=2 and zero elsewhere, giving Omega=lambda^2 exp(-lambda). Both displayed risk formulas and their difference agree. The packet correctly avoids tensorizing this example into a common-histogram large-n counterexample.

## 4. Turn 3: rare-deletion Monte Carlo

**Pass, as an explicitly modified implementation.** Conditioning on a nonzero total deletion gives the exact decomposition around the delete-one anchor. The eta anchor adjustment changes the cross-term coefficient from -2 to -2 alpha as required. The I distribution proportional to y_i turns the sum into an unbiased sampled term. The S=0 and S=1 branches do not invoke nonexistent conditional laws.

Conditioned on the total deleted count, allocation among coordinate capacities has the multivariate hypergeometric law, so the proposed rejection-free finite distributions implement the intended conditional thinnings. This is an exact distributional specification, not a claim of easy numerical evaluation for every real alpha.

The summand lies in [-L_alpha,L_alpha]; Hoeffding's exponential-moment bound for its B-sample average has variance proxy L_alpha^2/B. The union/maximum bounds require no independence across candidates. The inequality L_alpha<=D_alpha and the Poisson moment estimate yield the stated small-noise Monte Carlo order. The exact anchor still requires delete-one fits and is correctly charged as computational work.

For randomized selection, applying Hudson at each fixed independent seed is valid because the envelope supplies integrability uniformly in that seed. The same-seed convention specifies a coupling; it does not itself prove its stability. The naive fixed-B countercontrol is exact: the no-deletion event has probability alpha^(2B) and chooses the wrong candidate in the n=1 example. This does not become an asymptotic large-n risk lower bound.

## 5. Turn 4: positive-h comparison and bounded-prior regret

**Pass.** This is the key new statistical bridge in the packet.

For each corrupted count z, every ordinary numerator term lies at t<=s, where s is the largest observed value at most z. The only remaining possible term is at t=z+1. Thus the low/jump decomposition is exhaustive. Dividing by the s denominator contribution gives the bound mn h for the low part. It is uniform in z, so it survives the infinite Poisson averaging.

For a jump at the next observed t, the factorial and h-power expression in (3) is exact. The first such jump has s=y; its denominator remainder is at most nh, and its difference from the gap-filled value is at most mn(n+1)h. Later jumps have s-y>=1 and total at most mn h. Together these give mn(n+3)h. No factorial or power depending on the gap has been dropped in the wrong direction. Weighted isotonic projection is order-preserving and translation-equivariant by its max-min formula, so it is a contraction in the supremum norm. The same bound therefore holds after the actual source projection.

The comparison b_+>=b_0 is pointwise only on the observed domain, which is exactly where it is needed. Order preservation gives 0<=Delta_0<=Delta_+<=m. Mean preservation yields the missing-predecessor-bin expression with the empirical minimum excluded. Since each coordinate difference is in [0,m], multiplying the mean difference by m bounds the empirical squared gap.

The adjacent mixture probability inequality t p_t<=M p_{t-1} holds for all priors on [0,M]. The expectation of N(t) times an empty predecessor event is n p_t(1-p_{t-1})^(n-1), by summing designated-observation indicators, not by assuming independent histogram bins. Truncation at m<=L then gives ML^2/n. On the complement the maximum is dominated by the sum of individual tail squares, and each count is stochastically dominated by Poisson(M). The factorial-moment tail identity is correctly indexed. L of order log n/log log n with a sufficiently large fixed constant makes this tail negligible and also bounds E m^2 at the required order.

The iid-prior posterior mean vector belongs to the monotone cone, so projection cannot increase its squared distance from Robbins. Combining the credited fixed-sample Robbins theorem with the expected missing-bin gap proves the rate for Delta_+. The uniform finite-h comparison then proves the rate for h_n=n^-4. This is not an inference from continuity at h=0, and no unknown-prior clipping has been introduced.

For terminological precision, the matching nonzero minimax lower bound is for a fixed support interval with M>0. At M=0 every estimator in the packet vanishes and the regret is zero. The text already handles that degenerate case explicitly; no mathematical correction is needed to the stated upper bounds.

## 6. Turn 5: data-selected shrinking windows and guard

**Pass with the restrictions exactly as stated.** The pathwise finite-h bound is simultaneous over the entire permitted interval, so a data-dependent or independently randomized selection within that interval needs no score-unbiasedness or concentration argument. Its additional regret term is O_M(n^4 epsilon_n^2 (log n/log log n)^2). Thus epsilon_n=O(n^-5/2) suffices, and the displayed n-element grid with maximum n^-3 is valid.

The resulting finite-thinning/refit algorithm genuinely selects h from data. Its rate holds for any deterministic alpha_n in (0,1) and finite B_n>=1 because every allowable full-data output is close to the comparator. It is important that this reasoning offers no benefit from the CV criterion itself and no permission to enlarge the grid arbitrarily. Inclusion of the separately defined h=0 can be handled by the expected gap bound; it does not restore pathwise positive-limit continuity.

For the deletion correction, a count deletion leaves the vector length n unchanged. Applying the same window to both selectors and the Turn-4 bound yields the coefficient 4(n+3)epsilon_n in front of E[S m]. Bounding this by the Poisson second moment gives the displayed O_M(n^-1) result for epsilon_n=n^-4. The deterministic-mean validity of this correction bound does not automatically extend the Bayesian comparator theorem to a different compound-regret objective.

The general-grid safeguard is a separately modified output protocol. Its deterministic distance test always keeps the final output within tau_n of the known comparator in empirical squared norm. The squared-triangle regret bound follows directly. It does not prove the unguarded original CV selector optimal, and the packet does not claim otherwise.

## 7. Disposition and exact unresolved boundary

Retain **unsolved, 5/5**, with a passed scoped-results package. The strongest positive statement is a rate-optimal positive corruption schedule and a precisely specified genuinely data-selected shrinking-grid finite-thinning/refit rule for iid priors on a fixed bounded interval. A separate guarded rule has an additional protocol change.

There is no general-grid adaptive selection/refit oracle or regret theorem here for the practical moderate-smoothing choices. A good comparator alone does not control the unrestricted deletion-selection correction. Heavy-tail, unrestricted prior and unspecified deterministic-mean compound-regret variants are also outside the proved result. The OWR source is open-ended, so this boundary is a qualified assessment of the intended broader objective rather than a purported verbatim universal conjecture from that report.

No mandatory mathematical revision is requested. Any publication should retain these scope restrictions, the known-input credits, all frozen evidence, and the exhausted five-turn count. Neither novelty nor human peer review is certified.
