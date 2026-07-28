# Multi-anchor frozen projections and the exact parameter-lifting gap

## Status and claim boundary

Date: 2026-07-28 (PDT)

This note audits whether the accepted frozen-projection and inactive-link
results, together with a hypothetical proof of the parameter-three case,
would prove the full gamma--theta conjecture by induction.

The answer is:

1. **PROVED:** any nonempty proper set of anchors can be frozen
   simultaneously.  This gives an exact equality instance with that many
   fewer guards, without iterating or changing the reference response lists.
2. **PROVED:** in a minimum counterexample, every proper response-palette
   slice has an exact list-respecting coloring.
3. **PROVED:** any set of target-inactive guards lying in one retained
   independent state gives a jointly colorable target-link suspension.  This
   strictly generalizes the one-vertex inactive suspension C-112.
4. **REFUTED AS A PURE LIST INFERENCE:** even connected, vertex-minimal
   uncolorable list systems with no full lists can have every proper-palette
   slice colorable, satisfy clique-wise Hall, satisfy the C-059 degree and
   collision-transfer conditions, and still fail globally.
5. **OPEN:** the accepted eternal-family constraints might forbid those
   abstract gluing obstructions.  No proof of that dynamic statement is
   given here.

Consequently, a complete parameter-three theorem would be a genuine base
case, but it would **not automatically** lift to all parameters using the
currently accepted results.  The exact additional induction lemma is stated
in Section 6.

All statements use the standard one-guard-moves model.  Attacks occur only
at unoccupied vertices, exactly one adjacent guard moves, and every state of
an eternal family dominates.

The accepted sources read in full were:

- `math/lemmas/independent_antineighborhood_projection.md` (C-051);
- `math/working/k3_cross_state_attack.md` (C-063);
- `math/working/universal_transition_private_neighborhood_attack.md`
  (C-058);
- `math/working/universal_complement_local_balance_attack.md` (C-059);
- `math/lemmas/general_target_response_propagation.md` (C-108);
- `math/working/inactive_set_coloring_bridge/NOTE.md` (C-109); and
- `math/working/all_k_extension_bridge/NOTE.md` (C-112).

No literature-priority claim is made.  The universal conjecture is not
resolved here.

## 1. Response lists and a restoration fact

Let \(\mathcal F\) be an eternal family of \(k\)-sets in a finite simple
graph \(G\), and let \(S\in\mathcal F\) be an independent \(k\)-set.
For \(x\notin S\), define the family-response and static-response lists

\[
 L^{\mathcal F}_S(x)
 =
 \{u\in S:ux\in E(G),\ S-u+x\in\mathcal F\},
\tag{1.1}
\]

\[
 L^{\mathrm{stat}}_S(x)
 =
 \{u\in S:ux\in E(G),\ S-u+x\text{ dominates }G\}.
\tag{1.2}
\]

Thus

\[
 L^{\mathcal F}_S(x)\subseteq L^{\mathrm{stat}}_S(x).
\tag{1.3}
\]

Both lists are nonempty: attack \(x\) from \(S\).  In the equality setting
\(\alpha(G)=\gamma^\infty(G)=k\), every independent \(k\)-set belongs to
every eternal \(k\)-family, so any chosen maximum independent state can be
used as \(S\).

We record the restoration statement needed below.

### Lemma 1.1 (restoration) — PROVED

For \(D\in\mathcal F\), put

\[
 U=S-D,\qquad X=D-S.
\]

Then

\[
 U\subseteq\bigcup_{x\in X}L^{\mathcal F}_S(x).
\tag{1.4}
\]

#### Proof

Fix \(u\in U\).  Starting afresh from \(D\), attack every vertex of
\(U-\{u\}\).  A currently occupied vertex of \(S\) cannot answer an attack
at another vertex of \(S\), because \(S\) is independent.  Each attack
therefore moves an outside guard back to \(S\).  After these attacks, the
family contains a state \(S-u+x\) for some \(x\in X\).

Attack the still-unoccupied vertex \(u\).  No guard in \(S-\{u\}\) is
adjacent to \(u\), so the guard at \(x\) must answer.  Hence \(ux\in E(G)\)
and \(S-u+x\in\mathcal F\), proving
\(u\in L^{\mathcal F}_S(x)\). \(\square\)

