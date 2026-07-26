# Cross-state attack at \(k=3\): frozen-color projections

## Status

Date: 2026-07-26 (PDT)

All statements use the standard one-guard-moves model: attacks are made only
at unoccupied vertices, exactly one adjacent guard moves, and every state in
an eternal family dominates.

The main result is a genuine cross-state reduction.  If one response color is
absent from a set of attacks relative to an independent family state, then
that guard cannot leave its reference position while attacks remain in the
corresponding induced subgraph.  Deleting the frozen guard produces an
eternal family with one fewer guard and, under the original domination
equality, an exact smaller instance of the gamma--theta hypothesis.

For \(k=3\), the accepted \(\alpha=2\) theorem makes every such projected
complement bipartite.  Consequently, an odd response-core cycle with one
common missing color, including the tight common-two-list odd-cycle
obstruction, is impossible.

This does **not** resolve the \(k=3\) slice.  Mixed three-color cut-block and
high-degree cores remain.  Explicit residual list instances and the named
stress tests below delimit that gap.

## 1. Two response-list notions

Let \(\mathcal F\) be an eternal family of \(k\)-sets, and let
\(S\in\mathcal F\) be an independent \(k\)-set.  In the conjecture setting,
every maximum independent \(k\)-set belongs to every eternal \(k\)-family,
so this is the relevant reference state.

For \(x\notin S\), define the **family-response list**

\[
 L^{\mathcal F}_S(x)=
 \{u\in S:ux\in E(G)\text{ and }S-u+x\in\mathcal F\}
\tag{1.1}
\]

and the **static viable list**

\[
 L^{\mathrm{stat}}_S(x)=
 \{u\in S:ux\in E(G)\text{ and }S-u+x
                 \text{ dominates }G\}.
\tag{1.2}
\]

Plainly,

\[
 L^{\mathcal F}_S(x)\subseteq L^{\mathrm{stat}}_S(x).
\tag{1.3}
\]

Both lists are nonempty in the equality setting.  The family lists are those
used in C-059.  The static lists are the viable lists used in C-058.

The independently proved ridge-covariance theorem in
`math/working/cross_state_response_exchange.md` says that if independent
family states \(S,T\) share \(k-1\) vertices and \(\rho\) transposes their
exchanged vertices, then

\[
 \rho(L^{\mathcal F}_S(x))
 =L^{\mathcal F}_T(\rho(x)).
\tag{1.4}
\]

In particular, response omission is genuinely covariant across reference
states:

\[
 \rho(W^{\mathcal F}_{S,u})
 =W^{\mathcal F}_{T,\rho(u)}.
\tag{1.5}
\]

Here \(W^{\mathcal F}_{S,u}\) denotes the set in (2.1), with the reference
state displayed in the subscript.

This is an incidence statement; \(\rho\) need not be a graph automorphism.
The frozen projection below supplies the graph-theoretic constraint on every
one of these transported omission sets.

We will use the following restoration fact in its exact family form.

### Lemma 1 (restoration from an arbitrary family state) — PROVED

For \(D\in\mathcal F\), put

\[
 U=S-D,\qquad X=D-S.
\]

Then

\[
 U\subseteq\bigcup_{x\in X}L^{\mathcal F}_S(x)
 \subseteq\bigcup_{x\in X}L^{\mathrm{stat}}_S(x).
\tag{1.6}
\]

#### Proof

Fix \(u\in U\).  Starting afresh from \(D\), attack every vertex of
\(U-\{u\}\).  A currently occupied member of \(S\) cannot answer an attack
at another member of \(S\), because \(S\) is independent.  Thus these
attacks restore all but \(u\) using guards originally in \(X\).  The family
now contains a state \(S-u+x\) for some \(x\in X\).

Attack the still-unoccupied vertex \(u\).  No member of \(S-\{u\}\) is
adjacent to \(u\), so the guard at \(x\) must answer.  Hence \(ux\in E(G)\)
and \(S-u+x\in\mathcal F\), proving
\(u\in L^{\mathcal F}_S(x)\).  The static inclusion is (1.3). \(\square\)

## 2. The frozen-color projection

Fix \(u\in S\).  For either
\(\diamond\in\{\mathcal F,\mathrm{stat}\}\), set

