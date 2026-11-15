# Final adversarial derivations — complete original claim

The eight-family initial reconstruction is the main independent proof artifact. It was sealed before any foreign body, supplied programme/result or archived opinion. This document closes its explicit imported-interface frontier after direct source reading. It changes no target assumption or conclusion and supplies no new repair to conceal a substantive defect.

## 1. Pointwise threshold and exact optimization

For each nonempty finite connected unit-edge input graph let D=n−1. For R≥0, every budget b_u=max{k∈[0,D]∩Z:kw(u)≤R} exists. For every vertex x and site u, integer d(x,u)∈[0,D] gives

    w(u)d(x,u)≤R ⇔ d(x,u)≤b_u ⇔ d(x,u)+(D−b_u)≤D.

This includes w(u)=0: b_u=D. Conjoining all sites preserves the entire feasible vertex set. Negative thresholds are separately empty. This proof holds on every connected unit-edge graph; medianity supplies the fast additive oracle. Zero-weight vertices remain in all shortest paths and the center domain.

For n≥2, every optimum is one of the conceptual products kw(u), 0≤k≤D. Set feasible B=D max w and any witness vertex. With row endpoints and lower middles only, choose a weighted median of middles, weighted by current inclusive row length. Save a feasible pivot before deleting its weak upper side; delete the weak lower side for an infeasible pivot. Maintain B feasible and either B=ρ or an active optimum copy. A feasible pivot equal to ρ is saved, a larger one preserves all optimum copies, and an infeasible pivot is strictly below ρ. Thus empty rows force B=ρ. The saved witness has radius at most ρ, hence is a center. The final full feasible set at B is exactly all centers.

Each row middle has at least half its length on either weak side. The median charges at least half the total active length to the relevant weak side of row middles. Therefore at least M/4 entries disappear each iteration, even with ties, zero rows and singleton active intervals. M starts at n² and stays integral, so O(log(2n)) queries suffice. Sorting n representatives and bounded binary searches cost O(n log(2n)) per iteration; no candidate table is created. The row storage claim is O(n) beyond the oracle, not a claim that all internals of every credited oracle have linear space.

The n=1 and all-zero cases return radius zero and all vertices. For n=1 no k=1 comparison is needed. Every subsequent pivot, budget test, sort and incumbent comparison compares two pairs (k,u). Rational cross-products are k p_u q_v versus j p_v q_u, with O(B+log n) bits for B-bit components. Arbitrary finite real weights are handled in the expressly declared exact comparison model, rather than by an unspecified Turing encoding.

## 2. Structural frontier of the additive call

The following mathematical reconstruction distinguishes the objective and model from the mere theorem name. In a finite median graph, complementary Θ-halfspaces and their nonempty convex intersections are gated median subgraphs. A gate g_H(y) obeys d(x,y)=d(x,g_H(y))+d(g_H(y),y) for every x∈H. For a source subset U define the external profile at v∈H by the maximum of d(v,u)+a(u) over u∈U with gate v. Grouping this finite maximum by gate gives the max-plus identity from the early reconstruction exactly.

For a balanced cut H,K, this yields for x∈H:

    E_G(x)=max(E_H(x), d(x,g_K(x))+E_K(g_K(x))).

It is symmetric for K. Nonnegative integer profiles remain such under the needed finite max-plus updates.

At an unbalanced recursion node, use the common majority median v0. If v0 itself is an additive farthest vertex from v0, triangle inequality gives E(x)=d(x,v0)+a(v0) for every x. Otherwise choose a weighted farthest u*. The incident separating classes of v0 and u* form the wide ladder. Pairwise orthogonality puts them in a cube; hence their number ℓ is at most log₂s. For a vertex whose ladder avoids that wide ladder, the gate/interval structure puts v0 on a shortest path to u*, so triangle inequality and this equality determine its eccentricity as d(x,v0)+E(v0).

Enumerate the wide classes and let G_i be the successive intersections of their majority halfspaces, and S_i the removed minority slice. Every G_i contains v0. Each S_i is nonempty: the neighbor of v0 across its own incident class crosses none of the other classes, so it survives earlier majority intersections. These facts close the otherwise omitted nonempty condition in an abstract statement about intersections of gated sets; empty gated subgraphs are never used by this recursion.

