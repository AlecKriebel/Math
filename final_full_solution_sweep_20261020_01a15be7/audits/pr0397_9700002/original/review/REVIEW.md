# Independent mathematical and source-fidelity review: public projection

Date: 2026-10-03 UTC.

## Verdict

**PASS: the turn-2 theorem is mathematically sound as stated, and it supports a complete, explicitly specialized conceptual-model response to the extracted existence/model-construction task.** There is no mathematical repair that warrants spending another author turn. This is an acceptable HOT toy example, not a certification that Aldous's open-ended search has a uniquely correct or historically new resolution. The honest result is a rigorous example exhibiting the requested joint signature under declared assumptions.

The review distinguishes three conclusions:

1. **Mathematical correctness:** accepted. No blocking error found in the model, optimization, all-cuts proof, probability bound, endpoint handling, or optimizer quantifiers.
2. **Source adequacy:** accepted for a specialized existence response. The result analytically controls both the admitted-demand marginal and physical spare connectivity under a least-cost doubled-demand design. It is not merely a finite saturation picture or a simulated analogue.
3. **Historical novelty / broader explanatory universality:** not established. Classical random-transport feasibility is directly relevant prior work, and the sparse physical tree has a highly specialized dense traffic matrix and redundant internal constraints.

Two of five substantive author turns have been used. Three remain unused. The audit itself is not a new author turn. Preserve turn 1 as an illustrative partial, not a second full solution.

## Public provenance note

This public copy preserves the complete original verdict and every section from "Primary-source judgment" through the end, without changing any mathematical review text. Only the original execution/delegation header and local input/replay-location section are omitted. Their replacement is this provenance note; this is not a byte-identical copy of the full original review.

Original review SHA256: 7a37a97ebb053e8dfbb16a7ec96299c70ffc315c0455db408ab0b25462b2921b.
Original review-manifest SHA256: 437537d5153465e84e4b2dfe9e99b70e398dfacb834ed7415caacad8494208bd.
Reviewed author-packet manifest SHA256: 9bcd9dfb367e1bbf810c5f49e20ccdce89e143b35fbbe2eae146d2d4d5b1b3b3.

The selected proof files retain their original bytes. Public reproducibility uses a separately identified portable derivative of the independent test program; its mathematical test body is unchanged. See PUBLIC_PROJECTION.json and REPLAY_ALL.py. Third-party source documents are linked, not republished.

## Primary-source judgment

Aldous's [original problem](https://www.stat.berkeley.edu/~aldous/Research/OP/congestion.html), read in full, begins with unrestricted multicommodity demands. It explicitly allows fixed topology with cheapest capacity increases to meet doubled current demand, followed by random demand growth. Linear mean and variance are introduced as an example. Its requested signature couples a near-one-to-near-zero marginal change with fragmentation of the spare graph. The text asks for a useful tractable model rather than a formally unique conjecture.

My source judgment is therefore permissive but bounded: fixed topology, cross-tree-only demand, random affine slopes, and an asymptotic graph family are defensible specializations. Neither a particular variance law, cycles, a bounded number of OD streams per terminal, nor universal critical exponents is specified as mandatory. The declaration of these choices matters. The adjective “right” remains a scientific modeling judgment, which a proof cannot certify.

## Mathematical audit

### 1. Physical network and traffic scaling

The height-H complete binary tree has 2k leaves, k in each root subtree, with k=2^(H-1), N=4k-1 vertices, and maximum degree three. Every left-to-right route has 2H edges. Its two top edges carry every commodity; a nonroot edge below the root carries precisely k*k_e baseline units, where k_e is its number of descendant terminals. These counts are correct.

There are k^2 OD streams on O(k) physical vertices. This is **sparse topology with dense OD traffic**, not a sparse-traffic model. Baseline total demand is k^2, leaf capacity after design is 2k, and each top edge has capacity 2k^2. Those capacities grow with the graph family. Each individual graph and its capacities are then held fixed as t varies. No topological evolution is being smuggled into the post-design time parameter.

