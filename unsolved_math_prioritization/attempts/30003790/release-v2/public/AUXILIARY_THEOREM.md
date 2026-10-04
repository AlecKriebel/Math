# Candidate auxiliary proof of broader literal consistency

Problem 30003790 / OWR-16161-003. Developed during independent audit, 4 October 2026.

**Review status: newly developed audit candidate, not independently audited.** This is not part of the frozen author packet and must not be represented as a second independent validation. A fresh reviewer should check it before it changes any publication or solved-status claim. No novelty claim is made: the argument uses elementary nearest-neighbor localization and conditional averaging.

## Candidate theorem

Let D be a fixed positive integer and let P be any Borel probability law on R^D, with support K. Assume:

1. The regression pairs (X_i,Y_i) are iid, Y_i=F(X_i)+epsilon_i, and the independent test point X has law P.
2. F:K -> R is bounded and continuous in the relative Euclidean topology. Write |F|<=M. Compact support with continuous F is a sufficient special case. Neither compact support nor a design density is otherwise required.
3. E[epsilon_i | X_i]=0 and E[epsilon_i^2 | X_i]<=sigma^2 almost surely, for one finite constant sigma^2.
4. An auxiliary training sample T_n is independent of the regression sample and the test point. The field a_n(T_n,z) is jointly measurable in (T_n,z), with Euclidean norm at most one. It can be arbitrary, inconsistent, or identically zero. No accuracy or growth assumption on T_n is needed.
5. Integers 1<=k_n<=n satisfy k_n -> infinity and k_n/n -> 0. All ties are broken by deterministic sample index.

For a query x, let R_n(x) be the kth Euclidean-neighbor distance among X_1,...,X_n. Order the regression covariates by

    d_n(x,X_i)=|a_n(T_n,X_i)^T(x-X_i)| + lambda_n(x) ||x-X_i||,

and average the k_n selected responses. Call the result Fhat_n(x).

Either of the following choices is allowed:

(A) lambda_n(x)=lambda for any fixed constant 0<lambda<=1;

(B) lambda_n(x)=min{1, sqrt(R_n(x)+1/n)}.

Then E[(Fhat_n(X)-F(X))^2] -> 0. If S_n includes T_n and the entire regression sample, the conditional integrated squared error

    R(S_n)=integral_K (Fhat_n(x)-F(x))^2 dP(x)

converges to zero in probability. In case (B), lambda_n(X) -> 0 in probability as well. These conclusions include any fixed nonzero noise variance satisfying assumption 3. They do not supply dimension-efficient rates or tangent recovery.

## Complete candidate proof

**Measurability.** Distances are jointly measurable, order statistics of finitely many measurable real functions are measurable, and lexicographic sorting by (distance,index) selects a measurable set of exactly k_n indices. Thus Fhat_n, R_n, lambda_n and the nonnegative integral R(S_n) are measurable. A_n may depend on both covariates and responses in T_n, but never on regression responses.

**Euclidean localization.** Fix x in K and delta>0. The definition of support gives p=P(B(x,delta))>0. For all sufficiently large n, k_n<=np/2. The number of regression covariates in B(x,delta) is Binomial(n,p), so

    P(R_n(x)>delta) <= P(Binomial(n,p)<k_n) <= exp(-np/8) -> 0.

This uses no uniform lower-mass constant; p depends on x and delta. Consequently R_n(x)->0 in probability for every x in K.

**Guard localization.** For each fixed realized sample, the scalar lambda_n(x) is common to every candidate at that query and is strictly positive. Cauchy-Schwarz gives

    lambda_n(x)||x-X_i|| <= d_n(x,X_i)
                             <= (1+lambda_n(x))||x-X_i||.

At least k_n candidates have Euclidean distance at most R_n(x). Hence the largest Euclidean distance among the selected candidates, denoted G_n(x), obeys

    G_n(x) <= (1+lambda_n(x)) R_n(x) / lambda_n(x).

