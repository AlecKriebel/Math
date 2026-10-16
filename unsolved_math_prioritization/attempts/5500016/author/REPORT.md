# Exact counting of simple polygonalizations: partial results and obstructions

Research note, 8 October 2026. Target: TOPP Problem 16, “Simple Polygonalizations” (5500016 / AMR-054-0016).

## Summary

The general exact-counting question is **unresolved by this report**. No polynomial-time algorithm, hardness reduction, or new complexity classification is established. The maintained problem page still identifies it as open [1]. The claims below are elementary, checkable partial results and obstructions to five particular approaches; no novelty is asserted.

The main mathematical outputs are:

1. An explicit counterexample to treating all noncrossing partial paths with the same visited set and endpoints as continuation-equivalent.
2. A polygon–triangulation incidence identity and a five-point counterexample to uniform extension multiplicity.
3. An exact crossing-event inclusion–exclusion identity with a closed formula for each forced-edge term.
4. A positivity obstruction to a naive parsimonious hardness reduction into general-position point sets.
5. An exact algorithm examining `k! binomial(n−1,k)` candidates when exactly `k` points lie strictly inside the convex hull. This is polynomial for each fixed `k`, but does not solve the unrestricted problem.

A small exact-arithmetic checker accompanies the note. Its finite tests are evidence about the stated examples and implementation, not a proof of polynomial-time tractability or intractability.

## 1. Exact question and conventions

Let `P={p_0,...,p_(n−1)}` be distinct points with rational coordinates, encoded in binary. The integer `N(P)` counts undirected simple straight-line Hamiltonian cycles on `P`. Every point is used exactly once. Two traversals differing only by the initial vertex or traversal direction represent the same polygon. Congruences or symmetries of the whole point set do not identify different edge sets. Labels merely name the fixed input positions.

For `n≥3`, a polygon has precisely `2n` vertex-sequence representations. A canonical representation starts at vertex `0` and requires its next label to be smaller than its last label. Thus symmetry does not require an orbit-counting correction depending on the geometry.

The principal proofs and algorithms below use the promise that no three points are collinear. For this promise, a cycle is simple exactly when no two nonincident edges cross. Four cocircular points are allowed in our definitions and checker.

For the checker’s broader, degenerate-input convention, a polygon is an injective polygonal closed curve, with straight, 180-degree boundary vertices permitted. Edges may meet only at a shared endpoint of consecutive edges. An edge cannot pass through another input vertex; overlapping or backtracking edges and nonadjacent touching are invalid. Fewer than three points and all-collinear point sets have count zero. Duplicate points are rejected as invalid input. These are explicit conventions, not a claim that every version of the source question uses the same treatment of degeneracies.

Arbitrary perturbation is not a counting-preserving reduction. For example, the boundary points `(0,0),(1,0),(2,0),(2,2),(0,2)` have one polygon under this convention. Moving `(1,0)` slightly inward creates a general-position set with four polygons. The integer-scaled example in the checker moves it to `(100,1)` while scaling the square by 100. A proof for general-position inputs alone therefore does not silently cover collinear inputs.

### Computational model

Write `L` for the total binary length of the rational input. “Polynomial time” means polynomial in `L`, with the integer answer in binary. Exact orientation and segment-intersection predicates are polynomial-time rational computations. Arbitrary unencoded real coordinates are not a Turing-machine input model; a real-RAM or order-type oracle formulation would have to be stated separately.

The elementary bound `N(P)≤(n−1)!/2` gives only `O(n log n)` answer bits. Exponentially many polygons do **not** create an exponential output-length obstruction to returning their count.

Membership in `#P` follows directly: guess one fixed-length binary encoding of a canonical permutation, reject invalid encodings, and test simplicity. Every counted polygon has exactly one accepting encoding; validation uses polynomial time and polynomial-bit exact arithmetic. This membership statement is not a hardness result.

On general-position inputs, `N(P)` depends only on the orientation signs of triples, since those signs determine every proper crossing. This fact also makes nonsingular affine transformations and relabelings useful tests.

## 2. Source and current-literature check

The following are source-attributed facts, not independently reverified implementations of the cited algorithms.

