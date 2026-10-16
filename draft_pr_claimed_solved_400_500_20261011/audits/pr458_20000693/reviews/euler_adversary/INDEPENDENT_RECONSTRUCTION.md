# Independent analytic/arithmetic reconstruction

This review addresses the defined constant and model mechanism, not priority and not a proof of the moment conjecture. Frozen PR458 head: `87a39f7b4e5ef81aacf98464f86586cc95684d7f`.

## Local algebra

For nonnegative weights a_i, put A=sum a_i. The analytic branch at zero of (1-u_i z)^(-a_i) has coefficients (a_i)_r u_i^r/r!, with u_i=chi_i(p) of modulus at most one. Cauchy convolution and the nonnegative binomial convolution identity give |b_r| <= (A)_r/r!. The latter sequence grows polynomially, so its square series converges at x=1/p <= 1/2. Parseval applies at radius sqrt(x), yielding a positive local mean; the constant coefficient gives J_p >= 1. The coefficient b_1 is exactly sum a_i u_i. For fixed weights, the entire tail from r>=2 is at most C_A x^2, uniformly in the prime and character values; one explicit finite C_A is sum_{r>=2} ((A)_r/r!)^2 2^{-(r-2)}. Hence J_p=1+|b_1|^2/p+O_A(p^-2).

## Exact deletions and common phase

If psi_i induces chi_i and has conductor f_i dividing q_i, deleting primitive Euler factors gives L(s,chi_i)=L(s,psi_i) times product over p|q_i of (1-psi_i(p)p^-s). The factors at p|f_i are one. For Q=lcm q_i, the character induced modulo Q has every p|Q deleted. Returning to the original q_i therefore requires inverse factors (1-psi_i(p)p^-s)^(-1) at p|Q, p not dividing q_i. This sign follows by dividing the two exact identities in the half-plane of absolute convergence and then continuation. On Re(s)=1/2 their denominators cannot vanish.

A deleted factor is correlated with other factors at the same prime: all see p^-it. Its phase mean must be joint. For two equal unit local values with weights one and x=1/p, the true joint mean is (1+x)/(1-x)^3. The product of two independent means would be 1/(1-x)^2 and differs for every x>0. This alone falsifies the separate-local-phase replacement.

## Primitive collisions and regularization

Group only equal primitive inducers and sum their weights to M_psi. At p outside S={p:p|Q}, each primitive value is a unit and |sum M_psi psi(p)|^2 = sum M_psi^2 + 2 sum_{psi<phi} M_psi M_phi Re(psi(p)conj(phi(p))). Thus the necessary divergent diagonal exponent is E=sum M_psi^2. Distinct primitive characters induce distinct characters on a common modulus: otherwise uniqueness of the primitive inducer would force equality. Consequently each cross quotient rho=psi*conj(phi) is nonprincipal. Conjugacy does not force equality; for a quartic primitive character chi modulo five, rho between chi and conj(chi) is chi^2, a nonprincipal quadratic character.

Multiplying J_p(1-1/p)^E by |1-rho(p)/p|^(2 M_psi M_phi) cancels, rather than doubles, the cross coefficient. The remainder H_p=1+O_a(p^-2) is positive. Absolute summability of H_p-1 and positivity of every finite factor imply the H product is finite and strictly positive. Solving the regularization identity restores positive powers |L^S(1,rho)|^(2 M_psi M_phi), not their reciprocals. Nonprincipal Dirichlet L-values at one are finite and nonzero; prime-ordered convergence follows from the prime number theorem for fixed arithmetic progressions with its classical error estimate, by partial summation. These are classical rigorous inputs to the defined arithmetic constant. The existence of that constant does not prove the moment model.

## Boundary checks

Zero weights are omitted before any absolute power is evaluated at a zero; this makes all definitions commute with omission. If all weights vanish, the exact integrand is one and the integral over [T,2T] is T. At exceptional primes character values may be zero, but the analytic factor still has constant coefficient one, and J_p>=1; no zero local factor is possible. Every factor (1-1/p)^E and every regularizing |1-rho/p| is strictly positive. Arbitrarily large but fixed conductors merely enlarge a finite exceptional-prime set.

## Benchmarks and hypotheses

