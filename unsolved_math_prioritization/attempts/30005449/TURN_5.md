# Turn 5: a cyclic graph class via monotone effective conductances

2026-10-01 06:29 UTC. Fifth and final substantive author turn. Status: a complete theorem for a genuinely cyclic class, with a sharp remaining general-graph gap. No original general convergence claim or novelty claim.

## A class beyond trees

Let H be any finite connected loop-free undirected graph with a marked vertex N; H may have arbitrary cycles and parallel edges. Attach to N a fresh simple path of length d≥2, ending at the unique food vertex F, whose other vertices are not in H. There are no other connections between the path and H. Run the exact trace-reinforced ant process with all initial weights one.

**Theorem.** Every food-path edge has normalized weight tending to 1. All H-edge normalized weights converge almost surely to a unique strictly positive deterministic vector χ. It is characterized below by a finite system of effective-conductance equations.

This is not every finite graph: graphs with several competing routes to food generally do not have this one-attachment geometry. In particular, the proof does not convert an arbitrary original N–F graph into this class without changing the process.

## 1. The exact cooperative drift

Fix e={u,v} in H. Remove e and introduce a success terminal Δ, joining u to Δ and v to Δ by edges of conductance w_e each. Keep every other H-edge with its original conductance. Let C_e(w) be the effective conductance from N to Δ in this network.

Equivalently,

 C_e(w)=min_{f(N)=1,f(Δ)=0}
   [sum_{b≠e} w_b(f(b_+)-f(b_-))²+w_e(f(u)²+f(v)²)]. (1)

The minimum can be restricted to potentials in [0,1]. Hence C_e is continuous, coordinatewise nondecreasing, concave and positively homogeneous of degree one. It is Lipschitz on the closed nonnegative orthant: changes in each ordinary coefficient multiply an energy at most one, and the distinguished coefficient multiplies an energy at most two. For strictly positive w, C_e(w)>0.

Every original ant traverses all d edges of the food path before stopping, so those edges have exact weight n+1. In normalized units their effective conductance from N to food is 1/d. Before its first crossing of e, the killed-edge construction of turn 1 is precisely the modified network above, with Δ a success terminal and F a failure terminal. Eliminating the two networks at their only common vertex N yields

    p_e(w)=d C_e(w)/(1+d C_e(w)).                   (2)

One can verify (2) by the harmonic flux equation C_e(p_N-1)+(1/d)p_N=0. Excursions that do not reach either terminal are already incorporated in the effective conductances.

Thus p is coordinatewise nondecreasing, globally Lipschitz, and strictly subhomogeneous on positive vectors:

    p(tw)>t p(w) for 0<t<1,
    p(tw)<t p(w) for t>1,                          (3)

componentwise. Strictness follows from C_e(w)>0 and the explicit scalar fraction in (2).

## 2. Existence and uniqueness of a positive equilibrium

Choose a spanning tree T of H rooted at N, and put b=(d-1)/d. On each tree edge at depth k assign v_e=b^k. In the network consisting only of T and the food path, turn 4 gives p_e(v)=v_e exactly.

Assign a common small positive value δ to every non-tree edge. For a tree edge, adding the non-tree edges cannot decrease C_e, so p_e(v)≥v_e remains true. For a non-tree edge e, choose a tree path from N to one endpoint. Let R_e<∞ be its resistance with the fixed positive tree weights. Deleting all other branches of the modified network in (1) gives the lower bound

    C_e(v)≥δ/(1+R_eδ),
    p_e(v)/δ≥d/[1+(R_e+d)δ].                       (4)

Choose δ≤1 small enough that the last quantity exceeds one for every non-tree edge. If H is itself a tree there are no such constraints. We have produced v>0 with p(v)≥v and v≤1. Iterating p gives an increasing sequence bounded above by 1, whose limit χ>0 satisfies p(χ)=χ by continuity.

For uniqueness, let x,y>0 be fixed points. If t=max_e x_e/y_e>1, then x≤ty. By monotonicity and strict subhomogeneity,

    x=p(x)≤p(ty)<t p(y)=ty,

contradicting equality in a coordinate attaining that maximum. If t≤1 and x≠y, reverse x and y to obtain the same contradiction. Thus χ is the unique positive fixed point. Each χ_e<1 because the conductances are finite in (2).

Uniqueness alone is not yet stochastic convergence; the next two sections establish attraction and boundary avoidance separately.

## 3. Global attraction in the positive orthant

