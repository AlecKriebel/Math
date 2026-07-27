# Gluing the three frozen-color projections at \(k=3\)

## Status and scope

Date: 2026-07-26 (PDT)

This note works in the standard one-guard-moves model.  Attacks are made
only at unoccupied vertices, exactly one adjacent guard moves, and every
retained family state dominates.

The outcome is exact but negative as an automatic proof mechanism.

1. When no family-response list is full, orienting the connected components
   of the three frozen-color bipartitions reduces **exactly** to 2-SAT.
   Singleton lists give parity units.  Every complement edge between two
   distinct two-lists gives one clause forbidding the endpoints from both
   taking their shared color.
2. The 2-SAT instance is satisfiable if and only if the three bipartitions
   glue to a global proper family-response list coloring.
3. A successful gluing transports across a ridge of independent family
   states by response covariance, and the underlying clique partition does
   not change.
4. Full family closure does **not** force the 2-SAT instance to be
   satisfiable.  The accepted `FDzro` family already refutes that assertion
   when \(\gamma=2\).  An explicit nine-vertex 46-state extension below
   shows that the additional dual deficient-pair witness layers \(W,Y\)
   still do not repair the failure.  Neither unsatisfiable example contains
   a pair of independent family states sharing a ridge, so these examples
   do not nonvacuously test covariance on an unsatisfiable instance.
5. The equality-specific assertion with
   \(\gamma=\alpha=\gamma^\infty=3\) remains open.  Full-list vertices are
   invisible to all three projections and remain a separate obstruction.

The symbolic statements proved below are labeled **PROVED**.  Finite
calculations are labeled **EXACT CHECK** or **OBSERVED**.  The evidence
script uses ordinary Python sets, at most nine vertices, and no SAT solver.
No order-14 computation was used.  No novelty or literature-priority claim
is made.

The prerequisite theorem and review files were read in full:

- `math/working/k3_cross_state_attack.md`;
- `math/working/universal_complement_local_balance_attack.md`;
- `math/working/cross_state_response_exchange.md`;
- `math/working/k3_mixed_p4_attack.md`; and
- their hostile and final integration reviews.

## 1. Setup

Let \(\mathcal F\) be an eternal family of triples, let

