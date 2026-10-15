# A quasilinear algorithm for multiplicatively weighted centers of median graphs

Problem 30006605 (OWR-14299911-007), rank 598. Author-stage complete candidate, 2026-10-04. One substantive attempt; independent audit pending. This note makes no historical-priority claim.

## 1. Exact question and answer

Let G=(V,E) be a finite, nonempty, connected, simple median graph, with unweighted edges and n vertices. A graph is median when each triple of vertices has a unique vertex lying on shortest paths between all three pairs. Let w:V→R_{≥0} be a multiplicative vertex profile, and define

    r_w(x) = max_{u∈V} w(u)d_G(x,u).

The target is to find a vertex minimizing r_w in almost-linear time when the largest induced cube has bounded dimension. The source is Guillaume Ducoffe, “Radius functions in median graphs,” Oberwolfach Report 8/2026, definition on p. 504 and Open problem 1 on p. 505; the report distinguishes this from arbitrary edge weights.

**Theorem.** On the usual exact arithmetic/comparison model for real input weights, a center, the optimum value, and the entire set of centers can be computed deterministically in O(n log^5(2n)) time for every finite median graph. No bound on cube dimension is required.

Here arithmetic involving input weights only multiplies them by integers between 0 and n−1 and compares the results. In particular, the claim is not a bit-complexity bound independent of the encoding length of arbitrary real numbers. Rational inputs can be handled exactly; see §6.

## 2. Explicit prior theorem

We use the following published algorithmic result, not a theorem proved anew here:

**Additive eccentricity oracle [BDH].** For a median graph and a nonnegative integer vertex function a, all values

    E_a(x) = max_{u∈V} (d_G(x,u)+a(u))

can be computed in O(n log^4(2n)) time.

Reference: Pierre Bergé, Guillaume Ducoffe, and Michel Habib, “Quasilinear-time eccentricities computation, and more, on median graphs,” SODA 2025, pp. 1679–1704, DOI https://doi.org/10.1137/1.9781611978322.52. The precise input/output definition is on p. 2 of https://arxiv.org/pdf/2410.10235v1; Theorem 1 is on p. 3 and is proved using Algorithm 1 and Theorems 3–4 on pp. 22–24. It is additive weighting, not a multiplicative center algorithm. Our calls use only a(u)∈{0,…,n−1}.

There is also a credited prior decision-to-optimization reduction: Guillaume Ducoffe, “Beyond Trees: The Weighted Center Problem on Gromov Hyperbolic Graphs,” ESA 2026, DOI https://doi.org/10.4230/LIPIcs.ESA.2026.133, Lemma 2 on pp. 133:6–133:7; full version https://arxiv.org/abs/2607.04287, Lemma 2.2. It gives an O((T(n,m)+n)log n) optimization algorithm from a T-time threshold oracle. We give a slightly slower, comparison-only variant in §4 for a self-contained reduction and exact reproducibility. The weighted-median mechanism is not claimed as new.

## 3. Multiplicative thresholds become additive eccentricities

Set D=n−1. All graph distances are integers between 0 and D. For each threshold R≥0 define

    b_R(u) = max {k∈{0,…,D}: k w(u)≤R},
    a_R(u) = D−b_R(u).

The defining set for b_R(u) is nonempty because k=0 is permitted. This definition also covers zero weights: b_R(u)=D if w(u)=0. For positive w(u), it is min(D,floor(R/w(u))). No unbounded floor or division primitive is necessary: binary search among the D+1 integers finds b_R(u) in O(log(2n)) comparisons of k w(u) with R.

**Lemma 1 (pointwise threshold identity).** For every x∈V,

    r_w(x)≤R  iff  E_{a_R}(x)≤D.

**Proof.** For every u, the integer d_G(x,u) lies in [0,D]. Since w(u)≥0, the definition of b_R(u) gives

    w(u)d_G(x,u)≤R  iff  d_G(x,u)≤b_R(u)
                            iff  d_G(x,u)+a_R(u)≤D.

