# Turn 1: exact marginals, two scoped positive results, and failed stronger mechanisms

2026-10-02. First substantive author turn for 30003338 / OWR-15206-017. **Original target unresolved, 1/5.** The results below do not prove association for arbitrary bipartite graphs and do not give a counterexample. No novelty claim is made for the scoped consequences of classical correlation inequalities.

## 1. An exact finite marginal and success criterion

Let G have bipartition A,B and q ≥ 3. For a color assignment g:A→{0,…,q−1}, the number of proper extensions to B is exactly

    W(g) = product_(b in B) (q − |g(N(b))|).                    (1)

Indeed the colors at different B vertices are conditionally independent and every color used among their A-neighbors is forbidden. Thus the unnormalized weight of an exact zero set S⊂A is

    w(S) = sum_(g: g^(-1)(0)=S) W(g).                         (2)

This counts every proper coloring once. Isolated B vertices and B vertices of degree one contribute constants q and q−1, respectively, so they have no effect on the normalized marginal. Repeated B neighborhoods must not be discarded: their factors multiply.

For an upward-closed family U⊂2^A, put Z_U=sum_(S in U) w(S), and Z=sum_S w(S). The full target is equivalent to

    Z_(U intersection V) Z ≥ Z_U Z_V                         (3)

for every pair of upward-closed families U,V. On a finite partially ordered set, every increasing real function is a constant plus a nonnegative linear combination of indicators of its increasing superlevel sets; bilinearity of covariance proves the equivalence. Thus checking only principal upsets is not enough in general.

## 2. A self-contained reduction for every forest

**Proposition.** If G is a forest, the zero-set marginal on either bipartition class satisfies the FKG lattice condition, and hence positive association, for every q ≥ 3.

Let n=|V(G)|, m=|E(G)|, and d_v be each degree. A full zero set R⊂V(G) must be independent. If it is, the remaining graph G−R is a forest with

    m_R=m−sum_(v in R)d_v,
    c_R=n−|R|−m_R

edges and components. These formulas include isolated vertices and the empty remaining graph. A forest with e edges and c components has (q−1)^c(q−2)^e proper colorings using the q−1 nonzero colors. Therefore the number of proper q-colorings with exact zero set R is

    C product_(v in R) lambda_v,
    C=(q−1)^(n−m)(q−2)^m,
    lambda_v=(q−1)^(d_v−1)/(q−2)^d_v,                         (4)

when R is independent, and zero otherwise. All lambda_v are strictly positive. This is an exact hard-core measure with vertex-dependent activities, not an approximation to the coloring law.

Summing (4) over the B part gives, for S⊂A,

    w(S)=C product_(a in S) lambda_a
             product_(b: N(b) intersection S is empty) (1+lambda_b). (5)

The first product is log-modular. For each b, the indicator h_b(S) of S avoiding N(b) is supermodular:

    h_b(S intersection T)+h_b(S union T) ≥ h_b(S)+h_b(T).

If both or exactly one of S,T avoid N(b), equality holds; if neither avoids it, the right side is zero and the inequality holds. Taking logs in (5) proves

    w(S intersection T)w(S union T) ≥ w(S)w(T).

The classical finite FKG inequality gives association. The proof works for disconnected forests by the same formulas, including isolated vertices and an empty bipartition class. This is a scoped consequence of standard hard-core/FKG ideas, not a full solution.

## 3. Every graph with degree at most two on the integrated-out side

**Proposition.** If every b∈B has degree at most two, then the requested A-marginal is positively associated for every q ≥ 3, even when G has cycles.

