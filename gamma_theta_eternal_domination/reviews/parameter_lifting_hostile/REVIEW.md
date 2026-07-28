# Hostile review: multi-anchor parameter lifting

Date: 2026-07-28 (PDT)

## Verdict

**UNCONDITIONAL PASS.**

I found no mathematical, model, complement, induction, or scope defect in
the frozen candidate
`math/working/parameter_lifting_audit/`.

The following candidate results are sound as stated:

1. the restoration lemma;
2. simultaneous freezing of every nonempty proper anchor set, for both the
   family and static response lists;
3. all displayed equalities for the projected graph;
4. exact static list coloring of every proper palette slice whenever the
   corresponding lower-parameter conjecture is known, and hence in every
   minimum-order counterexample;
5. the joint inactive-face suspension theorem;
6. the static list-coloring equivalence with a \(k\)-clique partition;
7. the conditional implication
   \[
   \mathsf P(k-1)+\mathsf{GL}(k)\Longrightarrow\mathsf P(k);
   \]
8. every asserted property of the abstract list system
   \(Y_k=K_{k-3}\vee P_4\).

The negative conclusion is also correct: a complete parameter-three theorem
would not automatically prove the universal conjecture using only the
accepted frozen-projection and inactive-link results.  A palette-gluing
statement using additional graph or eternal-family dynamics remains open.

## Line-by-line hostile findings

### Restoration and family restriction

Starting from an arbitrary retained state \(D\), attacks on the missing
vertices of \(S\) are legal and must be answered by outside guards.  Once an
outside guard moves onto \(S\), independence of \(S\) prevents it from
answering a later restoration attack.  Therefore all but one missing anchor
can be restored, leaving exactly a state \(S-u+x\).  The final attack at
\(u\) has only \(x\) as a possible responder.  This proves both the edge
\(ux\) and membership of \(S-u+x\) in the family-response list.  No guard
identity assumption, all-guards move, or occupied-vertex attack is used.

For the projected family, if a frozen guard \(g\in A\) answered an attack,
every outside position in the successor would still have a response list
disjoint from \(A\).  Restoration applied to the now-missing \(g\) gives the
required contradiction.  Thus the responder lies in the unfrozen projected
state, and the successor remains in the restricted family.  This checks the
quantifiers for every state and every unoccupied target, rather than merely
checking domination at the reference state.

### Parameter equalities

The set \(S-A\) is independent of size \(k-|A|\), while the restricted
family supplies an eternal family of that size.  The universal inequality
\(\alpha\leq\gamma^\infty\) forces
\[
\alpha(Q_A)=\gamma^\infty(Q_A)=k-|A|.
\]
Closure also shows that every projected state, in particular \(S-A\),
dominates the projection.

When \(\gamma(G)=k\), a smaller dominating set \(C\) in the projection
would combine with \(A\) to dominate \(G\): projected vertices are dominated
by \(C\), anchors in \(A\) are occupied, and every omitted outside vertex
has a response-list member in \(A\), hence a graph neighbor in \(A\).
Therefore
\[
\gamma(Q_A)=k-|A|.
\]

If \(\mathsf P(k-|A|)\) is known, its use is direct.  In a minimum-order
counterexample, \(Q_A\) is a proper induced graph because it omits the
nonempty set \(A\).  If its clique-cover number exceeded its equality
parameter, it would itself be a smaller counterexample.  This is a valid
minimal-counterexample argument and does not assume clique-cover
monotonicity.

### Proper-palette coloring and graph/complement bookkeeping

A \(k-|A|\) clique partition of the projected \(G\)-graph contains exactly
one anchor of \(S-A\) in each part, because those anchors are independent.
Labeling each part by its anchor gives a proper coloring of the induced
complement.  Replacing the anchor in one part by another vertex of that part
selects one representative from every \(G\)-clique, hence dominates the
projection.  Adding \(A\) dominates every omitted vertex.  This proves
membership in the **static** response list.

The candidate correctly does not claim the same membership for the original
family-response lists.  It also correctly uses clique partitions of \(G\)
as color classes of \(\overline G\), not the reverse.

### Joint inactive-face suspension

For a target \(x\) avoided by an independent retained state \(T\), joint
inactivity gives \(x\in W_A^{\mathcal F}\).  Every common complement
neighbor of \(A\) either is an unfrozen anchor in \(T-A\), or has no
\(G\)-edge to any anchor in \(A\), so it also lies in the frozen projection.
The projected complement coloring therefore restricts to
\(H[\{x\}\cup N_H(A)]\).  The clique \(T-A\) lies inside \(N_H(A)\) and
has the matching size \(k-|A|\).  Both the upper and lower bounds in the
displayed chromatic/clique equality are valid.

The scope is exact: \(A\) must lie in one retained independent state avoiding
the target, and the clique-cover step needs either the lower-parameter
theorem or minimum-counterexample minimality.

### Conditional induction and its stopping point

With one frozen anchor, \(\mathsf P(k-1)\) gives a static list coloring of
every one-color-omission slice.  The proposed statement \(\mathsf{GL}(k)\)
then gives a coloring of the whole static list instance, and the
list-coloring equivalence gives \(\theta(G)=k\).  Thus the displayed
conditional implication is valid.  Iterating it from \(\mathsf P(3)\) also
requires \(\mathsf{GL}(k)\) at every higher parameter, exactly as the
candidate says.

No compatibility of separately chosen local colorings is proved or assumed.
The note therefore does not claim either a universal proof or an automatic
lift of a future \(k=3\) theorem.

### Abstract obstruction

In \(Y_k=K_{k-3}\vee P_4\), the singleton-listed clique forces every color
in \(D\).  The join blocks those colors on the path, leaving
\[
\{a\},\quad\{a,c\},\quad\{b,c\},\quad\{b\},
\]
which is uncolorable.  Deleting any path vertex permits the displayed
base-color assignment; deleting \(z_d\) frees \(d\) for the second path
vertex.  Thus the instance is vertex-minimal uncolorable.

Every proper palette either omits a forced color, excluding the entire
path, or contains \(D\) and omits at least one of \(a,b,c\), leaving a
colorable path subgraph.  Direct counting verifies clique-wise Hall, the
minimum-core degree bound, absence of full lists, and the collision-transfer
consequence.  This is a valid uniform abstract countermodel for every
\(k\geq3\).

It is only an abstract complement-list system.  It is not asserted to arise
from an equality graph or an eternal family, and hence it refutes only a
pure list-theoretic gluing inference, not \(\mathsf{GL}(k)\) itself.

## Independent computation

The clean-room checker `independent_check.py` imports no campaign search
code.  It exhausts all 1,099 labelled graphs through order five, all 663
optimal eternal subfamilies occurring in the 375 equality graphs, and all
independent reference states in those families.  It checked:

- 12,347 restoration inclusions;
- 12,960 frozen projections, split equally between family and static lists;
- 6,480 static proper-palette colorings;
- 6,710 joint inactive-face suspensions; and
- 2,129 bounded \(\mathsf{GL}\)-premise/conclusion controls.

It separately reconstructs and checks every property of \(Y_k\) for
\(3\leq k\leq11\).  The complete evidence and reproducible output are in
`EVIDENCE.md`.

## Exact claim boundary

This review accepts no claim that:

- \(\mathsf{GL}(k)\) has been proved;
- \(Y_k\) is physically realizable by an equality graph;
- a parameter-three theorem automatically lifts;
- the universal gamma--theta conjecture is resolved; or
- any literature-priority statement has been established.

