# Turn 4 — Positive Hayman index and finite-energy perturbation

Checkpoint: 2026-10-05 06:45 UTC. Mechanism: compare logarithmic coefficients with those of a Koebe rotation using the published Bazilevich inequality. Outcome: exact Abel and Cesaro limits on the positive-index subclass; no extension to index zero. Best-guess progress toward full resolution: 20%.

## 1. Published theorem input

For f in S let

    alpha = lim_{r->1-}(1-r)^2 max_{|z|=r}|f(z)|.

The existence of this index and the maximal-growth direction are classical theorem inputs. When alpha>0, choose theta so that the direction is e^(i theta). The Bazilevich inequality, as stated and discussed on pages 106–107 of Duren–Schiffer (1988), gives

    E = sum_{n>=1} n |gamma_n-e^(-in theta)/n|^2
      <= (1/2)log(1/alpha) < infinity.                    (1)

The sign in the phase is fixed by rotating so that maximal growth occurs at 1. In fact only the existence of a unit-modulus phase lambda^n in (1) is used below. The case alpha=1 is included by E=0; then the coefficients are exactly those of a Koebe rotation.

The page images were inspected, including the constant 1/2. The original proof of Bazilevich's theorem and the full variational proof of the strengthened Grunsky theorem were not independently re-proved here. The conclusions below are complete deductions from (1), not claims to a new full-class theorem.

## 2. Finite weighted energy has a little-o linear majorant

Write d_n=gamma_n-e^(-in theta)/n and T(r)=sum n|d_n|r^n. For each cutoff K, Cauchy–Schwarz gives

    (1-r)T(r)
      <= (1-r)sum_{n<=K}n|d_n|
         + sqrt(sum_{n>K}n|d_n|^2) sqrt(r).

The finite term tends to zero as r->1. The square-root tail tends to zero as K->infinity by (1). Therefore

    (1-r)T(r) -> 0.                                    (2)

The reverse triangle inequality gives

    |A_f(r)-r/(1-r)| <= T(r).

Multiplying by 1-r and applying (2) proves

    lim_{r->1-}(1-r)A_f(r)=1.                          (3)

There is also the explicit, non-asymptotic bound

    A_f(r) <= [r+sqrt((r/2)log(1/alpha))]/(1-r).         (4)

## 3. Cesaro form

For the same cutoff K,

    sum_{n<=N} n|d_n|
      <= sum_{n<=K}n|d_n|
         + sqrt(sum_{n>K}n|d_n|^2) sqrt(N(N+1)/2).

Divide by N, first let N->infinity and then K->infinity. The result is o(N). Since each reference coefficient satisfies n|e^(-in theta)/n|=1,

    |sum_{n<=N} n|gamma_n|-N| <= sum_{n<=N}n|d_n|=o(N).

Thus the normalized coefficient averages also tend to 1.

## 4. Failure of the limiting extension

At alpha=0 the right-hand side of (1) is infinite; it gives no finite perturbation energy. The explicit bound (4) is not uniform as alpha decreases to zero. Passing to a sequence of approximating functions, without uniform tail control, would not preserve (2) or the target estimate. The general question therefore remains for zero-index functions not covered by TURN_3 or other additional hypotheses.

The limit (3) is retained as a useful consequence of a known theorem; no priority or novelty claim is made.
