# Row 118 — personal manuscript-only initial reconstruction

This is my own substantial reconstruction after reading all five actual deposited PDF pages, the full311-line controlling TeX and all five freshly rendered page images. It precedes any row118 foreign primary body, deposited program/result, archived triage/review or current peer scientific finding. Source metadata exposed support filenames and historical reading flags only. An unrelated row117 agent-inventory final summary was incidentally exposed earlier; no117 packet was opened or summary contents used/relayed, and root acknowledged that this supplies no118 findings. Earlier work on other rows is not represented as blind history. The target's own literature/priority paragraphs are part of the required complete manuscript read, not independent historical evidence.

Exact native identity:23385145, *Multiplicatively Weighted Centers of Median Graphs in Quasilinear Time*, API version string1.0, declared/printed14October2026, created15October2026. Actual PDF SHA-256 `d8d0049d312d564f72087c52e5c317c4ead05b40768fd9a57914a9a5909c1f0b`; TeX SHA-256 `15600ea002a5a054691dd18acb4275723dfc73ba81bd2f789da8b6e0607a7ecc`. The PDF front matter does not explicitly print a version. SOURCE_READY's controlling source locator is `extracted_path`, not a generic `path` field; the initial failed lookup occurred before TeX access and was corrected without source mutation.

## Family 1: exact category, quantifiers and output

The input is a finite nonempty connected simple graph with unit edges, supplied by adjacency lists and promised median, plus finite nonnegative real weights w(u). Median means a unique common vertex of the three pairwise intervals for every triple. The optimization is over graph vertices, with r_w(x)=max_u w(u)d(x,u), ρ=min_x r_w(x), C_w={x:r_w(x)=ρ}. It is not additive arrival eccentricity, recognition, arbitrary weighted edges, continuous edge facilities, infinite graphs or a unimodality theorem. No supplied cube embedding/dimension bound is assumed.

The full output is exactρ, one center and all centers, deterministically in O(n log^5(2n)) exact operations. Comparisons on original profile values are only comparisons of bounded products k w(u),0≤k≤n−1. An exact optimum is representable as a pair(k,u), not necessarily an evaluated real number. The all-centers output has at most n vertices, so enumeration does not itself exceed the bound. Classical median preprocessing and sparsity are explicit imported interfaces, not newly proved merely by the threshold identity.

Boundary deductions: n=1 givesρ=0 and the sole vertex, for any finite nonnegative weight. All-zero profiles giveρ=0 and every vertex. Exactly one positive support vertex givesρ=0 and that vertex uniquely, while zero-weight vertices remain legitimate facilities. Negative thresholds have empty feasible set because every product is nonnegative. Two or more centers are allowed. No numerical-genericity assumption can discard exact ties.

Status: exact target identified; no category weakening used. The scope of the workshop problem and older algorithms remains a primary-source interface to audit after sealing.

## Family 2: threshold conversion, without median geometry

Let D=n−1. Connected unit-edge distances are integers in[0,D]. For R≥0 define b_R(u)=max{k∈[0,D]∩Z:k w(u)≤R}, a_R(u)=D−b_R(u). Nonnegative w makes the predicate monotone in k; k=0 always works. If w(u)=0, all indices work and b_R=D. Otherwise this is the capped floor R/w(u), but binary search needs only comparisons of finite indexed products and no real division or unbounded-floor operation.

For each u, w(u)d(x,u)≤R iff d(x,u)≤b_R(u), since the actual distance is one of the indexed integers. This is iff d(x,u)+a_R(u)≤D. Taking the conjunction gives exactly r_w(x)≤R iff E_{a_R}(x)≤D, where E_a(x)=max_u(d(x,u)+a(u)). The identity holds on any connected unit-edge graph. Medianity enters solely through the fast additive oracle. The graph is unchanged, and a_R is an integer profile in[0,D].

Useful falsifiers: on path0−1−2 with weights(1,0,1), the unique center is the zero-weight vertex1 with radius1. Removing zero-weight vertices destroys a valid facility and the distance graph. On an edge of length1/2 with equal unit weights, the vertex optimum1/2 is not among indexed products{0,1}; arbitrary edge lengths cannot inherit the candidate argument. On an edge of length2, D=1 is not a distance bound and the capped additive threshold identity can fail. These are outside the exact written unit-edge category, not defects in it.

Status: complete independent pointwise equivalence, including zero weights. No Helly/ball-convexity/local-search claim is required.

## Family 3: the exact imported oracle and full feasible set

Assume, pending actual primary inspection, the stated BDH theorem: all additively weighted eccentricities E_a on a promised median graph, for the required nonnegative integer a, in O(n log^4(2n)) operations including preprocessing. Then build n budgets with O(n log(2n)) original-weight comparisons, make one oracle call, and scan E_a≤D. This returns the entire F_R, not just a yes/no answer. A nonempty result supplies an actual witness vertex. Monotonicity F_R⊆F_{R′} for R≤R′ follows directly from the original objective.