## 2. Simultaneously freezing an anchor set

Fix a nonempty proper subset

\[
 A\subset S,\qquad |A|=t<k,
\]

and choose either list notion
\(\diamond\in\{\mathcal F,\mathrm{stat}\}\).  Define

\[
 W_A^\diamond
 =
 \{x\in V(G)-S:
       L^\diamond_S(x)\cap A=\varnothing\},
\tag{2.1}
\]

\[
 Q_A^\diamond
 =
 G[(S-A)\cup W_A^\diamond].
\tag{2.2}
\]

These are the attacks that cannot be answered from any frozen anchor in
\(A\), together with the unfrozen anchors.

Define

\[
 \mathcal P_A^\diamond
 =
 \{B\subseteq V(Q_A^\diamond):
   |B|=k-t,\ A\cup B\in\mathcal F\}.
\tag{2.3}
\]

### Theorem 2.1 (multi-anchor frozen projection) — PROVED

The family \(\mathcal P_A^\diamond\) is an eternal dominating family of
\((k-t)\)-sets in \(Q_A^\diamond\).  Consequently

\[
 \alpha(Q_A^\diamond)
 =
 \gamma^\infty(Q_A^\diamond)
 =
 k-t.
\tag{2.4}
\]

If in addition \(\gamma(G)=k\), then

\[
 \gamma(Q_A^\diamond)=k-t.
\tag{2.5}
\]

#### Proof

The family is nonempty because \(S-A\in\mathcal P_A^\diamond\).
Take \(B\in\mathcal P_A^\diamond\), put \(D=A\cup B\), and attack

\[
 r\in V(Q_A^\diamond)-B.
\]

Eternal closure gives a legal successor \(D-g+r\in\mathcal F\) for some
guard \(g\in D\cap N_G(r)\).

Suppose \(g\in A\).  Every outside-\(S\) vertex of the successor lies in
\(W_A^\diamond\).  In the family-list case its family-response list is
disjoint from \(A\).  In the static-list case its static list is disjoint
from \(A\), and (1.3) says its family list is also disjoint from \(A\).
The successor misses \(g\) from \(S\), while the union of the family lists
of all its outside positions avoids every element of \(A\).  This
contradicts Lemma 1.1.

Therefore \(g\in B\), and

\[
 B-g+r\in\mathcal P_A^\diamond.
\tag{2.6}
\]

This proves one-guard closure inside \(Q_A^\diamond\).  It also proves that
every member \(B\) dominates \(Q_A^\diamond\): each unoccupied vertex has
the adjacent responder in \(B\), while occupied vertices dominate
themselves.  Hence \(\mathcal P_A^\diamond\) is eternal.

The set \(S-A\) is independent of size \(k-t\), so

\[
 k-t\leq\alpha(Q_A^\diamond)
 \leq\gamma^\infty(Q_A^\diamond)\leq k-t,
\]

which proves (2.4).

Now assume \(\gamma(G)=k\).  The preceding closure proof shows that
\(S-A\) dominates \(Q_A^\diamond\), so
\(\gamma(Q_A^\diamond)\leq k-t\).
If a set \(C\) of at most \(k-t-1\) vertices dominated
\(Q_A^\diamond\), then \(A\cup C\) would dominate \(G\).  Indeed, vertices
inside the projection are dominated by \(C\), vertices of \(A\) are
occupied, and every outside vertex \(y\notin V(Q_A^\diamond)\cup A\) has

\[
 L^\diamond_S(y)\cap A\ne\varnothing,
\]

so it is adjacent in \(G\) to some member of \(A\).  This would give a
dominating set of size at most \(k-1\), a contradiction.  Thus (2.5)
holds. \(\square\)

### Why this is not merely an iteration of C-063

The response lists in a first projected family need not equal the original
response lists with one color deleted, and the projected family need not be
greatest.  Theorem 2.1 freezes all of \(A\) in one argument and retains the
single original predicate

\[
 L^\diamond_S(x)\cap A=\varnothing.
\]

It therefore gives an exact palette slice without assuming that response
lists behave functorially under repeated projection.

## 3. Exact coloring of every proper palette slice

