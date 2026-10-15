# Five-turn result: planted unknown random trees

**Original status: UNSOLVED after five substantive author turns. Complete partial package, independent analytic review pending.** ID 30006395 / OWR-14299518-013. No sharp information-transition or novelty claim.

## Exact original scope

The target is strong statistical detection of an **unknown uniform labelled Cayley tree** on k vertices, uniformly embedded and forced into G(n,c/n), with fixed c>0. The detector knows the parameters, not the shape or embedding. The source distinguishes this mixture from a typical tree revealed beforehand. Its unknown-tree log² n bound is sufficient; an O(log n) detector is explicitly still asked for. We do not treat log² n as a proved sharp lower endpoint.

The original OWR contribution and formula pages were read and visually checked. Primary prior-work scopes and the absence of a prior exact campaign attempt are recorded in `SOURCE_GATE.md`. No full proof manuscript for its announced random-tree endpoints was located; those claims remain credited source statements rather than independently verified inputs to our new derivations.

## Proved author partials, pending independent review

### Turn 1: exact forest overlap and a high-c regime

A weighted Cayley/Prüfer count gives an exact finite-n expansion for E_P L², with all falling factorials retained. It proves TV indistinguishability for fixed c>e and k=o(sqrt(n)), no strong detection at k=O(sqrt(n)), and, together with the classical edge-count test, strong detection for k=omega(sqrt(n)). At c=e it gives the lower bound k=o(n^(4/9)), without a matching detector. Uniform near-e bounds are explicitly chi-square bounds only.

### Turn 2: a first constructive path criterion

An exact Cayley distance and path-prefix boundary law yields a genuine unknown-tree detector when k/log² n→infinity and

    (c+1)log(1+1/c)−1>log c.

Its criterion root lies strictly between 4/3 and 7/5. The proof includes all background edges and a null union bound. It does not claim k≥C log² n, O(log n), or polynomial running time.

### Turn 3: exact critical L² asymptotics

If lambda=k^(9/4)/n→a finite limit and theta=sqrt(k)log(c/e)→a finite constant, the second moment has an explicit convergent integral-series limit. A matching one-component lower bound makes n^(4/9) the sharp scale for L² convergence of the likelihood to one at c=e. It is **not established as an information threshold**. Nontrivial or divergent second moments alone do not imply nonvanishing total variation.

### Turn 4: actual likelihood and testing law at fixed c>e

For fixed c>e and k/sqrt(n)→a<infinity, the null likelihood tends to exp(sigma Z−sigma²/2), where sigma²=a²A(c) and

    A(c)=sum_(s≥2)c^(1−s)s^s/s!.

A fixed-tree diagram/Wick argument plus a uniform L² forest tail proves the distributional limit and uniform integrability. Consequently TV tends to 2Phi(sigma/2)−1, optimal sum of errors tends to 2Phi(−sigma/2), and the two laws are mutually contiguous. Fixed-degree graph polynomials approximate that high-c risk. The needed exponential forest tail fails at c=e; no critical-law transfer is made.

### Turn 5: richer finite-depth entropy detectors

A two-type finite-depth branching likelihood has exact recursions for likelihood, entropy and second moment. Exact Cayley selected-root extension counts justify O(log n) off-path neighborhoods of an actual planted tree; a multiplicative exact null-exploration formula avoids an invalid additive-coupling union bound. If its depth-d entropy D_d(c)>log c for some fixed d, strong detection follows for k/log² n→infinity.

An entirely rational finite certificate proves D_2(3/2)>log(3/2), while depth one fails there. If C_ent denotes the supremal mean degree admitted by these finite-depth criteria and C_poly the supremal mean degree admitting any polylogarithmic-size detector, then

    3/2 ≤ C_ent ≤ C_poly ≤ e.

Neither equality is established. The scalar auxiliary second moment changes behavior at e, but that does not prove an entropy transition or a global information transition there.

## Exact remaining gap

A full resolution still needs the actual threshold/boundary in the last display, a converse or stronger detector in the remaining interval, the optimal unknown-tree low-c size, and a critical testing law for growing supports. The source's sharp-looking log²-to-sqrt(n) shorthand cannot substitute for these missing statements. Our high-c results are mixture results and do not automatically imply revealed-template lower bounds.

All five substantive turns have been used. No further author proof-search turn is hidden as packaging or review. A separate reviewer must challenge every analytic bridge before any final partial PR; the queue must ultimately record **unsolved, 5/5**, not claimed_solved.

## Verification and credit

The five checkers separate finite exact controls from numerical diagnostics:

- Turn 1: 312,359 exact assertions; 972,471 ordered embedded-tree pairs
- Turn 2: 46,501 exact assertions; 18,248 labelled trees and 42,599 prefixes
- Turn 3: 19,221 exact assertions; separate 60-digit critical-limit diagnostics
- Turn 4: 91,293 exact assertions; separate 60-digit variance/TV diagnostics
- Turn 5: 8,285 exact assertions; Cayley/null exploration laws and rational entropy certificate

Finite tests do not prove asymptotic uniformity; the written arguments do that or mark the gap. A Turn 3 Fraction-initialization harness defect was caught and corrected before freezing; its successful receipt is preserved.

Cayley/Prüfer counting, likelihood ratios, second moments, centered graph-count diagrams, Hermite expansions, and the hairy-path idea are credited as classical or source-described mechanisms. No comprehensive priority claim is made. Per-turn manifests bind immutable inputs; the final manifest binds the final status files and complete package. Full source PDFs, page renders and imported records are not redistributed.
