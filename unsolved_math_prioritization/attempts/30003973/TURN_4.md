# Turn 4: exact star-forest host profiles and two rigid target families

Problem30003973 remains unresolved. This fourth turn uses the structure of actual graph copies, rather than arbitrary downward families. It gives an exact all-size characterization when both target and host are star forests, and proves all-host rigidity for star and matching cores. These are scoped elementary results, with no novelty claim; connected stars were already known to be Ramsey-isolated in the literature surveyed by Savery.

## 1. Star forests and color capacities

A nonempty isolate-free star forest is a disjoint union of stars K_(1,k_i), with positive component sizes k_1≥...≥k_s≥1. Here K_(1,1)=K_2, and a component size counts edges, not vertices. Let H be this target and let G have star-component sizes d_1≥...≥d_m≥1. Isolated host vertices are irrelevant for this target.

In one color, a host star of color-degree a can contain any one target star of size at most a, but cannot contain two vertex-disjoint nontrivial target components: every edge of a host star meets its center. This also holds for the edge target K_2. Consequently a monochromatic H exists exactly when the sorted monochromatic component capacities dominate k_1,...,k_s.

Define

    τ_H(t)=#{i:k_i≥t},     N_G(u)=#{j:d_j≥u}.

A color fails to contain H if and only if there is a threshold t among the distinct positive k_i for which fewer than τ_H(t) host components have color-degree at least t. This is the usual sorted-list embedding test, applied componentwise.

## 2. Exact threshold criterion

**Theorem.** For every q≥1,

    G→_q H

if and only if, for every q-tuple t_1,...,t_q chosen from the distinct component sizes of H,

    N_G(1+Σ_c(t_c−1)) ≥ 1+Σ_c(τ_H(t_c)−1).         (1)

**Necessity and sufficiency via avoiding colorings.** Suppose a coloring avoids H in every color. For each color c choose a witnessing deficient threshold t_c. That color has at most τ_H(t_c)−1 components whose color-degree reaches t_c. Put D=Σ_c(t_c−1). Every host star with more than D edges must cross at least one color's threshold. Counting these components, allowing overcounting if several colors cross, gives

    N_G(D+1) ≤ Σ_c(τ_H(t_c)−1).                      (2)

Conversely, suppose(2) holds for some threshold tuple. Assign every host star of size>D to a color, with at most τ_H(t_c)−1 assignments to color c; the total quota in(2) makes this possible. For an assigned star, distribute up to t_i−1 edges to each unassigned color i, and place all remaining edges in its assigned color c. Since its size exceeds D, color c reaches at least t_c, and no other color crosses its threshold. A star of size≤D can have all its edges distributed within the capacities t_c−1, crossing no threshold. Each prescribed nonnegative color-degree vector can plainly be realized on a star's edges. Thus every color stays deficient at its selected threshold, so H is avoided. This establishes the exact complement of(1). ∎

In the converse, the notation “size>D” refers to edge count. There is no claim that a large star's assigned color has a bounded degree; only the number of components crossing a threshold is bounded.

## 3. A canonical minimal star-forest host

There is a useful closed form for(1). Put a_i=k_(i+1)−1 for0≤i≤s−1, so a is a nonincreasing finite sequence of nonnegative integers. For0≤j≤q(s−1), define its q-fold max-plus convolution

    c_j=max{a_(i_1)+...+a_(i_q): 0≤i_l≤s−1, Σ_l i_l=j}.

Every index j in that range is attainable. The sequence c_j is nonincreasing: for any index tuple of positive sum, decreasing one positive index cannot decrease the corresponding a-value. Define F_q(H) as the star forest with q(s−1)+1 component sizes

    c_0+1, c_1+1, ..., c_(q(s−1))+1.                (3)

Then for every star-forest host G,

    G→_q H  iff  G contains F_q(H) as a subgraph.    (4)

