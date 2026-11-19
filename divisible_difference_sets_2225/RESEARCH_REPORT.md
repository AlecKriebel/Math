# EP-635: bounded research on the sharp excess

Date: 2026-10-21 UTC. Queue 1867 / ID 2225. This is a mathematical research note, not an acceptance report or a literature-novelty claim.

## Status and target

For positive integers t,N, let M_t(N) be the largest cardinality of A contained in [1,N] with no distinct a<b in A satisfying b−a≥t and (b−a)|b. Equivalently, exclude every pair kd,(k+1)d with d≥t and k≥1. The fixed-t asymptotic M_t(N)=N/2+o_t(N) is already recorded as solved in January 2026. The source gate `SOURCE_STATUS.md` has NOT audited that proof or checked a live current official status. This note does not repair either gap. In particular, no half-density result here is new and no sharp global upper bound is established.

The known t=2 logarithmic construction is attributed in the recovered source record; it is not claimed as a discovery here. The global sharp excess and exact structure remain unresolved by this work. The separate INDEPENDENT_AUDIT.md accepts only its explicitly scoped claims.

## Approach 1: recover the correct graph and isolate the known-proof boundary

Define G_t(N) on [1,N] with an edge exactly for the forbidden pairs above. Then M_t(N)=alpha(G_t(N)). Because d divides b iff d divides b−d, a difference dividing either endpoint divides both. This is a consecutive-multiples graph, not the usual divisibility/primitive-set graph. Replacing its edges by all divisibility pairs is invalid.

For t=1 the pairs (1,2),(3,4),… are edges. Thus alpha≤ceil(N/2), and all odds attain equality. For t≥2 all odds are still independent: an even difference cannot divide an odd endpoint. The t=1 matching proof does not extend because the difference-one edges have been removed.

The recovered gate records an Elliott-inequality proof route for fixed-t half density. No primary proof artifact was available in the supplied recovery and no formal proof was reconstructed here. Reconstructing the known leading asymptotic would not resolve the sharper question. We therefore stop this route at its verified source boundary rather than quietly treat a discussion estimate as a logarithmic-error theorem.

## Approach 2: parity, exact odd-neighbor description, and a restricted extremal theorem

Write every even x uniquely as x=2^k m, k≥1, m odd. Its odd neighbors are exactly those numbers x−d and x+d which lie in [1,N], where d is an odd divisor of m and d≥t. Indeed an odd-even difference d is odd, and the edge condition is equivalent to d|x. Conversely each such d produces the stated edges when in range.

Consequently, for t≥2, x is compatible with ALL odd integers in [1,N] if and only if m<t. Sufficiency is immediate. For necessity, if m≥t then x−m=(2^k−1)m is a positive odd integer below x, and is a forbidden neighbor. Thus every admissible superset of the odds consists of the odds together with an independent subset of

F_t(N)={2^k m≤N: k≥1, m odd, m<t}.

This is an exact characterization, not a statement that a global maximum must contain all odds.

For t=2, F_2 consists precisely of powers 2^k, k≥1. Two such powers with exponents i<j conflict exactly when j=i+1: their difference is 2^i(2^(j−i)−1), which divides 2^j only if the odd factor is 1. Hence the best set CONTAINING ALL ODDS has size

ceil(N/2)+ceil(floor(log_2 N)/2).

The extra exponents may be chosen odd (2,8,32,…). Powers 4,16,64,… also work but have one fewer member at some N. This proves only the restricted optimum. The assertion that an unrestricted optimum always has this size is an unproved candidate consistent with our finite computations, not a theorem or a novelty claim.

A potential global proof would have to control the net gain from deleting some odds and inserting non-power evens. The neighbor description alone does not establish the required Hall-type expansion. Moreover, the full graph is not bipartite: for t=2, vertices 6,8,12 form a triangle. Bipartite matching on the odd-even subgraph alone discards relevant even-even conflicts.

## Approach 3: explicit logarithmic constructions and t dependence

A uniform simple construction for every t≥2 is all odds plus selected powers of 2. Let L=floor(log_2 N) and q=max(1,ceil(log_2 t)). Among exponents 1,…,L, the only forbidden edges are k—(k+1) for k≥q. Therefore the maximum number of powers that can be adjoined is exactly

min(L,q−1)+ceil(max(0,L−q+1)/2).

This formula is restricted to odds plus powers and does not describe the whole F_t family.

Here is a larger explicit fixed-t family, included as an elementary derived lower bound without a novelty claim. Let h=floor(t/2), m*=2h−1, and Q=1+floor(log_2(2m*)). Adjoin every 2^k m≤N with m odd, 1≤m<t, k≥1, and k≡1 mod Q.

