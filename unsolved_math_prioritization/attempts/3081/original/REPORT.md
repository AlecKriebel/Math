# Monochromatic empty triangles: a bounded obstruction audit

Problem 3081 / OPG-2435. Checked 2026-10-06. **Unresolved; stopped after two substantive approaches.** No improved asymptotic bound or counterexample to the intended conjecture is claimed. The constructions below certify failures of specific proof shortcuts. Their novelty is not asserted.

## 1. Exact target and prior-work gate

For a finite planar set P with no three collinear and a map from P to {red, blue}, let E_s(P) count unordered triples whose vertices share a color and whose open triangle contains exactly s other points of P. Interior points of either color count. General position makes the open-interior and closed-convex-hull definitions of emptiness equivalent. The target is: there exist absolute constants c > 0 and N such that E_0(P) >= c n^2 for every n >= N and every such colored n-point set.

Both color classes may be arbitrary in size. This is vertex coloring, not edge coloring. Triangles may overlap; the target does not require disjointness. Dropping positivity of c makes the assertion vacuous. Requiring a positive bound for every small n is false, but that defect is already documented and does not refute the intended asymptotic conjecture.

The complete supplied exact-ID record was paired with the research-report lookup for OPG-2435 using the specified default json.dumps serialization. The report is absent, and the record's inherited work is literature-only triage. The match and full-file checks are recorded in CORPUS_GATE.json. Exact-ID/title connector searches returned no repository or PR matches; these bounded searches are not evidence of novelty. No inherited substantive attempt was found in the inspected sources. The live aggregator page returned HTTP 403; its complete corpus record and the actual Open Problem Garden page were inspected instead. This access limitation is not hidden by calling the live page verified.

## 2. Source alignment

[A] Aichholzer, Fabila-Monroy, Flores-Peñaloza, Hackl, Huemer, and Urrutia, *Empty Monochromatic Triangles*, CCCG 2008, pp. 75–78. The conference source states the quadratic conjecture and proves an n^(5/4) lower bound. It also explains a quadratic bound for two-colored Horton sets. The 2009 author manuscript was also inspected. https://cccg.ca/proceedings/2008/paper18.pdf

[B] Pach and Tóth, *Monochromatic empty triangles in two-colored point sets*, Discrete Applied Mathematics 161 (2013), 1259–1261; author version from 2008. The proved exponent is 4/3. https://doi.org/10.1016/j.dam.2011.08.026

[C] Bhattacharya, Das, Islam, Mohapatra, Paul, and Sen, *On the Number of Almost Empty Monochromatic Triangles*, arXiv:2601.18951v2, revised 2026-09-11. Theorems 1–2 and Remark 1 distinguish the quadratic result allowing one interior point from the 4/3 result requiring none. Remark 1 explicitly leaves the quadratic empty case open. https://arxiv.org/abs/2601.18951v2

[D] Bhattacharya, Das, Islam, Mohapatra, and Sen, *Almost Empty Monochromatic Triangles With Many Colors*, arXiv:2609.12325v2, revised 2026-09-21. Its results concern permitted interior-point thresholds for many colors and an existence result for Horton sets. The introduction still records 4/3 for the two-color empty counting problem; it supplies no quadratic solution. https://arxiv.org/abs/2609.12325v2

The PDFs were downloaded and their relevant statements and proofs inspected. Their byte counts, hashes, versions, and inspection scopes are in SOURCE_VERIFICATION.json. No third-party source text or PDF is included here. The literature conclusion is limited to the inspected sources and searches, not an exhaustive certification that no later or unindexed result exists.

## 3. Approach 1: star-fan counting and its missing surplus

The known discrepancy bound in [A, B] is E_0 >= r max(r-b-2,0)/3 when r >= b are the color sizes. Here is the counting mechanism. Around each red pivot, order the remaining red points by angle. Consecutive rays with angle below pi give at least r-2 red triangles, with disjoint interiors and no red point inside. At most b contain a blue point. Sum the surviving incidences over the r pivots, and divide by at most three incidences per triangle. In particular, a fixed positive fractional imbalance gives a quadratic bound. Balanced color sizes give no positive bound from this estimate.

Trying to sum such fans while charging each blue blocker only a constant number of times fails. This is a defect of that proposed charging rule, not of the discrepancy lemma.

