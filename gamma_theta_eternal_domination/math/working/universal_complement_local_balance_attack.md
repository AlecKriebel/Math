# Universal complement/local-balance attack

## Status and exact claim boundary

This is a proof-lane working note for the standard **one-guard-moves**
eternal domination model.  Attacks occur only at unoccupied vertices,
exactly one adjacent guard moves to the attacked vertex, and every successor
configuration dominates.

The labels used below have their campaign meanings:

- **PROVED** means that a complete proof is given here, sometimes relative to
  an accepted campaign theorem that is named explicitly.
- **REFUTED** means that the proposed proof mechanism has an explicit
  counterexample.
- **OBSERVED** means that a light exact diagnostic recorded the stated finite
  behavior; it is not promoted to a campaign claim.
- **CONJECTURED** means that no proof is claimed.

The new proved material in this note has not received independent hostile
review.  No novelty or priority claim is made.  In particular, this note does
not prove the gamma--theta conjecture, disprove it, or raise the certified
minimum counterexample order.

## 1. Exact minimum-counterexample dictionary

Let \(G\) be a hypothetical minimum-order counterexample, write

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=k<\theta(G),
 \qquad H=\overline G,
\tag{1.1}
\]

and let \(N_H(X)=\bigcap_{x\in X}N_H(x)\) denote a common open
neighborhood.

### Lemma 1 (arbitrary small sets have a common \(H\)-neighbor) — PROVED

For every \(X\subseteq V(H)\) with \(|X|\leq k-1\),

\[
 N_H(X)\ne\varnothing.
\tag{1.2}
\]

Consequently every maximal clique of \(H\) has size \(k\).

#### Proof

First let \(|X|=k-1\).  Since \(\gamma(G)=k\), the set \(X\) does not
dominate \(G\).  Hence some vertex \(z\notin X\) is nonadjacent in \(G\) to
every member of \(X\).  Equivalently, \(z\in N_H(X)\).

