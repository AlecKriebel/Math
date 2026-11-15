# Independent adversarial initial reconstruction — record 23385145

This reconstruction follows personal reading of the complete actual five-page published PDF, all311controlling-TeX lines and all five fresh page rasters. No cited foreign body, deposited programme, deposited result, historical audit, inventory triage or current peer opinion has been read. The manuscript itself is the sole scientific input. This is a falsification-oriented initial proof/claim reconstruction, not a final adoption of an imported theorem. Root118initialgate remains closed at this seal; no findings are released.

## Exact full hypothesis and success criterion

The target is a finite, nonempty, connected, simple, unit-edge median graph G supplied by adjacency lists, with n vertices and every finite real weight w(u) nonnegative. Centers are vertices of G. Define r_w(x)=max_u w(u)d(x,u), rho=min_x r_w(x) and C_w={x:r_w(x)=rho}. The complete claim is deterministic computation of rho, one center and every center in O(n log^5(2n)) exact operations, with no bounded cube dimension and no supplied embedding. Original-real-profile operations consist only of comparisons of k w(u) and j w(v), 0≤k,j≤n−1. Rho may be represented by a pair (k,u). Rational bit/input-reading costs are separate. The original theorem is not an arbitrary-edge-length, continuous-facility, recognition, infinite-graph, bit-independent or unimodality result.

The route has three central obligations: the exact threshold transformation; a genuinely logarithmic-query exact implicit optimization with complete output; and the applicability/complexity of the imported additive eccentricity algorithm, including the manuscript's own claimed repairs. A valid reduction alone is insufficient to certify the entire theorem if the last obligation fails. Conversely, a wrong literal estimate in an earlier source proof is not automatically a counterexample to the imported algorithm or to the repaired theorem.

## Family 1 — attack the threshold transformation and its integer boundary

For any connected unit-edge graph, D=n−1 bounds every distance and all distances are integers. For R≥0 set b_u=max{k∈{0,…,D}:k w(u)≤R}, a_u=D−b_u. Since 0 is admissible, b exists. When w(u)>0, monotonicity of k↦k w(u) gives, for every integer t∈[0,D],

    w(u)t≤R iff t≤b_u iff t+a_u≤D.

For w(u)=0, every k is admissible, b_u=D, a_u=0, and both constraints hold because t≤D. Taking all u gives r_w(x)≤R iff max_u(d(x,u)+a_u)≤D. This is a pointwise equivalence for every x, hence preserves the entire feasible set, not only whether one vertex exists. The reduction itself uses no median property, Helly theorem, ball convexity or local minima.

Boundary attacks: R=0; thresholds exactly k w(u); all w=0; one positive weight among zero weights; D=0; a positive threshold above D w(u); and symbolic infinitesimally separated positive weights. Binary search must use inclusive ≤ and cap at D, not an unbounded floor or floating approximation. For R<0 the original objective is always nonnegative (each x contributes w(x)·0), so feasibility is empty; that branch is separate from a formula whose admissible index set might be empty.

An actual excluded-model counterexample shows why integer distances matter. Let n=2, one edge have length1/2, w at one endpoint be1, and R=3/4. At the other endpoint the multiplicative contribution is1/2≤3/4, but D=1, b=0 and its additive contribution1/2+1 exceeds1. Thus replacing unit-edge distances by arbitrary lengths is not a harmless generalization of this lemma.

Falsifiers after this seal: exhaustive exact comparisons against brute all-pairs distances, equality thresholds and just-below/above rational thresholds; deliberately remove the cap, change ≤ to < or delete zero-weight vertices and require rejection of those wrong variants.

## Family 2 — attack the comparison model, candidate representation and hidden n² work

Every r_w(x) is an attained maximum among finitely many products k w(u), with 0≤k≤D. Therefore its finite minimum rho is an entry of one of n conceptual sorted rows S_u=(0,w(u),…,D w(u)). This uses attainment, not a continuous search argument. The proposed algorithm need store only active row endpoints, row lengths, one product-pair pivot/incumbent and a vertex witness. It must not materialize the n² candidates or all n² distances.