The X_ij are sampled after design and retain the identical Exp(1) law as k changes. At fixed t>1, each actual OD demand has variance (t-1)^2, independent of k. Each terminal sums k such streams and has relative aggregate fluctuations of order k^(-1/2). The microscopic law does not artificially collapse, although the relevant terminal loads do concentrate. The number of OD streams is the aggregation source. This is the precise, genuinely new modeling change from turn 1.

### 2. Cheapest design

Removing edge e identifies kk_e commodities whose unique simple paths must use it. Carrying doubled demand forces capacity at least 2kk_e on that edge. These separate lower bounds are simultaneously feasible. Because every capacity-increment price is strictly positive, their componentwise minimum is the unique minimizer of the stated linear cost. No optimization over topology, robustness, or future rate realizations is asserted. Initial capacities kk_e and final capacities 2kk_e are consistent with an enlargement problem.

### 3. Physical-tree / auxiliary-flow equivalence

The leaf edge loads are exactly row and column sums of the admitted matrix. Their capacities are 2k. Every internal load is a sum over descendant terminal loads, and its capacity is the corresponding sum of terminal capacities. Therefore the leaf constraints imply all internal constraints; the converse is immediate because leaf constraints are part of the physical problem. No route splitting, cancellation, circulation, or unphysical demand admission is introduced.

In the auxiliary directed transportation network, a cut placing A on the left and B on the right on the source side has capacity

2k(k-|A|+|B|) + sum_(i in A,j not in B) d_ij(t).

Substitution of d_ij(t)=1+(t-1)X_ij gives the candidate's f_AB exactly. The objective remains the original sum of admitted commodities. The auxiliary graph is a proof device; spare-component claims are evaluated on the physical tree.

### 4. Finite derivative and normalization

A finite minimum of affine functions is continuous, concave, piecewise affine. At a crossing, its right derivative is the smallest slope among the active cuts; inactive cuts cannot affect a sufficiently small right neighborhood. All those slopes lie between zero and S_k. Thus the exact marginal formula and 0<=r_k<=1 are correct, including ties.

The convention r_k=F'_(k,+)/S_k is exactly dF/dQ for this affine demand path. It is a declared extension of the proportional-demand normalization. If one insists on retaining the initial baseline denominator D=k^2, the finite subcritical value is S_k/k^2 rather than identically one. Since S_k/k^2 tends to one, the same macroscopic near-one-to-zero conclusion follows. The exact finite “one” statement should always retain its actual-offered-slope convention.

Neither F/Q nor a reachability fraction has replaced the admitted-demand derivative. Also, total throughput saturates; it does not decline.

### 5. All-optimizer spare graph

If every offered terminal sum is strictly below 2k, accepting every entry is feasible and attains the sum of all coordinatewise upper bounds. Every maximizing admitted matrix must equal the full demand matrix. Every internal edge then also has strict slack. Hence every optimizer has the entire physical tree spare.

If F=2k^2, all k row sums, each at most 2k, must equal 2k; the same holds for columns. Every internal edge is then saturated by summation. Thus every optimizer gives the edgeless spare graph, even though the matrix itself need not be unique. This argument does not depend on choosing a favorable LP optimum.

These are genuine outer-phase assertions. They cannot be extended to arbitrary critical-time instances: the independent test includes k=2, t=2 and positive rates [[3,3],[0.1,0.1]], for which two optimal matrices have respectively four and five spare edges. The candidate correctly makes no such extension.

### 6. Subcritical event and threshold strictness

At t_minus=2-delta, a terminal reaches its capacity only if its Gamma(k,1) slope sum is at least k/(1-delta). Chernoff gives at most exp(-k*delta^2/2) for each of the 2k terminals. Their overlap is irrelevant to the union bound. For delta=8*sqrt(log(k)/k), the failure probability is 2k^(-31), as claimed.

The good event excludes equality, so all edges have strict slack at the lower endpoint. With finitely many constraints and finite slopes, slack persists in a nonzero right neighborhood of that endpoint. Consequently the right derivative there is S_k, not just a left derivative. Monotonicity supplies the entire interval down to t=1.

