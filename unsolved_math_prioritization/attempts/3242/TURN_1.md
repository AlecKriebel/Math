# Turn 1: exact reformulation, bipartite case, and a general capacity bound

Problem3242 / OPG-46575. First substantive author turn, 2026-10-02.
**Partial results only; the general source inequality remains unresolved.**

The exact live OPG formula and its strict comparison were read before this attempt. The historical references are credited in SOURCE_GATE.md. No historical novelty of the elementary results below is claimed.

## 1. Domain and exact integer reformulation

Let G be a finite simple undirected graph, n>=2, with k=chi(G) and w distinct vertex degrees. Put d=n-w. Since an isolated and a universal vertex cannot coexist, the n possible degree values0,...,n-1 cannot all occur; hence d>=1.

The source asks whether

    k > ceil(floor(w/2)/d).

Because k and d are positive integers, this is equivalent, without any relaxation, to

    floor(w/2) <= (k-1)d,
    w <= 2(k-1)d+1,
    n-1 <= (2k-1)d.                                    (1)

Thus the issue is a lower bound on the repeated-degree deficit d in terms of the actual chromatic number. Dropping the outer ceiling or changing strict greater-than would alter the question at its sharp integer endpoints.

For an edgeless graph, k=w=1 and d=n-1, so(1) holds with equality. We henceforth assume that G has an edge, so k>=2.

## 2. A degree-capacity lemma for a proper coloring

First suppose H has no isolated vertices. Let N be its order, W its degree variety, D=N-W, and let a proper coloring partition its vertices into m nonempty independent classes of sizes

    a_1 <= a_2 <= ... <= a_m,
    S_i=a_1+...+a_i, S_0=0.

Then, for each i,

    a_i <= S_(i-1)+D.                                  (2)

Proof. Every vertex in a class of size at least a_i has degree at most N-a_i. A degree value larger than N-a_i can therefore be represented only by a vertex in one of the first i-1 classes, so there are at most S_(i-1) such values. All remaining degree values lie in the positive integer interval1,...,N-a_i, of cardinality N-a_i. Positivity is precisely where the no-isolate hypothesis is used. Hence

    W <= N-a_i+S_(i-1),

which rearranges to(2). The count of large degree values is bounded by the number of eligible vertices; it does not require those vertices to have distinct degrees. This proves the lemma for every proper coloring, not just an optimal one.

Equation(2) yields S_i<=2S_(i-1)+D. Induction from S_0=0 gives

    N=S_m <= (2^m-1)D.                                 (3)

In particular, taking an optimal coloring proves(3) with m=chi(H).

## 3. Isolates and the universal weaker inequality

Let G have an edge and r isolated vertices. If r=0, (3) gives n<=(2^k-1)d, which is slightly stronger than the claim below. If r>=1, remove all isolates and call the resulting graph H. Then

    N=n-r, W=w-1, D=N-W=d-r+1,
    chi(H)=chi(G)=k.

By(3), with C=2^k-1>=3,

    n-1=N+r-1 <= C(d-r+1)+r-1
                 =Cd-(C-1)(r-1) <=Cd.

Together with the edgeless case this proves the universal bound

    n-1 <= (2^chi(G)-1)(n-w(G)).                        (4)

Equivalently,

    chi(G) >= ceil(log_2(1+(n-1)/(n-w(G)))).             (5)

Formula(4), rather than a floating-point evaluation of(5), is the exact version used in the checker.

## 4. Complete resolution of the bipartite subcase

For graphs with chi(G)<=2, the coefficient2^k-1 in(4) equals2k-1. Thus(4) is exactly(1). Every bipartite graph, including graphs with isolates and the edgeless case, satisfies the source inequality.

For a graph with at least one edge and no isolates, the sharper bipartite statement is n<=3d. One can see it directly: if the two class sizes are a<=b, then positive degree values are at most b, and at most a high-degree vertices can supplement the values1,...,a. Therefore w<=min(b,2a); the two inequalities imply a<=d and b<=a+d, hence n<=3d. Removing isolates gives n-1<=3d exactly as above.

This is a theorem for the entire bipartite class, not an inference from finite graph enumeration. It is a proper subcase of the source question and does not imply its general answer.

## 5. Why the counting route alone does not settle the target

For k>=3, (4) has an exponential coefficient instead of the conjectured linear coefficient. The difference is genuine at the level of the capacity inequalities(2).

For any positive integer d and any number m of color classes, consider only formal class sizes

    a_i=2^(i-1)d, N=(2^m-1)d.

They satisfy equality in every inequality(2). Consequently those inequalities alone cannot force the stronger bound N<=(2m-1)d for m>=3.

For m=3, a more concrete relaxation has class sizes d,2d,4d. Assign the first class the distinct formal degrees5d+1,...,6d; the second the degrees3d+1,...,5d; and the third the degrees1,...,3d plus d extra copies of3d. There are7d vertices,6d distinct positive values and deficit d. Every assigned degree respects the capacity N-a_i of its class. The resulting formal data violate the desired n-1<=5d whenever d>=1.

These data are **not asserted to be a graph degree sequence or a realizable properly colored graph**. For example at d=1, the single first-class vertex would be adjacent to all six others. The two second-class vertices then require seven edges to the third class, but the third-class residual degrees supply only five. Thus this smallest formal obstruction is not realizable. The example identifies missing compatibility information, rather than providing a counterexample to Melnikov's question.

## 6. Remaining gap and next mechanism

The next proof route must use adjacency compatibility between color classes beyond individual degree ceilings. In particular, cut edge totals and simultaneous realization constraints may rule out formal extremal allocations that survive(2). The general chi>=3 case remains unresolved after this turn. No inaccessible historical formula has been silently repaired, no universal source theorem has been claimed, and finite checks are only diagnostics for the explicit arguments above.