For n≥2, max w can be selected by comparing 1·w(u); multiplying its representative by D creates an incumbent B=D max w with r_w(x)≤B for every vertex x. A witness to B need only have radius at most B; its radius need not equal the initial upper bound. For n=1, D=0, radius0 and the sole vertex is a center regardless of its finite weight, so no disallowed k=1 comparison is required.

Every later threshold is a selected pair q=jw(v) from active rows, and every budget test compares kw(u) with that pair. Pivot sorting, strict row deletion, B updates and equality use precisely these comparisons. No real division, arbitrary real floor, tolerance or evaluation of a transcendental weight operation is needed. A mathematical exact comparison oracle permits all finite real profiles in this declared model; this is not a Turing encoding for arbitrary reals.

For rational w(u)=p_u/q_u, q_u>0, compare k p_u q_v and j p_v q_u. With components at most B bits these products have O(B+log n) bits (the two B-bit factors contribute2B, which is still O(B)). O(n log²(2n)) real-product comparisons follow only after the logarithmic-query proof below. Their bit cost and input-reading cost must be included separately. An implementation using language rationals proves finite exact diagnostics, not automatically the declared unit-operation asymptotics.

The row lengths and total M≤n² use O(log n)-bit integers. Storage O(n) means words/pairs beyond the imported oracle, not n-bit reals of uniform encoding length. Reading an adjacency list must be O(n+m), so the median edge bound is an essential promise-specific input-size check. Even Q_d has m=nd/2=½n log₂n and unbounded d, still absorbed by the claimed bound.

## Family 3 — attack pruning invariants, witness updates and exact ties

Let each active row be an inclusive integer interval [l_u,h_u]. Maintain: B is feasible with a witness, and either B=rho or at least one active entry equals rho. Initially rho is a conceptual candidate and B is feasible. A feasible pivot q has rho≤q. If rho=q, setting B=min(B,q) saves equality and a witness whenever B decreases. If rho<q, deleting every active entry≥q preserves every optimum copy. If q is infeasible then rho>q, so deleting entries≤q likewise preserves every optimum copy. Empty active intervals therefore force B=rho; the stored witness, whose radius is≤B, is then a genuine center.

Strictness is essential. The feasible branch keeps only entries<q after saving the feasible incumbent; the infeasible branch keeps entries>q. Binary searches are lower_bound(q)−1 versus upper_bound(q), with no assumption of distinct candidates. Zero rows contain D+1 duplicate zeros. They must be removed exactly rather than treated as a unique numerical candidate. If an implementation discards a feasible equality without saving B/witness, it can lose the true optimum when all optimum copies are removed.

A final exact feasible-set query at B returns {x:r_w(x)≤rho}=C_w because no vertex has radius below rho. Merely returning the first oracle witness or all active rows would not compute all centers. The incumbent is a product pair; retaining its original representative avoids a later arithmetic encoding change.

Concrete sanity cases: a single positive-weight site u gives rho0 and center set{u}; an all-zero profile gives every vertex. On a unit path of four vertices with endpoint weights1 and interior weights0, both middle vertices have radius2 and must be output. On a unit two-vertex edge with both weights1, both endpoints are centers of radius1. These expose equality, multiple-output and witness-vs-bound mistakes.

## Family 4 — attack the iteration count independently of correctness

For a row of length L, the lower middle index floor((l+h)/2) has at least L/2 active entries on each weak numerical side; equal values only increase those counts. This holds for even L (the lower half has exactly L/2, the upper has at least L/2), odd L and singleton rows.

A weighted median of the row middle values with row selection weight L_u has total row length≥M/2 on either weak pivot side. If q is infeasible, take rows with q_u≤q: at least half of each such row is≤q, and those entries are deleted, totaling≥M/4. If q is feasible, take rows q_u≥q and delete their upper halves. The proof uses weak sides and multiplicity, so ties and zero rows do not create a gap.

Thus M_next≤3M/4 while M>0. Starting at M=n², after h iterations M≤(3/4)^h n²; since M is an integer, h=O(log(2n)). One oracle call per iteration plus the final all-centers call suffices. Sorting at most n pivots and two bounded binary searches per row each take O(n log(2n)) comparisons/work, giving O(n log²(2n)) overhead. Combined with an applicable O(n log⁴(2n)) additive oracle the result is O(n log⁵(2n)); the exponent is not inferred from test timings.