\[
 S=\{a,b,c\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).  For \(x\notin S\), write

\[
 L(x)=L^{\mathcal F}_S(x)
 =\{u\in S:ux\in E(G),\ S-u+x\in\mathcal F\}.
\tag{1.1}
\]

Every list is nonempty.  Put

\[
 O(x)=S-L(x),\qquad
 W_u=\{x\notin S:u\in O(x)\}.
\tag{1.2}
\]

The accepted frozen-color theorem says that

\[
 B_u:=H[(S-\{u\})\cup W_u]
\tag{1.3}
\]

is bipartite for every \(u\in S\).  The two anchors in \(S-\{u\}\)
are adjacent in \(H\), so they lie in the same connected component and on
opposite sides.

### Definition 1 (family-compatible anchored coloring)

A map

\[
 \kappa_S:V(G)\longrightarrow S
\tag{1.4}
\]

is a family-compatible anchored coloring at \(S\) if

1. \(\kappa_S(u)=u\) for \(u\in S\);
2. \(\kappa_S(x)\in L(x)\) for \(x\notin S\); and
3. \(\kappa_S\) is a proper coloring of \(H\).

Its color fibers are cliques of \(G\).  Hence its existence gives a
three-clique partition of \(G\), exactly as in the accepted
family-response coloring theorem.

The question is whether the bipartitions (1.3) force such a map.

## 2. Canonical component parities

Fix \(u\in S\), and order the two remaining colors as

\[
 S-\{u\}=\{r_u^0,r_u^1\}.
\]

On every connected component \(K\) of \(B_u\), fix a bipartition coordinate

\[
 \pi_u:K\longrightarrow\mathbb F_2.
\tag{2.1}
\]

On the anchor component, choose it so that

\[
 \pi_u(r_u^0)=0,\qquad \pi_u(r_u^1)=1.
\tag{2.2}
\]

The orientation of the anchor component is fixed.  Every other component
has one Boolean flip variable

\[
 z_{u,K}\in\mathbb F_2.
\tag{2.3}
\]

For uniform notation, set \(z_{u,K}=0\) on the anchor component.  The
oriented bipartition assigns

\[
 \beta_u(x)=r_u^{\,\pi_u(x)\oplus z_{u,K_u(x)}}.
\tag{2.4}
\]

These component flips are all the freedom present in the three
bipartitions.

### Singleton parity units

Suppose \(L(x)=\{v\}\).  For each \(u\in S-\{v\}\), the vertex \(x\)
belongs to \(W_u\), and agreement with its unique response color requires

\[
 \beta_u(x)=v.
\]

Let \(\iota_u(v)\in\mathbb F_2\) be the index satisfying
\(v=r_u^{\iota_u(v)}\).  The requirement is the unit equation

\[
 \boxed{
 z_{u,K_u(x)}
 =\pi_u(x)\oplus\iota_u(v).
 }
\tag{2.5}
\]

If \(K_u(x)\) is the anchor component, the right side must be zero.
Several singleton vertices in one component may impose the same unit or
contradictory units.

### Cross-projection clauses

Suppose \(xy\in E(H)\) and

\[
 L(x)=S-\{u\},\qquad L(y)=S-\{v\},\qquad u\ne v.
\tag{2.6}
\]

Let \(w\) be the third color:

\[
 \{w\}=L(x)\cap L(y).
\]

The vertices lie in different frozen-color projections: \(x\in W_u\) and
\(y\in W_v\).  Their edge is seen by neither projection simultaneously.
The only possible color collision is that both choose \(w\).

Define

\[
 q_x=\pi_u(x)\oplus\iota_u(w),\qquad
 q_y=\pi_v(y)\oplus\iota_v(w).
\tag{2.7}
\]

Then \(\beta_u(x)=w\) is the Boolean event
\(z_{u,K_u(x)}=q_x\), and similarly for \(y\).  Properness gives the
2-CNF clause

\[
 \boxed{
 \bigl(z_{u,K_u(x)}\ne q_x\bigr)
 \ \lor\
 \bigl(z_{v,K_v(y)}\ne q_y\bigr).
 }
\tag{2.8}
\]

Fixed anchor-component orientations are substituted as Boolean constants.

Let \(\Phi_S\) be the conjunction of all units (2.5) and clauses (2.8).

## 3. Exact projection-gluing theorem

### Theorem 2 (no-full-list gluing is exactly 2-SAT) — PROVED

Assume

\[
 1\le |L(x)|\le2
 \qquad\text{for every }x\notin S.
\tag{3.1}
\]

Then the following are equivalent.

1. The three frozen-color bipartitions can be oriented so that they agree
   with one family-compatible anchored coloring.
2. A family-compatible anchored coloring at \(S\) exists.
3. The 2-CNF formula \(\Phi_S\) is satisfiable.

Given a satisfying assignment, the coloring is

\[
 \kappa_S(x)=
 \begin{cases}
 x,&x\in S,\\
 v,&L(x)=\{v\},\\
 \beta_u(x),&L(x)=S-\{u\}.
 \end{cases}
\tag{3.2}
\]

#### Proof

Suppose first that \(\kappa_S\) is a family-compatible anchored coloring.
For fixed \(u\), every \(x\in W_u\) has

\[
 \kappa_S(x)\in L(x)\subseteq S-\{u\}.
\]

Thus the restriction of \(\kappa_S\) to \(B_u\) is a proper coloring with
the two colors in \(S-\{u\}\), anchored by their names.  On every connected
component it is one of the two bipartition orientations, and on the anchor
component its orientation is fixed.  It therefore determines values of all
the variables \(z_{u,K}\).

A singleton vertex receives its unique list color, so every equation (2.5)
holds.  A complement edge cannot have equal endpoint colors, so every
clause (2.8) holds.  Hence \(\Phi_S\) is satisfiable.

Conversely, let the component flips satisfy \(\Phi_S\), and define
\(\kappa_S\) by (3.2).  It belongs to every list by construction.  It
remains to prove properness in \(H\).

Anchor-anchor edges are safe because the three anchors have distinct
colors.  If \(x\notin S\) receives anchor color \(v\), then
\(v\in L(x)\), and the definition of a response list includes
\(vx\in E(G)\).  Thus \(vx\notin E(H)\), so anchor-outside edges are safe.

Now take \(xy\in E(H)\) with \(x,y\notin S\).

If \(O(x)\cap O(y)\ne\varnothing\), choose
\(u\in O(x)\cap O(y)\).  Both vertices lie in \(B_u\).  Equations (2.5)
make every singleton endpoint agree with \(\beta_u\), while a two-list
endpoint in \(W_u\) necessarily has list \(S-\{u\}\) and is assigned by
\(\beta_u\).  Since \(\beta_u\) is a proper bipartition, the endpoint
colors differ.

Suppose instead that \(O(x)\cap O(y)=\varnothing\).  If one omission set
has size two, its list is a singleton \(\{v\}\), while the other nonempty
omission set must be \(\{v\}\).  The second list is \(S-\{v\}\), so the
two lists are disjoint and no collision is possible.

The only remaining case is

\[
 |O(x)|=|O(y)|=1
\]

with distinct omitted colors.  Both endpoints have two-lists as in (2.6),
and their only common color is \(w\).  Clause (2.8) forbids the only
possible collision.  Thus every \(H\)-edge is proper.

This proves (3.2) is a family-compatible anchored coloring.  Its
restrictions are precisely the chosen orientations of all three
projections, proving all three equivalences. \(\square\)

### What is parity and what is genuinely 2-SAT

Inside one projection, every relation is an XOR parity relation inherited
from a bipartite component.  Across different projections, an edge produces
the disjunctive clause (2.8), not an XOR equation.  Therefore a parity
calculation alone cannot decide gluing; the exact global object is 2-SAT.

## 4. Minimal obstruction certificates

Theorem 2 gives two exact obstruction types.

### 4.1 Projection-internal parity obstruction

Two unit requirements in one component \(K\) are inconsistent precisely
when their demanded colors disagree with the parity of a path between their
vertices.  Anchors count as precolored unit markers.

Equivalently, if marked vertices \(x,y\in K\) demand colors
\(\ell(x),\ell(y)\in S-\{u\}\), then consistency requires

\[
 \operatorname{dist}_{B_u}(x,y)
 \equiv
 \iota_u(\ell(x))\oplus\iota_u(\ell(y))
 \pmod2.
\tag{4.1}
\]

A shortest path violating (4.1), together with its two endpoint
requirements, is a minimal parity certificate.  The accepted static
color-deletion theorem rules out this obstruction for static lists.  No
analogous family-list lift follows merely from the frozen-family theorem.

### 4.2 Cross-projection implication obstruction

After contracting the parity relations, make the usual implication graph of
\(\Phi_S\).  The formula is unsatisfiable if and only if some flip variable
\(z\) and its negation lie in the same strongly connected component.
Equivalently, there are directed implication paths

\[
 z\leadsto\neg z,\qquad
 \neg z\leadsto z.
\tag{4.2}
\]

An inclusion-minimal pair of such paths is the exact general obstruction,
often called a 2-SAT bicycle.  This description includes unit clauses and
clauses with a fixed anchor-component literal.

### 4.3 The mixed \(P_4\) is an inclusion-minimal forced-edge certificate

Let

\[
 x_0x_1x_2x_3
\]

be an induced path in \(H\), with

\[
 L(x_0)=\{a\},\quad
 L(x_1)=\{a,c\},\quad
 L(x_2)=\{b,c\},\quad
 L(x_3)=\{b\}.
\tag{4.3}
\]

The projection omitting \(b\) contains the edge \(x_0x_1\).  Its singleton
unit \(x_0=a\) forces

\[
 x_1=c.
\tag{4.4}
\]

The projection omitting \(a\) contains \(x_2x_3\).  Its singleton unit
\(x_3=b\) forces

\[
 x_2=c.
\tag{4.5}
\]

The middle edge belongs to no common omission projection.  It contributes
exactly

\[
 \neg(x_1=c)\lor\neg(x_2=c),
\tag{4.6}
\]

contradicting (4.4)--(4.5).  Deleting either unit or the middle clause makes
this certificate satisfiable.  Thus the residual mixed path is not an
informal failure to coordinate three colorings: it is an
inclusion-minimal two-unit/one-clause 2-SAT obstruction.

## 5. Full-list boundary

If

\[
 L(x)=S,
\]

then \(x\notin W_u\) for every \(u\in S\).  No frozen projection contains
\(x\), so no component flip assigns it a color and no formula \(\Phi_S\)
can encode its incident conflicts.

After solving the visible 2-SAT instance, extending over full-list vertices
is an ordinary three-color extension problem.  It is not generally 2-SAT.
Thus Theorem 2 is exact for the no-full-list slice and deliberately makes no
claim about a full-list/high-degree core.

## 6. Ridge transport of a successful gluing

The accepted response-covariance theorem does give a new gluing statement,
but it transports existence rather than creating it.

### Theorem 3 (ridge stability of family-compatible colorings) — PROVED

Let

\[
 S=C\cup\{a\},\qquad T=C\cup\{b\}
\tag{6.1}
\]

be independent triples in the same eternal family, and let
\(\rho=(a\ b)\).  A family-compatible anchored coloring exists at \(S\) if
and only if one exists at \(T\).

More precisely, from \(\kappa_S\) define

\[
 \kappa_T(y)=\rho\!\left(\kappa_S(\rho(y))\right).
\tag{6.2}
\]

Then \(\kappa_T\) is family-compatible at \(T\), and its three color fibers
are the same three subsets of \(V(G)\) as those of \(\kappa_S\), with only
the name \(a\) replaced by \(b\).

#### Proof

The ridge theorem gives

\[
 L^{\mathcal F}_S(b)=\{a\},\qquad
 L^{\mathcal F}_T(a)=\{b\}
\tag{6.3}
\]

and, for every \(x\notin S\),

\[
 \rho(L^{\mathcal F}_S(x))
 =L^{\mathcal F}_T(\rho(x)).
\tag{6.4}
\]

If \(y\in T\), (6.2) gives \(\kappa_T(y)=y\).  If \(y\notin T\), then
\(\rho(y)\notin S\), so (6.4) and compatibility of \(\kappa_S\) give

\[
 \kappa_T(y)
 =\rho(\kappa_S(\rho(y)))
 \in L^{\mathcal F}_T(y).
\tag{6.5}
\]

It remains to check properness without falsely treating \(\rho\) as a graph
automorphism.  The \(a\)-fiber of \(\kappa_S\) contains both \(a\) and
\(b\), by (6.3), and is therefore setwise fixed by \(\rho\).  Every
\(u\)-fiber with \(u\in C\) contains neither \(a\) nor \(b\), so it is
fixed pointwise by \(\rho\).  Consequently the fibers of \(\kappa_T\) are
exactly the old fibers as unlabelled vertex sets.  They remain independent
sets of \(H\), equivalently cliques of \(G\).

Applying the same involution in the reverse direction proves the
converse. \(\square\)

### Corollary 4 — PROVED

Under the no-full-list hypothesis, satisfiability of \(\Phi_S\) is invariant
along every ridge path of independent family states.

The formulas need not be literally isomorphic component by component:
\(\rho\) is not asserted to preserve graph edges or frozen-projection
parities.  The invariant is existence of a compatible coloring and its
underlying clique partition.

This is the strongest gluing consequence presently supplied by response
covariance.  It does not imply that the initial formula is satisfiable.

## 7. Full dynamics does not force gluing

### 7.1 `FDzro` already refutes automatic gluing

In the accepted specified 21-state family of

\[
 G=\texttt{FDzro},
\]

relative to \(S=\{0,1,2\}\), the lists are

\[
 L(3)=\{0\},\quad L(4)=\{0,2\},\quad
 L(5)=\{1,2\},\quad L(6)=\{1\}.
\tag{7.1}
\]

The two free projection components are

\[
 \{3,4\}\subseteq B_1,\qquad
 \{5,6\}\subseteq B_0.
\]

The singleton units force \(4=2\) and \(5=2\), while the complement edge
\(45\) contributes the clause forbidding both.  Hence

\[
 \Phi_S\text{ is unsatisfiable}.
\tag{7.2}
\]

All 84 state/attack obligations hold in the specified family, so
restoration, Hall, and the Hall-tight forced states coexist with (7.2).
The specified family has only one independent state, hence no independent
ridge pair; covariance is therefore vacuous in this example.  Its decisive
missing hypothesis is

\[
 \gamma(G)=2<3=\alpha(G)=\gamma^\infty(G)=\theta(G).
\]

### 7.2 A dual deficient-pair extension

The next countermodel includes the additional witness layers forced by the
absence of the middle dominating pair.

Use labels

\[
 a=0,\ b=1,\ c=2,\quad
 x_0=3,\ x_1=4,\ x_2=5,\ x_3=6,\quad
 w=7,\ y=8.
\]

Let \(G=\texttt{HDzruf]}\).  Equivalently, the edge set of \(H=\overline G\)
is

