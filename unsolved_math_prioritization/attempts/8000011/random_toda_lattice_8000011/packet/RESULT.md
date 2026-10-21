# Toda with tridiagonal GOE data: scoped five-turn partials

## Verdict

**Original problem unresolved after five substantive author turns. Independent review pending.** These results concern the **first simultaneous crossing**

T_all(n,epsilon)=inf{t>=0: max_(1<=i<n) b_i(t)<epsilon}.

They do not use a last-exit/permanent-decoupling time, one-end deflation, or the maximum of individual first-crossing times. The source, Deift 2007 Problem 11, asks an open-ended average-complexity question for arbitrary dimension and given positive tolerance; it does not restrict the question to a particular asymptotic regime.

## Declared model and clock

The independent initial entries are a_i~N(0,2), b_i~chi_(n−i)>0. The clock is J'=[B,J], where B has b_i above and −b_i below the diagonal. Other matrix scales follow T_(cJ)(epsilon)=c^−1 T_J(epsilon/c), c>0. A separate generator rescaling also changes time.

## Candidate partial theorems

1. **Every fixed n, small tolerance.** Let lambda_1<...<lambda_n, d=min_r(lambda_(r+1)−lambda_r), and r the almost surely unique minimizing index. As epsilon→0 with n fixed,

   E[T_all]=C_n log(1/epsilon)+B_n+o_n(1),

   C_n=E[1/d],
   B_n=E{[log d+sum_(j=r+2)^n log((lambda_j−lambda_r)/(lambda_j−lambda_(r+1)))]/d}.

   Both expectations are absolutely convergent under ordered density proportional to exp(−sum lambda_j²/4) Delta(lambda). This is a finite-n asymptotic, not a growing-n statement or an exact finite-tolerance mean. Turn 1 supplies fully explicit deterministic envelopes. Turn 2 proves integrability of the error envelope, including rare multiple collisions and norming-constant tails. Turn 3 derives the constant correction and cancels the conditional mean of the Dirichlet weight logarithms.

2. **Dimension two, every positive tolerance.** The exact first-crossing mean is

   E[T_all(2,epsilon)]=(1/(2pi)) integral_(2epsilon)^infinity exp(−d²/8) arcosh(d/(2epsilon)) arccos(2epsilon/d) dd.

   Here C_2=sqrt(pi/8) and B_2=C_2(log2−EulerGamma)/2. Dimension one has mean zero. Turn 4 derives the formula by radial/angular GOE coordinates, explicitly retaining the initial-below-threshold event.

3. **Every dimension and positive tolerance: bounds and moments.** Every positive moment of T_all is finite. In particular,

   E[T_all] <= (n−1)sqrt(n(n+1)(n+2))/(4sqrt(3)epsilon²).

   Turn 5 provides a sharper spectral upper bound, an initial-data lower bound, and a chi-CDF upper bound with Gaussian large-tolerance decay. These are inequalities, not equality formulas. The Lyapunov budget proves moment finiteness at fixed tolerance even though E[d^−2] diverges. The inverse-gap approximation must not be used to infer infinite variance of the actual stopping time.

## Explicit missing outcome

For general n>=3 and finite epsilon, this packet does not determine the expectation beyond explicit bounds, nor give a uniform dimension/tolerance asymptotic or a full-diagonalization universality law. Exact spectral formulas do not remove the simultaneous first-crossing event. The general source request is therefore unsolved. No new search or proof turns are added during review.

## Evidence and credit

- Complete arguments: turns/TURN_1.md through TURN_5.md, each with a hash checkpoint.
- Exact rational controls: 2,559 assertions across Turns 1, 3, and 5. They check formulas and signs in finite examples and do not replace the analytic proofs.
- Four floating 45-digit diagnostics for the n=2 quadrature; explicitly non-rigorous computational support.
- Classical inputs: Moser finite Toda spectral evolution; Gram/Hankel orthogonal-polynomial formulas; Dumitriu–Edelman GOE spectral coordinates. Published Deift–Trogdon and 2025 monograph 1-deflation universality is credited and not promoted to an all-coupling mean result.
- The imported prior report and desk review are credited and consume zero current author turns.
- Historical priority of these specific partial consequences is unverified. No novelty, complete-solution, human-peer-review, or external-publication claim is made.
