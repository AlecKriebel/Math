# Optimality of monotonized asymptotic risk: partial results and obstructions

Problem 30005253 / OWR-11695855-006. Disposition: **unsolved** after five substantive approaches. No novel or full resolution is claimed.

## 1. Exact setting and the missing quantifiers

The source is Alessandro Rinaldo's contribution, joint with Pratik Patil, Arun Kumar Kuchibhotla and Yuting Wei, in Oberwolfach Report 46/2022, printed pp.2677–2680. Its research question asks for an optimality principle for

\[
 E(\gamma)=\inf_{\zeta\in[\gamma,\infty]}r(\zeta),\qquad r(\zeta)=R_{\rm det}(\zeta;A).
\]

Here a training set consists of independent pairs from a distribution P_p on R^p × R; A is a learning rule, and the conditional prediction risk is

\[
 Q_{p,m}(D_m)=\mathbb E_{(X_0,Y_0)\sim P_p}
 [\ell(Y_0,A(D_m)(X_0))\mid D_m].
\]

The test observation is independent of training. The loss is nonnegative. Proportional asymptotics mean p,m→∞ with p/m→ζ, and the baseline hypothesis is convergence in probability Q_{p,m}→r(ζ). Dimension-dependent distributions must be specified coherently. The endpoint ζ=∞ permits m→∞ with m/p→0; it does not permit silently using a fixed training sample size.

The source does not specify a statistical comparator class, a parameter set over which to take a worst case, or whether optimality is pointwise, minimax, admissibility, or relative to a restricted wrapper. Consequently an elementary envelope identity is not automatically a statistical solution. The five sections below test different formulations and retain the exact additional hypotheses.

Infimum is used throughout. A minimum requires an attainment assumption, for example lower semicontinuity on the compactified interval [γ,∞]. None of the elementary statements below silently assumes attainment.

## Approach 1: order-theoretic extremality

**Proposition 1.** For any r:(0,∞]→[0,∞], E is the greatest nondecreasing minorant of r.

**Proof.** Increasing γ shrinks the set over which the infimum is taken, so E is nondecreasing. The choice ζ=γ gives E(γ)≤r(γ). If h is nondecreasing and h≤r, then, for every ζ≥γ,

\[
 h(\gamma)\le h(\zeta)\le r(\zeta).
\]

Taking the infimum proves h(γ)≤E(γ). This also proves uniqueness. □

This is a maximum in the pointwise order of functions, whereas prediction risk is something one wants to minimize. In particular, it does not say that every monotone improved learner has risk at least E. The full paper already identifies this greatest-minorant characterization. It is not a new solution.

Further elementary checks: E≤r; applying the operation twice leaves E unchanged; order is preserved; and if r,s are finite with sup|r−s|≤δ, then sup|E_r−E_s|≤δ. Each follows directly from the definition or Proposition 1.

**Gap:** a specified, nontrivial statistical class and a lower bound within that class.

## Approach 2: a sharp selection-only theorem under uniform approximation

Fix γ and a triangular array of candidate predictors f_{n,j}, 1≤j≤K_n, all measurable with respect to training data T_n. Let

\[
 Q_{n,j}=\mathbb E[\ell(Y_0,f_{n,j}(X_0))\mid T_n],
 \quad d_{n,j}=r(\zeta_{n,j}),\quad d_n=\min_jd_{n,j}.
\]

Assume finite real d_{n,j}, and assume

\[
 \Delta_n=\max_j|Q_{n,j}-d_{n,j}|\xrightarrow{p}0,
 \qquad d_n\longrightarrow E(\gamma)<\infty.\tag{U}
\]

The second assumption is a grid-approximation hypothesis, not a consequence of pointwise convergence. It includes any needed endpoint continuity, discretization and truncation analysis.

**Proposition 2 (selection benchmark).** Every measurable selector J_n taking one of these candidate predictors satisfies

\[
 Q_{n,J_n}\ge d_n-\Delta_n.
\]

