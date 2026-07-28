# Anchorless physical-inactive vertices have componentwise palettes

## Status and exact scope

Date: 2026-07-28 (PDT)

This is a **candidate theorem package awaiting hostile review**.  It uses
the standard one-guard-moves model: attacks are made only at unoccupied
vertices, and exactly one guard moves along one graph edge.

The main result incorporates the anchorless part of the physical
complement link into the component-palette theorem.  Anchorless vertices
are not shown to be impossible.  Instead, every vertex on one side of one
link component is proved to have the same retained response palette.  A
second result gives a genuine third-attack constraint on the external
common-neighbor layers forced by the deletion-critical condition.

Neither result proves the full-list branch, the complete parameter-three
case, or the universal gamma--theta conjecture.  No literature-priority
claim is made.

## 1. Setup and accepted dependencies

Let

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
 \qquad H=\overline G,
\]

and let \(\mathcal F\) be an optimal eternal family of dominating
triples.  Fix an independent state

\[
 S=\{s_0,s_1,s_2\}\in\mathcal F
\]

and a vertex \(x\notin S\) having a full family response at \(S\):

\[
 D_j=S-\{s_j\}+\{x\}\in\mathcal F
 \qquad(0\le j\le2).
\tag{1.1}
\]

Put

\[
 B=N_H(x),\qquad
 B_i=B\cap N_H(s_i),\qquad
 B_*=B-(B_0\cup B_1\cup B_2),
\tag{1.2}
\]

and define the retained anchor palette

\[
 P(b)=\{i:\{x,s_i,b\}\in\mathcal F\}
 \qquad(b\in B).
\tag{1.3}
\]

The following accepted results are used explicitly.

1. The physical complement link \(H[B]\) is bipartite and has no
   isolated vertex.  Along each connected component, ridge covariance
   makes the three response roles at an attacked anchor independent of
   the chosen link edge.  This is Theorem 5.2 in C-073.
2. C-132 proves
   \[
   |P(b)|\ge2
   \tag{1.4}
   \]
   for every \(b\in B\), and
   \[
   i\in P(b)
   \Longrightarrow
   N_{H[B]}(b)\cap B_i=\varnothing.
   \tag{1.5}
   \]
   It also proves \(b\in B_i\Longrightarrow i\in P(b)\).
3. In the equality-critical deletion branch,
   \(\gamma(G-x)\ge3\).  Equivalently, every pair of vertices of \(H-x\)
   has a common neighbor in \(H-x\); this is the C-127 target
   translation.

The first theorem below uses dependencies 1--2.  The external-layer
theorem additionally uses dependency 3.

## 2. Componentwise retained-palette rigidity

### Theorem 2.1 — PROVED IN THIS NOTE

Let \(C\) be a connected component of \(H[B]\), and fix its bipartition

\[
 C=U\mathbin{\dot\cup}V.
\tag{2.1}
\]

There are two palettes

\[
 \Pi_U,\Pi_V\subseteq\{0,1,2\},
 \qquad |\Pi_U|,|\Pi_V|\ge2,
\tag{2.2}
\]

such that

\[
 P(b)=\Pi_U\quad(b\in U),
 \qquad
 P(c)=\Pi_V\quad(c\in V).
\tag{2.3}
\]

Thus anchorless vertices on one side of a physical link component do not
carry independent dynamic choices: their complete retained palettes are
locked to that side.

#### Proof

Every vertex of \(C\) lies on an edge because \(H[B]\) has no isolated
vertices.  For an edge \(bc\), with \(b\in U,c\in V\), the triple

\[
 T_{bc}=\{x,b,c\}
\tag{2.4}
\]

is independent in \(G\).  Equality makes every maximum independent
triple a member of every optimal eternal family, so \(T_{bc}\in\mathcal
F\).

Fix an anchor \(s_i\), and attack it from \(T_{bc}\).  The \(c\)-guard
can answer exactly when

\[
 cs_i\in E(G)
 \quad\hbox{and}\quad
 \{x,b,s_i\}\in\mathcal F.
\tag{2.5}
\]

The second condition is \(i\in P(b)\).  Conversely, if \(i\in P(b)\),
then (1.5) and \(bc\in E(H[B])\) imply \(c\notin B_i\), so
\(cs_i\in E(G)\).  Hence

\[
 \boxed{
 c\hbox{ answers at }s_i\hbox{ from }T_{bc}
 \quad\Longleftrightarrow\quad i\in P(b).
 }
\tag{2.6}
\]

