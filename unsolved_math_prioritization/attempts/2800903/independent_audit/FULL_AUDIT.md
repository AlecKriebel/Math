# Independent audit: Gaussian data-point k-median LP partial results

Problem 2800903 / AMR-027-0903; queue rank 989. Review date: 2026-10-07 UTC.

## Verdict

**Accept all five mathematical routes as scoped partial results. The original random-model question remains unresolved.** No change to the mathematical proofs in `RESULT.md` is required. The planar certificate proves a strict LP/IP gap, the fixed-six-point theorem proves a positive dimension-only failure liminf, and neither the replication argument nor the concentration estimate settles a joint growing-sample/dimension exact-tightness probability.

**A verifier correction is required for optimization-safe verification.** The frozen `check()` consists of `assert b`, which Python removes under `-O` and `-OO`. Corrupt certificates then finish successfully and can still report 118,649 assertions. `VERIFY_HARDENING.patch` replaces this with an explicit conditional exception; `verify_hardened.py` contains exactly that change. Its valid output is byte-identical to the original saved `verification.json` in normal, `-O`, and `-OO` execution, and all ten negative controls are rejected in all three modes.

A small source-description correction is also supplied: the inspected Ahn–Cooper–Cornuéjols–Frieze abstract says Euclidean, without identifying a planar dimension. `SOURCE_SCOPE.patch` changes that unsupported qualifier to “Euclidean.” No theorem here depends on this reference. This is a limit of the inspected evidence, not a claim that the full paper lacks a planar model.

This is an independent AI mathematical and computational audit, not human peer review, a novelty determination, or a complete literature survey.

## 1. Frozen object and reproducibility

The reviewed `FROZEN_MANIFEST.json` has SHA-256:

`58932d752e971ec0789b637ceab3ae3f0246927befb6bece2dcb1188ae034100`

Its eight listed files all match both byte counts and SHA-256 digests. The original manifest and original files were preserved. Every execution of the author verifier occurred on a temporary copy; its output was never allowed to overwrite the frozen `verification.json`.

The audit deliverables contain authored analysis, public bibliographic metadata, and source-free certificate code. They contain no source PDFs, copied source passages, external datasets, or private coordination records. The five available archived source files match all five hashes and byte counts recorded in the author source manifest. Hash matching verifies the archived bytes; it does not retroactively authenticate every historical retrieval or visual-inspection event claimed by that manifest.

`replay_audit.py` independently reconstructs the finite geometry, symbolic radical costs, higher-precision rational enclosures, Gaussian covariance from Gaussian polynomial moments, line-rounding controls on different denominator grids, and duplicated-label configurations. It also reruns the original and hardened verifiers, and makes ten adversarial mutations to each. Its own checks use explicit exceptions, not Python assertions. `AUDIT_CHECKS.json` records the results and limits.

## 2. Problem identification and model equivalence

