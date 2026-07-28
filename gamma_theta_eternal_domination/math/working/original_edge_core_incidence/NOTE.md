# Original-edge incidence: physical caps and the surviving tight gate

## Status and exact boundary

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained state dominates.

This note resumes the no-full-list \(k=3\) proof lane after C-094 and
C-095.  It has one proved incidence theorem and two exact equality
controls.

1. **PROVED:** an original response-clause edge whose two literal events
   cannot be joined after physicalizing both endpoints has a common
   complement-neighbor cap.  Every cap misses at most one anchor.  Full
   one-guard closure determines the forced response-list inclusions and
   exclusions in (2.5); only the middle nonneutral signature determines
   the whole list.
2. **PROVED:** the original clause and the two cap edges form a
   **virtual rainbow triangle**: their local response constraints force
   the three colors to be pairwise distinct.  Unless the cap has exactly
   the third two-list, this gadget gives a resolution-derived unit and a
   length-two implication arm.
3. **REFUTED:** one same-sign physical representative need not retain two
   specified original clause edges.  The equality graph
   `MFzJbZYhlrDZdMhd_` is an exact countercontrol.
4. **REFUTED:** physicalizing both endpoints of one original clause need
   not produce a complement edge between any representative pair.  The
   equality graph `NFzJbZZhlrDZdMhd|h_` is an exact countercontrol.

Both controls have

\[
  \gamma=i=\alpha=\gamma^\infty=\theta=3
\]

and use their greatest eternal triple-families.  Their response formulas
are satisfiable (each has two compatible colorings), so they do not meet
the inclusion-minimal-unsatisfiable premise and are not counterexamples to
the gamma--theta conjecture.

The surviving universal target is now narrower: a genuinely unit-free
minimal bicycle can evade local shortening only by chaining exact
third-color virtual-rainbow gates.  Eliminating the resulting global
holonomy remains open.

No literature-priority claim is made.

## 1. Setup

Let \(\mathcal F\) be an eternal family of triples, let

