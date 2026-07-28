# The single-full deletion dichotomy at \(k=3\)

## Status and exact boundary

Date: 2026-07-27 (PDT)

This note works in the standard one-guard-moves model.  It assumes the
proved results in
`math/working/k3_full_list_slice/NOTE.md`, especially Corollary 2.3 and
Theorems 3.1, 4.1, 4.2, 5.2, and 5.3.

The outcome is a rigorous reduction, not a resolution.

1. **PROVED:** in a minimum \(k=3\) counterexample, deleting a full-list
   vertex gives exactly a critical four-color branch or an inherited
   \(\gamma=2,\alpha=\gamma^\infty=3<\theta\) near-miss.
2. **PROVED:** every three-coloring in the critical branch contains
   pairwise Kempe connections between all three colors on the complement
   link.
3. **PROVED:** every three-clique partition in the critical branch forces
   the eternal family to make a cross-part guard move before three selected
   link attacks can be completed.
4. **PROVED:** the three augmented 2-SAT failures split exactly into a
   pre-existing base obstruction or marked one-unit/two-unit terminal
   certificates.  A unit-free bicycle cannot be the new obstruction when
   the base formula is satisfiable.
5. **PROVED:** a marked two-list terminal is either on its corresponding
   spoke or is an \(A_\ast\) vertex whose missing response is purely
   dynamic.  Two terminals on distinct spokes either dominate \(G-x\) or
   have a common complement neighbor outside the link.
6. **AUDIT VERDICT:** the proposed slogan
   “minimal unsatisfiable response 2-CNF gives a canonical forbidden
   configuration or a dominating pair” is not currently a theorem.  With
   “canonical” interpreted logically it is the already proved 2-CNF
   terminal trichotomy; with “canonical” interpreted as a bounded physical
   graph configuration, the required shortening of arbitrary component
   paths is open.  In the \(\gamma(G-x)=2\) branch the dominating-pair
   disjunct is already Corollary 2.3, while in the
   \(\gamma(G-x)=3\) branch the slogan simply restates the missing
   \(\gamma=3\)-sensitive step.

No claim below resolves the \(k=3\) slice or the universal
\(\gamma\)--\(\theta\) conjecture.

## 1. Setup

Let \(G\) be a minimum-order counterexample with

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G),
 \qquad H=\overline G.
\tag{1.1}
\]

Let \(\mathcal F\) be an eternal family of triples, let

\[
 S=\{a,b,c\}
\tag{1.2}
\]

be independent, and assume that the full family-list set at \(S\) is

\[
 F_3(S)=\{x\}.
\tag{1.3}
\]

Put

\[
 R=N_H(x),\qquad
 Z=V(G)-(S\cup\{x\}\cup R).
\tag{1.4}
\]

Fullness makes \(x\) adjacent in \(G\) to all three anchors, so \(Z\) is
exactly \(N_G(x)-S\).  The accepted deletion theorem gives an eternal
family

\[
 \mathcal F^{-x}=\{D\in\mathcal F:x\notin D\}
\tag{1.5}
\]

in \(G-x\), with

\[
 \alpha(G-x)=\gamma^\infty(G-x)=3,
\tag{1.6}
\]

and preserves every response list at \(S\) for the remaining vertices.

## 2. Deletion--coloring trichotomy

### Theorem 2.1 — PROVED

Exactly one of the following occurs.

1. **Equality-critical deletion:**
   \[
   \gamma(G-x)=3,\qquad \theta(G-x)=3.
   \tag{2.1}
   \]
2. **Domination-drop critical deletion:**
   \[
   \gamma(G-x)=2,\qquad \theta(G-x)=3.
   \tag{2.2}
   \]
3. **Inherited near-miss:**
   \[
   \gamma(G-x)=2,\qquad
   \alpha(G-x)=\gamma^\infty(G-x)=3<\theta(G-x).
   \tag{2.3}
   \]

In cases 1 and 2,