These added evens have no odd neighbors by Approach 2. Two added evens with the same exponent k cannot conflict: their difference 2^k|m−n| would require the nonzero even number |m−n| to divide the odd number n. For differing exponents k>l, an edge requires |2^(k−l)m−n| to divide n; therefore 2^(k−l)m≤2n≤2m*. Thus k−l≤Q−1, whereas our selected exponents differ by at least Q. Contradiction. The threshold on the even-even edge is not needed for this sufficient construction.

The number of added evens is exactly

sum over odd m<t of max(0, 1+floor((floor(log_2(N/m))−1)/Q)).

For fixed t this is (h/Q)log_2 N+O_t(1). This exhibits a t-dependent logarithmic lower-bound coefficient, not a uniform asymptotic when t grows with N. For t=2 it reduces to the known odd-exponent powers construction. For t=4 it yields coefficient 2/3 in base-2 logarithms, versus 1/2 for a single powers chain. Optimality for t≥3 is not claimed.

## Approach 4: exact finite computations with exhaustive recurrence

`exact_check.py` constructs the integer graph directly from forbidden pairs and computes its independence number using the exhaustive identity

alpha(S)=max(alpha(S\{v}), 1+alpha(S\({v} union neighbors(v)))).

Disconnected components are summed; the empty graph has value zero. Every recursive call decreases the vertex set. The choice of a maximum-degree vertex is only a speed heuristic and does not affect correctness. No floating-point optimization or tolerance is involved. Every returned witness is also checked directly against the original arithmetic definition.

`exact_results.json` records all 300 cases 1≤N≤50 and 1≤t≤6, including optimum sizes, explicit witnesses, and memoized-state counts. In every tested t=1 case the result is ceil(N/2). In every tested t=2 case it is ceil(N/2)+ceil(floor(log_2 N)/2). Additional sampled t=2 calculations at N=60,80,100,120,150 give 33,43,53,63,79, respectively, also equal to this candidate. These sampled runs are separately recorded in `sampled_t2_results.json`.

This is a reproducible exhaustive computational certificate, not a formal proof-assistant certificate. The executable recurrence and bounded results must not be extrapolated to all N. For instance, with N=20 the results for t=2,…,6 are 12,13,14,14,15: increasing t changes the lower-order structure even at modest sizes.

## Approach 5: upper-bound barriers, exact threshold extremes, and unsuccessful routes

Monotonicity is immediate: M_t(N) is nondecreasing in t and N. Every forbidden edge has upper endpoint at least 2t. Consequently M_t(N)=N when N<2t. At N=2t there is exactly one edge, namely {t,2t}, so M_t(2t)=2t−1. These facts rule out a half-density estimate uniform over arbitrary growing t.

Keeping only the doubling edges {x,2x}, x≥t, gives disjoint paths along odd-part chains. At threshold 1 their total independence number is the finite alternating sum N−floor(N/2)+floor(N/4)−floor(N/8)+… =2N/3+O(log N). Removing the edges with x<t can increase this path-forest independence number by at most t−1. Therefore this subgraph supplies only the weak bound

M_t(N)≤2N/3+O(log N+t),

not the required N/2+O_t(log N). A sharper all-graph argument is indispensable. This is a limitation of this upper-bound route, not a lower bound for the original graph or an impossibility theorem for every matching method.

A tempting exchange argument replacing every non-power even x by its odd neighbor x−oddpart(x) is not injective. At t=2, a nonfree-only collision is x=18 (odd part 9) and x=12 (odd part 3), both mapping to 9; these two evens themselves conflict, so this collision alone is not a counterexample to a more refined simultaneous exchange. It does show why a naive per-vertex injection cannot be asserted. Whether a conflict-aware exchange can establish the t=2 candidate remains unanswered here.

Ordinary matching certificates also have a structural barrier. Every odd prime p>N/2 is isolated in G_t(N) for t≥2: the only possible nontrivial difference dividing p or a neighboring endpoint is p itself, and the possible partner 2p lies outside the interval. If I such primes occur, any matching leaves at least I vertices uncovered, so its resulting independence upper bound N−matching_size is at least (N+I)/2. Thus a matching-only certificate cannot deliver a logarithmic error whenever I exceeds a constant times log N. No asymptotic prime-counting estimate is needed for this conditional obstruction.

## Honest outcome

Five distinct routes were examined. Useful rigorous output consists of the exact odd-neighbor characterization; the restricted all-odds extremal formula at t=2; the powers-chain formula at general t≥2; an explicit t-dependent logarithmic family; and bounded exhaustive computations. None proves the sharp global excess, establishes a new literature result, or audits the known half-density proof. No external communication, GitHub mutation, or QUEUE edit was performed.
