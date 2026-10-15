# Universal transport and compactness audit proof

This is an independent reconstruction of the finite/infinite reformulation, not a new resolution of Q12.33. The proof applies for every integer d>=1, every x,y in Z^d, and every integer N>=0. Complete SRW laws and time 0 are mandatory.

## 1. Labeled words, finite transport and Hall deficiency

Write S_d={-e_1,+e_1,...,-e_d,+e_d}. The map from a word w in S_d^N to its vertex path starting at x is bijective: the successive differences recover w. There are L=(2d)^N equally likely words. Repeated vertex ranges do not identify distinct outcomes. Let E_N be the relation of disjoint vertex ranges of the two labeled paths. A finite coupling is a nonnegative L-by-L matrix C whose row and column sums are 1/L. Thus D=L C is doubly stochastic.

Here is a finite proof of the needed decomposition. In the positive support of D, for any subset A of left labels, all its row mass |A| enters its neighborhood, whose total column mass is |N(A)|. Hence |A|<=|N(A)|. To justify the matching conclusion without assuming the target result, take a maximum support matching. Starting from unmatched left vertices, follow alternating nonmatching edges left-to-right and matching edges right-to-left. Let U,V be the reached left/right sets. No reached right vertex is unmatched, since otherwise there is an augmenting path. Every neighbor of U is in V, and every V is a neighbor of U. The matching bijects V with the matched members of U. Consequently |U|-|N(U)| equals the number of unmatched left vertices. The preceding Hall inequalities force that number to vanish. So the support has a perfect matching P.

Subtract t P, where t is the least positive matched entry. If t=1, D=P. Otherwise (D-tP)/(1-t) is doubly stochastic, has fewer positive entries, and the same argument applies again. The finite number of positive entries makes this procedure terminate. Therefore D is a convex combination of permutation matrices. The linear E_N mass is no greater than the largest E_N edge count of a permutation divided by L. Any such edge set is a matching, so its size is at most M_N.

Conversely, choose a maximum E_N matching. There are equally many unmatched labels on the two sides, so any bijection of those labels completes it to a permutation. It cannot introduce any additional allowed edge: such an edge would enlarge the matching. Thus its exact allowed count is M_N and the coupling assigning 1/L to its pairs has the desired complete finite marginals. The finite optimum is a_N=M_N/L and is attained.

For any matching and any A, at most |N(A)| members of A can be matched. Thus |A|-|N(A)|<=L-M_N for a maximum matching. The alternating sets U,V constructed above satisfy equality. The empty subset is allowed and gives deficiency zero. Hence

  M_N = L_N - max_A (|A|-|N(A)|),
  a_N = 1 - max_A (|A|-|N(A)|)/L_N.

The neighborhood is a union: a right word belongs if it avoids at least one left word in A. It is not the words avoiding every member of A.

## 2. Complete marginals, extension and compactness

Identify a full SRW from x with Omega_d=S_d^{positive integers}, with product measure m of independent uniform coordinates. The map to vertex paths includes the fixed initial vertex x and is continuous on each finite coordinate. A compatible compact metric is rho(u,v)=sum_{n>=1} 2^{-n} 1{u_n!=v_n}. Sequential compactness follows by diagonal selection: extract a subsequence constant at coordinate 1, then 2, and so on. The diagonal subsequence converges. The pair space is also compact and metrizable.

Let K be all Borel probability measures on the pair space with both marginal increment laws equal to m. K is nonempty (product measure), compact for weak convergence, and closed: any weak limit retains the integrals of every continuous function of either coordinate, and hence retains its marginal law. For completeness, compactness of measures can be obtained by diagonal subsequences of the finitely many joint cylinder probabilities at each level. Their limits are consistent probability tables, extend to a measure, and yield weak convergence because continuous functions on the compact product are uniformly approximable by functions depending on finitely many coordinates. This also proves sequential compactness of K and suffices here.

For each N, R_N is the set of pairs having disjoint ranges through N, including both time-0 vertices. It depends only on the first N increments of each sequence; it is a finite union of pair cylinders and therefore clopen. R_{N+1} is contained in R_N. The intersection R is precisely all-pairs avoidance at every pair i,j>=0: any particular pair of times is included once N>=max(i,j). R is closed and measurable, though generally not open.

Every finite prefix coupling extends to an element of K. First sample its coupled prefixes, then append two independent sequences of iid uniform increments, independent also of the prefixes. Within either marginal, any prescribed length-(N+k) word has probability (2d)^(-N-k), because its prefix mass is (2d)^(-N) and its independent tail mass is (2d)^(-k). This checks the **complete** marginal path law, not just one-time positions. The tails need not be independent for all possible extensions; this particular choice is enough to establish existence.

