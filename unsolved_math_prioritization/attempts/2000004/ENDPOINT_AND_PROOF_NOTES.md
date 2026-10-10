# Endpoint calculation and local proof clarifications

## Review status of this edition

This AI-assisted mathematical exposition and independent internal AI source/proof audit are unrefereed. Bounded acceptance here does not mean external human peer review, journal acceptance of these authored documents, or formal proof-assistant certification. The AKM result is prior published work; no novelty is claimed. Deep cited existence, finite-distortion, change-of-variables and topological dependencies remain external. No author was contacted.

## Status of this note

This is an authored source audit, not an assertion that the published theorem is false. It identifies a failed endpoint construction in the inspected versions, and records small local repairs sufficient for the source's strict-range lower-bound argument. It makes no novelty claim and does not independently reprove the external existence or finite-distortion results.

The controlling versions are arXiv:2309.08288v2, 25 PDF pages, and the ZAMP 75:2 publisher PDF, 21 pages. Both were inspected. The logarithmic formula and integrability claim agree in arXiv pages 10–11 and publisher page 9, in the final paragraph of the proof of Proposition 3.3 after equation (3.9). The publisher HTML reproduces them too. This is not an extraction-only discrepancy.

## Exact endpoint determinant

Fix 0<s<1 and consider 0<t=x_1<s on the central rectangle S'_1. Put L=log(1/t)>0 and A=|log s|^2/s^beta. The two components of the printed endpoint map are

f(t)=t^alpha/L, and h(t)x_2=A t^beta x_2/L^2.

The gradient is lower triangular, so its determinant does not involve h'(t)x_2. Direct differentiation gives

f'(t)=t^(alpha−1)(alpha L+1)/L^2,

J(t)=f'(t)h(t)=A t^(alpha+beta−1)(alpha L+1)/L^4.

Consequently

J(t)^(−q)=A^(−q) t^[q(1−alpha−beta)] L^(4q)/(alpha L+1)^q.

At the source's chosen alpha=beta=(p−1)/p and q=p/(p−2),

q(1−alpha−beta)=−1,

and, as t tends to zero,

J(t)^(−q) ~ A^(−q) alpha^(−q) t^(−1) L^(3q).

This is a two-sided asymptotic consequence of the exact determinant; the conclusion is not drawn merely from the source's upper bound. For example, for L>=1/alpha, alpha L <= alpha L+1 <= 2alpha L, giving explicit positive two-sided multiples of t^(−1)L^(3q).

The energy is integrated in reference coordinates, dx_1 dx_2. Its inverse-Jacobian contribution on (0,s) x (−s,s) is

2s integral_0^s J(t)^(−q) dt = +infinity,

because substitution u=log(1/t) reduces the divergent tail to a positive multiple of integral^infinity u^(3q) du. There is no missing polar factor: S'_1 is a rectangle. Changing to deformed coordinates cannot remove the divergence, because the inverse change-of-variables factor restores exactly the same integral. Subtracting the finite constant W(I) also cannot remove it.

The derivative terms at these parameters behave at worst like t^(−1)L^(−p) and t^(−1)L^(−2p), which are integrable since p>2. Thus the obstruction found here is specifically the determinant penalty, not the continuity or p-Sobolev regularity of the displayed map.

Within this printed logarithmic family, p-Sobolev integrability requires alpha and beta at least (p−1)/p (the log powers permit equality). Avoiding a worse-than-t^(−1) determinant exponent requires alpha+beta<=2(p−1)/p. Both conditions force equality in both parameters, and equality still has the divergent positive log power. Altering these parameters within the printed family does not repair the endpoint. No alternative endpoint construction is claimed here.

## What is and is not accepted

The endpoint q=p/(p−2) in two-dimensional Theorem 3.2 and Proposition 3.3 is recorded as a published claim with an unresolved proof defect in the displayed competitor. Neither a counterexample to the theorem nor impossibility of every alternative endpoint construction has been proved by this audit.

For 1<q<p/(p−2), the preceding power-law construction has strict integrability inequalities and no logarithmic endpoint step. Theorem 4.1 likewise requires 2<q<p/(p−2). The endpoint defect does not enter that strict-range construction or its lower-bound argument.

A bounded correction search on 10 October 2026 inspected the arXiv version listing, the publisher article/PDF and explicit title/identifier searches for a correction, erratum or endpoint discussion. No repair was located. This is a bounded negative finding, not a proof that no correction exists. The arXiv listing displayed v2 as the last revision; no author was contacted.

## Normalized energy and distortion

The source's finite-distortion estimate is naturally written with the unnormalized energy. From

E_s(y)=integral [|gradient y|^p+gamma J^(−q)−W(I)],

one has

integral J^(−q) <= gamma^(−1)[E_s(y)+W(I)|Omega_s|].

For a finite-energy Lipschitz map,

integral K_y^q <= ||gradient y||_infinity^(dq) integral J^(−q) < infinity,

