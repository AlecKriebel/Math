# Checkable mechanism reductions and their limits

This is an independent mathematical assessment of priority implications, not a claim that the following new argument was published earlier.

## Established identification

Hansen–Scheinkman's 1993 NBER manuscript, printed p26/PDF p28, Proposition5.5, proves uniqueness of a self-adjoint generator given its time-one conditional expectation operator, by the injectivity of the real exponential under spectral calculus. It applies in the reversible setting, independent of dimension. The proposition and proof were OCR-read and visually checked in the original scan. The manuscript expressly defers nonparametric statistical inference on printed p3. Recovering a reversible generator from exact P is therefore established prior work.

Given the stationary joint density q, its first marginal identifies mu. Exact P is identified as q(x,y)/mu(x), so log(P)/Delta identifies L. Its action on cutoff affine/quadratic functions recovers the interior second-order coefficients and drift, hence S and div(S). This last test-function interpretation is elementary generator theory, and should be presented as such rather than a new identification theorem. It does not control finite-sample estimation.

## Compact inverse reduction: serious alternative, bounded conclusion

Let K be a compact metric parameter set and F:K→Y a continuous injection into a metric space. Its inverse on F(K) is uniformly continuous: otherwise there are pairs at parameter distance at least epsilon but observation distance tending to zero; compact subsequences and continuity contradict injectivity. If a measurable observation estimator z_n→F(theta) almost surely, and an approximate minimum-distance estimator theta_n in K has

    d_Y(F(theta_n), z_n) ≤ inf_(eta∈K) d_Y(F(eta), z_n) + epsilon_n,
    epsilon_n→0,

then d_Y(F(theta_n),F(theta))≤2 d_Y(z_n,F(theta))+epsilon_n→0, and theta_n→theta almost surely. A countable dense subset of K supplies a measurable approximate minimizer, using the first candidate satisfying the measurable residual threshold. This deduction shows that qualitative consistency on a fixed known compact class can be less difficult than an explicit spectral reconstruction.

The deduction alone is not a historical publication proving the submitted theorem. To invoke it for every unrestricted smooth tensor/density in the submitted class one must supply (a) compact coefficient classes with a topology strong enough to recover div S; (b) continuity of the fixed-lag forward map when the conormal boundary condition varies with S; (c) actual strong consistency for the stationary transition density; and (d) a justified selection over increasing compact classes with no known derivative-norm bound. Injectivity alone does not give inverse continuity on their noncompact union. None of the full primary results inspected proves this whole reduction for the target model. This route is not a positive worldwide-novelty argument; it prevents claiming that the *general concept* of statistical consistency by compact inverse continuity is new. A future covering primary theorem could invalidate priority even if it uses a different estimator.

## Operator-learning norm gap

Kostic et al.(2022) quantify excess prediction risk ||P S_H − S_H G||_HS² and derive finite-mode prediction/error bounds, with mixing-chain extensions. These are genuine fixed-lag operator-learning results. They do not prove convergence of all output spatial derivatives through order two, recovery of the unbounded log(P), or almost-sure local uniform tensor/divergence fitting. In an infinite eigenbasis, change just the nth positive eigenvalue of P from exp(−n²) to exp(−2n²): operator-norm error tends to zero while the generator logarithms differ by n² on that unit eigenvector. Thus bare operator-norm or prediction consistency cannot be silently converted to unrestricted generator consistency. This is an abstract operator counterexample, not a pair of tensor fields and not a impossibility theorem for the target estimator.

## Time-resolution gap

For dX=−a Xdt+sigma dW, fixed-lag mean increment/Delta tends to ((exp(−a Delta)−1)/Delta)x rather than −a x. The centered conditional increment covariance/Delta equals sigma²(1−exp(−2a Delta))/(2a Delta), generally not sigma². Fixed-lag infinitesimal-moment estimators need an inverse-semigroup correction; large sample size alone does not remove this discretization bias. This explains the materially different hypotheses in the high-frequency multivariate kernel and neural tensor bounds. It is not a critique of the submitted log-weighted estimator, which explicitly handles positive fixed lag.

## Unit-diffusion/Lamperti gap

Koskela–Spanò–Jenkins requires known covariance, and its section2 expressly says the Lamperti transform cannot be constructed from the discrete data in that result. General anisotropic covariances need not admit such a reduction: for the diagonal factor sigma(x,y)=diag(1+y,1), one necessary row-integrability identity for sigma^-1 fails: partial_y sigma^-1_11=−(1+y)^−2 whereas partial_x sigma^-1_12=0. Regardless of this witness, the paper's known-covariance hypothesis already excludes the target.

The accompanying exact controls check these formulae. They are diagnostic examples and elementary reductions, not numerical evidence of absence of earlier work.
