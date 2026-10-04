# Geometric Chapuy adaptations: five-turn scoped partials

**30006025 / OWR-14298589-010. Original problem unsolved; five substantive author turns completed. Independent full review pending.**

The exact target is Baptiste Louf's Question 4, OWR 41/2024, printed page 2405, in a contribution with Svante Janson. It concerns a geometric adaptation of Chapuy's bijection in the comparison between random metric maps and random hyperbolic surfaces. The source does not axiomatize “nice” or “geometric.” The imported addition about unified volume identities is the separate Question 6 and is not silently included here. Report year 2024 and actual publication 14 February 2025 are both retained.

Source: https://ems.press/journals/owr/articles/14298589

## Preserved results

1. **Fixed algebraic perimeter and equiangular closure.** For each cubic one-face map and any fixed positive algebraic perimeter, continuously sampled positive edge lengths almost surely cannot form the prescribed geodesic polygon with angles 2π/3. A nonzero analytic holonomy constraint is proved using Hermite–Lindemann at the equal-length point. Finite adaptive pairing choices do not remove the obstruction.
2. **Algebraic lengths versus algebraic angle cosines.** No positive-algebraic-side closed hyperbolic polygon with all angles in (0,2π) can have all angle cosines algebraic. The proof uses the unique maximal exponent in the holonomy trace and Lindemann–Weierstrass. A continuous fixed-algebraic-perimeter version excludes any countable algebraic-cosine palette almost surely. These are exact prescriptions, not all possible geometric limits.
3. **A classical positive lift, with an incompatible short-curve law.** Replacing the lengths by a regular polygon gives a smooth closed hyperbolic surface for each cubic one-face map. The underlying CFF correspondence and uniform-dessin construction are credited. Every resulting surface covers the triangle orbifold Δ(2,3,12g−6), so Philippe's credited systole formula gives systole greater than 1. The displayed Mirzakhani–Petri Poisson limit then gives a persistent count-law total-variation gap greater than 3/19 on the interval [1/2,1], for every input-map distribution. This excludes this particular replacement from the desired short-curve comparison.
4. **Angle-independent direct-realization obstruction.** A one-face piecewise geodesic graph in a smooth closed curvature−1 genus-g surface cuts it into an intrinsic hyperbolic disk. The credited disk isoperimetric inequality applies despite reentrant corners, and every edge counts twice in its boundary. Hence its perimeter is at least 4π√(g(g−1)). The source perimeter 12g is too small for g≥12. Any same-edge realization requires an asymptotic relative total-length increase at least π/3−1.
5. **Sparse adaptive repairs under the actual Dirichlet law.** For E=6g−3 and normalized source lengths X~Dirichlet(1^E), the sum of the k largest coordinates has exact mean (k/E)(1+H_E−H_k). Thus changing at most k edges by at most a factor C has success probability at most ((C−1)/δ_g)(k/E)(1+H_E−H_k), capped at 1, where δ_g=(π/3)√(1−1/g)−1. In particular bounded-factor repairs on o(g) edges fail with probability tending to 1, even with fully adaptive selection. An almost-sure repair without a fixed cap must instead pay the stated expected-stretch lower bound.

## What is still missing

There is no construction with the controlled random-surface behavior sought by the source, and no proof that all geometric adaptations are impossible. Length-changing constructions, different correspondences and weaker asymptotic comparisons remain open. A Gromov–Hausdorff comparison does not by itself control the sum of embedded edge arclengths. The necessary bounds are not sufficiency criteria. The ordinary ribbon-graph/Riemann-surface homeomorphism and known CFF–Dirichlet metric-map sampler are established background, not new solutions.

There is no historical novelty claim for either the primary inputs or the scoped deductions. The work preserves its source-specific hypotheses and exact proofs so the deductions can be checked without inflating the original problem's disposition.

## Verification and file scope

All five exact checker receipts replay byte-for-byte, totaling **15,618 assertions**. Turn 1 requires SymPy; turns 2–5 use Python's standard library. These are supplementary exact controls. The analytic zero-set argument, transcendence theorems, triangle-group classification, Poisson limit and disk inequality are proved or credited explicitly in the text; finite computation is not substituted for them.

`FINAL_AUTHOR_MANIFEST.json` binds the complete public packet. Every historical turn manifest and file is preserved. Source PDFs, extracted texts, screenshots, raw imports and retrieval logs remain local-only; public files supply primary links and source hashes. `PUBLIC_SCOPE.json` is the original turn-1 scope; `FINAL_PUBLIC_SCOPE.json` is the complete final list. No sixth author search is included or planned for this attempt.
