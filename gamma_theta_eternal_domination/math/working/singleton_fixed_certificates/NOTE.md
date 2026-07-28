# Anchor-fixed response certificates at \(k=3\)

## Status and exact scope

Date: 2026-07-28 (PDT)

All graph-game statements use the standard one-guard-moves model.  An
attack is made only at an unoccupied vertex, exactly one adjacent guard
moves, and the successor remains in the specified eternal family.

Let \(\mathcal F\) be an eternal family of triples, let

\[
 S=\{a,b,c\}\in\mathcal F
\]

be independent, put \(H=\overline G\), and write

\[
 L(x)=\{u\in S:S-u+x\in\mathcal F\}.
\tag{0.1}
\]

As usual, membership in (0.1) forces \(ux\in E(G)\).  The accepted
frozen-color theorem and the accepted parameter-two theorem imply that,
for every \(u\in S\),

\[
 B_u=H[(S-\{u\})\cup W_u],
 \qquad
 W_u=\{x\notin S:u\notin L(x)\},
\tag{0.2}
\]

is bipartite.

This note closes the immediate fixed-component branch left open in C-119.
Its results are:

1. **PROVED:** in any eternal family of pairs whose graph complement is
   bipartite, a retained pair cannot occupy the same side of one connected
   complement component.
2. **PROVED:** a singleton response demand lying in an anchor component of
   a frozen projection is automatically aligned with the demanded anchor.
   It can never simplify to a false constant.
3. **PROVED:** an exact-two response vertex never lies in the anchor
   component of its omitted-color projection.  Hence every cross-type
   collision clause has two free endpoint variables.  In particular, a
   fixed/fixed collision, fixed/free derived unit, fixed tautology, or
   fixed false constant cannot occur.
4. **EXACT SHARP CONTROLS:** `FCpbO` shows that singleton markers really can
   lie in anchor components; all eight such marker incidences are aligned.
   `LFzJbZYhdrDZdM` shows the surviving geometry with singleton lists,
   exact-two vertices in free components, and genuine cross-type clauses.

Consequently the no-full response 2-CNF under
\(\gamma=\alpha=\gamma^\infty=3\) has only:

- free-component units supplied by singleton markers; and
- genuine binary cross-type clauses on two free variables.

The remaining unsatisfiable terminals are therefore the one-/two-unit
branch and the unit-free residual bicycle branch.  This note does **not**
eliminate those branches, prove the complete \(k=3\) theorem, or resolve
the universal gamma--theta conjecture.

No literature-priority claim is made.

## 1. A two-guard component-transversal lemma

### Lemma 1.1 (retained pairs cross complement components)

Let \(J\) be a finite graph for which \(\overline J\) is bipartite, and
let \(\mathcal P\) be an eternal dominating family of pairs in \(J\).
Fix a bipartition of every connected component of \(\overline J\).

If

\[
 \{x,y\}\in\mathcal P
\tag{1.1}
\]

and \(x,y\) lie in the same connected component of \(\overline J\), then
they lie on opposite sides of that component.

#### Proof

Suppose otherwise.  Choose a retained same-side pair for which a shortest
complement path

\[
 x=v_0,v_1,\ldots,v_{2r}=y
\tag{1.2}
\]

has minimum positive even length.

If \(r=1\), the state \(\{x,y\}\) does not dominate \(v_1\) in \(J\):
both displayed incident edges are edges of \(\overline J\).  This
contradicts the requirement that every member of \(\mathcal P\) dominate.

Assume \(r\ge2\) and attack the unoccupied vertex \(v_2\).  Since
\(\overline J\) is bipartite, \(x,v_2,y\) lie on the same bipartition
side.  Distinct vertices on the same side are adjacent in \(J\), so
exactly the following one-guard successors can answer:

\[
 \{v_2,y\},
 \qquad
 \{x,v_2\}.
\tag{1.3}
\]

The first pair is absent from \(\mathcal P\), because the suffix

\[
 v_2,v_3,\ldots,v_{2r}=y
\]

is a shorter even complement path between same-side vertices, contrary to
the minimal choice in (1.2).  The second pair is not even dominating:
both \(xv_1\) and \(v_2v_1\) are complement edges.  Thus the attack at
\(v_2\) has no retained response, contradicting eternity. \(\square\)

The proof needs neither \(\gamma(J)=2\) nor connectedness of
\(\overline J\).  It uses bipartiteness, domination of every retained
state, and one-guard closure only.

## 2. Application to frozen response projections

For \(u\in S\), let

\[
 Q_u=G[(S-\{u\})\cup W_u]
\tag{2.1}
\]

and define

\[
 \mathcal P_u=
 \{A\subseteq V(Q_u):|A|=2,\ \{u\}\cup A\in\mathcal F\}.
\tag{2.2}
\]

The accepted frozen-color theorem says that \(\mathcal P_u\) is an
eternal dominating family of pairs in \(Q_u\).  Its independent anchor
pair \(S-\{u\}\) gives
\(\alpha(Q_u)=\gamma^\infty(Q_u)=2\).  The accepted parameter-two theorem
therefore gives

\[
 \theta(Q_u)=2,
 \qquad
 \overline{Q_u}=B_u\text{ is bipartite}.
\tag{2.3}
\]

Lemma 1.1 applies to every state of \(\mathcal P_u\).

### Theorem 2.1 (anchor-fixed singleton alignment)

Suppose

\[
 L(s)=\{d\},
\qquad
 u\in S-\{d\},
\tag{2.4}
\]

