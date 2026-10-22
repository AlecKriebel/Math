# Five substantive approaches

The five entries are distinct mathematical lines of attack, not five web searches or numerical parameter choices. They share the same fixed kernel and positive finite-measure class. The original arbitrary-measurable pointwise problem remains unresolved; the recommended campaign count is `5/5`, status `unsolved`, subject to fresh independent audit. No remote state was changed by the author.

## 1. Endpoint estimates and rearrangement characterization

Derived the exact set-integral bound with constant `2^alpha/(1-alpha)` and the weak `L^(1/alpha)` necessary condition. Tested whether endpoint distribution data could be sufficient. Constructed separated intervals with heights `2^n` and lengths `2^(-n/alpha)`, and a mass-one absolutely continuous test measure with bounded potential but infinite obstacle pairing. Rearranged the same spikes next to zero and proved domination by one atom. This supplies equimeasurable finite-valued counterexamples to any rearrangement-only criterion, not just failure of one chosen norm. Both functions are also integrable. See sections 1 and 2 of `PARTIAL_RESULTS.md`.

## 2. Constructive interval/atomic majorants

Built an explicit positive atomic majorant from a weighted interval cover with finite sum `sum b_j |I_j|^alpha`. Derived its exact mass. Tested necessity using the truncated atomic kernel `|x|^(-alpha)` on `0<|x|<=1`, with the origin reset to zero. The weight `|x|^(alpha-1)` proves that every such cover has infinite cost, even though one atom is a valid majorant. Thus the cover test is a strict sufficient condition. See section 5.

## 3. Functional separation and mass compactness

Replaced point constraints by smooth-density integral constraints whose kernel transforms lie in `C_0(R)`. Proved the finite-intersection property by nonnegative finite-dimensional separation and obtained a minimizing positive measure by weak-star compactness. This yields an exact dual criterion with mass attainment for almost-everywhere domination. Proved that local averages recover every potential value, giving the same exact criterion for lower semicontinuous pointwise obstacles. The remaining existential lower-semicontinuous-envelope reformulation is identified as a reformulation, not a solution of the arbitrary-measurable target. See section 3.

## 4. Singular exceptional sets and null-set repair

First proved arbitrary countable values can be handled with an arbitrarily small atomic measure. Then tested whether Lebesgue-null exceptional sets are always harmless. Constructed, for each alpha, a two-interval null Cantor set and an atomless probability measure whose Riesz potential is uniformly bounded by a direct geometric-series estimate. A finite-valued Borel obstacle on disjoint Cantor cylinders has infinite pairing against that measure, and so no pointwise majorant, despite being zero almost everywhere. This decisively prevents using approach 3 as a full solution. See section 4.

## 5. General measure duality and finite-program limits

Derived the necessary bounded-potential-measure test, which detects the singular example. Investigated a compactness/separation extension from smooth tests to pointwise constraints. Gave an explicit failure of weak-star closedness and proved that every finite or dense-countable set of point constraints is feasible with arbitrarily small mass, while the obstacle `1` on all of R is impossible. Also exhibited failure of mass attainment for a singleton obstacle. These identify the exact missing capacity/exceptional-set step rather than hiding it inside an unproved infinite-program duality. Sufficiency of the general singular test is not claimed. See section 6.

## Controls and limitations

The portable controls test exact scaling identities, geometric tails, rearrangement-cell lengths, finite-pairing lower bounds, Cantor-cylinder masses and gaps, strict rational bounds for the illustrative `alpha=1/2` constants, and explicit scope records. They do not establish infinite-dimensional compactness, analytic inequalities for all real parameters, or pointwise completeness. Those are proof obligations addressed in the prose and still subject to independent review.

