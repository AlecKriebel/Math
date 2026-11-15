# Independent oracle and source audit: PR 570 / problem 30006605

Assessment: **the candidate reduction and its O(n log^5(2n)) exact-arithmetic conclusion are mathematically sound, with explicit repairs to the primary import's proof presentation recorded below**. No counterexample to the candidate was found. The two primary-source proof defects do not force a weaker target: a fully consistent integer balance threshold and an elementary depth estimate recover the imported O(n log^4 n) theorem used by the candidate. The public original candidate should cite or attach this correction when presenting its verification record. Historical priority remains outside this audit.

The exact original is the claimed-solved head `417ca52e83cf06b07c388d89c756cfd86473d5b0`, `unsolved_math_prioritization/attempts/30006605/bundle/PROOF.md`, SHA256 `b0b948da64c113dfff1349a2aae48389531c2a8bd719dcdd2ab9483a6fc37d76`. All 16 original-packet files match the parent snapshot's hashes, as independently recorded in INPUT_HASH_CHECKS.json. This audit read the candidate proof in full, but did not read its old audit, author controls, or sibling reviews. Its source-first checkpoint was physically saved at 2026-10-15 04:10:05 UTC, before the first candidate read at 04:10:08 UTC. A manual timestamp error in that original checkpoint is preserved and corrected in TIMESTAMP_CORRECTION.md.

## Exact target and imported interface

The full Ducoffe contribution in OWR 8/2026, printed pp. 504-507, was independently read before the candidate. Open Problem 1 concerns finding a vertex minimizing the multiplicative radius max_u w(u)d(x,u) in almost linear time on bounded-cube-dimension median graphs. The n-vertex computational interpretation is finite, explicit graph input; the opening general definition also permits infinite graphs, for which no computational encoding is specified. The candidate openly restricts its algorithmic theorem to the finite interpretation and handles arbitrary nonnegative real weights in an exact arithmetic/comparison model. Its all-zero profile convention is radius zero at every vertex. The adjacent arbitrary-edge-length and unimodality questions are separate targets.

The BDH original theorem accepts a finite connected simple median graph and nonnegative INTEGER arrival offsets a(u), and returns all E_a(x)=max_u(d(x,u)+a(u)) in O(n log^4 n). The exact weighting semantics, including d_a(u,u)=a(u), are on its pp. 2 and 6; Theorem 1 and the complete Algorithm 1 proof are in sections 3-4. These relevant sections and their preliminary dependencies were read completely, with equation-critical pages visually checked. Its separate distance oracle is unnecessary. The source's classical median structural lemmas and O(m) preprocessing routines remain imported published results; their historical proofs and a fast implementation are not formalized here.

The candidate's oracle calls meet EVERY actual interface promise. The underlying graph is unchanged and remains finite, connected and median; its edges are unit length. The input offsets a_R(u) lie in [0,n-1] and are integers, including zero. Neither fractional weights, negative offsets, an all-pairs distance matrix, a product embedding, a dimension promise, nor a multiplicative-weight oracle is smuggled into BDH.

## Independent derivation and adversarial checks

For D=n-1 and R>=0, let b_R(u) be the largest k in [0,D] with kw(u)<=R. This set contains zero. For every actual graph distance d in [0,D], nonnegative w makes dw(u)<=R equivalent to d<=b_R(u), including w(u)=0. Hence with a_R=D-b_R,

    r_w(x)<=R  iff  for every u, d(x,u)+a_R(u)<=D
                iff  E_{a_R}(x)<=D.

There is no rounding relaxation: integrality comes from distances, while the real profile is only used in exact comparisons. A binary search over k supplies b_R without a floor or division primitive. Keeping zero-profile graph vertices is essential and is done correctly. A negative R is infeasible, a singleton has radius zero, and an all-zero profile makes every vertex a center.

For optimization, each radius and therefore its minimum belongs to the implicit multiset of n rows [0*w(u),...,D*w(u)]. The saved incumbent is always feasible, and either it equals the optimum or an active entry still equals the optimum. A feasible pivot retains only entries strictly smaller than it after saving it; an infeasible pivot retains only entries strictly larger. These operations preserve that invariant even with equality ties and zero rows. An empty active set forces the incumbent to equal the optimum. Its witness and the final complete threshold-feasible set are exactly a center and the entire center set.

Weighting each row midpoint by its active row length is sufficient for progress. Each row contributes at least half its entries on either side of its own midpoint. A weighted median has at least half the total row mass in midpoint values on each weak side, so the selected feasible or infeasible pruning removes at least one quarter of the active entries. Duplicates strengthen rather than invalidate pruning. There are O(log n) iterations from n^2 entries, without materializing them. Sorting/pruning and threshold construction require O(n log n) work per iteration; BDH dominates with O(n log^4 n). The final bound is O(n log^5 n). Only O(n log^2 n) comparisons involving original real input weights are needed. Rational comparisons can be implemented by exact cross-products of O(B+log n)-bit operands. The theorem is an exact-arithmetic bound, not a bit bound independent of B.

