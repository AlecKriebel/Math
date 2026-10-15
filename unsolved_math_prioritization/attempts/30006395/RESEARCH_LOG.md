# Research log

2026-10-01 08:02–08:06 UTC. Source-only gate: read instructions, full pinned record/embedded assessment, live campaign absence checks, exact OWR contribution and formula images. Restored unknown-versus-revealed Cayley-tree experiments and the fixed-c sparse model. Checked the relevant primary known-template/path/regular-tree theorem scopes and current targeted literature. No full transition theorem located; no claim of comprehensive search.

Important correction: the catalog's log²-to-sqrt(n) phrase is a research question, not a certified exact threshold curve. The source itself asks whether the unknown-tree upper bound can improve to O(log n). Statistical and computational detection are distinct.

Completion estimate: 5% toward original resolution. Author proof turns: zero. No new theorem claimed. First substantive work will be recorded as turn 1. No queue regeneration or external outreach.

## 2026-10-01 08:08–08:15 UTC: substantive author turn 1

Started only after the exact source gate and remote source checkpoint. Derived the likelihood of the unknown labelled-tree mixture, then used the classical weighted Prüfer count to sum all possible shared-edge forests exactly. Kept falling-factorial corrections explicit rather than assuming disjoint overlap components. A Gaussian bound in total overlap support permits componentwise exponential domination.

For fixed c>e, the component series converges and gives TV indistinguishability below sqrt(n), bounded-second-moment exclusion of strong detection at O(sqrt(n)), and the classical count test above sqrt(n). At c=e, Stirling plus Gaussian cutoff yields the lower bound n^(4/9), without a matching detector. Derived uniform near-e moment bounds and stated their limitations. No assertion that e is the true information threshold or that moment divergence implies detection.

The exact checker enumerated 3,270 fixed-label forests, 972,471 ordered embedded-tree pairs, and 1,232 small null graphs, comparing their moments to the formula. All 312,359 exact assertions pass. Scope is the unexposed mixture; the source's most-known-tree claims are stronger in information available and are not inferred.

Completion estimate: 25% toward the original transition problem. First-turn partial checkpoint is complete, but the original task continues. Further turns must attack typical/truncated likelihood or constructive detection rather than repackage this second-moment lower bound as full resolution. No independent final review or PR yet.

## 2026-10-01 08:16–08:25 UTC: substantive author turn 2

Pursued a constructive test instead of treating moment divergence as evidence of detectability. Reconstructed the exact distance law between two fixed labels of a Cayley tree and the exact strict-prefix boundary law by contracting its full connecting path in the weighted Prüfer distribution. This supplies a hidden length-K log n path with about one forced off-path neighbor per vertex when k/log²n→infinity. Added the independent background edges explicitly. A null union bound and binomial rate function prove strong detection when g(c)>0. Exact rational logarithm intervals certify c=4/3 and an explicit K=100, delta=1/100 test choice.

Also proved the edge-addition channel monotonicity in c, which brackets the supremal polylog-detectable mean degree between the criterion root c_h and e. The true transition remains unknown. The mechanism is the hairy-path idea already announced by the OWR authors; no novelty claim or polynomial-time algorithm is asserted, and the size condition is deliberately weaker than k≥C log²n.

The independent enumeration within the author checker covers 18,248 labelled trees and 42,599 actual path prefixes; all 46,501 exact assertions pass. Completion estimate: 40% toward original transition resolution. Second substantive turn complete; original task continues, no final PR or queue status.

## 2026-10-01 08:27–08:35 UTC: substantive author turn 3

Kept the full finite-population overlap factor and derived an exact coefficient recurrence for the likelihood second moment. Proved a two-parameter critical-window limit under k^(9/4)/n→lambda and sqrt(k)log(c/e)→theta. A multivariate Riemann-sum argument includes uniform control near zero, Gaussian tail domination and an exponential majorant over the number of forest components. Reduced the limiting integrals by the Dirichlet identity; at theta=0 a four-step Gamma-coefficient recurrence gives an entire positive series.

A one-component lower bound proves moment divergence above n^(4/9), so the scale is sharp for L² convergence to one at c=e. No claim of TV nonvanishing or a successful test follows. Bounded moments exclude strong detection in the finite critical window. The original mean-degree gap and actual information transition remain open.

The first checker run found a harness error: Python's empty integer sum at coefficient b1 produced float zero, contaminating later Fraction arithmetic. Initialized the empty sum as Fraction(0) and reran. The written recurrence was unchanged. All 19,221 exact assertions across 1,300 finite parameter cases then passed, with separately labeled 60-digit integral/convergence diagnostics. Slow finite-size numerical convergence is displayed rather than hidden and is not used as proof.

Completion estimate: 45% toward the original question. Third substantive turn complete; next work needs higher-moment/truncated-likelihood control or a stronger constructive statistic. No final result, queue update or PR.

## 2026-10-01 08:37–08:50 UTC: substantive author turn 4

Tried to bridge likelihood moments to testing. Growing critical overlaps still require new control, but for fixed c>e a full route works: centered counts of each fixed connected tree have jointly Gaussian limits by explicit overlap-diagram power counting; disjoint forests converge to Wick polynomials. Proved an exponentially small, uniform-in-n L² tail after truncating total forest vertices, allowing the whole likelihood to converge to a lognormal law. Uniform integrability then gives the actual total-variation and optimal-error limit, and positivity of the limit yields reverse contiguity.

The variance series has a classical rooted-tree generating-function expression. Fixed-degree graph polynomials approximate the high-c risk to any prescribed accuracy. No claim extends this to the source's low-c running-time question. Explained exactly why the argument breaks at c=e: the component series has no exponential vertex tail, and fixed-tree coefficients vanish in the n^(4/9) window while growing supports carry its moment.

All 91,293 exact controls pass, including actual centered-edge polynomial identities, error norms and diagram equality cases. Separate 60-digit variance/TV diagnostics agree with the convergent series. Completion estimate: 50% toward the original transition, still unresolved after four turns. Final fifth turn must attack the remaining mean-degree/critical issue or state the exact obstruction honestly. No final review, PR or queue update.

## 2026-10-01 08:52–09:07 UTC: substantive author turn 5

Pursued richer local statistics and the critical obstruction. Derived exact likelihood/entropy/second-moment recursions for a finite-depth signal-plus-noise branching experiment. Rather than assume that local model describes logarithmically many path roots, derived the exact selected-root Cayley forest law via allowed-attachment weighted extensions and proved its uniform total-variation approximation on a high-probability path-distance range. Deleted the path endpoints to avoid continuation contamination. Added independent background neighborhoods with explicit planted-hit and collision errors.

For the null, an additive local coupling would fail under the path union bound, so derived an exact rooted exploration probability and a uniform multiplicative comparison on the size-capped rare event. This proves the original-model entropy detector when D_d(c)>log c. Exact rational lower bounds for ten depth-two terms give D_2(3/2)−log(3/2)>1/500; depth one fails there. All 8,285 exact checks of the Cayley/null forest formulas and rational certificate pass.

The auxiliary second-moment recursion changes at e, but no converse from it to entropy or graph detection was found. Final rigorous bracket is 3/2≤C_ent≤C_poly≤e. The actual boundary, optimal low-c size and critical TV law remain unproved. Completion estimate: 55% toward original resolution; this is a subjective research-progress estimate, not a solved-status assertion.

Five substantive turns consumed. Original final status: unsolved 5/5, independent analytic review pending. No further author proof search is authorized as packaging; preserve every scoped result and exact gap. No PR or shared queue mutation before the review and parent publication gate.
