# Problem 2303021: a verified prior affirmative resolution

**Status:** already solved in the published literature. This is an AI-assisted source-status correction and mathematical scope check, not a new solution, novelty claim, human peer review, or formal verification.

## Exact mathematical interpretation

Write D = {z in C : |z| < 1}. A continuum means a nonempty compact connected set. For a continuum E contained in the closed unit disk with 0 not in E, let U be the connected component of D minus E containing 0. The quantity under discussion is

    h(E) = omega_U(0, E intersect boundary(U)).

Thus the exit-boundary payoff is 1 on E and 0 on the rest of the boundary of U. The datum includes any part of E on the unit circle. Interpreting the notation as ordinary harmonic measure in the unpunctured disk of E intersect boundary(D) would change the question when E has interior points.

Equivalently, for planar Brownian motion started at 0, let T be its first exit time from D and let tau_E be its first hitting time of E. The convention corresponding to this boundary payoff is P(tau_E <= T). The non-strict inequality is essential: if E is an arc of the unit circle, contact occurs at T. The strict-before-exit event would have probability zero in that example and would make the desired positive lower bound false. This probabilistic interpretation is explanatory; the cited theorem is about harmonic measure.

For d = diam(E), the asserted estimate is

    h(E) >= arcsin(d/2)/pi.

The inverse sine takes its real principal value in [0, pi/2], because 0 <= d <= 2. The argument is d/2, rather than a fixed inverse-sine value subsequently multiplied by d.

## Published result and its match

FitzGerald, Rodin, and Warschawski, *Estimates of the harmonic measure of a continuum in the unit disk*, Transactions of the American Mathematical Society 287(2) (1985), 681–685, Theorem 2, establishes this inequality for continua in the closed disk. The introduction excludes the observation point from the continuum and explicitly links the result to Problem 3.21. Their Section 3 uses a normalized radial-slit conformal map, its distance comparison, and Gaier's anchored-continuum estimate. The last dependency includes an extension from arcs which the paper describes without providing its full details. [DOI](https://doi.org/10.1090/S0002-9947-1985-0768733-1)

Applying that theorem to E = alpha gives precisely the requested result, with no limiting geometry, smoothness, simple-connectivity assumption on U, or diameter loss added by this application. The theorem itself is a cited external mathematical input. This packet does not independently re-prove Gaier's theorem or its continuum extension.

Hayman–Lingham's 2018 Update 3.21, printed page 67, already records the affirmative resolution and cites this paper as reference 270. The earlier open-triage classification is therefore stale. [Problem and update](https://arxiv.org/pdf/1809.07200v2#page=68)

Solynin's 1985 article, *On the harmonic measure of continua of a fixed diameter*, has a publisher abstract stating the same bound for the component containing 0 and excluding 0 from E. It provides independent corroboration; its proof and equality classification are not additional dependencies of this packet. [Publisher record](https://www.mathnet.ru/eng/znsl5307)

## Direct sharpness check

For any prescribed d in [0,2], put theta = arcsin(d/2) and

    A_theta = {exp(it) : -theta <= t <= theta}.

This set is a compact connected subset of the unit circle. For s,t in [-theta,theta],

    |exp(is)-exp(it)| = 2 |sin((s-t)/2)| <= 2 sin(theta) = d,

because |s-t|/2 <= theta <= pi/2. Equality occurs at the endpoints. Hence its diameter is exactly d, including the endpoint theta = pi/2, where the set is a semicircle.

The Poisson kernel of D at 0 is constant 1/(2 pi). Therefore

    h(A_theta) = (2 theta)/(2 pi) = arcsin(d/2)/pi.

This independently checks that the numerical bound cannot be increased for any allowed diameter. It establishes an extremizing family, not an exhaustive classification of equality. For d = 2 one must choose a semicircle in this construction: a longer arc still has diameter 2 but has strictly larger harmonic measure, so an arbitrary circular arc of that diameter need not attain equality.

## Degeneracies and necessary hypotheses

1. If d = 0 and 0 is outside E, the asserted lower bound is zero and follows from nonnegativity of harmonic measure. No positive-diameter theorem is needed for this case.
2. If 0 belongs to E, U as defined above does not exist. One may extend the obstacle-hitting notation by h(E) = 1 at an absorbing point. With that explicitly declared extension the bound is automatic, since its right side is at most 1/2. This convention is not a classical interior-point harmonic-measure assertion at a point of the obstacle.
3. Connectedness cannot be dropped. For E = {-1,1}, the diameter is 2. Exit from D at 0 has the uniform angular distribution, so these two boundary points have total harmonic measure zero, while arcsin(2/2)/pi = 1/2. This is a counterexample to the disconnected generalization, not to Problem 3.21.

## What was and was not verified

The complete 256-page Hayman–Lingham PDF was acquired; its problem/update page was inspected as a rendered image and its reference 270 was checked in extracted text. The complete five-page FRW article was available as author-posted web-extracted text, including its definitions, lemmas, and final theorem proof. That extraction has visibly damaged mathematical symbols. The AMS PDF request was blocked, so no FRW PDF-byte hash or page-image inspection is claimed. The source attribution and exact formula are additionally checked against the undamaged Hayman page and Solynin publisher abstract. The Gaier dependency was not independently retrieved.

The proof of the general estimate remains the published theorem, with the above dependency/access limits disclosed. The calculations in this packet check interpretation and sharpness, not the full continuum comparison. No experimental or finite-computation substitute for that theorem is claimed.

Recommended queue entry: **already_solved; 1/5 authored effort**. The single effort is a credited literature verification and scope audit. No five-approach exhaustion is claimed or needed after a full prior resolution is identified.
