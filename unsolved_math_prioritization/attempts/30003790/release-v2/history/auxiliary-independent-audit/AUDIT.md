# Independent audit of the guarded-regression auxiliary theorem

Problem 30003790 / OWR-16161-003. Audit completed 4 October 2026.

## 1. Verdict and exact object accepted

**ACCEPTED AS STATED, under the standard meaning that the test point is independent of all observed training and regression data.** No false step was found in the candidate proof. Both guard choices prove expected integrated squared-error consistency and sample-conditional integrated-risk convergence in probability for each fixed finite ambient dimension, every Borel design law, bounded continuous regression function, and conditionally centered noise with a common finite conditional second-moment bound.

This accepts a precise, elementary statistical theorem. It is not a novelty certification, a universal declaration that the source research problem is solved, a proof of efficient dimension dependence, or an endorsement of other results in the original packet.

The exact independently audited file is:

- Candidate: `../independent-audit/AUXILIARY_CANDIDATE.md`
- SHA256: `072aba944c908baf44bb86d6c9a3d1c87444b5f779c53a14b4a9648d9595351c`

The author packet was kept unchanged:

- `../public/RESULT.md`: `0c63e1801d50434d217a8a66d16ea8bad27cac4867919f7532abc4819eb9dc16`
- `../public/MANIFEST.json`: `a18df1c214a6ea7ed7aa14d8a038827f463a7c9ff4f069228e0eb68b247367d2`
- All nine manifest-listed files were checked against their declared byte counts and hashes.

The reviewer did not develop the auxiliary candidate. This audit inspected the candidate, the frozen author's relevant theorem and scope discussion, and the original primary report. Separate tests were written for this audit; neither the original candidate nor the earlier audit's controls were edited.

## 2. Exact accepted statement, with probability spaces made explicit

Fix an integer D >= 1. Let P be any Borel probability measure on R^D, and let K = supp(P). Let (X_i,Y_i), i >= 1, be iid with X_i distributed as P and

    Y_i = F(X_i) + epsilon_i.

Assume that F is continuous on K in its relative topology, |F| <= M < infinity, and

    E[epsilon_i | X_i] = 0,
    E[epsilon_i^2 | X_i] <= sigma^2 < infinity       almost surely.

For each n, let T_n be an auxiliary random object independent of the regression data. Let a_n(T_n,z) be jointly measurable, with Euclidean norm at most one for z in K. Let the test point X have law P and be independent of the joint observed-data sigma-field

    S_n = sigma(T_n, (X_1,Y_1), ..., (X_n,Y_n)).

Take deterministic integers 1 <= k_n <= n with k_n -> infinity and k_n/n -> 0. At query x, let R_n(x) be the kth order statistic of ||x-X_i||. Rank all n candidates lexicographically by (d_n(x,X_i), i), where

    d_n(x,X_i) = |a_n(T_n,X_i)^T(x-X_i)| + lambda_n(x)||x-X_i||.

Select exactly k_n distinct indices and average their Y_i. The choices accepted are:

    A: lambda_n(x) = lambda, for fixed 0 < lambda <= 1;
    B: lambda_n(x) = min(1, sqrt(R_n(x) + 1/n)).

Then, for either choice,

    E[(Fhat_n(X)-F(X))^2] -> 0,
    E[R(S_n)] -> 0,
    R(S_n) := integral_K (Fhat_n(x)-F(x))^2 dP(x) -> 0 in probability.

In B, lambda_n(X) -> 0 in probability. The acceptance does not require consistency of a_n, any relation between training-sample size and n, a design density, compact K, uniform continuity of F, or moments of ||X||.

The restatement makes the ordinary joint-independence interpretation explicit. Merely asserting that X is separately independent of T_n and separately independent of the regression data would be weaker and is not a substitute: pairwise independence need not give independence of their joint sigma-field. The original candidate already calls X an independent test point; this is a clarification, not a repair of the mathematical argument under its natural reading.

## 3. Step-by-step mathematical verification

### 3.1 Support and null sets

For a Borel probability on finite-dimensional Euclidean space, K is closed and P(K)=1. One way to check the latter is to cover its complement by the countable collection of rational balls of P-mass zero contained there. Every x in K has P(B(x,delta)) > 0 for every delta > 0.