Weight one for one character gives good-prime J=1/(1-x), bad-prime J=1, E=1, Barnes factor one and A=product_{p|q}(1-1/p)=phi(q)/q. Weight two gives J=(1+x)/(1-x)^3, E=4 and Barnes factor 1/12; A=zeta(2)^(-1) product_{p|q}(1-1/p)^3/(1+1/p). For zeta and the principal character modulo two, the primitive group has M=2 and E=4; at p=2 its actual J is 1/(1-x), so the ratio to the primitive-core J is (1-x)^2/(1+x)=1/6. This gives predicted coefficient 1/(12 pi^2).

For two unit local values u,v with weights one, rho=u*conj(v) and direct geometric-series algebra gives J=(1-x^2)/[(1-x)^2 |1-rho x|^2]. When their primitive classes are distinct, E=2 and H=1-x^2 at good primes, so the cross L-value exponent is +2. Equality of u,v at an individual prime does not merge distinct global primitive classes.

For general real nonnegative weights, the local facts above remain rigorous, and the unitary characteristic-polynomial identity is valid. The L-function asymptotic requires growing-cutoff prime averaging, replacement of primitive zero statistics by unitary random matrices, independence between distinct primitive constituents, and prime/zero splitting at the weighted-mean level. Integer moment information cannot establish real weights by an unsupported analytic continuation, and fixed finite-prime equidistribution cannot establish simultaneous T/cutoff limits. Exact deletion identities and bounded local corrections cannot promote transport of actual moment constants to a theorem. The author explicitly treats these steps as model assumptions.

## Prime ordering and a full boundary-limit argument

For any fixed nonprincipal quotient character rho modulo R, let theta_rho(t)=sum_{p<=t}rho(p) log p. The quantitative fixed-modulus prime number theorem in arithmetic progressions gives theta_rho(t)=O_R(t exp(-c_R sqrt(log t))); a possible fixed exceptional real zero does not defeat this eventual bound, with constants allowed to depend on R. Partial summation with g(t)=1/(t log t) gives convergence of sum_p rho(p)/p: the boundary term theta_rho(t)/(t log t) tends to zero, and the absolute value of the integral remainder is bounded by a constant times integral exp(-c_R sqrt(log t))/(t log t) dt, which is finite. The sum of every logarithmic Euler term of degree >=2 is absolutely convergent since |rho(p)|<=1. Thus the logs of the increasing-prime product converge.

To identify the boundary product with L(1,rho), rather than a merely unnamed number, use the Euler identity for sigma>1. The same partial-summation bound dominates the first-degree tails uniformly in sigma>=1, while the degree>=2 tails are uniformly dominated by sum_p p^-2. The product therefore has a continuous limit as sigma decreases to one. The nonprincipal Dirichlet L-function is continuous there, and its value is nonzero (DLMF25.15.9), so the prime-ordered boundary product equals L(1,rho), not only its modulus. Deleting the finitely many primes in S multiplies by nonzero factors. The existence and positivity of A follow. No conditional boundary Euler convergence is inferred solely from the easier Euler identity at Re(s)>1.

## Primary benchmark comparison after the independent reconstruction

The exact primary AIM request was fetched independently by direct HTTP, and its Problem5.3 object matches the author's heuristic-level scope. No quantified negative-power or variable-modulus theorem is imposed there.

Topacogullari, arXiv1909.11517v1, printed pp.2–3, was read visually. Theorem1.1 gives the fourth-moment leading constant (2pi^2)^(-1)(phi(q)/q)^2 product_{p|q}(1-2/(p+1)), which equals the coefficient derived above. Theorem1.3 has cross character conj(chi_1)*chi_2; conjugating rho changes no modulus of the L-value. Its exceptional-prime factor is phi(q_1)phi(q_2)/phi(q_1 q_2) times product_{p|q_1q_2}p/(p+1). At a prime dividing exactly one modulus this is 1/(1+x); at a prime dividing both it is (1-x)/(1+x). These are exactly J_p(1-x)^2/(1-x^2) when respectively one or both original local values vanish. This comparison is a normalization check, not a deduction of the general moment asymptotic.

Keating–Snaith, Commun.Math.Phys.214 (2000), printed pp.59–60, was read visually. Equation6 states the unitary gamma-product identity for Re(s)>-1; set s=2m for the present nonnegative real m. Equation15 gives the Barnes-G limit and exponent m^2. The matrix identity is a theorem about Haar unitary matrices; replacement of critical-line L-values by that model remains a hypothesis. The independently computed N=1 fractional gamma identity and finite normalized matrix products corroborate the matrix normalization; finite N=10000 is not asserted to be its limiting Barnes value.
