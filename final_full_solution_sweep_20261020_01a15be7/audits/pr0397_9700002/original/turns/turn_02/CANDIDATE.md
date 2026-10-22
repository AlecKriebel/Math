# Author turn 2: fixed-noise many-destination HOT model

Target 9700002 / AMR-096-0002. Date: 2026-10-03 UTC.

**Complete mathematical candidate for the model below, pending independent mathematical and source-fidelity review.** This supersedes turn 1 as the proposed answer. Turn 1 remains a qualified illustrative partial and is not erased.

## 1. Precise model

For H>=2 let T_H be the complete rooted binary tree of height H. Its two root subtrees each contain k=2^(H-1) leaves. Write L={1,...,k} for the left leaves and R={1,...,k} for the right leaves. The tree has N=4k-1 vertices and maximum degree three.

There is one commodity from every leaf i in L to every leaf j in R. All other entries of the demand matrix are zero. Each commodity uses the unique simple tree path, of length 2H. Thus there are k^2 commodities with k distinct destinations; this is not the one-destination model of turn 1.

Initially, each commodity demands one unit. For an edge e, let k_e be the number of leaves in the component below it, away from the root. Since that component lies entirely in L or entirely in R, its initial load is k k_e. Initial capacity is k k_e.

The network designer chooses edge-capacity increases at positive linear prices, with the requirement that all **twice-current** demands, two units per OD pair, can be carried. Topology is fixed. The designer then freezes the capacities.

After the design, take independent random variables

    X_ij ~ Exp(1),       i in L, j in R,

and define, using one common demand-growth parameter t>=1,

    d_ij(t) = 1 + (t-1) X_ij.

Every OD stream starts at the actual initial demand one and grows monotonically at its own independently sampled rate. Each rate has mean one and variance one, at every network size. Neither its distribution nor its variance is narrowed as H increases. Offered demand per stream has mean t and variance (t-1)^2. Capacity is designed before these future growth rates are used.

Let F_k(t) be the maximum total admitted demand, maximizing sum_ij y_ij subject to 0<=y_ij<=d_ij(t) and the tree capacities. This is the original admitted-demand objective, not a reachability surrogate. All admissible routing paths are simple; tree paths are unique.

The realized total offered demand is

    Q_k(t)=k^2+(t-1)S_k,       S_k=sum_ij X_ij>0.

Define the marginal satisfiability proportion by

    r_k(t)=F'_(k,+)(t)/S_k.

The right derivative is used at every breakpoint. This is the affine-growth version of Aldous's normalized marginal admitted demand, normalized by the actual offered-demand slope. It is not F_k(t)/Q_k(t).

For any optimal admitted-demand matrix, use its unique simple-path edge loads to define the spare graph E_k(t): an edge is retained exactly when its load is strictly less than capacity. We will prove the phase conclusions for **every** optimizer, without a favorable tie-break.

## 2. Candidate theorem

The following statements hold.

1. The unique least-cost doubled-demand design is

       C_e=2k k_e.

2. For every realization and every t>=1, the exact finite throughput is

       F_k(t)=min_(A subset L, B subset R) f_AB(t),

   where

       f_AB(t)=2k(k-|A|+|B|)
               + |A|(k-|B|)
               + (t-1) sum_(i in A,j notin B) X_ij.

   Let I_k(t) be the nonempty collection of minimizing cuts. Then the exact marginal is

       r_k(t)=min_((A,B) in I_k(t)) sum_(i in A,j notin B) X_ij / S_k.

   These formulas include critical times and all ties. They are finite analytic formulas; they do not assert an efficient enumeration or a closed elementary expectation at finite k.

3. Put

       delta_k=8 sqrt(log(k)/k),
       t_minus=2-delta_k,       t_plus=2+delta_k.

   For sufficiently large k, delta_k<1. With probability at least 1-epsilon_k, simultaneously:

   - for every t in [1,t_minus], all offered demand is admitted, r_k(t)=1, and the spare graph is the whole connected tree for every optimizer;
   - for every t>=t_plus, F_k(t)=2k^2, r_k(t)=0, and the spare graph is edgeless for every optimizer.

   A valid explicit failure bound is

       epsilon_k = 2 k^(-31)
                 + 2 k^(-2)/(1-k^(-2))^2
                 + (4/k^2)^k,

   which tends to zero. The constants are convenient rather than optimized.

