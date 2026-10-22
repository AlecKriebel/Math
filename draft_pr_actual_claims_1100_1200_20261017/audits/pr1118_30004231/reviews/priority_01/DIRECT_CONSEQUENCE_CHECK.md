# Direct-consequence and definition checks: PR1118

This document isolates the exact mathematical bridges required by a priority argument. It does not replace the pinned proof’s independent validation.

## 1. The stable criterion is strictly weaker

Let $D=D_4=\operatorname{conv}(v_0,\ldots,v_4)$, $v_0=0,v_i=e_i$. Choose disjoint two-element subsets $A,B\subset\{0,\ldots,4\}$. A functional taking a common maximum on $A$, minimum on $B$, and a strictly intermediate value on the remaining vertex exposes
$$
Q=\operatorname{conv}(v_i:i\in A)+\operatorname{conv}(-v_j:j\in B).
$$
The two edge directions are independent by affine independence of the five simplex vertices, so $\dim Q=2$.

For $P_1=D\times[0,1]$, $P_2=(-D)\times[0,1]$, use the same base functional and zero interval coefficient. The exposed proper face is
$$
V=Q\times[0,2],
$$
with canonical summands
$$
V_1=\operatorname{conv}(v_i:i\in A)\times[0,1],
\quad
V_2=\operatorname{conv}(-v_j:j\in B)\times[0,1].
$$
Therefore
$$
\dim V_1=\dim V_2=2,\qquad \dim(V_1+V_2)=3.
$$
The printed condition fails: $3\ne2+2$. The criterion in [Sturmfels–Tevelev,Thm 4.3](https://arxiv.org/abs/0704.3471), and [Adiprasito 2020,p 2](https://webusers.imj-prg.fr/~karim.adiprasito/cint.pdf), holds for every nonempty subset: individual dimensions are at least 1 and the two-summand dimension 3 is at least 2.

The two endpoint faces $Q\times\{0\}$ and $Q\times\{2\}$ qualify for both conditions; each has summand dimensions 1 and 1 and dimension 2. In the larger poset,
$$
Q\times\{0\}<V>Q\times\{2\}
$$
is a path of two edges in the order complex. It joins the two endpoint components of the exact-filtered poset. All three faces are proper. This concrete witness prevents the whole-face convention from affecting the comparison.

Thus the positive stable theorem cannot prove that the exact-filtered poset is connected or shellable. Conversely, the disconnected exact-filtered example cannot disprove the stable theorem. A genericity hypothesis cannot be silently dropped or added to identify them.

## 2. A rank check catches the sphere-dimension issue

For any qualifying proper face in ambient $\mathbb R^n$, positivity and additivity imply $\dim F\ge2$. A strict chain contains at most one face of each dimension 2 through $n-1$, hence at most $n-2$ elements. Its simplex in the order complex has dimension at most $n-3$.

This is an elementary internal consequence of the printed definition. It explains why a literal wedge of $(n-2)$-spheres is a suspicious target unless the realization is rationally acyclic. It is not evidence about an unprinted intended statement.

The $D_3-D_3$ six-point example is a classical geometric instance. It does not answer shellability, since any finite discrete complex is shellable in dimension zero. The $D_4$-prism example adds the genuinely necessary non-shellability obstruction: two disconnected components of positive pure dimension. It also has nonzero $H_1$, so replacing the target dimension with $n-3$does not repair it.

## 3. What is already in the classical sources

The simplex-difference face description can be expressed using disjoint nonempty ordered index sets:
$$
F(A,B)=\operatorname{conv}(v_i:i\in A)+\operatorname{conv}(-v_j:j\in B),
\quad
\dim F(A,B)=|A|+|B|-2.
$$
This follows immediately by maximizing a functional on the first simplex and minimizing it on the second. Inclusion is coordinatewise inclusion of the two index sets. The same classical structure is encoded by the simplex/polar face lattice in [Fukuda–Weibel 2007,Theorems 1 and 6](https://arxiv.org/abs/math/0510470). Their “exact decomposition” terminology already names the dimension equality.

For four simplex vertices, the only mixed pairs have sizes $(2,2)$, giving six incomparable parallelogram facets. [Sturmfels–Tevelev 2007/2008,Examples 1.3 and 4.10](https://arxiv.org/abs/0704.3471) explicitly uses scaled opposite tetrahedra and the associated six-ray generic complete intersection. Therefore the small control should be presented as a classical illustration, not a new tropical construction.

For five vertices, the sizes $(2,2),(2,3),(3,2)$ give the 50 vertex/60 edge graph in the pinned proof. Its graph interpretation via the bipartite double cover of the Petersen graph is also classical graph structure. No claim of a new graph is justified.

The whole shared-interval construction can be reconstructed from these ordinary face rules and dimension arithmetic. That is mathematical dependence on classical geometry. It is not, by itself, historical evidence that the **particular exact-filter deletion and its full non-shellability consequence** was previously observed. Neither inspected Fukuda–Weibel paper states that consequence. This audit found no prior topology theorem or counterexample for which the needed identification with that exact filtered poset is already supplied. The exclusion criterion is broader than an identical construction: any previously valid nonshellability example or theorem for the exact printed poset, combined with the classical homology control, would complete a prior full negative resolution and trigger the user’s strict exclusion. Different examples and sources for the two assertions suffice. No such prior exact-poset nonshellability implication was identified in the inspected literature.

## 4. Why two tempting universality/counterexample routes stop

In [Frick–Sanyal 2017,Proposition 2](https://arxiv.org/abs/1607.07814), the complex is formed from subsets of a set of summand labels, with a condition that a fixed point avoids the corresponding sum. The target’s vertices instead are geometric faces of a fixed two-summand sum satisfying positivity and additivity. An “arbitrary complex occurs” theorem for the first object does not imply an arbitrary complex occurs for the second. A new exact realization theorem would be required.

**Historical v1.** The [9 June 2026 v1](https://arxiv.org/pdf/2606.10817v1), §8, used a projected arrangement tropicalization in $\mathbb R^5$. The first audit's comparison concerned only that version. It missed the later revision and did not establish current-version coverage.

### Current v2: construction and independent link check

The [24 July 2026 v2](https://arxiv.org/html/2606.10817v2), §8, is materially different. It constructs a schön 3-fold in $(\mathbb C^*)^8$. Let $\Sigma_0$ be the 3-skeleton of the fan of $\mathbb P^9$, stellar-subdivided at the cones generated by $A=\{e_1,e_2,e_3\}$ and $B=\{e_4,e_5,e_6\}$. The new rays are $a=\sum A$ and $b=\sum B$. The quotient is $Q:\mathbb R^9\to\mathbb R^9/(a-b)\cong\mathbb R^8$. Proposition 8.1 describes its images as a fan, with only $a$ and $b$ merged; Proposition 8.2 gives the schön property. Proposition 8.7 concerns the uniform rank-4 matroid on 10 elements and gives link homology $(\mathbb Z,\mathbb Z,\mathbb Z^{84})$ in degrees $0,1,2$.

Here is an independent topological check from that cone identification. The original link is the 2-skeleton of the 9-simplex, with 10 vertices. Subdividing the two disjoint triangular facets adds two vertices, six edges, and four triangles in total. The resulting complex $K_0$ has
$$
(f_0,f_1,f_2)=(12,51,124).
$$
Its homotopy type is unchanged by the stellar subdivisions; the full simplex 2-skeleton is simply connected, so Euler characteristic gives $\widetilde H_2(K_0;\mathbb Z)=\mathbb Z^{84}$.

The two new vertices have disjoint neighbor sets $\{1,2,3\}$ and $\{4,5,6\}$. Identifying them merges no edge or triangle. Hence $K$ has face vector $(11,51,124)$. On integral chains the quotient changes only $C_0$, killing the single vector $a-b$. The kernel complex is $\mathbb Z$ in degree zero. Its map to $H_0(K_0)$ is zero because $K_0$ is connected. The resulting long exact sequence gives
$$
H_1(K;\mathbb Z)=\mathbb Z,\qquad H_2(K;\mathbb Z)=\mathbb Z^{84}.
$$
Exact rational elimination independently gave boundary ranks $(11,40)$ before and $(10,40)$ after identification, with ordinary Betti numbers $(1,0,84)$ and $(1,1,84)$. These checks are conditional on the geometric fan-image assertion of Proposition 8.1, not a new audit of all algebraic propositions in the source. The pure 2-dimensional link is nonshellable because its first rational homology is nonzero.

### Why a polytopal fan realization does not supply the target

The printed condition depends on a specified Minkowski decomposition. This can be proved without a literature-absence assertion. Put $D=D_4$ and $Q=D-D$. The pair $(D,-D)$ has nonempty positive exact mixed-face poset: choose disjoint two-element subsets of the simplex vertices, giving a sum of independent edges. The pair $(Q,Q)$ has an empty such poset. Indeed, any common supporting functional exposes the same face $F$ on both summands, and
$$
\dim(F+F)=\dim F<2\dim F
$$
whenever $\dim F>0$. Vertices fail positivity; the whole polytope also fails additivity. Yet the two sums are $Q$ and $2Q$ and have exactly the same normal fan.

Thus even a complete sum normal fan does not determine the exact mixed-face selection. Embedding, completing, or coherently refining the v2 fan into a polytopal fan would still leave the central requirement of finding two summands whose qualifying faces carry the required obstruction. A source theorem giving that decomposition/selection or another exact-poset realization would count, but none was identified.

The older universality route was rechecked at its actual construction. Frick–Sanyal Proposition 2 uses one axis-parallel box for each vertex of an arbitrary complex and tests whether a fixed point is absent from sums over subsets of those box labels. It does not give the geometric face poset of a fixed two-summand sum, and no two-summand reduction with positive canonical faces and full dimension additivity is proved there. Adiprasito–Sanyal §5.3 and Proposition 5.9 start with a family of polytopes and relate its Cayley boundary faces to a relative complex; the stated Buchsbaum/Cohen–Macaulay conclusions assume simplicial summands in relative general position. They are not a realization theorem for arbitrary projected tropical links with the printed additional filter.

The references used in current §8 give the Bergman-link homotopy calculation (Ardila–Klivans, source reference [6]) and tropicalization of a monomial image (Maclagan–Sturmfels, source reference [24]). Those uses do not assert a two-summand exact-face correspondence. Source reference [33] is Sturmfels–Tevelev, whose relevant mixed-face criterion was separately inspected and uses subset dimensions, not full additivity.

Codimension by itself is not an obstruction to an exact filtered representation: nongeneric filtering can remove expected-dimensional pieces. Nor does the same-normal-fan example rule out some different representation of the v2 link or a suitable homotopy model. It proves that the proposed fan-realization shortcut has omitted necessary summand data. No earlier theorem or construction supplying that data and yielding the exact-poset nonshellability obstruction was identified.

### Supplementary restricted reverse-poset test

This test excludes only the literal assertion that the nonzero cone poset of the displayed v2 fan, with order reversed, is the entire printed qualifying face poset. It is not needed for the verdict and does not exclude other realizations or homotopy transfers.

If $F=F_1+F_2$ qualifies and $d=\dim F$, full additivity makes the addition map from $F_1\times F_2$ an affine isomorphism. Every product subface $G_1\times G_2$ is globally a canonical Minkowski-sum face: expose $F$ by $u$, choose a functional with independent prescribed restrictions on the two disjoint direction spaces, extend it to the ambient space, and perturb $u$ by a sufficiently small positive multiple. Finiteness of vertices ensures the perturbation exposes precisely the chosen $G_i$ on each summand.

Consequently the lower qualifying interval consists of products of positive-dimensional faces of $F_1$ and $F_2$. Minimal elements have dimension 2, and maximal chains ending at $F$ contain dimensions $2,3,\ldots,d$, hence $d-1$ elements.

In the source fan the merged ray $q$ is contained in precisely the six triangles
$$
q12,\ q13,\ q23,\ q45,\ q46,\ q56.
$$
Its link is the disjoint union of the cycles $12,13,23$ and $45,46,56$. In a reversed-poset identification, $q$ would map to a maximal qualifying face $F$. Source maximal chains beginning at $q$ have three elements, so the previous rank calculation forces $\dim F=4$; this is an abstract rank conclusion, not the geometric dual-face dimension of an $\mathbb R^8$ ray.

The positive summand dimensions of this $F$ are $(1,3),(2,2)$, or $(3,1)$. For $(1,3)$ or $(3,1)$, the strict lower qualifying interval has connected edge–facet incidence graph of the 3-polytope. For $(2,2)$, it is a subdivision of the complete bipartite graph on the edges of the two polygons, hence connected. But the source strict upper interval above $q$ is the face poset of two disjoint cycles and has disconnected realization. This contradicts the restricted reverse-poset identification.

The obstruction leaves open different higher-dimensional filtered constructions, alternative posets with the same homology, or a prior general transfer theorem. Any proved earlier realization that yields an exact-poset nonshellability example would still trigger the strict exclusion criterion.


## 5. Remaining explicit limitation

The accessible Adiprasito manuscript is dated 27 July 2020. Its 2024 published successor has public metadata and an abstract identifying stable intersections, but its full body was paywalled. This audit proves a distinction from the **inspected 2020 definition** and from the published abstract’s advertised stable scope. It does not prove that no new 2024 remark discusses the exact-filtered counterexample. This is the most specific unresolved source-inspection gap, not a reason to invent either a prior resolution or a novelty certification.