The function F is Borel on K. Samples and the test point lie in K almost surely. All statements can be defined arbitrarily on the null event that a sample is outside K. No density or positive mass at an individual point is required. In particular, membership in K does not imply P({x}) > 0; positive neighborhood mass is the fact actually used.

### 3.2 Measurability and ties

Write d_i = d_n(x,X_i). The rank of candidate i can be expressed without invoking an unspecified sorting operation:

    rank_i = 1 + sum_{j != i} 1{d_j < d_i or (d_j = d_i and j < i)}.

Each comparison is measurable in (T_n,x,X_1,...,X_n). Thus w_i = 1{rank_i <= k_n}/k_n is jointly measurable, nonnegative, sums to one, and has exactly k_n nonzero values. R_n is a finite order statistic of continuous-in-x measurable functions; lambda_n is measurable and strictly positive. The finite weighted sum of responses and its squared error are measurable. Parameter integration of a nonnegative jointly measurable function gives measurability of R(S_n).

Deterministic sample-index tie breaking is valid even for atomic designs and repeated covariates. It need not be permutation invariant. No symmetry, triangle inequality, or metric property of d_n is needed. The tangent field may be discontinuous. Equal covariates have the same field value under the stated field definition, although the radius inequality would hold even for more general candidate-specific bounded vectors.

### 3.3 Euclidean nearest-neighbor localization

Fix x in K and delta > 0, and set p = P(B(x,delta)) > 0. Since k_n/n -> 0, eventually k_n <= np/2. The count N_delta of Xi in the open ball is Binomial(n,p). If R_n(x) > delta, then N_delta < k_n. The reverse implication is unnecessary, so observations exactly on the boundary cause no difficulty. The multiplicative Chernoff inequality gives

    P(R_n(x) > delta) <= P(N_delta < k_n) <= exp(-np/8).

The exponent is a valid conservative constant. Hence R_n(x) -> 0 in probability at every support point. The p here depends on x and delta; no inference of a uniform-in-x rate or a uniform lower-mass constant is made.

### 3.4 Deterministic guard comparison

By Cauchy-Schwarz and ||a_n|| <= 1, for every realized sample and every i,

    lambda_n(x)||x-X_i|| <= d_n(x,X_i)
                         <= (1+lambda_n(x))||x-X_i||.

At least k_n candidates have Euclidean distance <= R_n(x), so the kth smallest d_i is <= (1+lambda_n(x))R_n(x). Every selected d_i is at most that threshold, even if there is a tie. If G_n(x) is the greatest Euclidean distance among the selected candidates, then

    G_n(x) <= (1+lambda_n(x))R_n(x)/lambda_n(x).

It is essential that lambda_n(x) is a single positive scalar common to all candidates for that query. It may depend on the entire regression covariate sample. Its randomness is harmless both in this pathwise inequality and in the later conditioning argument.

For A, the coefficient (1+lambda)/lambda is finite and constant, so G_n(x) -> 0 in probability.

For B, on R_n(x) <= 1:

- If lambda_n(x) < 1, then (1+lambda_n(x))R_n(x)/lambda_n(x) <= 2R_n(x)/sqrt(R_n(x)+1/n) <= 2sqrt(R_n(x)).
- If lambda_n(x) = 1, the same conclusion follows from 2R_n(x) <= 2sqrt(R_n(x)).

The complement has probability tending to zero. Thus G_n(x) -> 0 in probability. Also lambda_n(x) <= sqrt(R_n(x)+1/n), which tends to zero in probability. The cap at 1 does not interfere with this conclusion.

When R_n(x)=0, there are at least k_n exact covariate matches. The positive 1/n safeguard makes lambda_n(x)>0, all selected d_i equal zero, and all selected Euclidean distances equal zero. Other points cannot tie with them. Conditional independence of iid labels still permits variance reduction among repeated covariates.

### 3.5 Conditional noise and response-selection independence

For a fixed query x, condition on

    H_n = sigma(T_n, X_1,...,X_n).