Restriction of any horizon-(N+1) coupling is a valid horizon-N coupling, and R_{N+1} subset R_N. Thus a_{N+1}<=a_N. The limit a=inf_N a_N=liminf_N a_N exists in [0,1]. For each N choose an optimum finite coupling and the extension pi_N described above. The sequence need not be projectively consistent. Compactness gives a subsequence pi_{N_j} converging weakly to pi in K, with N_j increasing to infinity. Fix k. For every j large enough that N_j>=k,

  pi_{N_j}(R_k) >= pi_{N_j}(R_{N_j}) = a_{N_j} >= a.

The continuous indicator of the fixed clopen set R_k permits passage to the weak limit: pi(R_k)>=a. Since these sets decrease, countable continuity from above gives pi(R)=lim_k pi(R_k)>=a. Conversely, every eta in K has eta(R)<=eta(R_N)<=a_N for every N, so eta(R)<=a. Therefore

  max_{eta in K} eta(R) = a = lim_N M_N/(2d)^N.

In particular, attainment is true even if a=0. One may also see attainment from the upper semicontinuity of eta -> eta(R) for closed R on compact K. **Invalid shortcut:** weak convergence does not generally justify substituting R_{N_j} for a fixed test event. The proof above uses fixed k first and continuity from above second.

## 3. Weighted finite laws and the general compact extension

For finite sets U,V, probability weights p_u,q_v, and an allowed relation E, a coupling has row sums p and column sums q. The unweighted cardinality result does not apply when individual weights differ. Define N(A) as above and D=max_{A subset U}(p(A)-q(N(A))). The empty set ensures D>=0.

Build a network with capacities p_u from source to u, capacity 2 on every allowed u-to-v edge, and capacities q_v from v to sink. Since total source mass is 1, the middle capacities never constrain a feasible total flow. A maximum flow exists because its feasible finite-dimensional set is compact. At a maximum, no positive-residual source-to-sink path exists; otherwise augmenting by the least residual capacity on it increases the flow. The source-reachable residual cut has capacity equal to the flow: forward crossing edges are saturated and backward crossing edges carry zero flow. Every cut has capacity at least any feasible flow, by summing conservation. This establishes max-flow/min-cut even for real weights without an integer-termination assumption.

A cut of capacity at most 1 cannot cut a middle edge of capacity 2. If A are its left vertices on the source side, it must also put N(A) on that side. It is cheapest to put exactly N(A) right vertices there. Its capacity is 1-p(A)+q(N(A)). Minimizing over A gives maximum safe subcoupling mass f=1-D. Each full coupling has safe mass at most f by restriction to safe edges. Conversely extend a maximizing subcoupling F: its remaining row masses r and column masses s total t=1-f. If t>0, add the nonnegative residual product matrix r_u s_v/t; if t=0 no addition is needed. This produces a full coupling and safe mass at least f. It cannot exceed f, so the exact weighted optimum is 1-D. This argument permits zeros and unequal support cardinalities.

For fixed complete probability laws on finite-alphabet path spaces (not necessarily SRW), each positive-probability prefix has a conditional full tail law. Couple the prefixes and, conditionally on them, independently sample these two conditional tails. Null prefixes never occur and their tail kernels may be assigned arbitrarily. This gives the extension step. The same fixed-k compactness proof yields the maximum infinite mass as the decreasing limit of weighted finite optima whenever the event is the decreasing intersection of clopen finite-prefix events. Using inconsistent ad hoc weights at different horizons would fail to define the prescribed complete laws.

## 4. Actual starts, bounds and failed shortcuts

Put v=y-x and r=||v||_1. For x!=y, synchronous translation Y_n=X_n+v is a valid complete-path coupling. A collision X_i=Y_j implies X_i-X_j=v. But any segment of one path with both indices in [0,N] has length |i-j|<=N, so ||X_i-X_j||_1<=N. Thus if N<r its ranges are disjoint and a_N=1. For r=10 this proves every horizon N=0,...,9, in all dimensions and for every signed/non-axis displacement of l1 norm 10. This is stronger than the coupling-independent fact that 2N<r makes every pair safe.

