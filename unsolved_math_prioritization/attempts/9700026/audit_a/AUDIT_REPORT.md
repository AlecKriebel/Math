# Independent audit of the city ODE counterexample

Problem 9700026 / AMR-096-0026, catalog rank 934. Audit date: 6 October 2026.

## Verdict and exact scope

ACCEPT the unchanged, pinned author proof as a counterexample to the literal 2007 Conjecture 32(a) and the corresponding imported catalog statement. There is no mathematical repair condition. For every finite collection of at least two distinct interior sites and every positive initial probability vector, the displayed ODE has uniformly positive weights when beta > 2 alpha. In particular the permitted choice alpha = 2, beta = 8 contradicts the alpha > 1 collapse alternative.

This is a correction to the literal source statement. It is not a resolution of the intended stochastic city model, a proof or disproof of collapse for beta < 2 alpha, a treatment of beta = 2 alpha, or a proof of convergence to a unique positive equilibrium. It is not a claim of novelty, human peer review, journal acceptance, or formal proof-assistant verification. This audit was performed separately from the author attempt and independently reconstructed its argument.

The precise accepted inputs are:

- Author archive: 11,844 bytes, SHA256 adc58ab6c2b52963f303582261ee603470dbf2728eee8b4546c04ba7cf9b201d.
- Author external manifest: 1,878 bytes, SHA256 1e2c8f73e3d7d0bb127773a089901d11d70f3f44445f08f128c399ee71c68fe9.
- PROOF.md: 5,736 bytes, SHA256 8b0922482116df0b6510b4d5a6c089c3478765d4fecf2c151fd04c50a6814767.
- All eight author members match their external manifest and their expanded copies under author/.

No author file was changed. The regularity proof below is an independent strengthening, not a patch needed to make the accepted counterexample valid.

## Primary source interpretation

