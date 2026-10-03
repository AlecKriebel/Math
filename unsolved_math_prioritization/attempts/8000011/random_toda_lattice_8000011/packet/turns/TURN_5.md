# Author turn 5: every finite tolerance has finite moments

2026-10-03 06:26 UTC. Final author turn, 5/5; original problem remains unresolved. Completion estimate: 100% toward this scoped partial packet, 25% toward the source's general expectation request.

This turn returns to general n and positive tolerance. It supplies explicit bounds and tail regularization, not a formula for the general-n expectation. All stopping times are FIRST simultaneous crossings.

## Lyapunov budget bounds the first crossing

For a fixed Jacobi matrix, write J(t)'=[B,J] as in the source. Let

 F(t)=sum_(i=1)^n i a_i(t), D0=diag(i−(n+1)/2),
 Q=||D0||_F=sqrt(n(n²−1)/12), S=||J(0)||_F.

Since a_i'=2(b_i²−b_(i−1)²), with b_0=b_n=0,

 F'(t)=−2 sum_(i=1)^(n−1) b_i(t)².                        (13)

Before the first time T_all at which all couplings are below epsilon, at least one coupling is >=epsilon. Therefore sum b_i²>=epsilon² on [0,T_all). Integration and the classical descending-order limit of the flow give

 0<=T_all <= [F(0)−F(infinity)]/(2epsilon²)
           <= QS/epsilon².                               (14)

For the last inequality subtract (n+1)/2 times the conserved trace from both F values, apply Frobenius Cauchy–Schwarz to each, and use ||J(infinity)||_F=S. No monotonicity of individual b_i is assumed. The proof applies up to every t<T and then takes the supremum, so it also rules out an infinite T using the finite Lyapunov budget.

For GOE, S has moments of every positive order (the independent diagonal Gaussians and off-diagonal chi variables do). Thus at EVERY fixed n and epsilon>0,

 E[T_all^p]<infinity for every p>0.                       (15)

In particular the inverse-minimum-gap asymptotic cannot be used to infer divergent second moments at fixed tolerance. Indeed E[d^−2]=infinity, whereas (15) is finite. The small-tolerance and moment limits are not interchangeable without further control.

## Explicit finite-tolerance mean bounds

Let lambda_1<...<lambda_n. Since the initial diagonals have mean zero and the descending limit is diag(lambda_n,...,lambda_1), taking the expectation of the first bound in (14) gives

 E[T_all] <= (1/(4epsilon²)) E[sum_(i<j)(lambda_j−lambda_i)]. (16)

To see the factor 1/4, sum_(i<j)(lambda_j−lambda_i)=sum_j(2j−n−1)lambda_j; the expected total trace is zero. This is a GOE spectral integral free of unknown flow or crossing times. It is an upper bound, not equality.

A closed elementary bound follows by applying Cauchy–Schwarz to the centered eigenvalue vector. Its expected squared norm is

 E[sum_j (lambda_j−mean(lambda))²]
   = E[tr J²]−E[(tr J)²]/n = n(n+1)−2 = (n−1)(n+2).

Hence

 E[T_all] <= (n−1)sqrt(n(n+1)(n+2))/(4 sqrt(3) epsilon²).    (17)

This bound is for n>=2; n=1 has T=0.

For a simple lower bound, put B0=max_i b_i(0) and rho=lambda_n−lambda_1>0. Each diagonal entry stays in [lambda_1,lambda_n], and b_i'/b_i=a_(i+1)−a_i>=−rho. Therefore

 T_all >= log^+(B0/epsilon)/rho.                          (18)

This is valid for the first simultaneous crossing; it is zero whenever all initial couplings are small. Taking expectation yields a finite initial-data/spectral integral lower bound.

One may also sharpen the large-epsilon decay of the crude upper bound. Except on a null equality event, T_all=0 on {B0<epsilon}, so (14), Cauchy–Schwarz and E[S²]=n(n+1) imply

 E[T_all] <= Q sqrt(n(n+1)) epsilon^−2 sqrt(1−prod_(k=1)^(n−1) F_(chi_k)(epsilon)).                          (19)

The product is exact because initial off-diagonals are independent. Formula (19) is an explicit all-dimension, all-tolerance upper bound with Gaussian high-tolerance decay. No asymptotic equivalence is claimed.

## Scaling convention

If the initial matrix is multiplied by c>0 while keeping the same Lax equation, its trajectory is cJ(ct). Hence T_(cJ)(epsilon)=c^−1 T_J(epsilon/c). This converts every statement in this packet to an explicitly chosen normalized GOE. It must not be confused with changing the generator by an additional factor of two.

## Final verdict after five turns

NO RESOLUTION of the original general-n, general-epsilon average-time request. The established candidates for independent review are: (i) explicit deterministic first-crossing envelopes; (ii) a rigorous fixed-n two-term expectation asymptotic with eigenvalue-only coefficients; (iii) an exact n=2 all-tolerance quadrature; and (iv) general-n all-tolerance mean bounds and all positive moments. The precise missing result is an evaluation or sharp general characterization of E[T_all] beyond the fixed-n small-tolerance regime and special dimension. No general growing-n theorem or quantitative universality is asserted.

The Lyapunov identity, orthogonal-polynomial solution and GOE laws are classical tools. Historical priority of these particular consequences is unverified, so no novelty claim is made. No further author search turns are authorized under this packet's five-turn cap; independent checking must audit these existing artifacts without silently turning into a sixth proof attempt.
