# Turn 5: mandatory-cut rigidity and the final positive-exponent obstruction

**Fifth and final substantive author turn. The original general target remains UNSOLVED.** This turn tests two possible ways to close beta>3: forcing positive road-size moments from the available scalar estimates, and constructing a tree-like counterexample with traffic across a separating road. Neither completes the target. The first route has an explicit scalar obstruction; the second is ruled out under the precisely stated positive-area cut condition by a new consequence of the critical theorem.

## 1. A critical fractional-separation lemma

**Lemma.** Let A be a Lebesgue-measurable subset of R^2 such that both A and its complement have positive measure. Then

    integral_A integral_{A^c} |x−y|^(−3) dy dx = infinity.        (1)

The same conclusion holds if the integral is restricted to |x−y|<epsilon, for any epsilon>0.

**Proof.** Put f=1_A. Since f is not almost everywhere constant, there is a smooth compactly supported function phi for which

    v := integral f(x) grad phi(x) dx != 0.

Otherwise every distributional derivative of f would vanish; convolving with smooth approximate identities would give constant smooth functions, and their local L1 limit f would be constant, a contradiction.

For a unit vector e and small t>0, Taylor's formula gives, uniformly in e,

    integral [f(x+te)−f(x)] phi(x) dx
         = −t e dot v + O(t^2).                                (2)

The remainder is uniform because f is bounded and phi has compact support and bounded integrable second derivatives on a fixed compact neighborhood. Let

    D_e(t) := integral |f(x+te)−f(x)| dx,

allowing infinity. The absolute value of the left side in (2) is at most ||phi||_infinity D_e(t). Integrating over directions, and using integral_0^{2pi}|e_theta dot v|dtheta=4|v|, proves

    integral_0^{2pi} D_{e_theta}(t) dtheta ≥ c t                (3)