Write \(\mathsf P(q)\) for the gamma--theta conjecture restricted to common
parameter \(q\):

\[
 \gamma(J)=\gamma^\infty(J)=q
 \quad\Longrightarrow\quad
 \theta(J)=q.
\tag{3.1}
\]

### Corollary 3.1 (conditional parameter drop) — PROVED

If \(\gamma(G)=\gamma^\infty(G)=k\) and \(\mathsf P(k-t)\) holds, then

\[
 \theta(Q_A^\diamond)=k-t.
\tag{3.2}
\]

If \(G\) is instead a minimum-order counterexample, then (3.2) holds for
every nonempty proper \(A\subset S\), without separately assuming any
\(\mathsf P(q)\).

#### Proof

Theorem 2.1 gives

\[
 \gamma(Q_A^\diamond)
 =
 \gamma^\infty(Q_A^\diamond)
 =
 k-t.
\]

Apply \(\mathsf P(k-t)\) in the first case.  In the second case,
\(Q_A^\diamond\) is a proper induced subgraph of \(G\).  If its clique-cover
number exceeded \(k-t\), it would be a smaller counterexample.  The general
chain gives the reverse inequality. \(\square\)

The static lists yield more than an unlabelled clique partition.

### Theorem 3.2 (list-respecting palette coloring) — PROVED

Under Corollary 3.1 with \(\diamond=\mathrm{stat}\), there is a proper
coloring

\[
 f_A:
 \overline G[W_A^{\mathrm{stat}}]\longrightarrow S-A
\tag{3.3}
\]

such that

\[
 f_A(x)\in L^{\mathrm{stat}}_S(x)
\quad\text{for every }x\in W_A^{\mathrm{stat}}.
\tag{3.4}
\]

#### Proof

Partition \(Q_A^{\mathrm{stat}}\) into \(k-t\) cliques of \(G\).
The independent set \(S-A\) has \(k-t\) vertices, so each clique part
contains exactly one of these anchors.  Label a part by its anchor.

For \(x\in W_A^{\mathrm{stat}}\), let \(v\in S-A\) label its part and put
\(f_A(x)=v\).  The vertices receiving one label lie in a \(G\)-clique, so
\(f_A\) is proper in \(\overline G\).

It remains to verify list membership.  Choose one vertex from every clique
part: use \(x\) in the \(v\)-part and the anchor of every other part.
This transversal dominates \(Q_A^{\mathrm{stat}}\).  Adding the occupied
anchors \(A\) dominates every vertex outside the projection, exactly as in
the final paragraph of Theorem 2.1.  The resulting set is \(S-v+x\), and
\(vx\in E(G)\) because \(v,x\) lie in one \(G\)-clique.  Hence
\(v\in L^{\mathrm{stat}}_S(x)\). \(\square\)

Put \(B=S-A\).  For the static lists, (2.1) can be rewritten as

\[
 W_A^{\mathrm{stat}}
 =
 \{x\notin S:L^{\mathrm{stat}}_S(x)\subseteq B\}.
\tag{3.5}
\]

Thus a minimum counterexample has the following strong property:

> For every nonempty proper palette \(B\subset S\), the induced list
> instance on all vertices whose entire static response list lies in \(B\)
> is properly list-colorable using \(B\).

If only \(\mathsf P(3)\) is assumed, Theorem 3.2 applies to every
three-color palette \(B\subset S\).  Equivalently, it controls every slice
obtained by freezing \(k-3\) anchors.  A vertex belongs to at least one such
slice exactly when its response list has size at most three.  Lists of size
at least four are invisible to all parameter-three projections.

## 4. Joint inactive-face suspensions

Let \(H=\overline G\), fix a target \(x\), and let \(T\) be a retained
independent \(k\)-state avoiding \(x\).  By C-108, whether a guard
\(r\in T\) can answer the attack at \(x\) is independent of the retained
independent state containing \(r\).  Call \(r\) **inactive at \(x\)** when

\[
 r\notin L_T^{\mathcal F}(x).
\tag{4.1}
\]

### Theorem 4.1 (joint inactive-face suspension) — PROVED