This remains valid for w(u)=0, because both restrictions are vacuous: d_G(x,u)≤D. Taking the conjunction over every u proves the equivalence. ∎

**Corollary 2 (feasibility and witnesses).** Given R≥0, form a_R, call [BDH] once, and scan its n outputs. The set

    F_R = {x:E_{a_R}(x)≤D}

is exactly {x:r_w(x)≤R}. Thus we can either return a feasible vertex or certify infeasibility in O(n log^4(2n)) time. If R<0, every vertex is infeasible because r_w≥0.

Crucially, the graph is unchanged: no subdivision, extra vertices, representation as a product of trees, convexity of balls, or local-unimodality assumption is introduced. The zero-weight vertices remain available as centers and as graph vertices. No actual pairwise-distance table is constructed by this algorithm.

## 4. Searching an implicit quadratic candidate set

Let ρ=min_x r_w(x). For each x, its maximum is attained at some vertex u, so r_w(x)=k w(u) for some integer k∈[0,D]. Consequently

    ρ ∈ S = multiset {k w(u):u∈V, 0≤k≤D}.

There are n² entries, but we never enumerate them. Each u contributes a nondecreasing row indexed by k. Repeated values, including entire zero rows, cause no difficulty.

For completeness, the following algorithm optimizes using any correct feasibility oracle, not only one for median graphs.

1. If n=1, return its vertex, value 0, and its singleton center set.
2. Initialize a feasible incumbent B=D max_u w(u), with an arbitrary vertex as witness. Its radius is at most B by the distance bound. If B=0, all vertices are centers and we are done.
3. In every row retain an inclusive integer interval [l_u,h_u], initially [0,D]. An empty interval has l_u>h_u. Let L_u=h_u−l_u+1 for nonempty rows, and M=Σ_u L_u.
4. While M>0:
   - For every nonempty row set m_u=floor((l_u+h_u)/2), q_u=m_u w(u), and give q_u selection weight L_u.
   - Choose a weighted median q of the q_u: the total weight of entries with q_u≤q and the total weight of entries with q_u≥q are both at least M/2. Sorting at most n midpoint values and scanning cumulative weights does this in O(n log(2n)) comparisons, with ties retained in the cumulative scan.
   - Query feasibility at q.
   - If feasible, save B=min(B,q), saving a corresponding witness when B decreases (or retaining the old witness if B is unchanged). In every active row discard all entries ≥q, using a binary-search lower bound for the first k with k w(u)≥q. Keep only entries <q.
   - If infeasible, in every active row discard all entries ≤q, using a binary-search upper bound for the first k with k w(u)>q. Keep only entries >q.
5. When no entries remain, return B and its feasible witness. One final feasibility call at B returns the entire center set.

An equivalent implementation may replace B by q whenever feasibility is true: active feasible pivots necessarily strictly decrease after the first feasible pivot. The min version makes the invariant transparent without that observation.

**Lemma 3 (correctness).** The algorithm returns the optimum.

**Proof.** Initially B is feasible and ρ occurs in an active row. Maintain: B is feasible, and either B=ρ or at least one active entry equals ρ. Suppose a query q is feasible. Then ρ≤q. If ρ=q, saving q establishes B=ρ. If ρ<q, every entry equal to ρ survives the strict-less-than pruning. If q is infeasible, then ρ>q; every entry equal to ρ survives the strict-greater-than pruning. The invariant is preserved. At termination no active entry exists, so B=ρ. Its saved witness has radius at most B=ρ and hence is a center. The feasible set F_B is precisely the center set. ∎

**Lemma 4 (constant-factor progress).** Every iteration removes at least M/4 entries, counting multiplicities.

**Proof.** In a row of length L_u, at least L_u/2 entries are ≤q_u and at least L_u/2 entries are ≥q_u, because q_u is a middle entry and the row is nondecreasing. If q is infeasible, consider the rows with q_u≤q. Their combined row lengths are at least M/2 by the weighted-median property. At least half their entries are ≤q_u≤q, so at least M/4 entries are removed. If q is feasible, use instead the rows with q_u≥q: at least half of their entries are ≥q_u≥q and removed. This proof also covers singleton rows and equal midpoint values; no strict-monotonicity assumption is used. ∎

