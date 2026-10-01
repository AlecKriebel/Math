# Independent LCT endpoint and optimal-constant audit

Checked frozen `source_snapshot/BOUND.md` independently on 2026-10-01 04:38 UTC. No other audit verdict was consulted.

**Verdict:** Sections 2 and 4 are correct in their algebraic Fano setting. A precise general scope is: a normal finite-type complex algebraic surface S with (S,0) klt, and a finite-support effective R-Cartier R-divisor B. Properness of S is unnecessary. The strongest verified result is the finite-resolution formula below, including its attainment. Subaudit completion estimate: 100%.

## Checkable reconstruction

Choose a log resolution pi:Y -> S of the finite support of B. List the finitely many exceptional components and strict transforms needed to contain the support of both pi*B and K_Y-pi*K_S, and write

    pi*B = sum_i m_i E_i,
    K_Y-pi*K_S = sum_i (A_i-1) E_i.

Here A_i=A_S(E_i)>0 because S is klt. For BOUND's B=sum_j a_j D_j with a_j>=0 and D_j effective Cartier, m_i>=0 is immediate. Effective R-Cartier pullback is also effective in the stated general scope. Include strict transforms: restricting the list to exceptional divisors would miss thresholds imposed by divisor components on S itself.

For B!=0, at least one strict transform has m_i>0. Define

    c = min_{i:m_i>0} A_i/m_i.

The minimum is over a finite nonempty set, so 0<c<infinity. On Y, the crepant boundary for (S,tB) has coefficients

    d_i(t) = 1-A_i+t*m_i.

At t=c all are <=1. The boundary has simple normal crossings. This implies log canonicity even if some d_i are negative: blowing up a point lying on k<=2 boundary components introduces coefficient sum(d_i)-1<=1. Repeating point blowups preserves this inequality; every prime divisor over a smooth surface is obtained on a model dominated by such a finite sequence. Thus A_S(F)-c*ord_F(B)>=0 for every prime divisor F over S. An index attaining the minimum has equality, and fails this inequality for every t>c. Therefore

    lct(S;B)=c,
    (S,cB) is log canonical,
    sup_F ord_F(B)/A_S(F)
      = max_{i:m_i>0} m_i/A_i
      = 1/c.

Because all A_S(F)>0, this supremum is precisely the least nonnegative constant K with ord_F(B)<=K*A_S(F) for every F. Real, including irrational, coefficients cause no change; rationality of c is not asserted.

If B=0, all valuation orders vanish, lct(S;0)=infinity, and Kopt=0 using 1/infinity=0. There is no pair (S,infinity*0) to evaluate. BOUND already separates this case and discards zero D_j before its finite-endpoint argument.

The componentwise bound follows by applying the endpoint inequality to each remaining D_j and summing with the nonnegative finite weights a_j. It requires no equality between a threshold of a sum and thresholds of its summands.

## Local centers

For a fixed closed point P, use only E_i with P in pi(E_i) and m_i>0 in the minimum. Each pi(E_i) is closed because pi is proper. Remove the finitely many images not containing P; the resulting neighborhood of P makes the same finite-resolution computation valid. This proves the local threshold inequality for every F satisfying P in c_S(F), including divisorial centers which contain P. It does not prove a global inequality for centers elsewhere.

If P is outside Supp(B), a neighborhood misses B, the local threshold is infinity, and ord_F(B)=0 for all centers containing P. If P lies in Supp(B), its local threshold is finite and positive. Neither restricting to point centers nor forgetting strict transforms is needed.

## Boundary of the algebraic claim

A nonproper **finite-type algebraic** surface is still quasi-compact; its log resolution and the relevant divisor support have finitely many components. Thus nonproperness alone is harmless. An infinite formal sum is not an R-divisor in this setting, and lies outside BOUND's explicit finite-sum hypothesis.

If “complex surface” were broadened to an arbitrary noncompact **analytic** surface, global positivity can fail. On S=C^2 with coordinates (z,w), let

    E_n(t)=(1-t)*exp(t+t^2/2+...+t^n/n),
    f(z)=product_{n>=1} E_n(z/n)^n.

This product converges uniformly on compact sets: for |z|<=R and n>2R, n*|log E_n(z/n)| is bounded by 2n*(R/n)^(n+1), a summable sequence. Its zero at z=n has multiplicity n. The effective analytic Cartier divisor B=div(f) is consequently the locally finite sum sum_n n*{z=n}. For F_n={z=n}, A_S(F_n)=1 and ord_{F_n}(B)=n. Hence the global lct is 0 and no finite K works. This is a scope counterexample, not a counterexample to the projective algebraic source or BOUND's finite divisor family. If an analytic generalization is intended, require a finite global log resolution with finitely many relevant coefficients or another uniform positivity hypothesis.

## Primary-source cross-check

[Aline Zanardini, *A note on the stability of pencils of plane curves*, Section 2.1](https://link.springer.com/article/10.1007/s00209-021-02857-w) gives the algebraic log-resolution setup, the simple-normal-crossings coefficient criterion for log canonicity, and the local threshold definition as log canonicity on a neighborhood of a point. The formulas and the analytic boundary counterexample above were independently derived rather than quoted.