- TOPP p16 remains marked open, with an entry revision dated 18 June 2025. It distinguishes monotone special cases and random generation from the general counting question [1].
- Marx and Miltzow explicitly include noncrossing Hamiltonian cycles in their `n^{O(sqrt(n))}` counting framework: conference Theorem 6 and full-version Theorem 8 [2]. The coefficient `11+o(1)` belongs to their triangulation theorem; we do not assert it for arbitrary graph families. Their full version also excludes four cocircular points in its general-position assumptions. Their constrained-Delaunay completion and annotation machinery supplies substantially more than naive triangulation double counting. We have not reproduced its full proof, perturbation/tie handling, or bit-complexity implementation.
- Wettstein gives an exponential-time counting framework for spanning cycles, with a stated base below 5.61804 and a polynomial factor [3]. This does not settle polynomial-time exact counting.
- Eppstein’s 2024 journal paper gives output-polynomial enumeration and a polynomial-time approximation of the logarithm of the count. Its conclusion still asks about `#P`-completeness and discusses `n^{O(k)}` algorithms and the stronger FPT question [4]. Neither output-polynomial listing nor a logarithmic approximation is an exact polynomial-time counter.
- The `#P`-completeness result in *Counting Polygon Triangulations is Hard* concerns triangulations of polygons with holes, under Turing reductions. Its conclusion explicitly distinguishes the unresolved counts of noncrossing structures on unconstrained point sets [5]. It cannot be used as a hardness theorem for this target.
- A 2025 workshop contribution on reachability-based Hamiltonian-path enumeration studies pruning and experiments, while a 2026 paper concerns drawings of a fixed combinatorial triangulation [6,7]. The inspected statements do not resolve this exact-counting problem. These were scope checks, not full proof audits.

Bounded searches through 8 October 2026 did not locate a full resolution. That is not a certification of exhaustive coverage, worldwide openness, or priority. No raw AI claim is used as a theorem. The overlapping exact-counting component of the older random-polygon question is the same target; uniform sampling, extremal counts, and other graph families are outside this report.

## 3. Approach A: compress partial paths into subset/endpoints

### Proposed recurrence

A natural plan is a Held–Karp-style recurrence whose state stores a visited subset `S`, a fixed starting vertex `s`, and a final vertex `t`. In ordinary graph path counting, appending a vertex depends only on the final vertex and the unused set. Here a newly appended segment must avoid the entire earlier path. There are already exponentially many subset states; even this exponential-size baseline needs more information before any further compression could help.

### Exact obstruction

Use the six points

`p0=(0,0), p1=(12,0), p2=(13,10), p3=(0,13), p4=(2,3), p5=(7,5)`.

The two noncrossing paths

`A=(0,1,4,2)` and `B=(0,4,1,2)`

have the same visited set `{0,1,2,4}`, start `0`, and end `2`. Only vertices `3,5` remain.

Neither completion of A is simple:

- In `(0,1,4,2,3,5)`, edges `42` and `35` cross.
- In `(0,1,4,2,5,3)`, the same undirected edges `42` and `35` cross.

For the first ordering of these two segments, the four orientation determinants are `124,−13,−54,83`. The opposite signs on both lines certify the proper crossing.

B has exactly one completion:

- `(0,4,1,2,3,5)` has crossing edges `41` and `50`, with determinants `35,−36,−11,60`.
- `(0,4,1,2,5,3)` is simple: every pair of nonincident edges is disjoint, as verified by exact determinants.

Thus the continuation counts are 0 and 1. Any recurrence that regards **each path in this state as having the same future behavior** is invalid. A scalar count of prefixes cannot be multiplied by a state-only continuation count.

One valid recursion retains the entire ordered prefix, branches over unvisited vertices whose new edge meets no earlier edge, and finally checks the closing edge. It gives finite exact enumeration, but has no polynomial state bound.

### Exact remaining gap

The example rules out only this specific sufficient-state assertion. It does not prove that all subset DPs, aggregate summaries, or alternative encodings need exponentially many states. A polynomial-size geometric summary with correct transitions remains unsupported here.

## 4. Approach B: sum over triangulation completions

Let `T(P)` be the triangulations of the point set, `H(T)` the Hamiltonian cycles in a triangulation `T`, and

`e(Q)=#{T in T(P): E(Q) is a subset of E(T)}`.

Every polygonalization extends to at least one triangulation: add hull edges and triangulate the regions without crossing the polygon. Double counting pairs `(Q,T)` proves

`sum_T |H(T)| = sum_Q e(Q)`.

A weighted identity is also immediate:

`N(P) = sum_T sum_(Q in H(T)) 1/e(Q)`.

The denominator depends on the polygon. Neither identity supplies a fast algorithm by itself.

