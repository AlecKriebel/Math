# Fresh adversarial audit: Local complexity of functional estimation

Problem 30005248 · OWR-11695855-001 · rank 486  
Audit date: 3 October 2026

## Verdict

**PASS for the stated, scoped partial results. Retain UNSOLVED / 5 substantive approaches.**

No mathematical blocker was found in the ten-file frozen public package. The elementary proofs survive independent derivation, the cited main theorem restrictions are accurately retained, and the claims do not amount to a broad classification or a new full resolution. This is an audit of the supplied package and its cited source snapshots, not a claim that the entire literature has been exhausted.

- All ten input hashes matched the frozen allowlist before and after the audit.
- The author's verifier reproduced its exact JSON output and **16,459 assertions**, from a temporary copy so that no frozen input was written.
- A separate standard-library control program passed **20,738 assertions**, including seven rejected invalid extrapolations or mutations.
- The original report, Jiao–Han–Weissman, Canonne–Jain–Kamath–Li, and Kania–Manole–Wasserman–Balakrishnan were checked from local primary-source PDFs/text. Critical displayed formulas were visually checked where layout mattered.
- No remote action or publication was performed. Source PDFs, page images, private work, and machine-specific paths are not part of the portable audit allowlist.

The number of checks is a coverage statistic, not a measure of proof strength. In particular, 14,854 of the author's 16,459 checks concern a finite grid reconstruction inequality. Neither the author's count nor this audit's larger count proves an asymptotic minimax theorem, source priority, novelty, or completeness.

## 1. Source, attribution, and scope

### Original question

