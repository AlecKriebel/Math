# Hostile review: frozen-color projection at \(k=3\)

## Verdict

**ACCEPT THEOREMS 2 AND 4 AND COROLLARIES 3, 5, AND 6, WITH ONE
REQUIRED SCOPE ADDENDUM.**

I re-derived the argument from the exact one-guard definition and found no
mathematical defect in the frozen-color projection, its domination-number
lift, the conditional induction step, the static list-coloring lift, or the
\(k=3\) odd-cycle consequence.

Before this note is promoted to an accepted campaign claim, it should state
explicitly that the projected eternal family
\(\mathcal P^\diamond_u\) need not be the **greatest** eternal family of
\(Q^\diamond_u\).  The independently verified graph `FCZbg` gives a
four-state projection inside a six-state greatest projected family.  Thus a
lower-parameter product strategy or clique partition cannot automatically be
lifted to colors in the original **family-response** lists.  The note already
avoids making that false inference in its proof of Theorem 4, but this strict
boundary deserves an explicit warning and witness because “exact smaller
instance” can otherwise be over-read.

Two nonblocking editorial clarifications are also recommended:

1. say “distinct \(x,y\)” in Lemma 8, so that both successive attacks are
   visibly at unoccupied vertices; and
2. in the two-list cycle argument, say that the greedy path is oriented to
   finish at \(y\), whose list omits the color assigned to \(x\).

No novelty claim is made in this review.

## Reviewed bytes

| artifact | SHA-256 |
|---|---|
| `math/working/k3_cross_state_attack.md` | `5a0ae81ca468441f161d21758b68036e7e58cf2f1f539f8dc8738885acbedca6` |
| `math/working/cross_state_response_exchange.md` | `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7` |
| accepted parameter-two reduction | `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13` |
| accepted maximum-independent-state lemma | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |
| C-051 theorem note | `543df545dea27669645979ce61451091140d4621f1e11cfdeeaa33437f4b5620` |
| C-051 hostile review | `4da9ddf1b9d1f4087e5617dc6f6ae2428c0dd1ec576b8f89a3166418e4b7f7cb` |
| this review's independent probe | `40d86a20713da48263021ca603b137edbae53ab3dc10d453f96d5367554d8ba8` |
| independent probe result | `bb4dcc3767ae79b3c7d6e8a86014994165f2c04fb838096d424239a496caf87c` |

The machine evidence is in `probe.py` and `probe_result.json` in this
directory.  It uses verifier B's ordinary `frozenset` graph representation,
the literal eternal-family checker, and no helper from the working-note
probe.

## 1. Exact model and quantifier audit

The note uses the correct model throughout:

- every attack used in a proof is at a vertex outside the current state;
- exactly one guard traverses one graph edge;
- every successor invoked through family membership is dominating; and
- closure is existential for each state/attack pair, never a simultaneous
  all-guards move.

The two list notions remain separate:

\[
L^{\mathcal F}_S(x)
=\{u\in S:ux\in E(G),\ S-u+x\in\mathcal F\}
\subseteq
L^{\mathrm{stat}}_S(x).
\]

The proof never replaces a family-list membership by mere static viability.
The only direction used between the notions is the valid implication

\[
u\notin L^{\mathrm{stat}}_S(x)
\Longrightarrow
u\notin L^{\mathcal F}_S(x).
\]

The fixed reference \(S\) is assumed to belong to the arbitrary eternal
family \(\mathcal F\).  In the conjecture setting this follows, for every
maximum independent \(S\), from the accepted independent-state forcing
lemma.  Theorem 2 itself does not silently assume that \(\mathcal F\) is the
greatest family.

## 2. Lemma 1 re-derivation

Let \(D\in\mathcal F\), \(U=S-D\), and \(X=D-S\).  Fix \(u\in U\).
Starting afresh at \(D\), attack the vertices of \(U-\{u\}\).

An occupied member of \(S\) cannot answer an attack at a different member of
\(S\), because \(S\) is independent.  A guard already moved into \(S\)
cannot answer a later such attack for the same reason.  Therefore
\(|U|-1\) distinct guards originally in \(X\) are moved into
\(U-\{u\}\).  Since \(|U|=|X|\), the resulting state is exactly