All w_i and all selected indices are H_n-measurable. Since the real-valued pairs are iid and T_n is independent of them, conditional laws of the responses given the covariates factor. In particular, for i != j,

    E[epsilon_i | H_n] = 0,
    E[epsilon_i epsilon_j | H_n] = 0,
    E[epsilon_i^2 | H_n] <= sigma^2.

The first two statements can also be checked directly using the product conditional kernels of iid Euclidean-valued pairs. No assumption that epsilon is independent of its own covariate is needed. Heteroskedastic noise and non-Gaussian finite-variance noise are allowed.

With eta_n(x) = sum_i w_i epsilon_i,

    E[eta_n(x) | H_n] = 0,
    E[eta_n(x)^2 | H_n]
        = sum_i w_i^2 E[epsilon_i^2 | X_i]
        <= sigma^2 sum_i w_i^2 = sigma^2/k_n.

The conditional second-moment assumption implies unconditional square integrability and justifies these products. It cannot silently be replaced in this proof by an unconditional variance bound. Selected covariates can concentrate in high-variance regions.

The independent training data may use its own labels to estimate directions. The field evaluated on the regression sample must still be a function of T_n and the covariate z only. Splitting samples does not authorize assigning a held-out Xi to its slice by looking at its held-out Yi. Such label reuse would generally invalidate the displayed conditional expectations.

### 3.6 Bias, continuity, and bounded domination

Let

    b_n(x) = sum_i w_i(F(X_i)-F(x)).

Fix any eta > 0. Continuity relative to K supplies a delta > 0 such that |F(z)-F(x)| < eta whenever z in K and ||z-x|| < delta. On G_n(x)<delta, all selected differences have absolute value < eta, and hence |b_n(x)| < eta. It follows that b_n(x) -> 0 in probability.

For all n,x, |b_n(x)| <= 2M. More explicitly,

    E[b_n(x)^2] <= eta^2 + 4M^2 P(G_n(x) >= delta),

with a suitably chosen strict continuity radius. First let n -> infinity, then eta -> 0. Thus E[b_n(x)^2] -> 0 without requiring almost-sure convergence or uniform continuity.

The mixed term vanishes after conditioning on H_n. Consequently,

    E[(Fhat_n(x)-F(x))^2]
      = E[b_n(x)^2] + E[eta_n(x)^2]
      <= E[b_n(x)^2] + sigma^2/k_n -> 0.

The uniform dominating constant 4M^2+sigma^2 is finite. It is a bound on the expected squared error, not a bound on every realized noisy estimate.

### 3.7 Integrating over an arbitrary unbounded design

The preceding expected pointwise error is measurable as a function of x and tends to zero for every x in K. Integrate with respect to the probability measure P and apply dominated convergence using 4M^2+sigma^2. Independence of the test point from S_n and Tonelli yield

    E[(Fhat_n(X)-F(X))^2]
      = integral_K E[(Fhat_n(x)-F(x))^2] dP(x)
      = E[R(S_n)] -> 0.

No integration of ||X||, no finite support diameter, and no global modulus of continuity appear. Thus unbounded support and infinite covariate moments are genuinely covered when F remains bounded and continuous. A bounded function such as sin(||x||^2), which need not be uniformly continuous on an unbounded support, is allowed.

Every realized finite response average is bounded in absolute value by max_{i<=n}|Y_i|, so R(S_n) is finite almost surely under the theorem's assumptions. Markov gives

    P(R(S_n) > eta) <= E[R(S_n)]/eta -> 0.

Likewise, integrate the measurable probabilities P(lambda_n(x)>eta) <= 1 to obtain lambda_n(X) -> 0 in probability. Neither conclusion requires inter-n independence or an increasing nested auxiliary sample.

## 4. What the proof does and does not establish

### Accepted risk modes

- Pointwise expected squared error tends to zero at every x in K.
- Expected integrated squared error tends to zero.
- Sample-conditional integrated squared error tends to zero in probability.
- The local guard in B vanishes in probability at each support point and at an independent random query.

The error is measured against F(X)=E[Y|X], not against a fresh noisy response. Expected prediction loss against a fresh Y includes irreducible noise variance; under nonzero noise it generally cannot tend to zero. With the stated centering, the proven quantity is also the excess squared prediction risk over the regression function.

### Claims not established by this audit

