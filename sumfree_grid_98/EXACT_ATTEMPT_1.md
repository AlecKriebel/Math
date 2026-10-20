# Exact finite-grid attempt 1

Date: 2026-10-20. Target: f_d(N), the maximum cardinality of A⊆{1,…,N}^d with (A+A)∩A=∅. Repeated summands are forbidden too. This is the stronger exact finite interpretation, not merely the limiting constant in Green's highlighted question.

## Outcome

The general exact finite problem is **not resolved** here. We obtain an exact slice-count formula, elementary exact infinite families, and independently checked finite upper certificates. The strongest finite coordinate-sum slice conjecture is **false**: f_6(3)≥706, while the largest coordinate-sum slice has only 700 points. See the explicit counterexample below. Exact upper optimality of 706 had not yet been proved at this stage. The later [attempt 2](EXACT_ATTEMPT_2.md) proves f_6(3)=706, independently confirmed in [FINITE_AUDIT.md](FINITE_AUDIT.md).

## Primary-source boundary

1. P. J. Cameron, *Sum-free subsets of a square*, December 2002, Proposition 1: f_2(N)≥floor(3N(N+1)/5), from an optimized diagonal stripe. This is a lower bound, not a matching exact upper theorem. Source: https://maths.qmul.ac.uk/~pjc/odds/sfsq.pdf . Search extraction from a second author-hosted mirror misrenders floor as ceiling; direct counting resolves the ambiguity (N=2 gives 3, not 4).
2. Elsholtz–Rackham, *Maximal sum-free sets of integer lattice grids*, JLMS 95 (2017), 353–372: the primary publisher abstract identifies the limiting 2D density, not a finite exact formula: https://doi.org/10.1112/jlms.12006 .
3. Liu–Wang–Wilkes–Yang, *Shape of the asymptotic maximum sum-free sets in integer lattice grids*, arXiv:2108.10526v2, Introduction and Theorems 1.2–1.3: stability and asymptotic size results. Although the abstract says “maximum size” for the generalized equation, the actual theorem retains O(N), so it is not an exact finite solution. https://arxiv.org/html/2108.10526v2 .
4. Lepsveridze–Sun v3 and Keevash–Lim v2 are checked in SOURCE_GATE.md: their theorems retain error terms. The all-dimensional Keevash–Lim result is a submitted preprint whose proof is being independently audited separately.

The primary sources inspected establish f_1(N)=ceil(N/2). This search has **not** established a literature theorem determining f_d(N) for arbitrary finite N and d≥2, nor does absence from this search prove that no such theorem exists.

## Exact finite slice calculation

Put H_{d,N}(s)=#{x∈{1,…,N}^d: Σx_i≤s}. With binomial(a,d)=0 when the integer a<d,

H_{d,N}(s)=Σ_{j=0}^d (-1)^j binomial(d,j) binomial(s-jN,d).

Proof: write x_i=1+y_i, use stars-and-bars for nonnegative y_i with total at most s-d, and inclusion-exclusion on y_i≥N.

For each positive integer t, S_t={x:t≤Σx_i≤2t−1} is sum-free, since sums of two members have coordinate sum at least 2t. Therefore

f_d(N)≥L_d(N):=max_{1≤t≤dN}[H_{d,N}(2t−1)−H_{d,N}(t−1)].

This is the sharp maximum **within the coordinate-sum slice family**. Allowing a real lower endpoint u cannot improve it: with t=ceil(u), the lower integer rank is t and ceil(2u)−1≤2t−1, so the real-endpoint slice is contained in S_t.

For d=2 the maximizing t can be chosen as floor((4N+7)/5), and the resulting maximum is floor(3N(N+1)/5), including small N. In the central range, the count is [-5t²+(8N+9)t−2(N+1)(N+2)]/2. Outside that range, moving toward the central range cannot reduce the count; rounding the concave quadratic's vertex proves the formula.

## Elementary exact families

- f_1(N)=ceil(N/2). If m=max A, the involution x↦m−x pairs the integers 1,…,m−1; at most one of each pair lies in A, and a fixed point m/2 cannot belong to A. Include m separately. This gives |A|≤ceil(m/2)≤ceil(N/2), attained by integers greater than N/2.
- f_d(1)=1.
- f_d(2)=2^d−1 for every d≥1. The only possible sum relation in {1,2}^d is 1⃗+1⃗=2⃗. At least one of these vertices must be deleted, and deleting 1⃗ suffices. This is also the slice t=d+1.