Thus, for every ε>0, P(Q_{n,J_n}<E(γ)−ε)→0. If independent validation provides estimates \widehat Q_{n,j} with

\[
 e_n=\max_j|\widehat Q_{n,j}-Q_{n,j}|\xrightarrow{p}0,
\]

and \widehat J_n minimizes these estimates, then Q_{n,\widehat J_n}→E(γ) in probability.

**Proof.** The lower bound holds simultaneously for all j and therefore for a data-dependent choice. For the upper bound, let j_* minimize true Q. Then

\[
 Q_{n,\widehat J_n}
 \le\widehat Q_{n,\widehat J_n}+e_n
 \le\widehat Q_{n,j_*}+e_n
 \le Q_{n,j_*}+2e_n
 \le d_n+\Delta_n+2e_n.
\]

Sandwiching proves the claim. □

If 0≤ℓ≤B and the validation sample size is v_n, conditional Hoeffding and a union bound give

\[
 \mathbb P(e_n>t\mid T_n)\le 2K_n\exp(-2v_nt^2/B^2).
\]

Therefore log(2K_n)/v_n→0 suffices. Conditioning the final risk on both training and validation still gives Q of the selected, unchanged predictor: the independent future observation is integrated against P_p. The selector must not subsequently refit an uncontrolled predictor.

Randomizing the choice does not defeat the lower bound, whether one conditions on the realized choice or averages its risk. Averaging the predictions themselves is different: for convex loss Jensen only gives an upper bound by the average risk and permits strict improvement.

This is an exact restricted optimum. It is an elementary consequence of uniform approximation and validation consistency, closely aligned with the source's oracle inequalities and its formal strong deterministic-equivalent assumption. It supplies no lower bound for general modifications, aggregation, or a different estimator. No novelty is claimed.

**Gap:** proving a useful lower bound for a broader class without assuming the required simultaneous lower bound in (U).

## Approach 3: pointwise limits cannot replace uniform approximation

The following counterexample uses bounded loss, a permutation-invariant learner, coherent distributions, and no unknown-model oracle in the selector.

For every p, let X have p independent uniform coordinates on [0,1), write U for its first coordinate, and let Y be an independent fair ±1 random variable. Set ℓ(y,a)=(y−a)^2. On m training points define

\[
 S_m=\left\{\sum_{i=1}^m U_i\right\},\qquad
 A(D_m)(x)=\begin{cases}0,&S_m\le1/m,\\1,&S_m>1/m.\end{cases}\tag{1}
\]

Braces denote fractional part. The rule is symmetric in the training observations, ignores labels, and always returns a constant. Its conditional risk is 1 in the first case and 2 otherwise. Its loss is at most 4. Since S_m is uniform, for every deterministic m,p→∞, regardless of aspect ratio,

\[
 \mathbb P(Q_{p,m}\ne2)=1/m\longrightarrow0.
\]

Thus r(ζ)=2 for every ζ∈(0,∞], and E(γ)=2 for every γ.

Now take N training observations, a=ceil(sqrt N), and build the base learner on every prefix of sizes a,…,N. The vector (S_1,…,S_N) consists of independent uniform coordinates: the map from (U_1,…,U_N) to cumulative sums modulo one is invertible and Haar-measure preserving on the N-dimensional torus. Equivalently, S_m is conditionally uniform given all previous sums, because U_m is fresh uniform. Hence

\[
 \mathbb P(\text{no candidate outputs }0)
 =\prod_{m=a}^N(1-1/m)=\frac{a-1}{N}\longrightarrow0.\tag{2}
\]

A selector can simply choose the first candidate that outputs 0, if any. It is a legitimate data-based selector and has conditional risk→1. It chooses only base fits; it never synthesizes a new predictor. This already disproves a selection lower bound E under pointwise convergence alone.

The same conclusion holds for ordinary validation: reserve v=ceil(sqrt N) fresh observations and choose the smallest empirical-risk candidate. The empirical loss difference between prediction 1 and prediction 0 is 1−2\bar Y_v. By Hoeffding,