\[
 \theta(G)=4,
\tag{2.4}
\]

and every three-clique partition of \(G-x\) meets \(R\) in all three
parts.  Equivalently,

\[
 \chi(H)=4,\qquad \chi(H-x)=3,
\tag{2.5}
\]

and every proper three-coloring of \(H-x\) uses all three colors on \(R\).

In cases 2 and 3 there is a dominating pair

\[
 \{p,q\}\subseteq R
\tag{2.6}
\]

in \(G-x\), and

\[
 N_H(p)\cap N_H(q)=\{x\}.
\tag{2.7}
\]

#### Proof

Corollary 2.3 of the accepted full-list note proves that
\(\gamma(G-x)\in\{2,3\}\), proves (2.1) when the value is three, and proves
(2.6)--(2.7) when the value is two.  If the value is two, either
\(\theta(G-x)=3\) or \(\theta(G-x)>3\); together with (1.6), the latter
alternative is exactly (2.3).

Suppose now that \(\theta(G-x)=3\).  Adding \(\{x\}\) as a fourth clique
gives \(\theta(G)\leq4\), while \(G\) is a counterexample, so (2.4)
follows.  If one part of a three-clique partition of \(G-x\) avoided
\(R=N_H(x)\), then \(x\) could be added to that part, giving a
three-clique partition of \(G\).  Hence every part meets \(R\).  Translating
clique partitions of \(G\) into proper colorings of \(H\) gives (2.5) and
the saturation assertion. \(\square\)

Thus any counterexample in this slice with \(\theta(G)\geq5\) must be in
case 3.  Case 3 is not a smaller counterexample to the original
conjecture: its deletion has \(\gamma=2<\gamma^\infty=3\).

## 3. What the critical branch forces

The next two lemmas apply to either case 1 or case 2 of Theorem 2.1.

### Lemma 3.1 (three pairwise Kempe linkages) — PROVED

Let \(\kappa\) be any proper three-coloring of \(H-x\).  For each two
distinct colors \(i,j\), some connected component of

\[
 (H-x)[\kappa^{-1}(\{i,j\})]
\tag{3.1}
\]

contains both an \(i\)-colored vertex of \(R\) and a \(j\)-colored vertex
of \(R\).

#### Proof

All three colors occur on \(R\) by Theorem 2.1.  Suppose no
\(\{i,j\}\)-component met both corresponding link color classes.  Swap
\(i\) and \(j\) on every \(\{i,j\}\)-component that meets the
\(i\)-colored part of \(R\).  Every \(i\)-colored link vertex is changed
to \(j\), and no \(j\)-colored link vertex is changed to \(i\).  The
result is a proper coloring of \(H-x\) in which \(R\) avoids \(i\).
Coloring \(x\) with \(i\) would then three-color \(H\), contradicting
\(\chi(H)=4\). \(\square\)

This is stronger than mere color saturation.  It does not say that the
Kempe paths stay inside the bipartite link \(H[R]\).

### Lemma 3.2 (forced cross-part escape) — PROVED

Fix a three-clique partition

\[
 V(G-x)=C_a\mathbin{\dot\cup}C_b\mathbin{\dot\cup}C_c
\tag{3.2}
\]

labeled so that \(u\in C_u\) for \(u\in S\).  Choose

\[
 r_u\in C_u\cap R
\tag{3.3}
\]

for every \(u\in S\).

There is a state \(D\in\mathcal F^{-x}\) having one guard in each part
and an attack at one of the still-unoccupied vertices \(r_u\) such that
the guard in \(C_u\) has a graph edge to \(r_u\), but its same-part
successor is not in \(\mathcal F^{-x}\).  Consequently every retained
response to that attack moves a guard from a different clique part into
\(C_u\).

#### Proof

Start at \(S\), and consider the attacks \(r_a,r_b,r_c\) in any fixed
order.  As long as the successor obtained by moving the guard in the same
clique part is retained, choose it.  The move is legal because each
\(C_u\) is a clique, and the resulting state still has one guard per part.

