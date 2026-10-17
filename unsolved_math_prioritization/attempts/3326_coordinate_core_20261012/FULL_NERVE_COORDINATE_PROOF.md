# Reconstructing the convex full-nerve consequence of an incidence realizer

## Scope, credit, and result

This is the third confirmed substantive pass on problem 3326 / OPG-596. It reconstructs the convex-representation consequence stated on p. 135 of de Fraysseix, Ossona de Mendez and Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*. The coordinates here are an explicit exponential specialization of the rapidly increasing-coordinate and radial-normalization construction in Ossona de Mendez, *Realization of Posets*. The argument below supplies the missing full-nerve justification directly from those coordinates. It does not claim a new result in the literature or a solution of the general triangle-and-segment conjecture.

In particular, the deduction does **not** infer a full nerve merely from separation of symmetric differences. It proves that no nonface has a common intersection by comparing different lifts of a hypothetical common point on the same positive ray. This removes the previously retained unproved dependency in the maximum-vertex-degree-three reduction.

Objects are finite closed filled convex hulls, and an intersection hypergraph means the inclusion-maximal index sets with nonempty common intersection. Intersections are unrestricted; no one-sided contact, boundary-only, or disjoint-interior property is asserted.

## 1. Constructive theorem

Let H=(V,E) be a finite hypergraph with nonempty edges covering V. Edge elements are labeled separately from vertex elements, even when an edge is a singleton. Suppose L_1,...,L_d is a realizer of its incidence poset P, whose strict relations are v<e exactly when v belongs to e. The number d here is the supplied realizer length; minimality of that length is unnecessary.

Reverse each L_i to obtain a realizer of the dual poset P*. Let r_i(x) be the position of x in the i-th reversed order, starting at 1. Choose an integer B>d, for example B=d+1, and put

    F_i(x)=B^{r_i(x)},
    F(x)=(F_1(x),...,F_d(x)),
    s_e=sum_i F_i(e),
    q_e=F(e)/s_e.

Thus every q_e lies in the positive part of the affine hyperplane sum_i z_i=1. Set

    C_v=conv{q_e : v belongs to e}.

Then, for every nonempty S subseteq V,

    intersection_{v in S} C_v is nonempty
    if and only if
    S is contained in an edge of H.

The affine hyperplane is a copy of R^{d-1}; for d=3, deleting the last coordinate gives an explicit rational planar representation. Since the full nerve is the downward closure of E, its maximal faces are exactly the inclusion-maximal members of E. Therefore the displayed family represents H itself as a maximal-common-intersection hypergraph whenever H is Sperner. In particular it does so for every covered loopless linear H. Nested singleton edges cannot be retained as separate maximal faces; the previous convention caveat remains unchanged.

### Empty case

If V=E=empty, use the empty family. Otherwise coverage makes each C_v nonempty. The empty index set is the customary empty face and needs no geometric witness.

## 2. Minimal nonfaces have size at most the realizer length

Let S={v_1,...,v_k} be an inclusion-minimal nonface of the downward closure of E. Coverage gives k>=2. For every i, minimality supplies an edge e_i containing S minus {v_i}; because S is a nonface, e_i omits v_i. These edges are distinct: if e_i=e_j for different i,j, that edge contains all of S.

For every i the incomparable pair v_i,e_i must be reversed in some original linear extension, so e_i precedes v_i in that extension. No one extension can reverse two of these pairs. Indeed, if it reversed the pairs indexed i and j, the cross-incidences give the impossible chain

    e_i < v_i < e_j < v_j < e_i.

Consequently k distinct extensions are needed, and k<=d. This is the usual standard-example reversal argument, included here rather than invoked as an external theorem. It applies without linearity or the Sperner assumption.

## 3. Reciprocal-coordinate separation bounds

For a vertex w define the positive linear functional

    h_w(z)=sum_i z_i/F_i(w).

If e contains w, then e<w in P*. Thus r_i(e)<=r_i(w)-1 for every i, and

    h_w(F(e)) <= d/B.                                      (1)

If e does not contain w, the pair e,w is incomparable. The reversed realizer therefore has an index i with r_i(e)>r_i(w). Its contribution alone is at least B, giving

    h_w(F(e)) >= B.                                        (2)