The [2007 notes](https://www.stat.berkeley.edu/~aldous/Research/OP/cities-notes.pdf) permit all positive alpha and beta on page 2; page 7 adds no exponent normalization. Source-wide parameter and rescaling review found no contrary global convention. Page 40 fixes the cities and gives exactly the ODE analyzed here, including collapse for alpha > 1. Its time variable is already logarithmic relative to population time. General position concerns sites and starting weights and is undefined. The document labels itself preliminary. Page 8 separates stochastic conclusions from the ODE question.

The [2012 paper](https://arxiv.org/abs/1209.5120) restricts its model to alpha <= 1, permits new cities, and does not state Conjecture 32. Its qualitative deterministic-approximation remark is not the displayed fixed-city conjecture. Thus it cannot rescue or replace the literal 2007 hypothesis. The [author page](https://www.stat.berkeley.edu/~aldous/Research/OP/cities.html) links both documents. Targeted searches identified no later resolution; this establishes neither novelty nor current open status. The live [catalog page](https://www.unsolvedmath.com/problems/9700026) remained inaccessible through the web tool; identity rests on the privately verified complete corpus and primary PDF.

## Independent mathematical reconstruction

Write D = [0,1]^2, fix distinct x_i in its interior, and put q = alpha/beta. For a positive state z, city i wins precisely when

    |y-x_i| <= (z_i/z_j)^q |y-x_j| for every j.

The finite set of sites can be discarded when defining areas. Raising all influences to the same positive power leaves winners unchanged. Consequently the vector field depends only on q, with no time multiplier. For example (2,8) and (1/2,2) yield identical cells and identical right-hand sides. This is a useful consistency warning, but the acceptance rests on a direct persistence proof rather than assuming either conjectured branch.

### Continuity and existence

For each pair i != j, the equality set is the zero set of

    f(y) = |y-x_i|^2 - lambda |y-x_j|^2,
    lambda = (z_i/z_j)^(2q) > 0.

This polynomial cannot vanish identically: if its quadratic coefficient vanishes, lambda = 1, and its linear coefficient is nonzero because the sites differ. Its zero set is a line or circle and has planar measure zero. Outside all pairwise ties the winner is locally unchanged as positive weights vary. Bounded convergence of indicators therefore proves continuity of all cell areas A_i. They satisfy 0 <= A_i <= 1 and sum A_i = 1. This justifies Peano existence on the positive orthant.

For every resulting solution, s = sum z_i obeys s' = 1-s, so the probability simplex is invariant. Also z_i' >= -z_i, whence z_i(t) >= z_i(0) exp(-t). On a finite time interval the state remains in a compact subset of the positive simplex and the derivative is bounded. If a maximal endpoint T were finite, the trajectory would have a limit there in that subset, and local existence would extend it. Thus every such solution extends globally. This is already sufficient for the author's proof; it does not rely on uniqueness.

### Supplementary local Lipschitz and uniqueness proof

Local Lipschitz regularity can also be proved without a smooth-cell-topology assumption. Fix a pair of distinct sites a,b, let d = |a-b| > 0, and let

    f_lambda(y) = |y-a|^2 - lambda |y-b|^2.

On a compact set of positive weights, all relevant lambda lie in [m,M_1] with m > 0. Define H = max(1, |1-m|, |1-M_1|). Direct expansion gives

    |gradient f_lambda|^2 = 4[(1-lambda)f_lambda + lambda d^2].

If |f_lambda| <= epsilon and epsilon <= m d^2/(2H), then |gradient f_lambda|^2 >= 2m d^2. At least one coordinate derivative has absolute value at least gamma = sqrt(m)d.

For fixed second coordinate, f_lambda is a quadratic in the first coordinate. Where its first derivative has absolute value at least gamma there are at most two monotonicity intervals. On each interval the part with |f_lambda| <= epsilon has length at most 2 epsilon/gamma. Fubini bounds the area where the first derivative is large by 4 epsilon/gamma. Interchanging coordinates and covering the strip by these two sets yields

    area{y in D: |f_lambda(y)| <= epsilon} <= 8 epsilon/gamma.

If the pairwise dominance test changes between lambda and mu, then

    |f_lambda(y)| <= |lambda-mu| |y-b|^2 <= 2|lambda-mu|.

For sufficiently close lambda,mu the preceding strip estimate therefore bounds the symmetric-difference area by 16|lambda-mu|/gamma. Each full city cell is a finite intersection of such pairwise dominance sets; the symmetric difference of intersections is contained in the union of the pairwise symmetric differences. Finally z -> (z_i/z_j)^(2q) is smooth on the positive orthant. Hence every A_i, and A-z, is locally Lipschitz there.

Picard-Lindelof now gives uniqueness as well as local existence, and the preceding continuation argument gives a unique global positive classical solution for each positive initial state. This supplement addresses possible regularity objections at changing cell combinatorics or at equal weights. It does not establish convergence or uniqueness of an equilibrium.

### Geometric lower bound

Choose h_i > 0 so that x_i + [-h_i,h_i]^2 lies in D and |x_i-x_j| >= 2 sqrt(2) h_i for all j != i. Interiority and finiteness make this possible. For any positive probability vector consider the smaller square with halfwidth h_i z_i^q. Every y in it satisfies

    |y-x_i| <= sqrt(2) h_i z_i^q,
    |y-x_j| >= |x_i-x_j| - |y-x_i| >= sqrt(2) h_i.

Since z_j <= 1, we obtain |y-x_i| <= (z_i/z_j)^q |y-x_j|. Thus the small square lies in the i-th cell apart from irrelevant null sets. Its area is 4h_i^2 z_i^(2q). Therefore

    A_i(z) >= K_i z_i^p,  K_i = 4h_i^2 > 0,  p = 2alpha/beta.

This is a global inequality over the whole positive simplex. It is not based on a symmetric equilibrium, a simulated trajectory, or a conjectured attraction basin.

### Comparison in the displayed ODE time

When beta > 2alpha, 0 < p < 1. Positivity permits the change u_i = z_i^(1-p) along the solution. The chain rule gives

    u_i' >= (1-p)(K_i-u_i).

Multiplication by exp((1-p)t), integration, and the monotonicity of a positive power give

    z_i(t) >= [K_i + (z_i(0)^(1-p)-K_i) exp(-(1-p)t)]^(1/(1-p)).

The bracket is a convex combination of two positive numbers. Hence for all t >= 0,

    z_i(t) >= min(z_i(0), K_i^(1/(1-p))) > 0,
    liminf z_i(t) >= K_i^(1/(1-p)) > 0.

Every competing city remains bounded below; summing their bounds rules out any z_i tending to 1. No additional time change is present, so the estimate addresses exactly the trajectory quantified by the conjecture.

## Rational witness and robustness

The author instance has alpha = 2, beta = 8; sites (1/5,1/4), (3/4,1/3), (2/5,4/5); initial weights (1/6,1/3,1/2); and h_i = 1/16. Independent exact arithmetic gives squared pairwise distances 557/1800, 137/400, 49/144 and signed triangle determinant 343/1200. The triangle is noncollinear and scalene. All initial weights are distinct and positive.

The smallest distance to the square boundary is 1/5 > 1/16. The least squared site separation is 557/1800 > 8(1/16)^2. Thus all geometric inequalities are strict. We obtain p = 1/2, K_i = 1/64, and K_i^(1/(1-p)) = 1/4096. Each initial weight exceeds that threshold. For every i and every t >= 0,

    1/4096 <= z_i(t) <= 1 - 2/4096 = 2047/2048.

This is an all-time consequence of the analytic differential inequality. The exact checks only certify the constants and selected algebra.

The theorem holds for every finite number n >= 2 of distinct interior sites, every positive initial probability vector, and every alpha,beta with beta > 2alpha. Therefore the examples with alpha > 1 occupy an open set in the relative parameter, site, and probability-simplex topology. Usual generic-position exclusions cannot remove them. The same numerical bound is asserted only for the displayed witness (and inputs for which its exact hypotheses remain valid); arbitrary exponent perturbations can change the bound while preserving noncollapse.

## Provenance and artifact audit

All three complete corpus files were rehashed, parsed, and checked at exact ID 9700026. The canonical complete-record/report pair uses default json.dumps with sort_keys=True and UTF-8. Its 4,409 bytes hash to 7b18458d71482e2c4e1c62601be1824eba6ad6243c78135d90d1b75223e8e193, matching the catalog review hash. The statement hash also matches. The exact prior report is literature-only; it is not an earlier authored solution. Fresh connected GitHub searches found no matching commits or pull requests for either identifier. Those bounded searches are not an exhaustive novelty test.

Fresh PDF downloads returned HTTP 200 and matched the author pins byte for byte. Text was independently extracted. The 2007 parameter and rescaling contexts were checked across all pages; the key parameter, notation, stochastic-versus-ODE, and Conjecture 32 passages were inspected. The provided page 2 and page 40 renders were inspected, and page 40 was independently rendered from the freshly downloaded PDF. The later paper was read throughout and its page 2 render inspected.

The saved queue response contains an embedded content SHA c87c275c638939b8008fd58db80657491d14971e and an outer metadata SHA 03f0ef6adc2b8d550f8b2b370f63689d72757553. They differ and are not reconciled or represented as a verified complete Git blob hash. A fresh bounded connector read again identifies rank 934, ID 9700026 / AMR-096-0026, status queued, turns 0/5, and reports the latter metadata SHA. This verifies the observed row identity, not consistency of full-response provenance. No queue write occurred.

The frozen author archive, its eight members, and its external manifest match exactly. Normal, optimized, isolated, and isolated-optimized author and independently written checkers passed in original and relocated working directories. Source/corpus verification also passed in those modes. Mutations of the author archive, manifest, proof, certificate, checker, and complete corpus inputs were rejected. Detailed metadata-only receipts are included.

The independent checker adds 600 rational influence comparisons at different sample states, five scalar comparison identities, 27 gradient identities, 13 invalid-certificate controls, and two valid controls. The author checker independently replays its 216 influence comparisons, four comparison identities, 16 negative controls, and two positive controls. Neither finite tests nor hashes certify the analytic theorem. The argument above and the unchanged author proof supply that reasoning.

## Acceptance boundary

The exact author freeze is accepted without repair for the literal counterexample. The author's historical pending-review labels remain unchanged inside that immutable input; ACCEPTANCE.json supplies this audit's verdict. Do not promote the result to a claim that the intended or restricted stability problem is solved. No third-party text, source PDF, dataset record, raw queue content, or private coordination is part of this audit's safe deliverable. Only authored mathematics, checker code, public citations, and verification metadata are included. No GitHub write or public dissemination was performed during this audit.