- Almost-sure convergence of conditional integrated risk, uniform-in-x convergence, or uniform-over-model consistency.
- Consistency for every measurable or unbounded regression function.
- Consistency under arbitrary noise merely because it is called nonzero noise.
- A deterministic schedule for an arbitrarily rapidly vanishing guard.
- Convergence of estimated tangents, correctness of response-slice assignments, consistency of a retained segment classifier, or recovery of the latent curve coordinate.
- A rate for arbitrary Borel designs, one-dimensional sample rates, rates uniform as D grows, or preservation of the original algorithm's geometric efficiency.

These are limits of the accepted statement, not assertions that all such extensions are false.

The radius comparison ranks all n regression covariates. If an implementation first filters candidates into an estimated coarse segment, at least k_n points within the Euclidean radius need not remain in that segment. The present proof then does not apply unless an additional localization property of the filter is established. Retaining tangent directions does not require retaining that filtering step.

## 5. Adversarial boundary controls

### 5.1 Response-dependent ties are a real failure, even at one atom

Take X_i=x=0, F=0, and iid Rademacher noises. All distances tie. Under the valid deterministic index rule, averaging k responses has squared risk 1/k. If one instead chooses the k largest responses, then whenever at least k signs are positive, the estimate is exactly 1. For k/n -> 0 this event has probability tending to one, so consistency fails. The exact finite control n=12, k=3 gives mean 2017/2048 and squared risk 755/768, rather than a zero mean and a variance bound 1/3.

This tests the most fragile statistical step in the proof. Sample splitting and deterministic tie handling are substantive safeguards, not cosmetic choices.

### 5.2 An unguarded tangent term can ignore a regression coordinate

Let X=(U,V) be uniform on [-1,1]^2, F(U,V)=V, and a_n identically e1. With lambda=0, selection depends on the U coordinates and the query U only. The selected V values remain iid uniform and independent of the query V. The exact noiseless integrated risk is

    1/3 + 1/(3k),

which tends to 1/3. Independent centered response noise of variance one adds 1/k. This violates neither smoothness nor boundedness; it violates the positive guard condition.

An arbitrary tiny positive deterministic guard is not a general replacement for choices A or B. For example, take lambda_n=exp(-n) in this same model. Except on an event of probability O(n^2 exp(-n)), perturbations are too small to change any ordering of the scalar distances |U-U_i|. To verify the estimate: conditional on U, these scalar distances have density at most 1; a union bound over pairs makes the probability of a pairwise gap <= 2sqrt(2)lambda_n at most a constant times n^2 lambda_n. Each Euclidean perturbation lies in [0,2sqrt(2)lambda_n]. Thus the selected indices agree with the unguarded ones with probability tending to one. Since the noiseless squared errors are bounded by 4, their risks have the same positive limit. The candidate avoids this issue by adapting its guard to the actual local Euclidean radius.

### 5.3 Centering identifies the target

With a one-point design, F=0, and epsilon=1+Z for centered variance-one Z, the sample-average error is 1+1/k and does not vanish. More generally, without conditional centering the same joint law of (X,Y) admits different decompositions into F and epsilon. Even unconditional centering is insufficient: for uniform U on [-1,1], Y=U+Z can be written either with F(U)=U and epsilon=Z or with F(U)=2U and epsilon=Z-U. Both noises have unconditional mean zero; only the first is conditionally centered. Both links are smooth and strictly monotone.

Thus a fully unspecified source noise term cannot itself define an identifiable regression target.

### 5.4 Removing boundedness without replacing integrability can fail dramatically

Let Z have the standard Cauchy distribution, U be independent uniform on [-1,1], and X=(Z,U). Let gamma(t)=(t,0) for t in R, so X lies in a fixed-width straight tube with unique orthogonal projection. Let F(X)=Z, a smooth strictly monotone single-index link, and add independent Rademacher response noise.

For any realized finite data set, any average of selected responses satisfies |Fhat_n(x)| <= B_n := max_{i<=n}|Y_i| < infinity. For z >= max(1,2B_n),

    (Fhat_n((z,u))-z)^2 >= z^2/4,
    z^2/[4*pi*(1+z^2)] >= 1/(8*pi).