If \(|X|<k-1\), extend \(X\) arbitrarily to a \((k-1)\)-set \(X'\).
Every common \(H\)-neighbor of \(X'\) is also a common neighbor of \(X\).
This proves (1.2).

Now let \(A\) be a clique with \(|A|<k\).  Equation (1.2), applied directly
if \(|A|=k-1\) and after extending \(A\) to a \((k-1)\)-set otherwise,
gives a vertex adjacent to every member of \(A\).  Thus \(A\) is not a
maximal clique.  Since

\[
 \omega(H)=\alpha(G)=k,
\]

all maximal cliques have size \(k\). \(\square\)

The last conclusion therefore follows already from
\(\gamma(G)=\alpha(G)=k\); it does not require a separate appeal to
well-coveredness.  The equality collapse remains the reason that a
counterexample has \(\alpha=k\).

### Accepted local-link hierarchy — PROVED INPUT C-051

The accepted independent-antineighborhood projection gives more when the
anchor \(A\) is a clique.  For every nonempty \(t\)-clique \(A\) of \(H\),
\(t<k\),

\[
 \chi\bigl(H[N_H(A)]\bigr)
 =
 \omega\bigl(H[N_H(A)]\bigr)
 =
 k-t.
\tag{1.3}
\]

Thus the clique complex of \(H\) is pure of dimension \(k-1\), and every
nonempty face link has the exact smaller coloring number prescribed by its
dimension.  In the language of balanced complexes, every proper face link
is balanced.

Equation (1.3) does **not** extend from clique anchors to arbitrary sets.
For example, in \(H=\overline{C_7}\) with the cyclic labeling
\(0,\ldots,6\), the nonedge \(\{0,1\}\) has common neighborhood
\(\{3,4,5\}\), and vertices \(3,5\) are adjacent in \(H\).  Its common
neighborhood is not independent, even though \(k-|\{0,1\}|=1\).

### Minimum-counterexample nonsimpliciality in the complement — PROVED

The accepted simplicial-neighborhood reduction C-048 says that \(G\) has no
simplicial vertex.  For \(v\in V(H)\), put

\[
 M_H(v)=V(H)-N_H(v).
\tag{1.4}
\]

This set includes \(v\), and it is exactly \(N_G[v]\).  Therefore

\[
 H[M_H(v)]\text{ contains an edge for every }v.
\tag{1.5}
\]

Indeed, if \(H[M_H(v)]\) were edgeless, \(G[N_G[v]]\) would be a clique and
\(v\) would be simplicial in \(G\).

The three restrictions (1.2), (1.3), and (1.5) are genuinely different:
(1.2) applies to nonfaces, (1.3) controls chromatic numbers of face links,
and (1.5) rules out a local reduction in \(G\).

## 2. Attempt one: force global balance by facet transport

Let a **facet** mean a \(k\)-clique of \(H\).  Two facets are
ridge-adjacent if they share \(k-1\) vertices.

### Lemma 2 (ridge exchanges are forced game moves) — PROVED

Let

\[
 T=R\cup\{x\},\qquad T'=R\cup\{y\}
\tag{2.1}
\]

be distinct ridge-adjacent facets, with \(|R|=k-1\).  In every eternal
\(k\)-family of \(G\), an attack at \(y\) from state \(T\) has the unique
response \(x\to y\), and the successor is \(T'\).

#### Proof

Both facets are independent \(k\)-sets of \(G\), so the accepted
maximum-independent-state forcing lemma places both in every eternal
\(k\)-family.  The vertices \(x,y\) are nonadjacent in \(H\), since otherwise
\(R\cup\{x,y\}\) would be a \((k+1)\)-clique.  Hence \(xy\in E(G)\).
Every member of \(R\) is adjacent to \(y\) in \(H\), and therefore
nonadjacent to \(y\) in \(G\).  The guard at \(x\) is the unique guard that
can answer the unoccupied attack at \(y\), and its move gives \(T'\).
\(\square\)

This suggests a color-transport mechanism.  Color one facet with
\([k]\).  Across a ridge exchange, retain the \(k-1\) common colors and give
the entering vertex the color of the departing vertex.  Path independence
would give a consistent coloring inside one ridge-connected facet component
provided repeated vertex occurrences also agree.  A global coloring would
additionally require compatibility between different ridge components and
their lower-dimensional overlaps.  The proposed route was to derive all of
those compatibility conditions from the minimum-counterexample and eternal
transition hypotheses.

### The \(\overline{C_7}\) obstruction — REFUTED MECHANISM

The forced facet moves alone do not make the transport path-independent.
Let \(G=C_7\), so \(H=\overline{C_7}\), and consider the ridge-adjacent
facet loop

\[
\begin{split}
 024&\longrightarrow025\longrightarrow035\longrightarrow135\\
    &\longrightarrow136\longrightarrow146\longrightarrow246
      \longrightarrow024.
\end{split}
\tag{2.2}
\]

The exchanged vertices are, in order,

\[
 4\to5,\quad 2\to3,\quad 0\to1,\quad 5\to6,\quad
 3\to4,\quad 1\to2,\quad 6\to0.
\tag{2.3}
\]

Every arrow is a legal one-edge, one-guard move in \(C_7\), and every state
is a maximum independent triple and hence a dominating state.  If the three
guards initially at \(0,2,4\) are labeled \(A,B,C\), respectively, the loop
returns to the same occupied set with labels

\[
 0:C,\qquad 2:A,\qquad 4:B.
\tag{2.4}
\]

Thus the canonical ridge transport has a nontrivial three-cycle around
(2.2).  The graph \(H=\overline{C_7}\) also satisfies every static and local
condition established above for \(k=3\):

- \(\omega(H)=3<4=\chi(H)\);
- every pair has a common neighbor;
- every maximal clique is a triangle; and
- every vertex link is a copy of \(P_4\), hence bipartite with clique and
  chromatic number two.

What fails is full eternal closure:
\(\gamma^\infty(C_7)=4\).  The failure occurs after leaving the facet-only
part of the state space.  Therefore a proof using only facets, ridge links,
and their forced exchanges cannot distinguish this exact obstruction.

There is a second, more basic warning.  Guard labels are not invariants of
the one-guard game even when equality holds.  On \(G=C_4\), start with
labeled guards \(A\) at \(0\) and \(B\) at \(2\), and make the legal moves

\[
 0\to1,\qquad 2\to3,\qquad 3\to0,\qquad 1\to2.
\tag{2.5}
\]

The occupied states are

\[
 02,\ 12,\ 13,\ 01,\ 02,
\]

all dominating.  In fact, all six two-subsets of \(V(C_4)\) dominate, and
they form an eternal two-family, so the whole loop lies in one eternal
family.  At the end, \(B\) is at \(0\) and \(A\) is at \(2\).
Nevertheless

\[
 \gamma(C_4)=\gamma^\infty(C_4)=\theta(C_4)=2.
\]

Any proposed contradiction based on preserving physical guard identities is
therefore false in the exact model.

### Proposition 3 (equality does not force simple connectivity) — PROVED

It is also unsafe to require the clique complex of \(H\) to be simply
connected.  One explicit example has

\[
 G=\texttt{FCpbO},\qquad H=\overline G=\texttt{FzM[g}.
\tag{2.6}
\]

The edge set of \(G\) is

\[
\{03,04,14,15,16,25,26,46\}.
\tag{2.7}
\]

The three cliques

\[
 \{0,3\},\qquad \{1,4,6\},\qquad \{2,5\}
\tag{2.8}
\]

partition \(V(G)\), so their product strategy gives
\(\gamma^\infty(G)\leq3\) and \(\theta(G)\leq3\).  The independent triple
\(\{0,1,2\}\) gives \(\alpha(G)\geq3\).  The triangles of \(H\) are exactly

\[
 012,\ 056,\ 123,\ 234,\ 345,\ 356,
\tag{2.9}
\]

so \(H\) has no \(K_4\) and \(\alpha(G)=3\).  The general parameter chain
now forces

\[
 \alpha(G)=\gamma^\infty(G)=\theta(G)=3.
\]

Finally, every pair has a common neighbor in \(H\); one witness for the
pairs in lexicographic order is

\[
\begin{split}
&01{:}2,\ 02{:}1,\ 03{:}1,\ 04{:}2,\ 05{:}6,\ 06{:}5,\\
&12{:}0,\ 13{:}2,\ 14{:}2,\ 15{:}0,\ 16{:}0,
\end{split}
\]
\[
\begin{split}
&23{:}1,\ 24{:}3,\ 25{:}0,\ 26{:}0,\ 34{:}2,\\
&35{:}4,\ 36{:}5,\ 45{:}3,\ 46{:}3,\ 56{:}0.
\end{split}
\tag{2.10}
\]

Thus no pair dominates \(G\), so \(\gamma(G)=3\), and
\(i(G)=3\) follows from
\(\gamma\leq i\leq\alpha\).

For the topology, \(H\) has seven vertices, thirteen edges, and the six
triangles in (2.9).  Each triangle boundary has an edge occurring in no
other listed triangle, so the six boundary vectors are independent over
\(\mathbb F_2\).  Since \(H\) is connected,

\[
\dim H_1(\mathrm{Cl}(H);\mathbb F_2)
 =13-7+1-6=1.
\tag{2.11}
\]

The flag complex is therefore not simply connected, while

\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=\theta(G)=3.
\]

The light probe finds three additional connected order-seven examples, but
they are **OBSERVED** diagnostics and are not needed for Proposition 3.

### Attempt-one gate

**BLOCKED AFTER ONE SERIOUS ITERATION.**  C-051 makes all proper face links
balanced, but global imbalance can survive as a genuine gluing obstruction.
Forced ridge moves transport labels, yet the game state forgets labels.
Neither simple connectivity nor label invariance follows from eternal
domination.  A viable continuation would have to use non-facet
configurations and a gauge-invariant obstruction; merely renaming the
failure “holonomy” does not advance the conjecture.

The sibling stress test
`math/working/universal_holonomy_critical_graph_referee.md` independently
reaches the same boundary from line graphs: exact local link colorability is
not a global coloring theorem, and singleton clique overlaps do not define a
canonical permutation transport.

## 3. Attempt two: private blocks and the shared-response list core

This attempt starts at the precise gap in the historically flawed
private-neighborhood proof rather than repeating it.

Fix an eternal \(k\)-family \(\mathcal F\), and fix a maximum independent
set \(S\).  The forcing lemma gives \(S\in\mathcal F\).  For \(u\in S\),
write

\[
 B_u=P_S(u)=\{x\in V(G):N_G[x]\cap S=\{u\}\}.
\tag{3.1}
\]

These are closed private blocks, so \(u\in B_u\).  Let

\[
 X=V(G)-\bigcup_{u\in S}B_u.
\tag{3.2}
\]

Every vertex of \(X\) lies outside \(S\) and is adjacent in \(G\) to at
least two members of \(S\); these are exactly the shared vertices relative
to \(S\).

### Lemma 4 (the private blocks are cliques) — PROVED

For every \(u\in S\), \(G[B_u]\) is a clique, and the blocks \(B_u\) are
pairwise disjoint.

#### Proof

Disjointness follows directly from unique domination.  If distinct
\(x,y\in B_u\) were nonadjacent in \(G\), then both would be nonadjacent to
every member of \(S-\{u\}\).  Hence

\[
 (S-\{u\})\cup\{x,y\}
\]

would be an independent set of size \(k+1\), contradicting
\(\alpha(G)=k\). \(\square\)

For every vertex \(x\in V(G)-S\), define its **response list**

\[
 L_{\mathcal F}(x)=
 \{u\in S:ux\in E(G)\text{ and }S-\{u\}+\{x\}\in\mathcal F\}.
\tag{3.3}
\]

Every list is nonempty by closure of \(\mathcal F\) at \(S\).  The swap
criterion gives

\[
 u\in L_{\mathcal F}(x)
 \quad\Longrightarrow\quad
 B_u\subseteq N_G[x].
\tag{3.4}
\]

Thus a family response color \(u\) in particular certifies that the outside
vertex can be adjoined to the private clique \(B_u\) while preserving
domination.  The converse domination condition alone need not put the
successor in the chosen family \(\mathcal F\).

If \(x\in B_u-\{u\}\), then \(u\) is its only neighbor in \(S\), while
\(S-\{u\}+\{x\}\) is an independent \(k\)-set and hence belongs to every
eternal \(k\)-family.  Therefore

\[
 L_{\mathcal F}(x)=\{u\}.
\]

The private vertices already have their forced block colors; only the lists
on \(X\) remain to be selected.

### Lemma 5 (family-response Hall condition) — PROVED

For every independent set \(Z\subseteq V(G)-S\),

\[
 \left|\bigcup_{z\in Z}L_{\mathcal F}(z)\right|\geq |Z|.
\tag{3.5}
\]

Equivalently, the response-list bipartite graph has a matching that assigns
distinct guards of \(S\) to all vertices of \(Z\).

#### Proof

Starting at \(S\), attack the vertices of \(Z\) one at a time.  A guard
already moved to an earlier vertex of \(Z\) cannot answer a later attack,
because \(Z\) is independent.  Thus the responses move \(|Z|\) distinct
guards of \(S\), and closure puts a state

\[
 D=(S-U)\cup Z\in\mathcal F,\qquad |U|=|Z|.
\tag{3.6}
\]

Fix \(u\in U\).  Starting afresh from \(D\), attack the vertices of
\(U-\{u\}\) one at a time.  Currently occupied vertices of \(S\) cannot
answer these attacks, because \(S\) is independent.  Each response therefore
moves one of the outside guards in \(Z\) back to the attacked vertex of
\(S\).  After \(|U|-1\) such attacks, the family contains a state

\[
 S-\{u\}+\{z\}
\]

for some \(z\in Z\).  Attack the still-unoccupied vertex \(u\).  No guard in
\(S-\{u\}\) is adjacent to \(u\), so the sole outside guard at \(z\) must
move to \(u\).  In particular \(uz\in E(G)\), and the preceding state lies
in \(\mathcal F\).  Hence \(u\in L_{\mathcal F}(z)\).

The vertex \(u\) was arbitrary, so

\[
 U\subseteq\bigcup_{z\in Z}L_{\mathcal F}(z),
\]

which proves (3.5).  Every subset of \(Z\) is independent, so the same
inequality for all subsets is exactly Hall's condition. \(\square\)

This strengthens the pointwise nonemptiness of the lists.  In complement
language, every clique \(Z\) of \(H-S\), and in particular every clique of
\(H[X]\), has enough response colors for a system of distinct
representatives.  It does not imply a proper list coloring on all of
\(H[X]\).  The restoration idea was found independently in the sibling
transition/private-neighborhood lane; no novelty claim is made here.

### Theorem 6 (response-list coloring is sufficient) — PROVED

If the complement-induced graph \(H[X]\) has a proper coloring

\[
 f:X\longrightarrow S
\tag{3.7}
\]

such that \(f(x)\in L_{\mathcal F}(x)\) for every \(x\in X\), then

\[
 \theta(G)=k.
\tag{3.8}
\]

#### Proof

For each \(u\in S\), set

\[
 C_u=B_u\cup f^{-1}(u).
\]

Lemma 4 makes \(B_u\) a clique of \(G\).  Equation (3.4) makes every vertex
of \(f^{-1}(u)\) adjacent in \(G\) to every member of \(B_u\).  Properness
of \(f\) in \(H[X]\) means that any two vertices of \(f^{-1}(u)\) are
nonadjacent in \(H\), hence adjacent in \(G\).  Therefore every \(C_u\) is a
clique of \(G\).

The private blocks and \(X\) partition \(V(G)\), so the \(k\) sets \(C_u\)
form a clique partition.  Thus \(\theta(G)\leq k\), while the accepted
parameter chain gives
\(\theta(G)\geq\gamma^\infty(G)=k\). \(\square\)

### Proposition 7 (exactness for the greatest family) — PROVED

Let \(\mathcal K_\ast\) be the greatest eternal \(k\)-family.  Under
\(\gamma(G)=\gamma^\infty(G)=k\), the response-list instance
\((H[X],L_{\mathcal K_\ast})\) is colorable if and only if
\(\theta(G)=k\).

#### Proof

The forward direction is Theorem 6.  Conversely, suppose
\(\theta(G)=k\), and fix a partition of \(V(G)\) into \(k\) cliques.
Because \(S\) is an independent \(k\)-set, it meets every part exactly
once.  Index the part containing \(u\in S\) by \(u\).

The product strategy with one guard in every clique part is an eternal
\(k\)-family and is contained in \(\mathcal K_\ast\).  Color each shared
vertex \(x\) by the index \(u\) of its clique part.  Then
\(S-\{u\}+\{x\}\) is a state of the product family, and \(ux\in E(G)\).
Thus \(u\in L_{\mathcal K_\ast}(x)\).  Since clique parts of \(G\) are
independent color classes of \(H\), this is a proper response-list coloring.
\(\square\)

Proposition 7 is an exact localization of the problem, not a resolution:
proving its list instance colorable in every equality graph is equivalent to
proving the original conclusion.  Its value is that the only unresolved
vertices are the shared vertices, and the transition family supplies
concrete allowed-color lists.

### Lemma 8 (collision transfer) — PROVED

Let \(x,y\in X\) be nonadjacent in \(G\), and suppose

\[
 u\in L_{\mathcal F}(x)\cap L_{\mathcal F}(y).
\tag{3.9}
\]

Then there is a vertex \(v\in S-\{u\}\) such that

\[
 v\in L_{\mathcal F}(x)\cup L_{\mathcal F}(y).
\tag{3.10}
\]

More precisely, closure produces a state

\[
 S-\{u,v\}+\{x,y\}\in\mathcal F,
\tag{3.11}
\]

and the subsequent attack at \(u\) proves either
\(v\in L_{\mathcal F}(x)\) or
\(v\in L_{\mathcal F}(y)\).

#### Proof

Start at \(D_x=S-\{u\}+\{x\}\in\mathcal F\) and attack \(y\).  The guard at
\(x\) cannot respond because \(xy\notin E(G)\).  Closure therefore moves a
guard \(v\in S-\{u\}\) to \(y\), giving (3.11).

Now attack the unoccupied vertex \(u\).  No guard in
\(S-\{u,v\}\) is adjacent to \(u\), because \(S\) is independent.  Both
\(x\) and \(y\) are adjacent to \(u\) by (3.9), so the responding guard is
one of them.  If \(x\to u\), the successor is
\(S-\{v\}+\{y\}\), proving \(v\in L_{\mathcal F}(y)\).  If \(y\to u\), the
successor is \(S-\{v\}+\{x\}\).  This state dominates \(v\); no member of
\(S-\{v\}\) is adjacent to \(v\), so \(xv\in E(G)\).  It therefore proves
\(v\in L_{\mathcal F}(x)\).  (In the first branch, \(vy\in E(G)\) already
holds because \(v\to y\) was the preceding response.) \(\square\)

### Corollary 9 (singleton response classes are safe) — PROVED

If

\[
 L_{\mathcal F}(x)=L_{\mathcal F}(y)=\{u\},
\]

then \(xy\in E(G)\).  Equivalently, the shared vertices with the same
singleton response list form a clique of \(G\).

This is immediate from Lemma 8: a nonedge \(xy\) would force an additional
list color for one endpoint.

### Corollary 10 (a counterexample has a list-critical shared core) — PROVED

In a counterexample, use \(\mathcal F=\mathcal K_\ast\).  There is a
vertex-minimal induced subgraph \(Y\) of \(H[X]\) whose response-list instance
is uncolorable.  Every such \(Y\) has the following properties:

1. \(Y\) is connected;
2. for every \(x\in V(Y)\),
   \[
   d_Y(x)\geq |L_{\mathcal K_\ast}(x)|;
   \tag{3.12}
   \]
3. \(|V(Y)|\geq3\);
4. either \(Y\) contains a cycle, or \(Y\) is a tree whose leaves have
   singleton response lists; in the tree case, the neighbor of each leaf has
   at least two response colors; and
5. every clique \(Q\) of \(Y\) satisfies
   \[
   \left|\bigcup_{x\in Q}L_{\mathcal K_\ast}(x)\right|\geq |Q|.
   \tag{3.13}
   \]

#### Proof

Existence follows from Proposition 7 and finiteness.  Different connected
components could be colored independently, proving item 1.

By minimality, \(Y-x\) has a response-list coloring.  If
\(d_Y(x)<|L(x)|\), at least one color in \(L(x)\) is unused by the neighbors
of \(x\), so that coloring extends to \(x\), a contradiction.  This proves
(3.12).

A one-vertex instance is colorable because every list is nonempty.  A
two-vertex uncolorable instance must put the same singleton list on both
ends of its edge, which Corollary 9 forbids.  Hence item 3 holds.

If \(Y\) is acyclic, connectedness makes it a tree.  A leaf \(x\) has
degree one, so (3.12) forces \(|L(x)|=1\), say \(L(x)=\{u\}\).  Color
\(Y-x\).  Its unique neighbor must receive \(u\), or the coloring would
extend to \(x\).  Lemma 8 applied to this edge and common color \(u\) forces
an additional color into the neighbor's list.

A clique of \(Y\subseteq H[X]\) is an independent set of \(G[X]\), so
item 5 is exactly Lemma 5. \(\square\)

This core is a rigorous version of the “shared vertices do not extend”
obstruction identified when Klostermeyer--Mynhardt corrected the 2009
private-neighborhood argument.  No novelty is claimed for the basic private
blocks; the response-list formulation and collision-transfer statement are
recorded here as campaign working lemmas pending literature and hostile
review.

Item 5 is an important boundary: the obstruction is not a shortage of
responses on any complement clique.  Every clique subinstance already has a
system of distinct response colors.  What can still fail is global
compatibility across overlapping cliques, just as clique-wise color
feasibility does not imply a coloring in an imperfect graph.

### Why collision transfer does not finish the proof

The natural second iteration was to choose one response color for every
shared vertex, minimize the number of monochromatic \(H\)-edges, and use
Lemma 8 to reroute one endpoint of a conflict.  Lemma 8 guarantees an
alternative color somewhere, but it does not guarantee that rerouting
decreases the number of conflicts.  The new color may already be blocked by
other shared vertices.  Repetition can close into a cycle or terminate at
different singleton boundary constraints, exactly the two alternatives in
Corollary 10.

This is not merely a hypothetical concern.  The accepted deep near-miss

\[
 G=\texttt{J@l|bfNuVK_}
\]

has

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4).
\]

The light diagnostic probe records for
\(H=\texttt{J\}QA[WoHgr?}\):

- every pair of vertices has a common neighbor;
- every maximal clique is a triangle;
- every vertex link is bipartite; and
- all eight maximum independent triples survive the simultaneous kernels
  \(\mathcal K_0,\ldots,\mathcal K_4\).

The exact kernel sizes are

\[
 110,\ 105,\ 100,\ 88,\ 64,\ 10,\ 0,
\]

and the eight forced triples first start disappearing at
\(\mathcal K_5\).  The parameter and finite-horizon behavior agree with
accepted C-023 and C-026.  Thus every condition based on the static
dictionary **only through the additional requirement that every forced
triangle lies in \(\mathcal K_4\)** is insufficient.  Deeper or genuinely
global transition information is still necessary.

### Attempt-two gate

**BLOCKED AFTER THE SECOND SERIOUS ITERATION.**  The private-block argument
now has an exact endpoint:

\[
 \boxed{\text{rule out the list-critical shared-response core }Y.}
\]

Theorem 6 proves that doing so gives a clique partition.  Lemma 8 shows that
an edge conflict cannot be trapped between two identical singleton lists.
What is missing is a monotone invariant that prevents the alternating
cycle/tree obstruction of Corollary 10.  Asking directly for a proper
response-list coloring without such an invariant is equivalent to the
original conjecture by Proposition 7, so this route is stopped at the
campaign gate rather than relabeled as a proof.

## 4. Consolidated outcome

### PROVED in this note

1. \(\gamma=\alpha=k\) gives a common \(H\)-neighbor for every set of at
   most \(k-1\) vertices and already forces purity of the \(k\)-clique
   complex.
2. Ridge-adjacent maximum cliques are connected by a unique forced
   one-guard move.
3. A maximum independent state decomposes the graph into private cliques and
   shared vertices with exact response lists.
4. Those family-membership response lists satisfy Hall's condition on every
   independent attack set (equivalently, every complement clique).
5. A proper response-list coloring of the shared graph produces a
   \(k\)-clique partition.
6. In the greatest eternal family, that response-list condition is exact.
7. The collision-transfer lemma and the list-critical-core consequences
   hold.

### REFUTED mechanisms

1. Proper colorings of all face links do not automatically glue globally.
2. Physical guard labels are not invariant, even in an equality graph.
3. Simple connectivity of the complement clique complex is not a necessary
   consequence suggested by the data.
4. The conjunction of the complete static/local \(k=3\) dictionary with
   survival of every forced triangle through \(\mathcal K_4\) is too weak.

### Open gap

The universal conjecture would follow from a theorem forbidding the
list-critical shared-response core of Corollary 10 in a graph satisfying
(1.2), (1.3), (1.5), and full eternal closure.  No such theorem is proved
here.  The exact obstruction is global consistency of shared-vertex
responses, not the already controlled clique links.

## 5. If this lane is resumed

The next acceptable iteration must add a mechanism not present in this
note.  The highest-value targets are:

1. use the C-051 colorings of all clique links to constrain the lists along
   a minimal core \(Y\), rather than merely recoloring \(Y\) abstractly;
2. find a potential on the full family states that strictly decreases under
   the collision transfer, or prove by a named equality example that no such
   natural potential exists; and
3. use `J@l|bfNuVK_` as the first falsification target for every proposed
   lemma, because it satisfies the complete static/local \(k=3\) dictionary
   and four adaptive transition levels before failing.

No order-13 SAT or certificate-production job is justified by this proof
lane.
