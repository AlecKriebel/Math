# Exact classical-corollary comparison

This is an audit deduction, not a claim that an earlier source already published the birational-map application, and not a proposed new research contribution.

## Primary analytic statement

Deshouillers–Hassani, *A note on the distribution function of phi(p−1)/(p−1)*, J. Austral. Math. Soc.93 (2012),77–83, DOI10.1017/S1446788712000250, Proposition2.1 (printed78), equation2.1 (printed79), with m=2 and g(n)=phi(n)/n, gives a continuous empirical distribution F for theta_p=phi(p−1)/(p−1), over all odd primes. The authors attribute the underlying theorem to Kátai1968. The body was read independently at printed77–79. The proper limiting-distribution assertion and continuity, rather than mere existence of a mean, are the dependencies.

Primary published PDF: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/85266A1CBFB0DE0E70C723D2EDF847AB/S1446788712000250a.pdf/a-note-on-the-distribution-function-of-varphi-lowercase-p-1-lowercase-p-1.pdf

Reading-copy SHA256017161ad82cc686054a7c7f961354c68434e8fd92228ff941ddf24623357a093. The locally read prior copy is under priority_mechanism_01/private_reading/deshouillers2012.txt; no duplicate PDF was downloaded.

Aivazidis–Sofos, arXiv:1308.5701v2, Theorem1.3(i) and its proof also provide continuity; Remark1.2 credits the n=1 mean to Stephens1969 and equivalent Pillai1941. Independently read here: PDF1–4, not the complete paper. Their prime-power wording does not cause a gap: genuine prime powers have relative density zero in the prime-power counting function, so the same continuous empirical limit holds along primes; their proof starts with primes. https://arxiv.org/pdf/1308.5701v2

## General atom obstruction

Let (a_p) be a real sequence indexed by primes. Suppose

    (1/pi(X)) #{p <= X : a_p <= t} -> F(t)

at every real t, where F is continuous. Then a_p cannot converge on a subset S of primes of positive relative upper density.

Proof. If a_p -> c along S and delta=limsup_X #S(X)/pi(X)>0, then, for every epsilon>0, all but finitely many primes of S satisfy c−epsilon < a_p <= c+epsilon. Consequently

    F(c+epsilon)−F(c−epsilon) >= delta.

Continuity at c and epsilon down to zero contradict delta>0. Endpoint values c=0 or c=1/2 present no exception. This uses only elementary weak-convergence/atom reasoning.

Applying the lemma to a_p=theta_p and S={p : p=3 mod4} proves ordinary nonconvergence of theta_p on that prime class. It also rules out convergence on any positive-density further thinning of that class. This is a direct deduction from the old scalar distribution theorem; it is not a new analytic-number-theory result.

## Published primitive-value count already supplies the approximation

Booker, Cohen, Sutherland and Trudgian, *Primitive values of quadratic polynomials in a finite field*, arXiv:1803.01435v2 (2018), section2 equations(5)–(6), Lemma1 (PDF3), supplies the estimate needed for P_p. Independently read here: PDF1–4, including the complete indicator, equations, Lemma1 and proof. Primary version: https://arxiv.org/pdf/1803.01435v2

Take Q(t)=t^2+1, e1=1, e2=N=p−1. Since Q has no zero for p=3mod4, the principal-principal sum is p−1. Lemma1 bounds every remaining sum by sqrt(p)+1. The number of squarefree divisor terms is W(N)=2^omega(N). Thus

    |P_p−theta_p(p−1)| <= theta_p (W(N)−1)(sqrt(p)+1).

Here P_p=N(1,N) for p>=3: u=0 has Q(u)=1 and is not counted as primitive, so the exclusion of u=0 in N(1,N) causes no discrepancy. The source's nonzero-discriminant hypothesis holds because disc(Q)=−4 and p is odd. The elementary W(N)<=64 N^(1/4) yields P_p/p=theta_p+o(1). This is a genuine specialization of a prior primitive-value estimate, not a conjectural fixed-base primitive-root assertion.

Ostafe–Shparlinski, arXiv:0902.3884v3, section2.1 equation(1), gives the exact map family. Set m=1, a=1, b=0, g0(X1)=X1^2+1 and h0=0, then exchange coordinates (X0,X1)=(v,u). This yields precisely L(u,v)=(u,(u^2+1)v). Independently read here: PDF2–3 construction and degree-growth context. Their theorems concern degree growth and pseudorandom-number estimates, not the target ordinary CDF. https://arxiv.org/pdf/0902.3884v3

## Transfer to the candidate statistic

For L(u,v)=(u,(u^2+1)v), the candidate's checkable finite formula and elementary Jacobi-sum estimate give, for each fixed 1/2<=x<1,

    D_p(x) = 1−theta_p+o(1),  p=3 mod4.

If D_p(x) converged along such an S, then theta_p would converge to one minus that limit, contradicting the atom obstruction. Thus no positive-density thinning of the admissible prime class can restore the ordinary CDF limit. The candidate's 23/24 bound needs its separate old mean input, but the full nonexistence conclusion already follows from the older continuous distribution theorem plus the map-counting bridge.

The map-counting bridge remains an application step: the old scalar theorem does not mention this fixed map, affine phase space, point weighting, or the OWR2004 assertion. Finding that implication in this audit is not evidence of a pre-existing published application. Conversely, merely changing the vocabulary from primitive-element density to cycle density does not create a new arithmetic mechanism. The remaining historical novelty question is exactly the application, including whether it was already known or is too immediate a corollary to satisfy the project's contribution standard.


## Novelty boundary

This comparison establishes that every nontrivial construction/arithmetic step is available from pre-2026 primary bodies, and identifies the short exact deductions that connect them. It does not establish that a previous author made those deductions or answered the2004 question. A claim of a novel triangular construction or new primitive/totient theorem is false; a claim of a new exact application is a different historical question. An audit should neither award novelty because the final wording was not found verbatim nor reject all possible application novelty solely because its proof uses classical theorems.