where K_y=|gradient y|^d/J. The additive normalization term should not be silently dropped, but it is finite and does not affect the required integrability. Since q>d−1, the cited finite-distortion theorem supplies openness and discreteness on each nonconstant component. The prescribed traces (or J>0 almost everywhere) preclude a constant component. CN and the Lipschitz area formula exclude overlaps of positive measure, upgrading to global injectivity across the components. In particular, if two disjoint neighborhoods had a common image point, openness would make their image overlap contain an open set, contradicting the area formula and CN.

This application checks the hypotheses of the external theorem. Its deep proof is not reproduced here.

## Directional lower bounds without an invalid pointwise inference

At equation (3.14) and the end of the proof of Proposition 4.3, the source passes from | ||F||_op−1 | to | |F e_j|−1 |. That pointwise domination does not follow merely from |F e_j|<=||F||_op. For example, F=diag(1,1/2) has ||F||_op−1=0 but |F e_2|−1=−1/2.

The needed integrated estimate nevertheless follows directly from Proposition 2.2 with positive parts. On a reference line of length 2, put a=|partial_j y|, b=||gradient y||_op and D=integral_(−1)^1(a−1). The fixed endpoint data give D>=0. Pointwise,

(a−1)_+ <= (b−1)_+ <= |b−1|.

Hölder's inequality therefore gives

D^p <= (integral_(−1)^1(a−1)_+)^p <= 2^(p−1) integral_(−1)^1 |b−1|^p.

Hence the line-integrated energy is at least c 2^(1−p) D^p. This is exactly the quantity needed for the line-length obstruction in d=2 and the slice excesses in d=3. The coefficient 2^(1−p) is the correctly normalized Hölder/Jensen coefficient; positive constants may be renamed afterward. No coercivity against the negative directional strain is needed.

For the two-dimensional detour, the line length is at least 2 sqrt(2)(1−s), so D>=2 sqrt(2)(1−s)−2, which is uniformly positive for all sufficiently small s. Integrating over a set of total transverse measure 2s yields the required positive multiple of s. This also avoids treating an unnormalized integral over a length-2 interval as a mean.

In three dimensions, integrate the same bound in x_1 and then over the good transverse slices. If one slice integral ∫D(x_1)^p dx_1 exceeds epsilon, its energy is at least c 2^(1−p) epsilon. The good-slice measure is at least (18/10)s, giving the required m s bound.

## Other small-range and sign clarifications

- The explicit regular competitors in Proposition 3.4 and Lemma 4.4 use (1+s)/(1−2s). They should be used on a fixed sufficiently small range, such as 0<s<=1/4, where that factor is uniformly bounded. They do not establish the literal all-s formulation of Lemma 4.4 by that formula at s=1/2. Only small s is required by the gap theorems. In three dimensions the competitor keeps x_1 fixed and shifts the second component in x_2; it is triangular with determinant one, satisfies the end-face traces, and avoids overlap for small s.
- In Lemma 4.5 the proof uses gamma=1−2/p<1/2, which is valid throughout Theorem 4.1's range 3<p<4. For small epsilon, the terms epsilon^[1/(2(p+1))] and epsilon^[1/(p+1)] are then bounded by constants times epsilon^[gamma/(p+1)]. The argument does not justify dropping the restriction p<4.
- The curve-length step in Lemma 4.5 is consistent: for a path of length at most 2+delta with endpoints two units apart, a point whose axial projection is inside the endpoint segment has transverse distance at most sqrt(delta+delta^2/4). If the axial projection is outside the segment, the distance to the farther endpoint is at least 2, so the distance to the nearer endpoint is at most delta. Both cases give the stated square-root scale.
- In the last face inequality for the Poincaré–Miranda argument, the valid estimate is g_3(x_1,tau_1,1)>=1+sigma−1/3>0 for |sigma|<1/3. That gives the required sign regardless of the printed stronger expression. The other five face signs follow from the same 1/3 closeness and prescribed end data.

These local clarifications preserve the source's strict-range architecture. They do not establish a connected-domain extension, a homeomorphism-class result, or the disputed two-dimensional endpoint.

## References and exact locations

- arXiv v2: https://arxiv.org/pdf/2309.08288v2 ; Proposition 3.3 endpoint, PDF pp.10–11; normalized-distortion step, p.12; (3.14), pp.13–14; Lemmas 4.4–4.5, pp.17–20; Proposition 4.3, pp.20–22.
- ZAMP publisher PDF: https://link.springer.com/content/pdf/10.1007/s00033-023-02132-4.pdf ; endpoint, p.9; normalized-distortion step, p.10; (3.14), pp.11–12; Lemmas 4.4–4.5 and Proposition 4.3, pp.14–19.
- Publisher HTML: https://link.springer.com/article/10.1007/s00033-023-02132-4 ; proof of Proposition 3.3 immediately after (3.9), and the corresponding numbered propositions/lemmas.
