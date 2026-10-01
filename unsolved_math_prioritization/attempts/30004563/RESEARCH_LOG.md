# Cube-move central points: recovery log

## 2026-10-01 03:59 UTC — source restoration (not a research turn)

Target 30004563 / OWR-2654831-006 is the all-alpha>1 upper bound of three potential cube-move central points, with crossing edges permitted and both alternating boundary triples noncollinear. Read the complete primary source setting in Melotti–Ramassamy–Thévenin, arXiv:2003.08941v2, Definitions2.1–2.7, Remark2.8, Theorem4.7, and Remark4.8. Retrieved the official OWR35/2020 report and checked printed p.1785. Both sources state the upper bound as an expectation, not a theorem.

The historical local-only work is unavailable. Its reported partial results were a general scalar-radius reduction, a reflection-symmetric equal-level three-root bound, and an exact alpha=4 six-boundary-point example attaining three. The historical number of author turns is unknown and is not recorded as zero. Current recovery instructions authorize five documented substantive recovered turns unless the exact full target is resolved earlier. Source retrieval alone consumes none.

## Recovered turn 1 — 2026-10-01 04:04 UTC (20% toward full target)

Reconstructed the exact scalar reduction for arbitrary noncollinear foci and arbitrary levels, and proved its endpoint signs: G(s_min)>=0 and G(s)/s^(2/alpha)->-1. This gives existence and boundedness but not the required three-root bound. Showed how arbitrary common-focus intersection configurations lift to admissible six-point cube boundaries, so a numerical or symbolic counterexample cannot be dismissed as outside the graph construction merely because it began with level curves.

Reconstructed an exact alpha=4 six-point configuration with three distinct centers and a separate admissible incoming center. Its new centers are (5/3,0) and ((13+-sqrt(69))/6,0). The boundary points are rational and both alternating triples are noncollinear. See PARTIAL_RESULTS.md. This restores a sharp lower-bound example, not the full conjecture.

Remaining exact gap: prove that the scalar G has at most three zeros on its physical domain for every alpha>1 and every noncollinear focal triple, or construct four or more admissible centers. One recovered substantive turn used; historical count remains unknown.

## Recovered turn 2 — 2026-10-01 04:21 UTC (100% candidate resolution; review pending)

Attacked the original nonsymmetric all-alpha root bound rather than repeating a reflection-symmetric subcase. Reordered foci to make both additive levels positive, normalized the larger level to one, and searched the exact scalar model across noncollinear triangles and exponents. A fixed-seed first batch of 1,000 exploratory configurations contained a five-sign-change example. High-precision checks confirmed it; rounding the geometry and levels to rationals and setting alpha=16 preserved five changes.

Replaced all numerical sign evidence by exact rational interval arithmetic: eighth roots are bounded using integer square roots and explicitly checked eighth powers. Six rational radius cutpoints have signs +,-,+,-,+,-, giving five distinct geometric centers by an exact bijection between scalar roots and common-focus solutions. Three algebraic odd boundary vertices are uniquely defined by rational polynomial equations; all six vertices are distinct and all twenty boundary triples are noncollinear. An incoming center is independently certified by a second scalar sign interval. All three old and all three new alpha-quad equations follow from exact level identities. New and old centers avoid every boundary point and every line through a boundary pair.

The frozen candidate and its 6,987-check exact certificate were sent for separate adversarial review. This is a complete counterexample candidate to the proposed upper bound, not a claimed determination of the actual maximum. There have been two substantive recovered turns; historical count remains unknown. No publication has occurred.

## 2026-10-01 04:34 UTC — full independent review passed

Separate adversarial review returned PASS_COMPLETE_COUNTEREXAMPLE with no mandatory correction. The author certificate replayed byte-for-byte, and an independently authored implementation with different eighth-root arithmetic and fresh brackets passed 13,948 exact checks. It verified source scope, all boundary and center nondegeneracy, all six quad identities, and the directly certified incoming center. The full candidate remains unchanged. The conclusion is at least five centers in the crossing-allowed realization setting, with no maximality or historical-priority claim. Recovered author count remains 2/5, with earlier historical count unknown. A single scoped draft PR is the authorized publication checkpoint.