If all three same-part successors were retained, the final state would be
\(\{r_a,r_b,r_c\}\).  All three vertices lie in \(R\), so that state
fails to dominate \(x\), contradicting its membership in the original
family \(\mathcal F\).  Hence a first same-part successor is absent.
Closure of \(\mathcal F^{-x}\) still supplies a response to the
unoccupied attack, and every such retained response must come from a
different part. \(\square\)

This is a literal one-guard statement.  It identifies where every deletion
partition must depart from its ordinary one-guard-per-clique product
strategy.

## 4. Exact augmented-2-SAT fork

Let \(\Phi\) be the no-full-list projection formula for
\((G-x,\mathcal F^{-x},S)\).  List preservation shows that this is also
the base formula obtained from \(G\) after leaving the unique full vertex
\(x\) uncolored.

For \(w\in S\), the formula for assigning color \(w\) to \(x\) is

\[
 \Psi_w=\Phi\wedge U_w.
\tag{4.1}
\]

The augmentation \(U_w\) is supported only on \(R\):

- if \(y\in R\) and \(L_S^{\mathcal F}(y)=\{w\}\), it contributes the
  false constant;
- if \(y\in R\), \(L_S^{\mathcal F}(y)=S-\{u\}\), and
  \(w\in L_S^{\mathcal F}(y)\), it contributes the unit forbidding the
  port event \(P(y,w)\);
- every other vertex contributes nothing.

This is just Theorem 3.1 of the accepted full-list note specialized to one
full vertex.

### Theorem 4.1 (base obstruction or marked terminal certificate) — PROVED

All three formulas \(\Psi_w\) are unsatisfiable.  Moreover, exactly one of
the following logical regimes holds.

1. **Base-unsatisfiable regime:** \(\Phi\) is already unsatisfiable.  The
   obstruction survives deletion of \(x\) and is not caused by the full
   vertex.
2. **Augmentation-sensitive regime:** \(\Phi\) is satisfiable.  For each
   \(w\), either \(U_w\) contains an immediate false constant, or every
   inclusion-minimal unsatisfiable subformula of \(\Psi_w\) is:
   - a one-unit lollipop whose unit is from \(U_w\); or
   - a two-unit chain in which at least one terminal unit is from \(U_w\).

In particular, a unit-free bicycle cannot be a new obstruction in regime
2.

#### Proof

A satisfying \(\Psi_w\) would give a family-compatible proper coloring of
\(H\), hence a three-clique partition of \(G\), so every \(\Psi_w\) is
unsatisfiable.

Assume \(\Phi\) is satisfiable and there is no immediate false constant.
Choose an inclusion-minimal unsatisfiable subformula \(M\subseteq\Psi_w\).
It must contain a unit from \(U_w\), since otherwise it would be an
unsatisfiable subformula of \(\Phi\).  The accepted minimal-2-CNF terminal
trichotomy gives a two-unit chain, a one-unit lollipop, or a unit-free
bicycle.  The last case has no unit from \(U_w\) and is impossible.  In
the one-unit case the unique unit is augmented; in the two-unit case at
least one is augmented. \(\square\)

If \(\gamma(G-x)=3\), regime 1 would be an unsatisfiable no-full-list
response formula in the smaller equality graph \(G-x\), even though
\(\theta(G-x)=3\).  That would refute the response-list coloring mechanism
for an arbitrary family, not the gamma--theta conjecture itself.

## 5. Terminal geometry: spoke or dynamic omission

Recall

\[
 A_u=N_H(x)\cap N_H(u),\qquad
 A_\ast=\{y\in R:y\text{ is adjacent in }G\text{ to all of }S\}.
\tag{5.1}
\]

### Lemma 5.1 — PROVED

If \(y\in R\) has

\[
 L_S^{\mathcal F}(y)=S-\{u\},
\tag{5.2}
\]

