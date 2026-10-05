# Turn 2: a pathwise non-excursion criterion for the full beta interval

**Scoped result; ordinary SIRSN axioms still unresolved. Author turn 2 of 5.** This turn attempts to remove the high route-length moment assumption from Turn 1. It succeeds under a different, explicitly pathwise regularity condition on route diameter. It does not prove that condition from the ordinary axioms.

## 1. The geometric regularity condition

Retain the jointly measurable continuum realization (JM), the ordinary SIRSN assumptions and the Poisson-defined major-road sets E_r from Turn 1. In particular E_r is not a speed cutoff. The route images are rectifiable and non-self-intersecting. Statements about routes may hold for Lebesgue-almost every endpoint pair.

For each integer m≥1, assume that there are almost surely an epsilon_m>0 and a finite, nondecreasing function omega_m on (0,epsilon_m], tending to zero at zero, such that

    R(x,y) is contained in the closed ball B(x,omega_m(|y−x|))     (LC)

whenever x,y belong to B_m and 0<|y−x|≤epsilon_m, apart from a null set of endpoint pairs. The radius is measured from the first endpoint. The functions and epsilon_m may depend on the realized network; no integrability of their sizes or constants is assumed. This is a uniform local non-excursion condition, stronger than pointwise a.e. continuity of routes. Necessarily omega_m(t)≥t at distances for which there are eligible endpoint pairs.

For an exponent beta>2, impose the pathwise integral condition

    integral_0^{epsilon_m} t^(1−beta) omega_m(t)^2 dt < infinity   (DI)

for every m. Decreasing epsilon_m does not weaken the useful conclusion. The pair (LC),(DI) is a stated additional hypothesis, not a consequence asserted for all SIRSNs.

## 2. Theorem: locally bounded traffic density on major roads

**Theorem.** Under (JM), (LC) and (DI), the traffic measure T_{beta,r} is almost surely locally finite for every r>0. More precisely, for every bounded disc B_R, there is an almost surely finite random constant K_R,beta, independent of r, such that for every Borel A contained in B_R,

    T_{beta,r}(A) ≤ K_R,beta H^1(E_r intersect A).                 (1)

Thus the traffic Radon–Nikodym density with respect to major-road length is locally essentially bounded, uniformly over r. The unrestricted traffic is sigma-finite on the union of E_r and has the source push-forward scaling c^(beta−5).

The uniformity in r is a bound on density relative to each road-length measure. It does not imply ambient local finiteness of unrestricted traffic: H^1(union_r E_r intersect B_R) can be infinite.

**Proof.** Work on the probability-one event of the sampled-road support and far-endpoint cutoff established in Turn 1, Sections 2–3, and the countably many hypotheses (LC),(DI). Fix R. There is a finite random M such that, for almost every pair whose route has positive length in B_R, at least one endpoint belongs to B_M. This cutoff used only major-road intensity, Campbell/Tonelli and Borel–Cantelli, not any stronger route-length moment.

Choose an integer m>M+1. Choose epsilon in (0,min(1,epsilon_m)). Whenever |y−x|<epsilon and the route has positive length in B_R, both endpoints then belong to B_m. Hence (LC) applies to all contributing short pairs, outside a null set.

For a fixed displacement z, t=|z|<epsilon, the non-self-intersecting route image gives the length bound

    H^1(R(x,x+z) intersect E_r intersect A)
      ≤ H^1(E_r intersect A intersect closed B(x,omega_m(t)))    (2)

for almost every contributing x. Noncontributing routes have zero left side, so the bound holds almost everywhere after their inclusion. No estimate of the route's total length is needed. In particular a route may wiggle extensively inside its confinement ball.

Integrating (2) over x and interchanging nonnegative integrals yields

    integral H^1(R(x,x+z) intersect E_r intersect A) dx
      ≤ pi omega_m(t)^2 H^1(E_r intersect A),                    (3)

since the set of centers x whose closed radius-omega_m(t) ball contains a fixed point has area pi omega_m(t)^2. Fubini's theorem ensures the endpoint-pair null exceptional set causes no difficulty for almost every displacement z; an assertion for every individual displacement is unnecessary.

Now integrate against |z|^(−beta) dz in polar coordinates. The complete short-pair contribution is bounded by

    2 pi^2 H^1(E_r intersect A)
       integral_0^epsilon t^(1−beta) omega_m(t)^2 dt.             (4)

For |y−x|≥epsilon, ignore the route indicator but use the same far-endpoint cutoff and its elementary source-mass integral. The contribution is at most

    H^1(E_r intersect A)
        4 pi^2 M^2 epsilon^(2−beta)/(beta−2).                    (5)