\[
\begin{split}
E(H)=\{&
01,02,12,\ 34,45,56,\ 13,06,\\
&27,47,57,\ 28,78\}.
\end{split}
\tag{7.3}
\]

The following 46 triples form the checked family \(\mathcal F\):

\[
\begin{split}
\{&
012,014,015,025,026,027,028,045,046,047,048,056,058,\\
&123,124,127,128,134,135,145,148,157,158,\\
&235,236,237,238,246,247,257,267,268,278,\\
&345,346,347,348,356,358,456,457,468,478,567,568,578
\}.
\end{split}
\tag{7.4}
\]

The exact checker verifies that all 46 states dominate and that every one
of the

\[
 46(9-3)=276
\]

unoccupied state/attack obligations has a legal one-edge, one-guard
successor in (7.4).

At \(S=012\), its exact lists are

\[
\begin{array}{c|c}
x_0&\{a\}\\
x_1&\{a,c\}\\
x_2&\{b,c\}\\
x_3&\{b\}\\
w&\{a,b\}\\
y&\{a,b\}.
\end{array}
\tag{7.5}
\]

The middle-pair witness and the dual witness are literal:

\[
 N_H(x_1)\cap N_H(x_2)=\{w\},\qquad
 N_H(c)\cap N_H(w)=\{y\}.
\tag{7.6}
\]