The original contribution is Sivaraman Balakrishnan, *Minimax hypothesis testing*, printed pp. 2663–2664 of [Oberwolfach Report 46/2022](https://doi.org/10.4171/OWR/2022/46). The title and author occur on printed p. 2663; the functional-estimation discussion is on p. 2664. The Yuxin Chen heading on that page begins the next, reinforcement-learning contribution. The package corrects this attribution appropriately.

The source discusses iid observations, a known reference, possibly distinct structured null and alternative classes, and two related directions: tolerance-dependent testing transitions and reference-dependent functional-estimation difficulty. It does not prescribe one loss, one neighborhood convention, or an exhaustive mathematical classification. The package supplies concrete conventions rather than claiming that one example answers every part of the source.

The workshop dates, 2–8 October 2022, appear in the report. Its locally available PDF has July 2023 creation metadata. The package's July 2023 publication statement is consistent with that metadata; the publisher's current publication record was not independently re-queried in this offline audit.

### Jiao–Han–Weissman (2018)

Theorem 4, displayed on PDF p. 5 of [*Minimax Estimation of the L1 Distance*](https://arxiv.org/abs/1705.00807), has the restriction recorded in Attempt 2:

- S >= 2;
- c log S <= log n <= C log B_n(Q), for fixed positive constants;
- B_n(Q) = sum_i min(sqrt(q_i), q_i sqrt(n log n)).

Under that restriction, the fixed-reference Poisson minimax squared risk is comparable to

A_n(Q)^2, where A_n(Q) = sum_i min(q_i, sqrt(q_i/(n log n))).

The source uses Poisson sampling and, in its construction, rescales the symbol n after sample splitting. This can alter an absolute constant in the sampling intensity, not the order conclusion used here. The logarithmic expressions require n > 1. They are not a uniform all-n statement.

For uniform Q and n comparable to S, n log n >= S for sufficiently large S. Thus B_n(Q) = sqrt(S), A_n(Q)^2 = S/(n log n), and fixed constants satisfy the theorem's conditions. For a point reference and n >= 2, B_n(Q) = 1, so the upper logarithmic condition fails. The package correctly refuses that extrapolation. The journal year and page range are also corroborated by the references in the other supplied papers. The linked DOI itself was not separately resolved during this audit.

### Canonne–Jain–Kamath–Li (2022)

In [*The Price of Tolerance in Distribution Testing*](https://proceedings.mlr.press/v178/canonne22a.html), Theorem 5 on pp. 9–10 requires epsilon_1 <= c epsilon_2; it also restricts epsilon_2 to the stated bounded range. Theorem 39 on p. 49 strengthens the instance-sensitive upper-bound restriction to epsilon_1 <= c epsilon_2 / log(S/epsilon_2), after replacing the paper's alphabet-size notation n by S.

These hypotheses agree with the package's warning. Neither theorem, simply read through its introductory informal summary, licenses an arbitrary small-gap conclusion. The paper's bibliography also corroborates the Paninski (2008) bibliographic citation. The original Paninski PDF was not present and was not separately fetched; the audited paired-sign proof is self-contained, and no precise unverified Paninski theorem is used as a premise.

### Kania–Manole–Wasserman–Balakrishnan (2026)

The local version is [arXiv:2510.20717v2](https://arxiv.org/abs/2510.20717v2). Its arXiv stamp says 27 January 2026; its title-page manuscript date is 28 January 2026. Calling 27 January the version/revision date is appropriate.

Theorem 3.1 on p. 12 states the L1 Gaussian-sequence critical **gap**, up to logarithmic factors, at scales sigma d^(3/4), sigma sqrt(d lambda), and sigma d over the three ranges reproduced in the package, with lambda = epsilon_0/sigma. The last range is lambda comparable to d. It does not state an unrestricted larger-tolerance theorem. The boundary symbols are constant-factor comparisons rather than exact transition equalities.

Appendix C.8, p. 51, explicitly retains a constrained-moment-matching conjecture for nonsmooth norms. The paper also has sections on smooth Gaussian white noise and smooth densities. The package neither ignores those advances nor promotes the remaining conjecture to a proved statement.

**Scope conclusion:** the source-sensitive account is sound. Existing results already answer important discrete and Gaussian special cases. The audit supports the package's restrained conclusion, not an assertion that no other relevant theorem exists.

## 2. Attempt 1: fixed-reference multinomial squared risk

### Point-mass reference

For Q=e_1, the functional is exactly 2(1-p_1). The empirical estimator has squared risk 4p_1(1-p_1)/n <= 1/n. The comparison pair p_1=1/2 and p_1=1/2+h with h=1/(8 sqrt(n)) is admissible for every integer n >= 1.

Its one-observation chi-square divergence, in the stated direction, is 4h^2; the product divergence is (1+4h^2)^n-1 <= exp(1/16)-1 <= 1/15. The final numerical inequality follows from exp(x) <= 1/(1-x), 0 <= x < 1. The total-variation convention is one half the L1 distance, so TV <= sqrt(chi-square)/2 is the correct factor.

The nearest-value conversion gives max squared risk at least Delta^2(1-TV)/8 for functional separation Delta. With Delta=2h this proves a universal positive constant times 1/n. No dependence on S is hidden in that lower bound.

### Paired-sign mixture

For even S, each perturbed vector sums to one and is nonnegative when 0 <= a <= 1. Every component has L1 distance a from the uniform law. For a pair of sign vectors, the one-observation likelihood cross moment is

1 + (2a^2/S) sum_j z_j z'_j.

Taking the nth power and then averaging gives the stated second moment. The term is nonnegative and can equal zero when a=1; the exponential bound remains valid for integer n >= 1 at that endpoint. Independence of the products z_j z'_j yields the cosh expression, and cosh(t) <= exp(t^2/2) gives exp(n^2 a^4/S).

The proposed choice a^4=S/(16n^2) is admissible exactly under the stated n >= sqrt(S)/4 condition. It is not asserted outside that regime. The threshold-a/2 estimation-to-testing step is valid for the simple uniform null and the mixture alternative: average alternative risk is bounded by worst-case risk, and the optimal sum of errors is 1-TV. Consequently the reported lower-bound coefficient is correct.

At n=S, the proved risk ratio is at least a constant times sqrt(S). It is only a lower separation, not a sharp uniform-reference result. The stronger order S/log S ratio belongs to the cited theorem and the next attempt.

Independent controls reconstructed complete multinomial count distributions and their mixture, rather than merely resumming the author's likelihood-kernel formula. They include a=0 and a=1. Deliberately dropping the factor 2 in that kernel fails the control.

## 3. Attempt 2: Poisson/fixed-size transfer and sharp ratio

Both comparison directions are correct:

R^P_(2m) <= R^F_m + 4 Pr(Pois(2m)<m),

R^F_m <= R^P_(m/2) + 4 Pr(Pois(m/2)>m).

Clipping to [0,2] makes squared loss at most 4 and cannot increase loss for a target in [0,2]. In the first construction, the first m observations on N>=m have the correct iid law because N is independent of the infinite iid sequence. In the second, the independent sampled N produces the desired Poisson experiment on the event N<=m; the discarded event contributes at most 4 times its probability.

Independent Poisson counts and an independent total count followed by a multinomial sample are equivalent experiments. If only counts are given, random ordering recovers a sequence. Additional randomization is harmless: conditional expectation of the output removes it under squared loss. Infima that are not attained are handled with arbitrarily nearly minimax estimators.

Explicit admissible tail bounds are Pr(Pois(2m)<m) <= exp(-m/4) and Pr(Pois(m/2)>m) <= exp(-m/6). The precise exponential constants are immaterial. Applying the source theorem at intensities 2S and S/2, with the restrictions checked separately at each intensity, sandwiches the fixed-S-sample uniform-reference risk at order 1/log S. Exponentially small terms cannot change that order for large S.

The point-reference risk is order 1/S, so the ratio is order S/log S. The argument uses the same alphabet size and number of iid draws. It does not compare a Poisson lower bound to a fixed-size upper bound without transfer.

The unrestricted candidate A_n(Q)^2 would give 1/(n log n) at a point reference, in conflict with its order-1/n lower bound. This is a genuine obstruction to the unrestricted formula, not a proof of a particular repaired formula. The package correctly leaves the general repair unclaimed.

## 4. Attempt 3: invariance and neighborhood-local risks

The group proof is valid provided the stated preservation assumptions hold. Transforming the data by a measurable bijection transports the experiment and discrepancy exactly; applying the inverse gives equality rather than a one-sided risk comparison. The same argument transports both hypotheses of a tolerant test. For the unrestricted identity-covariance Gaussian location family, translations are transitive on the reference means. A restriction on the mean space could destroy this conclusion, as the package notes.

The Bernoulli neighborhood criterion is genuinely different from Attempts 1–2: it takes an absolute-error risk over a shrinking interval around the fixed q, rather than squared error over all P. Its two rate bounds are correct for 0<r<=1/4 and n>=1.

At q=0, zero estimation gives the r upper bound, and the empirical mean gives sqrt(r/n). For the lower pair p_0=r/2, p_1=p_0+h, h=(1/8)min(r,sqrt(r/n)), both parameters remain in [0,r]. Since p_0(1-p_0)>=3r/8, the quoted KL upper bound is valid and n KL <= 1/24. Pinsker's bound and the absolute-error nearest-value argument give the stated coefficient.

At q=1/2, the reverse triangle inequality controls empirical plug-in error. The pair with h=(1/8)min(r,n^(-1/2)) has n KL <= 1/16, and the same two-point argument applies. In particular, r=n^(-1/2), n>=16 yields n^(-3/4) at the boundary and n^(-1/2) in the interior.

Neither this neighborhood example nor changing the loss supplies an additional proof of the fixed-reference global squared-risk theorem. The package explicitly maintains the distinction. The factors of 2 between total variation and L1 in the different examples are also consistent with their stated functionals.

## 5. Attempt 4: testing–estimation reductions

The estimator-to-test argument is valid pointwise: an erroneous decision forces absolute estimation error at least delta/2. Markov's inequality then gives 2r/delta, and squared-error Markov gives 4v/delta^2. The source's constant-error implication uses delta>=6r and a nonempty alternative.

For the grid converse, all tests must concern the same scalar functional and model and have the stated uniform error guarantee at their own threshold. At a fixed functional value, at most one cell has no imposed error guarantee. The triangle inequality gives the printed 2delta+M alpha bound. In fact the deterministic inequality can be tightened to delta+delta times the number of erroneous constrained cells, so the printed result is safely conservative. Equality at a grid point and F=0 or M do not cause a missing cell.

No independence across thresholds is needed. Independent sample blocks do provide independent repetitions of any one threshold test. With base error <=1/3, the correct Hoeffding exponent is k/18; choosing odd k avoids ties. k>=18 log K, together with k>=1, gives the printed risk guarantee with kn observations. The K=1 case is harmless; if M=0 the problem is constant and should simply be treated separately rather than evaluating log(M/delta).

A single threshold only separates two sets; it does not determine values within either set. It therefore cannot replace the full family needed by this construction. Finally, the outer radius and the gap differ by the null radius. The package uses the gap when relating testing to shrinking estimation error, which is essential.

## 6. Attempt 5: complete restricted Bernoulli transition

Let p_0=nu, p_1=nu+delta, with 0<=p_0<p_1<=1/2. These are exactly the restrictions used in the proof. The alternative can still include p>1/2; monotonicity makes p_1 its least favorable endpoint.

### Endpoint and affinity bounds

For interior endpoints the Bernoulli/binomial likelihood ratio increases with the count. At p_0=0, direct inspection gives the same threshold structure, even though the familiar ratio formula contains a division by zero. Arbitrary tie randomization at a threshold can be chosen monotonically. Thus null and alternative errors are maximized at their stated endpoints.

With affinity A and h^2=1-A, the identity obtained by rationalizing both coordinate differences is exact. The first squared denominator lies between p_1 and 4p_1. The second term is at most delta^2/(1-p_1), which is at most delta^2/p_1 when p_1<=1/2. Dividing the sum by 2 gives

delta^2/(8p_1) <= h^2 <= delta^2/p_1.

This includes p_0=0 and p_1=1/2. It is not an unrestricted bound up to p_1=1: for p_0=(99/100)^2 and p_1=1, h^2=1/100 exceeds delta^2/p_1. The separate negative control detects precisely that invalid extension.

The minimum sum of endpoint errors is 1-TV. The inequalities 1-TV<=A^n<=exp(-n h^2) make **each** error at most 1/3 when their sum is at most 1/3. The proof does not make the invalid substitution that a sum at most 2/3 guarantees each at most 1/3. Conversely, each error at most 1/3 forces TV>=1/3; TV^2<=1-A^(2n)<=2n h^2 gives the stated necessary condition.

Consequently, with ceiling understood for the sufficient integer sample size,

p_1/(18 delta^2) <= n_min <= ceil(8 log(3) p_1/delta^2).

This proves the claimed universal-constant order. The likelihood-ratio test used for sufficiency need not be the equal-error minimax test; its stronger sum-error bound suffices.

### Critical-gap equivalence and feasibility

Writing g=sqrt(nu/n)+1/n, the package's algebra is correct. Put x=sqrt(nu n); for delta=Cg the relevant information quantity becomes

n delta^2/(nu+delta) = C^2(x+1)^2/[x^2+C(x+1)] >= C^2/(1+C).

For delta<=cg and 0<c<=1, it is at most 4c. For example, delta<=g/100 cannot achieve both errors <=1/3, while delta=16g is sufficient whenever that endpoint is admissible.

The phrase “within the nonvacuous range” is important. For a fully formal critical-gap definition, take the infimum over successful admissible delta in (0,1/2-nu], and assign +infinity if that set is empty. For n=1, nu=.49, even delta=.01 gives endpoint TV=.01 and is impossible. A finite rate expression alone does not remove that truncation. The package already conditions the equivalence on admissible endpoints; making the empty-set convention explicit is a nonblocking clarity improvement.

At nu=0, a sharper direct check is available. Rejecting positive counts and rejecting the all-zero sample with probability 1/3 attains both errors <=1/3 exactly when (1-delta)^n<=1/2. This agrees with the order-1/n gap. Dropping 1/n fails: delta=1/(100n) gives TV<=n delta=1/100. For fixed positive nu separated from 1/2, g has the ordinary n^(-1/2) order. The displayed interpolation is therefore complete for the stated restricted Bernoulli subproblem, with no multidimensional implication.

## 7. Reproducibility, controls, and nonblocking cautions

The portable files are:

1. `AUDIT_REPORT.md` — this source and proof audit.
2. `FROZEN_INPUTS.json` — sanitized names and SHA-256 hashes for the ten inputs.
3. `audit_controls.py` — portable, standard-library exact controls.
4. `audit_controls.json` — the recorded control output.
5. `AUDIT_MANIFEST.json` — hashes and disposition for the audit deliverables.

Run from this directory:

    python audit_controls.py --bundle ../public --output audit_controls.json

The program reads all input files, checks the exact allowlist, and hashes again after execution. It runs an unchanged author-verifier copy inside a temporary directory. This isolation is necessary because the author script writes `verification.json` beside itself. The audit does not call that script in the frozen directory.

Independent controls cover direct probability-space multinomial mixtures; zero-probability endpoints; Poisson/multinomial factorization and bounded-loss coupling directions; Bernoulli local information budgets; affinity tensorization; monotone composite endpoint errors; actual sufficient sample budgets; critical-gap algebra; and pointwise estimation/testing and grid inequalities. Seven deliberately invalid claims are rejected. Some controls overlap in mathematical subject with the author tests, but the direct mixture calculation and added negative controls are separately implemented.

No blocking correction is requested. Small possible clarifications are: make n>=1 and M>0 explicit where appropriate; specify the empty feasible-set convention for the truncated critical gap; and warn readers that the author's script writes its adjacent JSON file. The existing hypotheses and cautions already protect the mathematical conclusions.

## Final disposition

Accept the frozen package as **credited partial progress with five substantive approaches and no full resolution**. Preserve the absence of novelty and first-priority claims. Do not label the source research program solved, do not extend the cited theorems outside their restrictions, and do not present the finite checks as an independent verification of all asymptotic literature.
