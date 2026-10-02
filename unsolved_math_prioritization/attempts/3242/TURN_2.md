# Turn 2: cross-class edge balance and a quadratic necessary condition

Second substantive author turn. The general source target remains unresolved.
This turn adds an adjacency constraint that the individual degree ceilings of Turn1 omit.

## 1. Exact cut identity

Let H be a graph without isolated vertices, of order N, with W degree values and deficit D=N-W. Fix an independent vertex set C, of size c, and put B=V(H)\C and S=|B|=N-c. Write e(B) for the number of edges induced by B. Then

    sum_(v in B) deg(v) - sum_(v in C) deg(v) = 2e(B).    (1)

Every crossing edge occurs once on both sides and cancels; only internal B edges remain. Independence of C is required.

Assume W>=S. Then

    W(W+1)/2 - S(S+1) - D S <= 2e(B).                  (2)

Proof. Select one representative vertex of each distinct degree. For any degree t>S, its representative cannot lie in C, since each vertex of C has at most S neighbors. Its contribution to the left-hand side of(1) is therefore +t. For1<=t<=S, the contribution is at least -t, whichever side its representative occupies. Every nonrepresentative vertex contributes at least -S: a negative contribution can only come from C, where degree is at most S. There are exactly D nonrepresentatives.

Define h(t)=-t for1<=t<=S and h(t)=t for t>S. The smallest possible sum of h over W distinct positive integers, when W>=S, is obtained by choosing all1,...,S and then S+1,...,W. Its value is

    -S(S+1)/2 + [W(W+1)-S(S+1)]/2
      = W(W+1)/2-S(S+1).

Thus(1) is at least this value minus DS, proving(2). Missing a low degree can only raise this minimum. Repeated high degrees are not subtracted improperly: their actual positive contribution is at least the lower bound -S used for every nonrepresentative.

## 2. Proper-coloring specialization

If B is partitioned into nonempty independent classes of sizes a_1,...,a_(m-1), then

    2e(B) <= 2 sum_(i<j) a_i a_j.

Combining this with(2) gives an exact quadratic necessary condition on a properly colored degree-variety configuration. For three classes of sizes a,b,c, with C the third class, it reads

    W(W+1)/2-(a+b)(a+b+1)-D(a+b) <=2ab,                (3)

provided W>=a+b. This is an additional graph-realizability requirement, not an inequality for arbitrary assignments of degree labels to independent classes.

If the classes are ordered by size, Turn1 also gives a<=D, b<=a+D, c<=a+b+D. Those separate inequalities must be retained; (3) does not replace them.

## 3. Actual progress beyond Turn1's relaxation

The formal sizes(1,2,4), order7, variety6 and deficit1 meet every capacity constraint from Turn1. But(3) gives

    21-12-3 = 6 <= 4,

which is impossible. Thus no isolate-free properly3-colored graph realizes those parameters.

More generally, the formal geometric class sizes(d,2d,4d) with variety6d fail(3) whenever d>=1. Its left-hand side is

    (6d)(6d+1)/2-(3d)(3d+1)-3d^2 = 6d^2,

whereas the right-hand side is4d^2. The incompatibility survives all repeated-degree assignments and all choices of the present degree values, because the proof of(2) minimized over those choices.

At order12 and deficit2, the candidate class sizes(2,3,7), variety10, are likewise excluded: the lower cut bound is15 while2ab=12. The other capacity-compatible shape(2,4,6) is not excluded: its lower bound is1 and its upper bound is16. This is a concrete surviving gap, not a graph construction or counterexample.

## 4. Consequence for one isolate-free boundary slice

An isolate-free3-colorable graph with deficit1 has at most7 vertices by Turn1. If it has7, its nonempty proper-color class sizes must be(1,2,4): a<=1, b<=a+1, c<=a+b+1, and their sum is7. The preceding contradiction excludes that case. Hence such a graph has at most6 vertices. This proves the exact source inequality for isolate-free graphs of chromatic number3 and deficit1. The cases with chromatic number at most2 were already established.

The statement here does not silently remove isolates from that boundary slice: removing an isolate shifts both order and variety and requires the stronger bound on the remaining core. That extension is not asserted from this argument alone.

## 5. Limit of the route and next question

The cut identity genuinely adds compatibility information to color-class capacities. It still leaves near-boundary3-colorable formal allocations, such as(2,4,6), that could only be decided by finer simultaneous adjacency constraints. Numerical feasibility of a relaxation would not supply a graph; an infeasible numerical model without a checked certificate would not supply an unrestricted theorem.

The original problem remains unresolved after2/5 turns. The next structural route will test whether exact deficit inequalities are preserved under graph composition and whether special graph classes can be handled without guessing degree-sequence realizability. No historical novelty is claimed for these elementary inequalities.
