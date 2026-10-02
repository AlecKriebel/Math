# Turn 3: deletion-anchored Monte Carlo for the actual refitted family

**Scoped partial; original selector question remains unresolved at 3/5.** This turn gives an unbiased, variance-controlled finite Monte Carlo implementation of the centered, conditionally averaged thinning score from Turn 2. It uses a different sampling implementation, with an exact delete-one anchor. The resulting selector remains subject to the same unresolved adaptive deletion correction. It does not prove the original naive finite-split implementation rate-optimal.

## 1. Setup and credit

Retain the source family F_h(y)_i=Delta_h^y(y_i), the separately defined h=0 endpoint, deterministic finite candidate set H of size K, and deterministic tie rule. Let alpha in (0,1), eta=1-alpha, n>=1, S=sum_i y_i, and m=max_i y_i. Put

 A_h(y)=||F_h(y)||^2/n,
 B_{h,i}(y)=F_h(y)_i.

Turn 1 proves 0<=F_h(u)_i<=m whenever 0<=u<=y coordinatewise. Turn 2 proves

 C_{alpha,h}(y)=E A_h(Bin(y,alpha))
   -(2 alpha/n) sum_i y_i E B_{h,i}(Bin(y-e_i,alpha)),

and

 C_{1,h}(y)=A_h(y)-(2/n)sum_i y_i B_{h,i}(y-e_i).

All zero-weight terms are omitted. The fixed-algorithm Hudson/coupled-bootstrap identity is credited to prior literature, including Oliveira--Lei--Tibshirani (2025), DOI 10.1214/24-EJS2336. Their reducible-variance discussion explicitly distinguishes finite bootstrap sampling from the infinitely averaged score. Control variates, stratification, and Hoeffding concentration are classical techniques. No historical novelty claim is made here.

## 2. Exact rare-deletion decomposition

If S=0, define all scores below to be zero. Suppose S>0. Set

 q0=1-alpha^S, q1=1-alpha^(S-1).

Let U^- have the law Bin(y,alpha) conditioned on U^-!=y. For each i with y_i>0 and S>=2, let W_i^- have the law Bin(y-e_i,alpha) conditioned on W_i^-!=y-e_i. The latter conditional law is only used when q1>0. If S=1 the q1 term is zero and no such draw is requested.

Define the exactly computable anchor

 J_{alpha,h}(y)=C_{1,h}(y)+(2 eta/n)sum_i y_i B_{h,i}(y-e_i).

Conditioning on whether any deletion occurs gives

 C_{alpha,h}(y)=J_{alpha,h}(y)
  +q0 E[A_h(U^-)-A_h(y)]
  -(2 alpha q1/n)sum_i y_i E[B_{h,i}(W_i^-)-B_{h,i}(y-e_i)].       (1)

This is an exact equality of finite sums. Indeed, for any f,

 E f(Bin(y,alpha))=f(y)+q0 E[f(U^-)-f(y)],

and the same identity for y-e_i uses q1. The anchor's eta term changes -2 to -2 alpha in the deletion term. The S=1 and S=0 conventions follow directly from the original score.

Choose I independently with P(I=i)=y_i/S. Conditional on I, draw W_I^- as above. Draw U^- independently of these, and use the same draws for every h. Define

 X_h=q0[A_h(U^-)-A_h(y)]
      -(2 alpha q1 S/n)[B_{h,I}(W_I^-)-B_{h,I}(y-e_I)],          (2)

omitting the second term if q1=0. Equation (1) implies E[X_h|y]=C_{alpha,h}(y)-J_{alpha,h}(y).

For B>=1 independent repetitions, the finite-sampling score is

 Chat_{alpha,h}(y)=J_{alpha,h}(y)+(1/B)sum_{b=1}^B X_{h,b}.        (3)

It is unbiased conditionally on y for each fixed h. Candidate scores may be strongly dependent because the sampling is shared; none of the following bounds assumes their independence.

### Sampling without rare-event rejection

It is unnecessary to repeat ordinary thinning until a deletion occurs. Draw the total deleted count D from Binomial(S,eta) conditioned on D>=1, then allocate these D deletions among the coordinate capacities y_i using the multivariate hypergeometric law. This gives U^-=y-d. For W_i^- use total S-1 and capacities y-e_i. Both are finite distributions. Equivalently, inverse-CDF sampling on their explicitly given finite probability masses realizes the algorithm from a data-independent uniform seed. This is an exact specification, not a floating-point complexity guarantee for arbitrary real alpha. The conditionally truncated-binomial probabilities must be evaluated stably if implemented numerically.

## 3. Uniform finite-sampling error

Let

 L_alpha(y)=q0 m^2+(2 alpha q1 S m/n).

The envelope gives |X_h|<=L_alpha(y) for every candidate and every draw. Therefore Hoeffding's lemma for a variable in [-L,L] gives, conditionally on y,

 E exp(t(Chat_h-C_h)) <= exp(t^2 L_alpha(y)^2/(2B)).

