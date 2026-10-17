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

In [Hiatt–Simpson–Wang–Wu 2026,§8](https://arxiv.org/abs/2606.10817), a projected tropical fan is obtained by identifying two directions of an arrangement tropicalization under a monomial projection. No pair of polytopes or exact mixed-face realization is provided in the inspected construction. Its lower link homology therefore cannot be treated as an already solved instance of this face-poset question. Proving the missing representation would be substantive work. The comparison requires no acceptance of the paper’s particular numerical homology table.

## 5. Remaining explicit limitation

The accessible Adiprasito manuscript is dated 27 July 2020. Its 2024 published successor has public metadata and an abstract identifying stable intersections, but its full body was paywalled. This audit proves a distinction from the **inspected 2020 definition** and from the published abstract’s advertised stable scope. It does not prove that no new 2024 remark discusses the exact-filtered counterexample. This is the most specific unresolved source-inspection gap, not a reason to invent either a prior resolution or a novelty certification.