An unweighted median of row middles is not a substitute. For example, about half the active rows can be singletons near zero while the other half have length n with much larger middles. An infeasible zero pivot can remove only O(n) entries out of Θ(n²). The required charging proof is based on L_u weights, not the number of active rows. This supplies a structural falsifier for a tempting implementation shortcut.

## Family 5 — attack output domains, support removal and graph promises

Zero-weight vertices cannot be deleted from the graph or candidate-center domain. On P3 with weights(1,0,1), the unique center is the zero-weight middle vertex and rho1; removing it also disconnects the positive support. Threshold arrival0 is not a license to delete that vertex: its d≤D additive constraint is merely vacuous, while its role as a vertex and part of shortest paths remains.

Uniform weights1 on Q_d give radius d at every vertex, hence C_w=V with output size n. This is compatible with O(n polylog n) output but falsifies a claim that only boundedly many centers need be returned. Unbounded cube dimension does not mean d can exceed log₂n: the d-cube itself has2^dvertices.

On a unit edge with equal positive weights the continuous facility center has radius1/2 whereas vertex centers have radius1. The theorem must not be read as the continuous problem. A nonmedian integer graph still satisfies Family1, but the fast imported oracle is unavailable; the reduction is not a proof of quasilinear weighted centers for every graph. Disconnected/infinite graphs, nonfinite weights and unsupplied infinite encodings also fall outside the literal model. Negative weights would break the nondecreasing-row optimization premise (all-negative profiles already have radius0 because self terms are0 while D max w is negative); no such extension is claimed or repaired.

For input size, a median Θ-split has convex median halfspaces of sizes p,q and a matching of at most min(p,q) crossing edges. Given that classical structural interface, induction yields m≤½n log₂n: add the two inductive bounds and min(p,q), then use binary entropy H(p/n)≥2 min(p,q)/n, the chord bound from concavity on[0,1/2]. This is an independent consistency derivation of the edge-count scale, not a constructed fast embedding/preprocessing algorithm.

## Family 6 — attack the imported additive objective and fiber semantics

The actual needed oracle computes all E_a(x)=max_u(d(x,u)+a(u)), with nonnegative integer a(u) initially in[0,D], from adjacency lists on the promised median graph, in O(n log⁴(2n)) including preprocessing. A theorem for unweighted eccentricity, multiplicative weights, supplied embeddings, bounded cube dimension, or only one center is insufficient. This exact source interface must be read after the initial seal; it has not yet been authenticated here.

The max-plus gate identity can be reconstructed independently. For a gated subgraph H and a source subset U, put b(v)=max_{u∈U:g_H(u)=v}(d(u,v)+a(u)), with max empty=−∞. Gatedness gives, for x∈H,

    max_{u∈U}(d(x,u)+a(u)) = max_{v∈H}(d(x,v)+b(v)).

For full U=V, b(v)≥a(v) since v lies in its own fiber. For a proper subset U, that dominance need not hold. On path0–1–2 with H={1,2}, U={0}, a(0)=0 and a(1)=100, the external fiber weight at1 is1, below100. Replacing the original profile by that external profile alone loses the original E value100 at x=1. This is a concrete falsifier for dropping an original-weight slice call under an unjustified dominance assumption.

The manuscript expressly retains both original and fiber-weight slice calls. Their actual source definitions, excluded source sets, empty-fiber conventions, merge identity and preprocessing must be checked, not guessed from the word“fiber”. Adding zero to an empty external fiber is harmless only with a separately retained nonnegative original-source call that dominates the added distance-only terms. This family is currently an explicit external-interface frontier; no source-proof correctness has been assumed.

## Family 7 — attack repaired recursion, word bounds and hidden parameter dependence

Conditionally on the stated gated-slice structure and nonrecursive work bound, the manuscript's replacement estimates can be rederived without the source's alleged product inequality. For s≥3 define L=ceil(log₂s), f=2L. If at most ell≤L slices each have size<s/f, the two retained calls per slice have summed volume<2ell s/f≤s. Balanced children partition s. Consequently per-level summed graph order≤the root N by induction, despite duplicated calls.

