# Checkable derivation of the prior-source corollary relation

This is authored analysis of the exact submitted theorem, not a reproduction of a third-party source. The starting comparison is credited to [Anari and Rezaei, arXiv:1811.02933v2](https://arxiv.org/abs/1811.02933v2), section 4, equation (6), printed/PDF page 12. The retrieved PDF SHA-256 is c6d22620c7963ead242068941ef05562c8c72c40accea40cd3304705d546b405. This document establishes a mathematical implication; it does not establish who first published the final norm consequence.

## 1. Exact input and prior comparison

Let A be a nonnegative row-stochastic n-by-n matrix. If its permanent is zero the desired upper bound is immediate. Otherwise let mu be the probability of a permutation sigma proportional to the product of a_i,sigma(i), and let b_ij=Pr_mu(sigma(i)=j). These b are assignment marginals, not entries of A. They form a doubly stochastic matrix. For a probability row b and a uniform random ordering pi of its coordinates, define

    T(b) = sum_j b_j E_pi log(sum_{k >=_pi j} b_k).

The cited prior equation states

    log per(A) <= sum_ij b_ij log(a_ij/b_ij) + sum_i T(b_i).       (P)

For positive matrices its sequential comparison is well-defined everywhere. The submitted conditional-history argument handles the zero case directly. Alternatively, replace A by (1-epsilon)A+epsilon J/n, use the positive-matrix result, and pass to the limit in the final continuous input-only bound. The permanent and a^2 log(e/a), extended by zero at a=0, are continuous. This extends the prior corollary to every nonnegative row-stochastic A without importing a sparse greedy sampler that could encounter a dead end. This source-interface care is useful exposition, and is not a new entropy mechanism.

## 2. Conditional Jensen, with all coefficients retained

Assign independent uniform priorities to row coordinates. For a fixed chosen coordinate j and its priority t, the mean suffix mass is

    b_j+(1-t)(1-b_j).

Concavity of logarithm gives

    E_pi log(suffix mass at j)
       <= integral_0^1 log(b_j+(1-t)(1-b_j)) dt
       = -1 - b_j log(b_j)/(1-b_j),                         0<b_j<1.

The integral is zero at b_j=1; coordinates with b_j=0 are not sampled. Multiplying by b_j and summing the row gives

    T(b) <= -1 + sum_j q(b_j),
    q(x) = -x^2 log x/(1-x), q(0)=0, q(1)=1.                (J)

The second factor x comes from the marginal sampling weight. It is not an assumption that B has the input Frobenius bound. Combining (P) and (J),

    log per(A) <= -n + sum_ij q(b_ij) - D_matrix(B||A),
    D_matrix(B||A)=sum_ij b_ij log(b_ij/a_ij).               (E)

This is exactly the submitted equation (6). Sections 2-3 of the submitted proof reconstruct a prior comparison and an elementary Jensen simplification.

## 3. The remaining scalar step is explicit and elementary

Both A and B have total mass n. Hence

    D_matrix(B||A)=sum_ij d(b_ij,a_ij),
    d(b,a)=b log(b/a)-b+a >=0.

The entry with b=0<a contributes d(0,a)=a, even though its original KL summand is zero. Dropping those linear terms individually would be wrong; only their global sum cancels. If a=0, Gibbs support forces b=0 and d(0,0)=0.

For 0<=b<=1, elementary log inequalities give

    q(b)<=b,
    q(b)<=h(b)=b^2 log(e/b),
    h'(b)=b(1+2 log(1/b))>0 for 0<b<=1.

For permitted a,b in [0,1], split at b=e^2 a. If b>=e^2 a, then log(b/a)>=2 and d(b,a)>=b+a>=q(b). Otherwise d>=0 can be discarded. For b<=a, monotonicity gives h(b)<=h(a). For a<b<e^2 a, b^2<e^4 a^2 and log(e/b)<=log(e/a). Thus in every case

    q(b)-d(b,a)<=e^4 a^2 log(e/a).                          (S)

The endpoints b=0 and (a,b)=(0,0) are immediate; b=1 follows by continuity. The proof never applies monotonicity of h beyond one. Summing (S) in (E) yields exactly

    per(A)<=exp(-n+e^4 sum_ij a_ij^2 log(e/a_ij)).           (C1)

No new theorem from the Bethe row maximization or the 2026 stability machinery is required here. The elementary estimate (S) is an added estimate in this exposition; this review neither identifies a prior printed occurrence of (S) nor certifies it as novel or non-routine.

## 4. Input Frobenius conversion and exact source quantifiers

Put S=sum a_ij^2. Row stochasticity gives 1<=S<=n. With p_ij=a_ij^2/S,

    sum a_ij^2 log(1/a_ij)=(S/2)(H(p)-log S)
                            <= S log n,

since p has at most n^2 points and log S>=0. Hence

    per(A)<=exp(-n+e^4 S(1+log n)).                         (C2)

For each fixed gamma>=1 and S<=gamma this is at most

    exp(e^4 gamma)n^(e^4 gamma)e^(-n),                      all n>=1,
    n^(3e^4 gamma)e^(-n),                                  n>=2.

The prefactor-free second formula fails at n=1, where per([1])=1. For doubly stochastic matrices, the prior van der Waerden lower bound n!/n^n supplies the other side of the original polynomial-factor exponential order. The hypothesis is unnormalized S<=gamma; replacing it by S/n<=gamma would admit I_n and invalidate the target. Allowing gamma=gamma_n to grow gives only exp(-n+O(gamma_n log n)), which is not a fixed-degree polynomial factor in general.

## 5. The 2026 exact sequential identity gives the same corollary

[Anari, arXiv:2608.28031v2](https://arxiv.org/abs/2608.28031v2), section 4, Lemma 7 / equation (24), pp. 9-10, has PDF hash e166fb3d448e33307396df4eb6d00bef8b804c6387d8aba56c959ea7ff942927. Let

    c(B)=sum_ij(1-b_ij)log(1-b_ij),
    beta_A(B)=-D_matrix(B||A)+c(B),
    g_Anari(b)=T(b)-sum_j(1-b_j)log(1-b_j),
    D_seq=E_pi D_KL(mu||nu_pi)>=0.

Their identity is

    log per(A)=beta_A(B)+sum_i g_Anari(b_i)-D_seq
              =-D_matrix(B||A)+sum_i T(b_i)-D_seq.           (A26)

The sequential KL is a divergence between distributions on permutations. It is distinct from the matrix divergence between B and A. The source's vector g is also distinct from the submitted scalar q. Discarding D_seq, then applying (J), (S), and the input entropy conversion, proves (C1)-(C2). The final norm consequence is therefore demonstrably a corollary of this source too, although its Lemma 7 does not itself print that consequence. Literal Frobenius searches in its optimization appendix cannot decide this implication.

## 6. Another current entropy theorem has the same implication

[Dong and Jain, arXiv:2609.02017v1](https://arxiv.org/abs/2609.02017v1), section 3, Theorem 3.1, p. 9, bounds the entropy of an arbitrary law on perfect matchings using its marginals. For g=4 on the complete bipartite graph, their bound is

    H(mu)<=H_B(B)+(1/2)sum_{vertices v} F(B_v),
    F(b)=T(b)-sum_j(1-b_j)log(1-b_j).

Every edge contributes twice to the vertex sum. Therefore its right side equals

    -sum_ij b_ij log b_ij + (1/2)(sum_rows T(b_i)+sum_columns T(b^j)).

Applying (J) to rows and columns yields precisely

    H(mu)<=-sum_ij b_ij log b_ij-n+sum_ij q(b_ij).

This is the submitted arbitrary-permutation entropy lemma, now obtained from another prior theorem with an explicit algebraic comparison. Its general girth-dependent results are stronger in a different direction. The submission's scalar estimate and Frobenius conversion again finish the same corollary. This reinforces method credit, not a claim that the norm statement was already explicitly published there.

## 7. What this proves and what it leaves open

The target theorem is an explicit consequence of established marginal-entropy comparisons with elementary added estimates. It is inappropriate to describe the whole mechanism as a new method or as independent of those sources. The source relation is affirmative and checkable; it is stronger evidence than a negative keyword search. The separate historical question whether the exact scalar or norm conclusion has been previously published remains UNKNOWN. No conclusion concerning copying, intent, worldwide open status, first solution, sharp exponent, or scholarly independence follows from these mathematical implications.
