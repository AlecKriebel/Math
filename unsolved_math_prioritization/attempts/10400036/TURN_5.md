# Author turn 5: finite descent, a fixed-link obstruction, and the final gap

**Final author outcome: scoped partial results; the requested unrestricted iterated-derived-link construction was not established after five substantive turns.** No claim is made that the original problem is currently open in the literature. No novelty is claimed for the classical algebraic/topological deductions assembled here.

The final route tests whether the proper surface from Turn 4 can be converted into a finite ordinary derived link downstairs while retaining the original last strand. It produces an exact obstruction to a substantial class of such attempts, but not to every interpretation permitted by Polyak's wording.

## 1. No fixed ordinary derived link can represent the full coefficient

Fix $r\ge2$ straight, based strands in a ball, with their standard boundary closures, and let $M_0$ be their exterior. Its fundamental group is the free group on meridians $x_1,\ldots,x_r$. Let $C$ be any fixed finite integral combination of smooth oriented closed curves in the interior of this exterior, disjoint from the fixed boundary closing arcs. A finite oriented link is a special case.

**Proposition.** There is no such fixed $C$, depending only on these first $r$ strands, for which

$$
\operatorname{lk}(C,\widehat L_*)=\mu_{12\cdots r,*}(L)
\tag{1}
$$

holds for every additional based strand $L_*$ disjoint from $C$ and the first strands. The hat denotes its fixed boundary closure. This includes integer-weighted finite links $C$ and does not assume that $C$ is the boundary of a particular surface.

**Proof.** Choose a reference completion arc $L_*^0$, disjoint from $C$, whose closure represents the identity in $\pi_1(M_0)$. For example perturb the straight reference arc slightly to avoid $C$; this preserves its class in $M_0$. A regular diagram with only the last strand varied, or the direct group definition, identifies the target coefficient with that of the based closed last arc in the free meridians of $M_0$.

Every finite meridian word $w$ can be represented by a based loop in $M_0\setminus C$. The inclusion of this complement into $M_0$ is surjective on fundamental groups: a one-dimensional loop can be perturbed away from a one-dimensional cycle in a three-manifold. Insert such a loop into the reference completion and perturb the resulting proper arc into an embedding, relative to its endpoints, while staying disjoint from $C$ and the first strands. Call the completion $L_*^w$. Its closure represents $w$ in $\pi_1(M_0)$, and in the complement of $C$ its homology class is the sum of the reference closure and the inserted loop.

Use chosen representatives of words $u$ and $v$, and their concatenation as the representative of $uv$. Ordinary linking with the fixed cycle $C$ is additive on these one-cycles. If (1) held, its value on the identity completion would be zero. Hence it would force

$$
\mu_{12\cdots r,*}(L_*^{uv})
=\mu_{12\cdots r,*}(L_*^u)
+\mu_{12\cdots r,*}(L_*^v). \tag{2}
$$

Take $u=x_1\cdots x_{r-1}$ and $v=x_r$. The target Magnus coefficient is zero in each of $u$ and $v$, but it is one in $uv=x_1\cdots x_r$. This contradicts (2). All completions used above are finite embedded string links, obtained by general position in the fixed complement. ∎

The same obstruction can be formulated by the ordinary product rule for Magnus coefficients: the cross terms from proper subwords are nonzero, while ordinary linking with a fixed cycle is additive.

### Scope of this obstruction

The source does **not** require that a derived link be chosen once from the first strands and work for every possible final strand. Seifert surfaces can be chosen in the complement of the entire link, and “in an appropriate sense” can permit relative, based, or state-dependent corrections. Thus the proposition blocks a natural fixed-link descent of Turn 4 but is not a counterexample to Polyak's original request.

It explains why the construction of Turn 4 uses a lift and a closing path depending on the last strand's lower data, even though the covering surface itself can be chosen from the other strands alone.

## 2. The central extension has no homomorphic closing section

Retain $U=U_{r+1}(\mathbb Z)$, its top central subgroup $Z$, and $Q=U/Z$. For every $r\ge2$, the central extension

$$
1\longrightarrow Z\longrightarrow U\longrightarrow Q\longrightarrow1
\tag{3}
$$

does not split as a group extension.

Indeed let $A=I+E_{12}$ and $B=I+E_{2,r+1}$. Their commutator is $I+E_{1,r+1}\ne I$, while their images in $Q$ commute. Any other lifts of these two quotient elements differ from $A$ and $B$ by central factors, so their commutator is unchanged. A homomorphic section would send the commuting quotient pair to commuting lifts, a contradiction.

Thus the lower-data return paths in Turn 4 cannot be chosen to be globally multiplicative in the quotient data. This is an obstruction to an additive or stacking-compatible shortcut, not to using a fixed set-theoretic section with its explicit correction cocycle.

## 3. The triple case makes the missing state data visible

For the trivial two-strand sublink, the quotient cover in Turn 4 has deck group $Q=\mathbb Z^2$. Write a sheet as $(a,b)$. Its deformation-retract graph has horizontal edges $x_1$ and vertical edges $x_2$. It is the abelian cover of the two-petal rose: **the drawn grid squares are not filled two-cells**. Their boundary commutators are genuine nontrivial loops in this graph and in the covering handlebody.