\[
S-u+x
\]

for one \(x\in X\).  The attack at the still-unoccupied \(u\) can be
answered by no guard in \(S-\{u\}\); closure forces \(x\to u\).  Thus
\(ux\in E(G)\), and the pre-attack state \(S-u+x\) lies in
\(\mathcal F\).  Hence

\[
u\in L^{\mathcal F}_S(x).
\]

This proves the required restoration inclusion with the correct
“for every missing \(u\), there exists an outside \(x\)” quantifiers.

## 3. Theorem 2 re-derivation

Fix \(u\in S\), either list notion \(\diamond\), and

\[
Q=G[(S-\{u\})\cup W^\diamond_u],\qquad
\mathcal P=\{A:|A|=k-1,\ \{u\}\cup A\in\mathcal F\}.
\]

### Nonemptiness

The state \(S-\{u\}\) belongs to \(\mathcal P\) because \(S\in\mathcal F\).
No greatest-family assumption is involved.

### Literal projected closure

Take \(A\in\mathcal P\), put \(D=\{u\}\cup A\), and attack an arbitrary
\(r\in V(Q)-A\).  This is unoccupied in \(D\), since \(u\notin V(Q)\).

If \(u\to r\) were a retained family response, its successor
\(D'=A\cup\{r\}\) would miss \(u\), while every member of \(D'-S\) would
lie in \(W^\diamond_u\).  For family lists those vertices omit \(u\)
directly; for static lists they omit \(u\) from the family lists by the
displayed inclusion above.  Lemma 1 applied to \(D'\) nevertheless forces
\(u\) into the union of precisely those family lists, a contradiction.

Therefore the retained response must be \(v\to r\) for some \(v\in A\),
and

\[
A-v+r\in\mathcal P.
\]

This is the exact one-guard closure obligation for the projected family.

### Domination of projected states

Domination is not assumed by naively deleting \(u\).  It is proved:
for every \(r\in V(Q)-A\), the preceding closure argument exhibits a
neighbor \(v\in A\).  Occupied vertices dominate themselves.  Hence every
\(A\in\mathcal P\) dominates \(Q\).

### Exact \(\alpha\) and \(\gamma^\infty\)

The independent set \(S-\{u\}\) gives
\(\alpha(Q)\geq k-1\), while the explicit projected eternal family gives
\(\gamma^\infty(Q)\leq k-1\).  The general inequality
\(\alpha\leq\gamma^\infty\) sandwiches both values at \(k-1\).

### Domination-number lift

Under \(\gamma(G)=k\), the projected state \(S-\{u\}\) proves
\(\gamma(Q)\leq k-1\).  If \(B\) with \(|B|\leq k-2\) dominated \(Q\),
then every vertex outside \(Q\), other than \(u\), has
\(u\in L^\diamond_S(x)\), and therefore is adjacent to \(u\).  Thus
\(B\cup\{u\}\) would dominate all of \(G\) with at most \(k-1\) vertices.
This contradiction proves \(\gamma(Q)=k-1\).

This lift uses \(\gamma(G)=k\), not minimum-counterexample minimality.

## 4. Corollary 3 and absence of circularity

Theorem 2 supplies

\[
\gamma(Q)=\gamma^\infty(Q)=k-1.
\]

If the conjecture has already been proved for common parameter \(k-1\),
applying it to \(Q\) gives \(\theta(Q)=k-1\).  This is a conditional
induction step, not an attempted proof of the induction hypothesis.

At \(k=3\), the needed lower-parameter statement is independently available
in the stronger accepted form

\[
\alpha(Q)=\gamma^\infty(Q)=2\Longrightarrow\theta(Q)=2.
\]

No minimum-counterexample argument and no instance of C-051 enters this
deduction.

## 5. Theorem 4 re-derivation

Take a partition of \(Q^{\mathrm{stat}}_u\) into \(k-1\) cliques.
The \(k-1\) vertices of the independent set \(S-\{u\}\) occupy distinct
parts.  Since the number of parts is also \(k-1\), each part contains
exactly one such anchor.

For \(x\in W^{\mathrm{stat}}_u\), let \(v\) anchor its part.  Then
\(vx\in E(G)\).  Replacing the anchor \(v\) by \(x\), while retaining every
other anchor, selects one representative from every clique part and hence
dominates \(Q^{\mathrm{stat}}_u\).  Adding \(u\) dominates all vertices
outside \(Q^{\mathrm{stat}}_u\), because every such outside vertex is either
\(u\) or has \(u\) in its static list and is adjacent to \(u\).  Therefore

\[
S-v+x
\]

dominates \(G\), so \(v\in L^{\mathrm{stat}}_S(x)\).  Equal anchor colors
form subsets of clique parts of \(G\), and hence give a proper coloring in
\(\overline G\).

The proof correctly makes no analogous claim for family lists.

## 6. Corollaries 5 and 6

For \(k=3\), every projection has
\(\alpha(Q)=\gamma^\infty(Q)=2\).  The accepted parameter-two theorem
therefore gives \(\theta(Q)=2\), equivalently that \(\overline Q\) is
bipartite.  The static list statement then follows from the anchor coloring
in Theorem 4.

If every vertex of an odd complement cycle has list \(\{a,b\}\), every
cycle vertex lies in \(W_c\).  The cycle is therefore contained in a
bipartite projected complement, an immediate contradiction.  The same
argument works for family and static lists separately.

The conclusion is only that an odd obstruction must collectively use all
three colors.  It does not make three separately valid deletion colorings
compatible.

There is a harmless strengthening available: at \(k=3\), the bipartite
projection conclusion uses only the existence of an eternal three-family
containing an independent triple, not the extra equality \(\gamma(G)=3\),
because Theorem 2 already gives
\(\alpha(Q)=\gamma^\infty(Q)=2\).  The static anchor-coloring proof likewise
needs only \(\theta(Q)=2\).  The note's stated version is weaker but correct.

## 7. Comparison with C-051

C-051 projects through a closed antineighborhood

\[
G-N[A]
\]

of an independent set \(A\).  Its clique-cover conclusion for a general
parameter uses minimum-counterexample minimality.

The present projection instead keeps the other reference anchors and the
vertices omitting one response color:

\[
G[(S-\{u\})\cup W^\diamond_u].
\]

Its literal family closure is proved by the arbitrary-state restoration
argument.  Its domination-number lift uses only \(\gamma(G)=k\), and its
\(k=3\) clique-cover conclusion uses the universal accepted parameter-two
theorem.  Consequently:

- Theorems 2 and 4 do not assume \(G\) is a minimum counterexample;
- no \(\theta\)-conclusion from C-051 is imported;
- the projected closure is not inferred from a static induced-subgraph
  argument; and
- there is no circular use of the original conjecture in Corollaries 5 or 6.

## 8. Required non-greatest-family boundary

The theorem proves that \(\mathcal P^\diamond_u\) is **an** eternal family
of \(Q^\diamond_u\), not that it is the greatest one.  This distinction is
strict.

The independent witness is:

\[
G=\texttt{FCZbg},\qquad
S=\{0,4,6\},\qquad u=4.
\]

For the greatest eternal three-family of \(G\), the family-response lists
are

\[
\begin{array}{c|c}
1&\{4,6\}\\
2&\{4,6\}\\
3&\{0\}\\
5&\{6\}.
\end{array}
\]

Thus \(W^{\mathcal F}_4=\{3,5\}\) and the projected graph has original
vertex set \(\{0,3,5,6\}\), graph6 `Cr`.  The frozen projection is

\[
\mathcal P^{\mathcal F}_4
=\{05,06,35,36\},
\]

whereas the greatest eternal two-family of `Cr` is

\[
\{03,05,06,35,36,56\}.
\]

Both families pass a literal independent checker.  The inclusion is proper.
Therefore a response or coloring available in the smaller graph's greatest
family may use states \(03\) or \(56\) that do not lift to the original
family slice.

This does not damage Theorem 2, Corollary 3, or Theorem 4.  It does block the
stronger, tempting inference that a lower-parameter product strategy
automatically supplies a coloring from the original family-response lists.
That boundary should be recorded explicitly in the theorem note.

## 9. Independent bounded falsification

The review probe recomputed the following with verifier B and literal
family checking:

| population | graphs | eligible \(\alpha=\gamma^\infty\) graphs | independent reference states | projections | projected states | projected attack obligations |
|---|---:|---:|---:|---:|---:|---:|
| all connected unlabeled graphs, orders \(2\) through \(7\) | 995 | 952 | 2,657 | 15,234 | 57,899 | 119,987 |
| MMV 2022 Table 9 catalog | 56 | 55 | 322 | 1,932 | 12,231 | 27,733 |

Every tested family and static projection was nonempty, dominating, and
closed under every unoccupied attack.  Every projected independence number
was exactly \(k-1\); every applicable domination lift was exact; every
tested \(k=3\) projected complement was bipartite; and all tested static
anchor assignments belonged to the original static lists.

To probe the theorem's arbitrary-family quantifier rather than only greatest
families, the checker exhaustively enumerated all subsets of:

- the six-state greatest family of \(C_4\), finding seven eternal
  subfamilies and checking all 56 resulting projections; and
- the twelve-state greatest family of `FCpbO`, finding its unique eternal
  subfamily and checking all 36 projections.

The named controls also matched the note:

- \(C_4\) has all-six-pair greatest family and trivial one-anchor
  projections;
- \(C_7\) has no eternal three-family, and its static \(u=0\) projection is
  nonbipartite; and
- `J@l|bfNuVK_` has
  \((\gamma,\alpha,\gamma^\infty,\theta)=(3,3,4,4)\), no eternal
  three-family, and three bipartite static deletion projections despite its
  uncolorable mixed residual core.

These computations are falsification evidence only.  The accepted verdict
rests on the analytic proofs above.

## 10. Residual boundary audit

The four-vertex path list assignment in Section 6 is indeed
vertex-minimal uncolorable while every single missing-color subinstance is
list-colorable.  It is correctly labeled an abstract list obstruction, not
an eternal-equality graph.

Full-list vertices lie in no omission set \(W_u\), so the projection cannot
see a core made entirely of full-list vertices.  Mixed-color cut blocks can
also connect individually colorable deletion pieces incompatibly.  The
`J@l|bfNuVK_` control confirms this phenomenon at the static level.

Accordingly, the note's final stopping statement is accurate after adding
the non-greatest-family warning: the result eliminates a substantial
two-color odd-cycle branch but does not prove the full \(k=3\) slice and
does not resolve the universal conjecture.

## Revised-byte addendum

Date: 2026-07-26 PDT

I reviewed the corrected theorem note at SHA-256

`3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68`.

The revision makes all three requested changes:

1. it gives the exact `FCZbg` proper-subfamily witness
   \(\{05,06,35,36\}\subsetneq
   \{03,05,06,35,36,56\}\), explicitly warns that the projected family
   need not be greatest, and correctly says that a lower-parameter strategy
   cannot be lifted into the original family-response lists without a
   separate argument;
2. Lemma 8 now assumes distinct \(x,y\), so its successive attacks are
   explicitly unoccupied; and
3. the two-list cycle proof now orients the greedy path from the other
   neighbor of \(x\) to \(y\), whose list omits the color on \(x\).

These edits preserve the previously reviewed proofs and close the only
required scope defect.  The full finite scan was not rerun because none of
the theorem statements or algorithms changed; `probe_result.json`
intentionally remains bound to the initially reviewed bytes and the
analytic verdict above supplies the revised-byte bridge.

**FINAL VERDICT ON THE REVISED BYTES: ACCEPT.**

Theorems 2 and 4, Corollaries 3, 5, and 6, the explicit non-greatest-family
boundary, and the stated residual limitations are correct.  This is a
substantial parameter-\(3\) structural advance, not a proof of the full
\(k=3\) slice and not a resolution of the universal conjecture.  No novelty
claim is made by this review.