and let \(e\) be the third anchor, so

\[
 S=\{u,d,e\}.
\]

If \(s\) lies in the anchor component of \(B_u\), then \(s\) lies on the
same bipartition side as \(d\).  Thus the singleton demand for color \(d\)
is satisfied by the fixed anchor orientation.

#### Proof

The direct response state

\[
 S-d+s=\{u,e,s\}
\]

belongs to \(\mathcal F\).  Hence

\[
 \{e,s\}\in\mathcal P_u.
\tag{2.5}
\]

If \(s\) is in the anchor component, Lemma 1.1 puts \(e\) and \(s\) on
opposite sides.  The anchor edge \(de\in E(H)\) also puts \(d\) and \(e\)
on opposite sides.  Therefore \(d\) and \(s\) lie on the same side, which
is exactly the demanded fixed orientation. \(\square\)

This applies separately to the two frozen projections in which a
singleton marker appears.  The marker may be anchor-fixed in neither, one,
or both projections, but every fixed occurrence is automatically
consistent.

### Theorem 2.2 (exact-two components are free)

Suppose

\[
 L(x)=S-\{u\}=\{d,e\}.
\tag{2.6}
\]

Then \(x\) does not lie in the anchor component of \(B_u\).

#### Proof

Both direct response states

\[
 S-d+x=\{u,e,x\},
 \qquad
 S-e+x=\{u,d,x\}
\]

belong to \(\mathcal F\).  Therefore

\[
 \{e,x\},\{d,x\}\in\mathcal P_u.
\tag{2.7}
\]

If \(x\) lay in the anchor component, Lemma 1.1 applied to the first pair
would put \(x\) opposite \(e\), hence on the same side as \(d\).  Applied
to the second pair it would put \(x\) opposite \(d\), hence on the same
side as \(e\).  But the anchors \(d,e\) are on opposite sides.  This is
impossible. \(\square\)

### Corollary 2.3 (the C-119 immediate branch is empty)

Assume every outside response list is nonempty and proper.  In the exact
response 2-CNF obtained by contracting the three frozen projections:

1. every singleton demand in an anchor component substitutes to `true`;
2. every exact-two vertex belongs to a nonanchor component and therefore
   has a free flip variable; and
3. every complement edge between distinct exact-two types contributes a
   genuine binary clause on two free variables.

Consequently initial fixed-component substitution produces no false
constant, no fixed/free derived unit, and no fixed/fixed collision.

#### Proof

Item 1 is Theorem 2.1 and item 2 is Theorem 2.2.  A cross-type clause has
two exact-two endpoints, each in the projection associated with its omitted
color.  Item 2 makes both component orientations free.  The omitted colors
are distinct, so the two variables belong to distinct projections.  The
clause is therefore binary rather than a constant, unit, or tautology.
\(\square\)

Combining Corollary 2.3 with the accepted 2-CNF terminal theorem leaves
exactly:

- a contradiction reached from one or two free-component singleton pins;
  or
- a unit-free bicycle after consistent pin propagation.

This is a strict simplification of the obstruction ledger, not a proof
that either remaining branch is satisfiable.

## 3. Sharp equality controls

### 3.1 Singleton markers may all be anchor-fixed

The graph

```text
FCpbO
```

has order seven, size eight, and

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{3.1}
\]

Its greatest eternal triple-family has twelve states and satisfies all

\[
 12(7-3)=48
\]

unoccupied attack obligations.  At

\[
 S=\{0,5,6\},
\]

the response lists are

\[
 L(1)=\{6\},\quad
 L(2)=\{5\},\quad
 L(3)=\{0\},\quad
 L(4)=\{6\}.
\tag{3.2}
\]

Every one of the eight singleton-marker/projection incidences lies in an
anchor component.  All eight demands agree with the fixed orientation,
and there is one compatible response coloring.  Thus Theorem 2.1 cannot
be strengthened to say that singleton markers avoid anchor components.

### 3.2 Exact-two vertices and cross clauses remain free

The connected graph

```text
LFzJbZYhdrDZdM
```

has order thirteen, size forty-three, and again

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{3.3}
\]

Its greatest eternal triple-family has 142 states and satisfies all

\[
 142(13-3)=1420
\]

unoccupied attack obligations.  At \(S=\{0,1,2\}\), its lists are

\[
\begin{array}{c|cccccccccc}
x&3&4&5&6&7&8&9&10&11&12\\ \hline
L(x)&01&12&01&12&12&01&02&02&2&0 .
\end{array}
\tag{3.4}
\]

Every exact-two vertex belongs to a nonanchor component in its omitted
color projection.  The instance has genuine cross-type complement edges,
and each corresponding clause has two free endpoints.  The response
formula has two colorings.

This control shows that removing fixed substitutions does not remove the
remaining free-variable 2-SAT geometry.

## 4. Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  math/working/singleton_fixed_certificates/verify.py \
  --check math/working/singleton_fixed_certificates/controls.json
```

The verifier imports no campaign module.  It decodes the two graph6
records, recomputes all five parameters, reconstructs the greatest eternal
triple-family by simultaneous greatest-fixed-point deletion, checks every
one-guard obligation, reconstructs the response lists and frozen
components, checks all anchor-fixed singleton alignments, proves every
exact-two component is nonanchor in the controls, classifies every
cross-type clause endpoint, and counts compatible response colorings.

`probe_k2_transversal.py` was a discovery-only sanity probe.  The proof of
Lemma 1.1 is independent of that search.
