# Expanded mathematical audit of the torus partial result

The notation below follows the authored report: the torus has dimension d, and f_i counts i-cells. These are independent explanations of the proof obligations, not claims of new theorems.

## 1. Category and h-double-prime hypotheses

A simplicial-poset realization has an embedded closed simplex for each cell. Its vertices are different points, although distinct cells may have the same vertex set. The order complex is a subdivision with the same underlying space. Since the space is T^d, local homology is that of Euclidean d-space. Taking a point in the relative interior of each face identifies the appropriate shifted local homology with the reduced homology of the corresponding link. Thus this is a connected, closed simplicial-cell homology manifold. The torus has top Betti number one over F_2, so it is orientable in the sense required by the h-double-prime theorem. Passing to an infinite extension of F_2, if needed for a linear-system-of-parameters argument, changes none of these Betti numbers.

The source used is Murai, Theorem 2.1, together with his definitions preceding it. No lower-bound theorem for abstract simplicial complexes is imported into the more general simplicial-poset category. In particular, the stronger g_2 bounds discussed in the introduction of Basak–Datta are not available without their additional hypotheses.

## 2. Independent derivation of the central-binomial formula

Set n=d+1. The identity sum h_k=sum f_{k-1}(1-1)^(n-k)=f_d follows by evaluation at t=1. Evaluation at t=0 gives h_n=(-1)^(d+1), because the reduced Euler characteristic of the nonzero-dimensional torus is -1.

Write B_k=sum_{j=0}^{k-1}(-1)^(k-1-j) beta_j. For a connected torus beta_0=0, whereas beta_j=C(d,j) for j>0. The elementary alternating partial-binomial identity gives

B_k=C(d-1,k-1)-(-1)^(k-1), 1<=k<=d.

Substituting h_k=h''_k+C(d+1,k)B_k for the interior indices gives

f_d=1+(-1)^(d+1)+sum_{k=1}^d h''_k
    +sum_{k=1}^d C(d+1,k)C(d-1,k-1)
    -sum_{k=1}^d (-1)^(k-1)C(d+1,k).

The last sum equals 1+(-1)^(d+1), so the endpoints cancel. The remaining convolution equals C(2d,d), because C(d-1,k-1)=C(d-1,d-k), with the omitted endpoint terms zero. This proves the exact formula in the report for every positive d, not merely for the range tested by code.

Nonnegativity gives the central-binomial lower bound. If d>=2, h''_1=f_0-d-1 and h''_d=h''_1 occupy different coordinates. Discarding the other nonnegative coordinates proves the stated vertex refinement. This doubled refinement is deliberately not applied to d=1, where the two indices would coincide.

The ratio test is also correct: R_3=6/5 and R_(d+1)/R_d=(d+2)(d+1)/(2(2d+1)); subtracting the denominator from the numerator gives d(d-1)>0 for d>=2. Hence the central-binomial estimate alone does not reach the factorial target above dimension two.

## 3. Why the four-color reduction is legitimate

Let P be a regular simplicial-cell decomposition of T^3 with a proper coloring of its vertices by four colors. Each tetrahedron has all four colors. Every triangle is incident with precisely two distinct tetrahedra; regularity rules out self-incidence of a cell along one of its own boundary faces. Construct the dual multigraph G by assigning a graph vertex to each tetrahedron and an edge to each triangle. Color a dual edge by the color absent from the triangle.

Each color class is a perfect matching. The graph is connected, because a connected closed manifold is strongly connected through its codimension-one faces. For a fixed color c, the components of the graph formed by deleting the c-edges correspond exactly to the original vertices of color c: a crossing through any other color preserves that vertex, and the link of that vertex is strongly connected. Murai's Proposition 4.1 and Corollary 4.2 also give the complete poset identification, not merely a correspondence of facet counts.

Suppose the c-deleted graph is disconnected. A path in G between two of its components contains a c-edge xy crossing between components. There cannot be another edge of color different from c joining x and y, since that would connect them in the c-deleted graph. Nor can there be a second c-edge at a vertex, since color c is a matching. Thus the complete set of edges between x and y has precisely the single color c, and x and y lie in different components after its deletion. This is exactly a 1-dipole under Murai's definition.

The PL hypothesis in the cited dipole theorem is satisfied here. The barycentric subdivision is a triangulation of a three-manifold. Its edge links are circles, and its vertex links are closed triangulated surfaces with the homology of S^2. A connected closed surface with that homology over F_2 is S^2. Consequently the triangulation is a PL three-manifold. Equivalently one may perform this argument in the links of the original simplicial cells before subdivision.

The dipole theorem preserves the underlying PL-manifold and leaves an admissible colored graph. The associated poset is still a regular simplicial-cell decomposition. Each cancellation removes two tetrahedra. Whenever the graph is not contracted, the preceding argument supplies another cancellation. Since the number of graph vertices strictly decreases, the process terminates; at termination all four color-deleted subgraphs are connected. The resulting decomposition has exactly four vertices. Basak–Datta's contracted lower bound now applies and forces at least 24 tetrahedra at termination, and hence at least 24 initially.

This proof has no step that colors an arbitrary simplicial poset with four colors. With exactly five original vertices and a missing simple-graph edge uv, assigning the same color to u and v and different colors to the other three vertices does supply the required coloring. Therefore a five-vertex example with fewer than 24 facets must have underlying simple graph K_5. The argument does not exclude such a K_5 example.