then exactly one of the following holds:

1. \(y\in A_u\); the omitted response color is also the unique anchor
   missed by \(y\) in the graph;
2. \(y\in A_\ast\); the graph edge \(uy\) exists, but the direct successor
   \(S-u+y\) is absent from \(\mathcal F\).

#### Proof

Response membership for both colors in \(S-\{u\}\) includes adjacency in
\(G\) to those two anchors.  The remaining edge \(uy\) is either absent,
placing \(y\) in \(A_u\), or present, placing it in \(A_\ast\).  In the
second case \(u\notin L(y)\) says precisely that the direct successor is
not retained. \(\square\)

### Lemma 5.2 (dominating pair or external defect witness) — PROVED

Let \(y\in A_u\) and \(z\in A_v\) for distinct anchors \(u,v\).  Then

\[
 N_H(y)\cap N_H(z)\cap R=\varnothing.
\tag{5.3}
\]

Consequently, exactly one of the following holds:

1. \(\{y,z\}\) dominates \(G-x\), equivalently
   \[
   N_H(y)\cap N_H(z)=\{x\};
   \tag{5.4}
   \]
2. there is a common complement neighbor
   \[
   t\in N_H(y)\cap N_H(z)\cap Z.
   \tag{5.5}
   \]

In particular, alternative 2 is forced when \(\gamma(G-x)=3\).

#### Proof

If \(r\in R\) were adjacent in \(H\) to both \(y\) and \(z\), then
\(y-r-z\) would put \(y,z\) on the same side of one component of the
bipartite link \(H[R]\).  The accepted cross-spoke separation theorem
forbids two distinct spoke types on the same side, proving (5.3).

A pair fails to dominate \(G-x\) exactly when it has a common
\(H\)-neighbor other than \(x\).  Such a neighbor cannot be an anchor:
\(y\) sees in \(G\) both anchors other than \(u\), \(z\) sees both anchors
other than \(v\), and \(u\ne v\).  Equation (5.3) excludes \(R\), leaving
exactly \(Z\).  If \(\gamma(G-x)=3\), no pair dominates, so (5.5) follows.
\(\square\)

The dominating pair supplied by Corollary 2.3 in the
\(\gamma(G-x)=2\) branch cannot have both endpoints in the same spoke,
because that spoke's anchor would be undominated.  Thus, if neither
endpoint lies in \(A_\ast\), its endpoints lie on two distinct spokes.

Lemma 5.2 is the rigorous part of the proposed “dominating pair” framing:
for distinct spoke terminals it gives a sharp fork between a dominating
pair and a new residual witness.  It does not eliminate the residual
witness branch, and it does not cover \(A_\ast\) terminals or one-unit
lollipops.

## 6. Audit of the proposed canonical-configuration slogan

There are three inequivalent meanings of “minimal”:

1. inclusion-minimal in logical clauses;
2. minimal in Boolean variables; and
3. vertex/edge-minimal in the physical graph realization.

Only the first is covered by the accepted 2-CNF theorem.  It gives the
exact chain/lollipop/bicycle trichotomy.  When an implication path is
expanded back into \(H\), consecutive clauses are joined by parity-fixed
paths inside frozen projection components.  Those paths may be arbitrarily
subdivided, may intersect, and may revisit a component.  Clause-minimality
does not shorten them or make their union an induced hole.

Therefore:

- if “canonical forbidden configuration” means a logical terminal form,
  the slogan is true but adds no graph-theoretic mechanism;
- if it means one of the already excluded bounded physical lollipop or
  two-variable bicycle configurations, the claim is unproved for longer
  subdivisions and multi-variable bicycles;
- in the \(\gamma(G-x)=2\) deletion branch, a dominating pair is already
  known before inspecting the formula;
- in the \(\gamma(G-x)=3\) branch, asserting that every noncanonical
  response core creates a dominating pair is exactly the missing
  \(\gamma=3\)-sensitive theorem, since such a pair would contradict
  \(\gamma(G-x)=3\).

