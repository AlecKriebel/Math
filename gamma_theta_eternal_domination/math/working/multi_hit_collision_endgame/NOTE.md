# Multi-hit collision endgame at \(k=3\)

## Status and exact boundary

Date: 2026-07-28 (PDT)

Assume throughout that

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{0.1}
\]

and that \(\mathcal K\) is the literal greatest eternal family of
dominating triples in the one-guard-moves model.  Suppose

\[
 u\triangleright x,\qquad x\not\triangleright u,
\tag{0.2}
\]

let

\[
 T=\{x,p,q\}
\tag{0.3}
\]

be a maximum independent triple, and put

\[
 B=T-x+u=\{u,p,q\}.
\tag{0.4}
\]

By C-143, \(B\) dominates.  By C-108 and (0.2), \(B\notin\mathcal K\),
so \(B\) has a positive finite deletion rank \(h\).  Let \(r\) be an
attack deleting \(B\) at round \(h\).  When \(B\) is a minimum-rank
reverse endpoint, C-146 says that \(r\) hits at least two vertices of
\(T\).

This note gives the exact six-case split of that multi-hit branch and
proves three further reductions.

1. At every rank, the case
   \[
   N(r)\cap T=\{x,p\},\qquad ur\notin E(G)
   \]
   has a unique lower-rank successor, forces \(q\leftrightarrow u\),
   and has an exact response square.
2. At rank one, that same case is impossible.
3. The remaining rank-one cases with \(ur\notin E(G)\) have a rigid
   paired-private-witness ridge, while the
   \(N(r)\cap T=\{x,p\},ur\in E(G)\) case has a forced four-facet
   independent ridge path.

For the \(N(r)\cap T=\{p,q\}\) collision realized by `GEjbug`, equality
forces a nonempty completion clique for the pair \(\{x,r\}\).  Unless a
reverse activity already appears, every vertex in that clique must hit
both \(p\) and \(q\).  `GEjbug` lies sharply outside this conclusion:
\(\{x,r\}\) is a dominating pair, so the completion clique is empty and
\(\gamma=i=2\).

The shared-pivot/all-three-hit branches and the full-hit completion-clique
branch remain open.  Nothing below proves greatest-family reciprocity, the
complete \(k=3\) case, or the gamma--theta conjecture.

## 1. Conventions

For a retained independent triple \(I\) and an unoccupied target \(v\),
write

\[
 L_I(v)=
 \{g\in I:I-g+v\in\mathcal K\}.
\tag{1.1}
\]

The graph-edge condition is implicit: membership of the successor in
\(\mathcal K\) forces the move \(g\to v\) to be along an edge.

For \(g\in B\cap N(r)\), put

\[
 C_g=B-g+r.
\tag{1.2}
\]

Because \(r\) deletes \(B\), every \(C_g\) has rank below \(h\), with
rank zero allowed.

The reverse state \(B\) is the forbidden \(x\)-successor at the attack
on \(u\) from \(T\).  Hence

\[
 \varnothing\ne L_T(u)\subseteq\{p,q\}.
\tag{1.3}
\]

## 2. The exact six-case table

Subject to the multi-hit hypothesis (2.0), up to interchanging \(p\) and
\(q\) there are exactly three possible sets \(N(r)\cap T\).  The edge
\(ur\) may be present or absent, giving exactly six raw cases.

### Theorem 2.1 (six-case multi-hit split) — PROVED

Assume that the chosen deleting attack is multi-hit:

\[
 |N(r)\cap T|\ge 2.
\tag{2.0}
\]

(In the applications below this follows when \(B\) has rank one; it
also follows when \(B\) has globally minimum rank among reverse
endpoints, by C-146.)

The following table is exhaustive.