Equations (4)–(5) prove (1), with the sum of their finite coefficients as K_R,beta. No independence of routes from major roads or of the random modulus from the network has been used. This is a deterministic calculation in each admissible realization.

Major-road length is almost surely finite on bounded sets. Taking countable exhaustions by R and r, and using nestedness of E_r, gives simultaneous local finiteness for all r>0. The countable union E_{1/k} supports typical route length by Turn 1's sampled-road support argument; the resulting unrestricted traffic is sigma-finite. The change-of-variables calculation in Turn 1, Section 7, supplies the stated scaling. QED.

## 3. Consequences without route-length moments

1. **Local linear confinement.** If for every m there are finite random C_m and epsilon_m>0 such that R(x,y) is contained in B(x,C_m|y−x|) for nearby endpoints in B_m, then (DI) holds for every 2<beta<4. Consequently the full source interval is covered. No moment of C_m and no high moment of total route length is required.

2. **Near-linear confinement.** It is enough that, for every rational alpha<1 sufficiently close to 1, the local bound R(x,y) contained in B(x,C_m,alpha |y−x|^alpha) holds with finite random constants. For any fixed beta<4 choose alpha>(beta−2)/2. Countably many alpha and rational beta values, together with monotonicity of the short-pair kernel, give a single probability-one event for all 2<beta<4. A modulus t times any fixed power of log(e/t) is another sufficient near-linear example.

3. **A single Holder exponent.** A modulus C_m t^alpha, with 0<alpha≤1, gives 2<beta<2+2alpha. At beta=2+2alpha, a bound C_m t^alpha/[log(e/t)]^a gives convergence if a>1/2. For alpha=1 and a>0 this proposed modulus is eventually smaller than t and cannot contain both endpoints; that formal endpoint example is meaningful only for alpha<1.

4. **Bounded stretch remains an application.** A deterministic or locally random upper bound on route length divided by Euclidean separation implies the corresponding linear diameter confinement. Aldous's bounded-stretch binary hierarchy is credited source material. The theorem does not turn that construction into a result for every SIRSN.

These conditions control Euclidean excursion, not the entire curve length. Therefore this theorem is not a relabeling of the all-moments hypothesis in Turn 1. No strict inclusion between these classes of SIRSNs is claimed without a construction witnessing it.

## 4. Relation to the first-turn estimate

The translated-ball identity (3) also offers a simpler substitute for the short-route tube bound in Turn 1. On the event len R(x,x+z)≤tK, the route is inside B(x,tK), so the expected short-route contribution is bounded by

    pi (tK)^2 E H^1(E_r intersect A)
      = pi (tK)^2 (p/r)|A|.                                    (6)

This uses the unconditional inclusion before expectation, not a false independence factorization. The long-route contribution remains |A|t E[D 1{D>K}], as before. Thus the original moment range and logarithmic beta=3 endpoint are preserved, with a simpler short-route estimate. The first-turn packing proof is not invalidated; its frozen evidence is retained unchanged.

In particular, the moment method still does not derive the full interval from E D<infinity. Replacing the finite expectation by an almost-sure local density conclusion is justified here only through the additional pathwise modulus.

## 5. Why this does not settle the ordinary-axiom case

The published source separates several continuity/coalescence properties and does not assert even its stronger Section 7.2 conditions for every SIRSN. Lemma 7.2 and the following discussion concern routes between neighborhoods of two distinct endpoints. They do not supply a quantitative uniform modulus as the two endpoints approach one another. The text explicitly leaves additional endpoint-length control open. None of those properties has been substituted for (LC),(DI) here.

Qualitative convergence omega(t)→0 alone is insufficient for the present estimate: for instance omega(t)=1/log(e/t) tends to zero, but integral t^(1−beta) omega(t)^2 dt diverges for every beta>2. This is a scalar obstruction to an inference, not a constructed SIRSN counterexample. Conversely, divergence of our upper bound at beta=4 is not a proof that the actual traffic diverges there.

The remaining unrestricted target is still to control the close-endpoint traffic for 3≤beta<4 using only ordinary source assumptions, or to produce a valid SIRSN counterexample. An automatic jointly measurable continuum realization also remains to be justified if one starts from bare finite-dimensional laws. This turn supplies a full-interval conditional theorem with a different geometric hypothesis and a stronger local density conclusion; it does not close these gaps.

**Status:** unreviewed scoped partial, 2/5 substantive author turns. Uncalibrated completion estimate for the ordinary-axiom target: 45%. The calculations use standard Tonelli/Radon–Nikodym arguments and credited SIRSN structural facts; no novelty claim.
