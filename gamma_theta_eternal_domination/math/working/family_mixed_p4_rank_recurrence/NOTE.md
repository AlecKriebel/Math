# Rank recurrence for the greatest-family mixed \(P_4\)

## Status and exact boundary

Date: 2026-07-28 (PDT)

This note studies the exact next step after accepted C-151, the endpoint
domination theorem in `family_mixed_p4_lift/NOTE.md`.

Assume

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\]

let \(\mathcal K\) be the literal greatest one-guard eternal family of
dominating triples, let \(S=\{a,b,c\}\) be independent, and suppose
\(x_0x_1x_2x_3\) is an induced path in \(\overline G\) with exact
\(\mathcal K\)-response lists

\[
L_S(x_0)=\{a\},\qquad
L_S(x_1)=\{a,c\},\qquad
L_S(x_2)=\{b,c\},\qquad
L_S(x_3)=\{b\}.
\tag{0.1}
\]

Put

\[
Q_i=S-c+x_i=\{a,b,x_i\},\qquad i\in\{0,3\}.
\tag{0.2}
\]

Accepted C-151 proves that both \(Q_i\) dominate.  Exactness of (0.1)
excludes them from \(\mathcal K\), so each has positive finite
synchronous deletion rank.

The complete desired recurrence has not yet been proved.  What is proved
below is the full single-hit branch, including exact rank loss and exact
transport of the entire mixed-\(P_4\) row.  The only remaining branch is
a deleting attack adjacent to at least two members of the independent
root.

No omitted family response is used as a graph nonedge.

## 1. Rank convention

Let \(\mathcal K_0\) be all dominating triples and define
\(\mathcal K_{j+1}\) synchronously from \(\mathcal K_j\) by retaining
exactly the states having a one-edge, one-guard successor in
\(\mathcal K_j\) at every unoccupied attack.  Set

\[
\rho(D)=
\begin{cases}
0,&D\notin\mathcal K_0,\\
h,&D\in\mathcal K_{h-1}-\mathcal K_h,\\
\infty,&D\in\bigcap_j\mathcal K_j.
\end{cases}
\tag{1.1}
\]

An attack \(r\notin D\) deletes a positive-rank state \(D\) of rank
\(h\) when every adjacency-eligible successor at \(r\) has rank below
\(h\).

## 2. Ridge transport of the complete list system

### Lemma 2.1 (exact ridge relabeling) — PROVED

Let \(g\in S\), let \(r\notin S\cup\{x_0,x_1,x_2,x_3\}\), and suppose

\[
S'=S-g+r
\tag{2.1}
\]