### Nonuniform multiplicity on one fixed point set

Take

`p0=(0,0), p1=(12,0), p2=(0,13), p3=(2,3), p4=(5,2)`.

The hull is the triangle `012`. Among all segments, the only proper crossing pair is `13` with `24`. A triangulation has `3n−h−3=9` edges. Consequently there are precisely two triangulations:

- `T1=K5−{24}`
- `T2=K5−{13}`

There are 12 undirected Hamiltonian cycles in `K5`; exactly 4 contain both of the crossing edges. Hence there are 8 polygonalizations. Each `Ti` has 6 Hamiltonian cycles, so the incidence sum is 12.

More specifically:

- `Q1=(0,1,2,3,4)` avoids both `13` and `24`, and has `e(Q1)=2`.
- `Q2=(0,1,2,4,3)` contains `24`, and has `e(Q2)=1`.

In fact four polygons have multiplicity 1 and four multiplicity 2. This disproves the proposed uniform extension count. Dividing the incidence sum by the number of triangulations gives 6 rather than 8; a universal object-by-object multiplicity does not exist even for this one input. Nor can a divisor depending only on n work for all point sets: a convex five-point set has one polygon and five triangulations, giving incidence/count ratio 5 rather than 12/8.

### Canonical completion and connectivity

Choosing a deterministic unique completion removes the multiplicity logically, but still requires counting only polygons whose chosen completion is the current triangulation. That is an additional nontrivial constraint, not an ordinary unweighted sum. Likewise, degree-two subgraphs can consist of several cycles; enforcing one connected spanning cycle cannot be omitted in a determinant or matching-based approach.

### Exact remaining gap

The attempted simplification yields no polynomial-time summation or canonical-completion recognizer that makes the whole count tractable. The established subexponential annotation method [2] does address unique completion, but is not a polynomial-time result. The example is not a hardness theorem for counting inside triangulations or for any other algorithm.

## 5. Approach C: remove crossings by inclusion–exclusion

Let `X(P)` consist of all unordered pairs of disjoint-endpoint edges that cross properly. For `A⊆X(P)`, let `F(A)` be the union of the edges appearing in these pairs. Define `h_n(F)` to be the number of undirected Hamiltonian cycles in the complete abstract graph `K_n` containing every edge of `F`.

### Theorem: exact crossing formula

For a general-position point set,

`N(P) = sum_(A⊆X(P)) (−1)^|A| h_n(F(A))`.

**Proof.** Sum the expansion of the product of `(1−I_x)` over all abstract Hamiltonian cycles, where `I_x` records that both edges of crossing pair `x` occur in the cycle. Each crossing-free cycle contributes 1, and each cycle with at least one crossing contributes 0. Exchanging the finite sums gives the formula. General position matters: otherwise forbidden contacts and overlaps are not exhausted by proper crossing pairs. ∎

### Lemma: each forced-edge term has a closed form

Assume `n≥3` and `F` is a simple undirected graph on the `n` vertices.

1. If some vertex has degree greater than 2, then `h_n(F)=0`.
2. If a connected component of `F` is a cycle, then `h_n(F)=1` when it is a spanning cycle, and 0 otherwise.
3. Otherwise `F` is a disjoint union of paths and isolated vertices. Let `e=|F|`, `m=n−e`, and let `p` be the number of path components containing an edge. Then

   `h_n(F) = 2^p (m−1)! / 2`.

**Proof.** The first two assertions follow from degree two and connectedness of a Hamiltonian cycle. In the third case, every nontrivial path must appear consecutively in any containing cycle. Contract all path components to blocks; there are `m` blocks. Choose a cyclic ordering of the blocks, and orient each of the `p` nontrivial paths. There are `(m−1)! 2^p` oriented constructions. Reversal acts without fixed points on the full oriented Hamiltonian cycle, so divide by 2. This remains valid for `m=1`, when the sole block is a spanning path, and for `m=2`; `n≥3` excludes the exceptional two-singleton situation. Expanding the blocks recovers exactly the original containing cycles. ∎

This reduces each term to a polynomial-time graph check and factorial, but leaves exponentially many subsets.

### Why discarding zero terms alone does not fix the expansion

Put `n=4r` points in strictly convex position, divide them into `r` consecutive groups of four, and select the crossing diagonal pair within each group. Every subset of these `r` events forces a matching, so every one of its `2^r` terms has positive `h_n`. Therefore a method that explicitly expands all nonzero terms still processes exponentially many terms, even though this convex instance has `N(P)=1`.

