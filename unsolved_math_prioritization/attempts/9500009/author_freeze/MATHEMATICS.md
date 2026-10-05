# Exact formulation and partial results

## 1. Target and quantifiers

Let G_n=P_n square P_n, with vertices (i,j), 0<=i,j<n, and an edge precisely when
the Manhattan distance is one. There are N=n² vertices. A labeling L is a uniform
bijection V(G_n)->{1,...,N}. A vertex v is a peak when L(v)>L(w) for each neighbor
w. Corners and boundary vertices are included. Write K(L) for the number of peaks
and Q_n for the conditional law given K(L)=2. For n>=2 the conditioning event has
positive probability, as proved below. For n=1 it is impossible and Q_1 is not used.

Under Q_n let rho_n be the distance between the two peaks. Burdzy's Problem 9 asks
whether rho_n/n converges in distribution to the constant zero. Equivalently,

    for every epsilon>0,
    Q_n(rho_n >= epsilon*n) -> 0 as n -> infinity.             (1)

Using a strict instead of weak tail inequality gives the same limit criterion.
Since 0<=rho_n/n<2, this is also equivalent to E_Qn[rho_n/n]->0. For completeness,
Markov's inequality proves one implication. In the other direction split the
expectation over rho_n/n<=epsilon and its complement, obtaining an upper bound
epsilon+2 Q_n(rho_n/n>epsilon), then let n tend to infinity and epsilon to zero.
Convergence in distribution to a constant is equivalent to convergence in
probability. A negative answer requires some epsilon,delta>0 and infinitely many
n for which the tail probability in (1) is at least delta.

The primary source is [B]. Its spelling of the title is immaterial. Its displayed
question asks about convergence to zero; the title does not assert the answer.

## 2. Exact enumeration: peaks as births

This section applies to any finite nonempty graph G=(V,E). Write a labeling as its
decreasing-label placement order v_1,...,v_N, so that L(v_i)=N+1-i. Put
S_i={v_1,...,v_i}. A vertex v_i is a peak if and only if it has no neighbor in S_{i-1}.
Indeed, precisely the earlier vertices have larger labels. Thus a peak is a birth
in this growth order. This tracks the global condition exactly.

For an allowed set R of peak locations define F_R(S) to count orders of S in which
every vertex outside R has an earlier neighbor. Set F_R(empty)=1 and update

    F_R(S union {v}) += F_R(S)
    when v not in S and [v in R or N_G(v) intersects S].       (2)

Every order has a unique predecessor, obtained by deleting its last vertex; hence
induction proves the recurrence counts each valid order once. At S=V it counts
labelings whose entire peak set is a subset of R. In particular, for distinct a,b,

    W_G(a,b) = F_{a,b}(V)-F_{a}(V)-F_{b}(V)                  (3)

counts labelings with peak set exactly {a,b}. The subtracted classes are disjoint:
every labeling of a finite nonempty graph has a peak, namely its largest label.

A second recurrence counts exactly the desired root set without subtraction:

    E_R(empty)=1,
    E_R(S union {v}) += E_R(S)
    exactly when [v in R] iff [N_G(v) has empty intersection with S].  (4)

It follows directly from the birth characterization that E_R(V) is the exact-root
count. Recurrences (2)-(4) agree for all pairs in the recorded experiments.

For a separate check, let B(S,k) count orders of S having k births. Adding v not
in S increments k by 1 if N_G(v) misses S and by 0 otherwise. Then
sum_k B(V,k)=N!, and B(V,2)=sum_{a<b} W_G(a,b). The implementation verifies both
identities. An exhaustive comparison with permutations, using labels and direct
neighbor comparisons instead of growth orders, verifies every pair for n=2,3.

For each allowed R, (2) uses O(N*2^N) arithmetic operations and O(2^N) memory.
Running it for all pairs is O(N³*2^N). This is a finite algorithm, not a
polynomial-time or asymptotic spacing theorem. Counting peak sets on general
graphs is established territory; see [D]. No novelty is asserted for this method.

## 3. Exact results and their limits

Vertices are row-major, v=i*n+j. The following are integer numbers of labelings,
not Monte Carlo estimates. The count at distance one is zero in every case.

| n | distance 2 | distance 3 | distance 4 | distance 5 | distance 6 | total |
|---|---:|---:|---:|---:|---:|---:|
| 2 | 8 | 0 | 0 | 0 | 0 | 8 |
| 3 | 63,552 | 64,512 | 15,744 | 0 | 0 | 143,808 |
| 4 | 173,341,437,440 | 313,977,112,960 | 217,620,337,600 | 66,746,375,360 | 7,613,910,720 | 779,299,174,080 |