The objective and constraints match the data-point, unsquared-distance LP displayed in [Bandeira's Open Problem 9.3](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-of-data-science-fall-2015/29dc319cb9f8992c5b4b46b917ecd86d_MIT18_S096F15_Open9.3.pdf). Both clients and admissible centers are sample points. Its integral solutions are medoid solutions. The stray k-means terminology next to that LP is inconsistent with its unsquared objective; the packet correctly does not substitute the k-means SDP or continuous geometric-median problem.

The [Mixon/Ward Problem 6](https://dustingmixon.wordpress.com/2015/08/25/applied-harmonic-analysis-and-sparse-approximation/) supplies the unit-Frobenius-sphere distribution and asks about increasing dimension and sample size. It does not specify their relative growth or the behavior of k. The packet correctly distinguishes these possible limits. Calling the question unresolved is appropriately conservative; the source does not warrant inventing a prescribed joint regime.

For a standard Gaussian matrix G, its vectorization has a radial Gaussian density, so G/||G||_F has the uniform spherical law. The denominator is positive almost surely. Every feasible cost scales by the same positive scalar, so both optima scale and the exact-tightness event is unchanged. This is an equivalence of tightness events, not independence of the normalized columns.

The upper-bound comparison with source LPs is correct. Capping each opening at one preserves x <= y because assignment columns imply x <= 1. The capped sum is at most k. The remaining capacities sum to n minus that capped sum, at least the deficit to k, so opening mass can be restored without affecting x or its objective. Only equality of optimal values is inferred. The packet correctly avoids transferring uniqueness claims.

Tightness L = I means existence of an integral optimum. It does not mean every optimal solution is integral, and solver output alone cannot certify a strict gap. The finite proofs use a feasible fractional witness below every integral solution.

## 3. Six-point planar certificate and robustness

The six coordinates independently reproduce every entry of matrix (3). The specified opening vector is in [0,1]^6 and sums to two. Each assignment column has two entries of one half, both under an open half-facility, and sums to one. Its symbolic cost reduces to exactly the radical expression (5). Its diagonal assignment mass is two; its off-diagonal mass is four.

All fifteen facility pairs were re-enumerated. Nearest-facility selection can be performed on squared distances because the square root is increasing. Independent interval sums reproduce all fifteen printed lower numerators. The upper bound for {1,2} is below every other pair's lower bound, proving it is the unique optimal center pair, without needing to assert uniqueness of assignments when distance ties occur. Its radical expression is (6).

For each integer radicand m, the floor integer a = floor(sqrt(m) 10^6) satisfies a^2 <= 10^12 m < (a+1)^2. The resulting nonnegative rational brackets justify every displayed enclosure. Subtraction gives the exact lower bound

I - F >= 232103/400000 = 0.5802575 > 29/50.

Thus L <= F < I. It is unnecessary to determine the exact fractional optimum. The independent higher-precision brackets are recorded in `AUDIT_CHECKS.json`.

The perturbation proof is valid in any Euclidean dimension: moving each point by at most epsilon changes every pair distance by at most 2 epsilon. Each feasible assignment has mass n, so its cost changes by at most 2n epsilon. A finite minimum of integral costs has the same bound. Comparing the perturbed integral minimum with the fixed perturbed witness therefore loses at most 4n epsilon. At epsilon = 1/100 and n = 6 the strict lower margin exceeds 17/50. A product of six positive neighborhood probabilities is positive, giving the stated finite-size failure event. Its mass need not be uniform in dimension.

## 4. Line-metric rounding

The written rounding proof is complete and does not depend on finite-grid tests. Facility intervals partition [0,k), have length at most one, and contain exactly one of the k shifted lattice points in aggregate. Half-open endpoint conventions eliminate double ownership; each facility receives at most one selected phase point. Exactly k distinct facility labels therefore open. Zero openings, unit openings, and coincident facility locations cause no problem.

A consecutive block is a single interval in cumulative-opening space. If its length ell is below one, its projection modulo one has measure ell; if ell is at least one, every shifted integer lattice meets it. The miss probability is exactly (1-ell)_+. For a line client, every closed metric ball contains a consecutive block, including all labels tied at a boundary location. With k >= 1, a closest opened facility exists.

The assignment mass inside that block is at most its opening mass and at most one. Thus fractional mass outside is at least (1-y(B))_+. Integrating tails gives the stated expected rounded-cost inequality. Summation and selection of a phase yield an integral solution no more expensive than the fractional optimum. The reverse inequality is relaxation containment. Nonnegative client weights and separate line clients preserve the argument.

[Hajiaghayi–Hu–Li–Li–Saha, Lemma 3.1](https://cse.buffalo.edu/~shil/papers/FTKM-SODA2014.pdf), independently inspected in the archived author PDF, states a more general fault-tolerant line-LP optimal-integrality result. The credit is appropriate. An integral optimum for line costs is not integrality of the whole general k-median feasible polytope.

## 5. Fixed-six-point Gaussian-distance limit

For each coordinate index t, the six centered squares and fifteen pairwise products are centered and independent across t. Their covariance is diagonal: centered-square variances are two, product variances are one, and cross terms vanish by independence and odd Gaussian moments. Finite second moments suffice for the fixed 21-dimensional multivariate CLT. A diagonal covariance makes the limiting Gaussian coordinates independent; independence at finite d between all these summands is not being assumed.

For each of the fifteen pairs, the squared-distance fluctuation divided by sqrt(d) converges to V_i + V_j - 2 W_ij. The law of large numbers gives D_ij/sqrt(d) -> sqrt(2) in probability. Dividing by (D_ij + sqrt(2d))/sqrt(d) yields precisely the denominator 2 sqrt(2) in (9). The number of pairs is fixed, so this application of Slutsky is joint and valid.

Independent polynomial-moment calculations reproduce covariance one on the diagonal, one quarter for shared endpoints, and zero for disjoint edges. An additional exact structural certificate is

Cov(Z) = (1/2) Id_15 + (1/4) B B^T,

where B is the unsigned edge-vertex incidence matrix of K6. This covariance is bounded below by (1/2) Id_15, hence is positive definite. Since B^T B = 4 Id_6 + J_6, its eigenvalues are 3 once, 3/2 five times, and 1/2 nine times. The limiting Gaussian therefore has a strictly positive density throughout R^15.

For each two-center set the noncenter-client cost is 4-Lipschitz in the maximum norm. Taking a minimum preserves that constant. The fixed witness also has off-diagonal mass four and is 4-Lipschitz. Their difference Psi is consequently 8-Lipschitz. In the definition of Psi, negative entries are permitted as algebraic centered costs; no claim is made that these arrays themselves are metrics.

Scaling C by 1/10 and subtracting one off-diagonal subtracts four from each cost term. Hence Psi(H*) = (I-F)/10 > 29/500. The open box of radius 1/1000 leaves a margin greater than 1/20. Its limiting Gaussian probability q is strictly positive by full support.

For actual distance arrays, each integral center serves itself at zero cost, leaving exactly four noncenter clients, and the fixed witness has off-diagonal mass four. Subtracting sqrt(2d) therefore cancels exactly in their difference. Psi(H^(d)) > 0 implies LP failure. Portmanteau for the fixed open box proves liminf p_(d,6,2) >= q > 0. No moving-dimensional CLT, rate, or positive uniform-in-n probability has been smuggled into the argument. Normalization transfers the event to the spherical matrix model.

## 6. Concentration and value ratio

The deterministic inequality is correct: diagonal assignment mass is at most total opening k, so off-diagonal mass is at least n-k. This gives L >= a(n-k), while any k facilities provide an integral solution of cost at most b(n-k). For k < n and a > 0 the denominator is positive, permitting division. For k = n both costs vanish.

The chi-square moment-generating function and both optimized Chernoff exponents are correct. For 0 < epsilon < 1, the derivatives verify

epsilon - log(1+epsilon) >= epsilon^2/4,

-epsilon - log(1-epsilon) >= epsilon^2/2.

The two-tail bound 2 exp(-d epsilon^2/8), multiplied by n(n-1)/2 pairs, is exactly the exceptional term in (11). No independence of pair distances is needed. On the simultaneous distance event, the deterministic bound applies to every 1 <= k < n at once.

With d -> infinity, n >= 2, and log(n+1) = o(d), the proposed epsilon tends to zero and eventually lies in (0,1). The exponent 2 log n - sqrt(d log(n+1))/8 tends to minus infinity: its negative term dominates the positive term and diverges in magnitude. Thus the maximal ratio tends to one in probability, including fixed n >= 2. The trivial n = 1 case has no k < n ratio to maximize and can simply be omitted.

This is compatible with a positive probability of a strict additive gap when n = 6: the common leading distance scale grows as sqrt(d). Approximate value equality has no implication of exact equality. The packet respects this distinction throughout.

## 7. Replication

For r copies of every base point, choosing centers at two distinct base locations gives exactly r times the corresponding six-point objective. Choosing two labels at the same base location gives a one-location cost, which is at least rI since another distinct location could be added without increasing cost. Selecting labels at base sites 1 and 2 attains rI, proving the duplicated integral optimum.

Using one representative for each of the four half-open base sites is feasible: k-median has no aggregate facility-capacity constraint across clients. Every copied client retains its two half-assignments, yielding cost rF. The same 4n epsilon perturbation argument with n = 6r leaves a gap greater than 17r/50 at epsilon = 1/100, including perturbations with distinct coordinates.

A full-support probability measure assigns positive mass to every indicated open ball. Independence makes the prescribed ordered-label event have probability product_i mu(B_i)^r > 0. Gaussian samples are distinct almost surely. For these disjoint neighborhoods, the product decays exponentially in r and also depends on dimension. The theorem establishes finite positive probability at sample sizes divisible by six, not all sample sizes and not a nonvanishing growing-n probability. It remains an event under one Gaussian law rather than a change to a planted mixture.

## 8. Primary-source correction and evidence limits

[Del Pia–Ma, arXiv v2](https://arxiv.org/abs/2109.02547v2) was checked against the archived PDF, especially its model definitions, Definition 4, Theorems 6–8, and Appendix B Example 2. The article's use of tightness in its abstract must be read alongside its stronger planted exact-recovery definition. Example 2 establishes that the planted medoid assignment is not LP-optimal with high probability. It does not by itself eliminate every nonplanted integral optimum. The packet correctly declines to infer a global LP/IP gap from that result.

The reported seven-ball, two-dimensional, separation-2.2 counterexample and regularity description match the example. The sufficient-condition synopsis matches the theorem hypotheses: unit radii, equal counts and expected radii for Theorems 6–7, the stated invariance/absolute-continuity/positive-center-mass assumptions, and strict radial density decrease in Theorem 8. The square-root dimension dependence was visually checked. High probability is in the sample count per ball. These theorems provide no unplanted single-Gaussian exact-tightness theorem.

The version and acceptance status match arXiv. The final publication coordinates, Mathematical Programming 200 (2023), 357–423, were independently confirmed on [Alberto Del Pia's author research page](https://sites.google.com/site/albertodelpia/research). The DOI endpoint could not be reopened in this audit, so this review does not claim to have repeated the author's publisher-page inspection.

[Awasthi et al., arXiv v5](https://arxiv.org/abs/1408.4045v5) was checked for its historical clustering LP and disjoint-ball recovery claim. Its use in the packet is historical; none of the five proofs depends on the disputed theorem. The distinction between refuting planted recovery and refuting bare optimal-value integrality should continue to be preserved when describing the later correction.

The [Ahn et al. publisher abstract](https://doi.org/10.1287/moor.13.1.1) supports a near-optimal-value Euclidean analysis, not exact-tightness conclusions. This audit did not inspect the full paper. The separate source-scope patch removes the unjustified planar qualifier from the abstract-only summary. Bounded searches did not establish a directly applicable resolution of the original unspecified regime; this is not evidence of literature completeness or novelty.

## 9. Executable verification and failure controls

Python used: 3.12.14. The original and hardened scripts each reproduce the exact frozen JSON in all three interpreter modes. In the original optimized runs the predicates are evaluated as arguments to check(), but the only rejection mechanism is stripped out. Incrementing a counter and printing the same result is therefore not proof that any predicate was enforced.

The ten deliberate corruptions are: an explicit false check; zero total opening; incorrect assignment column mass; assignment to an unopened facility; invalid radical lower enclosures; a false six-point gap threshold; a false replicated-gap threshold; a negative covariance diagonal; four repeated rounding phases; and an incorrect off-diagonal-mass identity.

Results:

- Original, normal Python: 10/10 mutations rejected with an assertion failure before writing a report.
- Original, `-O` and `-OO`: all 20 mutated executions falsely succeed and write reports.
- Hardened, normal/`-O`/`-OO`: all 30 mutated executions reject before writing a report.
- Valid baseline: all six executions reproduce the frozen report byte for byte, retaining 118,649 enforced checks for the hardened version.
- Independent replay: 30,090 explicit checks, including 834 line-opening vectors and 5,838 line-client comparisons on denominators 3, 5 and 7; 3,810 additional replicated center-pair comparisons; Gaussian polynomial-moment and covariance-spectrum controls; and all 960 assignments to the fifteen fixed center pairs.

Finite computation supplements the universal proofs; it does not prove their probabilistic limit theorems. The mutation suite demonstrates the identified rejection failure and its repair, not resistance to arbitrary malicious program rewrites.

## 10. Acceptance conditions

The mathematical content is accepted without proof amendments. The hardening patch is required before treating the verifier as reliable under optimized Python. The source-scope wording patch aligns the optional older-paper synopsis with inspected evidence. With those corrections supplied separately and the original freeze retained, the packet is acceptable as an independently audited **unresolved partial-results record with five substantive mathematical routes**.

No proof of the original general probability question, exact value of the fractional optimum, novelty, exhaustive bibliography, or human review is accepted or implied.