A finite diagnostic in independent_check.py starts with the regular four-vertex, 24-facet Kuhn quotient, inserts a 1-dipole to obtain color-deleted component counts (2,1,1,1) and 26 facets, and cancels it back to the exact original graph. This checks an implementation example; it is not the reason the universal colored reduction holds.

## 4. The contracted bound and the two numerical vectors

Basak–Datta use the same regular-CW simplicial-cell category. Their Theorem 1.4 gives the group-weight lower bound only for contracted pseudotriangulations; Lemma 3.1(v) gives weight 24 for Z^3. This yields the needed four-vertex result for T^3.

For general vertex count v, the preceding h-double-prime identity reads

F=20+2(v-4)+h''_2.

Every tetrahedron requires four distinct vertices. If v=4 the contracted theorem gives F>=24. If v>=6 nonnegativity gives F>=24. Thus F<24 implies v=5 and F in {22,23}. In a closed three-manifold each triangle has two incident tetrahedra, so f_2=2F; Euler characteristic zero then gives f_1=v+F. Substitution produces precisely the two displayed f-vectors and their displayed h-double-prime vectors.

Murai's vanishing-coordinate parity restriction is respected: the 22-facet case has h''_2=0 and even F; the 23-facet case has no zero interior coordinate. It does not exclude the latter. Neither vector is a certified realization.

## 5. The parity equation is global, not an assumption on gluing types

Label the five vertices by 0,...,4. Mapping every cell to the simplex on its vertex labels gives a cellular simplicial map into the boundary of the 4-simplex. This is well-defined on shared faces even when several source cells have the same vertex set. Over F_2 the sum of all source tetrahedra is a cycle, since each source triangle occurs twice in its boundary.

Let a_i count tetrahedra whose vertex set omits i. Its image chain is sum_i (a_i mod 2) F_i, where F_i is the target tetrahedron missing i. The coefficient at the target triangle missing i and j is a_i+a_j. All ten coefficients vanish. Therefore the five a_i have common parity. Summing them shows this parity equals F mod 2, because there are five types. The 22-facet case has all a_i even; the 23-facet case has all a_i odd and thus positive.

One sentence in the author text says a triangle lies in two tetrahedron types. The precise reading needed is that a target triangle is contained in two possible target tetrahedra. The two incident source tetrahedra can have the same type. The chain argument above permits this and proves the claim without an assumption that incident source types differ. This is a clarification, not a change to the author's result.

## 6. Lattice volume and regularity in all dimensions

For the restricted class, the torus quotient has q=[L:Gamma] vertex orbits. Since every closed d-simplex embeds, its d+1 vertices are distinct in the quotient; hence q>=d+1. A fundamental domain for Gamma has volume q covol(L). Each facet has volume covol(L)/d!, and overlaps occur only on lower-dimensional faces. Volume additivity gives f_d=q d!, proving the stated bound under exactly the assumed hypotheses.

For the equality construction, the sum-of-coordinates map Z^d -> Z/(d+1) is onto and has kernel Gamma. The standard Kuhn triangulation is invariant under Z^d, has unimodular facets, and each facet has one vertex in every residue class. To see that this vertex check really implies embedding of each closed facet in this example, suppose a simplex sigma met sigma+gamma for nonzero gamma in Gamma. They are simplices of one geometric triangulation, so their nonempty intersection is a common face containing a lattice vertex w. Then w and w-gamma are two distinct vertices of sigma in the same residue class, impossible. The same argument covers each lower-dimensional face. The quotient thus has embedded closed cells with Boolean face intervals, even though two different quotient cells can share more than one face.

The quotient space is R^d/Gamma, which is homeomorphic to T^d. The homeomorphism statement is geometric; matching Betti numbers alone would not establish it. No comparable flat, unimodular, or lattice realization is assumed for a general simplicial-poset torus.

## 7. Other routes stay within their actual scope

The product computation concerns the standard staircase triangulation: C(p+q,p)(p+1)!(q+1)!-(p+q+1)!=(p+q)!pq. It cannot be promoted to a lower bound on every triangulation of a product. The mapping-torus paper supplies 120 graph vertices, hence 120 four-simplices, in the inspected construction, and does not identify arbitrary monodromy with the identity.

For the cup-product theorem, closed regular simplex cells are contractible and the d coordinate classes on T^d have nonzero product. Therefore the exponential bound applies. For a generic linear dependence among d+1 vectors with all coefficients nonzero, exactly two of the 2^(d+1) independent sign assignments make all coefficients share a sign. This explains the factor 2^(-d) and excludes the proposed factorial probability substitution. The published 2026 Corollary 1.2 agrees with the inspected preprint on this point.

## Primary references

- Murai, OWR 08/2011, pp. 396–398: https://ems.press/content/serial-article-files/46323?nt=1
- Murai, Theorem 2.1, Proposition 4.1, Corollary 4.2, Lemma 6.1: https://arxiv.org/abs/1010.0319
- Basak–Datta, definitions, Theorem 1.4 and Lemma 3.1(v): https://arxiv.org/abs/1308.6137
- Dilks–Petersen–Stembridge, Section 2.4: https://arxiv.org/abs/0709.4291
- Avvakumov–Karasev, published Corollary 1.2: https://link.springer.com/article/10.1007/s00454-026-00823-z
- Basak, Theorem 5 and construction: https://arxiv.org/abs/1509.08217
