# Complementary review of the two-point squared-kernel bound

Shared PASS3, 14 October 2026. Reviewed `pass3_concentration_audit/TWO_SHUFFLE_BOUND.md`, 9407 bytes, SHA-256 `86c292c667305a12943e5b7321171b3660770cb6ff0da228811d254201e07754`.

## Verdict

**Accepted.** For every n >= 1 the exact count satisfies `a_n <= S_(n+2)`. This improves the additive size shift of the three-point ordinary-square construction. It proves the same obstruction beta >= lambda and does not by itself provide a reciprocal-product inequality. The separately accepted symmetric four-point guard remains useful for that stronger structural purpose.

No unconditional 1324 weak limit, macroscopic-cell probability, critical-radius convergence claim, or strict beta > lambda claim follows from this result.

## Full proof review

The two raw domino flattenings and their reversed state orientation are correct. Same-parity staircase cells are in skew order, so each within-color increasing pair lies in one original cell. A forbidden cross-color 1324 would require alternating increasing pairs, which can only lie in the corresponding vertical or horizontal neighbor pair. The flattening does not change those comparisons. Anti-diagonal reflection of the horizontal flattening gives states (C,A), not (A,C).

The two color words, together with the induced patterns A and S(C), reconstruct the original permutation exactly. At least two greedy cells make both colors nonempty. Exactly one greedy cell is equivalent to the whole permutation avoiding 213, so the omitted part has precisely Cat_n elements. Thus the first inequality with a Catalan remainder is correct. Summing 2xy <= x^2+y^2 over the symmetric finite state-pair index set gives the ordinary square bound without any reversibility assumption.

For a nonempty upper state A and lower state S(C), let m=|C|. The proposed prefix `(m+2,m+1)` consists of a new upper minimum followed by a new lower maximum; old upper values increase by two. The new states are exactly `(1 direct-sum A, 1 skew-sum C)`.

A prepended minimum cannot take part in a 213 in the upper state, and a prepended maximum cannot take part in a 132 in the lower state. Both designated cell classes are therefore preserved. Any 1324 using the first new point must start there, with its remaining three points old upper entries forming 213. If the second new point starts the occurrence, the same contradiction applies. If it were the second occurrence point, its only possible predecessor is the larger first guard point, whereas the first entry of a 1324 must be smaller. Its position prevents it occupying either of the remaining roles. Hence the padded permutation avoids 1324.

The lower maximum is the second guard point. The new upper minimum before it and any old upper point after it form an increasing upper pair. The old upper state is nonempty, so this witness exists. It is exactly the forward maximality condition defining K, not merely a choice of a nongreedy divider.

Deleting the first two global points recovers the old shuffle. Deleting the fixed first singleton from each padded state recovers A and C, so images from different input state pairs cannot overlap. Squaring the within-pair injection is legitimate: both ordered shuffles use the same state transformation and land in the same target kernel multiplicity.

For a single-cell avoider A of size n >= 1, the analogous image has second state of size one and has the same verified witness. Distinct A give distinct target state pairs. These terms do not overlap any padded pair with nonempty C, whose second state has size at least two. This disjointness justifies adding the Catalan contribution inside the same coefficient S_(n+2), including n=1.

Finally, a fixed shift does not affect the finite upper exponential growth rate. Taking nth-root limsups proves beta >= lambda and excludes an open Hilbert–Schmidt radius margin beyond rho. It says nothing about convergence exactly at rho.

## Independent diagnostics and dependencies

The separate script `check_two_point_padding.py` verifies the exact state formulas, avoidance, greedy witness, inverse deletion, and distinct images for all 10831 unrestricted dominoes with nonempty colors through total size seven, and all 625 single-cell cases through size seven. It also verifies disjointness of their target state pairs. All checks pass; `TWO_POINT_PADDING_CHECKS.json` records them.

The independent two-collapse and reconstruction check in `check_domino_obstruction.py` already covers all 19204 avoiders through size eight. These computations check indexing and edge cases; acceptance rests on the all-size argument.

The canonical kernel definition and staircase geometry remain the previously accepted PASS2 inputs. This is a complementary review of a reviewer-authored lemma within the same shared PASS3, not an additional independent pass.