### 7. Supercritical all-cuts estimate

Writing D=R\B, a=|A|, d=|D|, only a+d>k can require a positive OD-cut lower bound. All other cuts automatically pass because demands are nonnegative. For the remaining cuts,

ad-k(a+d-k)=(k-a)(k-d)>=0.

A failing cut at t_plus has rectangle slope sum below [2k(a+d-k)-ad]/(1+delta), hence below ad/(1+delta). If the former threshold is nonpositive, the cut cannot fail; using the latter threshold merely overcounts a harmless event. The Gamma lower-tail bound exp(-c ad), c>=delta^2/8, is valid.

For q=min(a,d), ell=k-max(a,d), the constraint is exactly 0<=ell<q, and ad=q(k-ell). For q<=floor(k/2), there are at most 2 binom(k,q) binom(k,ell) cuts of those sizes. Summing the ell values and using the crude power bounds gives 2q k^(2q), while the area is at least qk/2. With c>=8 log(k)/k, the contribution is bounded by sum 2q k^(-2q)=2k^(-2)/(1-k^(-2))^2.

For q>k/2, every rectangle area exceeds k^2/4, and at most 4^k ordered pairs of subsets exist. Their total contribution is at most (4/k^2)^k. These two classes cover every positive-demand cut. Overcounting symmetric or full rectangles is harmless. Independence between cuts is never used.

This is a real all-cut proof. Terminal total checks alone would be insufficient; an independent k=4 obstruction has every offered terminal sum above eight, yet maximum throughput 156/5<32 because a 3-by-2 rectangle violates a mixed cut.

### 8. Upper endpoint and uniformity over time

When all cuts pass at t_plus, the value is 2k^2. The same feasible matrix stays feasible at all later times because every offered entry is nondecreasing, and the global terminal cut prevents any larger value. The right derivative at the upper endpoint is therefore zero, even if one of the relevant cut conditions holds at equality. Every optimizer then saturates every physical edge for all later times.

Combining the two events gives precisely the displayed epsilon_k. The resulting event controls uncountably many times through deterministic monotonicity, so a further time-union bound is unnecessary.

### 9. Graph sequence, orders of limits, and the critical point

The asymptotic parameter is k=2^(H-1) tending to infinity. For each finite member, t is a post-design demand parameter, and its value function remains a finite piecewise-linear curve with random kinks. The theorem takes fixed t<2 or fixed t>2 and then the graph-size limit; the uniform event also handles times outside the stated shrinking window. It does not assert that every finite sample switches exactly at t=2.

The half-window delta_k tends to zero. The first power-of-two k for which the stated delta<1 is k=512 (H=10, N=2047). The guaranteed width there is about 1.766; the constants are conservative. The proof supplies an **O(sqrt(log(k)/k)) upper bound** on a transition window, not a matching lower bound or a determination of the true critical scaling.

On the good event the largest physical spare component equals N on the lower side and one on the upper side. Therefore it meets the giant-to-small criterion in a stronger form than merely vanishing relative density.

S_k/k^2 tends to one by its variance 1/k^2. The critical throughput bound uses monotonicity and the already proved lower endpoint. No derivative is exchanged with a singular limit. At t=2 the limiting throughput is two; no limit for r_k(2) or optimizer-independent spare graph is claimed. The input's Borel-Cantelli strengthening is valid since epsilon_k is summable along powers of two under any common coupling; independence across network sizes is unnecessary.

## Why turn 2 clears the first-turn limitation

Turn 1 is internally correct, including its explicit negative control: at fixed aggregation m and every finite t>1, the spare giant has positive limiting density. Its advertised sharp joint limit relied on choosing m to diverge, which narrowed each commodity's growth-rate law.

Turn 2 instead increases the number of actual source-destination commodities, keeps each rate law fixed, and proves that *all* terminal and mixed-cut obstructions disappear outside a shrinking window. It does not simply rename m as k in the same scalar formula: the additional destination constraints create an actual transportation feasibility problem, and the mixed-cut proof is necessary to solve it.