C-073 response-role rigidity says that the membership of the
\(V\)-side guard in this response list is independent of the chosen edge
of \(C\).  Equation (2.6) therefore makes \(P(b)\) independent of the
chosen \(b\in U\).  Interchanging \(U,V\) proves the analogous statement
on \(V\).  Equation (1.4) gives the two size bounds. \(\square\)

### Corollary 2.2 (exact component types) — PROVED

With the notation of Theorem 2.1:

1. each bipartition side meets at most one root spoke;
2. if \(U\cap B_q\ne\varnothing\), then
   \[
   q\in\Pi_U,\qquad
   \Pi_V=\{0,1,2\}-\{q\};
   \tag{2.7}
   \]
3. if \(U\cap B_q\ne\varnothing\) and
   \(V\cap B_r\ne\varnothing\), then \(q\ne r\) and
   \[
   \Pi_U=\{0,1,2\}-\{r\},\qquad
   \Pi_V=\{0,1,2\}-\{q\}.
   \tag{2.8}
   \]

Consequently every component uses zero, one, or two spoke types.
Anchorless vertices merely inherit the palette of their side.

#### Proof

Suppose \(b_q\in U\cap B_q\), and choose a neighbor \(c\in V\).  C-132
gives \(q\in P(b_q)=\Pi_U\).  If \(q\in P(c)=\Pi_V\), then (1.5) would
make \(c\) anticomplete in \(H[B]\) to \(B_q\), contrary to
\(cb_q\in E(H)\).  Thus \(q\notin\Pi_V\), and the size bound in (2.2)
forces (2.7).

If the same side \(U\) met two spokes \(B_q,B_r\), with \(q\ne r\), the
same argument would omit both \(q\) and \(r\) from \(\Pi_V\), contradicting
\(|\Pi_V|\ge2\).  Thus each side meets at most one spoke.  When the two
sides meet spokes \(B_q,B_r\), they are distinct: if \(q=r\), membership
of the \(V\)-side spoke gives \(q\in\Pi_V\), while the \(U\)-side spoke
and (2.7) give \(q\notin\Pi_V\).  Applying (2.7) in both directions gives
(2.8). \(\square\)

### Corollary 2.3 (forced reverse role) — PROVED

If an index \(i\) is absent from both side palettes,

\[
 i\notin\Pi_U\cup\Pi_V,
\tag{2.9}
\]

then for every edge \(bc\) of \(C\),

\[
 \boxed{\{s_i,b,c\}\in\mathcal F.}
\tag{2.10}
\]

#### Proof

Attack \(s_i\) from the independent retained state
\(\{x,b,c\}\).  A move by \(b\) would leave
\(\{x,s_i,c\}\), which is absent because \(i\notin P(c)\).  A move by
\(c\) would leave \(\{x,s_i,b\}\), absent because \(i\notin P(b)\).
Closure therefore forces the \(x\)-guard to move to \(s_i\), producing
(2.10).  The move is along a \(G\)-edge by the full-response hypothesis
(1.1). \(\square\)

Because both side palettes have size at least two, (2.9) can involve at
most one anchor.  It occurs precisely when the two palettes omit the same
anchor.

## 3. The deletion-critical third-attack layer

Assume now, in addition, that

\[
 \gamma(G-x)\ge3.
\tag{3.1}
\]

For an anchorless \(b\in B_*\) and \(i\in P(b)\), define

\[
 Y_i(b)=N_{H-x}(b)\cap N_{H-x}(s_i).
\tag{3.2}
\]

These are common complement neighbors of the graph-adjacent pair
\(\{b,s_i\}\) in the deletion.

### Theorem 3.1 (installed external clique layer) — PROVED

For every \(b\in B_*\) and \(i\in P(b)\):

1. \(Y_i(b)\ne\varnothing\);
2. \(Y_i(b)\cap B=\varnothing\), so every member of \(Y_i(b)\) is
   adjacent to \(x\) in \(G\);
3. for every \(y\in Y_i(b)\),
   \[
   \boxed{\{b,s_i,y\}\in\mathcal F;}
   \tag{3.3}
   \]
4. \(Y_i(b)\) is independent in \(H\), equivalently a clique in \(G\).

Thus every retained color at an anchorless physical-inactive vertex
installs a nonempty external \(G\)-clique through a forced third attack.

#### Proof

Condition (3.1) says that every pair in \(H-x\) has a common neighbor in
\(H-x\).  Applied to \(b,s_i\), it proves item 1.

The palette state

\[
 E_i(b)=\{x,s_i,b\}\in\mathcal F
\tag{3.4}
\]

dominates \(G\).  If \(y\in Y_i(b)\cap B\), then \(y\) would be adjacent
in \(H\) to all three vertices of \(E_i(b)\), contradicting domination.
This proves item 2.

