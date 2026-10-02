# Turn 5: safe shrinking-grid selection, and the exact unrestricted-grid boundary

**Final author turn, 5/5.** The unrestricted tuning/refit question remains unresolved. This turn proves a rate guarantee for genuine data-selected source estimators on a specified shrinking grid, and for a separately labeled output-safeguarded rule on a general grid. Neither theorem says that unmodified cross-validation on a general grid is rate-optimal. The final packet preserves this distinction for independent source review.

## 1. A pathwise transfer principle

Keep the iid bounded-prior model and average-regret definition of Turn 4. Let r_n=(log n/log log n)^2/n for sufficiently large n; all asymptotic statements below allow constants depending on the fixed support bound M. Let R denote arbitrary auxiliary randomness independent of the latent parameters and data before the algorithm runs.

Suppose a measurable selector hhat(Y,R) always takes values in (0,epsilon_n], where 0<epsilon_n<=1 is deterministic. The output is the exact original source fit

 A_n(Y,R)=Delta_{hhat(Y,R)}^Y(Y).

Turn 4's uniform samplewise bound holds simultaneously for every h in this interval. Therefore

 ||A_n-Delta_+||^2/n <= [n(n+3)epsilon_n]^2 m^2,                 (1)

where m=max_i Y_i. Since Reg_G(Delta_+)=O_M(r_n) and E m^2=O_M((log n/log log n)^2),

 sup_G Reg_G(A_n)
  <=O_M(r_n)+O_M(n^4 epsilon_n^2 (log n/log log n)^2).            (2)

The proof is the squared triangle inequality relative to the posterior mean vector f_G(Y), using the exact Bayesian excess-risk identity. It does not use unbiasedness of the selected score. It applies to randomized selectors as well, because conditioning on Y and R still leaves posterior mean f_G(Y).

In particular, any epsilon_n=O(n^(-5/2)) gives Reg_G(A_n)=O_M(r_n). The convenient choice epsilon_n=n^(-3) even makes the second term smaller than r_n by a factor of order n^(-1).

### A fully specified original finite-thinning protocol

For n>=2 choose, for example,

 H_n={n^(-4), 2n^(-4), ..., n*n^(-4)}.

This is a nontrivial n-element positive grid with maximum n^(-3). Choose any deterministic alpha_n in (0,1) and any integer B_n>=1. Generate B_n ordinary binomial thinnings of Y, average the original uncentered source validation scores over those thinnings, choose a minimizing h in H_n by a fixed tie rule, and refit Delta_h on the full Y. Its average regret is O_M(r_n), by (2), with no condition on alpha_n or B_n.

The same statement holds for exact Rao--Blackwell averaging or Turn 3's anchored score. The reason is the uniform closeness of all permitted full-data outputs to a good comparator, not concentration or unbiasedness of these scores. This cannot justify allowing fixed positive h, a wider unspecified grid, or claiming finite-sample oracle adaptivity. The shrinking-grid restriction is substantive and the rule need not capture the practical benefit of moderate smoothing described by the source.

For completeness, allowing the separate h=0 endpoint alongside these positive values also preserves the rate: use Delta_0 as reference, Turn 4's expected squared gap bound, and (1). This observation does not remove the positive-limit discontinuity.

## 2. Deletion-switch control in a narrower window

The previous proof avoids the adaptive correction Omega entirely. There is also an explicit bound on that correction for a narrower common window, which identifies a class where the Turn 2 reduction closes.

If hhat(y,R) belongs to (0,epsilon_n] for every count vector of length n, then for z=y-e_i and y_i>0, Turn 4 implies

 |F_{hhat(y,R)}(z)_i-F_{hhat(z,R)}(z)_i|
   <=2m_i(y)n(n+3)epsilon_n,

where m_i(y)=max_j(y-e_i)_j. Importantly, deleting one count leaves the vector length n unchanged, so the same window epsilon_n applies to both selections. Thus

 |Omega_lambda(hhat)|
  <=4(n+3)epsilon_n E_lambda[S m]
  <=4(n+3)epsilon_n [(nM)^2+nM]                                (3)

for every deterministic mean vector in [0,M]^n, using m<=S and S~Poisson(sum_i lambda_i). If epsilon_n=n^(-4), this is O_M(n^(-1)), hence no larger than the bounded-prior regret order. Integrating over bounded iid priors is permitted. This correction estimate is a deterministic-mean statement, but a minimax Bayes-regret conclusion still uses the bounded-prior comparator and its precise risk convention.

The common-window condition is essential: (3) does not bound a selector that may choose h outside it. The weaker nearzero-grid rate in Section 1 remains valid even where this particular crude correction bound is too large.

## 3. A separately labeled safeguard for a general candidate grid

Let hCV(Y,R) be the output of any proposed tuning method on an arbitrary nonempty grid; it may include moderate h, and the method may be the original finite-split selector. Let

 B_n(Y)=Delta_{n^(-4)}^Y(Y)

be the positive comparator from Turn 4. For a deterministic tolerance tau_n>=0, compute

 d_n(Y,R)=||Delta_{hCV(Y,R)}^Y(Y)-B_n(Y)||^2/n.

Define a modified selected parameter by retaining hCV if d_n<=tau_n and otherwise choosing n^(-4). Its full-data output A_safe always satisfies

 ||A_safe-B_n||^2/n<=tau_n.

Therefore, directly from the regret identity,

 Reg_G(A_safe)<=2Reg_G(B_n)+2tau_n.                              (4)

Choosing tau_n=O(r_n) yields the minimax order for bounded iid priors, whatever the preliminary selector does. The guard uses only fitted values, not the unknown G or M; constants in the rate nevertheless depend on M. It returns an estimator from the original Delta_h family, but it changes the tuning protocol. It is not the original unmodified CV rule, and no superiority in practical risk or computation is claimed. The simple squared-distance guard is a standard deterministic stability device, not asserted novel in general.

## 4. What the five turns establish

- Turn 1: the exact source family is uniformly bounded by the sample maximum; a genuine single-thinning oracle inequality holds for the U-trained loss.
- Turn 2: the exactly averaged centered score has a uniform Hudson limit; full-data refitting introduces an explicit adaptive deletion correction; an actual-family n=1 example proves that correction can be positive.
- Turn 3: an explicitly modified anchored Monte Carlo implementation approximates the averaged score at regret scale, while naive fixed-B splitting can have a different small-noise selection limit.
- Turn 4: a strictly positive deterministic corruption schedule attains the known bounded-prior minimax order, via a quantified version of the known gap-filled limit and a missing-bin comparison.
- Turn 5: arbitrary data-dependent selection within a sufficiently small positive window, including a precisely specified original finite-thinning/refit protocol, preserves that order. A general-grid output guard also gives that order, with its protocol change explicit.

The unresolved boundary is unmodified adaptive selection and full-data refitting over a general candidate grid, including the source's practical moderate-smoothing choices, without the shrinking-window restriction or a guard. Unbounded-prior/compound-risk variants likewise are not silently included. The OWR contribution states an open-ended smoothing-choice objective rather than a single fully quantified conjecture; the final source assessment must distinguish our proved constructions from that broader unresolved objective, rather than declare a stronger claim by omission.

No sixth author research turn is authorized by this packet. Subsequent work is limited to independent review, necessary correction of the five-turn material, and accurate publication of the scoped result. No historical novelty claim or human peer-review claim is made.