The same translation has zero infinite full-range avoidance. Fix one increment word of length r summing to v. Every disjoint block of r iid increments equals that word with probability b=(2d)^(-r)>0, independently. Probability no such block occurs among the first k is (1-b)^k ->0. Any occurrence yields X_{r(k+1)}=X_{rk}+v=Y_{rk}, a different-time collision. Infinitely many occurrences hold as well, but one is enough. Simultaneous collisions never occur because Y_n-X_n=v!=0. This proves only failure of this particular coupling, not failure of unrestricted couplings.

The optional one-dimensional limiting control needs no recurrence assumption. Translate its starts to 0<r. Stop the martingale X_n on first reaching -m or r. Exit occurs almost surely: from anywhere in this finite interval, a fixed run of at most m+r positive steps exits, with probability at least 2^(-(m+r)) per disjoint block, so the chance of no exit tends to zero. The stopped martingale is bounded; its expected terminal position is zero. Therefore P_0(T_r<T_{-m})=m/(m+r), which tends to one as m tends to infinity. Hence P_0(T_r<infty)=1. At every finite N, the all-negative prefix from 0 and all-positive prefix from r are disjoint. Give that one pair mass 2^(-N), then couple the remaining equally weighted labels arbitrarily and append independent tails. This proves positive finite optimal mass at every N and zero infinite mass for the actual SRW event in d=1.

A separate moving-event control even preserves both complete fair-bit marginals. Let X be iid fair bits and let Y equal X except for complementing bit N. Each Y marginal is again iid fair. Let C_k require equality of the first k coordinates. For every fixed k, pi_N(C_k)=1 when N>k, so pi_N tends weakly to the diagonal coupling pi. But pi_N(C_N)=0 for every N whereas pi(intersection_k C_k)=1. Thus continuity of moving clopen indicators cannot be invoked; fixed-k weak passage is essential. This does not contradict the correct optimizer argument above.

For every complete coupling, R implies X never visits the deterministic Y_0=y. Hence alpha(x,y)<=1-P_x(T_y<infty). If x!=y, a prescribed shortest word gives a strictly positive hitting probability, so the right side is <1. In d=3,4 transience does not convert this upper bound into a positive lower bound for alpha. The same argument using Y visiting x also applies. If x=y, R_0 is empty and every a_N and alpha is zero. N=0 has L_0=1 and for distinct starts a_0=1.

At r=10, a hit by time 10 must occur exactly at time 10. Every contributing word uses only the sign-directed coordinate steps, a_i=|v_i| times in coordinate i. Conversely each such ordering reaches y at time 10 and cannot reach earlier. There are 10!/(product_i a_i!) such words, each of mass (2d)^(-10), including zero coordinates and either sign. Consequently

  P_x(T_y<=10) = 10!/(product_i a_i!) * (2d)^(-10),
  a_10 <= 1 - 10!/(product_i a_i!) * (2d)^(-10) < 1.

The block failure of translation does not rule out a different optimizer. Nor does a_N>0 for every finite N imply inf_N a_N>0. A particularly transparent consistent finite-alphabet countermodel has two iid fair-bit marginal sequences and R_N requiring the first sequence's first N bits to be zero (and no restriction on the second). Every coupling has optimum 2^(-N)>0, but R requires an infinite all-zero sequence of probability 0 under its fixed marginal. Clopenness, compactness, consistent laws and attainment all hold; positivity alone is the missing uniform estimate. For the SRW event itself, d=1 distinct starts supplies the analogous obstruction: the first walk hits y almost surely, yet each finite horizon has a safe pair (all steps to the left from x and all steps to the right from y after ordering x<y). A positive-mass prefix pair extends to complete SRW laws, so each finite optimum is positive; nevertheless alpha=0. The independent controls also check the fair-bit countermodel exactly, without relying on a recurrence citation.

## 5. What remains in dimension three

For each fixed x,y in Z^3 with ||x-y||_1=10, positive infinite avoidance is equivalent to the existence of epsilon(x,y)>0 such that, for every N>=0 and every subset A of P_N(x),

  |A|-|N(A)| <= (1-epsilon(x,y)) 6^N.

The negation is: for every epsilon>0 some N and A have deficiency greater than (1-epsilon)6^N. The reduction proves neither side. If the intended target quantifies over all distance-10 starts, signed coordinate permutations and translations leave finitely many displacement types, so positivity for each type implies a common epsilon by taking the finite minimum. No uniform estimate over arbitrary distance or dimension has been inferred. Prior 4D theorem validity, source status and novelty are separate conditional dependencies. The universal theorem and controls above do not settle the remaining 3D question and add 0 original proof-attempt turns.