| case | \(N(r)\cap T\) | \(ur\) | legal movers from \(B\) | forced information at \(T\) |
|---|---|---:|---|---|
| XQ0 | \(\{x,p\}\) | no | \(p\) | \(L_T(u)=\{q\}\), \(q\leftrightarrow u\) |
| XQ1 | \(\{x,p\}\) | yes | \(u,p\) | \(L_T(r)=\{p\}\), \(p\leftrightarrow r\) |
| QQ0 | \(\{p,q\}\) | no | \(p,q\) | \(\varnothing\ne L_T(r)\subseteq\{p,q\}\) |
| QQ1 | \(\{p,q\}\) | yes | \(u,p,q\) | \(\varnothing\ne L_T(r)\subseteq\{p,q\}\) |
| AQ0 | \(\{x,p,q\}\) | no | \(p,q\) | \(\varnothing\ne L_T(r)\subseteq\{x,p,q\}\) |
| AQ1 | \(\{x,p,q\}\) | yes | \(u,p,q\) | \(\varnothing\ne L_T(r)\subseteq\{p,q\}\) |

In XQ0, the unique successor satisfies

\[
 \rho(C_p)=h-1.
\tag{2.1}
\]

In XQ0, if \(L_T(r)\) is a singleton, its member is reciprocal with
\(r\).  The same is true in QQ0 and QQ1.  Thus the only unresolved
response-list alternatives in those rows are the lists of size two.

#### Proof

C-146 gives \(N(r)\cap\{p,q\}\ne\varnothing\).  Relabel so that
\(pr\in E(G)\).  A multi-hit has at least one further neighbor in
\(\{x,p,q\}\), leaving exactly

\[
 \{x,p\},\qquad \{p,q\},\qquad \{x,p,q\}.
\]

Intersecting \(N(r)\) with \(B=\{u,p,q\}\) gives the six mover sets in
the table.

If both \(ur\) and \(xr\) are edges, the \(x\)-successor from \(T\) is

\[
 T-x+r=\{r,p,q\}=C_u.
\]

It is excluded from \(\mathcal K\) by the deleting attack on \(B\).
This removes \(x\) from \(L_T(r)\) in XQ1 and AQ1.  The remaining list
statements follow from eternal closure of \(T\).

Now consider XQ0.  The attack \(r\) from \(B\) has the unique
adjacency-eligible successor

\[
 C_p=\{u,r,q\}.
\tag{2.2}
\]

For \(h=1\), this successor has rank zero.  For \(h\ge2\), membership
\(B\in\mathcal K_{h-1}\) forces the unique successor at every attack to
belong to \(\mathcal K_{h-2}\), while deletion at round \(h\) gives rank
strictly below \(h\).  Hence (2.1) holds in every case.

If \(p\in L_T(u)\), then

\[
 A=T-p+u=\{x,u,q\}\in\mathcal K.
\]

Attack \(r\) from \(A\).  The guards \(u,q\) miss \(r\), while the only
possible \(x\)-move lands in \(C_p\notin\mathcal K\).  This contradicts
closure.  Therefore (1.3) forces

\[
 L_T(u)=\{q\},
\]

so \(q\triangleright u\).  The vertex \(r\) is a common nonneighbor of
\(q,u\).  If \(u\not\triangleright q\), accepted C-145 applied to the
one-sided edge \(q\triangleright u\) would retain the common-nonneighbor
ridge

\[
 \{q,u,r\}=C_p,
\]

again a contradiction.  Thus \(q\leftrightarrow u\).

For the singleton assertions, first stay in XQ0.  The vertex \(q\) is a
common nonneighbor of \(x,r\) and also of \(p,r\).  If
\(L_T(r)=\{x\}\) and \(r\not\triangleright x\), C-145 retains
\(\{x,r,q\}=T-p+r\), adding \(p\) to the list.  If
\(L_T(r)=\{p\}\) and \(r\not\triangleright p\), it retains
\(\{p,r,q\}=T-x+r\), adding \(x\).  Either conclusion contradicts
singletonhood.

In QQ0 and QQ1, the vertex \(x\) is a common nonneighbor of \(p,r\) and
of \(q,r\).  If the list is the singleton \(\{p\}\), failure of
\(r\triangleright p\) would retain
\(\{p,r,x\}=T-q+r\), adding \(q\).  The case \(\{q\}\) is symmetric.

Finally, in XQ1 the list at \(r\) is already the singleton \(\{p\}\).
Here \(q\) is a common nonneighbor of \(p,r\), but the ridge
\[
 \{p,r,q\}=C_u
\]
is excluded by the deleting attack.  C-145 therefore forces
\(r\triangleright p\), proving \(p\leftrightarrow r\). \(\square\)

