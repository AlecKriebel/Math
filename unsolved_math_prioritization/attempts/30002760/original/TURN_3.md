# Approach 3: exhaustive mesh search with nested overlays

## Aim and disposition

Try to bypass difficult local-marking analysis by globally comparing finitely many admissible meshes. A conditional construction attains the correct mesh-cardinality exponent. It does not give an efficient or source-general algorithm because its comparator and computational cost remain substantive requirements.

## Proposition 3.1 (conditional nested rate transfer)

Let a refinement family have a root mesh T_0. Set m(T)=#T-#T_0. Suppose the family with m(T)<=N is finite for every integer N>=0. Assume any two admissible meshes have an admissible overlay T join S refining both and satisfying

m(T join S)<=m(T)+m(S).

Let X_T be finite-dimensional subspaces of a Hilbert space X, nested under refinement, and put E(T)=inf_{v in X_T}||u-v||_X and E_N=min_{m(T)<=N}E(T). Suppose:

1. A comparator supplies scores a(T) with c E(T)<=a(T)<=C E(T), where 0<c<=C<infinity are independent of T.
2. At budget 2^k a selector returns P_k with m(P_k)<=2^k and a(P_k)<=lambda min_{m(T)<=2^k}a(T), lambda>=1.
3. The discrete solve on any T returns U_T with ||u-U_T||_X<=Q E(T), for a mesh-independent Q.

Define S_0=P_0 and S_k=S_{k-1} join P_k. For s>0 let A_s=sup_{N>=0}(N+1)^s E_N. If A_s<infinity, then

||u-U_{S_k}||_X <= Q lambda (C/c) 2^s A_s (m(S_k)+1)^-s.

Proof. Repeated overlay gives m(S_k)<=sum_{j=0}^k 2^j=2^{k+1}-1. By inclusion, E(S_k)<=E(P_k). The score inequalities yield E(P_k)<=lambda(C/c)E_{2^k}. Hence the error is at most Q lambda(C/c) A_s(2^k+1)^-s. Since m(S_k)+1<=2^{k+1}<=2(2^k+1), the desired bound follows. This proof includes zero errors; no division by an error is used.

The selector is an actual finite procedure if, for example, the admissible meshes can be enumerated and every nonnegative score is exactly computable and comparable in a specified finite representation. One may then take lambda=1. Alternatively, certified multiplicative comparisons, including a valid treatment of zero scores, suffice. An oracle for the unknown exact solution is not a practical implementation. Computable real numbers alone do not automatically supply terminating exact equality/order decisions.

## Proposition 3.2 (the exhaustive-search cost is real)

For binary midpoint refinement of one initial interval, the distinct partitions with N internal splits are in bijection with rooted ordered full binary trees with N internal vertices. The internal splits are uniquely recovered by joining sibling dyadic intervals from the leaves up. Thus their number C_N obeys

C_0=1, C_N=sum_{j=0}^{N-1} C_j C_{N-1-j}.

For N>=2, the two endpoint terms are distinct and give C_N>=2C_{N-1}. Since C_1=1, induction gives C_N>=2^{N-1} for all N>=1. Therefore a literal enumeration of every budget-N candidate uses at least exponentially many visits even in this one-dimensional refinement family. This is a lower bound for that exhaustive procedure only; it is not a complexity lower bound for all mesh-selection algorithms.

## Remaining gap and credit

The overlay idea and nonlinear best-approximation classes are standard in adaptive approximation. The proof is a self-contained conditional reconstruction, not a new solution claim. In an actual convection-diffusion method the score may estimate total error including oscillation rather than E(T) alone; uniform two-sided equivalence is not free. For parabolic problems the admissible space-time family, stability, comparator and cost must also be specified. The source does not fix those details, so the conditional theorem cannot be promoted to a complete answer by simply assuming them.
