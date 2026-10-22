# Independent reconstruction and falsification record

This reconstruction concerns the bound version1.0 source and PDF. I used no earlier review verdict as a premise. All statements below are deductions for the declared model; the finite computations are supplementary controls.

For H>=2, the rooted binary tree has 2k leaves and 4k-1 vertices, with k=2^(H-1). Removing an edge separates k_e leaves, all on one root side, from the opposite k leaves. Exactly k*k_e unit commodities use that edge. Doubling demand forces its capacity to be at least2k*k_e. These lower bounds fit simultaneously. Every increment has a positive coefficient in the linear objective, so any strictly larger feasible capacity vector costs strictly more. This proves uniqueness for fixed topology. It would fail if a price could vanish; the paper explicitly excludes that case.

For an admitted matrix y, the left terminal constraints are its k row bounds2k, and the right constraints are its k column bounds2k. Every other physical load is a sum of the appropriate descendant row or column loads, and its capacity is the same sum of terminal capacities. Consequently there is exact equivalence between the tree and capped bipartite transportation. No cancellation, circulation or route splitting is assumed: each physical route is the unique simple path.

An auxiliary cut with source-side left set A and right set B has capacity

    2k(k-|A|+|B|) + |A|(k-|B|) + (t-1) sum_(i in A,j notin B) X_ij.

Max-flow/min-cut gives the paper's finite minimum. Because the number of cuts is finite, inactive cuts have a positive value gap at any fixed time, and sufficiently small perturbations cannot make them active. Among active affine lines, the smallest slope wins to the right, including at ties. Thus the stated right derivative is correct. Every cut slope is in[0,S_k]. Division by the realized slope S_k gives a marginal in[0,1]. Normalization by k^2 would instead give S_k/k^2 in the fully admitted phase and would not give exactly one at finite k.

If offered terminal totals are all strictly below2k, the full matrix d is feasible. Its total is the sum of all coordinate upper bounds. A maximizing matrix can therefore have no deficient entry. It equals d uniquely. Sums over finitely many descendant terminals preserve strict slack, so every physical edge is spare. Conversely, throughput is at most2k^2. If equality holds, the sum of k row bounds is tight, forcing every row to be tight, and the same applies to columns. All internal sums are then tight for every optimizer. Nonuniqueness of individual entries creates no ambiguity in these outer phases.

For Z~Gamma(n,1), the exponential moment (1-lambda)^(-n), lambda<1, gives exp[-n I(a)] as the upper-tail bound for a>1 and lower-tail bound for0<a<1, where I(a)=a-1-log(a). For the lower tail lambda<0, the Markov event is reversed when exponentiating, as required. With delta in(0,1),

    I(1/(1-delta)) = integral_0^delta u/(1-u)^2 du >= delta^2/2,
    I(1/(1+delta)) = integral_0^delta u/(1+u)^2 du >= delta^2/8.

At2-delta, a terminal can reach capacity only if a Gamma(k,1) slope sum reaches k/(1-delta). Union over2k terminals gives2k exp(-k delta^2/2). No independence of rows and columns is used. At delta=8 sqrt(log(k)/k), the exponent is exactly-31 after the union factor. The good event excludes equality at the lower endpoint. Since the number of constraints is finite and slopes are finite, this strict slack persists for a right neighborhood. That supplies the endpoint right derivative. Earlier-time uniformity follows from entrywise monotonicity, without a union over times.

For the upper endpoint set D=R\B, a=|A|, d=|D|. A cut can obstruct throughput2k^2 only if a+d>k; otherwise its required rectangle lower bound is nonpositive. Full throughput is equivalent to all inequalities

    sum_(A x D) [1+(1+delta)X_ij] >= 2k(a+d-k).

The identity ad-k(a+d-k)=(k-a)(k-d)>=0 means failure implies a Gamma(ad,1) sum below ad/(1+delta). If the actual threshold is nonpositive, failure is impossible; using this larger positive threshold remains safe. Each cut fails with probability at most exp(-c ad), c>=delta^2/8.

Write q=min(a,d), ell=k-max(a,d). Then0<=ell<q and ad=q(k-ell). For q<=floor(k/2), the count at fixed q,ell is at most2 binom(k,q)binom(k,ell), including harmless double counting. Summing ell gives at most2q k^(2q). The area is at least qk/2. For q>k/2, area is strictly above k^2/4, and at most4^k subset pairs occur. Hence the full failure union is at most

    sum_(q=1)^floor(k/2) 2q k^(2q) exp(-c qk/2) + 4^k exp(-c k^2/4).

At the declared delta, c>=8 log(k)/k. The two terms are bounded by2k^(-2)/(1-k^(-2))^2 and(4/k^2)^k. The cut-size partition covers boundary sizes, asymmetric rectangles and ties. Neither inter-cut independence nor a terminal-only sufficient criterion has been assumed.

On the resulting upper-endpoint event, a maximizing matrix of total2k^2 stays feasible at every later time because all entry upper bounds increase. The global row bound prevents growth in total throughput. Its right derivative, including at the upper endpoint, is therefore zero. Every later optimizer saturates all physical edges. Combining the endpoint failure bounds gives exactly the stated epsilon, simultaneously over both outer time intervals and all optimizers.

For fixed t<2 or t>2, delta_k tends to zero and epsilon_k tends to zero. The event forces the respective marginal and component values. The high-phase largest component is one, so its normalized size tends to zero. At t=2,

    k^2+(1-delta_k)S_k <= F_k(2) <= 2k^2

on the same event. Since E[S_k/k^2]=1 and Var(S_k/k^2)=1/k^2, the squeeze proves the critical throughput limit. There is no exchange of derivative and limit. The event failure series is summable along powers of two, giving eventual outer-phase statements under any common coupling by first Borel-Cantelli; no independence across sizes is needed.

The measurable-selection qualification is sound. With a fixed inequality matrix and finitely many possible bases, each nonsingular basis defines an affine candidate vertex in the demand parameters. Basis feasibility and optimality are Borel conditions. Choose the first feasible optimal basis in a fixed finite ordering. This gives a Borel optimizer, including on degeneracy regions. Any measurable choice has a measurable finite spare graph and component size. The universal endpoint event bounds all such choices at once; measurability is not used to choose a favorable optimizer.

Attempts to strengthen the result were deliberately rejected: a mixed cut can obstruct throughput despite ample offered totals at every terminal; an intermediate-time optimum can have different spare graphs; identical slopes x put the finite kink at1+1/x; the all-zero slope array makes the normalization undefined and lies outside the almost-sure positive-rate model. None falsifies the stated theorem. They explain why its restrictions matter.

Independent fresh controls enumerate every vertex of80 rational k=2 transportation polytopes, including137 optimal vertices and57 nontrivial optimal faces. Every optimum agrees with the separately enumerated cut formula, and every optimal vertex has the required terminal behavior in the strict/full-capacity phases. Convexity explains why testing a complete finite optimal face is stronger than sampling one solver's optimizer in these examples. This is not a substitute for the general deductions above.