for all sufficiently small t, with c>0. Polar coordinates now give

    integral_{|z|<epsilon} |z|^(−3)
         integral |f(x+z)−f(x)| dx dz
      ≥ c integral_0^{epsilon'} dt/t = infinity.

The left side is twice the symmetric cross-partition integral in (1), with the indicated separation restriction. QED.

This is the critical fractional-perimeter fact in a self-contained form. It is not being inferred merely from a smooth-boundary picture. Arbitrarily irregular measurable partitions are included.

## 2. No positive-length mandatory road with two positive-area sides

Work in the (JM) setting of Turn 3. Suppose C is a measurable subset of the sampled road union E_{0+}. For length-almost every w in C, suppose there is a measurable set A_w with both A_w and A_w^c of positive Lebesgue measure, such that every route from A_w to A_w^c is forced to pass through w, apart from null exceptional sets. The exact measurable assumption required is that (w,x) -> 1_{A_w}(x) is measurable and that, for almost every endpoint pair,

    H^1(R(x,y) intersect C intersect H)
      ≥ integral_{C intersect H}
           |1_{A_w}(x)−1_{A_w}(y)| dH^1(w)                    (4)

for each bounded road window H=E_r intersect B_R. This formulation makes all endpoint/road-point exceptional sets and Tonelli uses explicit. It is satisfied by a measurable family of genuine mandatory cuts whose two source populations have positive area.

**Proposition.** Almost surely H^1(C intersect B_R)=0 for every bounded R.

**Proof.** The critical theorem gives T_{3,r}(B_R)<infinity almost surely. Multiply (4) by |x−y|^(−3), integrate the endpoints, and use Tonelli. By the lemma, the inner endpoint integral on the right is infinite at length-almost every w in C intersect E_r intersect B_R. Thus positive length of that intersection would force T_{3,r}(B_R)=infinity, a contradiction. Take a countable exhaustion by r↓0 and R↑infinity. QED.

Consequently a proposed counterexample built by forcing all pairs across a positive-area bipartition to traverse a positive-length road cannot satisfy the hypotheses of the critical SIRSN theorem. This rules out that simple tree/bottleneck mechanism. It is **not** a theorem that every abstract tree-shaped routing object is impossible: branches whose endpoint populations have zero area, nonmeasurable partitions, or objects without the SIRSN moment/intensity assumptions are not covered. Nor does the proposition bound the usage relation of a general road segment by a cross-partition relation.

In particular, the proposition does not resolve beta>3. A general compatible routing network may have cycles and pair-dependent choices; its road-usage relation need not be a cut of the endpoint plane.

## 3. A scalar obstruction to the positive-mark-moment shortcut

Turn 3 reduces finite expected traffic at beta=3+alpha to the positive intrinsic mark moment

    M_alpha = E integral_R S(w)^alpha dH^1(w).

A natural attempted shortcut is to infer some M_alpha<infinity from E D<infinity, the logarithmic band identity, and the elementary large-road/short-route bounds. The following explicit scalar model shows that these scalar facts alone do not imply any positive M_alpha. It is deliberately **not** asserted to be a SIRSN.

Let a random variable D take values 2^n for n≥1 with probabilities

    P(D=2^n) = 1/[2^(n+1) n^2],

and take the value 1 with the remaining probability. These probabilities are positive and sum to less than 1/2, so the remaining atom is legitimate. Since sum_{n≥1}1/n^2<2,

    d := E D = 1−sum_n P(D=2^n) + (1/2)sum_n 1/n^2 < 2.       (5)

Imagine a scalar route of total length D carrying one uniform mark S=D^2. Define

    h(u)=E[D 1{S>u}],
    ell(u)=E[D 1{u<S≤2u}].                                    (6)

All the exact dyadic partition identities hold:

    sum_{j in Z} ell(2^j u)=d,
    integral_0^infinity ell(u)du/u=d log 2.                    (7)

Nevertheless, for every alpha>0,

    E[D S^alpha] = E[D^(1+2alpha)] = infinity.                 (8)

Indeed its n-th series term is 2^(2alpha n)/(2n^2), which does not tend to zero. To see this without any delicate asymptotics, choose an integer m with 2alpha m≥1 and take n=mj. The terms are bounded below by 2^j/(2m^2 j^2), whose successive ratio is at least 4/3 once j≥5.

This model also respects the relevant scalar geometric upper bounds, with harmless constants. For every u,K>0,

    h(u) ≤ 2K^2/u + E[D 1{D>K}].                              (9)

If K≤sqrt(u), the tail term already bounds h(u); if K>sqrt(u), the first term is greater than 2>d. Similarly,

    P(S>u, D≤K) ≤ 2K/u.                                      (10)

The event is empty when K≤sqrt(u). Otherwise Markov gives P(D>sqrt(u))≤d/sqrt(u)≤2K/u. These are the forms obtained by bounding intersection with a high road-size set inside a route-confinement disc and using the finite major-road intensity.

Thus one cannot legitimately deduce positive mark moments solely by rearranging these identities and truncation inequalities. Additional routing geometry, stronger moment information or a genuinely quenched argument is required.

The scalar construction has no embedded planar network, no consistent route family, no verified Poisson-sampled road process and no Euclidean invariant SIRSN law. It is an obstruction to a proof shortcut, **not a counterexample to the problem**. It also does not show that M_alpha<infinity is necessary for almost-sure traffic finiteness; that necessity was never claimed.

## 4. What was attempted and what remains

The critical theorem excludes positive-area mandatory-cut traffic as a simple counterexample mechanism. The heavy scalar mark model shows why the current moment/band estimates alone cannot prove the desired positive-exponent integrability. These results pull in different directions and leave the real geometric issue untouched: control the very close endpoint pairs that share a road segment in a general compatible network, without replacing their usage relation by a tree partition or inserting extra moment assumptions.

The strongest original-assumption statement obtained is local traffic finiteness for **2<beta≤3**, with the explicit continuum realization qualification in Turns 1–3; Turn 4 gives a countably sampled traffic completion at the critical exponent under its stated (CS) setup. The full interval **2<beta<4** is covered only under the additional route-moment or non-excursion regularity proved in Turns 1–2, or under the positive mark moment in Turn 3.

For the ordinary source assumptions, the exact remaining task is:

    prove almost-sure local finiteness of T_{beta,r} for every
    3<beta<4 and r>0, or construct a SIRSN counterexample.

Finite expected traffic would follow from M_{beta−3}<infinity, but almost-sure finiteness could hold without it. A deterministic jointly measurable route version has not been constructed from arbitrary bare FDDs; the sampled completion is explicitly distinguished from that stronger claim.

## 5. Final five-turn disposition

**Original target: UNSOLVED, 5/5 substantive author turns consumed.** No sixth research turn, full-scope proof, valid original counterexample, or novelty certification is claimed. The critical theorem, geometric regularity theorem, sampling completion and final rigidity proposition require independent scoped review. Prior author artifacts and their manifests are preserved unchanged.

The proof uses credited SIRSN structural data and classical measure/probability tools. The fractional-separation argument and scalar obstruction are supplied explicitly rather than treated as numerical evidence. Uncalibrated completion estimate for the unrestricted original-axiom goal: 60%; this is not a correctness probability.