These are strict-gap certificates: d/B<B for B>d. They use the full incidence realizer, not only its restrictions to vertices or to edges.

For comparison with the source, the printed p. 151 growth condition is weaker than the inequality used immediately afterward. The choice B>d supplies the actual stronger condition F_i(y)>d F_i(x) whenever x precedes y. The full PDF text and rendered p. 151 were inspected. The argument here does not depend on adopting the weaker printed condition.

## 4. Radial lifting of a convex combination

If x belongs to C_v, choose coefficients lambda_e>=0 on edges containing v, with sum_e lambda_e=1 and

    x=sum_e lambda_e q_e.

All s_e are positive. Define

    t_v=1/(sum_e lambda_e/s_e),
    alpha_e=t_v lambda_e/s_e.

Then alpha_e>=0, sum_e alpha_e=1, and

    t_v x=sum_e alpha_e F(e).                              (3)

Thus a point of the normalized convex hull has a positive radial lift into the unnormalized convex hull. Different C_v may require different values of t_v; treating them as equal would be an invalid shortcut.

## 5. Excluding every minimal nonface

Suppose S is a minimal nonface of size k and x lies in all C_v for v in S. Choose one lift (3) for every v, and take v in S for which t_v is minimal. For each other w in S, positivity and linearity give

    h_w(t_v x)=(t_v/t_w) h_w(t_w x) <= d/B,                 (4)

where the final bound follows from (1) and the convex combination for w. Hence

    sum_{w in S minus {v}} h_w(t_v x) <= (k-1)d/B.          (5)

On the other hand, every edge e containing v omits at least one vertex w in S minus {v}, since no edge contains S. By (2), and because every remaining functional term is positive,

    sum_{w in S minus {v}} h_w(F(e)) >= B.

Taking the convex combination (3) for v proves

    sum_{w in S minus {v}} h_w(t_v x) >= B.                 (6)

But k<=d and B>d imply

    (k-1)d/B <= (d-1)d/B < B.

Equations (5) and (6) contradict one another. Thus no minimal nonface has a common point. Any nonface contains a minimal one, so no nonface has a common point either. Conversely, if S is contained in e, the point q_e lies in every C_v indexed by S. This proves the full-nerve theorem.

### An equivalent coefficient interpretation

Equation (4) and bound (2) imply that the coefficient mass in the minimum lift on edges omitting w is at most d/B^2. Since every supporting edge omits at least one other member of S, a union bound would give total mass at most (k-1)d/B^2<1. This is the same contradiction. The summed-functional proof above is shorter and supplies an explicit root-exclusion certificate for each possible minimum-lift vertex.

### Specialization to the intended planar linear class

Take d=3 and B=4. For a missing pair or triple, choose each possible minimum-lift root v. The relevant summed reciprocal functional is at least 4 on every F(e) incident with v, while a hypothetical common point at the minimum lift would give at most 3/4 for a pair or 3/2 for a triple. These are positive rational gaps. The earlier purely combinatorial pair/triple criterion for linear hypergraphs is consistent with this argument, but it is no longer needed as a separate premise: the realizer itself already bounds every minimal nonface by three.

## 6. Consequences and remaining triangle gap

For incidence dimension at most three, use a three-order realizer, repeating orders if necessary. The normalized planar formula is now certified for the whole nerve, including missing triples. Each C_v has at most deg_H(v) generating points, with degrees counting incident hyperedges. If every vertex degree is at most three, each C_v is a point, segment, or triangle. The previously accepted finite stability/inflation argument converts these, if desired, to nondegenerate rational filled triangles while preserving the full nerve and making all edge witnesses interior. Hence the maximum-vertex-degree-three subclass follows without an unproved convex-representation deduction, while retaining the published source credit.

The coordinate formula does not give a three-corner bound for larger degrees. The exact four-leaf-star fixture below has four extreme vertices in its central coordinate hull. That hypergraph itself has a segment representation, so this is a limitation of this construction, not a counterexample. The previous fixed-neighbor and inscribed-replacement obstructions also remain relevant. Coordinated global triangle construction is still unresolved by this report.