It remains an averaging-and-design transition. Tree constraints are deliberately redundant beyond the leaves, every OD crosses the same root interface, and positive linear costs make designed capacities exactly tight at the target. These properties explain both tractability and simultaneous saturation. They narrow its explanatory reach, but do not invalidate it as a simple example. Rejecting it because it lacks cyclic rerouting, fixed per-terminal traffic, or a nontrivial percolation exponent would impose additional requirements absent from the extracted task.

The finite min-cut identity alone would not justify calling the problem answered: a generic exponential enumeration is not much analytic insight. Here the explicit all-cut probability estimate and the resulting marginal/structural phase theorem provide the substantive analytic calculation. A finite expected curve or critical-window distribution would be valuable further work, not a demonstrated obligation in this task.

## Prior work and source-fidelity limits

- Karp, Motwani and Nisan, *Probabilistic Analysis of Network Flow Algorithms*, Mathematics of Operations Research 18(1):71-97 (1993), [publisher](https://pubsonline.informs.org/doi/10.1287/moor.18.1.71), was independently checked. Its abstract covers high-probability random capacitated-transportation feasibility and source/sink-isolating minimum cuts. A [Berkeley technical report](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1988/5854.html) predates the journal article. The core random-transport phenomenon is longstanding.
- Hassin and Zemel, *Probabilistic Analysis of the Capacitated Transportation Problem*, Mathematics of Operations Research 13(1):80-89 (1988), [publisher](https://pubsonline.informs.org/doi/10.1287/moor.13.1.80), is the published antecedent associated with the packet's unnamed Northwestern discussion paper. The [author-hosted paper](https://www.tau.ac.il/~hassin/transportation_88.pdf) was downloaded and pages 80-82 visually inspected, including its formulation and first theorem. It establishes asymptotic random-capacity transportation feasibility under its own assumptions. This review does not claim its theorem directly supplies the candidate's near-capacity shrinking-window bound.

Add the full Hassin-Zemel citation to any eventual account. That is an attribution improvement, not a repair to the proof. No exhaustive historical search or theorem-by-theorem literature equivalence audit has been completed. Do not present the auxiliary feasibility result, Chernoff technique, or combined construction as proven novel. The earlier source gate's other literature statements were read but not all independently re-audited paper by paper here.

## Independent validation results

Both author reruns: all assertions passed, exact output-check byte matches.

Additional checks: all passed.

- 405 exact rational transportation / all-cut / physical-LP cases; maximum physical objective discrepancy zero.
- 153 true envelope kinks checked with exact rational left/right slopes and exact flow at the kink.
- Six complete optimal-face cases with 200 physical edge extrema; maximum numerical load-range width about 2.14e-14.
- A separate mixed-cut obstruction defeating terminal-sum-only reasoning.
- Exact deterministic ties at t=2, verifying zero right marginal and no strict spare edges.
- A positive-rate critical-time example demonstrating optimizer-dependent spare graphs within the excluded region.
- 88,559 positive-cut size classes, exact multiplicities, gamma lower-tail comparisons, and 1,000 tail-constant checks.
- First admissible power-of-two family member for delta<1 verified.

These tests supplement, rather than replace, the proof audit. They neither simulate the exponentially unlikely full large-k bad event nor establish historical novelty.

## Recommended wording and disposition

Recommended result description:

> A rigorous, specialized HOT toy model has been constructed and independently checked. With fixed independent OD-rate randomness and a cheapest doubled-demand tree design, its marginal admitted fraction and physical spare graph undergo a sharp joint transition outside an explicitly bounded shrinking window. This supplies a conceptual example of the requested phenomenon; historical novelty and universality are not claimed.

Retain the disclosed affine/quadratic-variance demand law, the actual-slope normalization, dense OD scaling, finite-size/critical-point exclusions, and classical transportation credit. No need to spend the remaining three author turns solely to strengthen an already adequate existence response. More stringent goals would require an explicitly new target, not a retroactive claim that this theorem proves them.