4. Consequently, for every fixed 1<=t<2,

       r_k(t) -> 1,
       largest spare-component size / N -> 1,

   in probability. For every fixed t>2,

       r_k(t) -> 0,
       largest spare-component size / N -> 0,

   in probability. In fact the largest component equals N below the lower window and one above the upper window on the high-probability event in item 3. The entire transition is confined to a window of width 16 sqrt(log(k)/k) tending to zero.

5. For every fixed t>=1, including t=2,

       F_k(t)/k^2 -> min(t,2)

   in probability. We do not assert a limit for the finite-instance r_k(2), or a critical-window profile. The limiting throughput has no ordinary derivative at t=2; its left and right derivatives are one and zero. The finite min-cut formula nevertheless determines r_k at that time for every realization.

This is a concrete optimized network-and-demand model with a sharp joint marginal/fragmentation transition at the mean doubled-demand time. Its mechanism is endogenous averaging of k independent fixed-noise OD streams at each terminal, together with optimized cut capacities. It is a HOT/concentration construction, not a universal percolation law.

## 3. Least-cost design proof

The unique route for each of the k k_e commodities using edge e must traverse it. At doubled demand, each carries two units, so any feasible capacity enlargement requires C_e>=2k k_e. These lower bounds hold separately for every edge and are simultaneously feasible by routing all doubled demands along their tree paths. With strictly positive prices for capacity increments, the componentwise-minimum feasible vector is the unique cost minimizer. Thus the displayed capacities are derived from the optimization problem.

## 4. Reduction to bipartite flow

For any admitted matrix y, the load on a left leaf edge is its row sum, and the load on a right leaf edge is its column sum. Each of these capacities is 2k. Every other tree-edge load is the sum of the row sums, or of the column sums, over its k_e descendant terminals.

It follows that the tree constraints are equivalent to

       sum_j y_ij <= 2k for each i,
       sum_i y_ij <= 2k for each j,
       0<=y_ij<=d_ij(t).

Indeed, the individual leaf constraints are necessary, and summing them over a subtree gives every internal constraint, whose capacity is 2k k_e. This equivalence is exact.

Introduce an auxiliary directed network with a source connected to each L vertex by capacity 2k, arcs i->j of capacity d_ij(t), and arcs from each R vertex to the sink of capacity 2k. Feasible auxiliary flows are exactly feasible admitted matrices, with equal objectives. The elementary max-flow/min-cut theorem gives the displayed f_AB, where A is the set of left vertices on the source side of the cut, and B is the set of right vertices on that side.

Each f_AB is affine and nondecreasing in t. A finite minimum of affine functions is continuous, concave, and piecewise affine. Its right derivative is the minimum slope among the functions attaining the minimum at that point. All slopes are between zero and S_k. This proves the exact r formula and 0<=r_k<=1, including ties.

The global leaf cut gives F_k(t)<=2k^2 for all t. If this bound is attained, every row sum and every column sum must equal 2k. Every internal edge is then also saturated. Therefore **every** optimal admitted matrix gives an edgeless spare graph whenever F_k=2k^2, even if the admitted matrices themselves are nonunique.

Conversely, if all offered row sums and column sums are strictly less than 2k, admitting the whole demand matrix is feasible. It is the unique admitted matrix with maximum total Q_k(t), because every entry is individually bounded by its offered value. Each internal edge then has strictly smaller load than its capacity. Hence the whole tree is spare for every optimizer. These two conclusions concern the actual optimized loads, not artificial edge removal.

## 5. Exponential-sum tail bound

For q independent Exp(1) variables Z_l, write Z=sum_l Z_l and I(a)=a-1-log a. The moment-generating function is E[exp(lambda Z)]=(1-lambda)^(-q) for lambda<1. Chernoff's inequality, with lambda=1-1/a, gives

       P(Z>=qa) <= exp(-q I(a)),       a>1,
       P(Z<=qa) <= exp(-q I(a)),       0<a<1.

For 0<delta<1,

       I(1/(1-delta)) >= delta^2/2,
       I(1/(1+delta)) >= delta^2/8.