Discard the constant factors from degrees zero and one in (1). Each degree-two b with distinct neighbors a,a' contributes

    (q−2)+1_(g(a)=g(a')).                                    (6)

Hence g has exactly the law of a ferromagnetic q-state Potts model on the multigraph H on A having one edge for each such b. Parallel edges can instead be collapsed into the corresponding product interaction. After dropping positive constants, each edge weight is

    1 + t 1_(g(a)=g(a')),    t=1/(q−2)>0.

Expand the product over edges. Given the selected edge set η, the assignment g is constant on each connected component, with its q labels independent and uniform between components. The marginal weight of η is proportional to

    t^|η| q^(number of components),

which is the random-cluster model with edge probability p=t/(1+t)=1/(q−1). Thus the fixed-color indicator is exactly its fractional fuzzy Potts model, with a component marked 1 with probability 1/q independently.

Kahn–Weininger, *Positive association in the fractional fuzzy Potts model*, Ann. Probab. 35 (2007), 2038–2043, Theorem 1, proves association whenever the random-cluster parameter is at least 1. It applies here with parameter q and marking probability 1/q. The primary theorem and its hypotheses were checked directly: https://arxiv.org/pdf/0711.3136 . This is an explicit reduction to a credited published theorem, rather than a new proof of that theorem or a claim that degree-two cases settle the source target.

## 4. Exact obstruction to extending this local random-cluster mechanism

Already one B vertex of degree three produces an obstruction. For its three neighboring colors let δ_ij indicate equality, and δ_123 indicate all three equal. Its extension count has the unique partition-indicator expansion

    q − number of distinct colors
      = (q−3) + δ_12 + δ_13 + δ_23 − δ_123.                 (7)

Verification on the five equality patterns proves (7). The coefficient of each pair equality must be 1 after evaluating the corresponding two-equal pattern; evaluating the all-equal pattern then forces the all-equal coefficient to be −1. The equality-pattern indicators form a basis for these five pattern values when q≥3.

Consequently a single degree-three factor cannot be represented as a nonnegative linear combination of these equality-partition constraints. The direct local ferromagnetic random-cluster expansion used in Section 3 therefore fails. This does not rule out a nonlocal representation, a different coupling, or association itself.

Separately, the fixed-color marginal need not satisfy the FKG lattice condition: the nine-vertex dreidel example is already in Peled–Spinka, arXiv:2001.11566v2, pp. 48–49. Its published conditional probabilities 23/56 > 9/22 are reproduced below. That stronger-condition failure is not a target counterexample. In fact the complete increasing-event check here verifies positive association for this particular graph at q=3.

## 5. Exact finite controls and their bounds

The portable C++ checker evaluates (1)–(3) with integer arithmetic. Its upward-closed truth tables are generated recursively: a monotone Boolean function on n coordinates is uniquely a pair (f_0,f_1) of monotone functions on n−1 coordinates with f_0≤f_1. This yields all 168 upsets on four coordinates and all 7,581 on five coordinates. It checks every unordered pair, including repetitions, not only conjunctions.

The complete finite search covers:

- A of size four; for each of the eleven nontrivial neighborhoods of sizes 2,3,4, either zero or one B vertex with that neighborhood
- All 2^11=2,048 choices, at each q=3,4,5,6,7,8: 12,288 graph/q cases
- All 174,440,448 increasing-event pairs across these cases
- The published nine-vertex dreidel graph at q=3, with A coordinates (u,v,w,left-top,right-top) and B-neighborhood masks (25,14,22,6)
- All 28,739,571 increasing-event pairs for the dreidel, whose total proper-coloring count is 336

Every tested covariance numerator is nonnegative. This certifies only the stated finite cases. Graphs with repeated nontrivial B neighborhoods, more A vertices, or other q are not covered by this enumeration. Arbitrarily many degree-zero/one B vertices do not change any tested normalized marginal.

Counts and event masses use signed 64-bit integers; covariance products use signed 128-bit integers. In the A=4 sweep there are at most 15 total vertices and q≤8, so every count is at most 8^15=2^45 and every product at most 2^90. The smaller dreidel case also lies inside these bounds. Thus the comparisons have no floating-point tolerance or integer-overflow ambiguity.

A separate Python checker directly enumerates all proper colorings of every forest subgraph of K_(3,3) at q=3,4, checks (4), (5), and all marginal lattice inequalities, and independently reconstructs the dreidel weights. Its 656 forest graph/q cases give 89,220 exact assertions including the dreidel controls. These finite tests corroborate the two written reductions; they do not replace the universal proofs of their scoped propositions.

Commands (Python 3, C++17 compiler; no third-party Python package needed):

    g++ -O2 -std=c++17 turn1_search.cpp -o /tmp/coloring_turn1_search
    /tmp/coloring_turn1_search
    python verify_turn1.py

The saved outputs are TURN_1_SEARCH.json and TURN_1_CHECKS.json. The Python checker uses the saved search output only to compare its independently generated 32 dreidel weights.

## 6. Remaining gap and next mechanism

No inequality for all increasing events on an arbitrary bipartite graph has been proved. The forest reduction and degree-two-side reduction do not cover general cyclic graphs with degree-three neighborhoods. The local positive random-cluster expansion and the ordinary FKG lattice route cannot simply be extended, for the exact reasons above. Small finite successes do not justify extrapolation.

A materially new next step is a direct Kempe-chain or two-copy coupling for arbitrary increasing events, or an exact counterexample search allowing repeated higher-degree neighborhoods and larger A, directed by a genuine association witness rather than lattice failure. A mixture of conditionally associated laws is not automatically associated; any latent-color argument must control the covariance of its conditional expectations rather than assume it away. The original target remains unresolved at 1/5.