## Certified finite searches

The completed integer-only searches give:

| d | N | f_d(N) | best slice |
|---|---|---|---|
| 2 | 2 | 3 | 3 |
| 2 | 3 | 7 | 7 |
| 2 | 4 | 12 | 12 |
| 2 | 5 | 18 | 18 |
| 2 | 6 | 25 | 25 |
| 2 | 7 | 33 | 33 |
| 2 | 8 | 43 | 43 |
| 3 | 2 | 7 | 7 |
| 3 | 3 | 23 | 23 |
| 3 | 4 | 53 | 53 |
| 3 | 5 | 101 | 101 |
| 4 | 3 | 75 | 75 |

These are authored computations, not claims that the values are new to the literature.

### Upper-certificate logic

Make a hypergraph whose vertices are grid points and whose edges are the distinct sets {x,y,x+y} for all valid sums. When x=y the edge has two vertices, which is essential. A sum-free set is exactly the complement of a vertex cover.

To show f_d(N)≤K, prove every cover has size at least N^d−K. At a node with already deleted vertex set D:

- A leaf supplies pairwise vertex-disjoint forbidden edges, all disjoint from D. Each needs one further deletion. If |D| plus the packing size is at least N^d−K, this node is certified.
- Otherwise choose one unmet forbidden edge e. Any cover extending D deletes at least one vertex of e. Branch on every vertex v∈e, with child deletion set D∪{v}. No possibility is omitted.

The finite directed certificate graph rooted at D=∅ proves the upper bound by induction. Its state sets strictly increase along edges, so no circular justification is possible. The lower bound is an actual slice, independently recounted.

`exact_finite_search.py` performs integer-only exhaustive search. `certify_finite.py` separately exports compressed JSON branching certificates and independently reconstructs every forbidden edge for replay. Replay checks each packing, every branch, the threshold, and the matching lower bound. Certificate files are `finite_certificate_d*_n*.json.gz`; `FINITE_CERTIFICATE_LOG.txt` records completed replays. `EXACT_FINITE_RESULTS.jsonl` retains witnesses and search-node counts. No floating-point solver bound is used for these exact claims.

## Explicit finite counterexample to coordinate-sum slice extremality

In {1,2,3}^6 take S={x:9≤Σx_i≤17} and add the six permutations of (3,1,1,1,1,1). The slice contains 700 points. Each added point has coordinate sum 8 and so is new. More importantly, every added point is isolated from all sum relations in the entire grid: its coordinate 3 prevents it from being a summand, and its coordinate 1 prevents it from being a sum. Hence the enlarged set is sum-free and has 706 points.

The slice counts for integer t=1,…,18 are respectively 0,0,0,7,78,294,560,694,700,651,561,435,294,168,78,28,7,1. The real-endpoint dominance proof above therefore proves that no coordinate-sum slice exceeds 700. `D6N3_COUNTEREXAMPLE_CHECK.json` records an exhaustive check of all 498436 ordered pairs of points in the construction, including equal points. The argument itself is independent of the numerical solver that suggested the example. This does not contradict a fixed-d asymptotic theorem; it concerns a small positive-grid boundary effect. No novelty claim is made.

The verifier now uses explicit exceptions, not assert statements. All 12 completed certificates passed under python -OO; reducing the claimed K by one was rejected for every certificate.

## Next gap and discriminating attempts

The counterexample disproves f_d(N)=L_d(N) for all d,N. The missing step is a corrected finite structural theorem or a matching exact upper bound for the improved construction. A promising concrete target is a systematically constructed cover-packing certificate matching L_d(N), potentially using the discrete slice couplings while retaining endpoint and integrality effects. The isolated-vertex improvement already provides such a witness. The next structural target is an exact reduction for N=3 to disjoint unions of Boolean subsets, with the central vertex counted only once.

Larger exact searches and a separate MILP witness exploration are in progress. MILP output, if any, is only a source of candidate subsets: integer sum-free validation proves a lower bound, but solver status or floating-point objective bounds are not accepted here as exact upper certificates.