For the first bound, the derivative in delta of delta/(1-delta)+log(1-delta) is delta/(1-delta)^2>=delta. For the second, the exact expression log(1+delta)-delta/(1+delta) is the integral from zero to delta of x/(1+x)^2, at least delta^2/[2(1+delta)^2]>=delta^2/8. Both expressions vanish at zero.

## 6. Subcritical simultaneous event

At t=2-delta, an offered row sum is

       k+(1-delta) sum_(j=1)^k X_ij.

It is below 2k unless the exponential sum is at least k/(1-delta). The same statement holds for each column. Rows and columns need not be jointly independent: a union bound over their 2k marginal tail estimates suffices. Thus

       P(any offered row or column reaches 2k)
       <=2k exp(-k delta^2/2).

For delta=delta_k this is 2k^(-31). On the complementary event all row and column sums are strictly below capacity at t_minus, and also at every earlier t>=1 because all growth rates are positive. Section 4 gives full admission, r=1, and a connected full spare graph throughout that interval. Strict slack at the endpoint also ensures the right derivative there equals S_k.

## 7. Supercritical simultaneous cut bound

At t=2+delta, max flow equals 2k^2 if and only if every cut obeys

       sum_(i in A,j notin B) d_ij(t) >= 2k(|A|-|B|).

Cuts with |A|<=|B| automatically satisfy it. For any remaining cut, put D=R\B, a=|A|, d=|D|. Then a+d>k and its random rectangle has ad entries. The elementary identity

       ad - k(a+d-k) = (k-a)(k-d) >= 0

is important. Failure of this cut implies

       ad+(1+delta) sum_(A x D) X_ij < 2k(a+d-k) <=2ad,

and hence

       sum_(A x D) X_ij < ad/(1+delta).

For this one cut, failure probability is therefore at most exp(-c ad), with c=I(1/(1+delta))>=delta^2/8. No independence between different cuts is asserted or needed.

We now sum over **all** positive-demand cuts, not merely single-vertex cuts. Let q=min(a,d) and ell=k-max(a,d). Since a+d>k, 0<=ell<q. Their rectangle area is q(k-ell).

When q<=floor(k/2), for any fixed q and ell there are at most 2 binom(k,q) binom(k,ell) choices of the two sets, including their possible interchange. Summing ell=0,...,q-1 gives at most 2q k^(2q) choices. Also q(k-ell)>=qk/2. Thus the total contribution of these cuts is at most

       sum_(q=1)^floor(k/2) 2q k^(2q) exp(-c qk/2).

For q>k/2, the area exceeds k^2/4. There are at most 4^k choices of A,D in total, so this range contributes at most

       4^k exp(-c k^2/4).

With delta=8 sqrt(log(k)/k)<1, c>=8 log(k)/k. The first range is bounded by

       sum_(q=1)^infinity 2q k^(-2q)
       = 2 k^(-2)/(1-k^(-2))^2,

and the second by (4/k^2)^k. This proves the stated all-cuts bound. The use of a crude 4^k union bound alone for the smallest cuts would not work; the size split is essential.

When all cuts pass, the auxiliary flow has value 2k^2. Demands increase coordinatewise afterwards, so that same admitted flow stays feasible for every t>=t_plus. The global leaf cut still forbids values above 2k^2. Hence F remains exactly 2k^2 and r=0 at all such times, and every optimizer saturates every tree edge by Section 4.

Combining Sections 6 and 7 with a union bound proves the single high-probability event in the theorem.

## 8. Limits and the critical point

There are k^2 independent rate variables with mean and variance one, so

       S_k/k^2 ->1 in probability,
       Var(S_k/k^2)=1/k^2.

Outside the shrinking window the exact event above supplies the marginal and structural conclusions. For t<2 the throughput is Q_k(t) with probability tending to one; for t>2 it is 2k^2 with probability tending to one. At t=2, monotonicity gives

       F_k(t_minus)<=F_k(2)<=2k^2.

On the good event, the left bound is k^2+(1-delta_k)S_k. Dividing by k^2 and using delta_k->0 proves convergence to two. No derivative is exchanged with this limit.

The convergence is along the explicit binary-tree family k=2^(H-1). The failure bound is summable along this sequence, so under any common coupling of the instances the displayed outside-window conclusions even hold eventually almost surely by the first Borel--Cantelli lemma. Independence across network sizes is unnecessary. The in-probability formulation already suffices for the theorem.