For a balanced split both children have size≤s−s/f. For unbalanced slice calls, child size<s/f≤s(1−1/f) since f≥2. Also L≤2log₂s for s≥2, so f≤4log₂s=λ ln s with λ=4/ln2. Along any nonterminal path from rootN,

    s_(i+1)≤s_i(1−1/(λ ln s_i))≤s_i(1−1/(λ ln N)).

Iterating and using1−t≤exp(−t), s_h≤N exp(−h/(λ ln N)). At h=ceil(λ(ln N)²), this is≤1, so the path must already have hit the direct s≤2 case. No reversed comparison of a product is needed. O(s log²(2s)) nonrecursive cost at every node then gives O(N log²(2N)) per level and O(N log⁴(2N)) total.

If every fiber update adds a graph distance≤N−1 to a previous maximum label, an initial label≤N−1 becomes at most(N−1)(h+1)=O(N log²(2N)) on a path. Its bit length is O(logN), so a word-RAM using Θ(logN)-bit words can still count these integer operations uniformly. This is a global-root word bound, not a false bound by the much smaller local child size.

Central falsification frontier: actual BDH proofs must permit this replacement of the balance threshold and retain the claimed per-node work, structural orthogonality, slice containment, gate identities, preprocessing and update form for all recursion nodes. Merely proving a recurrence after changing an algorithm parameter does not prove an unchanged source algorithm meets it. If that interface fails substantively, the full paper cannot be promoted by narrowing it to a conditional reduction or inventing a new repair.

## Family 8 — attack the explicit succinct counterexample and its source applicability

The displayed large construction can be checked exactly without allocating10^12vertices. Q30 has2^30=1,073,741,824vertices. Attach A=17,000,000,000leaves to each of30unit vertices and B=488,926,258,176leaves at0. The total is2^30+30A+B=10^12. Attaching a pendant tree at a vertex preserves medianity: all routes from a new leaf to old vertices pass its attachment point, so triple medians reduce to old medians, with repeated-leaf cases immediate.

A coordinate minority halfspace contains2^29cube vertices plus exactly A leaves from its matching unit vertex, hence17,536,870,912vertices. Every leaf edge gives minority1. Own exact Fraction arithmetic finds a positive degree11Taylor partial sum of exp(7) greater than1000. Therefore ln(10^12)=4ln1000<28. Every coordinate minority then satisfies(2lnN)·minority<56·minority=982,064,771,072<N; leaf cuts do too. All cuts are unbalanced at the literal natural-log threshold if the source uses that threshold.

The union of all coordinate minorities is every cube vertex except0 plus all30Aunit-vertex leaves:511,073,741,823vertices. Two copies total1,022,147,483,646>N. With arrival N−1 only at the cube antipode and0elsewhere, that antipode is uniquely weighted farthest from0, and the30incident cube classes are pairwise orthogonal. This arrival profile can even arise from Family1 at R0 with the antipode as the sole positive multiplicative-weight site; it is not obviously excluded by the reduction's initial offset range.

The arithmetic assertions are confirmed in OWN_INITIAL_ARITHMETIC.json. Actual applicability to the source's “wide ladder” and exact slice union/partition remains to be read in the primary algorithm; a claimed volume counterexample requires the real definitions and calls. Even if it refutes that intermediate literal bound, it does not by itself refute the advertised algorithm or the manuscript's repaired complexity. No historical-source error is declared independently authenticated before reading that source.

## Independence, remaining work and stopping rule

The threshold and optimization deductions above are checkable directly from the manuscript's literal definitions. The imported additive algorithm and claimed proof repair are the main unresolved source interfaces. After this seal, write/run independent exact finite diagnostics and inspect the actual cited primary interfaces and deposited supporting artifacts, preserving all original bytes and exact historical status objects. Finite brute algorithms test coverage, ties, invariants, model boundaries and arithmetic; they will not be called a fast implementation or a proof of the asymptotic theorem.

Any substantive gap/counterexample affects the whole literal claim and must be recorded without extended repair or narrowed promotion. Priority/worldwide openness are not inferred from a negative search, and no external contact will be prepared or initiated. Scientific findings remain gated until root118's explicit initial OPEN. This initial reconstruction is complete as an independence checkpoint; the overall adversarial review is approximately30% complete.
