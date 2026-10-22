# Approach 5: identify the closed smooth-approximation class

Work on a fixed closed smooth manifold and fix a constant kappa. These are additional hypotheses for this route only. Let S_kappa be its smooth metrics with scalar curvature >= kappa. Let R_kappa denote the C0 closure of S_kappa within the space of continuous positive-definite metrics. Let V_kappa be the volumic lower-bound class in the intended source convention.

## Exact closed-hull lemma

R_kappa is closed. More explicitly, if g_j -> g in C0 and each g_j is in R_kappa, choose a smooth h_j with scalar curvature >= kappa and d_C0(h_j,g_j)<1/j. The triangle inequality gives h_j -> g, so g is in R_kappa. On a compact manifold one may take the supremum norm of the difference relative to a fixed smooth background tensor; positivity restricts to an open subset. This proves the assertion without any curvature argument.

If both implications

V_kappa subset R_kappa,                            (A)
R_kappa subset V_kappa                             (B)

hold, then the desired closure follows: approximate g by members of V_kappa, use (A), closedness of R_kappa, and (B), in that order. Conversely, closure of V_kappa and smooth compatibility S_kappa subset V_kappa imply (B), simply by taking smooth approximations. Thus (B) already contains an important special case of the target and must not be assumed for free.

At the zero endpoint, the preceding smooth-compatibility assertion applies to the intended relaxed scalar lower bound, not automatically to a stronger requirement of exact Euclidean ball-volume domination at every small radius. This distinction is essential.

## What the Ricci-flow literature actually supplies

Burkhardt-Guim's Theorems 4.1 and 4.3 identify the Ricci-flow weak lower-bound class on a closed manifold with R_kappa, and establish its closedness also for varying lower bounds approaching kappa. These statements do not identify it with V_kappa. The Gromov class compared in that survey's Section 5 is the cube/dihedral definition, not the small-ball definition of Section 26 of the 2017 problem list.

Gromov's neighboring smoothing question is related to (A), with strict lower bounds and possible slack in kappa; it is not the present closure question. Even if a suitable smoothing implication were available, merely knowing the smooth-to-smooth C0 closure theorem would not establish (B) for a continuous limit. The endpoint could lack any classical scalar curvature.

## Slack version, with proof

Suppose on the fixed closed manifold that:

(A') for every continuous metric v with volumic lower bound kappa and every epsilon>0, v is in R_(kappa-epsilon);
(B') every C0 limit of smooth metrics h_j with scalar curvature >= kappa-epsilon_j, epsilon_j -> 0, belongs to V_kappa.

Then volumic closure holds. Given g_j -> g with g_j in V_kappa, use (A') with epsilon=1/j to choose smooth h_j having scalar curvature >= kappa-1/j and d_C0(h_j,g_j)<1/j. The triangle inequality gives h_j -> g; (B') then gives g in V_kappa. This is a fully proved conditional reduction, not a proof of either hypothesis.

## Current results and residual obstruction

Lee's 2026 quantitative theorem still assumes smooth comparison metrics. The 2026 Fogagnolo–Gatti–Pluda theorem proves closure for an IMCF formulation in a restricted three-dimensional setting. Neither supplies the two necessary bridges above. We did not establish a volume-comparison characterization of the weak Ricci-flow class, a smoothing map preserving these volumic bounds, or a converse theorem turning its smooth limits into volumically bounded metrics. The original closure question therefore remains unresolved by this route.
