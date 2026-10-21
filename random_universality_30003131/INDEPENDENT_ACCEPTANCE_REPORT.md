# Independent audit: quadratic random-permutation universality

Date: 2026-10-21 UTC. Scope: Chen–Wang arXiv:2610.13530v1, Theorem 1.1, its complete Section 3 proof, and the invoked He–Kwan Lemma 2.2. No queue or GitHub changes are part of this audit.

## Verdict

**PASS: the stated quadratic-length theorem has a complete, independently checked mathematical proof.** No substantive gap was found in the dependency, adaptivity, uniformity, counting, coupling, or asymptotic estimates. This is an independent mathematical acceptance assessment, not a claim of journal acceptance or community consensus. The observed arXiv record lists version 1, submitted 9 October 2026, and supplies no journal-reference field. “Peer-reviewed/published resolution” is therefore not established by this inspection.

The theorem resolves the weaker quadratic-order question, specifically Alon's 1000k² problem. It does **not** resolve the sharp 1/4 threshold conjecture. Nor does it prove He–Kwan's stronger proposed fixed-pattern failure exponent 3/2.

## Exact scope of the original problem

Alon's original contribution, printed page 1218 of Oberwolfach Report 22/2016, defines universality of an iid continuous uniform sequence through simultaneous containment of every k-permutation. It states both the sharp asymptotic coefficient 1/4 conjecture and the weaker upper bound 1000k². These are distinct claims. An iid continuous sequence induces a uniform permutation because every strict ordering of its coordinates has equal probability. Consequently the random models match exactly; ties have probability zero.

Passing from a length-32k² theorem to length-1000k² is valid: the first 32k² coordinates of a longer uniform permutation induce a uniform shorter permutation, and occurrence of all patterns is preserved when coordinates are added. Thus no unproved monotonicity of a special coupling is needed.

Source: https://publications.mfo.de/bitstream/handle/mfo/3526/OWR_2016_22.pdf?isAllowed=y&sequence=1 (Alon contribution, printed p.1218). The original passage was independently inspected in the recovered report.

## Independent reconstruction and failure-mode checks

Write q for the target size in the following audit to avoid conflating target and host lengths. Define d=ceil(48 ln q), h=ceil(q/d), and use 2h disjoint column strips of width 3d inside a 2q by 8q independent fair-bit array. The following checks reconstruct the logical dependencies rather than relying on the manuscript's claim of correctness.

### 1. Reduction to an independent array

He–Kwan's coupling uses 4q iid uniform points per column and 2q equal value bands. Every permutation pattern in its occupancy array lifts to the rank permutation: choose an actual point witness for each selected occupied cell. Increasing column blocks enforce increasing positions, and distinct ordered value bands enforce the required relative values. If expressing this as an interval contraction, delete empty value bands first; no realized embedding uses them. The unreduced array need not literally be a contraction when empty bands occur. To verify stochastic domination by independent fair bits, fix one band and reveal occupancy of other bands by searching for their first witnesses. A complete transcript fixes at most 2q−1 distinct positive witnesses. At least 2q point variables remain viable for the unexamined band. Conditional on the complete transcript, each such variable is independently uniform on a residual set containing that band, giving hit probability at least 1/(2q). The no-hit probability is at most (1−1/(2q))^(2q)≤e^(−1)<1/2. Averaging over transcripts gives the same bound conditional on the occupancy vector. Sequential uniform-threshold coupling then dominates a product Bernoulli(1/2) vector; independent columns give the entire array. Divisibility is exact for host length 32q².

He–Kwan's displayed ordering-permutation convention may transpose the occupancy matrix relative to another common convention. This creates no mathematical defect: inversion preserves the uniform distribution and swaps the two coordinate orders. The coupling can equivalently be defined from the rank permutation directly. The target theorem is unaffected.

Source: https://arxiv.org/pdf/1911.12878v2, Lemma 2.2, PDF pages 5–6. The source is the publicly available version of the paper published in Bulletin of the London Mathematical Society 52 (2020), 515–529, DOI https://doi.org/10.1112/blms.12345.

### 2. Single-test probability and adaptivity

Fix a tuple of distinct labels of length l≤d and one shift/strip. Greedy left-to-right matching succeeds if any increasing-column embedding exists; choosing the earliest possible column cannot obstruct a later tuple entry. Exactly one bit is queried per column. Even when the row choice depends on previous outcomes, the next column is unexamined, so its queried bit is conditionally fair independently of the entire preceding query transcript. Padding after success with queries in any fixed row makes the total count exactly Bin(3d,1/2); success corresponds precisely to at least l successful queries. Padding does not change the failure event.

The mean is 3d/2. The threshold d is a multiplicative lower deviation of 1/3, so the elementary multiplicative Chernoff exponent is (3d/2)(1/3)²/2=d/12. Hence each test has failure probability at most exp(−d/12). No conditioning on failures of other overlapping tests is performed.

### 3. Independence is applied to deterministic supports only

A tuple test's complete badness event is measurable on (S+t) times its strip, where S is the fixed set of tuple labels. Its support is NOT the random greedy trace. Different strips have disjoint supports. Within one strip, overlap requires a nonzero shift difference in S−S. There are at most l(l−1) such differences, giving maximum degree at most d²−1. (Indeed l(l−1)≤d(d−1)≤d²−1.)