At the critical time t=2, every finite instance is defined by the cut formulas, but neither a universal optimizer-independent spare graph nor a limiting r_k(2) is claimed. The full/no-edge statements are deliberately confined to the proved sides of the window.

## 9. Source fidelity and limitations

The source is Aldous's congestion problem, https://www.stat.berkeley.edu/~aldous/Research/OP/congestion.html . Its demand matrix is unrestricted, so traffic from every left leaf to every right leaf is an allowed, explicitly specialized matrix. The source permits fixed-topology cheapest capacity enlargement to handle twice current demand, followed by random demand growth. Those features are implemented literally here. The common parameter t has mean doubled demand at t=2.

The construction retains fixed microscopic randomness: the actual unnormalized OD demands have variance (t-1)^2 for every k. There is no independent aggregation parameter m and no shrinking per-stream noise. Averaging arises because each source sends to k destinations and each destination receives from k sources. Thus terminal relative fluctuations become small as a consequence of this many-destination network sequence. The resulting sharp transition is still a concentration-and-design phenomenon; it is not claimed to arise from a nontrivial independent-bond critical probability or universal critical exponents.

The source gives linear-in-time variance as one illustrative random-growth choice. Our random-slope process has quadratic variance. It preserves monotone traffic growth and an ordinary quenched marginal derivative. We do not claim the optional linear-variance example was solved, or hide the difference by redefining an expectation as a pathwise derivative.

This model is a bounded-degree tree with many sources and many destinations. It is not a generic cyclic traffic network. Its graph geometry and OD pattern make internal capacity constraints reducible to terminal constraints, and the proof openly relies on this tractability. The model supplies a sharp giant-to-isolated-vertices transition; it does not describe a critical component-size distribution inside the shrinking window.

Finite r_k(t) has the explicit min-cut derivative formula. The macroscopic r is analytically one below two and zero above two; a finite-k expectation or nontrivial critical-window curve is not supplied. Whether that level of analytic description is the 'right' toy model sought by a conceptual source is a separate source-fidelity judgment, not a theorem proved by these calculations.

Total admitted throughput saturates rather than dropping. It is the marginal absorption of extra demand that drops, in accordance with the source's observable. Spare-capacity conclusions on both sides hold for every optimal simple-path flow, without assuming a favorable allocation.

Only the HOT alternative is addressed. There is no SOC or adaptive-growth claim, and no claim covering arbitrary demand matrices or costs that change the topology.

## 10. Prior credit and review request

The complete source/prior audit remains in ../../SOURCE_GATE.md. Prior random-capacity multicommodity-flow theory and prior demand/percolation frameworks are credited there and in turn 1. Max-flow/min-cut, exponential Chernoff bounds, and concentration of independent traffic are standard ingredients. A claim that no analytic congestion model existed would be false.

Further directly relevant prior credit found during this turn is Karp, Motwani, and Nisan (1993), *Probabilistic Analysis of Network Flow Algorithms*, Mathematics of Operations Research 18(1):71-97, https://doi.org/10.1287/moor.18.1.71 . Its publisher abstract describes high-probability feasibility for random capacitated transportation and source/sink-isolating minimum cuts. The auxiliary random-transport result here is not claimed as novel. A Northwestern primary discussion paper at https://www.kellogg.northwestern.edu/research/math/papers/660.pdf likewise treats asymptotic random capacitated transportation, but its full PDF could not be inspected reliably, so no theorem-level comparison with that document is asserted.

No novelty claim is made for either the ingredients or the combined construction. The item to be independently evaluated is the specified cheapest-design physical-tree model and optimizer-independent coupling of its marginal-demand and spare-connectivity observables; whether that construction already exists in the literature remains a separate historical check.

Independent review is requested on: (a) cut counting and inequalities; (b) equivalence of physical tree and auxiliary flows; (c) all-optimizer spare-graph conclusions; (d) the affine-growth normalization and optional linear-variance example; (e) whether this concentration-based HOT construction genuinely answers the primary conceptual request; and (f) novelty relative to existing dense bipartite transportation results. No full-resolution or novelty verdict is made before that review.

Author turn count: 2/5. No remote write or external communication.