Integration over the Cauchy tail and U shows R(S_n)=infinity almost surely for every n, for both candidate guards and every tangent field. This is not a counterexample to the candidate: F is unbounded and its square is not integrable. It proves that the omitted moment/domain assumptions in the short source cannot all be ignored when interpreting a mean-square claim. The finite-control file checks the elementary truncated-tail lower bound, not an approximation to the improper integral.

### 5.5 The remaining hypotheses have distinct roles

- If k stays fixed, the one-point design with independent variance-one noise has risk 1/k forever.
- If all noises equal one shared random sign, averaging has variance one. That construction violates iid pairs and illustrates the conditional-independence requirement.
- A rare atom of mass 10^-6 is missed by all 100 observations with probability about 0.999900005. A support-point argument cannot give a common finite-n localization bound without the actual local mass.
- Conditional variance may vary with X, but it must have the displayed common bound for the simple sigma^2/k argument. The proof does not need bounded responses or sub-Gaussian tails.

## 6. Source interpretation and relation to known regression consistency

### 6.1 Literal target in the primary source

The primary OWR contribution defines sample-conditional mean-square error, proposes response-slice tangent estimation and tangent-based neighbors for a tube-supported curve-projection model, and ends by asking for a modification consistent with nonzero response noise. The final question states no dimension-efficient rate requirement. Earlier paragraphs motivate one-dimensional learning rates and computational efficiency. Those motivations do not turn an unstated rate into a necessary condition for the literal consistency question. [S1]

**Consequent classification:** under the conventional bounded-continuous, conditionally centered uniformly finite-variance interpretation, the candidate gives an affirmative fixed-D answer to the literal consistency request. It removes the frozen theorem's lower-mass and compact-design restrictions. It retains a nonzero learned tangent term if desired, even when that term is inaccurate.

For a compact support inside a tube on which the projection-coordinate/link composition is continuous, F is bounded automatically. Independent centered finite-variance noise supplies the conditional noise bound. Such models are covered. Smoothness of a curve alone does not establish uniqueness or continuity of its closest-point projection everywhere; those properties must hold where the model is used.

The short report does not enumerate all necessary design, target-integrability, and noise-identification assumptions. Therefore the candidate cannot be promoted to an unconditional theorem over every distribution compatible with its informal notation. The Cauchy tube and noncentering examples above explain precisely why. A statement that the literal bounded regression problem remains unresolved solely because an ambient-dimensional rate is poor would nevertheless be incorrect.

### 6.2 Is it an actual modification of the tangent method?

Yes, as a neighbor-selection safeguard with honest label separation. The scalar tangent-projection term is retained; a positive Euclidean term forces all selected neighbors to become truly local. The resulting consistency proof does not need that tangent term to be accurate.

A training procedure must produce a measurable covariate-only field. One explicit implementation is to estimate slice directions on the auxiliary sample, choose a deterministic convention for empty or singular cells, and extend directions to a new covariate by the Euclidean nearest auxiliary covariate, using index ties. This supplies such a field; the theorem does not claim it estimates the tangent well. Alternatively, the zero field is permitted and reduces the ordering exactly to ordinary Euclidean k-nearest neighbors. The latter special case illustrates why bare existence of a consistent estimator is a much easier target than efficient geometric learning.

A modification retaining a source-style coarse classifier or holding out samples but reassigning slices using their labels needs a separate argument. It is not automatically the audited estimator.

### 6.3 Known generic facts and novelty limits

Charles J. Stone's primary paper proves general consistency results for nonparametric probability weights. Its Section 3, Theorem 2 and Corollary 3, include consistent nearest-neighbor weights when k_n -> infinity and k_n/n -> 0; its definition in Section 1 covers L^r convergence for finite rth response moments. The original paper uses a particular averaging convention for tied ranks. It is evidence that generic nearest-neighbor regression consistency long predates this candidate, not a substitute for checking the candidate's different data-dependent ordering and deterministic ties. [S2]

The candidate's bounded-continuity proof is self-contained and simpler than a universal finite-second-moment regression theorem: it can bypass Stone-type weight domination because bounded continuous bias and a uniform conditional variance bound directly control error. No claim was established that this exact guard formula is novel, that all its generalizations are covered by Stone, or that its unbounded/discontinuous extensions follow for free. No exhaustive novelty search was conducted.