Moreover,

- \(w\) is adjacent in \(G\) to \(a,b,x_0,x_3\);
- \(y\) is adjacent in \(G\) to \(a,b,x_0,x_1,x_2,x_3\); and
- \(L(w)=L(y)=\{a,b\}\).

Thus this example realizes the proposed \(W/Y\) deficient-pair dynamics in
a full eternal family.

It still does not repair the 2-SAT obstruction.  The edges
\(wx_1,wx_2\in E(H)\) add only

\[
 \neg(w=a\land x_1=a),\qquad
 \neg(w=b\land x_2=b).
\tag{7.7}
\]

The original units force \(x_1=x_2=c\), so both new clauses are vacuous.
The edge \(wy\) lies inside the common projection omitting \(c\) and merely
forces \(w,y\) to opposite \(a/b\) colors.  It creates no relation between
the two middle projection flips.

The parameters are checked directly:

\[
 (\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3).
\tag{7.8}
\]

Indeed, \(012\) is independent, while

\[
 \{0,3,7\}\mid\{1,4,6,8\}\mid\{2,5\}
\tag{7.9}
\]

is a three-clique partition of \(G\), proving \(\alpha=\theta=3\).
The family proves \(\gamma^\infty\le3\), and
\(\alpha\le\gamma^\infty\) gives equality.  The pair \(\{0,4\}\)
dominates, while \(H\) has no isolated vertex, so \(\gamma=2\).