Assume \(G\) is a minimum-order counterexample of common parameter \(k\).
Let \(A\) be a nonempty proper subset of one retained independent
\(k\)-state \(T\) avoiding \(x\), and suppose every member of \(A\) is
inactive at \(x\).  Put \(t=|A|\).  Then

\[
 \boxed{
 \chi\!\left(H[\{x\}\cup N_H(A)]\right)
 =
 \omega\!\left(H[\{x\}\cup N_H(A)]\right)
 =
 k-t.
 }
\tag{4.2}
\]

More generally, the same conclusion holds in any equality graph if
\(\mathsf P(k-t)\) is known.

#### Proof

Use \(T\) as the reference state in Theorem 2.1 and use family lists.
The joint inactivity assumption says

\[
 L_T^{\mathcal F}(x)\cap A=\varnothing,
\]

so \(x\in W_A^{\mathcal F}\).

If \(z\in N_H(A)\), then either \(z\in T-A\), in which case it is an
unfrozen anchor of the projection, or \(z\notin T\).  In the latter case
no member of \(A\) is adjacent to \(z\) in \(G\), so
\(L_T^{\mathcal F}(z)\cap A=\varnothing\) and
\(z\in W_A^{\mathcal F}\).  Hence

\[
 \{x\}\cup N_H(A)\subseteq V(Q_A^{\mathcal F}).
\tag{4.3}
\]

Corollary 3.1 gives a \((k-t)\)-clique partition of the projected
\(G\)-graph, equivalently a proper \((k-t)\)-coloring of its complement.
Restricting this coloring proves the upper bound in (4.2).

Finally, \(T-A\) is a \((k-t)\)-clique of \(H\) contained in \(N_H(A)\).
This proves the matching lower bound. \(\square\)

For \(t=1\), Theorem 4.1 is C-112.  The direct multi-anchor proof adds all
higher-codimension cases.  For example, \(k-3\) jointly inactive guards
force a three-colorable suspension if \(\mathsf P(3)\) is known, while
\(k-2\) jointly inactive guards force a bipartite suspension.

This still does not select compatible color permutations on two overlapping
suspensions.  The passage from one inactive vertex to an inactive face
strengthens the local information but does not perform the global gluing.

## 5. The global conclusion is exactly a response-list coloring

Continue with \(\gamma(G)=\gamma^\infty(G)=k\), an independent
\(k\)-state \(S\), and the static lists \(L=L_S^{\mathrm{stat}}\).
Put

\[
 X=V(G)-S,\qquad H=\overline G.
\]

### Lemma 5.1 (static list-coloring equivalence) — PROVED

There is a proper list coloring

\[
 f:H[X]\longrightarrow S,\qquad f(x)\in L(x),
\tag{5.1}
\]

if and only if \(\theta(G)=k\).

#### Proof

If \(f\) exists, then for each \(u\in S\),

\[
 C_u=\{u\}\cup f^{-1}(u)
\]

is a clique of \(G\).  List membership gives every edge from \(u\) to its
fiber, and properness in \(H\) gives all edges inside the fiber.  The
\(C_u\) partition \(V(G)\), so \(\theta(G)\leq k\).  The parameter chain
gives \(\theta(G)\geq\gamma^\infty(G)=k\).

Conversely, let \(V(G)\) be partitioned into \(k\) cliques.  Since \(S\) is
independent of size \(k\), each part contains exactly one anchor \(u\in S\).
Color every outside vertex by the anchor of its part.  This is proper in
\(H\).  Replacing \(u\) in \(S\) by a vertex \(x\) of its part leaves one
representative in every \(G\)-clique part, hence a dominating set.  Also
\(ux\in E(G)\).  Therefore \(u\in L(x)\). \(\square\)

The family lists can be strictly smaller, and a clique partition of a frozen
family projection need not use family-response colors of the original
eternal family.  This is why Theorems 3.2 and 5.1 use the static lists.

## 6. The exact missing induction lemma

For \(u\in S\), write

\[
 W_u=\{x\in X:u\notin L(x)\}.
\tag{6.1}
\]

Here is the exact additional statement needed at parameter \(k\).

### Frozen-palette gluing statement \(\mathsf{GL}(k)\) — OPEN

Let \(G\) satisfy

\[
 \gamma(G)=\gamma^\infty(G)=k,
\]

