# Independent variational and measurable-localization baseline

Derived from the exact source question before reading the candidate proof or code. Put s=n-2>0 and k(x,y)=|x-y|^(-s), with infinity on the diagonal. For compact K define C(K)=1/inf I(mu), where the infimum is over probability measures supported on K. This normalization only multiplies the source capacity by a positive dimensional constant.

## Foundations and boundaries

Classical compact equilibrium existence follows from weak compactness of probability measures and lower semicontinuity of the nonnegative kernel energy. Ordinary Borel Choquet capacitability, regularity of finite Borel measures, and the equivalence of Borel Newtonian capacity zero with polarity are permitted classical foundations. The proof must not invoke Kellogg, the fine-topological Choquet property, Dirichlet irregularity, or equivalence of the displayed integral with potential-theoretic thinness. Positive-energy measures charge no Borel capacity-zero set: on compact F, I(mu restricted to F) >= mu(F)^2/C(F); measure regularity handles Borel sets.

The restriction x in E is essential: outside a nonempty E, every point at positive distance from E has finite integral, and an open exterior region is not polar. The case n=2 is excluded because s=0 changes the kernel and layer-cake identities. Empty and capacity-zero compact sets have zero local capacities, so their integral-finiteness set is E itself and is polar. Altering the fixed positive upper radius affects only a finite tail.

## Equilibrium first variation and global weak bound

Let mu minimize probability energy V=I(mu)<infinity on positive-capacity compact K. For any finite-energy probability nu on K, expand I((1-t)mu+t nu) and differentiate at t=0+, obtaining integral U_mu dnu >= V. The mutual energy is finite by the energy Cauchy–Schwarz inequality. If U_mu<V on a positive-capacity subset of K, select a compact subset on which U_mu<=V-epsilon and a finite-energy probability nu there; first variation contradicts this. Consequently U_mu>=V quasi-everywhere on K and mu-almost everywhere. Since its mu integral is V, it equals V mu-almost everywhere. Lower semicontinuity and the definition of supp(mu) then give U_mu<=V everywhere on supp(mu): a strict excess at a support point would have positive mu measure.

Set sigma=mu/V, so sigma(K)=C(K), U_sigma<=1 on supp(sigma), and U_sigma=1 sigma-almost everywhere. For x outside the support, let z be a nearest support point. For every support y, |z-y|<=2|x-y|, hence k(x,y)<=2^s k(z,y). Thus U_sigma(x)<=M=2^s globally. This is an elementary weak maximum bound and invokes no Wiener or Kellogg conclusion.

For every compact F, restriction energy gives sigma(F)^2/C(F)<=I(sigma restricted to F)<=M sigma(F), hence sigma(F)<=M C(F), including zero-capacity sets by finite energy. For Borel F this extends by measure regularity and inner capacity. A claimed constant 1 requires a genuine stronger maximum principle; the explicit M suffices here.

## Measurability and an independent uniform-tail localization

For compact E, f(x,r)=C(E intersect closed B(x,r)) is jointly upper semicontinuous for r>0. If (x_j,r_j)->(x,r), eventual containment in E intersect closed B(x,r+eta), followed by compact capacity continuity from above as eta decreases to zero, proves the assertion. Hence the weighted integrals are Borel. More strongly, for every eta>0 the truncated integral T_eta(x)=integral_eta^1 f(x,r)r^(-s-1)dr is continuous: inclusions at radii r plus/minus |x_j-x| give convergence for every continuity radius of the monotone function r->f(x,r), which excludes only countably many radii; dominated convergence applies on [eta,1]. Thus W_E=sup T_eta is lower semicontinuous and A(E)=E intersect union_m {W_E<=m} is Borel, indeed F_sigma. No fine-topological Choquet property is needed.

Assume C(A(E))>0. Ordinary Borel capacitability supplies compact K contained in A(E) with positive capacity and a finite-energy probability tau on K. For integers j, tails t_j(x)=integral_0^(2^-j) f(x,r)r^(-s-1)dr tend to zero at every x in K. Egorov plus regularity supplies a compact S contained in K with tau(S)>0 and uniform convergence of these tails. Fix small epsilon>0 and choose r0 such that t_{r0}(x)<epsilon for x in S. A finite covering by small closed balls has some intersection L=S intersect closed B(a,delta) with tau(L)>0. This L is compact and positive capacity, with C(L)<=diam(L)^s<=(2 delta)^s. For x in L,

    W_L(x) <= epsilon + C(L) integral_(r0)^1 r^(-s-1)dr
            <= epsilon + (2 delta)^s/(s r0^s).

Choose epsilon and then delta to make both the right side and C(L) sufficiently small. This localization is independent of the source's near-maximum-of-W argument and directly checks its required outcome.

## All-set layer cake and contradiction

For t>0, t^(-s)<=1+s integral_0^1 1_{t<=r}r^(-s-1)dr, with equality for t<=1. The inequality also holds at t=0 with extended infinities. Tonelli for nonnegative functions, without any prior integrability assumption, gives for every x

    U_sigma(x)<=sigma(L)+s integral_0^1 sigma(closed B(x,r))r^(-s-1)dr
              <=C(L)+s M W_L(x).

The right side can be made less than 1 uniformly on L, contradicting U_sigma=1 sigma-almost everywhere and sigma(L)>0. Therefore C(A(E))=0 and A(E) is polar. All references to small tails concern W_E at x in K; no uniform tail claim on all E is presumed.

## Exact sharpness claims and falsifiable tests

The ball/diameter capacity bound C(E intersect closed B(x,r))<=(2r)^s gives, for every epsilon>0, integral_0^1 C(E intersect closed B(x,r))r^(-s-1+epsilon)dr <=2^s/epsilon at every x and every compact E. Choosing a closed ball of positive capacity disproves the polar conclusion after any positive decrease in the denominator exponent. Likewise a nonnegative measurable weight w with integral_0^1 w(r)dr/r finite gives a finite weighted condition everywhere. This does not settle arbitrary nonintegrable gauge weakenings.

The middle-thirds Cantor set on a line is uncountable, compact, and polar in every n>=3: its level-j cover has 2^j pieces of diameter 3^(-j), so capacity is at most (2/3^s)^j, which tends to zero. Every local compact intersection has capacity zero, so W_E is identically zero on E. This tests the boundary that the exceptional set need not be countable.

Falsifiable checks for the candidate: correct first-variation coefficients and sign; finite mutual energy; support rather than all K in the upper bound; correct direction of the nearest-point kernel inequality; compact support of restrictions; genuinely compact positive-capacity localization; measurability before Choquet selection; justified passage of extended-valued integrals through Tonelli; n-dependent constants retained; explicit x in E; exact scope of power/weight sharpness; no claim that supplementary arithmetic checks prove these analytic steps.

This baseline supplies a complete independent mathematical route subject only to the listed classical foundations. The candidate has not yet been evaluated. Baseline checkpoint: independent setup 35%; final candidate audit 0% pending.
