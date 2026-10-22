# Independent adversarial review: 30005731

## Verdict and frozen inputs

**Accept the five-turn partial packet as a research checkpoint. The original problem remains unsolved, 5/5.** No blocking mathematical defect was found in the stated conditional and counterexample-to-a-proof-mechanism claims. This is not a proof of the OWR optimizer conjecture, a counterexample using an optimal confining strategy, a novelty certification, or human peer review.

Reviewed on 2026-10-01 by an independent worker not involved in the five author turns. The frozen manifest SHA-256 is `409e87bfbe04ab1c7c957ee62cca81d1fe599231e3dae2f2c096c039bb9babd2`. Its 23 entries all matched their hashes and byte counts. In particular:

- RESULT.md: `386a83f000232dd1e5c4fd54cb3811d81f0540c3d5d004438b3c33a78fabc2e9`
- TURN_4.md: `cb3848cea49b797118abfe07095c783aca361508134ef23f152bc31e3892a9c3`

All five author checkers were read and replayed successfully, returning 107, 102, 8,360, 158 and 366 exact assertions. The retained replay outputs are separate review artifacts. Their counts do not imply that the continuum geometry has been checked by finite tests.

## Source and target audit

The [OWR primary report](https://ems.press/content/serial-article-files/48173), printed pp.2955–2958, was read in full for this contribution; its p.2957 was also visually inspected. The broad class fixes the initial point, arc-length order, simplicity before the last endpoint and nondecreasing arrival. Constant-arrival arcs are explicitly allowed. The question concerns optimal members of that broad class, not bare feasibility. The text does not supply a complete objective/quantifier specification for this assertion. Its printed A1 uses vertical e2.

The [2025 full preprint](https://arxiv.org/abs/2508.05324), Definitions 2.4, 2.6 and 2.10, was checked in the actual text. Definition 2.10 assumes local convexity. Its p.24 condition (2.7), visually checked, uses horizontal e1. Equation (1.6) is a weighted burned-area-plus-barrier objective; (1.9) is a terminal ray-length objective. The packet correctly declines to identify these optimization problems, to turn the convex-class theorem into a proof of its own convexity hypothesis, or to erase the source's axis/initial-set differences.

Zizza's thesis Lemma 6.0.3 and Remark 6.0.4 were inspected. That is an external-boundary comparison in its stated setting. The remark explicitly distinguishes length-only convexification from a burned-area objective. Bressan–Chiri's [2020 preprint](https://arxiv.org/abs/2012.00799), Definitions 1.1–1.2, arrival trace, Figure 1 and Lemma 3.1 were inspected. The delay-wall warning is real; its Hausdorff continuity theorem off the barrier does not provide the signed quantitative suffix bound needed here. All four local PDF hashes match the source manifest. No third-party code was executed.

## Turns 1, 2, 3 and 5

The two radial examples use a polar-angle interval shorter than a full turn, with strictly increasing radius. Each radial segment is therefore unobstructed except at the target endpoint. Euclidean distance supplies the opposite bound on arrival, yielding exactly r−1 with the reachable-closure convention. Their pointwise speed ratios give the displayed construction slack by integration. Reparametrization by length changes none of these geometric claims.

For Turn 1, direct differentiation gives the asserted curvature factor and the opposite signs 7 and −3. Hence the example is not locally convex. It is explicitly only a finite prefix.

For Turn 2, the Euler expression has the sign of signed curvature. The compactly supported outward bump preserves strict radial monotonicity for sufficiently small positive size. Importantly, the derivative of *every* prefix margin is nonnegative for all those sizes, not only at size zero. This makes the active-budget case legitimate. Terminal length decreases because the endpoint bump term vanishes. The hypotheses do not encompass global winding curves, corners, arbitrary weighted objectives or unknown optimizer regularity.

Turn 3's first-contact lemma is valid with traces defined through approaching paths. If a path avoiding the old prefix first meets the removed suffix before the assumed arrival threshold, its first-contact point is a full-barrier trace point reached too early, contradicting monotone arrival. Compactness of the full wall supplies first contact; the strict time gap accommodates approximating paths. Equal-arrival plateaus do not invalidate this argument. This causal fact says nothing about a changed prefix's effect on a future suffix.

In the nonradial chart, differentiation in the moving frame gives z'=p e+J e-perp and z''=(q−alpha' J)e+(J_v+2 alpha' p)e-perp. Thus E=J*kappa with precisely the sign used by the author. Stable ray visibility and positive chart Jacobian are explicit hypotheses, not consequences established for arbitrary barriers. The suffix accounting is an exact identity. At saturation, a shortening Delta only tolerates arrival advance Delta/sigma.

For Turn 5, the bounded derivative and positive radial slope justify the Lipschitz extension and length parametrization. The two tangent phase subsequences and two secant phase subsequences have distinct limits. The nonzero-speed bounds prevent a zero derivative from evading the secant obstruction after reparametrization. The example meets feasibility, not optimality or confinement, and the packet makes that limitation explicit.

## Turn 4: thin-wall geodesic audit

I challenged the use of a filled circle to analyze a wall that is only an attached arc. The distinction is material. The written proof does account for the missing portions as follows.

For a target in the upper half-plane, a route which reaches the upper exterior without entering the auxiliary disk obeys the usual convex-obstacle tangent-and-boundary distance. A route crossing from the lower side into the upper half-plane to the right of A has length at least 3+|q−A|, regardless of intermediate detours. This bound follows from the Euclidean distance from the initial disk to its axis-crossing point and the remaining distance to q; minimizing over x>=4 gives x=4. Crossing the axis through the radial wall is forbidden. Routes entering the auxiliary disk from the upper side must first enter on its unblocked upper boundary beyond the terminal arc endpoint. Their preceding upper-exterior length is at least the exterior arrival at that endpoint. If they reached that entrance through the lower side, they belong to the preceding lower-route case. These alternatives exclude a hidden shortcut through the unfilled disk.

The certified lower-route gap is positive on the shadowed circle and on the involute. I independently differentiated |W(v)−A|²; its derivative is 2(B−v)(cos(v)−1), so its minimum in the relevant interval is indeed at v=B. The terminal gap is approximately 0.12045845, comfortably above the proved 0.1 bound. Also |W−C|²=1+(B−v)² establishes separation from the circular part and injectivity by strictly varying radius. The entire involute is above the radial segment. Its degeneracy in the auxiliary v derivative at the first endpoint is removed by length parametrization.

The incoming tangent reaches every involute point in the same exterior time U. Before reaching the endpoint its exterior time is less than U. Therefore it cannot meet the future involute first: all its points have exterior time U. This justifies appending the entire level-set plateau without changing earlier traces, rather than incorrectly treating the wall as transparent.

For the perturbation, the exact bump is C3 across the endpoints, has nonzero mass and the computed derivative-energy integral. The chosen epsilon keeps the full auxiliary oval strictly convex and inside the old disk. Both the initial and suffix tangent contacts are outside the modified interval (independently checked B−a≈1.40703671>1.39). Their old support lines remain supports with unique unchanged contacts. The relevant exterior shortest path consequently loses exactly the modified boundary-length saving Delta, with the incoming tangent segment unchanged. Lower-side and upper-terminal-entry routes remain worse by the proved strict bounds. This is the crucial geometric point: the use of the full oval is a lower-bound comparison coupled with an explicit route-classification argument for the actual thin wall.

The visible-prefix budget certificate really is continuous: the rational Taylor grid is combined with the proved 43/20 Lipschitz bound. The modified shadowed prefix loses at most the stated small multiple of epsilon in margin and stays admissible. On the unchanged involute, arrival is U−Delta while construction length is reduced by only Delta. At the old saturated endpoint the new budget is exactly −(sigma−1)Delta. Plateau admissibility checks the whole level set, so this negative endpoint margin is a genuine static/dynamic obstruction, not merely a bad choice of construction order.

The independently authored checker verifies 19 symbolic identities and the source hashes; high-precision constants are included only as diagnostics. The written continuous reasoning above and the author's rational certificate, not those decimal evaluations, support acceptance.

## Publication boundary and remaining gap

The public disposition should be **unsolved**, with five completed author turns. The retained partials are valid only within their explicit scopes. In particular, Turn 4 refutes a universal unchanged-suffix estimate; it does not refute automatic convexity of a globally optimal confining spiral. The problem still needs an exact global optimizer formulation and a global competitor/regularity argument controlling future arrivals, closing geometry and initial tangent.

Do not publish the unmanifested complete imported record, source PDFs, extracted full text, source images or local reading paths. The manifest-bound mathematical packet and these portable review files are the reviewed material. No author file was edited during this review, and no further proof-search turn was supplied.