### Proposition 1: unbounded reuse of one blocker

For every integer k >= 1, put r = 2k+1 red points at

    a_i = (2i, 2i^2),  -k <= i <= k,

and one blue point q = (0,1). For each red pivot, take the ordinary triangulation of the red convex polygon by its diagonals. Exactly one triangular face in each of these r fans contains q. Hence the single blue point blocks exactly r pivot-face incidences.

**Proof.** The parabola points are in strictly convex position: the supporting tangent at each point separates it from all the others. Three parabola points are not collinear. The line through a_i and a_j has equation y = (i+j)x - 2ij. It cannot contain q, since -2ij is even and q has y = 1. Thus the full set is in general position. The point q is strictly inside the triangle a_-1 a_0 a_1, hence inside the red polygon. Each pivot's diagonal fan partitions the polygon. Since q lies on no diagonal, it lies in exactly one face. Summing over all r pivots proves the claim.

This family has precisely k^2 red triangles containing q: each must include a_0, because every other red point has y >= 2, and its other vertices must have opposite x signs. Conversely, every triangle a_-i a_0 a_j, with 1 <= i,j <= k, contains q. All remaining red triangles are empty because all red points are extreme. Thus E_1 = k^2 and E_0 = binom(2k+1,3)-k^2. The latter is cubic, so this is emphatically not a counterexample to the quadratic conjecture. It only disproves the proposed uniform constant capacity per opposite-color blocker across pivot fans.

The exact missing ingredient in this route is a global lower bound on the total unblocked fan incidences (or another controlled family) of order n^2 in the near-balanced regime. The individual-pivot bound does not supply it, and Proposition 1 rules out one overly strong replacement for its blocking budget.

## 4. Approach 2: converting almost-empty triangles locally

A tempting use of [C] is to replace each monochromatic triangle containing one point by an empty monochromatic triangle using just its vertices and that point. If the interior point has the opposite color, all three triangles obtained by inserting it are bichromatic; the original monochromatic triangle remains nonempty.

The following balanced, integer-coordinate configuration makes this failure exhaustive. Points have indices 0 through 7 in the displayed order:

    0 (-3,14) red      1 (-2,-14) blue
    2 (1,1) blue       3 (-5,-4) red
    4 (-4,2) blue      5 (-8,-12) blue
    6 (-1,-5) red      7 (9,11) red

There are four points of each color. The full list of monochromatic triangles, followed by their sole interior point, is:

    (0,3,6): 4       (0,3,7): 4
    (0,6,7): 2       (3,6,7): 2
    (1,2,4): 6       (1,2,5): 6
    (1,4,5): 3       (2,4,5): 3

All eight listed interior points have the opposite color. The exact checker verifies all 56 orientation determinants are nonzero, every containment using two integer formulations, and that these are all eight monochromatic triples. Consequently E_0 = 0 and E_1 = 8. There is no empty monochromatic triangle even if a replacement rule may use any of these eight points.

This certifies failure of a universal local replacement rule; it is not a large-n counterexample. A successful use of the almost-empty theorem must coordinate different triangles, use further points, or obtain additional global structure. Simply deleting the blocker is invalid for the original problem: it makes a triangle empty only in the reduced set. Under independent retention with probability p, the exact expectation of the reduced set's empty monochromatic count is

    p^3 * sum_{s >= 0} (1-p)^s E_s(P).

This follows by retaining the three vertices and deleting all s interior points. A lower bound on this sum does not by itself isolate its E_0 term. The checker verifies the formula by exact enumeration of all 256 retained subsets of the eight-point witness at p = 1/2. The positive expectation there comes entirely from E_1, while E_0 is zero.

## 5. Stop decision and claim boundaries

Two substantive routes were investigated. Both stopped at a precise obstruction, so the five-approach ceiling was not filled artificially. The only general quantitative lower bound reproduced here is already known. No asymptotic advance, full solution, or asymptotic refutation has been obtained. Finite checks prove the finite certificates, not the conjecture. The all-k blocker claim has the separate proof above.

The certificate is author-generated, not extracted from a third-party dataset. The package has an exact, dependency-free checker, full-file metadata, relocation tests, normal/optimized-mode tests, and tamper rejection. A new independent mathematical and packaging audit is required before publication. No repository or queue changes were made in this task.