### Corollary 2.2 (exact XQ0 response square) — PROVED

In XQ0, let \(g\in L_T(r)\), so \(g\in\{x,p\}\), and put
\[
 D=T-g+r.
\]
Then the attack at \(u\) from \(D\) is forced to move \(q\), and the
subsequent attack at \(q\) is forced to move \(u\), returning to \(D\).

#### Proof

The guard \(r\) misses \(u\).  At the attack on \(u\), the move by the
other member of \(\{x,p\}\) lands in \(C_p\) whenever it is
adjacency-eligible, and \(C_p\notin\mathcal K\).  The already proved
identity \(L_T(u)=\{q\}\) supplies \(qu\in E(G)\).  Thus closure forces
\(q\to u\).  In the resulting state, \(xq,pq,rq\) are all nonedges, so
the only response to \(q\) is \(u\to q\), returning to \(D\). \(\square\)

## 3. Rank-one private witnesses

Assume for this section that \(h=1\).  Then every legal successor
\(C_g\) of the deleting attack is non-dominating.

### Lemma 3.1 (private-witness rule) — PROVED

For every \(g\in B\cap N(r)\), there is a vertex \(y_g\) such that

\[
 gy_g\in E(G),
\qquad
 y_g r\notin E(G),
\qquad
 y_g b\notin E(G)\quad(b\in B-\{g\}).
\tag{3.1}
\]

The witnesses for different guards are distinct.

#### Proof

