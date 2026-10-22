# Initial independent attack (saved before candidate or old-audit intake)

Timestamp: 2026-10-16T16:15:10.398798+00:00

## Exact target and falsifiable necessary condition

The printed Conjecture 7.30 (Ohtsuki, printed 492) asks for interpolation in R1prime = inverse_limit R1[t]/P_k(t), P_k=product_{j=1}^k(t-q^j), with R1 the integral Laurent Habiro completion printed on page 490. It sets the n=1 value to 1. We must not replace the coefficient ring by a rationalized or localized interpolation ring.

Let x=q-1. The quotient at k=2 already suffices. Every compatible element has a unique representative a(q)+b(q)(t-q) modulo P_2 because P_2 is monic. Its n-th evaluation modulo x^2 is a(q)+b(q)(q^n-q), since every factor q^n-q^j is x-divisible and P_2(q^n) is x^2-divisible. Consequently the x coefficient is a_1+(n-1)b_0. If the n=1 value is 1 then a=1 and this coefficient is (n-1)b_0. Necessary test: c_3=2c_2. The finite quotient argument avoids assuming global convergence, uniqueness of Newton series, or division by q^a-q^b.

## Primary source intake and provisional counterexample

I personally read the printed equations on Ohtsuki 490-492 (PDF 118-120) and Le, Topology 39 (2000), printed 815 and 821 (PDF 3 and 9); also Habiro-Le (2016), printed 2693 (PDF 7). Le states c_1(M)=|H_1|^{-n(n-1)/2} n(n^2-1) lambda_C(M), in Lescop normalization, and uses q=1+x, n for sl_n (Lie rank n-1), and roots of squared length 2. On an integral sphere this predicts c_3/c_2=4, contradicting the necessary ratio 2 whenever the coefficient is nonzero. Habiro-Le Proposition 1.9 identifies its unified Taylor series with the Ohtsuki series; its projective/WRT matching still needs an exact body check.

The Poincare example printed on Ohtsuki 492 is explicitly -1 surgery on the left-handed trefoil. Its n=0 summand is 1; its n=1 summand has linear coefficient -6; all n>=2 summands start in x^2. Thus it supplies a nonzero coefficient with a directly fixed orientation. Avoid asserting a named Casson sign until conventions are checked. A provisional expected triple is (c_1,c_2,c_3)=(0,-6,-24).

## Distinct mechanism to test next

Using B(X,Y)=tr(XY) on sl_n (roots squared length 2), the adjoint quadratic Casimir has eigenvalue 2n. The theta contraction is therefore, up to its graph orientation sign, 2n dim(sl_n)=2n(n^2-1). A degree-one universal Jacobi-diagram term must yield the same cubic rank dependence. Calibrate its scalar at n=2 from the printed Poincare series; then n=3 must have four times its coefficient. To count this as independent verification, check the precise LMO-to-perturbative primary theorem and derive the contraction explicitly, rather than cite the first-coefficient assertion alone.

## Remaining bridge risks

Need to check unified invariant identification by quantum evaluations; SU(n)/PSU(n) equality on integral spheres; q versus v versus h; n versus Lie rank; root normalization; surgery orientation; and Lescop/Casson factors. Sign and a common nonzero scalar do not affect the contradiction, but an n-dependent renormalization would. No conclusion about novelty or exhaustive literature status is made.
