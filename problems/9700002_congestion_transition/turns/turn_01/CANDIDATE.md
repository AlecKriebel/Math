# Author turn 1: an optimized binary-tree congestion model

Date: 2026-10-03 UTC. Target: 9700002 / AMR-096-0002.

**Status: complete candidate for the precise existence statement below; not yet independently reviewed.** The model is an illustrative high-aggregation HOT construction. It is not claimed to characterize arbitrary optimized networks or to settle every interpretation of Aldous's conceptual request.

## 1. Model and exact statement

Let T_h be the rooted complete binary tree of height h, with n=2^h leaves and N=2n-1 vertices. Every edge has a positive linear capacity-improvement price. Initially each leaf generates one unit of demand per unit time, all destined for the root. Initial edge capacity equals the number k_e of leaves below edge e.

At the design stage, increase capacities at least total cost so that twice the current demand can be carried. After design, freeze capacities. This is precisely an allowed fixed-topology capacity-enlargement operation; topology is not a decision variable.

For an integer m>=1, independently at each leaf i, draw

    W_i = (Z_i1 + ... + Z_im)/m,
    with all Z_ij independent exponential random variables of mean one.

Post-design traffic demand from leaf i to the root is

    d_i(t) = 1 + (t-1) W_i,       t >= 1.

Thus demand starts at the actual design-time unit demand, increases monotonically, and has mean t. Randomness represents an average of m independent client growth rates. Its variance is (t-1)^2/m, not linear in t. Aldous presents a linear-variance growth process as an example, not as a mandatory hypothesis. We make this modeling difference explicit.

Admitted traffic y_i must obey 0<=y_i<=d_i(t). Route each commodity along a simple path to the root; there is exactly one such path in a tree. Shared edge loads must not exceed capacities. Let F_h,m(t) be the maximum of sum_i y_i.

For a realized collection of W_i, total offered demand has constant post-design slope S_h=sum_i W_i. Define the normalized marginal admitted fraction by the right derivative

    r_h,m(t) = F'_h,m,+ (t) / S_h.

This is the marginal-demand observable, not the fraction of currently served demand. Using a right derivative fixes all breakpoints. The normalization is the actual total demand-growth slope. It is the natural extension of D1'(t)/D to this affine, randomly growing demand family.

Define the spare-capacity graph on all N vertices by retaining exactly the edges whose load in an optimal simple-path routing is strictly below capacity. Let L_h,m(t) be its largest-component size.

### Candidate theorem

The design is uniquely optimal and has capacities C_e=2k_e. For every realization and t>=1,

    F_h,m(t) = sum_i min{1+(t-1)W_i, 2},
    r_h,m(t) = [sum_i W_i 1{(t-1)W_i<1}]/S_h.

Optimal admitted quantities and simple-path edge loads are unique. An edge is spare exactly when at least one leaf below it satisfies (t-1)W_i<1. The spare graph has one root component and otherwise isolated vertices.

For t>1 put a=1/(t-1), z=ma, and

    p_m(t) = 1 - exp(-z) sum_{k=0}^{m-1} z^k/k!,
    R_m(t) = 1 - exp(-z) sum_{k=0}^{m} z^k/k!.

At t=1 set p_m=R_m=1. Define

    G(p) = sum_{j=0}^infinity 2^(-j-1) [1-(1-p)^(2^j)].

For any deterministic sequence m=m_h>=1 and deterministic times t=t_h>=1,

    r_h,m_h(t_h) - R_m_h(t_h) -> 0 in probability,
    L_h,m_h(t_h)/N - G(p_m_h(t_h)) -> 0 in probability.

Consequently, choose the concrete network family m_h=h. For every fixed 1<=t<2,

    r_h,h(t) -> 1,       L_h,h(t)/N -> 1,

whereas for every fixed t>2,

    r_h,h(t) -> 0,       L_h,h(t)/N -> 0.

Thus the optimized marginal curve and the giant-component density both change at the design target t=2. Below it there is one spare-capacity component containing all but o_p(N) vertices. Above it every spare-capacity component is o_p(N).

The transition window is explicit. For every fixed real x, at t_h=2+x/sqrt(m_h), with any m_h->infinity,

    r_h,m_h(t_h) -> Phi(-x),
    L_h,m_h(t_h)/N -> G(Phi(-x)),