The import must genuinely accept additive arrival labels, not multiplicative weights or an unweighted-only objective. Its exact integer-label category, preprocessing, word bounds and promise/embedding requirements are load-bearing. The paper expressly repairs estimates in a particular public preprint; a theorem headline is not enough to certify that repair. I have not read the foreign body yet and do not treat these interfaces as closed at this initial seal.

Falsifiable checks after seal: compare the oracle result to direct distances on small median graphs; retain zeros, singleton support, ties, R=0 and equality boundaries. Distinguish a slow reference implementation used for such checks from an implementation demonstrating the claimed fast asymptotic algorithm.

Status: algorithmic reduction closes conditionally on the exact imported interface; primary proof/interface audit remains necessary.

## Family 4: exact optimum candidates and incumbent invariant

Every radius is an attained maximum over a finite nonempty set of products d(x,u)w(u), so each radius and the minimumρ belong to n conceptual sorted rows S_u=(0,w(u),...,D w(u)). The n² entries need not be materialized. Use inclusive row intervals[l_u,h_u] and store only their integer endpoints. B=D max_u w(u) is initially feasible because every actual distance≤D; any graph vertex witnesses it. This is an upper bound, not a claim that the witness radius equals B. Handle D=0 or B=0 explicitly.

The maintained assertion is: B is feasible, and either B=ρ or at least one active row entry equalsρ. For a feasible pivot q,ρ≤q. Save a witness and lower B to min(B,q) before deleting all entries≥q. If q=ρ, B stores it; ifρ<q, optimum copies survive. For an infeasible q,ρ>q, so deleting entries≤q preserves all optimum copies. If an old incumbent is already smaller than a feasible q, keeping it is sound and the active optimum survives unless the incumbent already equalsρ. Empty active rows therefore force B=ρ. Its saved witness is a center, and the final full query returns F_B=C_w.

Critical falsifier: path0−1−2 with weights(1,0,1) has initial B=2 butρ=1. A feasible pivot1 followed by deleting all copies≥1 without first saving it can lose the optimum and return2. The paper's saving order and equality case avoid this error. For weights(1,0,2), centers{1,2} haveρ=2; changing≤ to< in budget construction loses both equality cases. Zero rows have repeated equal candidates and must be pruned by exact weak comparisons.

Status: independent invariant proof closes, including incumbent/pivot ties and multiple optimum copies.

## Family 5: weighted pivot progress and multiplicities

For a row of active length L, its lower middle has at least L/2 entries on either weak side. For even L=2k it has k on the lower side and k+1 on the upper; for odd L=2k+1 both have k+1. Constant zero rows only increase weak-side counts.

Give each row middle selection weight equal to its full active length. A deterministic weighted median q exists: sort the n middle values and choose the first whose cumulative length reaches M/2, M=sum L. Its weak lower and upper sides each carry at least M/2. If q is infeasible, rows with middle≤q lose at least half their entries; if feasible, use rows with middle≥q. Thus at least M/4 conceptual entries are deleted. The new integer M is at most3M/4, and M starts at n², so there are O(log(2n)) iterations, with the final integer tail also ending. Equal values, singletons and zero rows are included.

An unweighted median of the row middles would not prove this. Many length1 rows can outvote one huge interval while deleting an arbitrarily small fraction of total M. The row length weights, and inclusive pruning at equality, are essential. No probabilistic pivot is used.

Status: full independent progress proof closes and provides a precise mechanism to test in finite controls after sealing.

## Family 6: complexity and representation accounting

Each iteration sorts at most n product-pairs and performs bounded binary searches for row pruning and for n threshold budgets. This costs O(n log(2n)) original-weight comparisons per iteration. With O(log(2n)) iterations, comparison overhead is O(n log²(2n)); the final query adds only another n log(2n). The oracle cost per call is O(n log⁴(2n)), and O(log(2n)) calls plus one final complete-output call yield O(n log⁵(2n)). Repeating oracle preprocessing is already allowed in this bound. Row endpoints/storage use O(n) words beyond the oracle, and M≤n² needs only O(log n) bits per counter.

The graph's adjacency read cost is absorbed only using the imported median sparsity bound m≤n log₂n; it must not silently be assumed for general graphs. A hypercube graph has dimension log₂n, so excluding a supplied embedding or dimension bound is substantive, not a constant-factor convention.

On rational input w(u)=p_u/q_u, compare k w(u) and j w(v) by k p_u q_v versus j p_v q_u. With B-bit components and k,j≤n−1 these have at most2B+O(log n) bits, hence O(B+log n). The operation bound is not a bit bound independent of input encoding. Exact real input is an oracle/comparison model; approximation/tolerance and irrational-bit encodings are not supplied by the theorem. Label arithmetic inside the additive oracle is a separate small-integer issue audited in the appendix.

Status: complexity composition closes conditionally on the exact BDH/imported structure bounds and word model, with no hidden quadratic candidate materialization.