Every collection of q vertices in a graph of maximum degree d²−1 has an independent subset of size at least ceil(q/d²), by iteratively choosing a vertex and deleting its closed neighborhood. Call this number a. For each FIXED independent subset, all its badness events depend on disjoint independent bits, so their joint probability is at most exp(−da/12). Although the subset witnessing many failures is chosen after the array is seen, a union bound over all deterministic candidate subsets removes that selection bias. At most (2qh)^a subsets need be counted. Overlapping tests are never asserted independent.

### 4. Simultaneous control of every target, without an n! union bound

Control all ordered tuples of distinct labels of length at most d; there are at most d q^d. Require each tuple to have fewer than q bad shift/strip pairs. This is one target-independent event.

For an arbitrary full permutation, divide its value sequence into h successive tuples and try the tuples in order across strips, restarting an unfinished tuple from scratch at each new strip. If all q shifts fail to finish, every shift has at most h−1 successful strips among 2h strips, hence at least h+1 failed strips. Total failures are at least q(h+1).

For any fixed tuple occurrence, the failed pairs encountered across the searches are distinct shift/strip pairs. Their count is below q. Summing over the h tuple occurrences gives fewer than qh failures, a contradiction. Even were identical tuples allowed, summing separately over occurrences would be a valid upper bound; actual permutation tuples have disjoint label sets. Success across increasing strips gives strictly increasing columns. Adding the same row shift preserves all value comparisons. The selected entries therefore form the desired permutation pattern. This reasoning is deterministic on the common good event and applies simultaneously to every permutation; there is no omitted union bound over q! possibilities.

### 5. Parameters, floors, and an explicit large-size regime

All row indices are in {2,...,2q}. Strip allocation is valid because 6dh<6(q+d)≤8q once d≤q/3. Also h≤q/2 eventually, so 2qh≤q². Since d≥48 ln q, ln(2qh)≤2 ln q≤d/24. The final logarithmic failure bound is consequently

ln d + d ln q − da/24 ≤ ln d + d ln q − q/(24d).

This is negative of order q/ln q: the positive part is O((ln q)²), not O(q ln q).

For a completely explicit conservative choice, let x=ln q≥32. Then d≤49x, ln d≤x², and thus ln d+d ln q≤50x². Since e^x/x³ is increasing for x>3 and e^32≥117600·32³, we have 50x²≤q/(2352x). Also q/(24d)≥q/(1176x). The total bound is at most −q/(2352 ln q). The strip and h inequalities hold in this regime as well. Therefore c=1/2352 and q≥ceil(e^32) are valid conservative parameters obtained directly from the proof. These are audit-derived values, not constants optimized or supplied by the authors. Small q are not claimed by the theorem and need no separate repair.

## Optional concluding sketch

The manuscript also sketches an improvement to any fixed coefficient above 1 using one-hot columns and negative association. This stronger sketch is not required to settle the assigned quadratic-order problem. Its apparent dependence issue is handled correctly in principle: bad-test indicators are decreasing functions of disjoint deterministic coordinate sets, and negative association yields the product upper bound. Fresh columns still give success probability 1/R for greedy queries. Empty value bands should be deleted only when passing to the permutation matrix; any realized embedding uses nonempty bands and survives the deletion. No defect was identified in this sketch, but the acceptance conclusion above is deliberately based on the fully written 32q² theorem and does not require claiming a separately formalized improved-constant theorem.

## Reproducibility and source status

Full main manuscript PDF and HTML proof were inspected, as was the entire invoked coupling proof. Original Alon text was checked in the recovered primary report. Finite checks in check_audit.py verify the single-test binomial-tail bound for d=1,...,200 and the overlap-degree estimate for all 2036 nonempty support sets in [q], q=1,...,10; they also check the explicit asymptotic base inequality. CHECK_RESULTS.json records PASS. These checks supplement the analytic argument and are not presented as a formal proof-assistant certificate.

Primary new source: https://arxiv.org/abs/2610.13530v1 and https://arxiv.org/html/2610.13530v1 (Theorem 1.1, Sections 2–3; original-question distinction in Section 1). Authors: Yu Chen and Yiting Wang; submission 9 October 2026. The manuscript discloses a GPT-6 Pro proof origin and author verification. That disclosure is an attribution fact, neither a substitute for proof audit nor evidence of journal acceptance.

Source PDFs are retained privately for inspection, not included in any proposed public authored artifact. Hashes identify exactly what was inspected:

- Chen–Wang PDF, https://arxiv.org/pdf/2610.13530v1: 437824 bytes; SHA-256 bd49c03c0e1b874dc83f38b459198dea0d1b4937edf68442eb4f6e6de6d98909.
- He–Kwan PDF, https://arxiv.org/pdf/1911.12878v2: 274762 bytes; SHA-256 196a3d5691ebcdc7859329fc4dd07d7a5dbd5198425287a63d648fdbceab6f6a.

The exact dataset-record identity and queue adjudication are outside this independent proof audit and must be checked separately. A title alone is not used here to decide whether a database row means the quadratic-order question or the unresolved sharp threshold.