where Phi is the standard normal distribution function. Eventually t_h>=1. At t=2 the limits are 1/2 and G(1/2), respectively. This is an analytic smoothing profile, not a claim of a discontinuity in a finite stochastic sample or of independent bond percolation.

## 2. Proof of the capacity-design claim

Removing edge e separates its k_e descendant leaves from the root. Each must send two units at the design target, so any feasible enlargement must have capacity at least 2k_e on e. These componentwise bounds are simultaneously achieved by routing two units along each leaf-root path. Since each improvement price is strictly positive, the unique least-cost capacity vector is 2k_e. No unproved network-design optimization assumption is used.

## 3. Exact optimized throughput and routing

The edge incident to leaf i has capacity two. Therefore any feasible admitted amount satisfies y_i<=min{d_i(t),2}. Summing gives the displayed upper bound for F.

Set y_i=min{d_i(t),2}. On edge e the resulting load is the sum of y_i over its k_e descendant leaves, at most 2k_e. Hence this vector is feasible, attaining the upper bound. Every maximizer must attain every individual upper bound, because none of the other coordinates can exceed its own. Admitted amounts are therefore unique. Tree simple paths then give unique loads on all edges.

At a time when d_i(t)=2, the right derivative of its clipped demand is zero; otherwise it is W_i below capacity and zero above. Summation and division by S_h>0 gives the exact r formula. There is no choice of optimizer or hidden load-based tie-break.

The path formulation excludes flow circulations that carry no commodity. If flows are instead represented by conservation equations admitting gratuitous circulations, use the canonical cycle-free representative before defining spare capacity. Arbitrary wasteful optimal circulations are not covered by the spare-graph claim.

## 4. Exact spare graph

The slack on an edge e is

    C_e - load_e = sum_{i below e} (2-y_i).

All terms are nonnegative. The edge is spare if and only if at least one of its descendant leaves is under capacity. Consequently, all spare edges are precisely the union of the root paths from under-capacity leaves. This union is connected whenever it is nonempty. A subtree with no under-capacity leaf has every edge saturated, so each vertex outside the root component is isolated. The largest component is therefore the root component, including the case where its size is one.

For independent Gamma(m, rate m) variables W_i, a leaf is under capacity with probability p_m(t). This yields an exact finite expression:

    E[L_h,m(t)] = 1 + sum_{j=0}^{h-1} 2^(h-j) [1-(1-p_m(t))^(2^j)].

Here j is the height of a vertex above the leaves, and the root is counted separately. Dividing by 2^(h+1)-1, the expression differs from G(p_m(t)) by O(2^-h), uniformly in p_m in [0,1]. For example the absolute error is at most 4/2^h, which suffices.

To see concentration without independence of edge states, reveal the independent active-leaf indicators one at a time. Changing one indicator changes the root-component size by at most h: only its path to the root can change membership, and the root is already counted. The Doob martingale increments have magnitude at most h; orthogonality gives Var(L)<=nh^2. Chebyshev's inequality yields

    P(|L-E L|>epsilon N) <= nh^2/(epsilon^2 N^2) -> 0.

This bound is uniform in the active probability, so it applies to m_h and t_h varying with h. Together with the uniform mean approximation it proves the giant-density formula.

## 5. Exact analytic marginal curve

The Gamma density is f_m(w)=m^m w^(m-1) exp(-mw)/(m-1)! for w>0. Integration gives

    p_m(t) = P(W<a),
    R_m(t) = E[W 1{W<a}].

The two finite-sum formulas follow by integrating the gamma density and the size-weighted gamma density. Equivalently, R_m(t) is the Gamma(m+1,rate m) distribution function at a.

For completeness, the exact expected optimal throughput per source is

    H_m(t) = E[F_h,m(t)]/n
           = 2 - p_m(t) + (t-1)R_m(t),      t>1,
    H_m(1) = 1,
    H'_m(t) = R_m(t).

The last identity can be obtained by differentiating the clipped-demand integral; domination by W, whose expectation is one, justifies differentiation. The expectation-normalized derivative is thus exactly R_m for every finite h. The quenched marginal r_h,m uses S_h rather than E[S_h]=n; it is not asserted to have expectation exactly R_m.

