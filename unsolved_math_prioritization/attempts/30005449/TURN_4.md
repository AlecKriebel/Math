# Turn 4: deterministic limits on every finite tree

2026-10-01 06:21 UTC. Fourth substantive author turn. Status: a complete special-class theorem, not the arbitrary-graph conjecture. The class here is an ordinary finite tree with one food vertex, not a tree whose several leaves have been identified into food. No novelty claim is made.

## Theorem and explicit constants

Let G be a finite tree with distinct N,F, and use the exact trace-reinforced model with initial weights one. Let P be its unique N–F path.

- Every edge of P has W_e(n)=n+1, hence limiting normalized weight 1.
- Edges in components inaccessible from N without first visiting F are never crossed and have limit 0.
- For any other edge e off P, let a be the attachment of its branch to P, let d be the graph distance from a to F, and let k≥1 be the edge depth of e in that branch, counted from a. Then almost surely

    W_e(n)/(n+1) → ((d-1)/d)^k.                     (1)

In particular, branches attached one step from food have zero limits; branches attached d≥2 steps from food have strictly positive, explicitly determined limits. Replacing n+1 by n leaves the limits unchanged.

## Exact hitting probability

Every stopped walk must traverse every edge of P. Hence the first assertion is exact at every n, including repeated crossings because reinforcement occurs only once per trace.

For an off-path edge e at depth k, label the branch path from a to its farther endpoint e_1,...,e_k=e. Crossing e is equivalent to hitting that farther endpoint before F. The walk started at N hits a before F almost surely. In a tree, excursions into all branches not on the path between the two prospective absorbing endpoints return to that path before either endpoint is reached. The usual one-dimensional resistance calculation therefore gives

 p_e(W(n)) = [d/(n+1)] / [d/(n+1)+sum_{j=1}^k 1/W_(e_j)(n)]. (2)

For completeness, the harmonic hitting function on the unique path from the far endpoint to F has voltage drops proportional to reciprocal conductances; its value at a is the resistance from a to F divided by the total resistance between the endpoints. Removing returning excursions does not change this harmonic equation.

Set X_e(n)=W_e(n)/(n+1). Formula (2) becomes

    p_e(X(n))=d/[d+sum_{j=1}^k 1/X_(e_j)(n)].        (3)

All weights are positive at finite n, so these denominators are defined. Trace events are nested down each branch; consequently W_child(n)≤W_parent(n), an exact pathwise bound.

## Scalar stochastic-approximation lemma

Suppose Y_n≥1 increases by Bernoulli increments B_(n+1), Y_n≤n+1, and for a fixed integer d≥2,

 P(B_(n+1)=1 | F_n)=d Y_n/[a_nY_n+n+1],

where positive adapted a_n→a>0 almost surely, with the displayed expression being a probability. Assume β=(d-1)/a∈(0,1]. Then Y_n/(n+1)→β almost surely.

Here are the two necessary steps, including exclusion of the unstable boundary zero.

Writing X_n=Y_n/(n+1) gives a scalar stochastic approximation with limiting drift

    f(x)=x[d/(1+ax)-1].

The steps are 1/(n+2), the martingale increments are bounded, and the drift error from a_n-a tends uniformly to zero on [0,1]. The standard one-dimensional ODE argument yields convergence to one of the two zeros 0 or β: martingale perturbations have vanishing tails on bounded ODE-time intervals because the squared step sizes are summable; the remaining error tends uniformly to zero; and the scalar flow has no recurrent set outside its two equilibria. This is the elementary scalar instance of the stochastic-approximation/chain-transitivity framework used in the primary paper's Theorem 2.5. A connected internally chain-transitive limit set for this scalar flow must be one of the two singleton equilibria, since f is strictly positive on (0,β) and strictly negative above β.

It remains to rule out convergence to zero, which cannot be omitted. Since a_n is eventually bounded above and 1≤Y_n≤n+1, the conditional probabilities have a divergent harmonic lower bound. Conditional Borel–Cantelli gives Y_n→∞ almost surely. The logarithmic increment has conditional mean

 E[log Y_(n+1)-log Y_n | F_n]
   = d/(n+1) · [Y_n log(1+1/Y_n)]/[1+a_n X_n].      (4)

The associated martingale difference has conditional variance at most

    p_n/Y_n² ≤ d/[(n+1)Y_n] ≤ d/(n+1).

Thus its partial sums divided by log n tend to zero almost surely: divide increments by log(n+2), use square-summability of 1/[n log²n], then apply the martingale convergence theorem and Kronecker's lemma. On the event X_n→0, the bracket in (4) tends to one, so summation would give

    log Y_n/log n → d>1.

This contradicts Y_n≤n+1. Hence the boundary equilibrium has probability zero, proving the lemma. Eventual random bounds on a_n can be handled on the increasing union of events on which the bound holds after a finite time; no deterministic convergence rate for a_n is required.

## Induction down the branches

If d=1, start with the first edge of a branch. Its conditional trace probability is X/(1+X), so X_n is a nonnegative supermartingale with drift -X²/[(1+X)(n+2)]. It converges almost surely. Its total compensator has finite expectation; a positive limit would force that compensator to diverge harmonically. Thus its limit is zero. Every descendant is bounded above by this first edge and also has limit zero.

Now let d≥2 and put b=(d-1)/d. At depth one, (3) has the scalar form with a_n=d, giving limit b. Suppose the limits for the preceding k-1 edges are b,b²,...,b^(k-1), all positive. For edge e_k, rewrite (3) as

 p_(e_k)=d X_(e_k)/[1+a_n X_(e_k)],
    a_n=d+sum_{j=1}^{k-1}1/X_(e_j)(n)
       →d+sum_{j=1}^{k-1}b^(-j)=d b^(-(k-1)).

The scalar lemma gives limit (d-1)/(d b^(-(k-1)))=b^k. Since the graph is finite, finitely many almost-sure induction statements can be intersected, proving (1) for all edges.

## Scope of the increment

This establishes genuine almost-sure deterministic limits, not only equilibrium uniqueness or numerical ODE attraction, for every finite tree. It also explicitly controls edges with zero limits. Cycles destroy the unique-path resistance reduction: two possible routes to the queried edge can interact, and the ancestor induction no longer applies. Consequently the full finite-graph conjecture is still unresolved after four author turns.

The positivity clause in the primary paper is stronger than the imported deterministic-limit question; no claim about that additional clause is needed here. The theorem is stated for ordinary trees as defined above, retaining any dangling branches rather than silently deleting edges that an ant can visit before food.