\[
 W^\diamond_u=
 \{x\in V(G)-S:u\notin L^\diamond_S(x)\}
\tag{2.1}
\]

and let

\[
 Q^\diamond_u=
 G[(S-\{u\})\cup W^\diamond_u].
\tag{2.2}
\]

Define a family of \((k-1)\)-sets in \(Q^\diamond_u\) by

\[
 \mathcal P^\diamond_u=
 \{A\subseteq V(Q^\diamond_u):
       |A|=k-1\text{ and }\{u\}\cup A\in\mathcal F\}.
\tag{2.3}
\]

### Theorem 2 (frozen-color projection) — PROVED

For \(k\geq2\), \(\mathcal P^\diamond_u\) is an eternal dominating family of
size \(k-1\) in \(Q^\diamond_u\).  Consequently,

\[
 \alpha(Q^\diamond_u)=
 \gamma^\infty(Q^\diamond_u)=k-1.
\tag{2.4}
\]

If in addition \(\gamma(G)=k\), then

\[
 \gamma(Q^\diamond_u)=k-1
\tag{2.5}
\]

as well.

#### Proof

The family is nonempty because

\[
 S-\{u\}\in\mathcal P^\diamond_u.
\tag{2.6}
\]

Take \(A\in\mathcal P^\diamond_u\) and attack
\(r\in V(Q^\diamond_u)-A\) from the family state
\(D=\{u\}\cup A\).  Suppose that the guard at \(u\) answered.  The successor

\[
 D'=A\cup\{r\}\in\mathcal F
\tag{2.7}
\]

misses \(u\).  Moreover,

\[
 D'-S\subseteq W^\diamond_u.
\]