For x∈S_i, split the source sites into S_i and G_(i+1). The external sites enter S_i through their gates. The source's modified profile on boundary vertices is the maximum from the open external fiber, excluding the gate itself; nonboundary vertices retain their original label. Therefore it need not dominate the original profile at a boundary vertex. Both recursive vectors are necessary, and their maximum gives E_(G_i)(x). Contributions from artificial retained original labels at nonboundary vertices are already bounded by the separate original-profile vector. For x in a later slice, combine its already known E_(G_(i+1))(x) with

    d(x,g_(S_i)(x))+E_(S_i,original)(g_(S_i)(x)).

This is again the same gate identity. Thus descending slice reconstruction keeps the full objective and all output vertices. The path example in the early proof shows why the original-profile call must not be dropped. Inspection of the actual source algorithm confirms both calls are retained. The parameter change affects only which valid structural branch is chosen, and does not replace these identities.

## 3. Complexity and all finite reductions

Use the manuscript's integer choice L(s)=ceil(log₂s), f(s)=2L(s), with direct s≤2 base cases. A balanced child has at most s(1−1/f(s)) vertices. In an unbalanced node every slice has fewer than s/f(s) vertices and ℓ≤L(s). Consequently its two calls per slice have total volume at most s. Balanced children partition s, so induction gives summed graph order at every depth at most root N.

For s≥3, f(s)≤4log₂s=λln s, λ=4/ln2. A nonterminal path satisfies s_(i+1)≤s_i(1−1/(λln N)). Thus s_h≤N exp(−h/(λln N)); at h=ceil(λln²N) it is at most one and already terminal. This root-bound comparison has the correct inequality direction. O(s log²(2s)) nonrecursive work, per-level volume N and O(log²N) levels give O(N log⁴(2N)). Linear-time Θ/halfspace/median preprocessing is a credited interface, not an assumed supplied embedding. Its actual primary preprocessing constructions were inspected. Reading adjacency lists is absorbed by m=O(n log n), and n=1 is a separate constant-size case.

Each arrival update adds a distance at most root N−1 to a previous maximum. Starting from labels at most N−1, the full path gives O(N log²(2N)) labels, hence O(log(2N)) bits. This is a global-root word bound; local small subgraphs are not required to fit labels into their own smaller log s. Original-profile real comparisons never move into the additive recursion.

Together, O(log(2n)) complete additive queries give the original deterministic O(n log⁵(2n)) exact-operation theorem, radius pair, one witness and all centers, without dimension or embedding input. No finite test is used to infer this asymptotic exponent.

## 4. Literal earlier estimate versus complete theorem

The early exact Q30 construction has order 10¹², all cuts unbalanced for the literal natural-log threshold, and duplicated slice volume 1,022,147,483,646>10¹². Its actual wide-ladder/slice interpretation was checked against the cited definitions. This refutes that intermediate estimate in the specified public preprint, not the output identities or the theorem after the manuscript's stated repair. With f(10¹²)=80 its coordinate cuts are balanced instead, so that bad volume branch does not apply. The independent Taylor and integer arithmetic are retained, without constructing a trillion-vertex graph.

The other displayed product estimate is replaced by the root-size contraction argument above. A rounding or small-base issue in an earlier source is not transferred into the target's explicit integer f and s≤2 bases. No claim is made about the uninspected final SODA chapter's typography or whether it contains those earlier displayed estimates.

## 5. Boundary falsifiers and remaining limits

The eight recorded wrong-variant controls detect strict instead of inclusive budgets, arbitrary nonintegral lengths, deletion of zero-weight centers, continuous-center reinterpretation, negative profiles, unweighted row-median progress, assumed external-fiber dominance and deletion of the original-profile slice call. They are falsifiers of those altered models/algorithms, not counterexamples to the literal target.

Classical median structure and preprocessing remain mathematical dependencies, as in the manuscript. No human peer review, proof assistant, fast general oracle implementation or asymptotic benchmark is claimed. No substantive gap in the full stated finite theorem was found. Historical firstness and present worldwide open status are not established by this adversarial lane. These are evidentiary boundaries, not narrowed replacements for the theorem.