The conditional means E[rho_n/n] are 1, 666/749, and
377754599/463868556, approximately 1, 0.88919, 0.81436. The conditional probabilities
of rho_n>=n are 1, 418/749, and 101382161/270589991. The three values are not a
limit theorem, nor does a visually decreasing sequence establish any monotonicity
at larger n. All untested sizes remain untested.

Pair weights also depend on location, not only distance: on the 3x3 square,
W(0,2)=2688 whereas W(0,4)=5280, although both distances are two. Square symmetries
therefore do not imply full translation invariance or a radial weight formula.

## 4. Admissible peak sets and forest lower bounds

For any finite connected graph, its possible peak sets under the present definition
are exactly the nonempty independent vertex sets. Necessity follows from existence
of a global maximum and from the impossibility of adjacent strict local maxima.
For sufficiency, assign the highest labels to the roots R. Order every remaining
vertex by increasing distance from R and assign the remaining labels in decreasing
order, breaking ties arbitrarily. Each nonroot has a neighbor at smaller distance,
with a larger label; each root has a larger label than every neighbor. This proves
the assertion. On the squares here this agrees with the admissibility construction
in [D, Proposition 2.2]; their degree convention needs adjustment on graphs with
leaves, but every vertex of G_n has degree at least two for n>=2.

Consequently, every nonadjacent pair in G_n is possible, including pairs at distance
2n-2. This establishes support, not a nonvanishing asymptotic probability.

A quantitative lower bound comes from a rooted spanning forest T with two components,
roots a,b, and all its edges in G_n. Assume a,b are nonadjacent. Write s_v for the
size of the descendant subtree of a nonroot v, including v. Require the roots to
receive N and N-1, in either order, and every forest parent to exceed its children.
Every such labeling has exactly those two peaks, irrespective of the other edges.
The number of these labelings is

    2*(N-2)! / product_{v not in {a,b}} s_v.                 (5)

Proof of the counting formula: after deleting the two roots, the remaining forest
poset requires every root to precede its descendants. For a rooted tree, choosing
the relative positions of its child subtrees and applying induction gives the
hook-length count m!/product_v s_v. Interleaving the orders of several trees gives
the same formula for a forest. Apply it to the N-2 nonroots, then multiply by two
for the root labels. The descendant sizes of nonroots are unchanged when roots
are deleted.

The verifier builds a breadth-first forest for every admissible pair in the three
tested squares and checks its explicit labels and inequality (5)<=W_G(a,b).
These bounds count only a subset, with roots as the two highest labels. Two peaks
need not be the two highest-labeled vertices: the second-largest label can be
adjacent to the global maximum. Nothing here shows that (5) captures a substantial
fraction of all two-peak labelings uniformly as n increases.

## 5. Local independence and a rare-conditioning bound

Assign independent continuous uniform random variables U_v, then replace them by
their ranks. This produces a uniform labeling and preserves every peak event.
The unconditioned probability that v is a peak is 1/(deg(v)+1). Peak indicators at
vertices with disjoint closed neighborhoods are independent, because they depend
on disjoint collections of U_v. In particular,

    E[K(L)] = 4/3 + (n-2) + (n-2)²/5,  for n>=2.            (6)

Choose interior centers with both coordinates in {1,4,7,...} in zero-based
coordinates, stopping at n-2. There are m=floor(n/3)² such centers. Their closed
neighborhoods are pairwise disjoint and each center has degree four. Their number
of peaks is therefore X~Binomial(m,1/5). Since K(L)=2 implies X<=2,

    P(K(L)=2) <= (4/5)^m [1 + m/4 + m(m-1)/32].              (7)

The formula also holds for m=0 or 1. Thus the conditioning event is at most
polynomial(n) times exp(-c*n²) for some c>0 at sufficiently large n.

This independence is not preserved by conditioning on the global count. For the
opposite corners 0 and 8 on G_3, which have disjoint closed neighborhoods, the
exact conditional joint peak probability is 41/749. The product of its conditional
marginals is 130321/2244004. Their difference is -7485/2244004, not zero.
Both fractions are obtained from the full enumerated conditional population.
This is a direct counterexample to retaining local independence after conditioning.
It does not imply a sign theorem for all pairs or larger graphs.

An upper bound on the unconditional denominator cannot settle (1). To do so one
must compare distant two-peak labelings to all two-peak labelings on the same
exponentially small scale.

## 6. Completion-weighted growth, not uniform boundary growth