## 7. Publication corrections and clarification checklist

No correction to the accepted mathematical theorem is required. Before using it to revise a status or public conclusion:

1. State the two risk modes, fixed D, bounded continuity, conditional centering, and the uniform conditional second-moment bound explicitly.
2. Define S_n as all observed training/regression data and keep the test point independent of that joint sigma-field.
3. Describe the field assignment to regression covariates as response-independent. Splitting alone is not sufficient if slice labels are recomputed from held-out responses.
4. State that all n regression candidates are ranked. Do not silently retain an unproved segment filter.
5. Distinguish an affirmative answer to literal consistency under the stated model from unresolved dimension-efficient geometric learning. Do not use the latter to negate the former.
6. Do not add novelty, universal-noise coverage, strong/ almost-sure consistency, tangent recovery, or a quantitative rate to the accepted conclusion.
7. Preserve the original author disposition and this auxiliary audit as distinct historical records. Changing a project status is a separate scope decision, not something the arithmetic tests determine.

Suggested concise statement:

> An independently checked Euclidean safeguard gives expected L2 consistency, and sample-conditional integrated-risk consistency in probability, for the sample-split tangent-neighbor estimator in every fixed dimension under bounded continuity and conditionally centered uniformly finite-variance noise, for arbitrary Borel designs. This answers the literal noisy-consistency request under that explicit model interpretation. It establishes no novel or dimension-efficient geometric result.

## 8. Reproducible controls and their limits

Run from any working directory, using Python 3 with its standard library:

    python3 verification/check_auxiliary.py /path/to/rank618-30003790

Without the optional argument the controls still run, but input-hash verification is skipped. The output is JSON; the recorded bound run is `verification/result.json`.

Results:

- 15,855 exact rational fixed-guard order-statistic cases, including 1D and 2D, duplicated coordinates, zero fields, sign changes, and ties.
- 1,620 adaptive-guard selected-radius checks with 70-digit decimal arithmetic, plus 24 formula boundary checks, including R=0, the cap transition, and large radii. Numerical comparison tolerance is 10^-60.
- Exact enumeration of independent heteroskedastic sign noise for several selected subsets and the invalid response-selected tie rule.
- Exact binomial bias/risk calculations for a Bernoulli design at sample sizes through 1,024. With unit noise and k=floor(sqrt(n)), expected risk is about 0.03125 at n=1,024, with vanishing atom-mismatch bias.
- Analytic negative-control values for zero guard, fixed k, noncentering, shared noise, rare atoms, and the unbounded Cauchy target.
- Candidate hash and all original frozen manifest entries pass.

**Interpretation:** these finite and exact-algebra controls do not prove the universal asymptotic theorem. Acceptance rests on the full mathematical verification in Section 3. Conversely, the negative controls are not counterexamples to the actual theorem because each explicitly removes a stated hypothesis.

## 9. Primary sources and source binding

[S1] T. Klock, joint work with Z. Kereta, M. Maggioni and V. Naumova, "Estimation of Nonlinear Single Index Models," Oberwolfach Report 20/2018, pp. 1192-1194. Contribution text and the rendered final page were inspected. Source PDF SHA256: `c74075e3755dda76a289dd874174ca0e620ff5ea91159ced278c385aa679380d`.

- Publisher: https://doi.org/10.4171/OWR/2018/20
- Primary PDF: https://ems.press/content/serial-article-files/46744

[S2] Charles J. Stone, "Consistent Nonparametric Regression," Annals of Statistics 5(4), 595-620 (1977), with subsequent discussion/reply in the same issue. Original-paper scan, pp. 595 and 597-600, inspected visually; especially Section 1's consistency definition and Section 3's Corollary 3. Download SHA256: `544011c0923a8ac3cef34ec5c1844ed30faabf0df8146f870a0c046480213afa`.

- DOI: https://doi.org/10.1214/aos/1176343886
- University-hosted original scan: https://websites.umich.edu/~jizhu/jizhu/wuke/Stone-AoS77.pdf

Downloaded third-party documents and page images are kept separately under `private/` for audit provenance and are excluded from the audit's distributable manifest. This report contains original reasoning and source summaries, not a republication of those documents.