is independent.  Then \(S'\in\mathcal K\), and for every path target
\(x_j\), its response list at \(S'\) is obtained from \(L_S(x_j)\) by
the transposition \(g\leftrightarrow r\), fixing the other two root
positions.

#### Proof

Every independent triple belongs to every eternal triple-family under
\(\alpha(G)=\gamma^\infty(G)=3\), so \(S'\in\mathcal K\).

For either shared root vertex \(v\in S\cap S'\), accepted C-108 applies
to the independent triples \(S,S'\), which both avoid \(x_j\), and
makes the \(v\)-response status identical at the two roots.

For the exchanged positions, the two possible direct successors are
literally the same triple:

\[
S-g+x_j=S'-r+x_j.
\tag{2.2}
\]

Thus the \(g\)-role occurs at \(S\) exactly when the \(r\)-role occurs at
\(S'\).  This proves the complete relabeling. \(\square\)

This is a family statement.  In particular, a negative role means only
that the direct successor in (2.2) is absent from \(\mathcal K\); it is
not converted into a graph nonedge.

## 3. Exact single-hit recurrence

### Theorem 3.1 (single-hit endpoint-row descent) — PROVED

Fix \(i\in\{0,3\}\), write

\[
Q=Q_i=S-c+x_i,
\qquad
\rho(Q)=h\in\mathbb N_{>0},
\tag{3.1}
\]

and let \(r\) delete \(Q\) at round \(h\).  Suppose

\[
|N_G(r)\cap S|=1.
\tag{3.2}
\]

Then the unique member of \(N_G(r)\cap S\) is some
\(g\in\{a,b\}\), the triple

\[
S'=S-g+r
\tag{3.3}
\]

is an independent root carrying the exact relabeled mixed-\(P_4\)
lists, and

\[
Q'=S'-c+x_i=Q-g+r
\tag{3.4}
\]

is an adjacency-eligible successor with

\[
\boxed{\rho(Q')=h-1.}
\tag{3.5}
\]

Consequently exactly one of the following occurs:

1. \(h\ge2\) and \(Q'\) is a strictly lower positive-finite-rank copy of
   the same endpoint row; or
2. \(h=1\), \(Q'\) is non-dominating, and the relabeled exact family
   lists plus a vertex missed by \(Q'\) give the one-defect input of
   accepted C-148.

#### Proof

First audit the possible named collisions.  Every path vertex has at
least two graph neighbors in \(S\): \(x_1,x_2\) have their two positive
roles from (0.1), while \(x_0,x_3\) have their positive endpoint role
from (0.1) and the \(c\)-edge supplied by accepted C-070.  Thus (3.2)
implies that \(r\) is not any \(x_j\).

Also \(r\notin\{a,b\}\), since those vertices are occupied in \(Q\).  If
\(r=c\), then \(S\) is independent and
\(|N_G(c)\cap S|=0\), contrary to (3.2).  Hence

\[
r\notin S\cup\{x_0,x_1,x_2,x_3\},
\tag{3.6}
\]

as required for Lemma 2.1.

The unique root neighbor cannot be \(c\).  If it were, then \(a\) and
\(b\) would both miss \(r\).  Since \(Q=\{a,b,x_i\}\) dominates,
\(x_ir\in E(G)\).  The legal move \(x_i\to r\) would have successor

\[
Q-x_i+r=\{a,b,r\}=S-c+r.
\tag{3.7}
\]

Under the assumed unique root neighbor \(c\), (3.7) is an independent
triple.  It therefore belongs to \(\mathcal K\), contradicting that \(r\)
deletes \(Q\).

Thus the unique root neighbor is \(g\in\{a,b\}\).  The other two members
of \(S\) miss \(r\), so \(S'=S-g+r\) is independent.  The move
\(g\to r\) is adjacency-eligible from \(Q\), and its successor is
exactly (3.4).  Deletion gives

\[
\rho(Q')<h.
\tag{3.8}
\]

Lemma 2.1 transports the full exact list system to \(S'\).  In
particular the \(c\)-role at \(x_i\) remains absent, so \(Q'\notin
\mathcal K\); its rank is finite.

Accepted C-146's star-Lipschitz theorem applies to the two independent
sources \(S,S'\), fixed responder \(c\), and fixed target \(x_i\).
They differ by one vertex, hence

\[
|\rho(Q)-\rho(Q')|\le1
\tag{3.9}
\]

even when the finite rank \(\rho(Q')\) is zero.  Combining
(3.8)--(3.9) proves (3.5).

If \(h\ge2\), then \(\rho(Q')>0\), yielding item 1.  If \(h=1\), then
\(\rho(Q')=0\), so \(Q'\) misses a vertex.  Lemma 2.1 supplies the exact
relabeled family lists and accepted C-070 supplies the relabeled endpoint
edge.  These are exactly the one-defect hypotheses isolated from C-148,
giving item 2. \(\square\)

### Corollary 3.2 (exact obstruction boundary) — PROVED

Any deleting row that yields neither a lower-rank endpoint copy nor a
C-148 domination-defect core must satisfy

\[
\boxed{|N_G(r)\cap S|\ge2.}
\tag{3.10}
\]

#### Proof

The deleting target is unoccupied in \(Q_i\).  It cannot equal \(a\) or
\(b\), which are occupied.  It also cannot equal \(c\): accepted C-070
gives \(cx_i\in E(G)\), so the attack at \(c\) from \(Q_i\) has the legal
surviving response

\[
x_i\to c,\qquad Q_i-x_i+c=S\in\mathcal K.
\]

Thus every deleting target lies outside \(S\).  The retained root \(S\)
dominates that target, so \(N_G(r)\cap S\ne\varnothing\).  Theorem 3.1
resolves intersection size one.
\(\square\)

### Corollary 3.3 (finite descent reaches a multi-hit row) — PROVED

Start from either endpoint row in (0.2).  Whenever its chosen deleting
attack is single-hit, replace the independent root and endpoint row by
the objects \(S',Q'\) in Theorem 3.1.  Then after finitely many such
steps one reaches a transported endpoint row having a multi-hit deleting
attack.

#### Proof

Every single-hit step lowers the nonnegative integer rank by exactly one
and transports the full exact list pattern.  A step from rank one would
produce the rank-zero C-148 one-defect core, which accepted C-148
excludes.  Hence a realization cannot continue through single-hit rows
down to rank zero.  It must encounter a multi-hit deleting attack at an
earlier positive rank. \(\square\)

## 4. Multi-hit case table

### Observation 4.1 — PROVED AS AN EXHAUSTIVE BOOKKEEPING SPLIT

For a deleting attack \(r\) left after Corollary 3.2, its root
neighborhood is one of

\[
\{a,b\},\qquad
\{a,c\},\qquad
\{b,c\},\qquad
\{a,b,c\}.
\tag{4.1}
\]

For bookkeeping, split each row further according to whether
\(rx_i\in E(G)\).  This gives at most eight raw incidence cells per
endpoint before reflection and exact-list reductions.  It does not assert
that all eight cells are realizable or independent.  In particular, the
deleting target may be another named path vertex \(x_j\); inducedness and
the known positive roles then constrain both its root neighborhood and
its adjacency to \(x_i\).  Every such named collision must be checked in
its compatible cell rather than treated as a fresh free vertex.

This table is not a recurrence.  The difficult point is that a lower-rank
successor such as \(Q-a+r=\{b,x_i,r\}\) is an endpoint row at the
putative root \(\{b,c,r\}\) only when that root is independent.  In the
multi-hit cases it need not be.  Omission of a response role at \(r\)
cannot repair this gap, because omission is not a graph nonedge.

### Theorem 4.2 (exact named-target audit) — PROVED

At every transported exact-list root, a deleting target for an endpoint
row has the following fate:

1. neither middle path vertex \(x_1,x_2\) can delete either endpoint row;
2. the opposite path endpoint can delete \(Q_i\) only by producing the
   other endpoint row \(Q_{3-i}\) as a strictly lower-rank legal
   successor.

Consequently, any deleting target still outside the recurrence lies
outside

\[
S\cup\{x_0,x_1,x_2,x_3\}.
\tag{4.2}
\]

#### Proof

Work first at \(Q_0=\{a,b,x_0\}\).

The target \(x_2\) cannot delete \(Q_0\), because
\(x_0x_2\in E(G)\) and the legal successor

\[
Q_0-x_0+x_2=\{a,b,x_2\}
\]

belongs to \(\mathcal K\) by the positive \(c\)-role at \(x_2\).

For the target \(x_1\), start instead from the retained direct
\(a\)-response

\[
A_0=\{b,c,x_0\}\in\mathcal K.
\]

At the attack on \(x_1\), the guard \(x_0\) has no move edge.
The move \(c\to x_1\) gives

\[
\{b,x_0,x_1\}=Q_0-a+x_1.
\tag{4.3}
\]

If the optional edge \(bx_1\) is absent, (4.3) is the unique possible
response.  If \(bx_1\) is present, the other successor
\(\{c,x_0,x_1\}\) is excluded by accepted arbitrary-state restoration:
its missing root positions are \(a,b\), whereas

\[
L_S(x_0)\cup L_S(x_1)=\{a,c\}
\]

does not restore \(b\).  Closure therefore retains (4.3) in either graph
case.  Since \(ax_1\in E(G)\), it is a legal surviving successor from
\(Q_0\), so \(x_1\) cannot delete \(Q_0\).

Finally, \(x_0x_3\in E(G)\), and the \(x_0\to x_3\) successor of
\(Q_0\) is \(Q_3\).  If \(x_3\) deletes \(Q_0\), then

\[
\rho(Q_3)<\rho(Q_0),
\]

which is the required other-endpoint descent.

Reflection

\[
a\leftrightarrow b,\qquad
x_0\leftrightarrow x_3,\qquad
x_1\leftrightarrow x_2
\]

proves the three corresponding statements for \(Q_3\).  Corollary 3.2
already excludes every root vertex as a deleting target. \(\square\)

## 5. Fresh multi-hit normal form

For one endpoint row, write

\[
u=x_i,\qquad
\ell=
\begin{cases}a,&i=0,\\ b,&i=3,\end{cases}
\qquad
m=\{a,b\}-\{\ell\}.
\tag{5.1}
\]

Thus

\[
S=\{c,\ell,m\},\qquad
Q=\{u,\ell,m\},\qquad
L_S(u)=\{\ell\}.
\tag{5.2}
\]

For a deleting target \(r\) of rank-\(h\) state \(Q\), put

\[
C_g=Q-g+r
\qquad(g\in Q\cap N_G(r)).
\tag{5.3}
\]

Every \(C_g\) has rank below \(h\) and is outside \(\mathcal K\).

### Theorem 5.1 (eight-cell multi-hit reduction) — PROVED

Assume \(r\) is a fresh multi-hit target as in (4.2).  The following
table is exhaustive.

| \(N_G(r)\cap S\) | \(ur\) | movers from \(Q\) | proved conclusion |
|---|---:|---|---|
| \(\{c,\ell\}\) | no | \(\ell\) | impossible |
| \(\{c,m\}\) | no | \(m\) | \(\rho(C_m)=h-1\) and \(\ell\leftrightarrow u\) |
| \(\{c,\ell\}\) | yes | \(u,\ell\) | \(L_S(r)=\{\ell\}\) and \(\ell\leftrightarrow r\) |
| \(\{c,m\}\) | yes | \(u,m\) | \(L_S(r)=\{m\}\) and \(m\leftrightarrow r\) |
| \(\{\ell,m\}\) | no | \(\ell,m\) | \(\varnothing\ne L_S(r)\subseteq\{\ell,m\}\) |
| \(\{\ell,m\}\) | yes | \(u,\ell,m\) | \(\varnothing\ne L_S(r)\subseteq\{\ell,m\}\) |
| \(S\) | no | \(\ell,m\) | \(\varnothing\ne L_S(r)\subseteq S\) |
| \(S\) | yes | \(u,\ell,m\) | \(\varnothing\ne L_S(r)\subseteq\{\ell,m\}\) |

In either \(\{\ell,m\}\)-row, a singleton list
\(L_S(r)=\{g\}\) forces \(g\leftrightarrow r\).

#### Proof

Suppose first that \(N_G(r)\cap S=\{c,\ell\}\) and \(ur\notin E(G)\).
The unique mover from \(Q\) is \(\ell\), so \(C_\ell\notin\mathcal K\).
But the positive \(\ell\)-role at \(u\) retains

\[
D=S-\ell+u=\{c,m,u\}.
\]

At the attack \(r\) from \(D\), the guards \(m,u\) miss \(r\), while
the only possible \(c\)-move lands in

\[
D-c+r=\{r,m,u\}=C_\ell\notin\mathcal K.
\]

This contradicts closure of \(D\).

Next assume \(N_G(r)\cap S=\{c,m\}\) and \(ur\notin E(G)\).  The attack
from \(Q\) has the unique adjacency-eligible successor \(C_m\).
Membership of \(Q\) through horizon \(h-1\), together with deletion at
round \(h\), gives

\[
\rho(C_m)=h-1
\tag{5.4}
\]

(including rank zero when \(h=1\)).  The active edge
\(\ell\triangleright u\) comes from (5.2), while \(r\) is a common
nonneighbor of \(\ell,u\).  If \(u\not\triangleright\ell\), accepted
C-145 would retain the common-nonneighbor ridge

\[
\{\ell,u,r\}=C_m,
\]

contrary to the deleting row.  Hence \(\ell\leftrightarrow u\).

Now suppose \(N_G(r)\cap S=\{c,g\}\), where
\(g\in\{\ell,m\}\), and \(ur\in E(G)\).  The \(c\)-response from \(S\)
would be

\[
S-c+r=\{\ell,m,r\}=C_u,
\]

which the deleting row excludes.  The other outer root vertex misses
\(r\), so closure forces \(L_S(r)=\{g\}\).  Let \(q\) be the other outer
root vertex.  It is a common nonneighbor of \(g,r\).  If
\(r\not\triangleright g\), accepted C-145 would retain
\(\{g,r,q\}=C_u\), again a contradiction.  Therefore
\(g\leftrightarrow r\).

If \(N_G(r)\cap S=\{\ell,m\}\), graph adjacency already excludes \(c\)
from \(L_S(r)\), while closure makes the list a nonempty subset of
\(\{\ell,m\}\).  If it is the singleton \(\{g\}\), then \(c\) is a
common nonneighbor of \(g,r\).  Failure of the reverse activity would,
by C-145, retain \(\{g,r,c\}\), which is exactly the missing other
outer-root response at \(r\).  This contradicts singletonhood, so
\(g\leftrightarrow r\).

The two all-root rows have the displayed mover sets.  When \(ur\) is an
edge, the deleting row excludes \(C_u=S-c+r\), so the \(c\)-role is
absent and closure leaves a nonempty subset of \(\{\ell,m\}\).  When
\(ur\) is absent, no further role is excluded.  This proves the table.
\(\square\)

The unique descent (5.4) is real but is not yet the requested endpoint
recurrence: \(C_m=\{\ell,u,r\}\) is an endpoint row over
\(\{\ell,c,r\}\) only if that putative root is independent, whereas the
current case has \(cr\in E(G)\).  C-145 explains why the obstruction
then closes into the reciprocal edge \(\ell\leftrightarrow u\).

### Theorem 5.2 (completion-clique alternative in the outer collision) — PROVED

Suppose

\[
N_G(r)\cap S=\{\ell,m\}.
\tag{5.5}
\]

Put

\[
W_{cr}=\{w\notin\{c,r\}:cw,rw\notin E(G)\}.
\tag{5.6}
\]

Then exactly one of the following holds:

1. \(W_{cr}=\varnothing\), in which case \(\{c,r\}\) is a dominating
   pair; or
2. \(W_{cr}\) is a nonempty \(G\)-clique, every member hits at least one
   of \(\ell,m\), and
   \[
   w\ell\notin E(G)\Longrightarrow r\leftrightarrow\ell,
   \qquad
   wm\notin E(G)\Longrightarrow r\leftrightarrow m.
   \tag{5.7}
   \]

Under the equality hypotheses, item 1 is impossible and item 2 holds.
If additionally

\[
L_S(r)=\{\ell,m\},\qquad
r\not\triangleright\ell,\qquad
r\not\triangleright m,
\tag{5.8}
\]

then every \(w\in W_{cr}\) hits both outer anchors.

#### Proof

The first alternative is the definition of domination by the pair
\(\{c,r\}\).  Otherwise take \(w\in W_{cr}\).  Two distinct vertices of
\(W_{cr}\) must be adjacent, since together with the nonadjacent pair
\(\{c,r\}\) they would otherwise form an independent four-set,
contrary to \(\alpha(G)=3\).  Likewise \(w\) cannot miss both
\(\ell,m\), since then \(S\cup\{w\}\) would be independent of size four.

If \(w\ell\notin E(G)\), then

\[
\{c,\ell,w\},\qquad \{c,r,w\}
\]

are two maximum independent triples sharing the ridge \(\{c,w\}\).
The exchanged vertices \(\ell,r\) are adjacent by (5.5), so both
one-guard exchanges survive and \(r\leftrightarrow\ell\).  The statement
for \(m\) is symmetric.

Finally, \(\gamma(G)=3\) excludes item 1.  Under (5.8), neither implication
in (5.7) may fire, so every completion vertex hits both outer anchors.
\(\square\)

This theorem explains why the no-dominating-pair hypothesis does not by
itself close the collision: equality replaces the forbidden pair by a
nonempty completion clique, and the full-hit subcase remains.

## 6. Current conclusion

### PROVED

- Complete exact-list transport across every independent root ridge.
- Exact one-round rank descent for every single-hit deleting attack.
- Rank zero in that descent is exactly the transported C-148
  domination-defect alternative, and accepted C-148 excludes it.
- Iterating the well-founded single-hit recurrence necessarily reaches a
  transported endpoint row with a genuine multi-hit collision at its
  independent root.
- Every named path target is either impossible as a deleting attack or
  gives immediate descent to the other endpoint row.
- The fresh multi-hit branch has the exact eight-cell table in
  Theorem 5.1; one cell is impossible and three cells force reciprocal
  active edges.
- The outer collision has the dominating-pair/completion-clique
  alternative in Theorem 5.2.

### CANDIDATE

The desired **full eight-cell recurrence remains open**.  It would show
that every surviving cell of Theorem 5.1 constructs another independent
root supporting a lower-rank endpoint row, triggers the C-148 defect
core, or forces a dominating pair.  The unique lower-rank state in
(5.4) is not itself an endpoint row, and the completion clique in
Theorem 5.2 need not be empty.  No proof of the required final mapping is
currently available.

### OBSERVED

The bounded synthesis in `family_mixed_p4_lift/`, together with the
replay recorded in this directory, reports no equality-compatible
exact-family-list model at any order \(7\) through \(22\).  Those runs
have no independently audited certificate and are not used in the proof
above.
