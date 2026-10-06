# Turn 2: algebraic side lengths require a nonalgebraic angle cosine

Problem 30006025. Second substantive author turn. **The source geometric question remains unresolved.** This turn treats the finite discretized map model, rather than only the continuous metric-map law. It proves that an exact length-preserving polygon realization with algebraic side lengths cannot use only algebraic angle cosines. In particular, equally dividing 2pi around each map vertex fails for the finitely rescaled unit-edge models motivating the source.

The proof uses the classical Lindemann–Weierstrass linear-independence theorem, credited as an external input. Its precise statement was visually checked as Theorem C on page 1 of E. Delaygue, https://arxiv.org/abs/2210.12046v2 : exponentials of distinct algebraic numbers are linearly independent over the algebraic numbers. The paper's new E-function results are not used. No historical novelty assertion is made for the polygon deduction.

## 1. A deterministic polygon obstruction

Work at curvature minus one. Consider a simple closed geodesic N-gon with positive finite side lengths l_1,...,l_N and interior angles alpha_j strictly between zero and 2pi. Concave corners are permitted. Put beta_j=pi−alpha_j, the signed exterior turns, so beta_j is in (−pi,pi).

**Theorem.** It is impossible that all side lengths l_j are algebraic real numbers and all cos(alpha_j) are algebraic numbers.

Consequently, in any such polygon with algebraic side lengths, at least one interior-angle cosine is transcendental. Merely saying that an angle is an irrational multiple of pi would be weaker and would not state the result correctly.

As in Turn 1, framed closure requires

    H=product_j [T(l_j) R_j] = I in PSL_2(R),
    T(l)=diag(exp(l/2), exp(−l/2)),
    R_j=[c_j s_j; −s_j c_j],
    c_j=cos(beta_j/2),       s_j=sin(beta_j/2).            (1)

The angle bounds give c_j>0. If cos(alpha_j) is algebraic, both c_j and s_j are algebraic by the half-angle identities, with the appropriate real signs. Thus every coefficient in the expansion of trace(H) is algebraic.

Expand the trace in cyclic binary matrix indices i_1,...,i_N, with i_(N+1)=i_1. The term indexed by this binary sequence has the form

    [product_j (R_j)_(i_j,i_(j+1))]
       exp( (1/2) sum_j epsilon_(i_j) l_j ),              (2)

where epsilon_1=1 and epsilon_2=−1. Some coefficients may vanish, which causes no problem. The largest exponent is

    L_max=(l_1+...+l_N)/2 >0,

and, because all l_j are strictly positive, it occurs **only** for the all-one index sequence. Its coefficient is product_j c_j>0. No other term has that exponent.

If trace(H) were either 2 or −2, move that constant to the left, regarding it as an exponential term with exponent zero. Group all terms with equal exponents. Every exponent is algebraic because all l_j are algebraic, and all coefficients are algebraic. The term at L_max survives with a nonzero coefficient. We obtain a nontrivial algebraic linear relation among exponentials of distinct algebraic numbers, contradicting Lindemann–Weierstrass. Hence trace(H) is neither 2 nor −2, contradicting framed closure. This proves the theorem.

The proof includes straight corners alpha=pi, where c_j=1 and s_j=0. Degenerate zero/full angles and ideal vertices are excluded explicitly. Reversing orientation changes the signs of turns but leaves the unique maximal-exponent argument intact.

## 2. Application to the finite Janson–Louf discretization

The source's cited Janson–Louf model starts with a finite one-face map with unit edge lengths, and rescales distances by sqrt(12g/n), for positive integers n and g. This factor is algebraic. Removing tree tentacles leaves a 2-core; suppressing degree-two vertices replaces paths by edges whose lengths are integer multiples of that same algebraic factor. Every retained edge length is therefore positive algebraic.

A natural direct geometric prescription is to retain these lengths and give every corner at a degree-d vertex the angle 2pi/d. On the core d>=2, so the corner angles are in (0,pi], their cosines are algebraic (roots of unity), and the d angles sum to 2pi as required for a smooth glued vertex. Each graph edge occurs twice on the polygon boundary.

**Corollary.** No finite core in this class can be realized by a closed hyperbolic polygon with both those exact side lengths and that equal-sharing corner prescription.

More generally, allowing different corner angles does not help if all their cosines remain algebraic. Thus any exact length-preserving polygon realization must leave every wholly algebraic-cosine angle palette, even though smoothness still only demands vertexwise angle sums of 2pi.

This is a finite exact obstruction. It does not disprove an asymptotic coupling, a small length correction, or a construction with unrestricted angle variables. The source's conjectural geometric interpretation does not require the equal-sharing prescription; our corollary must not be substituted for that conjecture.

## 3. A countable-palette extension for continuous metric maps

There is also a stronger version of Turn 1 for the continuous model. Fix a positive algebraic perimeter P and any fixed profile of N angles with algebraic cosines and values in (0,2pi). Fix any side pairing/order with positive edge lengths summing to P/2.

At the equal-length point l_j=P/N, set q=exp(P/(2N)). Equation (1) makes trace(H) a Laurent polynomial in q with algebraic coefficients. Its highest term is

    (product_j c_j) q^N,

with nonzero coefficient, by the same all-one index argument. Therefore trace(H)−2 and trace(H)+2 are nonzero Laurent polynomials. Hermite–Lindemann makes q transcendental, so neither can vanish. The analytic function (trace H)^2−4 is consequently not identically zero on the length simplex. Its zero set has measure zero, exactly as in Turn 1.

There are only countably many possible angle profiles with algebraic cosines, because the algebraic numbers are countable and each cosine value has at most two preimages in (0,2pi). Taking the countable union over profiles and the finite union over pairings/orders preserves measure zero.

**Corollary.** At P=12g, or any other positive algebraic fixed perimeter, a length vector drawn from a density on the metric-map simplex almost surely has no closed geodesic polygon realization whose every angle cosine is algebraic. This holds even if the angle profile and pairing are selected after inspecting the lengths.

This assertion does not exclude the uncountable family of freely varying real angle profiles. Generic nonalgebraic angle cosines are not themselves a geometric defect. The corollary only shows that a finite or countable algebraic angle prescription cannot supply the intended lift without changing lengths or another hypothesis.

## 4. Scope and exact controls

A regular hyperbolic polygon with rational-multiple-of-pi angles has logarithmic, usually transcendental side lengths; it is consistent with the theorem. We have not asserted that arbitrary positive lengths admit a realization with free angles, or that such a realization would have the desired random-surface law. Those remain separate geometric and probabilistic tasks.

The checker uses exact rational rotation matrices with positive diagonal cosines, verifies the unique highest and lowest Laurent coefficients for many profiles, compares the matrix-product trace with the full binary-index expansion, and checks the fixed-perimeter factor of two and algebraicity structure of finite rescalings. It contains no numerical test purporting to prove transcendence. The universal conclusions rest on the expansion and the explicitly credited classical theorems.

Author turns completed: 2/5. Original question unresolved. Subjective completion estimate: 10%. The next turn will examine a controlled positive hyperbolic construction after relaxing exact length preservation, with its sampling law and existing geometric literature kept explicit.