Initially M=n². Since M is a nonnegative integer and M_next≤3M/4 whenever M>0, there are O(log(2n)) iterations. Computing a weighted median and pruning all row intervals costs O(n log(2n)) time per iteration, and requires O(n) active-row storage. Thus any T(n,m)-time witness-producing feasibility oracle yields total time

    O((T(n,m)+n log(2n)) log(2n)).

This is deliberately weaker than Ducoffe's credited O((T+n)log n) lemma, but avoids any constant-time floor/division assumption and is sufficient here.

## 5. Completion of the theorem

Use Corollary 2 for each feasibility query in §4. Its time is T(n,m)=O(n log^4(2n)), including construction of a_R and scanning labels. There are O(log(2n)) calls, plus one final call to recover all centers. Sorting/pruning overhead is O(n log²(2n)). The total is O(n log^5(2n)). Median graphs have O(n log n) edges, so reading their adjacency lists is also within this bound. In bounded cube dimension d, m≤dn; no embedding need be supplied. The theorem answers the finite algorithmic interpretation of the exact workshop question affirmatively. ∎

## 6. Scope, arithmetic, dependencies, and limitations

- The theorem concerns vertices of a finite input graph. The workshop's general definition allows infinite graphs with finite-support profiles, but its n-vertex running-time question does not specify an encoding for an infinite graph. We do not claim an algorithm for implicitly represented infinite median graphs or for continuous centers in cube complexes.
- Edge lengths are all 1. Arbitrary edge-weighted median graphs are a separate question in the workshop report, and are not covered.
- Nonnegative finite real profile values are permitted in an exact comparison model. For rational input p_u/q_u of at most B bits, each comparison k w(u)≤j w(v) is an exact comparison of k p_u q_v and j p_v q_u, with O(B+log n) bit operands. There are O(n log²(2n)) input-weight comparisons; bit costs multiply these comparisons by the cost of integer arithmetic. The center index and optimum value (as k w(u)) require no approximation.
- The [BDH] calls only receive O(log n)-bit nonnegative integers. No claim that arbitrary real input is encoded in constant space is needed. A precise bit implementation of [BDH] is not reconstructed here.
- The public control program supplies an explicitly quadratic reference implementation of the additive oracle, and an independent linear-time tree oracle. It tests the new reduction and implicit search exactly; it does not implement the fast median-graph [BDH] algorithm or experimentally verify its asymptotic bound.
- The complexity theorem therefore depends on [BDH] as an imported mathematical theorem. It is not conditional on an unproved conjecture, but independent review should verify that theorem's exact domain and interface. Its full proof is not reproduced.
- No novelty claim is made for the additive algorithm or weighted-median search. This note isolates a short threshold transformation and their consequence. The source workshop still lists the question as open in February 2026. A later published search lemma already supplies the optimization step. Whether this precise consequence was previously recorded requires a separate priority check.

## References

[OWR] G. Ducoffe, “Radius functions in median graphs,” in *Median Geometry and Applications*, Oberwolfach Reports 8/2026, pp. 504–507. https://doi.org/10.4171/OWR/2026/8

[BDH] P. Bergé, G. Ducoffe, M. Habib, *Quasilinear-time eccentricities computation, and more, on median graphs*, SODA 2025, pp. 1679–1704. https://doi.org/10.1137/1.9781611978322.52 ; precise public full text https://arxiv.org/abs/2410.10235v1

[D26] G. Ducoffe, *Beyond Trees: The Weighted Center Problem on Gromov Hyperbolic Graphs*, ESA 2026, 133:1–133:19, Lemma 2. https://doi.org/10.4230/LIPIcs.ESA.2026.133 ; full version Lemma 2.2, https://arxiv.org/abs/2607.04287v1