let \(S\) be a maximum independent \(k\)-set, and use its static response
lists \(L\).  If every omission slice

\[
 (H[W_u],L|_{W_u}),\qquad u\in S,
\tag{6.2}
\]

has a proper list coloring, then the whole instance

\[
 (H[V(G)-S],L)
\tag{6.3}
\]

has a proper list coloring.

The premise in (6.2) is equivalent to requiring the list-colorability of
every proper-palette slice in (3.5): the palettes \(S-\{u\}\) are among the
proper palettes, and every smaller slice is an induced subinstance of one
of them.

### Theorem 6.1 (conditional induction) — PROVED

For \(k\geq2\),

\[
 \mathsf P(k-1)+\mathsf{GL}(k)
 \quad\Longrightarrow\quad
 \mathsf P(k).
\tag{6.4}
\]

Consequently, a hypothetical proof of \(\mathsf P(3)\), together with
\(\mathsf{GL}(k)\) for every \(k\geq4\), proves the universal conjecture.

#### Proof

Let \(\gamma(G)=\gamma^\infty(G)=k\), fix \(S\), and take
\(A=\{u\}\) in Theorems 2.1 and 3.2.  The hypothesis
\(\mathsf P(k-1)\) gives a proper list coloring of every \(H[W_u]\).
Apply \(\mathsf{GL}(k)\) to obtain a proper coloring of the entire static
response-list instance.  Lemma 5.1 gives \(\theta(G)=k\). \(\square\)

Thus the parameter drop itself is complete.  What is missing is a
simultaneous choice of the local colorings, including all cross-slice edges
and vertices with full response lists.

