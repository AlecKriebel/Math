# Turn 3: a conditioned subdivision-edge representation and optimal-event search

2026-10-02. Third substantive author turn for 30003338. **Original target unresolved, 3/5.** The conditional theorem and nonlinear event subclass below are rigorous scoped results. They do not remove the conditioning for arbitrary increasing events or cover all bipartite graphs. No historical novelty claim is made.

## 1. A genuinely different subdivision setting

Let H=(B,E) be a finite loopless multigraph. Replace each edge e by a length-two path through a new vertex a_e. The resulting bipartite graph has A={a_e:e∈E} as the observed class and B as the original vertices. Thus every observed vertex has degree two. This is different from turn 1, where the integrated-out B vertices had degree at most two.

Let f be uniform among proper q-colorings, q≥3, and let S={e:f(a_e)=0}. For W⊂B put

    C_W = {f(v)≠0 for every v∈W},
    J = {e∈E: both endpoints of e belong to W}.

The event C_W has positive probability. Empty or isolated cases are allowed; a later edge-cover requirement is impossible for an isolated member of W and then the corresponding assertion is trivial.

**Conditional theorem.** Given C_W, the zero-edge indicator family (1_(e∈S))_(e∈J) is positively associated.

The proof gives an exact random-cluster representation. Set a=q−2≥1 and r=q−1. For an open-edge set η⊂E, let k_1(η) be its number of connected components meeting W and k_0(η) the number not meeting W, with isolated vertices counted. Choose η with probability proportional to

    a^(|E|−|η|) r^k_1(η) q^k_0(η).                           (1)

Then, independently for each closed edge of J, retain it with probability 1/a. The retained edge set has exactly the conditional law S∩J given C_W. At q=3 the retention probability is one.

## 2. Exact coefficient proof of the representation

Integrating out subdivision vertices gives the color law on B with edge factor

    a + δ_e(g),   δ_e(g)=1_(g(u)=g(v)).

Under C_W all endpoints of every edge in J have nonzero colors. At an observed edge e∈J, exactly one allowed midpoint color is 0. Hence the actual generating factor for its zero indicator is

    (a−1)+δ_e(g)+x_e.

Edges outside J retain the factor a+δ_e(g). Summing the product of these factors over B-colorings with g(W) avoiding 0 gives the unnormalized generating polynomial for S∩J.

Expand each factor by choosing either δ_e or its remaining part. The selected δ edges form η and force a constant color on each open component. Such a component has r choices if it meets W and q otherwise. A closed edge outside J contributes a; a closed edge of J contributes (a−1)+x_e. At every x_e=1 these are all a, yielding (1). Conditional on η, the normalized generating factors for closed J edges are

    (a−1)/a + x_e/a,

independently. Open edges of J have zero indicator 0. This proves the claimed law exactly, without assuming a relation between an artificial bond and an individual midpoint color.

## 3. Positive association of the boundary-weighted bond model

The edge measure (1) satisfies the finite FKG lattice condition whenever q≥r≥1. To see this, condition on every edge except e. The odds that e is open are:

    1/a        if its endpoints are already connected;
    1/(ar)     if they are disconnected and both components meet W;
    1/(aq)     otherwise.                                    (2)

The ratios follow by merging the affected component weights. Adding other open edges can merge the endpoint components or turn an unmarked component into a marked one. If the endpoints remain disconnected, the only possible odds change is from 1/(aq) to 1/(ar). If they become connected, the odds become 1/a. Thus the conditional odds are nondecreasing in all other edge variables. Since all bond configurations have positive weight, these one-coordinate likelihood-ratio inequalities imply log-supermodularity by telescoping, and the finite FKG inequality applies.

Complementing all coordinates preserves association: two increasing functions of closed-edge indicators are two decreasing functions of the open indicators, whose negatives are increasing. Taking a product with independent Bernoulli retention variables preserves association by the conditional covariance identity. Finally each retained indicator is the coordinatewise increasing product of its closed-edge indicator and its retention indicator. Therefore the retained family is associated. Together with Section 2 this proves the conditional theorem.

Only classical finite FKG and product closure are used. The ordinary random-cluster and fuzzy-Potts setting is described in the credited Kahn–Weininger paper, https://arxiv.org/pdf/0711.3136 ; the marked-component weights and all required odds were checked explicitly here rather than imported without their hypotheses.

## 4. A nonlinear unconditioned event subclass

Let U,V be upward events determined by zero indicators on J, and assume that whenever either event occurs, the zero edges in J cover every vertex of W. Then U and V are positively correlated under the original unconditioned coloring law.

Indeed either event forces C_W: a zero subdivision vertex forbids color 0 at both endpoints. With p=P(C_W)>0, the conditional theorem gives

    P(U∩V)=p P(U∩V | C_W)
           ≥p P(U | C_W)P(V | C_W)
           =P(U)P(V)/p ≥P(U)P(V).                            (3)