Suppose a decreasing-label prefix has occupied S and already created k births.
Let h(S,k) count completions with exactly two births in total, with h(V,2)=1 and
h(V,k)=0 for k!=2. With b(v,S)=1 if v has no neighbor in S and 0 otherwise,

    h(S,k) = sum_{v not in S} h(S union {v},k+b(v,S)).        (8)

Impossible k>2 states have value zero. Conditional on a feasible *specific* prefix,
the probability of the next vertex v is the corresponding summand divided by
h(S,k). This is because each remaining order is equally likely before conditioning,
and exactly the counted completions survive. The number of completions, rather than
the current boundary size alone, determines the transition.

Even one-peak growth on the actual square is not uniform on its available boundary.
On G_3, given the unique peak at 0 and descending prefix (0,1), the three possible
next boundary vertices 2,3,4 have respectively 156,180,336 valid completions. Their
probabilities are 13/56,15/56,1/2, not 1/3 each. The verifier computes these integers
by an independent recursive completion function. The general discrepancy between
uniform labeling and Eden growth is already illustrated in [BP, Example 2.1].

Formula (8) yields an exact conditional sampler when its full completion table is
available. Replacing that table by a spatial growth heuristic is an additional,
unproved change of measure. We have no uniform estimates for h that settle (1).

## 7. Cutting into blocks does not preserve the peak constraint

One might hope to restrict a two-peak square labeling to smaller squares and use
one-dimensional or fixed-graph results on each piece. Boundary maxima introduced
by restriction prevent a direct factorization. For example, the 4x4 labeling

    4   6   7  10
    12  5   1  16
    14 11  13  15
    3   2   8   9

has exactly two peaks, at row-major vertices 7 and 8. Its top-left 3x3 induced
subgraph has three peaks, at vertices 2,8,10 of the original indexing. Standardizing
the restricted labels to ranks does not change this. Direct neighbor comparisons
in the verifier certify both claims.

This example rules out the assertion that every block inherits at most the global
number of peaks. It does not rule out all coarse-graining arguments. Such an
argument needs new control of boundary-created peaks and of the coupling between
blocks. Fixed-metric-graph subdivision and increasing square grids also have
different topology: the latter's cycle rank is (n-1)², whereas subdivisions preserve
the base graph's cycle rank.

## 8. Literature boundary and exact remaining gap

[B] currently retains the square question without a solution notice. [BP]'s
introduction formulates a torus analogue and conjectures a negative answer. Its
square theorem (4.2) assumes one peak; its two-peak results (6.5, 7.2) concern trees.
Neither assertion settles this square question. [F] treats subdivisions of a fixed
metric graph; applying it while the square's cycle rank grows needs additional
uniform estimates. [D] gives general graph peak-set enumeration. [BBS] concerns
one-dimensional permutations, omitting endpoint peaks. Its results cannot be
transferred without matching the graph and boundary convention. These checked
sources supply no resolution of (1); the literature search was targeted, not exhaustive.

Define Z_n=sum_{a<b}W_Gn(a,b). The exact remaining task is to establish or refute

    [sum_{a<b, dist(a,b)>=epsilon*n} W_Gn(a,b)] / Z_n -> 0
    for every epsilon>0.                                  (9)

The recurrences, positive lower bounds, local rarity estimate, and finite
certificates above do not supply this relative large-n estimate. Both a complete
affirmative proof and a complete negative proof remain absent from this packet.

## References

- [B] K. Burdzy, *My favorite open problems*, Problem 9, inspected 2026-10-05.
  https://sites.math.washington.edu/~burdzy/open_mathjax.php
- [BP] K. Burdzy and S. Pal, *Twin peaks*, Random Structures & Algorithms 56
  (2020), 432-460. DOI: https://doi.org/10.1002/rsa.20883 . Inspected preprint:
  https://arxiv.org/abs/1606.08025v2 (23 February 2017).
- [F] K. Burdzy and S. Pal, *Floodings of metric graphs*, Probability Theory and
  Related Fields 177 (2020), 577-620. Inspected preprint:
  https://arxiv.org/abs/1708.03825 .
- [D] A. Diaz-Lopez, L. Everham, P. E. Harris, E. Insko, V. Marcantonio, and
  M. Omar, *Counting peaks on graphs*, Australasian Journal of Combinatorics
  75(2) (2019), 174-189. https://par.nsf.gov/servlets/purl/10130403
- [BBS] S. Billey, K. Burdzy, and B. E. Sagan, *Permutations with Given Peak Set*,
  Journal of Integer Sequences 16 (2013), Article 13.6.1.
  https://cs.uwaterloo.ca/journals/JIS/VOL16/Billey/billey2.html