Consequently, for delta in (0,1), simultaneously for h in H with conditional probability at least 1-delta,

 max_h |Chat_h-C_h| <= L_alpha(y) sqrt(2 log(2K/delta)/B).         (4)

The same exponential-moment argument, summing over both signs and optimizing t, gives

 E[max_h |Chat_h-C_h| |y]
   <= L_alpha(y) sqrt(2 log(2K)/B).                              (5)

No smoothness in h, stability under deletion, or regularity of the isotonic active blocks is used. Further,

 L_alpha(y) <= eta[m^2 S+2mS(S-1)/n] <= D_alpha(y),               (6)

where D_alpha is Turn 2's deterministic score-to-Hudson error bound. This follows from 1-alpha^k<=eta k and alpha<=1.

For independent Poisson means 0<=lambda_i<=M, S~Poisson(Lambda), Lambda<=nM, and m<=S. Thus

 E L_alpha(Y) <= eta(1+2/n)[(nM)^3+3(nM)^2+nM].                  (7)

In particular, alpha_n=1-n^(-5), n>=2, B=1, and any grid with log(2K_n)=O(log n) give

 E max_h |Chat_h-C_h| = O_M(n^(-2) sqrt(log n)).                  (8)

This is smaller than the bounded-prior average-regret benchmark (log n/log log n)^2/n. The one-draw statement concerns the correction draws in (2); the exact anchor requires all relevant delete-one fits and is not free. For a permutation-equivariant histogram estimator, equal count values permit reuse of equivalent fits. No claim is made that this outperforms direct Hudson-score minimization in computational cost.

## 4. Full-data refit and the remaining statistical term

Let R be a data-independent random seed realizing all conditional simulations, and let hhat(y,R) minimize (3). The actual output is A(y,R)=F_{hhat(y,R)}(y). If the same seed is used when defining the algorithm on y-e_i, Hudson's identity applied for each fixed seed gives

 Risk_lambda(A)=E U_{hhat(Y,R)}(Y)+Omega_lambda(hhat),

where U_h is Turn 2's fixed-h unbiased risk expression and

 Omega_lambda(hhat)=(2/n)E sum_i Y_i[
   F_{hhat(Y,R)}(Y-e_i)_i-F_{hhat(Y-e_i,R)}(Y-e_i)_i].             (9)

Only the marginal simulation law at each input is essential to this identity; using the common seed makes the coupling explicit. It does not prove stability of that coupling.

Write E_MC(y,R)=max_h |Chat_h(y,R)-C_h(y)|. Score minimization and Turn 2's uniform D_alpha bound imply pointwise

 U_{hhat(y,R)}(y)<=min_h U_h(y)+2D_alpha(y)+2E_MC(y,R).

Taking expectations yields the finite-sampling, full-refit oracle reduction

 Risk_lambda(A)<=min_h Risk_lambda(F_h)+2E D_alpha(Y)
                  +2E L_alpha(Y) sqrt(2log(2K)/B)
                  +Omega_lambda(hhat).                         (10)

The modified simulation scheme closes a purely Monte Carlo approximation issue at regret scale under the displayed schedule and envelope. It does not bound Omega, and the positive-only grid comparator also remains unproved at this checkpoint. Thus (10) is conditional in precisely those statistical respects; small criterion error alone is not rate-optimality of the selected refit.

## 5. Why naive finite splitting has a different small-noise limit

The actual source-family n=1 example from Turn 2 makes the implementation distinction exact. Set y=2, H={0,log 2}, and break ties toward 0. The true family gives F_0(u)=0 and F_{log2}(u)=u/2. For alpha>1/3, exact conditional averaging selects log2 at y=2.

Instead average the original raw validation score over B ordinary independent thinnings. With probability alpha^(2B), no deletion occurs in any of the B splits. On that event all U=2,V=0, the average scores are 0 for h=0 and 1 for h=log2, and the naive Monte Carlo selector chooses 0. Therefore

 P(naive selector differs from exactly averaged selector |Y=2)
   >= alpha^(2B).                                               (11)

If alpha tends to 1 with B(1-alpha) tending to zero, this lower bound tends to one. Thus no fixed-B approximation justifies exchanging the small-noise limit with naive finite-split selection, even in the original family. This is a finite-sample conditional countercontrol. It is not a large-n regret lower bound, and separate coordinate fits cannot be substituted for the common histogram in the n>1 source algorithm.

## 6. Status and validation scope

This completes substantive author turn 3. Original status is unresolved; two author turns remain. The finite checks verify the exact centered-score decomposition, conditional laws, range bounds, and source-family n=1 selector discrepancy. Hoeffding bounds and Poisson expectations are proved above rather than inferred from numerical controls. The new sampling implementation is explicitly distinguished from the original naive finite-split proposal. All substantive claims require a separate independent audit before any result PR.