Here is a precise justification of the passage from thresholds to convolution. Let D_H be the finite lattice downset

    D_H={(x,y): 0≤y≤s−1, 0≤x≤k_(y+1)−1}.

Its maximal corners are exactly (t−1,τ_H(t)−1) for the distinct component sizes t, with redundant corners harmless. The q-fold ordinary Minkowski sum qD_H is again a lattice downset. Its horizontal row at height j consists of the integers x with0≤x≤c_j: after choosing the index tuple, any integer up to the sum of its horizontal capacities can be allocated among the summands. Criterion(1), extended downward using monotonicity of N_G, says precisely that

    N_G(x+1)≥y+1  for every(x,y)∈qD_H.

It suffices to use the row endpoints(c_j,j). These inequalities are equivalent to the j+1-th largest host component having at least c_j+1 edges, for every j. That is exactly the ordinary componentwise containment of the star forest(3). ∎

For instance, if H=P_3⊔K_2 then a=(1,0), F_2(H) has component sizes(3,2,1), and F_3(H) has sizes(4,3,2,1).

This gives a complete finite encoding of Ramsey behavior on **all star-forest hosts**, not just a finite scan. It does not identify behavior on hosts with cycles or other components.

## 4. Consequences for unrestricted equivalence

Any target universally q-equivalent to a star forest must have a star-forest core. Indeed, F_q(H) is Ramsey for H, hence for that target. Its all-one-color coloring contains the target as an ordinary subgraph of a star forest. After removing isolated vertices, every component of that subgraph is a star. Turn1 then gives equivalence of the cores.

For two isolate-free star-forest targets, universal q-equivalence therefore implies identical canonical F_q profiles. In particular it forces the same number s of components and the same largest component size k_1: the canonical profile has q(s−1)+1 entries and largest entry q(k_1−1)+1. These are necessary conditions, not a sufficiency claim for unrestricted hosts.

Two special cases admit complete all-host rigidity.

**Single-star cores.** Suppose a target J is q-equivalent to K_(1,k), with q≥2. Remove its isolates using Turn1 and call its core C. The star with q(k−1)+1 edges is q-Ramsey for K_(1,k). Color its edges with one color appearing k times and each other color k−1 times. Since C must occur in some monochromatic class, it is a nontrivial star K_(1,l) with l≤k. If l<k, the star with q(l−1)+1 edges is q-Ramsey for K_(1,l) but can be colored with no class having k edges, since q(l−1)+1≤q(k−1). This contradicts core equivalence. Hence C≅K_(1,k).

**Matching cores.** The same argument, replacing a host star by a host matching, shows that a target q-equivalent to the matching kK_2 has core exactly kK_2. The witnessing matching has q(k−1)+1 edges; a balanced coloring has largest color matching k, forcing the other core to be lK_2 with l≤k, and the smaller matching witness excludes l<k.

Combining either conclusion with Turn1 gives the full classification: the q-equivalent targets are exactly the same core padded with h−|V(core)| isolated vertices, where h≤r_q(core). In particular, any2-equivalence pair having a star or matching core transfers to every q≥2. No formula for the multicolor Ramsey number r_q(core) is assumed or needed.

## 5. Validation and remaining gap

The checker compares(1), the canonical-profile test and direct component color-degree enumeration over explicitly bounded integer partitions. It reconstructs an avoiding coloring whenever a threshold inequality fails. These exact controls validate boundary cases and the all-size derivation; they do not substitute for it.

The canonical profile can lose information. For example, the two targets with component lists(5,4,2,2,1) and(5,4,3,2,1) have the same two-color canonical host: component sizes(9,8,7,6,5,4,3,2,1). This certifies identical behavior on every star-forest host. It does **not** establish universal2-equivalence. The final author turn will test this concrete collision against non-star hosts and make the remaining host-class limitation explicit.

Original2-to3 implication unresolved. Completion estimate:20%, as graph-specific reductions and exact restricted-host structure. One substantive author turn remains after this checkpoint.