## Family 7: recursion repair, path depth and label size

For a recursive graph of order s≥3 set L(s)=ceil(log₂s), f(s)=2L(s), computable as twice the bit length of s−1. Assume the actual BDH structural and merging identities apply to this balance parameter and that each slice lies inside one minority halfspace. A balanced cut partitions s into two children, each at most s(1−1/f). In the unbalanced case ell pairwise orthogonal incident classes yield ell≤log₂s≤L, each slice size<s/f, and both slice calls are retained. Thus total child volume2 sum|S_i|≤2ell s/f≤s, and each child is at most s(1−1/f), since f≥2. Gatedness must justify the identities; the parameter alone does not prove them.

For λ=4/ln2, f(s)≤4log₂s=λlns. Along a nonterminal path under root size N≥3,
s_{i+1}≤s_i(1−1/f(s_i))≤s_i(1−1/(λlns_i))≤s_i(1−1/(λlnN)).
Consequently s_h≤N exp(−h/(λlnN)); h=ceil(λ(lnN)²) forces s_h≤1, so a path must already have reached the s≤2 base case. Depth is O(log²N) without invoking the preprint's alleged product comparison. Child volumes≤parent give total volume≤N per recursion level. If the actual local work is O(s log²(2s)), total work is O(N log⁴(2N)).

If an arrival-label update has form max over fibers of old label plus graph distance, every update increases the previous global maximum by at most N−1. Initial labels≤N−1 and O(log²N) update depth imply O(N log²(2N)) labels and O(log(2N)) bits. This requires inspection of the actual updates; it cannot be assumed if labels are summed/multiplied differently. Retaining both original and fiber-weight calls is important because a fiber weight need not pointwise dominate the original profile.

Status: independent numerical/recurrence proof is complete under explicitly listed structural inputs. Actual preprint algorithm/parameter/preprocessing/label update interfaces remain the principal post-seal task. The paper's claim about the sign error and final SODA edition is not independently verified here yet.

## Family 8: succinct appendix witness and source-scope credit

The stated enormous witness can be checked symbolically, without constructing10¹² vertices. A Q30 cube has2³⁰=1,073,741,824 vertices. Add30×17,000,000,000 leaves at its unit vectors and488,926,258,176 at zero: total10¹² exactly. Attaching pendant trees preserves medianity, since path intervals involving a leaf pass through its attachment vertex and the remaining triple median reduces to the original cube/tree median.

Each coordinate1 halfspace contains2²⁹+17,000,000,000=17,536,870,912 vertices. The positive Taylor partial sum sum_{j=0}^{11}7^j/j! exceeds1000 (the terms through10 total about988.59 and the next exceeds49). Thus e⁷>1000 and ln(10¹²)=4ln1000<28. Multiplying a coordinate minority by56 gives982,064,771,072<10¹². Pendant cuts are also unbalanced for the literal2lnN threshold. Coordinate-majority halfspaces and pendant-majority sides intersect only at zero. The cube antipode with arrival N−1 is uniquely farthest there, because every other arrival is zero and the entire unweighted graph has small diameter. The30 incident cube classes are pairwise orthogonal.

The coordinate minority union has2³⁰−1+30×17,000,000,000=511,073,741,823 vertices. Two copies have1,022,147,483,646>N. This verifies the stated integer arithmetic and conditional geometric picture. To conclude that it refutes the cited algorithm's literal intermediate volume estimate, I must still inspect the actual definition/partition of its wide-ladder slices and the preprint's log convention. It does not by itself refute the algorithm's correctness or asymptotic theorem. Under f(N)=2ceil(log₂N)=80, these coordinate cuts instead become balanced, illustrating why the changed parameter avoids that root configuration.

Credit interfaces requiring actual bodies after this seal: exact OWR finite multiplicative-weight problem and separate unimodality/edge-length questions; BDH public preprint additive theorem, Algorithm1 and recursion proof, with final SODA edition distinguished; Ducoffe's ESA/full-preprint decision-to-optimization lemma; the earlier cube-free O(n log²n) special case; tree-product representation promise; classical median preprocessing. The manuscript expressly attributes these mechanisms and makes only a bounded priority claim. It does not certify continued worldwide openness. I will not replace those actual-source checks with archived reviews or code output.

## Initial conclusion and next evidence

The threshold and implicit-search mathematics reconstruct cleanly on the exact written category. No in-category counterexample is identified at this initial stage. The principal unresolved verification is the full BDH imported algorithm and parameter-compatible structural/preprocessing/label estimates, plus precise source/problem/priority interfaces. This is a provisional initial reconstruction, not final clearance. I will inspect actual primary bodies and applicable support after sealing, retain defects precisely if found, and avoid extended repair or narrowed promotion.

All eight families have a distinct mechanism, explicit conditions, checkable deductions and stated remaining interfaces. Supporting computational checks will target these obligations rather than repeat a huge historic campaign. They will not substitute finite samples for the universal proof.