This is a limitation of explicit expansion, not a lower bound for symbolic cancellation or exact counting. The convex example itself has a trivial closed answer.

### Exact remaining gap

No polynomial-time method is obtained for aggregating the signed terms over arbitrary order types. The identity is an exact specification and a small-instance cross-check, not an improved worst-case algorithm.

## 6. Approach D: transfer hardness from graph Hamiltonian counting

A sparse graph specifies which edges may be used. A general-position point set provides every segment joining two input points; it does not contain an arbitrary allowed-edge mask. Mapping graph vertices to points and ignoring the mask changes the problem.

An attempted direct gadget reduction would need to eliminate every undesired geometric polygon while preserving the desired graph cycles, with a controlled count. There is a simple obstruction to the most literal version.

### Positivity lemma

Every general-position point set of at least three points has a polygonalization.

**Proof.** Among the finitely many abstract Hamiltonian cycles, choose one of minimum Euclidean length. If edges `ab` and `cd` cross, delete them and use the uncrossing reconnection that leaves one Hamiltonian cycle. Each replacement length is strictly smaller than the corresponding two broken segments through the intersection, and their sum is strictly smaller than `|ab|+|cd|`. Strictness follows because the intersecting lines are distinct and endpoints are in general position. This contradicts minimality. There are no remaining non-proper contacts in general position, so the minimizing cycle is simple. This is an existence proof and does not require a polynomial-time TSP algorithm. ∎

### Corollary: a particular parsimonious reduction is impossible

Let `f` be a counting problem with at least one zero-valued input. There is no map whose outputs are always valid general-position point sets with at least three points and that satisfies `f(x)=N(P_x)` for every input. At a zero-valued input it would equate zero with a positive integer. The same argument excludes a positive multiplicative factor alone.

This unconditional statement concerns a promise-preserving, count-preserving map. It **does not** exclude reductions using subtraction of a baseline, interpolation, multiple oracle calls, or a larger domain with efficiently recognizable zero-count instances. Positivity is compatible with `#P`-hardness under more general reductions.

Hardness of minimizing area or length also supplies no such reduction by itself. A count contains no objective values. Recovering an optimum from an unweighted count would require an additional construction connecting objective restrictions to queries on permitted point-set instances.

### Exact remaining gap

No geometric gadget family and no reconstruction formula meeting those requirements has been constructed here. This route yields a restricted reduction obstruction, not tractability and not a refutation of `#P`-hardness.

## 7. Approach E: parameterize by points inside the hull

Assume general position. Let `h` points be hull vertices and `k=n−h` points lie strictly inside the hull, with `h≥3`.

### Hull-order lemma

Every simple polygonalization visits the hull vertices in their hull cyclic order or its reverse.

**Proof.** The polygon lies in the convex hull. Consider the polygon arc between two hull vertices consecutive in the polygon’s restricted hull-vertex sequence. Its interior contains no hull vertex and lies in the interior of the hull, unless the arc is a hull edge. If its endpoints are not hull neighbors, this simple arc is a crosscut of the convex disk. The two open boundary arcs between its endpoints each contain hull vertices. Removing the endpoints, the complementary polygon arc is connected, disjoint from the crosscut, and would have to visit both sides of it, which is impossible by the Jordan separation property. Hence consecutive hull vertices in the polygon are hull neighbors. Their cyclic order is therefore the hull order up to reversal. ∎

### Exact hull-gap algorithm

Fix the counterclockwise hull order `(v0,...,v_(h−1))`. Choose an ordering of all `k` interior points and a weak composition `(a0,...,a_(h−1))` of `k`. Insert the first `a0` interior points after `v0`, the next `a1` after `v1`, and so on. Test the resulting cycle for simplicity.

There are exactly

`k! binomial(k+h−1,k) = k! binomial(n−1,k) = (n−1)!/(h−1)!`

candidates. Each polygon has exactly one counterclockwise-hull representation and exactly one such ordered-list/composition pair. The algorithm therefore counts it once.

Each simplicity test takes `O(n²)` exact geometric predicates; preprocessing and rational arithmetic add polynomial factors in input bit size. The candidate count is at most `n^k`. Thus this gives `n^{k+O(1)}` time with polynomial-bit arithmetic, polynomial for every fixed `k`.

For `k=0`, there is exactly one polygon, the hull boundary. For `k=1`, each insertion into one of the `h` hull edges is simple, and every polygon is such an insertion; hence `N(P)=h=n−1`.