\[
  S=\{a,b,c\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).  For \(t\notin S\), write

\[
  L(t)=\{i\in S:S-i+t\in\mathcal F\}.
\tag{1.1}
\]

Membership \(i\in L(t)\) forces \(it\in E(G)\): the retained successor
must dominate the omitted anchor \(i\), while the other two anchors miss
it.

Assume

\[
  \gamma(G)=3,\qquad
  1\le |L(t)|\le2\quad(t\notin S).
\tag{1.2}
\]

The independent state and the eternal triple-family give
\(\alpha(G)=3\).

We use C-094 in its exact form.  Every port \(q\) with
\(L(q)=\{a,b\}\) has a same-sign physical representative \(x\) such
that

\[
  L(x)=\{a,b\},\qquad cx\in E(H),
\tag{1.3}
\]

and the \(b\)-color event at \(x\) is literally the same Boolean event as
the \(b\)-color event at \(q\).  The cyclic versions hold for the other
two-list types.  C-095 warns that an original complement edge at \(q\)
need not be incident with \(x\).

## 2. The edge-or-virtual-rainbow-cap theorem

### Theorem 2.1 (physical cap for a failed joint incidence) — PROVED

Suppose an original cross-clause edge has ports

\[
  qv\in E(H),\qquad
  L(q)=\{a,b\},\qquad
  L(v)=\{b,c\}.
\tag{2.1}
\]

Let \(x,y\) be same-sign physical representatives supplied by C-094:

\[
\begin{aligned}
  &L(x)=\{a,b\},\quad cx\in E(H),\\
  &L(y)=\{b,c\},\quad ay\in E(H),
\end{aligned}
\tag{2.2}
\]

with the \(b\)-events of \(q,x\), and of \(v,y\), respectively equal.
Then exactly one of the following incidence alternatives holds.

1. \(xy\in E(H)\).  The original clause has a literal complement edge
   between physical representatives.
2. \(xy\in E(G)\).  There is a vertex
   \[
     z\in N_H(x)\cap N_H(y)
   \tag{2.3}
   \]
   with
   \[
     |\sigma(z)|\le1,\qquad
     \sigma(z):=N_H(z)\cap S.
   \tag{2.4}
   \]
   Moreover:
   \[
   \begin{array}{c|c}
   \sigma(z)&\text{forced family-list information}\\ \hline
   \{a\}&c\in L(z),\ a\notin L(z),\\
   \{b\}&L(z)=\{a,c\},\\
   \{c\}&a\in L(z),\ c\notin L(z).
   \end{array}
   \tag{2.5}
   \]
   If \(\sigma(z)=\varnothing\), no stronger list conclusion follows
   from this local argument; by (1.2), its list is nevertheless one of
   the six nonempty proper subsets of \(S\).

#### Proof

Only the second alternative needs proof.  Since \(xy\in E(G)\) and
\(\gamma(G)=3\), the pair \(\{x,y\}\) does not dominate.  Hence it has a
common complement neighbor \(z\), proving (2.3).

The four direct states

\[
\begin{array}{ll}
 D_a=S-a+x=\{b,c,x\},&
 D_b=S-b+x=\{a,c,x\},\\
 E_b=S-b+y=\{a,c,y\},&
 E_c=S-c+y=\{a,b,y\}
\end{array}
\tag{2.6}
\]

belong to \(\mathcal F\).  They all dominate \(z\), while \(x\) and
\(y\) miss \(z\).  Consequently \(z\) cannot miss both anchors in any
of the pairs

\[
 \{b,c\},\qquad \{a,c\},\qquad \{a,b\}.
\tag{2.7}
\]

Thus \(z\) misses at most one anchor, proving (2.4).  Notice also that
no anchor can itself be \(z\): \(x\) sees \(a,b\) in \(G\), while \(y\)
sees \(b,c\).

Suppose first that \(\sigma(z)=\{a\}\).  Attack \(z\) from
\(D_b=\{a,c,x\}\).  The guards at \(a,x\) miss \(z\), so closure forces

\[
  \{a,x,z\}\in\mathcal F.
\tag{2.8}
\]

Attack \(b\) from (2.8).  The guard at \(a\) cannot move because \(S\)
is independent.  Moving \(z\) gives

\[
  \{a,b,x\}=S-c+x\notin\mathcal F
\]

because \(c\notin L(x)\).  Closure therefore forces \(x\to b\) and the
successor

\[
  \{a,b,z\}=S-c+z\in\mathcal F.
\]

Hence \(c\in L(z)\).  The graph nonedge \(az\in E(H)\) gives
\(a\notin L(z)\).

The case \(\sigma(z)=\{c\}\) is cyclically symmetric, using \(E_b,E_c\);
it gives \(a\in L(z)\) and \(c\notin L(z)\).

Finally suppose \(\sigma(z)=\{b\}\).  Attack \(z\) from
\(D_a=\{b,c,x\}\).  Only \(c\) can move, forcing
\(\{b,x,z\}\in\mathcal F\).  An attack at \(a\) there forces
\[
  \{a,b,z\}=S-c+z\in\mathcal F,
\]
exactly as above, so \(c\in L(z)\).

Similarly, attack \(z\) from \(E_c=\{a,b,y\}\).  Only \(a\) can move,
forcing \(\{b,y,z\}\in\mathcal F\).  An attack at \(c\) then forces
\[
  \{b,c,z\}=S-a+z\in\mathcal F,
\]
so \(a\in L(z)\).  Since \(bz\in E(H)\), one has \(b\notin L(z)\).
Therefore \(L(z)=\{a,c\}\), completing (2.5).  Every attack was made at
an unoccupied vertex and every successor changed exactly one guard along
a graph edge. \(\square\)

### Theorem 2.2 (virtual rainbow triangle) — PROVED

In alternative 2 of Theorem 2.1, the original clause \(qv\), the
same-sign identities \(q\equiv x\), \(v\equiv y\), and the literal cap
edges

\[
  xz,yz\in E(H)
\tag{2.9}
\]

force the local colors of \(x,y,z\) to be pairwise distinct in every
assignment satisfying these local response constraints.

Equivalently, writing \(X,Y,Z\) for their colors, the complete table is

\[
\begin{array}{c|c}
L(z)&(X,Y,Z)\\ \hline
\{a\}&(b,c,a)\\
\{b\}&(a,c,b)\\
\{c\}&(a,b,c)\\
\{a,b\}&(b,c,a)\text{ or }(a,c,b)\\
\{b,c\}&(a,b,c)\text{ or }(a,c,b)\\
\{a,c\}&(b,c,a)\text{ or }(a,b,c).
\end{array}
\tag{2.10}
\]

#### Proof

The two original port lists overlap only in \(b\).  Hence the original
cross clause says exactly that \(q\) and \(v\) cannot both receive \(b\).
The C-094 same-sign identities replace this by

\[
  X\ne Y.
\tag{2.11}
\]

The physical complement edges in (2.9) give

\[
  X\ne Z,\qquad Y\ne Z.
\tag{2.12}
\]

Thus \(X,Y,Z\) are three distinct members of the three-element set \(S\).
Intersecting the six permutations with
\[
  X\in\{a,b\},\quad Y\in\{b,c\},\quad Z\in L(z)
\]
gives exactly (2.10). \(\square\)

The proof uses the **original** edge \(qv\) for (2.11) and the new literal
edges \(xz,yz\) only for (2.12).  It never claims that \(xy\in E(H)\).

## 3. Consequences for the three terminal obstruction types

The table separates one tight case from five shortening cases.

### 3.1 Two-list caps

Let \(X_b\) and \(Y_b\) denote the events \(X=b\) and \(Y=b\).
The original clause is

\[
  \neg X_b\lor\neg Y_b.
\tag{3.1}
\]

If \(L(z)=\{b,c\}\), then the physical edge \(yz\) puts \(y,z\) on
opposite sides of one \(a\)-omitting component.  Hence
\(Z_b=\neg Y_b\).  The cap edge \(xz\) contributes

\[
  \neg X_b\lor\neg Z_b
  =
  \neg X_b\lor Y_b.
\tag{3.2}
\]

Resolving (3.1) and (3.2) yields

\[
  \neg X_b,
\tag{3.3}
\]

that is, the forced endpoint color \(X=a\).

If \(L(z)=\{a,b\}\), the symmetric calculation gives the unit
\(Y=c\).

The only two-list cap that produces no endpoint unit is therefore

\[
  \boxed{L(z)=\{a,c\}.}
\tag{3.4}
\]

In this **tight third-color gate**, the three local clauses allow exactly
the two assignments

\[
  (X,Y,Z)=(b,c,a),\qquad (a,b,c).
\tag{3.5}
\]

If this cap is neutral relative to \(S\), C-094 physicalizes its
\(\{a,c\}\) event and the incidence analysis repeats.  If its anchor
signature is nonempty, Theorem 2.1 shows that the tight gate occurs
precisely in the shared-color signature \(\sigma(z)=\{b\}\); the two
other pure signatures give endpoint units.

### 3.2 Singleton caps

The first three rows of (2.10) give two endpoint units directly:

\[
\begin{array}{c|cc}
L(z)&X&Y\\ \hline
\{a\}&b&c\\
\{b\}&a&c\\
\{c\}&a&b.
\end{array}
\tag{3.6}
\]

These units are supported by literal singleton constraints and the
original/cap incidences.  No omission has been interpreted as a graph
nonedge.

### 3.3 Effect on chains, lollipops, and bicycles

Consider one selected original clause on a terminal obstruction path.

- In a **two-unit chain**, a non-tight cap supplies an endpoint unit at
  that clause.  In the implication digraph it cuts the chain into a
  shorter marked prefix or suffix.
- In a **one-unit lollipop**, the same derived unit cuts the
  literal-to-complement path into a shorter unit-bearing obstruction.
- In a **unit-free bicycle**, the two clauses in (3.1)--(3.2) give a
  length-two implication arm from \(X_b\) to its complement (and the
  symmetric case does the same at \(Y_b\)).  Thus a failed physical
  incidence is locally reducible to a marked arm unless its cap is the
  tight third-color gate (3.4).

This is a logical/local reduction, not yet a one-guard attack eliminating
arbitrary long obstructions.  In particular, a resolution-derived unit
must retain its displayed original-edge support when translated into an
attack tree.

The exact remaining unit-free geometry is consequently:

> original cross edges, same-sign physicalization paths, and exact
> third-color virtual-rainbow gates chained into a global bicycle.

That is a genuine global-holonomy problem.  The next proof must rule out
such a closed chain or show that it forces a dominating pair/canonical
dead-state attack.  C-095 alone could not isolate this gate.

## 4. Two exact equality countercontrols

The controls below were found by bounded local augmentation of the C-095
coordinate construction and then rebuilt from scratch by `verify.py`.

### 4.1 No representative retains two specified original edges

The graph

```text
MFzJbZYhlrDZdMhd_
```

has order \(14\), size \(51\), and

\[
  (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{4.1}
\]

Its greatest eternal triple-family has \(177\) states and satisfies all

\[
  177(14-3)=1947
\]

unoccupied attack obligations.  At \(S=012\),

\[
\begin{aligned}
 L(3)&=\{0,1\},&
 L(4)&=\{1,2\},&
 L(9)&=\{0,2\},&
 L(8)&=\{0,1\}.
\end{aligned}
\tag{4.2}
\]

Vertex \(8\) is the unique same-sign physical representative of port
\(3\).  Both

\[
  3\,4,\ 3\,9\in E(H)
\tag{4.3}
\]

are original cross-clause edges, but

\[
  8\,4,\ 8\,9\in E(G).
\tag{4.4}
\]

Thus the unique representative retains neither specified edge.  The two
failed incidences have tight caps \(13\) and \(7\), respectively.

### 4.2 Joint physicalization of one clause can fail

The graph

```text
NFzJbZZhlrDZdMhd|h_
```

has order \(15\), size \(60\), and again

\[
  (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{4.5}
\]

Its greatest eternal triple-family has \(216\) states and satisfies all

\[
  216(15-3)=2592
\]

unoccupied attack obligations.  The original clause edge is

\[
  3\,4\in E(H),
\qquad
  L(3)=\{0,1\},\quad L(4)=\{1,2\}.
\tag{4.6}
\]

The same-sign physical representative sets are singletons:

\[
  R_3=\{8\},\qquad R_4=\{7\},
\tag{4.7}
\]

but

\[
  8\,7\in E(G).
\tag{4.8}
\]

Thus no pair of same-sign physical representatives realizes the original
clause edge.  The pair \(8,7\) has the unique common complement neighbor
\(13\), with

\[
  L(13)=\{0,2\},\qquad
  N_H(13)\cap S=\{1\}.
\tag{4.9}
\]

This is exactly the tight third-color gate (3.4), showing that the
surviving branch is real even under full equality and greatest-family
closure.

Both controls have exactly two family-compatible response-list colorings.
They therefore refute the two incidence strengthenings but not any
minimal-unsatisfiable theorem and not the gamma--theta conjecture.

## 5. Reproduction

From the campaign directory, run

```text
python3 -I -B -W error \
  math/working/original_edge_core_incidence/verify.py \
  --check math/working/original_edge_core_incidence/result.json
```

The standalone ordinary-set verifier:

- constructs both graphs without importing campaign search code;
- checks graph6 records, edge counts, connectedness, and exact
  \(\gamma,\alpha,\theta\);
- computes the greatest eternal triple-family by fixed-point deletion;
- replays all \(1947+2592=4539\) one-guard obligations;
- reconstructs every response list at \(S\);
- rebuilds every frozen projection and same-sign representative set;
- checks the two specified-edge and joint-endpoint incidence failures;
- checks the exact tight caps and their anchor signatures; and
- exhaustively enumerates the two compatible response-list colorings of
  each control.

The controls are boundary artifacts, not conjecture counterexamples.