The target-response route has an analogous, narrower gluing obligation.
C-108 reduces extension over a target \(x\) to finding one proper
\(k\)-coloring of \(H-x\) that uses at most \(k-1\) colors on the inactive
set \(R_x\).  C-112 and Theorem 4.1 color every inactive-face suspension
separately.  They do not select one deletion coloring satisfying the global
inactive-palette bound.  The accepted equality control
``Ksv`f\knJVis`` already shows that an arbitrary deletion coloring cannot
be used.

## 7. A sharp abstract countermodel to naive gluing

The following family proves that \(\mathsf{GL}(k)\) cannot be replaced by a
pure list theorem using only the currently available local conclusions.
It is an abstract list system, **not** a claimed response-list realization
inside an eternal equality graph.

Fix \(k\geq3\).  Let the color set be

\[
 S=\{a,b,c\}\cup D,\qquad |D|=k-3.
\]

Let \(Y_k\) be the join of a clique

\[
 Z=\{z_d:d\in D\}
\]

and the four-vertex path

\[
 x_0x_1x_2x_3.
\]

Give the vertices the lists

\[
\begin{array}{c|c}
\text{vertex}&\text{list}\\ \hline
z_d&\{d\}\\
x_0&D\cup\{a\}\\
x_1&D\cup\{a,c\}\\
x_2&D\cup\{b,c\}\\
x_3&D\cup\{b\}.
\end{array}
\tag{7.1}
\]

### Proposition 7.1 (all proper slices color, the union does not) — PROVED

For every \(k\geq3\), the list instance \((Y_k,L)\) has all of the following
properties.

1. It is connected and vertex-minimal uncolorable.
2. No vertex has the full list \(S\).
3. Every proper-palette slice
   \[
   Y_k[\{v:L(v)\subseteq B\}],\qquad B\subsetneq S,
   \]
   is list-colorable.
4. Every clique \(C\) satisfies
   \[
   \left|\bigcup_{v\in C}L(v)\right|\geq |C|.
   \]
5. Every vertex satisfies \(d_{Y_k}(v)\geq |L(v)|\).
6. The C-059 collision-transfer list consequence holds: if
   \(xy\in E(Y_k)\) and \(u\in L(x)\cap L(y)\), then
   \[
   (L(x)\cup L(y))-\{u\}\ne\varnothing.
   \]
7. Nevertheless, \(Y_k\) has no proper \(L\)-coloring.

#### Proof

Every \(z_d\) is forced to color \(d\).  Since every \(z_d\) is adjacent to
every path vertex, no path vertex can use a color in \(D\).  The path lists
therefore reduce to

\[
 \{a\},\quad\{a,c\},\quad\{b,c\},\quad\{b\}.
\]

The first edge forces \(x_1=c\), while the last edge forces \(x_2=c\),
contradicting the middle edge.  This proves item 7.

Now take a proper palette \(B\subsetneq S\).  If \(D\nsubseteq B\), no path
vertex belongs to the slice; the included \(z_d\)'s form a clique with
distinct forced colors.  If \(D\subseteq B\), then \(B\) omits at least one
of \(a,b,c\).  Omitting \(a\) leaves at most the colorable edge
\(x_2x_3\), colored \(c,b\).  Omitting \(b\) leaves at most
\(x_0x_1\), colored \(a,c\).  Omitting \(c\) leaves at most the nonadjacent
pair \(x_0,x_3\), colored \(a,b\).  Omitting more base colors only takes an
induced subgraph of one of these.  Adjoin the distinctly colored clique
vertices \(z_d\).  This proves item 3.

Any clique consists of some vertices of \(Z\) and at most one edge of the
path.  A clique using one path vertex has at most \(k-2\) vertices and its
list union contains all \(k-3\) colors of \(D\) plus a base color.  For the
end edges, the union has \(k-1\) colors; for the middle edge, it has all
\(k\) colors.  Cliques contained in \(Z\) have distinct singleton lists.
This proves item 4.

For a path endpoint, degree and list size are both \(k-2\); for an internal
path vertex, both are \(k-1\).  Every \(z_d\) has degree \(k\) and a
singleton list.  This proves item 5.  On an edge from \(z_d\) to the path,
the common color \(d\) is accompanied by a base color in the path list.
The two \(z\)-lists on a \(Z\)-edge are disjoint.  Every path edge has a
list union of size at least two.  This proves item 6.

Deleting a path vertex leaves, respectively, the following base-color
assignments on the remaining path vertices:

\[
\begin{array}{c|c}
\text{deleted vertex}&\text{colors in path order}\\ \hline
x_0&(x_1,x_2,x_3)=(a,c,b)\\
x_1&(x_0,x_2,x_3)=(a,c,b)\\
x_2&(x_0,x_1,x_3)=(a,c,b)\\
x_3&(x_0,x_1,x_2)=(a,c,b).
\end{array}
\]

Deleting \(z_d\) frees color \(d\), and the path can be colored

\[
 x_0=a,\quad x_1=d,\quad x_2=c,\quad x_3=b.
\]

Together with connectivity this proves item 1.  Item 2 is immediate from
(7.1). \(\square\)

For \(k=3\), this is exactly the canonical mixed two-unit path obstruction.
For larger \(k\), the forced clique \(Z\) hides the same obstruction from
every proper palette while keeping every list non-full.  Therefore:

\[
 \boxed{
 \text{separate lower-parameter colorings do not glue by list theory alone.}
 }
\]

The checker

```text
python3 -I -B -W error \
  math/working/parameter_lifting_audit/verify_abstract_countermodel.py
```

independently verifies items 1--7 for every \(3\leq k\leq10\).  The proof
above is uniform and is the mathematical justification for all \(k\).

## 8. Audit verdict

A hypothetical complete \(k=3\) theorem would materially advance the
universal program:

- every three-color frozen palette would be exactly colorable;
- every \(k-3\)-inactive face would have a three-colorable target
  suspension; and
- an induction step from \(k-1\) would already have all of its
  lower-parameter instances certified.

It would not, with the accepted results alone, prove \(k=4\) or any larger
parameter.  The unresolved operation is not another parameter reduction.
It is one of the following genuinely global statements:

1. prove \(\mathsf{GL}(k)\) from full eternal closure and
   \(\gamma(G)=k\); or
2. in the target formulation, synchronize the jointly balanced inactive
   suspensions into one deletion coloring with a common responder color.

Proposition 7.1 rules out any proof of that step based only on
proper-palette list colorability, clique-wise Hall, minimum-core degree,
collision transfer, absence of full lists, and vertex-minimality.  A valid
continuation must use additional multi-state one-guard dynamics or the
no-\((k-1)\)-dominating-set condition in a way not encoded by those abstract
list properties.

No universal proof or counterexample is claimed.