### Exact remaining gap

When `h=3`, the candidate count is `(n−1)!/2`, precisely the number of all undirected abstract Hamiltonian cycles. The parameter is not bounded in the original question. No uniform polynomial-time algorithm, and no improvement to an `f(k) n^{O(1)}` bound, is proved. This elementary parameterization is a known-type partial direction, consistent with the stronger discussion in [4], not a claimed new result.

## 8. Reproducibility and limitations

`check_counting.py` uses Python’s standard library and exact integers/Fractions. It makes no network requests and writes no files. Its mathematical checks use explicit exceptions rather than `assert`, so optimization cannot remove validation.

The program compares:

- canonical-permutation enumeration with independent degree-two connected edge-subset enumeration on inputs of at most six points;
- direct counting with the inclusion–exclusion formula where there are at most 18 crossing events;
- direct counting with hull-gap enumeration;
- the forced-edge formula with all 1,096 edge subsets of `K3`, `K4`, and `K5`;
- the explicit continuation and triangulation-incidence examples;
- affine, rational-rescaling, and relabeling invariance.

Both enumeration routes use the same exact segment predicates. This is not independent implementation of every geometric primitive; independent review should inspect those predicates and the short determinant certificates above.

The limits are intentional: at most nine points, exact input coordinates of at most 64 numerator/denominator bits, at most six points for edge-subset/triangulation enumeration, and at most 18 inclusion–exclusion events. Invalid types, Boolean/float coordinates, duplicate points, excessive sizes, and inappropriate degeneracies are rejected. The demonstration harness also requires UID 1000, matching its recorded verification environment.

The checker passes under ordinary Python, `python -O`, and `python -OO`, as recorded in `VALIDATION.md`. The output contains synthetic mathematical fixtures, not source datasets. No cited source PDFs, copied source text, or private data are distributed with this note.

## 9. Final assessment

The exact unrestricted counting problem remains unsettled here. The polynomial-time special cases, `#P` membership, identities, and small counterexamples do not determine whether `N(P)` is polynomial-time computable. The two algorithmic paths need a fundamentally stronger aggregation mechanism; the hardness path needs a genuine geometric reduction with controlled counts. No claim of full resolution, novelty, or exhaustive literature coverage is made.

## References

[1] The Open Problems Project, [Problem 16: Simple Polygonalizations](https://topp.openproblem.net/p16). Maintained entry inspected 8 October 2026.

[2] Dániel Marx and Tillmann Miltzow, [Peeling and Nibbling the Cactus: Subexponential-Time Algorithms for Counting Triangulations and Related Problems](https://doi.org/10.4230/LIPIcs.SoCG.2016.52), SoCG 2016, 52:1–52:16. [Full version, arXiv:1603.07340](https://arxiv.org/abs/1603.07340).

[3] Manuel Wettstein, [Counting and Enumerating Crossing-free Geometric Graphs](https://doi.org/10.20382/jocg.v8i1a4), Journal of Computational Geometry 8(1), 47–77 (2017). [Author manuscript, arXiv:1604.05350](https://arxiv.org/abs/1604.05350).

[4] David Eppstein, [Non-crossing Hamiltonian Paths and Cycles in Output-Polynomial Time](https://doi.org/10.1007/s00453-024-01255-y), Algorithmica 86, 3027–3053 (2024). [Earlier preprint, arXiv:2303.00147](https://arxiv.org/abs/2303.00147). The journal HTML, rather than the earlier preprint conclusion, was used for the parameterized-complexity and `#P` questions.

[5] David Eppstein, [Counting Polygon Triangulations is Hard](https://arxiv.org/abs/1903.04737), inspected v2, 20 March 2020; published in Discrete & Computational Geometry 64, 1210–1234 (2020), [DOI](https://doi.org/10.1007/s00454-020-00251-7).

[6] Randal Tuggle and Jack Snoeyink, “Enumerating Non-Crossing Hamiltonian Paths by Reachability Checks and Bidirectional Search,” dated 19 October 2025, in the [FWCG 2025 abstract booklet](https://www.cs.qc.cuny.edu/goswami/Abstracts-FWCG-25.pdf), PDF pages 42–47.

[7] Belén Cruces, Clemens Huemer, and Dolores Lara, [On the Number of Drawings of a Combinatorial Triangulation](https://doi.org/10.1007/s00373-026-03010-2), Graphs and Combinatorics 42, article 16 (2026).
