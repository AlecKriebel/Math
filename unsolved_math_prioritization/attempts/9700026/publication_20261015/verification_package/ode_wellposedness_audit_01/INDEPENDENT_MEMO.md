# Independent ODE regularity memo (pre-author-proof)

Written at 2026-10-15T09:29:58+00:00 after reading only the primary model passages, before reading the author proof or earlier acceptance reports.

## Frozen input and scope

PR 880, problem 9700026, frozen head `fba74a301786f9648e48722e76f440097b0746c2`. Family: ODE regularity, continuation, and invariant barriers. No claim of solving the central persistence problem is made in this memo. Target conclusions remain hypotheses pending inspection.

Primary documents read directly: `private_sources/cities-notes.txt` lines 42–71 (model) and 2143–2177 (section 6.4, printed p. 40), plus `private_sources/1209.5120v1.txt` pp. 1–4. The 2007 notes define hard maximum influence, not probability allocation among positive scores. The deterministic state equation is z_i'=a_i(z)-z_i with a_i the Lebesgue area of the maximum-influence cell. The 2012 paper restricts its stochastic model to 0<alpha<=1 and does not by itself supply this deterministic ODE theorem.

Fix finitely many distinct interior sites x_i in Q=[0,1]^2, positive alpha,beta, and z in the positive simplex. Set p=2 alpha/beta. Pairwise dominance is equivalent, away from the finitely many sites, to

    F_ij(y,z) := |y-x_i|^2 - t_ij(z)|y-x_j|^2 <= 0,
    t_ij(z) := (z_i/z_j)^p > 0.

The equivalence uses beta>0. Multiplying alpha and beta by a common positive factor has no effect on a_i; only alpha/beta matters. In particular beta>2 alpha corresponds to p<1.

## Independent questions and failure scenarios

1. Equal weights make pairwise boundaries straight lines, so a proof that only treats genuine Apollonius circles is incomplete.
2. Multiple ties, collinear sites, tangent circles, and boundary intersections could change cell combinatorics. Differentiability of area need not be assumed; local Lipschitz continuity must survive these changes.
3. The scores are singular at the sites. Their values there can be assigned to their own sites without changing areas; a bounded-distance argument should not incorrectly treat the logarithmic scores as globally smooth.
4. Continuity alone supplies existence, not uniqueness. The ODE can nevertheless have barriers valid for every classical solution if the scalar differential inequality holds along every solution.
5. Compactness arguments must establish distance from zero on every finite time interval before invoking continuation on the open simplex.
6. No uniform local-Lipschitz constant is expected as z approaches the boundary. Distinctness of sites is essential: coincident equally weighted sites can give positive-area ties and discontinuous allocation conventions.
7. Zero populations, beta=0, or unspecified ties at positive-area coincidences are excluded; they require separate definitions and conclusions.

## Checkable auxiliary derivation independent of the candidate

For one pair write d=|x_i-x_j|>0, t=t_ij and F(y)=|y-x_i|^2-t|y-x_j|^2. Direct expansion gives the exact identity

    |grad_y F(y)|^2 = 4 [ t d^2 + (1-t) F(y) ].       (A)

Consequently the gradient is nonzero on F=0 even when t=1. On any compact range t in [m,M] subset (0,infinity), choose eps_0>0 with

    max(|1-m|,|1-M|) eps_0 <= m d^2 / 2.

Then |grad F| >= sqrt(2m) d on |F|<=eps_0. If m=M=1, any eps_0 works. Every nonempty regular level of F is a circle or a line. Its total length inside Q is <=8: split a circle into its four coordinate-monotone quadrants, and use ds<=|dx|+|dy| and variation at most 1 in each coordinate per quadrant. A line segment has length <=sqrt(2). Thus coarea yields

    area{y in Q: |F(y)|<=eps} <= 16 eps/(sqrt(2m)d),
    0<eps<=eps_0.                                      (B)

This uses neither transversal intersections between different pairwise boundaries nor generic positions. Ties lie on circles or lines and therefore have area zero. Hence the maximum defines a partition up to a null set, each a_i is well-defined, a_i>=0, and sum_i a_i=1.

For nearby t,t', |F_t-F_t'| <= 2|t-t'| on Q. A point that changes membership in the pairwise dominance region belongs to {|F_t|<=2|t-t'|}. On a compact interior population neighborhood, t_ij is Lipschitz in z and lies in a compact positive range. Formula (B), followed by a finite union over pairs, gives local Lipschitz continuity of each a_i. Multiple intersections, high imbalance with all populations still positive, collinearity, and t approaching 1 do not invalidate this argument. Constants may be large for close sites or small minimum populations; finiteness suffices.

It follows that the vector field is locally Lipschitz on the positive simplex (or positive orthant after the same area definition), so the initial-value problem has a unique local classical solution. Along any solution, a_i>=0 implies

    z_i(t) >= z_i(0)e^(-t).                            (C)

Also s=sum_i z_i satisfies s'=1-s and remains 1 when s(0)=1. Therefore on any finite interval [0,T), each coordinate is bounded below by z_i(0)e^(-T), and above by 1. The trajectory lies in a compact subset of the positive simplex, proving global forward continuation. This argument applies for every alpha,beta>0; the persistence threshold is not needed for finite-time positivity.

If an eventual scalar estimate a_i(z)>=C z_i^p is available with p<1, then z_i'>=C z_i^p-z_i. A level delta with C delta^(p-1)>1 has strict inward derivative for every positive simplex state with z_i=delta. Any first downward crossing is impossible. An all-time bound of the form min(z_i(0),delta)>0 holds without needing uniqueness, because the inequality is valid on every solution. This paragraph only checks the barrier mechanism conditional on its required area estimate.

## Pre-inspection status

Expected result: regularity and continuation should be provable by the explicit polynomial strip estimate above. Potential candidate gaps to test are an omitted uniform level-length bound, an omitted gradient bound on a whole strip, a line-limit omission, or uniqueness asserted only from continuity. These would be auxiliary ODE gaps if the elementary repair (A)–(C) applies to the exact model. Central persistence and collapse claims are not assessed here.

Checkpoint completion estimate: 35% of this ODE audit, 0% of any new central proof search. No author proof or prior verdict was consulted before this memo was saved.