The ODE is w'=p(w)-w. Its off-diagonal monotonicity gives the usual componentwise comparison principle (proved by the first-contact argument, or by adding a vanishing strict comparison term). For any c>0, homogeneity in (2) and p(χ)=χ give

 [p_e(cχ)-cχ_e]/χ_e
     =c(1-c)χ_e/[1+(c-1)χ_e].                      (5)

Let m=min_eχ_e>0 and M=max_eχ_e. If 0<c≤1, the right side of (5) is at least m c(1-c). Hence the scalar logistic subsolution c_-'=m c_-(1-c_-), starting below all initial ratios w_e(0)/χ_e and at most one, gives

    w(t)≥c_-(t)χ,  c_-(t)→1.

For an upper bound choose c_+(0)≥1 above all initial ratios. On 1≤c≤c_+(0), χ_e/[1+(c-1)χ_e] is at least

    k=m/[1+(c_+(0)-1)M]>0.

The scalar equation c_+'=-k c_+(c_+-1) supplies a supersolution of (5), so w(t)≤c_+(t)χ and c_+(t)→1. Therefore every strictly positive ODE trajectory converges to χ, uniformly when initial states range over a compact subset of the positive orthant. This also proves stability of χ there. No nonexistent gradient from turn 3 is used.

## 4. Almost-sure persistence away from the boundary

We must still prevent the stochastic process from converging toward a boundary face, where the preceding positive-orthant comparison does not by itself suffice.

Use the same spanning tree T. For a tree edge e incident to N, deleting the rest of the success network leaves the direct success edge of conductance X_e, so (2) gives

    p_e(X)≥d X_e/(1+d X_e).

By monotone Bernoulli coupling, W_e dominates a scalar process with success probability dY_n/[dY_n+n+1]. The scalar lemma of turn 4 therefore yields a strictly positive lower limit for X_e.

Proceed by depth in T. Suppose the finitely many ancestor edges along the tree path to one endpoint of e have positive almost-sure lower normalized limits. Eventually their reciprocal normalized weights sum to at most a finite constant R. Keeping that path and the success edge e, and deleting everything else, gives

    C_e(X)≥X_e/(1+R X_e),
    p_e(X)≥d X_e/[1+(R+d)X_e].                    (6)

Conditioning after that finite time, couple below with the scalar process from turn 4 with coefficient a=R+d. Its positive limit is (d-1)/(R+d), hence liminf X_e>0. The coupling is valid because the scalar lower probability is increasing in its weight and the actual conditional probability is bounded below by it. Random eventual bounds can be treated on a countable increasing union of deterministic bounds and starting times.

This proves persistence for every tree edge. For any non-tree edge, choose a path in T from N to one endpoint, which does not use that edge, and apply (6) again. There are finitely many edges, so almost surely the entire limit set of X(n) lies in a compact subset of the strictly positive orthant.

Finally the exact stochastic-approximation representation has bounded martingale noise and square-summable steps, and its drift here is Lipschitz. Its limit set is internally chain transitive for the ODE, as in the primary paper's Theorem 2.5. Uniform attraction to χ on positive compact sets from Section 3, together with the persistence just proved, implies that this limit set is {χ}. Equivalently apply the standard global-attractor criterion stated in the primary paper's Corollary 2.6. Thus X(n)→χ almost surely, completing the theorem.

## 5. Why the general conjecture is still open in this attempt

The essential mechanism is that all exits to food pass through a **fixed-conductance series path** from the same starting vertex. It turns every trace probability into the increasing effective-conductance fraction (2). In a general N–F graph, deleting or increasing a competing edge can either improve access to the queried edge or divert the walk directly toward food. The full drift is not globally cooperative; the triangle calculation in turn 3 demonstrates this. Thus neither the monotone fixed-point comparison nor the spanning-tree persistence argument transfers unchanged.

After five substantive author turns, this attempt has not proved deterministic almost-sure limits on every admissible finite graph and has not produced an admissible counterexample. The tree theorem and this cyclic-class theorem must remain explicitly partial.

The several-food question also remains unresolved as an intended general model. Two precise possibilities are absorption on first hitting any food vertex, or choosing a target food independently before each walk. They define different stochastic processes. Wiring several absorbing foods into one vertex can create exactly the parallel-food-edge structure excluded by the original deterministic-limit conjecture; therefore it cannot automatically inherit that conjecture. The source specifies no optimization criterion that would certify either construction as the intended “meaningful” extension. No general multi-food convergence or optimality claim is made.