\[
 \mathbb P(\bar Y_v\ge1/2)\le e^{-v/8}.
\]

Consequently

\[
 \mathbb P(Q_{\rm selected}=1)
 \ge1-\frac{a-1}{N}-e^{-v/8}\longrightarrow1.\tag{3}
\]

Choose p=floor(γ(N+v)) for any γ>0. Then p/(N+v)→γ, every candidate training size tends to infinity, and the maximum ratio p/a tends to infinity as permitted in the original domain. At the same time

\[
 \max_{a\le m\le N}|Q_{p,m}-2|=1
\]

with probability tending to one, so (U) fails exactly where it must.

Even bounded proportional subsample ratios expose the issue: retaining sizes ceil(N/2),…,N gives probability of an exceptional candidate tending to 1/2. The risk therefore has a nonvanishing probability of lying below E, sufficient to refute a universal asymptotic lower bound without using the endpoint ∞.

This is a counterexample to an overbroad interpretation, not to the paper's formal theorem under its stronger uniform assumptions. The source's informal equality must not be stripped of its additional hypotheses.

**Gap:** this blocks one possible general optimality claim; it does not establish the source's unspecified desired alternative principle.

## Approach 4: an explicit strict improvement in the motivating Gaussian model

Consider Y=X^Tβ_p+ε, with X∼N(0,I_p), ε∼N(0,1) independent, deterministic ||β_p||²=4, and squared loss. Let the base procedure be minimum Euclidean-norm least squares. The full conditional risk, including irreducible test noise, has deterministic profile

\[
 r(\zeta)=\begin{cases}
 (1-\zeta)^{-1},&0<\zeta<1,\\
 \infty,&\zeta=1,\\
 1+4(1-1/\zeta)+(\zeta-1)^{-1},&1<\zeta<\infty,\\
 5,&\zeta=\infty.
 \end{cases}\tag{4}
\]

These classical isotropic formulas also follow from Gaussian projections and inverse-Wishart quadratic forms. At γ=1 the envelope is exactly 4, since, for ζ>1,

\[
 r(\zeta)-4=\frac{(\zeta-2)^2}{\zeta(\zeta-1)}\ge0,
\]

with equality at ζ=2. More generally E(γ)=1/(1−γ) for 0<γ≤3/4, E(γ)=4 for 3/4≤γ≤2, and E(γ)=r(γ) for γ≥2.

Take total sample size n=p=2m, retain m observations, compute the base fit \widehat β, and return (2/3)\widehat β. This is an allowed statistical modification if scalar shrinkage is in the comparator class. Its conditional risk converges to 11/3, strictly below E(1)=4.

Here is a proof of the needed conditional, rather than merely averaged, limit. Write W=XX^T for the m×p design matrix X, P=X^TW^{-1}X, and η=X^TW^{-1}ε. Then \widehat β=Pβ+η and, for scalar t,

\[
 \|t\widehat β-β\|^2
 =\|(I-P)β\|^2+(t-1)^2\|Pβ\|^2+t^2\|η\|^2
 +2t(t-1)β^Tη.\tag{5}
\]

The two projection norms tend to 2 in probability. Indeed ||Pβ||²/4 has Beta(m/2,(p−m)/2) distribution, mean m/p=1/2 and variance tending to zero. Also

\[
 \|η\|^2=ε^TW^{-1}ε
 \ \stackrel d=\ \chi_m^2/\chi_{p-m+1}^2,
\]

where the displayed chi-square variables can be chosen independent. To see this, decompose ε into its independent radius and uniform direction, rotate that direction to a coordinate axis using the orthogonal invariance of W, and apply the Schur-complement formula for the corresponding diagonal element of W^{-1}. It is the reciprocal of the squared length of a Gaussian row after projection off the other m−1 rows, hence the reciprocal of χ²_{p−m+1}. At p=2m the ratio tends to 1 in probability.

Finally β^Tη has mean zero and