The exact `GFznc{` response-family control in
`math/working/k3_twosat_bicycle/NOTE.md` also shows that nonvacuous ridge
covariance can transport an unsatisfiable response formula rather than
shorten it.  That control has a dominating pair, so it does not refute the
equality-specific conjectural slogan; it shows only that covariance is not
the missing implication.

**Verdict:** the slogan is a useful research target, not a proved
dichotomy.  Treating it as a lemma would be circular in the
\(\gamma(G-x)=3\) branch.

## 7. Exact controls

The three named controls were recomputed with the ordinary-set/bitset
checkers already frozen in `k3_full_list_slice`.

### 7.1 Genuine order-12 full-list equality control

For the labeled graph

```text
Ksv`f\knJVis
```

(canonical `K{eYptMJynEn`), with \(S=\{1,2,3\}\) and \(x=0\),

\[
 \gamma(G-x)=2,\qquad \theta(G-x)=3.
\tag{7.1}
\]

The two dominating pairs of \(G-x\) whose unique common \(H\)-neighbor is
\(x\) are

\[
 \{6,8\},\qquad \{10,11\}.
\tag{7.2}
\]

The base response formula has exactly two compatible anchored colorings.
The augmentations for colors \(1\) and \(2\) are unsatisfiable, while the
augmentation for color \(3\) is satisfiable and gives the known clique
partition.

Each failed augmentation has a unique smallest two-unit/one-clause core.
Physically they are the complement paths

\[
 10-5-4-11\qquad(\text{color }1),
\tag{7.3}
\]

and

\[
 6-9-7-8\qquad(\text{color }2).
\tag{7.4}
\]

Their link endpoints are exactly the two pairs in (7.2).  This is positive
evidence for the proposed pattern, not a proof.  The graph is not in the
critical branch: one coloring of \(H-x\) avoids color \(3\) on \(R\) and
extends over \(x\).

### 7.2 `HCQebjw`

At \(S=\{0,1,2\},x=8\),

\[
 \gamma(G-x)=3,\qquad\theta(G-x)=3,
\]

but \(x\) is only statically full; its greatest-family list is
\(\{1\}\).  Its unique anchored coloring of \(H-x\) avoids color \(1\) on
\(R\) and extends over \(x\).  This control shows that family fullness and
the counterexample hypothesis cannot be dropped.

### 7.3 `FDzro`

In the displayed 17-state proper family at
\(S=\{0,1,2\},x=4\), the target is genuinely family-full, but

\[
 \gamma(G)=2.
\]

The base formula after deleting \(x\) has one coloring.  Color \(0\) for
\(x\) is blocked immediately by singleton-list vertices in \(R\), while
colors \(1\) and \(2\) extend.  This realizes the false-constant branch of
Theorem 4.1 and shows why equality is needed for the spoke conclusions.

## 8. Exact stopping boundary

The deletion split is now localized as follows.

- In the \(\gamma(G-x)=2\) branch, either \(G-x\) is a certified type of
  \(\alpha=\gamma^\infty=3<\theta\) near-miss, or \(x\) is a critical
  fourth-color vertex.  A dominating pair is already present.
- In the \(\gamma(G-x)=3\) branch, \(H\) is four-chromatic and
  \(x\)-critical.  Every deletion coloring has three pairwise link Kempe
  connections, and every deletion clique partition forces a cross-part
  family response.
- If the base formula is satisfiable, the remaining logical work is three
  marked chains/lollipops, not arbitrary unit-free bicycles.
- For two distinct spoke terminals, failure of a dominating pair forces a
  new common-neighbor witness in \(Z\).

No contradiction is known for the \(Z\)-witness branch, for an
\(A_\ast\) dynamic terminal, for a longer marked lollipop/chain, or for a
base formula that is already unsatisfiable.  Those are the precisely
delimited gaps.