Therefore the following proposed strengthening is **REFUTED**:

> full family closure, ridge covariance, and the first two deficient-pair
> witness layers force the three frozen projections to glue.

Here the reference to ridge covariance means that the countermodel violates
none of its conclusions.  It is not a nonvacuous covariance stress test:
the three independent states in the displayed family contain no pair
sharing two vertices.  The countermodel does not refute the
equality-specific version because it again fails exactly at \(\gamma=3\).

## 8. Named stress tests

The following are deterministic exact checks of the displayed graph and
family records.  They are falsification diagnostics, not inputs to Theorems
2 or 3.

| graph and family | family lists at the displayed \(S\) | flips / units / cross clauses | outcome |
|---|---|---:|---|
| `FCZbg`, greatest family, \(S=046\) | \(1,2:\{4,6\};\,3:\{0\};\,5:\{6\}\) | \(2/2/0\) | two gluings |
| `FCXfO`, specified 16-state family, \(S=012\) | \(3:\{0\};\,4,6:\{1,2\};\,5:\{1\}\) | \(1/1/0\) | unique gluing |
| `FDzro`, specified 21-state family, \(S=012\) | (7.1) | \(2/2/1\) | unsatisfiable |
| `FDzro`, greatest 33-state family, \(S=012\) | \(3:\{0,2\};\,4,5:S;\,6:\{1,2\}\) | \(2/0/0\) on visible vertices | four visible orientations; eleven direct full list colorings |
| `FCpbO`, greatest family, \(S=056\) | \(1,4:\{6\};\,2:\{5\};\,3:\{0\}\) | \(0/0/0\) | unique gluing |

More explicitly:

- `FCZbg` gives
  \[
  1{:}4,\ 2{:}6,\ 3{:}0,\ 5{:}6
  \]
  or the coloring obtained by exchanging the colors of \(1,2\).
  The strict inclusion of its frozen projected family in the greatest
  projected family therefore does not prevent gluing, but neither does it
  prove gluing in general.
- `FCXfO` has the unique compatible coloring
  \[
  3{:}0,\ 4{:}2,\ 5{:}1,\ 6{:}2.
  \]
  Its accepted failure of pairwise response reciprocity does not create a
  parity obstruction.