This includes arbitrary unions and other upward combinations of edge-cover conditions. In particular, if two fixed edge sets T_1,T_2 have the same set W of incident original vertices, the two events that all subdivision vertices indexed by T_1, respectively T_2, are zero are positively correlated. It also includes nonlinear increasing events whose minimal zero-edge witnesses all cover the same W.

This is not the full family of increasing events: a union of conditions on edges with different endpoint supports need not force any fixed C_W covering its whole support. Applying (3) without the implication U,V⊂C_W would be invalid.

## 5. Why a monotone conditioning argument still does not close the gap

Even inside this subdivision class, enlarging W can decrease a common observed zero probability. Let H be a triangle, q=3, and e join original vertices 0 and 1. Exact summation gives

    P(f(a_e)=0 | f(0),f(1)≠0) = 11/17,
    P(f(a_e)=0 | f(0),f(1),f(2)≠0) = 9/14.

The first exceeds the second by 1/238. Both are within the conditional theorem's domain, which asserts association at a fixed W, not stochastic increase as W grows. The subdivided triangle is a six-cycle and is already positively associated by turn 1's other reduction; this decrease is a method obstruction, not a source counterexample.

Thus an arbitrary mixture over latent color restrictions cannot be declared associated merely because the individual restrictions admit (1). Removing the restriction remains a real missing step.

## 6. Exact optimal-second-event search by minimum closure

The earlier searches sampled both increasing events except on very small A. This turn optimizes over **every** increasing second event G once the first event F is specified.

For exact weights w(s), total Z and first-event mass M_F, assign each Boolean state s the integer cost

    c_s = w(s)[Z 1_F(s) − M_F].

For any upward set G, its covariance numerator with F is precisely sum_(s∈G)c_s. Finding the minimum such sum is a minimum-closure problem on the Boolean lattice. Add an infinite-capacity directed arc s→s∪{i} for every cover relation; connect negative-cost states from the source with capacity −c_s and positive-cost states to the sink with capacity c_s. A minimum cut chooses an upward set on the source side. Its capacity equals the total negative cost magnitude plus the chosen cost sum. An “infinite” capacity exceeding that total magnitude suffices, because selecting no states is feasible. Thus an integral max-flow/min-cut computation gives the exact minimum covariance numerator and an explicit witness if it is negative.

The portable implementation uses signed 128-bit capacities, checks upward closure of the returned set, and verifies that its directly recomputed covariance equals cut capacity minus the negative-cost baseline. On 20 arbitrary small integer measures on four coordinates, it is additionally cross-checked against direct enumeration of every increasing G for every one of the 168 increasing F: 3,360 brute-force comparisons.

The search then covers:

- All 7,581 increasing F for the unconditioned dreidel, independently reproducing turn 1's complete association check
- The known pinned dreidel negative control, for which the optimal numerator for one coordinate is −16, i.e. covariance −1/784 after division by 112²
- One-edge subdivisions of every labeled simple graph on four original vertices with at least three edges, at q=3,4,5
- Eight specified dense graphs on five original vertices, at q=3
- 200 fixed-seed repeated-neighborhood graphs for each of (|A|,q)=(6,3),(7,3),(8,3),(6,4),(7,4)

For the latter graph cases, first events include every two- or three-coordinate conjunction plus sampled unions of principal upsets. The entire second-event space is optimized for each. No target counterexample was found in 1,134 graph/q cases. There are 109,077 total exact closure runs including all controls. The first-event and graph lists remain finite, so this is not an all-graph association theorem.

The largest crude coloring-count bound among these search cases is 4^23=2^46; products are below 2^92 and comfortably inside signed 128-bit capacity. Other cases are smaller. No floating-point comparison is used. Fixed random seed: 33003338; the separate brute-force-control seed is recorded in the source.

## 7. Artifacts and current limit

The conditional representation checker compares direct color-count coefficients with the boundary-random-cluster thinning coefficients for H=K4, q=3,4,5 and all 16 W. It also checks the finite bond lattice inequalities, the resulting small marginals, and the triangle conditioning decrease. All 209,849 exact assertions pass. These are author controls, not independent review.

Run:

    python turn3_representation_controls.py
    g++ -O2 -std=c++17 turn3_closure_search.cpp -o /tmp/coloring_turn3
    /tmp/coloring_turn3

Saved outputs: TURN_3_REPRESENTATION_CHECKS.json and TURN_3_SEARCH.json. The algorithmic success test remains an exact negative covariance for the unconditioned target, not for a pinned or stronger auxiliary law.

The new conditional representation and edge-cover-event theorem are scoped partials. The source asks for arbitrary finite bipartite graphs and arbitrary pairs of increasing functions. Neither full resolution nor a counterexample has been obtained after 3/5 turns. Turns 4–5 must address removal of the conditioning or a genuinely different full-target mechanism, rather than promote these special classes.