Now attack \(y\in Y_i(b)\) from \(E_i(b)\).  The attack is unoccupied.
Both \(b\) and \(s_i\) are blocked because \(y\) is their \(H\)-neighbor.
By item 2, \(xy\in E(G)\).  Hence the unique possible response is

\[
 x\longrightarrow y,
\]

and closure forces (3.3).

Finally, suppose distinct \(y,z\in Y_i(b)\) were adjacent in \(H\).
Then \(z\) would be a common \(H\)-neighbor of the retained state
\(\{b,s_i,y\}\), so that state would fail to dominate \(G\).  This
contradiction proves item 4. \(\square\)

### Corollary 3.2 (multiplicity and order floor) — PROVED

A vertex outside \(S\) belongs to at most two of the three sets
\(Y_0(b),Y_1(b),Y_2(b)\).  Consequently,

\[
 \left|\bigcup_{i\in P(b)}Y_i(b)\right|
 \ge
 \left\lceil\frac{|P(b)|}{2}\right\rceil.
\tag{3.5}
\]

In particular, a full palette \(P(b)=\{0,1,2\}\) forces at least two
external installed vertices.

Moreover, if \(t=|B_*|\), the accepted C-089 count gives

\[
 \boxed{|V(G)|\ge t+10.}
\tag{3.6}
\]

#### Proof

If one vertex belonged to all three \(Y_i(b)\), it would be adjacent in
\(H\) to all three vertices of the triangle \(S\), creating a \(K_4\) in
\(H\).  This contradicts \(\alpha(G)=3\), so (3.5) follows.

For (3.6), put

\[
 Q_S=\{q\notin S:q\text{ is adjacent in }G\text{ to every member of }S\}.
\]

Both \(x\) and every member of \(B_*\) belong to \(Q_S\), so
\(|Q_S|\ge t+1\).  C-089 proves
\(|V(G)|\ge|Q_S|+9\), yielding (3.6). \(\square\)

The order floor is conditional on the full-root pattern and is not a new
global counterexample frontier.

## 4. Exact controls and bounded discovery evidence

The six-vertex graph

```text
EEz_
```

has

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\]

At root \(S=\{0,1,2\}\) and target \(x=4\), its greatest eternal
triple-family has 18 states and

\[
 B=\{3,5\},\qquad B_2=\{3\},\qquad B_*=\{5\},
\]

with \(35\in E(H)\) and

\[
 P(3)=\{0,1,2\},\qquad P(5)=\{0,1\}.
\]

This exactly realizes the one-spoke component type (2.7): the side
opposite \(B_2\) omits color 2.  It also shows that anchorless physical
vertices are not forbidden by full one-guard closure alone; domination
equality has to do real work.

For the accepted equality control

```text
Ksv`f\knJVis
```

with root \(\{1,2,3\}\) and target 0, the two physical-link components
are the edges \(6\,8\) and \(10\,11\).  Their side palettes are

\[
\begin{array}{c|c|c}
\text{edge}&\text{first palette}&\text{second palette}\\ \hline
6\,8&\{1,2\}&\{2,3\}\\
10\,11&\{1,3\}&\{1,2\}.
\end{array}
\]

These are exactly the two-spoke palettes predicted by (2.8).

As a discovery regression, the candidate census scanned all connected
unlabeled graphs through order 9 and all 2,894,632 unlabeled \(K_4\)-free
complements at order 10.  At order 10, exactly 18,777 graphs passed the
static \(\gamma=\alpha=3\) test and the eternal-three fixed-point test.
No matching root occurred in the connected scans through order 9 or in
the complete order-10 complement scan, even without requiring (3.1).

This last statement is labelled **OBSERVED**, not certified finite.  It
is also consistent with the analytic bound (3.6), which already gives
the rigorous order-at-least-11 consequence as soon as
\(B_*\ne\varnothing\), without any connectedness assumption.

## 5. Corrected proof frontier

The anchorless physical-inactive case is no longer arbitrary:

\[
\boxed{
\begin{array}{c}
\text{every physical-link side has one retained palette;}\\
\text{a spoke fixes the opposite-side palette exactly;}\\
\text{two spokes fix both palettes exactly;}\\
\text{a shared omitted color forces every reverse edge state;}\\
\text{and each retained color at an anchorless vertex installs}\\
\text{a nonempty external clique layer in the deletion-critical branch.}
\end{array}}
\]

What remains is global.  Components with zero or one spoke still admit
more than one side-palette type, the residual vertices outside
\(S\cup B\cup\{x\}\) can couple different components, and nothing here
proves that one deletion coloring synchronizes all components.  Those are
the precise unresolved steps.