Choose a vertex \(y_g\) missed by the non-dominating state
\(C_g=B-g+r\).  It misses \(r\) and every member of \(B-\{g\}\).
Moreover \(y_g\ne g\), because \(gr\in E(G)\) whereas
\(y_gr\notin E(G)\).
Since \(B\) dominates, its only possible dominator in \(B\) is the
removed guard \(g\), proving (3.1).  A witness cannot equal any occupied
vertex of \(C_g\).  For \(g\ne g'\), the vertex \(y_g\) is adjacent to
\(g\), while \(y_{g'}\) is nonadjacent to \(g\), so they are distinct.
\(\square\)

### Theorem 3.2 (rank-one XQ0 is impossible) — PROVED

There is no rank-one collision satisfying

\[
 N(r)\cap T=\{x,p\},
\qquad
 ur\notin E(G).
\tag{3.2}
\]

#### Proof

The only mover from \(B\) is \(p\).  Let \(y=y_p\) be supplied by
Lemma 3.1.  Then

\[
 \{u,r,y\}
\]

is an independent triple: \(ur,uy,ry\) are all nonedges.  It therefore
belongs to \(\mathcal K\).  The active edge \(u\triangleright x\) and
C-108 retain

\[
 \{x,r,y\}.
\tag{3.3}
\]

But the unoccupied vertex \(q\) is nonadjacent to all three guards in
(3.3): \(xq\notin E(G)\) by independence of \(T\),
\(rq\notin E(G)\) by (3.2), and \(yq\notin E(G)\) by (3.1).
The retained state has no legal response to the attack at \(q\), a
contradiction. \(\square\)

The proof uses eternal activity essentially.  The static equality
\(\gamma=i=\alpha=3\) alone does not exclude this pattern; the exact
control `GCOedo` in Section 6 realizes it.

### Theorem 3.3 (paired-witness ridge when \(ur\) is absent) — PROVED

Assume \(ur\notin E(G)\), \(h=1\), and \(r\) hits both \(p\) and \(q\).
This covers QQ0 and AQ0.  For \(g\in\{p,q\}\), let \(t\) be the other
member of \(\{p,q\}\).  Then the following path is forced:

\[
\begin{array}{rcl}
 U_g&=&\{u,r,y_g\}\quad\text{(independent)},\\
 D_g&=&\{x,r,y_g\}\in\mathcal K,\\
 E_g&=&\{x,t,y_g\}\in\mathcal K,\\
 T&=&\{x,t,g\},
\end{array}
\tag{3.4}
\]

with moves

\[
 U_g\xrightarrow{\,u\to x\,}D_g
 \xrightarrow{\,r\to t\,}E_g
 \xrightarrow{\,y_g\to g\,}T.
\tag{3.5}
\]

Moreover,

\[
 y_py_q\in E(G),
\tag{3.6}
\]

and \(U_p,U_q\) are adjacent independent facets sharing the ridge
\(\{u,r\}\).  Their response lists satisfy

\[
\begin{aligned}
 \varnothing\ne L_{U_p}(p)=L_{U_q}(p)&\subseteq\{u,r\},\\
 \varnothing\ne L_{U_p}(q)=L_{U_q}(q)&\subseteq\{u,r\}.
\end{aligned}
\tag{3.7}
\]

In particular, neither private witness may answer the attack at the
endpoint it privately dominates.

#### Proof

Lemma 3.1 and \(ur\notin E(G)\) make \(U_g\) independent.  Activity of
\(u\to x\) retains \(D_g\).  At the attack on \(t\), the guards \(x\)
and \(y_g\) miss \(t\), while \(rt\in E(G)\), so \(r\to t\) is unique
and retains \(E_g\).  At the attack on \(g\), the guards \(x,t\) miss
\(g\), while \(y_gg\in E(G)\), so \(y_g\to g\) is unique and returns
to \(T\).

If \(y_p,y_q\) were nonadjacent, then
\(\{u,r,y_p,y_q\}\) would be an independent set of size four, contrary
to \(\alpha(G)=3\).  This proves (3.6), and hence \(U_p,U_q\) are
independent ridge-neighbors.

Apply accepted C-064 ridge response-covariance to \(U_p,U_q\), using
the transposition \(y_p\leftrightarrow y_q\).  At target \(p\),
the guard \(y_q\) is not even adjacent to \(p\), by (3.1) for \(g=q\).
Therefore \(y_q\notin L_{U_q}(p)\), and covariance excludes
\(y_p\) from \(L_{U_p}(p)\).  The two shared positions \(u,r\) are
fixed by the transposition, giving the first identity in (3.7).
The target \(q\) is symmetric.  Nonemptiness is eternal closure.
\(\square\)

### Theorem 3.4 (rank-one XQ1 witness ladder) — PROVED

Assume

\[
 N(r)\cap T=\{x,p\},\qquad ur\in E(G),\qquad h=1.
\tag{3.8}
\]

Let \(y=y_p\) and \(z=y_u\) be the two private witnesses.  Then

\[
 \{y,r,q\},\quad
 \{z,r,q\},\quad
 \{z,p,q\},\quad
 \{x,p,q\}
\tag{3.9}
\]

are four consecutive independent facets in \(\mathcal K\), joined by

\[
 y\to z,\qquad r\to p,\qquad z\to x.
\tag{3.10}
\]

Before that ridge path, the retained state \(T-p+r=\{x,r,q\}\) answers
the attack at \(y\) uniquely by \(x\to y\).

#### Proof

Theorem 2.1 gives \(L_T(r)=\{p\}\), so

\[
 D=T-p+r=\{x,r,q\}\in\mathcal K.
\]

The witness \(y\) misses \(u,r,q\).  Since \(D\) dominates \(y\), it
follows that \(xy\in E(G)\).  Thus the attack at \(y\) from \(D\) has
the unique response

\[
 x\to y,\qquad J=\{y,r,q\}\in\mathcal K.
\]

The set \(J\) is independent because \(rq,ry,qy\) are nonedges.

The witness \(z\) misses \(r,p,q\).  Domination by \(B\) forces
\(uz\in E(G)\), and domination by \(T\) forces \(xz\in E(G)\).
From \(J\), the guards \(r,q\) miss the attack at \(z\).  Closure
therefore forces \(yz\in E(G)\) and retains
\(\{z,r,q\}\), which is independent.  Its attack at \(p\) uniquely
moves \(r\), retaining the independent triple \(\{z,p,q\}\).  Finally,
the attack at \(x\) uniquely moves \(z\), returning to \(T\).
\(\square\)

## 4. The QQ completion-clique obstruction

The QQ rows have

\[
 xr\notin E(G),\qquad pr,qr\in E(G).
\tag{4.1}
\]

Put

\[
 C_{xr}=\{c\in V(G)-\{x,r\}:cx,cr\notin E(G)\}.
\tag{4.2}
\]

### Theorem 4.1 (completion-clique alternative) — PROVED

The set \(C_{xr}\) is a nonempty \(G\)-clique.  Every member is adjacent
to at least one of \(p,q\).  More precisely:

\[
\begin{array}{ll}
 cp\notin E(G)&\Longrightarrow r\leftrightarrow p,\\
 cq\notin E(G)&\Longrightarrow r\leftrightarrow q.
\end{array}
\tag{4.3}
\]

Consequently, if

\[
 L_T(r)=\{p,q\},
\qquad
 r\not\triangleright p,
\qquad
 r\not\triangleright q,
\tag{4.4}
\]

then every \(c\in C_{xr}\) is adjacent to both \(p\) and \(q\).

#### Proof

The pair \(\{x,r\}\) is independent.  Since \(i=\alpha=3\), it extends
to an independent triple, proving \(C_{xr}\ne\varnothing\).  If two
members \(c,c'\) of \(C_{xr}\) were nonadjacent, then
\(\{x,r,c,c'\}\) would be independent, contradicting \(\alpha=3\).
Thus \(C_{xr}\) is a clique.

No \(c\in C_{xr}\) can miss both \(p\) and \(q\), because then
\(\{x,p,q,c\}\) would be independent of size four.

Suppose \(cp\notin E(G)\).  The triples

\[
 \{x,p,c\},
\qquad
 \{x,r,c\}
\]

are independent, hence retained.  They share the ridge \(\{x,c\}\),
and exchanging \(p,r\) in either direction moves along the edge
\(pr\).  Therefore \(p\leftrightarrow r\).  The second implication in
(4.3) is symmetric.  The final assertion follows immediately. \(\square\)

This identifies the exact equality repair missing from `GEjbug`.
It does not eliminate the full-hit alternative in (4.4).

## 5. What remains

The reductions above leave these genuine branches.

1. XQ0 at rank at least two: its unique successor has exact rank
   \(h-1\), and \(q\leftrightarrow u\), but that successor is not itself
   a reverse endpoint.
2. XQ1 at rank one: the four-facet witness ladder is forced, but it does
   not yet yield a lower-rank reverse endpoint.
3. QQ: a two-response collision can persist only with a reciprocal
   \(r\)-edge or with a nonempty full-hit completion clique.
4. AQ: every member of \(T\) hits \(r\), so the repair-square pivot for
   a new one-sided edge must be external; no named endpoint supplies it.
5. At ranks above one, lower-rank successors need not have missed
   vertices, so the private-witness arguments do not apply directly.

There is no equality-compatible dynamic countermodel in this note.
The static control `GCOedo` and the \(\gamma=2\) dynamic control
`GEjbug` show why both eternal activity and \(\gamma=3\) are essential.

## 6. Exact controls

`verify_controls.py` independently decodes and evaluates two fixed
graph6 records.

- `GEjbug`, with
  \[
  (u,x,p,q,r)=(0,4,3,5,7),
  \]
  has \((\gamma,i,\alpha,\gamma^\infty)=(2,2,3,3)\).
  The reverse state `035` has rank one.  Its deleting attack at \(7\)
  is QQ1, all three legal successors are non-dominating, and both
  \(p,q\) answer from \(T=345\), while neither reverse direction is
  active.  The pair \(\{x,r\}=\{4,7\}\) dominates, so
  \(C_{xr}=\varnothing\).
- `GCOedo`, with
  \[
  (u,x,p,q,r)=(6,0,2,1,7),
  \]
  has \((\gamma,i,\alpha,\gamma^\infty)=(3,3,3,4)\).
  The dominating state `126` has rank one and its deleting attack at
  \(7\) is the XQ0 pattern with unique non-dominating successor `167`,
  missed by vertex \(5\).  The triple `567` is independent, but the
  would-be active successor `057` misses \(q=1\).  Thus the exact
  contradiction in Theorem 3.2 occurs at the missing eternal-activity
  hypothesis.

These are fixed-graph controls, not evidence for the unresolved
all-order branches.
