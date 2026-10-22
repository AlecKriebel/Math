# Attempt 1: First-contraction averaging and its inductive boundary

Timestamp: 2026-10-03 13:50 UTC. Budget: 1/5. Exact-target completion estimate: 2%.

For n>=2, let delta(u,v)=|(N(u) symmetric-difference N(v)) minus {u,v}|. The first contraction creates delta(u,v) red neighbours, so L(G)=min delta(u,v) is a lower bound on twin-width, not an upper bound.

## Degree-defect identity
Double-count triples (u,v,w) where w sees exactly one of u,v:

sum_{u<v} delta(u,v) = sum_w d(w)(n-1-d(w)).

Writing c=(n-1)/2, this gives the exact identity

average delta = c - 2 sum_w(d(w)-c)^2/[n(n-1)].

Hence if L(G)>=c-epsilon, then sum_w(d(w)-c)^2 <= epsilon n(n-1)/2. In particular, equality L(G)=c forces regularity d=c and every pair-distance equal to c; separating adjacent/nonadjacent pairs gives the conference parameters (n,c,(n-5)/4,(n-1)/4). This recovers the known equality characterization, while displaying its quantitative defect identity.

The known first-step estimate and equality characterization are credited to Ahn et al., Corollary 4.2, and Heinrich et al., Theorem 4.1. The defect rearrangement is an elementary reformulation, with no novelty claimed.

## Attempted induction and explicit failure
Try contracting a pair attaining L(G)<=c, then induct on the remaining n-1 vertices. This fails because the quotient is a trigraph with existing red edges, outside the all-black graph hypothesis. For the 5-cycle, every pair-distance is 2. Its first quotient has four parts and red degree 2, already exceeding the proposed four-vertex ceiling floor((4-1)/2)=1. Thus an induction claiming the same order-only bound for these quotients is false, even on the smallest conference graph. The original five-vertex bound remains possible, and is attained by C5.

Outcome: a checkable defect identity and a concrete obstruction to naive induction, but no upper bound on the later red-degree maximum. Reopening requires an invariant carrying the original n and accumulated red edges, rather than invoking an all-black theorem on a quotient.
