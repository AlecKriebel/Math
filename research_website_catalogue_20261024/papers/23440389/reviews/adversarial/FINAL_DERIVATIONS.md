# Final derivations and falsification boundaries

This supplements the unchanged early full proof. No target claim has been narrowed or repaired.

For rooted tree T, let p(v) be a parent. Define F_v(y,x) as the number of completions in the descendant subtree with parent label y and v-label x, conditional on boundary admissibility. It is zero unless x belongs to L(v), and for a nonroot y belongs to L(p(v)) and |x−y|≥2. At the root y must be the sentinel None. For children u of v,

    F_v(y,x) = sum over child values (z_u) of product over u of F_u(x,z_u),

where z_u∈L(u), |z_u−x|≥2, z_u≠y when a parent exists, and all child values are pairwise distinct. An admissible leaf has value1. The total is Σ_x F_root(None,x).

Every constrained pair falls into exactly the relevant part of this decomposition: an edge v-u is imposed locally; a grandparent-child pair is imposed by z_u≠y; siblings are covered by injectivity; all remaining constrained pairs are within one child subtree. For two different child subtrees, any pair other than their roots has distance at least3. This proves independence of the product and exhaustiveness of the sum. Each complete labeling selects exactly one tuple at each vertex, so no multiplicity or overcount is introduced. Conditional states need not know the grandparent value: the caller already enforces its inequality before allowing the state. Local admissibility is essential; a leaf is not unconditionally1. The explicit invalid-state checks are recorded in own output.

The CSP mechanism shares the literal graph and intended mathematical model, but not this recurrence. It computes all-pair graph distances and propagates binary numeric-gap constraints after each variable assignment. By induction each remaining domain contains exactly the values not yet excluded by assigned neighbours in the constraint graph; a full leaf is a complete labeling, and enumeration partitions by each selected value. Both mechanisms count labeled assignments, not isomorphism orbits. All-root agreement checks that no privileged root hides a missing grandparent or sibling constraint.

The universal list proof uses a breadth-first order, or another order with the same earlier-contact property; it does not assert that every arbitrary vertex ordering works. For parent p=root there are ≤deg(p)−1 earlier siblings and no grandparent. For p≠root there are ≤deg(p)−2 earlier siblings and one grandparent. Thus the distance-two count ≤Δ−1 is uniform, even at the first child, a path endpoint, a root of degree1, and Δ=0 for a singleton (where there are no nonroot steps). Integer labels matter because the parent excludes at most three integers. Allowing six distinct real numbers in a short interval would falsify the bound on an edge; arbitrary relabeling of numerical colors is not legitimate. Translations and a common reflection preserve gaps, while dilation can create new legal choices.

For extensions let leaves be indexed i=1,…,6 and lengths ℓ_i be independent nonnegative integers. Leaves of the extended tree lie at path tips (the old leaf itself when ℓ_i=0), so

    diameter(T_ell) = max_(i<j) [ℓ_i + dist_T(leaf_i,leaf_j) + ℓ_j].

No extra endpoint lies inside a path. Every old distance remains unchanged. The displayed original witness extends because a newly labeled vertex has just one earlier parent and one earlier grandparent at constrained distance; all other paths' new vertices are distance at least4. For a list lower bound, give arbitrary five-lists to new vertices while preserving the original bad lists: restriction would contradict the original obstruction. The upper bound is universal for Δ3. This covers zero lengths and every asymmetric finite tuple. For ℓ=(m,0,0,0,0,0) the diameter is m+6. Finite controls do not replace either proof.

The exhaustive small list tests cover all nonempty subsets of [4] on the three path sizes1,2,3 and all two-element subsets of [5] on the four-vertex star. They are bounded model checks, not an enumeration of all trees or all integer lists. The 732 extension tuples similarly provide diagnostic agreement, not a finite reduction of the infinite family. No claimed runtime theorem or global minimality is inferred from the programmes' node counts.

Actual Fig.4 in the 2001 primary can be distinguished without importing a native history audit: top row t1-t2-t3-t4, bottom row b1-b2-b3-b4, vertical edges t1-b1 and t4-b4, one left tip joined to t1,b1 and one right tip joined to t4,b4. This is ten vertices and twelve edges, with two visible triangles and the rectangle cycle. It cannot itself be a tree. Deleting edges to obtain a spanning tree can remove adjacency or distance-two constraints, so a cyclic counterexample does not by itself settle the tree claim. The construction here is checked directly, with no inference of firstness from a failed search.