- The specified `FDzro` family is the exact mixed-\(P_4\) obstruction.
  Passing to its greatest family enlarges two middle lists to full lists;
  the obstruction disappears from \(\Phi_S\) because those vertices become
  invisible, not because the three projections determine their colors.
- `FCpbO` has no free projection component at the displayed state and
  glues uniquely to
  \[
  1{:}6,\ 2{:}5,\ 3{:}0,\ 4{:}6.
  \]
  Its nontrivial complement flag homology is irrelevant to this local
  2-SAT instance.

Each specified family passed a literal full-closure replay: respectively
72, 64, 84, 132, and 48 state/attack obligations for the rows above.

## 9. Lightweight witness-extension search

The evidence script also tests whether the equality-forced witness of the
mixed \(P_4\) repairs the obstruction in the smallest possible labelled
extensions.

### Order eight — OBSERVED

Add one vertex \(w\) with

\[
 wx_1,wx_2\in E(H).
\]

After the fixed path, reference-state, and positive response edges, eleven
graph adjacencies remain free.  All \(2^{11}=2048\) masks were tested.

\[
\begin{array}{l|r}
\text{condition}&\text{masks}\\ \hline
\text{all seven required one-swap states dominate}&576\\
\text{the preceding condition and }\alpha=3&552\\
\gamma=\alpha=3&62\\
\text{both }\gamma=\alpha=3\text{ and all required states dominate}&0.
\end{array}
\tag{9.1}
\]

In particular, on exactly these eight vertices the required family states
force a dominating pair.

### Order nine — OBSERVED

Add a designated witness \(w\) and one arbitrary further vertex \(z\).
There are \(2^{19}=524\,288\) raw labelled edge masks.  Requiring \(w\)
and \(z\) to be dominated by every required state leaves 155,648 masks
before the full graph checks.

\[
\begin{array}{l|r}
\text{condition}&\text{masks}\\ \hline
\text{all required states dominate}&87\,552\\
\text{the preceding condition and }\alpha=3&68\,688\\
\text{the preceding condition and }\gamma=3&96\\
\text{an eternal family containing every positive swap and}\\
\quad\text{excluding every forbidden swap}&0.
\end{array}
\tag{9.2}
\]

For the last line, the checker removes the six forbidden one-swap states and
computes the greatest fixed point among all remaining dominating triples.
Thus it allows proper eternal subfamilies and does not search only the
unrestricted greatest family.

These are single-script labelled observations, not independently audited
coverage certificates.  They concern only orders eight and nine, do not
raise the finite counterexample frontier, and do not justify a larger
computation.

## 10. Exact stop gate

The gluing route has reached the following boundary.

### Proved

1. Every no-full-list gluing question is exactly the 2-SAT instance
   \(\Phi_S\).
2. Its minimal certificates are parity-inconsistent marked paths or
   contradictory implication cycles.
3. A successful gluing and its underlying clique partition transport across
   every independent-state ridge.

### Refuted

1. Bipartiteness of all three frozen projections does not force their
   component orientations to be compatible.
2. Full eternal closure, restoration, Hall, and Hall-tight states do not
   force compatibility.  The displayed unsatisfiable families have no
   independent ridge pair, so they make no stronger nonvacuous negative
   claim about covariance.
3. Adding the first two equality-motivated deficient-pair witness layers
   \(W,Y\) still does not force compatibility without using
   \(\gamma=3\).

### Still open

The following equality-specific statement is not proved or refuted:

> If
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\), \(\mathcal F\) is an
> eternal family of triples, \(S\) is independent, and no
> \(L^{\mathcal F}_S(x)\) is full, must \(\Phi_S\) be satisfiable?

For the greatest family, proving this throughout the no-full-list slice
would produce the desired clique partition there.  Merely restating that
\(\Phi_S\) should be satisfiable is not a new proof mechanism.

This lane should resume only if one obtains at least one of the following.

1. A genuinely \(\gamma=3\)-sensitive rule that forbids a contradictory
   implication cycle—for the mixed \(P_4\), a rule forcing at least one of
   \(x_1,x_2\) away from their shared color \(c\).  It must use information
   absent from both `FDzro` and `HDzruf]`.
2. A finite witness-proliferation theorem showing that the external
   domination witnesses forced by every newly dominating pair cannot
   continue under \(\alpha=3\) and full family closure.
3. A separate reduction for full-list vertices, which no frozen projection
   sees.

Absent one of these inputs, combining the three bipartitions is exactly the
already unresolved global response-list coloring problem, now written in
its minimal 2-SAT form.