If \(\diamond=\mathcal F\), every vertex in this outside set omits \(u\)
from its family list.  If \(\diamond=\mathrm{stat}\), it omits \(u\) from
the static list and hence, by (1.3), from the family list as well.  In both
cases Lemma 1 applied to \(D'\) says that the missing vertex \(u\) belongs
to the union of family lists of \(D'-S\), a contradiction.

Therefore \(u\) cannot answer.  Some guard \(v\in A\) moves to \(r\), and

\[
 A-v+r\in\mathcal P^\diamond_u.
\tag{2.8}
\]

This proves closure.  It also proves that every \(A\in\mathcal P^\diamond_u\)
dominates \(Q^\diamond_u\): every unoccupied vertex \(r\) has the responding
neighbor \(v\in A\), while occupied vertices dominate themselves.  Thus
\(\mathcal P^\diamond_u\) is an eternal \((k-1)\)-family.

The independent set \(S-\{u\}\) lies in \(Q^\diamond_u\), so
\(\alpha(Q^\diamond_u)\geq k-1\).  The general bound
\(\alpha\leq\gamma^\infty\), together with the family just constructed,
gives (2.4).

Now assume \(\gamma(G)=k\).  The preceding argument shows in particular
that \(S-\{u\}\) dominates \(Q^\diamond_u\), so
\(\gamma(Q^\diamond_u)\leq k-1\).  Conversely, suppose that a set
\(B\) of at most \(k-2\) vertices dominated \(Q^\diamond_u\).  Every vertex
outside \(Q^\diamond_u\) is either \(u\), or a vertex
\(x\notin S\) for which \(u\in L^\diamond_S(x)\).  In either list notion,
this membership includes the edge \(ux\).  Hence

\[
 B\cup\{u\}
\]

would dominate all of \(G\), contradicting \(\gamma(G)=k\).  This proves
(2.5). \(\square\)

### Corollary 3 (exact induction step) — PROVED

Assume the gamma--theta conjecture is known for parameter \(k-1\).  Under
the hypotheses of Theorem 2 with \(\gamma(G)=k\),

\[
 \theta(Q^\diamond_u)=k-1.
\tag{2.9}
\]

#### Proof

Theorem 2 gives

\[
 \gamma(Q^\diamond_u)=
 \gamma^\infty(Q^\diamond_u)=k-1.
\]

Apply the conjecture at parameter \(k-1\). \(\square\)

This is a genuine induction on the exact conjecture hypothesis, not merely
on \(\alpha=\gamma^\infty\).

### The projected family need not be greatest

Theorem 2 proves that \(\mathcal P^\diamond_u\) is **an** eternal family of
\(Q^\diamond_u\).  It need not be the greatest eternal family there.  This
distinction is strict even in an equality graph.

For the independently checked graph `FCZbg`, take the greatest eternal
three-family, \(S=\{0,4,6\}\), \(u=4\), and the family-list omission set
\(W^{\mathcal F}_4=\{3,5\}\).  On the projected vertex set
\(\{0,3,5,6\}\), the frozen family is

\[
 \mathcal P^{\mathcal F}_4=\{05,06,35,36\},
\tag{2.10}
\]

whereas the greatest eternal two-family of the projected graph is

\[
 \{03,05,06,35,36,56\}.
\tag{2.11}
\]

Thus a lower-parameter product strategy or another state in the greatest
projected family cannot automatically be lifted while keeping \(u\) frozen.
In particular, Corollary 3 does not by itself produce colors from the
original **family-response** lists.  The static lift proved next uses only a
clique partition and a fresh domination check, so it is unaffected by this
counterexample.

## 3. A stronger static deletion-coloring consequence

For family lists, (2.9) gives a clique partition of the projected graph but
does not assert that its colors belong to the original *family* lists.
For static viable lists, it does.

### Theorem 4 (static color-deletion compatibility) — PROVED

Under Corollary 3 with \(\diamond=\mathrm{stat}\), the complement-induced
graph

\[
 \overline G[W^{\mathrm{stat}}_u]
\]

has a proper coloring

\[
 f_u:W^{\mathrm{stat}}_u\longrightarrow S-\{u\}
\tag{3.1}
\]

such that

\[
 f_u(x)\in L^{\mathrm{stat}}_S(x)
\quad\text{for every }x\in W^{\mathrm{stat}}_u.
\tag{3.2}
\]

#### Proof

Take a partition of \(Q^{\mathrm{stat}}_u\) into \(k-1\) cliques.  The
independent set \(S-\{u\}\) has \(k-1\) vertices, so every clique part
contains exactly one of these anchors.  Label each part by its anchor.

Let \(x\in W^{\mathrm{stat}}_u\), and let \(v\in S-\{u\}\) be the anchor of
its part.  Then \(vx\in E(G)\).  Moreover,

\[
 A=(S-\{u,v\})\cup\{x\}
\tag{3.3}
\]

contains one representative from every clique part, so \(A\) dominates
\(Q^{\mathrm{stat}}_u\).  Adding \(u\) dominates every vertex outside
\(Q^{\mathrm{stat}}_u\): such a vertex is \(u\) itself or has
\(u\in L^{\mathrm{stat}}_S\) and is therefore adjacent to \(u\).  Thus

\[
 A\cup\{u\}=S-v+x
\]

dominates \(G\).  Together with \(vx\in E(G)\), this proves
\(v\in L^{\mathrm{stat}}_S(x)\).

Vertices assigned the same anchor lie in one clique of \(G\), so the
assignment is proper in \(\overline G\). \(\square\)

The genuinely new content for a vertex-minimal list obstruction occurs when
all of its vertices omit one color.  For a proper induced subgraph,
colorability already follows from vertex-minimality.  Theorem 4 should not
be read as a solution of mixed or full-list cores.

## 4. The \(k=3\) consequence

The parameter-two case is already proved in `math/reductions.md`: if
\(\alpha=\gamma^\infty=2\), then \(\theta=2\).  Therefore no unproved
induction hypothesis is needed at \(k=3\).

Let

\[
 S=\{a,b,c\},\qquad
 \gamma(G)=\gamma^\infty(G)=3.
\]

The equality collapse supplies \(\alpha(G)=3\), and every maximum
independent triple \(S\) lies in every eternal three-family.

### Corollary 5 (every missing-color projection is bipartite) — PROVED

For either list notion and every \(u\in S\),

\[
 \overline G[(S-\{u\})\cup W^\diamond_u]
\quad\text{is bipartite}.
\tag{4.1}
\]

In the static-list case,
\(\overline G[W^{\mathrm{stat}}_u]\) moreover has a proper coloring from the
two lists \(L^{\mathrm{stat}}_S(x)-\{u\}\).

#### Proof

Theorem 2 gives

\[
 \gamma(Q^\diamond_u)=
 \gamma^\infty(Q^\diamond_u)=2.
\]

The accepted parameter-two theorem gives
\(\theta(Q^\diamond_u)=2\), which is exactly (4.1).  The final assertion is
Theorem 4. \(\square\)

### Corollary 6 (the common-two-list odd cycle is impossible) — PROVED

There is no odd cycle \(C\) in \(\overline G\) all of whose vertices have

\[
 L^{\mathcal F}_S(x)=\{a,b\}.
\tag{4.2}
\]

The same conclusion holds for the static lists.

#### Proof

Every vertex of \(C\) omits \(c\), so \(C\) is a subgraph of
\(\overline G[W^\diamond_c]\).  Corollary 5 says that graph is bipartite,
contradicting the odd cycle. \(\square\)

More generally, every odd cycle in a response-list core must use all three
response colors:

\[
 \bigcup_{x\in V(C)}L^\diamond_S(x)=S.
\tag{4.3}
\]

This eliminates the entirely tight two-list cycle from the C-059
list-critical alternatives.  For completeness, if a cycle has a two-element
list at every vertex and those lists are not all equal, choose an edge
\(xy\) with a color in \(L(x)-L(y)\), color \(x\) with that color, and
greedily color the path obtained by deleting \(xy\), starting at the other
neighbor of \(x\) and finishing at \(y\).  The list of \(y\) omits the color
on \(x\), so the final choice cannot conflict with both path neighbors.
Hence an uncolorable two-list cycle has one common two-list and odd length,
exactly the case excluded above.

## 5. Two further full-family consequences

These facts were checked while trying to push the projection through the
remaining cut blocks.

### Lemma 7 (common complement neighborhood of a co-occupied ridge) — PROVED

Let

\[
 D=R\cup\{u\}\in\mathcal F,\qquad |R|=k-1,
\]

and put

\[
 C=N_{\overline G}(R)
   =\bigcap_{r\in R}N_{\overline G}(r).
\tag{5.1}
\]

Then \(G[C]\) is a clique.  For every \(x\in C-D\), the attack at \(x\)
has the unique response \(u\to x\), and

\[
 R\cup\{x\}\in\mathcal F.
\tag{5.2}
\]

#### Proof

No guard in \(R\) is adjacent in \(G\) to \(x\).  Since \(D\) dominates,
\(ux\in E(G)\), so \(u\to x\) is the unique possible response and (5.2)
follows.

For distinct \(x,y\in C-D\), the family state \(R\cup\{x\}\) must dominate
\(y\).  Every member of \(R\) misses \(y\), so \(xy\in E(G)\).  If
\(u\in C\), the same argument using \(D\), or domination of \(u\) by
\(R\cup\{x\}\), gives \(ux\in E(G)\) for every other \(x\in C\).  Thus all
pairs in \(C\) are \(G\)-edges. \(\square\)

### Lemma 8 (a Hall-tight core edge forces the two-outside state) — PROVED

Let distinct \(x,y\notin S\) be nonadjacent in \(G\), and suppose

\[
 L^{\mathcal F}_S(x)\cup L^{\mathcal F}_S(y)=U,
\qquad |U|=2.
\tag{5.3}
\]

Then

\[
 (S-U)\cup\{x,y\}\in\mathcal F.
\tag{5.4}
\]

In particular, at \(k=3\), if \(U=\{a,b\}\), then

\[
 \{c,x,y\}\in\mathcal F.
\tag{5.5}
\]

#### Proof

Starting at \(S\), attack \(x\) and then \(y\).  Since \(xy\notin E(G)\),
the first moved guard cannot answer the second attack, so two distinct
guards leave \(S\).  The resulting family state has the form

\[
 (S-U')\cup\{x,y\},\qquad |U'|=2.
\]

Lemma 1 gives

\[
 U'\subseteq
 L^{\mathcal F}_S(x)\cup L^{\mathcal F}_S(y)=U.
\]

The two sets have the same cardinality, hence \(U'=U\). \(\square\)

Lemma 7 applied to the forced states in Lemma 8 constrains common complement
neighborhoods, but it does not connect two Hall-tight edges separated by a
mixed-list edge.  That is the precise point at which the cut-block attempt
stops.

## 6. Residual obstruction: why the cut-block case remains

The following four-vertex list instance is a concrete refutation of the
claim that the projection and the C-059 local list conditions alone force a
coloring.

Let the core graph in \(\overline G\) be the path

\[
 x_0x_1x_2x_3
\]

and assign

\[
 L(x_0)=\{a\},\qquad
 L(x_1)=\{a,c\},\qquad
 L(x_2)=\{b,c\},\qquad
 L(x_3)=\{b\}.
\tag{6.1}
\]

This instance is uncolorable: \(x_0=a\) forces \(x_1=c\), while
\(x_3=b\) forces \(x_2=c\), creating a conflict on \(x_1x_2\).
It is vertex-minimal uncolorable.

Nevertheless:

1. every vertex satisfies \(d=|L|\);
2. every edge satisfies clique-wise Hall;
3. the collision-transfer list consequence holds on every edge;
4. singleton response classes are independent; and
5. every missing-color subinstance is list-colorable:
   - omitting \(a\), color \(x_2,x_3\) by \(c,b\);
   - omitting \(b\), color \(x_0,x_1\) by \(a,c\);
   - omitting \(c\), color the isolated \(x_0,x_3\) by \(a,b\).

Thus the frozen-color theorem eliminates the common-two-list odd block but
does not eliminate mixed three-color cut blocks.  Instance (6.1) is an
abstract list obstruction; it is **not** claimed to be realized by an
eternal equality graph.  Ruling out its realization requires a new
cross-state relation across the middle mixed-list edge, not another
single-reference coloring argument.

Full-list/high-degree cores are even less affected: a vertex with list
\(\{a,b,c\}\) lies in none of the sets \(W_u\).

## 7. Named stress tests

The theorem hypotheses and their failure modes were checked against all
required examples.  The \(C_4\), `FCpbO`, parameter, and kernel claims below
reuse accepted campaign artifacts.  The newly displayed response-list
tables and bipartitions are deterministic **OBSERVED** diagnostics from
those exact graph records; they are not inputs to Theorems 2--4.

### \(C_4\)

For \(S=\{0,2\}\), the greatest eternal two-family contains all six pairs and

\[
 L^{\mathcal F}_S(1)=L^{\mathcal F}_S(3)=\{0,2\}.
\]

Both missing-color sets are empty, and each projection is the one remaining
anchor.  The theorem is consistent with the known physical-label exchange
loop on \(C_4\); it makes no claim that physical guard identities are
invariant.

### `FCpbO`

For the equality graph `FCpbO`, its greatest eternal three-family has twelve
states.  At \(S=\{0,5,6\}\), the family lists are

\[
 L(1)=\{6\},\quad L(2)=\{5\},\quad
 L(3)=\{0\},\quad L(4)=\{6\}.
\]

The three projected complements have bipartitions

\[
\begin{array}{c|c}
u&\text{bipartition of }(S-u)\cup W^{\mathcal F}_u\\ \hline
0&\{1,4,6\}\mid\{2,5\}\\
5&\{0,3\}\mid\{1,4,6\}\\
6&\{0,3\}\mid\{2,5\}.
\end{array}
\]

Thus the result survives an equality graph with nontrivial complement flag
homology; no simple-connectivity assumption has entered.

### \(C_7\)

There is no eternal three-family.  For the one-ply/static lists at
\(S=\{0,2,4\}\),

\[
 L(1)=L(3)=\{2\},\qquad L(5)=\{4\},\qquad L(6)=\{0\}.
\]

For \(u=0\), the projected vertex set contains the complement triangle
\(\{1,3,5\}\), so the bipartite conclusion fails.  This is consistent with
the kernel profile \(K_0\supset K_1\supset K_2=\varnothing\): a one-ply
response set is not a full eternal family.

### `J@l|bfNuVK_`

This graph has

\[
 (\gamma,\alpha,\gamma^\infty,\theta)=(3,3,4,4),
\]

so again no eternal three-family exists.  At \(S=\{0,1,2\}\), its static
lists are

\[
\begin{array}{c|c}
3&\{2\}\\
4,6&\{0,2\}\\
5,7&\{1,2\}\\
8,9,10&\{0,1\}.
\end{array}
\tag{7.1}
\]

Each static missing-color subinstance is list-colorable:

\[
\begin{array}{c|c}
u&\text{one coloring of }W^{\mathrm{stat}}_u\\ \hline
0&3{:}2,\ 5{:}1,\ 7{:}2\\
1&3{:}2,\ 4{:}0,\ 6{:}2\\
2&8{:}0,\ 9{:}1,\ 10{:}1.
\end{array}
\]

Nevertheless the induced static-list core on
\(\{4,5,6,7,8,9,10\}\) is uncolorable.  Its complement edges are

\[
\begin{split}
&46,47,4\,10,\ 56,57,59,\ 69,\ 7\,10,\ 89,8\,10.
\end{split}
\tag{7.2}
\]

Indeed, edge \(46\) forces colors \(0,2\) to occur once each, edge \(57\)
forces \(1,2\) to occur once each, and edges \(89,8\,10\) force \(9\) and
\(10\) to have the same color \(t\in\{0,1\}\).  If \(t=0\), edge
\(4\,10\) forces \(4=2\), hence \(6=0\), contradicting edge \(69\).
If \(t=1\), edge \(59\) forces \(5=2\), hence \(7=1\), contradicting
edge \(7\,10\).

This is an exact high-degree/mixed-color stopping example for the static
mechanism, although it is not an eternal-equality graph.

There is also a full-closure stress check.  The six maximum independent
triples in \(K_5\) use successors in \(K_4\), but for
\(S=\{0,1,2\}\) these finite-horizon lists are

\[
 L(3)=\cdots=L(7)=\{2\},\qquad
 L(8)=L(9)=L(10)=\{0,1\}.
\]

For \(u=0\), the tentative projection contains the complement triangle
\(\{1,4,6\}\).  Hence survival through five deletion levels cannot replace
the arbitrary-state restoration used in Theorem 2.

### Schläfli graph

The 27-vertex Schläfli graph has
\(\gamma=\alpha=3<\theta=6\) but no eternal three-family:

\[
 |K_0|=1125,\qquad |K_1|=45,\qquad |K_2|=0.
\]

For the representative independent state \(S=\{0,11,16\}\), every
one-ply/static list has size two.  The vertices split into eight copies of
each list:

\[
\begin{array}{c|l}
\{0,16\}&1,2,3,4,20,23,25,26\\
\{0,11\}&5,6,17,18,19,21,22,24\\
\{11,16\}&7,8,9,10,12,13,14,15.
\end{array}
\]

All three tentative missing-color projections are bipartite and their
bipartitions respect the remaining lists.  Nevertheless \(K_2\) is empty.
Thus even the visible conclusion of Theorem 4 at one transition level is a
necessary pattern, not a substitute for an eternal family.

## 8. Exact stopping boundary

The cross-state mechanism proves:

1. deleting a response color projects a full eternal \(k\)-family to an
   exact \((k-1)\)-parameter instance;
2. at \(k=3\), every missing-color projection is bipartite;
3. static missing-color subinstances are colorable from their remaining
   lists;
4. no common-two-list odd cycle can occur; and
5. every Hall-tight response-core edge forces the corresponding two-outside
   family state.

The projected family may be a proper subfamily of the greatest family of the
projected graph, as `FCZbg` shows.  Consequently, lower-parameter strategies
cannot be imported into the original family-response lists without a separate
lifting proof.

What remains is a core in which every odd obstruction collectively uses all
three colors.  It may branch through cut vertices as in (6.1), contain
vertices with \(d>|L|\), or contain full-list vertices invisible to every
single frozen-color projection.  Lemma 8 supplies family states on the
Hall-tight edges, while Lemma 7 controls each such state's common complement
neighborhood, but neither statement relates the forced states across a
mixed-list edge.

Attempting to finish by merely combining the three color-deletion
colorings is another formulation of the unresolved global compatibility
problem.  The next valid step would need a genuinely multi-projection
compatibility law or a monotone transition invariant; no such law is proved
here.