To prove the quenched limit, let A_i=W_i 1{W_i<a}. Uniformly in m>=1 and a,

    E W_i=1,   E W_i^2=1+1/m<=2,
    E A_i=R_m,  Var(A_i)<=2.

Therefore S_h/n->1 and n^-1 sum_i A_i-R_m->0 in probability, with Chebyshev bounds uniform in m and t. Dividing by S_h/n proves the first convergence claim. This also verifies that the normalization is not being replaced silently by an expectation.

## 6. Sharp joint transition and window

For fixed 1<t<2 we have a>1. Since Var(W)=1/m, W->1 in probability as m->infinity, so p_m->1. Uniform integrability from E W^2<=2 gives R_m->1. For t>2, a<1, the same reasoning gives p_m,R_m->0. At t=1 the assertion is exact.

The series defining G converges uniformly on [0,1], because the summands are bounded by 2^-j-1. Thus G is continuous, G(0)=0, and G(1)=1. Apply the results of Sections 4 and 5 with m_h=h to obtain both macroscopic limits. This establishes a meaningful sparse bounded-degree graph limit: maximum degree is three, and all commodity paths have length h, which diverges.

For the window t=2+x/sqrt(m), write a=1/(1+x/sqrt(m)). The centered Gamma(m,m) variable sqrt(m)(W-1) tends to a standard normal. Since sqrt(m)(a-1)->-x, p_m(t)->Phi(-x). Using the Gamma(m+1,m) representation, the standardized threshold for R_m also tends to -x, so R_m(t)->Phi(-x). Continuity of G and the uniform-in-m,h concentration already proved give the stated joint window limits. No exchange of a derivative and a singular limiting function is needed.

## 7. Why this is qualified, and what it does not prove

- Capacities are derived by a genuine cost minimization for twice the actual design-time demand. They are not prescribed from desired edge-open probabilities.
- Throughput is the full maximum admitted multicommodity demand in the specified network. The marginal and spare graph are consequences of that optimum.
- The graph family is sparse and bounded-degree, rather than a star or a collection of independent edges. Its leaf-root paths share internal capacity constraints. Their redundancy after clipping is proved, not assumed.
- Nevertheless, this is an especially tractable one-destination tree model. It does not address cyclic route competition or generic all-pairs demand.
- The sharp transition uses increasing aggregation m_h->infinity, explicitly m_h=h. For fixed m and any finite t>1, p_m(t)>0 and G(p_m(t))>0. Therefore **there is no finite-time loss of the giant component in the fixed-m, h->infinity limit**. This negative control must accompany every description of the result.
- At finite h each quenched r is a step function with random breakpoints; the analytic expected curve R_m is smooth. The discontinuous 1-to-0 limit is a concentration phenomenon of the chosen joint limit. It is not a demonstration of universal critical exponents or ordinary independent-bond percolation.
- Throughput itself does not collapse: its normalized limit is min{t,2}. Marginal ability to absorb additional demand collapses, exactly the intended distinction.
- Random post-design slopes have quadratic-in-time variance. The source's illustrative linear-variance process is not implemented. If linear variance or a fixed nondegenerate microscopic demand law is made a required interpretation, this candidate does not meet that stronger target.
- Only the HOT/design alternative is treated. No claim is made about self-organized criticality from ongoing adaptive growth.
- Aldous asks for the 'right' toy model, a conceptual criterion that is not a unique mathematical theorem. Independent review should separately assess correctness, source fidelity, and whether this construction is an interesting answer to that request. Correctness of the precise theorem alone does not settle those judgments.

## 8. Prior credit

The source and current literature audit is in ../../SOURCE_GATE.md. Aldous's multicommodity-flow setting and capacity-design question are the source, not our invention. Analytic random-capacity flow results of Aldous--McDiarmid--Scott (2009) and Khandwawala--Sundaresan (2010), demand-weighted percolation of Hamedmoghadam et al. (2021), and analytical/algorithmic congestion work of Di Meco et al. and Chen--Wu (2024) precede this construction. We claim neither that analytic congestion models were previously absent nor that demand/connectivity coupling is a new idea. The candidate contribution, if judged worthwhile and novel, is this exact optimized tree construction with its two observables and joint-limit formulas.

No external communication or remote write was performed. Author turn count: 1/5; all mathematical assertions in this packet are candidate assertions pending independent verification.