## 7. Finite verification boundary

The exact verification described in the accompanying historical summary verifies the entire incidence-order relation, every reciprocal-coordinate bound, rational normalization, minimal-nonface size bounds, and each root-exclusion certificate. For the planar fixtures, two different exact feasibility procedures check the nerve: enumeration of intersections of independent boundary lines, and Fourier-Motzkin elimination. Full-subfamily checking is used for small fixtures, while larger stars check all pairs and triples and all declared edges, invoking the proved linear criterion.

The fixtures include genuine dimension-one and dimension-two realizers, several stars, the chapter's five-vertex nonplanar example and its printed realizer, the three-dimensional standard example, a four-dimensional standard example testing the general statement, isolated singleton components, and the nested-singleton caveat. The latter is checked against the downward-closed nerve, not falsely accepted as a maximal-edge representation of a non-Sperner hypergraph.

Negative controls include a genuinely invalid realizer, wrong poset orientation, corrupted normalization, inadmissible growth, a non-strict mass-gap inequality, and three concurrent segments whose pairwise graph matches a triangle but whose triple intersection is spurious. Gates are explicit exceptions rather than Python assertions and are replayed under normal Python, -O, and -OO. Mutation controls use disposable copies, never canonical files. Finite tests corroborate rather than replace the universal proof.

## 8. Small exact examples

For the three-vertex hypergraph with edges e_0={v_1,v_2}, e_1={v_0,v_2}, e_2={v_0,v_1}, use original incidence orders

    L_1: v_1, v_2, e_0, v_0, e_1, e_2
    L_2: v_0, v_2, e_1, v_1, e_0, e_2
    L_3: v_0, v_1, e_2, v_2, e_0, e_1.

Reverse them and use B=4. The planar coordinates, obtained by dropping the third normalized coordinate, are

    q_e0=(8/9, 1/18),
    q_e1=(4/69, 64/69),
    q_e2=(1/66, 1/66).

Each C_vi is the segment between the two incident witnesses. All pairs intersect, but the three have no common point. The summed-functional lower bounds for the three possible minimum-lift roots are respectively 4425/1024, 4233/1024, and 4425/1024. Each exceeds the forbidden upper bound 3/2. These rational values directly certify the missing triple.

For the four-leaf star with edges e_i={v_0,v_i}, use

    L_1: v_0, v_1, e_1, v_2, e_2, v_3, e_3, v_4, e_4
    L_2: v_0, v_4, e_4, v_3, e_3, v_2, e_2, v_1, e_1
    L_3: v_1, v_2, v_3, v_4, v_0, e_1, e_2, e_3, e_4.

The four planar witnesses are

    q_e1=(4096/4161, 1/4161),
    q_e2=(8/9, 1/18),
    q_e3=(4/69, 64/69),
    q_e4=(1/4098, 2048/2049).

All four are extreme vertices of C_v0, as checked by exact rational orientation tests. Each leaf is its single incident witness. This explicitly shows why the certified convex construction alone does not settle the degree-four frontier.

## Sources

1. Patrice Ossona de Mendez, *Realization of Posets*, Journal of Graph Algorithms and Applications 6(1) (2002), 149–153. Rapidly increasing-coordinate construction and projective normalization: Theorem 2.1, pp. 150–151; the explicit exponential specialization is chosen here. [Publisher article](https://jgaa.info/index.php/jgaa/article/view/paper48), [publisher PDF](https://jgaa.info/index.php/jgaa/article/download/paper48/2922).
2. Hubert de Fraysseix, Patrice Ossona de Mendez and Pierre Rosenstiehl, *Representation of Planar Hypergraphs by Contacts of Triangles*, Graph Drawing 2007, LNCS 4875, 125–136. Convex maximal-intersection consequence and mixed-object conjecture: p. 135. [Publisher chapter](https://doi.org/10.1007/978-3-540-77537-9_15).

The full two primary source texts were read; p. 151 of the 2002 paper was also visually inspected. Source PDFs, extracted source text, screenshots, programs, and nonmathematical operational records are not distributed in this prose edition. This pass makes no claim about present-day literature status or novelty.