\[
 \mathbb E(β^Tη)^2
 =\frac{\|β\|^2}{p}\mathbb E\operatorname{tr}(W^{-1})
 =\frac4p\frac{m}{p-m-1}\longrightarrow0.
\]

The first identity follows from rotational invariance and the second from the Gaussian inverse-Wishart mean; it can also be obtained by the same Schur-complement calculation. Chebyshev therefore sends the cross term to zero. Adding test noise 1 to (5) yields

\[
 Q_t\xrightarrow{p}3+2(t-1)^2+t^2
 =\frac{11}{3}+3(t-2/3)^2.
\]

The exact finite-sample expectation at t=2/3 and p=2m is

\[
 \mathbb E Q_{2/3}=\frac{11}{3}+\frac{4}{9(m-1)}<4\quad(m\ge3).
\]

No inference from expected risk alone is used: the separate concentration argument proves the required conditional limit. The same projection and quadratic-form arguments give (4) away from ζ=1; at interpolation the noise ratio diverges, and at ζ=∞ its contribution vanishes while the signal-projection fraction vanishes.

Thus unrestricted statistical optimality, even in the motivating Gaussian model, is false. This is consistent with the original authors' one-step improvement and does not claim a newly discovered failure.

**Gap:** a defensible restricted class, or a different benchmark, is needed; scalar shrinkage already leaves the single-fit selector class.

## Approach 5: minimax and information in the profile

The scalar profile alone cannot identify whether its envelope is statistically optimal, even for the same fixed base learner. Let A always predict 1 and keep any common independent feature distribution.

- Model P: Y is fair ±1. Its base risk and envelope are 2, but the Bayes prediction 0 has risk 1.
- Model Q: Y=1+Z with Z fair ±sqrt(2). The same base learner has the same profile and envelope 2, and is the Bayes predictor, so no predictor can beat 2.

In both models r(ζ)=2 exactly for every finite training set, so uniform convergence is not the issue. The discrepancy is information discarded by the scalar risk curve. Replacing the variance in P by ε² makes the ratio of base risk 1+ε² to Bayes risk ε² unbounded as ε→0. An unrestricted constant-factor minimax assertion cannot follow from existence of r alone.

A valid monotonicity statement for minimax risk is more modest. Fix for each dimension p a parameter space Θ_p and family P_{p,θ}, independent of available sample size. Define the *expected* minimax prediction risk

\[
 M_{p,n}=\inf_A\sup_{\theta\in\Theta_p}
 \mathbb E_\theta\ell(Y_0,A(D_n)(X_0)).
\]

If an estimator with n+1 observations may ignore one, M_{p,n+1}≤M_{p,n}. If the limits

\[
 M(\gamma)=\lim_{p\to\infty}M_{p,\lfloor p/\gamma\rfloor}
\]

exist, then M is nondecreasing: γ_1<γ_2 eventually orders the two sample sizes for the same p and Θ_p. This proves monotonicity of the minimax value, not equality with the envelope of an arbitrary A.

Three further quantifier obstacles remain. Conditional convergence in probability need not imply convergence of expected risk without uniform integrability. Pointwise-in-θ convergence need not be uniform in θ. And

\[
 \sup_\theta\inf_\zeta r_\theta(\zeta)
 \le\inf_\zeta\sup_\theta r_\theta(\zeta)
\]

can be strict: for the two-by-two matrix [[1,2],[2,1]], the two sides are 1 and 2. Adaptation may bridge such a gap only with an identifiability and estimation argument. None is supplied by a deterministic scalar risk limit. The source's SNR-dependent factor bound is compatible with all these obstructions and is not an exact minimax characterization.

**Final gap.** No full, nontrivial statistical optimality principle has been obtained under the source's broad framework. The greatest-minorant identity is known; a sharp selection theorem needs uniform candidate control; pointwise control is insufficient; scalar shrinkage can strictly improve the envelope; and minimax optimality needs an explicit parameter family, admissible procedures, and uniform lower/upper bounds. These distinctions justify **unsolved**, not a promotion of an elementary identity to a resolution.