For the zero-top section in $U_3$, the additive cover cocycle of Turn 4 is

$$
b((a,b),x_1)=0,\qquad b((a,b),x_2)=a.
$$

A reverse vertical edge contributes $-a$, and horizontal edges of either orientation contribute zero. Hence for a lifted word path starting at $(0,0)$,

$$
\mu_{12,*}=\sum_{\text{vertical steps}} a\,\Delta b. \tag{4}
$$

The lower-only closing path goes horizontally back to $a=0$ and then vertically to the origin. Both portions have zero contribution. Formula (4) is the signed lattice-area count for this based closure; equivalently it is the ordered-intersection count of Turn 1.

A unit square commutator has value 1, as it must. There is no contradiction with the cover cocycle being closed, because there is no square face on which a coboundary equation would set that integral to zero.

The section defect is explicit:

$$
s(a,b)s(a',b')s(a+a',b+b')^{-1}
=I+(ab')E_{13}. \tag{5}
$$

Its antisymmetric part is $ab'-a'b$, so it cannot be the coboundary of a scalar function on the abelian group $\mathbb Z^2$: every such two-coboundary is symmetric. This is the elementary degree-two instance of the nonsplitting in §2.

For concatenated paths the same computation gives

$$
c(uv)=c(u)+c(v)+a(u)b(v).
$$

This identifies the lower-order term that a fixed ordinary-linking construction would lose.

## 4. Why naive projection of the covering surface is not a finite construction

In the dual-cell representative corresponding to (4), the vertical edge at sheet $(a,b)$ has coefficient $a$. In a thickened-graph model, this can be represented geometrically by $|a|$ parallel meridian disks in that lifted vertical handle, oriented according to the sign of $a$. The resulting union is a proper locally finite surface upstairs. Over any one downstairs vertical edge there are infinitely many such lifted edges, with unbounded coefficients. Forgetting sheet labels would require an infinite, non-absolutely-convergent sum of these coefficients. In particular this natural representative has no locally finite unweighted cellular pushforward to the compact base exterior.

Pairing with a particular compact lifted longitude is nevertheless finite: that path visits finitely many edges and uses only finitely many coefficients. More generally, the compact curve and its transverse intersection points with the proper surface from Turn 4 lie in a compact region of the cover, so the intersection calculation can be localized to finitely many coordinate neighborhoods. This proves finiteness of the geometric calculation, but it does not manufacture a choice-independent finite downstairs derived link.

This paragraph does not claim that every surface representative has exactly the same projection pathology. The general obstruction to a faithful additive descent is the cohomological argument of Turn 4 and the fixed-link proposition of §1. Nor does it treat formal cancellation of infinitely many signed sheets as a valid finite geometric operation.

## 5. Comparison with the classical triple formula in its valid domain

For three closed components with all pairwise linking numbers zero, choose Seifert surfaces whose interiors avoid the other link components. Their pairwise intersections are closed curves. Mellor–Melvin's full primary theorem, and its explicit recovery of Cochran's case, give the triple Milnor invariant as minus the algebraic triple-intersection count. Orient the derived curve by

$$
L_{12}=-(F_1\cap F_2)
$$

relative to the convention in which ordered surface normals determine the triple-point sign. Then

$$
\operatorname{lk}(L_{12},L_3)
=-(F_1\cap F_2\cap F_3)
=\mu_{12,3}.
$$

The vanishing pairwise linking numbers remove the closed-link triple indeterminacy, so the associated string-link integer agrees. The cover intersection from Turn 4 gives the same number by its separately proved Magnus comparison. Thus the two descriptions are numerically consistent in this classical triple domain, with an explicit orientation convention.

This is a comparison of the two numerical invariants under the classical vanishing hypothesis. It is not a new ambient isotopy or cobordism comparison of the surfaces, and it does not extend the derived-curve construction to arbitrary lower values or all lengths. The full Cochran monograph was not recovered in this attempt; no additional all-order theorem is inferred from an unseen proof.

## 6. Final scoped disposition after five turns

The attempt establishes:

- necessary ordered lower corrections and explicit point-pushing examples;
- the canonical cut-open versus closed-group lift distinction and a complete degree-two transport formula for arbitrary string links;
- an integral all-order relative cocycle construction, with filling-choice independence and exact Milnor extraction;
- a genuine properly embedded surface in a marked nilpotent cover, whose pairing with a lower-data-corrected lifted last strand is the target coefficient;
- precise obstructions to fixed-link, additive, homomorphic-section, and naive sheet-forgetting descents; and a classical triple-domain consistency check.

None of these statements proves that the covering surface and corrected lift can be replaced by the source's appropriately defined recursively derived downstairs link for arbitrary based string links. No obstruction above covers every adaptive, relative or corrected construction allowed by that source wording. The full requested comparison is therefore **unproved in this attempt after 5/5 substantive author turns**.

The appropriate campaign disposition is a reviewed scoped partial, with the original target marked unsolved for this attempt if the separate adversarial audit passes. No final PR precedes that audit. The known skein, Gauss-diagram, configuration-space and surface-system results remain credited; this is not a claim of a new solution, a universal impossibility theorem, or current literature-wide openness.