The candidate does not implement the fast imported algorithm and says so. Its reduction is still a complete algorithmic proof using a published theorem, rather than an unsupported equivalent reformulation: the full additive algorithm accepts the exact bounded weights produced here. With the repaired source recursion below, those initial O(log n)-bit weights stay O(log n)-bit internally, since there are O(log^2 n) levels and any one update increases a weight by at most n-1. Arbitrary input real arithmetic is confined to the separately counted original-profile comparisons.

## Primary-source proof defects and explicit repairs

Two literal arguments in arXiv v1 cannot be called independently verified as printed.

1. It declares log=ln but uses ell<=log n after only proving ell<=log_2 n. The p. 24 duplicated-slice volume bound can actually fail for its written natural-log threshold. SOURCE_PROOF_REPAIR.md supplies a succinct finite median graph with n=10^12 whose two slice copies have 1,022,147,483,646 vertices. This falsifies that intermediate estimate, not the algorithm's correctness or the final theorem after repair.
2. The p. 13 proof of Lemma 16 reverses the factor comparison in its product bound by using the final s_r instead of the initial size. Its depth conclusion follows from the simple correct initial-size exponential estimate written in the repair document.

The explicit consistent replacement is f(N)=2 ceil(log_2 N) for every recursive N>=3, determined by integer bit length, with direct base cases N<=2. This gives no egalitarian cuts in the unbalanced branch, preserves unique-median, wide-ladder, gate, fiber and merge identities, ensures 2 sum|S_i|<=N, and bounds every child size by N(1-1/(lambda ln N)) with lambda=4/ln 2. The corrected elementary exponential estimate yields O(log^2 n) depth. Together with O(n log^2 n) work per level, this proves the required O(n log^4 n) import with no changed target or weight restriction. SOURCE_PROOF_REPAIR.md checks every relevant structural and runtime use, nonempty slice/base cases, v0 dominance and tie choice, and zero-weight behavior. It also gives a short independent median-based proof of the wide-ladder disjointness lemma.

The source's broader isometric-subgraph wording is unnecessary: every subgraph actually used is gated and median, where restricted Theta classes behave correctly. Thus no claim concerning arbitrary isometric nonmedian subgraphs is needed. A normal opening of the official SODA DOI was inaccessible via the web tool; this audit does not claim the final proceedings version has or has not corrected these issues, and no denied route was retried or bypassed.

## Reproducible finite controls

The independently authored controls do not import candidate code. All calculations involving profile values are exact rational calculations. They enumerate all labeled connected graphs through four vertices and all labeled median graphs on five vertices, with exhaustive nonnegative profiles from stated rational alphabets, including zeros, duplicates, unequal denominators and large ratios. The results are:

- 54,959 profile cases with optimum and entire-center-set agreement against direct radii.
- 2,646 complete feasibility-vector comparisons, including negative thresholds, attainable thresholds, and strict gaps.
- 199,663 implicit-search pivots, each checking its weighted-median property, quarter-removal inequality, feasible-witness invariant and optimum-survival invariant.
- 17 explicit source-recursion profiles, largest graph 408 vertices, exercising balanced and unbalanced cuts, all-zero weights, dominance and exact ties at v0, both fiber/original calls, and a wide ladder of size three.
- An exact rational certificate of the succinct primary-source volume counterexample, with no floating logarithm premise.

All assertions pass in CONTROL_RESULTS.json. The source recursion is reproduced using deliberately brute structural preprocessing; it verifies identities and branches, not the published asymptotic implementation. No finite test proves universal correctness or a runtime theorem. The first historical control version and output are preserved separately; the final version replaces a decimal-log illustration by an exact rational certificate and aligns its threshold with the final integer repair.

## Scope of acceptance and remaining boundary

The finite unit-edge target is resolved by the candidate, conditional only on ordinary use of the established classical median structural results and their preprocessing algorithms. This audit has supplied the needed explicit source-proof correction rather than treating the source as an opaque guarantee. It has not established a new historical-priority claim, formally verified a fast BDH implementation, handled arbitrary edge lengths, or assigned an encoding to infinite graphs. None of these is claimed by the candidate's finite theorem. The selected ID occurs in no existing related-target group; no different target was processed. No external individual was contacted, and no Git, branch, index, canonical research file, or original candidate file was modified.

The authored record is sealed by SHA256SUMS and excludes raw primary PDFs, OCR and page renders, which remain in ignored .cache only.