In case (A), this is at most ((1+lambda)/lambda)R_n(x), which tends to zero in probability.

In case (B), whenever R_n(x)<=1 and lambda_n(x)<1,

    G_n(x) <= 2 R_n(x)/sqrt(R_n(x)+1/n) <= 2 sqrt(R_n(x)).

If lambda_n(x)=1 and R_n(x)<=1, the same bound follows from 2R_n(x)<=2sqrt(R_n(x)). Thus the displayed square-root bound holds throughout {R_n(x)<=1}. Its complement has probability tending to zero. Therefore G_n(x)->0 in probability in case (B) also. The definition similarly gives lambda_n(x)->0 in probability. The 1/n term handles repeated covariates with R_n(x)=0, preserving a strictly positive guard; all selected distances are then zero.

**Bias and variance.** Condition on T_n and all regression covariates, fixing x. The selected indices depend only on this conditioning information. IID regression pairs imply conditional independence of their noises. The averaged selected noise has conditional mean zero and conditional variance at most sigma^2/k_n. Put

    b_n(x)=k_n^(-1) sum_selected (F(X_i)-F(x)).

Continuity of F at x and G_n(x)->0 in probability imply b_n(x)->0 in probability. Also |b_n(x)|<=2M. Therefore E[b_n(x)^2]->0, and the vanishing cross term yields

    E[(Fhat_n(x)-F(x))^2] = E[b_n(x)^2] + E[conditional noise variance]
                         <= E[b_n(x)^2] + sigma^2/k_n -> 0.

The expectation is bounded by 4M^2+sigma^2, independently of x and n. Dominated convergence with respect to P proves the integrated expected-risk conclusion. Tonelli gives E[R(S_n)]=E[(Fhat_n(X)-F(X))^2], and Markov proves R(S_n)->0 in probability. Integrating the bounded probabilities P(lambda_n(x)>delta) proves lambda_n(X)->0 in probability in case (B). This finishes the candidate proof.

## What this changes and what it does not

The frozen theorem needs a uniform lower-mass hypothesis because it chooses a specific deterministic, vanishing guard and proves an explicit rate. The candidate above does not need that hypothesis for consistency: a fixed positive guard, or a local covariate-only vanishing guard, suffices under bounded continuity and the displayed noise assumptions.

Thus the lower-mass condition is not an intrinsic obstruction to literal consistency. Nor is a dimension-dependent sample rate a valid reason, by itself, to call literal consistency unsolved. The method remains an actual modification of the tangent-based neighbor rule: the tangent term can be retained even if inaccurate.

The short OWR report does not formally specify bounded F, compact support, centered conditional noise, or a uniform conditional variance bound. Conventional smooth compact regression with independent finite-variance centered noise satisfies the candidate assumptions, but this is an explicit model interpretation, not a theorem covering every unspecified noise/design distribution. Without a centering/identification assumption, the decomposition Y=F(X)+epsilon does not itself identify F.

The result also does not prove uniform consistency, almost-sure conditional-risk consistency, recovery of a tangent field, a one-dimensional statistical rate, or a uniform sample bound over all Borel designs. Sparse regions can make convergence arbitrarily slow. Any final disposition should state the model and risk mode rather than silently strengthen the question.

## Reference and source comparison

T. Klock, “Estimation of Nonlinear Single Index Models,” Oberwolfach Report 20/2018, pp.1192-1194, especially the final paragraph on p.1194. The report proposes a tangent-neighbor method for a curve-projection model and asks for noisy consistency; its surrounding discussion motivates favorable dimension dependence, without making an explicit rate part of that final question.

https://ems.press/content/serial-article-files/46744

The argument above is provided in full and does not rely on a claimed new theorem in the literature. Classical nearest-neighbor consistency is longstanding; the frozen packet itself disclaims novelty. This audit has not completed a novelty search for either safeguard formulation.
