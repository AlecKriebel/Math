# The \(k=3\) full family-response-list slice

## Status and exact boundary

Date: 2026-07-26 (PDT)

This note uses the standard **one-guard-moves** eternal domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves to the attack, and every retained state dominates.

The family \(\mathcal F\) below is arbitrary.  It is never assumed to be
the greatest eternal family.

The outcomes are:

1. **PROVED:** deleting a vertex avoided by an independent family state
   preserves \(\alpha=\gamma^\infty=3\) and preserves every remaining
   response list at that state.
2. **PROVED:** after the full-list vertices are colored, extension over all
   non-full vertices is exactly the previously accepted projection-gluing
   2-SAT problem with additional units.  In particular, a single full-list
   vertex requires exactly three 2-SAT tests.
3. **PROVED:** one full family-list vertex in an equality graph forces three
   nonempty, pairwise disjoint clique spokes, forced spoke states, and a
   second external clique layer.  This alone forces at least nine vertices.
4. **PROVED:** the complement link of the full vertex is bipartite with no
   isolated vertices.  Its edge states form ridge-connected networks.
   Response covariance makes responder roles constant throughout each link
   component and forces different anchor spokes onto opposite sides.  Thus
   every one of the three colors is locally feasible for the full vertex.
5. **CERTIFIED-FINITE:** an independent ordinary-bitset scan exhausted all
   273,193 connected unlabeled graphs through order nine.  It found no full
   **family** list under
   \(\gamma=\alpha=\gamma^\infty=3\).  At order nine it did find 24 static
   full-list incidences in 15 equality graphs; every one collapsed to a
   singleton list in the greatest eternal family.
6. **CERTIFIED CONTROL:** a separately supplied order-12 equality graph has
   a genuine full greatest-family list.  It has a unique compatible anchored
   coloring and \(\theta=3\), so full lists are a live positive slice, not a
   contradiction.
7. **REFUTED:** a universal no-full-list theorem; static fullness implying
   family fullness; a full response column implying abstract
   base-orderability; and bipartite link geometry alone guaranteeing an
   anchored extension.

The universal gamma--theta conjecture and its \(k=3\) slice remain open.
The finite scan is not a counterexample exclusion beyond the already
certified campaign frontier.  No novelty or priority claim is made.

The accepted prerequisite notes and hostile reviews read in full for this
lane were:

- `math/lemmas/independent_antineighborhood_projection.md`;
- `math/lemmas/maximum_independent_states.md`;
- `math/working/universal_complement_local_balance_attack.md`;
- `math/working/cross_state_response_exchange.md`;
- `math/working/k3_cross_state_attack.md`;
- `math/working/k3_projection_gluing.md`; and
- their independent and hostile reviews.

## 1. Setup

Let

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
 \qquad H=\overline G,
\tag{1.1}
\]

let \(\mathcal F\) be an arbitrary eternal family of triples, and let

\[
 S=\{a,b,c\}
\tag{1.2}
\]

be independent.  The accepted maximum-independent-state lemma gives
\(S\in\mathcal F\).

For \(x\notin S\), write

\[
 L_S^{\mathcal F}(x)
 =
 \{u\in S:ux\in E(G),\ S-u+x\in\mathcal F\}.
\tag{1.3}
\]

Define the full family-list set

\[
 F_3(S)=
 \{x\notin S:L_S^{\mathcal F}(x)=S\}.
\tag{1.4}
\]

A member of \(F_3(S)\) is invisible to every frozen-color omission
projection, because it omits no color.

## 2. Family monotonicity and deletion

### Lemma 2.1 (three nested list notions) — PROVED

Let \(\mathcal K_\ast\) be the greatest eternal three-family of \(G\).
For every eternal subfamily \(\mathcal F\), independent
\(S\in\mathcal F\), and \(x\notin S\),

\[
 L_S^{\mathcal F}(x)
 \subseteq
 L_S^{\mathcal K_\ast}(x)
 \subseteq
 L_S^{\mathrm{stat}}(x).
\tag{2.1}
\]

Consequently, if \(x\) is full in any proper eternal subfamily, it is full
in the greatest family and statically full.

#### Proof

Every eternal family is contained in the greatest fixed point
\(\mathcal K_\ast\).  Membership of \(S-u+x\) in either family implies
that the state dominates, which is exactly the static condition after also
recording the edge \(ux\).  These are the two inclusions. \(\square\)

This elementary monotonicity is important computationally: a zero
greatest-family result covers **every** proper eternal family.  No
enumeration of subfamilies is needed.

### Theorem 2.2 (vertex-avoidance restriction) — PROVED

Let \(x\notin S\), without assuming that \(x\) has a full list, and define

\[
 \mathcal F^{-x}
 =
 \{D\in\mathcal F:x\notin D\}.
\tag{2.2}
\]

Then \(\mathcal F^{-x}\) is an eternal family of triples in \(G-x\), and

\[
 \alpha(G-x)=\gamma^\infty(G-x)=3.
\tag{2.3}
\]

Moreover, for every \(y\notin S\cup\{x\}\),

\[
 L_{S,G-x}^{\mathcal F^{-x}}(y)
 =
 L_{S,G}^{\mathcal F}(y).
\tag{2.4}
\]

#### Proof

The family is nonempty because \(S\in\mathcal F^{-x}\).  Every retained
state dominates \(G-x\).

Take \(D\in\mathcal F^{-x}\) and an unoccupied attack

\[
 r\in V(G-x)-D.
\]

Closure in \(\mathcal F\) supplies a guard \(u\in D\cap N_G(r)\) with

\[
 D-u+r\in\mathcal F.
\]

Neither \(D\) nor the attacked vertex contains \(x\), so the successor also
avoids \(x\).  The same one-edge move therefore remains in
\(\mathcal F^{-x}\).  This proves literal closure in \(G-x\).

The independent triple \(S\) survives deletion, so
\(\alpha(G-x)\geq3\), while induced-subgraph monotonicity gives
\(\alpha(G-x)\leq\alpha(G)=3\).  The displayed eternal family and the
general bound \(\alpha\leq\gamma^\infty\) then force (2.3).

Finally, each state \(S-u+y\) avoids \(x\).  Its membership in
\(\mathcal F^{-x}\) is therefore exactly its membership in
\(\mathcal F\), and the graph edge \(uy\) is unchanged by deleting \(x\).
This proves (2.4). \(\square\)

### Corollary 2.3 (minimum-counterexample deletion dichotomy) — PROVED

Suppose additionally that \(G\) is a minimum-order \(k=3\)
counterexample and \(x\in F_3(S)\).  Exactly one of the following holds.

1. \(\gamma(G-x)=3\).  Then
   \[
   \gamma(G-x)=\gamma^\infty(G-x)=\theta(G-x)=3.
   \tag{2.5}
   \]
   Every three-clique partition of \(G-x\) meets
   \(N_H(x)\) in all three parts; equivalently, every proper
   three-coloring of \(H-x\) uses all three colors on \(N_H(x)\).
2. \(\gamma(G-x)=2\).  There is a pair \(\{p,q\}\subseteq N_H(x)\)
   whose unique common \(H\)-neighbor is \(x\):
   \[
   N_H(p)\cap N_H(q)=\{x\}.
   \tag{2.6}
   \]

#### Proof

The independent state \(S\) dominates \(G-x\), so
\(\gamma(G-x)\leq3\).  It cannot equal one.  If \(v\) were universal in
\(G-x\) and adjacent to \(x\), it would be universal in \(G\).  If it
missed \(x\), then \(\{v,a\}\) would dominate \(G\), because full-list
membership includes \(ax\in E(G)\).  Both alternatives contradict
\(\gamma(G)=3\).

If \(\gamma(G-x)=3\), Theorem 2.2 gives the eternal equality, and
minimum-order minimality gives \(\theta(G-x)=3\).  If a clique part of a
three-partition of \(G-x\) were complete in \(G\) to \(x\), adjoining \(x\)
to that part would give a three-clique partition of \(G\), a contradiction.
This proves the coloring formulation.

If \(\gamma(G-x)=2\), let \(\{p,q\}\) dominate \(G-x\).  Neither vertex can
be adjacent to \(x\), or the pair would dominate \(G\).  Thus
\(p,q\in N_H(x)\).  A common \(H\)-neighbor of \(p,q\) is exactly a vertex
undominated by the pair in \(G\).  The pair dominates every vertex except
\(x\), proving (2.6). \(\square\)

This is a reduction, not an elimination: neither branch is presently
contradictory.

## 3. Exact extension over the full-list set

The accepted projection-gluing theorem constructs a 2-CNF formula
\(\Phi_S\) when every outside response list has size one or two.  Its
variables orient the connected components of the three frozen-color
bipartitions.  Singleton lists give units, and complement edges joining
distinct two-lists give collision clauses.

Full vertices do not appear in \(\Phi_S\).  They can nevertheless be
separated cleanly from the visible 2-SAT core.

Fix a proper coloring

\[
 f:H[F_3(S)]\longrightarrow S.
\tag{3.1}
\]

For a non-full vertex \(y\notin S\cup F_3(S)\), define the colors forbidden
by its already colored full neighbors:

\[
 C_f(y)=
 \{f(x):x\in F_3(S),\ xy\in E(H)\}.
\tag{3.2}
\]

Augment \(\Phi_S\) as follows.

1. If \(L_S^{\mathcal F}(y)=\{d\}\) and \(d\in C_f(y)\), add the false
   constant.
2. If \(L_S^{\mathcal F}(y)=S-\{u\}\) and
   \(d\in L_S^{\mathcal F}(y)\cap C_f(y)\), add the unit forbidding the
   event that the \(u\)-projection assigns \(d\) to \(y\).

Call the resulting formula \(\Psi_{S,f}\).

### Theorem 3.1 (full-core coloring plus 2-SAT is exact) — PROVED

The coloring \(f\) extends to a family-compatible anchored coloring of all
of \(H\) if and only if \(\Psi_{S,f}\) is satisfiable.

Consequently, a family-compatible anchored coloring exists if and only if
some proper three-coloring \(f\) of \(H[F_3(S)]\) makes
\(\Psi_{S,f}\) satisfiable.

#### Proof

Suppose first that a compatible coloring \(\kappa\) extends \(f\).
Restriction to the non-full vertices orients the frozen projections and
satisfies the original formula \(\Phi_S\).  If a non-full vertex \(y\)
received a color in \(C_f(y)\), it would share that color with an adjacent
full vertex, contradicting properness.  Hence every added constant and unit
is satisfied.

Conversely, let an orientation assignment satisfy \(\Psi_{S,f}\).  The
accepted no-full-list gluing theorem colors every non-full vertex from its
family list and separates:

- anchor--outside edges;
- edges whose endpoints share an omitted color; and
- cross-projection edges between distinct two-lists.

The coloring \(f\) separates all edges internal to \(F_3(S)\).  Every edge
from a full vertex \(x\) to a non-full vertex \(y\) is also separated:
the color \(f(x)\) belongs to \(C_f(y)\), and the added constant or unit
forbids \(y\) from receiving it.  These cases exhaust the edges of \(H\).
Thus the combined coloring is proper and family-compatible. \(\square\)

### Corollary 3.2 (one full vertex means three 2-SAT instances) — PROVED

If

\[
 F_3(S)=\{x\},
\]

then the full response-list coloring problem is decided by the three
formulas

\[
 \Psi_{S,x=a},\qquad
 \Psi_{S,x=b},\qquad
 \Psi_{S,x=c}.
\tag{3.3}
\]

Thus the single-full-vertex slice remains a linear-time 2-SAT decision
after three choices.  For several full vertices, the outer problem is the
proper three-coloring problem on \(H[F_3(S)]\), with an exact 2-SAT oracle
for each proposed coloring.

This theorem localizes the remaining difficulty.  It does not prove that
one of the formulas is satisfiable.

## 4. Forced spoke and external-witness geometry

Now fix a full family-list vertex

\[
 x\in F_3(S).
\tag{4.1}
\]

For \(u\in S\), define its **spoke**

\[
 A_u=N_H(x)\cap N_H(u).
\tag{4.2}
\]

Thus a spoke vertex misses both \(x\) and \(u\) in \(G\).

### Theorem 4.1 (full-list spoke saturation) — PROVED

For every \(u\in S\):

1. \(A_u\ne\varnothing\);
2. every \(p\in A_u\) is adjacent in \(G\) to both members of
   \(S-\{u\}\);
3. the spoke state
   \[
   \{x,u,p\}\in\mathcal F;
   \tag{4.3}
   \]
4. \(G[A_u]\) is a clique.

The three spokes are pairwise disjoint.

#### Proof

The pair \(\{x,u\}\) cannot dominate \(G\), because \(\gamma(G)=3\).
An undominated vertex lies in \(A_u\), proving nonemptiness.

Write \(S=\{u,v,w\}\), and take \(p\in A_u\).  Fullness gives both family
states

\[
 \{u,w,x\}=S-v+x,\qquad
 \{u,v,x\}=S-w+x.
\tag{4.4}
\]

The first state dominates \(p\).  The guards \(u,x\) both miss \(p\), so
\(wp\in E(G)\).  The second state similarly gives \(vp\in E(G)\).

Now attack \(p\) from \(\{u,w,x\}\).  It is unoccupied.  The guards at
\(u,x\) cannot respond, while \(w\) is adjacent to \(p\).  The unique
response \(w\to p\) gives (4.3).

For distinct \(p,q\in A_u\), the state \(\{x,u,p\}\) must dominate \(q\).
The guards \(x,u\) both miss \(q\), so \(pq\in E(G)\).  Hence the spoke is
a clique.

Finally, if \(p\in A_u\cap A_v\) for distinct anchors \(u,v\), then \(p\)
misses \(x,u,v\).  The full state \(S-w+x=\{u,v,x\}\), where \(w\) is the
third anchor, would fail to dominate \(p\).  Thus the spokes are disjoint.
\(\square\)

### Theorem 4.2 (a second clique layer) — PROVED

For \(u\in S\) and \(p\in A_u\), put

\[
 Y_{u,p}=N_H(u)\cap N_H(p)
        =V(G)-N_G[\{u,p\}].
\tag{4.5}
\]

Then:

1. \(Y_{u,p}\ne\varnothing\);
2. \(G[Y_{u,p}]\) is a clique;
3. every \(y\in Y_{u,p}\) is adjacent in \(G\) to \(x\); and
4. every triple
   \[
   \{u,p,y\}\in\mathcal F.
   \tag{4.6}
   \]

In particular, \(Y_{u,p}\) is disjoint from

\[
 S\cup\{x\}\cup N_H(x).
\tag{4.7}
\]

#### Proof

The pair \(\{u,p\}\) does not dominate, so (4.5) is nonempty.  It is an
independent pair in \(G\).  If distinct \(y,z\in Y_{u,p}\) were
nonadjacent, then

\[
 \{u,p,y,z\}
\]

would be an independent four-set, contradicting \(\alpha(G)=3\).
Thus the witness set is a clique.

The forced state \(\{x,u,p\}\) dominates every
\(y\in Y_{u,p}\).  Since \(y\) misses \(u,p\), it must be adjacent to
\(x\).  Finally, \(\{u,p,y\}\) is an independent triple, so the accepted
maximum-independent-state theorem places it in every eternal
three-family, including \(\mathcal F\).

The other anchors are adjacent to \(p\) by Theorem 4.1, so no member of
\(S\) lies in \(Y_{u,p}\).  Adjacency to \(x\) excludes
\(\{x\}\cup N_H(x)\), proving (4.7). \(\square\)

### Corollary 4.3 (analytic order floor for a full target) — PROVED

Any equality graph containing a full family-response target has order at
least nine.

#### Proof

Choose one \(p_u\in A_u\) for each of the three anchors.  The spokes are
disjoint, giving the seven distinct vertices

\[
 S,\quad x,\quad p_a,p_b,p_c.
\]

Each \(Y_{u,p_u}\) is nonempty and lies outside those seven vertices.
One vertex cannot belong to all three witness sets, because it would miss
all of \(S\), making an independent four-set with \(S\).  Hence their union
has at least two vertices. \(\square\)

The bound is not claimed sharp.  The independent finite scan below finds no
full family list even at order nine.

## 5. The forced ridge network in the complement link

Put

\[
 R_x=N_H(x),\qquad J_x=H[R_x].
\tag{5.1}
\]

### Lemma 5.1 (bipartite link with no isolates) — PROVED

The graph \(J_x\) is bipartite and has no isolated vertices.

#### Proof

Apply the accepted independent-antineighborhood projection to the
independent singleton \(\{x\}\).  The induced graph

\[
 G-N_G[x]=G[R_x]
\]

has

\[
 \gamma=\alpha=\gamma^\infty=2.
\]

The accepted parameter-two theorem gives clique-cover number two, so its
complement \(J_x\) is bipartite.

For \(p\in R_x\), the pair \(\{x,p\}\) does not dominate \(G\).
Any vertex undominated by that pair lies in

\[
 N_H(x)\cap N_H(p)=N_{J_x}(p).
\]

Thus \(p\) is not isolated. \(\square\)

Every edge \(pq\in E(J_x)\) makes

\[
 T_{pq}=\{x,p,q\}
\tag{5.2}
\]

an independent triple of \(G\).  Hence every \(T_{pq}\) lies in every
eternal family.

### Theorem 5.2 (componentwise response-role rigidity) — PROVED

Let \(C\) be a connected component of \(J_x\), with fixed bipartition

\[
 U_C\mid V_C.
\tag{5.3}
\]

For \(u\in S\) and an edge \(pq\) with
\(p\in U_C,q\in V_C\), define

\[
 M_{pq}(u)=
 L_{T_{pq}}^{\mathcal F}(u)
 \subseteq\{x,p,q\}.
\tag{5.4}
\]

There is a nonempty signature

\[
 \Sigma_C(u)\subseteq\{X,U,V\}
\tag{5.5}
\]

such that for **every** edge \(pq\) of \(C\),

\[
\begin{aligned}
 x\in M_{pq}(u)&\iff X\in\Sigma_C(u),\\
 p\in M_{pq}(u)&\iff U\in\Sigma_C(u),\\
 q\in M_{pq}(u)&\iff V\in\Sigma_C(u).
\end{aligned}
\tag{5.6}
\]

Moreover:

1. if \(A_u\cap U_C\ne\varnothing\), then
   \[
   U\notin\Sigma_C(u)
   \quad\text{and}\quad
   V\in\Sigma_C(u);
   \tag{5.7}
   \]
2. if \(A_u\cap V_C\ne\varnothing\), then
   \[
   V\notin\Sigma_C(u)
   \quad\text{and}\quad
   U\in\Sigma_C(u);
   \tag{5.8}
   \]
3. consequently, \(A_u\) meets at most one side of \(C\).

#### Proof

The line graph of a connected graph with an edge is connected.  Consider
two consecutive link edges \(pq\) and \(qr\).  The vertices \(p,r\) lie on
the same side of the bipartition, so \(pr\notin E(H)\), equivalently
\(pr\in E(G)\).  Therefore the independent family states

\[
 \{x,p,q\},\qquad \{x,q,r\}
\]

share the ridge \(\{x,q\}\).

The accepted ridge response-covariance theorem transports their complete
response-incidence systems by the transposition \((p\ r)\).  It fixes the
outside attack \(u\), fixes \(x\), fixes the shared-side endpoint \(q\), and
maps the other endpoint to the same bipartition role.  Composing along an
edge path in the line graph proves that the three role-memberships in
(5.6) are independent of the chosen edge.  Closure makes every
\(M_{pq}(u)\) nonempty, proving (5.5).

If \(p\in A_u\cap U_C\), then \(pu\notin E(G)\).  Since \(J_x\) has no
isolates, \(p\) lies on an edge \(pq\).  It cannot respond to the attack at
\(u\) from \(T_{pq}\), so the globally constant \(U\)-role is absent.
The opposite endpoint \(q\) is not in \(A_u\), because Theorem 4.1 makes
\(A_u\) a \(G\)-clique and \(pq\in E(H)\).  Every link vertex misses at
most one anchor, so \(qu\in E(G)\).  The move

\[
 q\to u
\]

has the forced spoke state

\[
 T_{pq}-q+u=\{x,p,u\}\in\mathcal F
\]

as its successor.  Hence the \(V\)-role is present.  The argument with the
two sides interchanged proves item 2.

If \(A_u\) met both sides, items 1 and 2 would say simultaneously that the
\(U\)-role is absent and present.  This proves item 3. \(\square\)

This is a genuinely controlled ridge network forced by one full vertex.
It uses arbitrary-family covariance nonvacuously.

### Theorem 5.3 (cross-spoke separation) — PROVED

Let \(C\) be a component of \(J_x\), with bipartition
\(U_C\mid V_C\).  If \(u,v\in S\) are distinct, then

\[
 A_u\cap U_C\ne\varnothing
 \quad\Longrightarrow\quad
 A_v\cap U_C=\varnothing,
\tag{5.9}
\]

and the analogous statement holds on \(V_C\).

Consequently, a link component meets at most two of the three spokes.  If
it meets two, they lie on opposite sides.

#### Proof

Suppose instead that

\[
 p\in A_u\cap U_C,\qquad q\in A_v\cap U_C
\]

for distinct anchors \(u,v\).  A path between vertices on the same side of
a bipartite graph has even length.  Write one such path as

\[
 p=v_0,v_1,\ldots,v_{2m}=q.
\tag{5.10}
\]

Let \(w\) be the third anchor.  Fullness of \(x\) gives the family state

\[
 D=S-w+x=\{x,u,v\}\in\mathcal F.
\tag{5.11}
\]

First suppose \(m=1\).  Attack \(v_1\) from \(D\).  The guard \(x\)
cannot move because \(xv_1\notin E(G)\).  If \(v\) moved, the successor
\(\{x,u,v_1\}\) would fail to dominate \(p\): all three displayed guards
miss \(p\).  If \(u\) moved, the successor \(\{x,v,v_1\}\) would similarly
fail to dominate \(q\).  No legal response exists, contradicting closure
of \(\mathcal F\).

Now suppose \(m\geq2\).  Attack \(v_1\) from \(D\) again.  The guard \(x\)
cannot move, and a move by \(v\) again gives a state that misses \(p\).
Closure therefore forces

\[
 u\longrightarrow v_1,\qquad
 D_1=\{x,v,v_1\}\in\mathcal F.
\tag{5.12}
\]

The state \(D_1\) must dominate \(v_2\).  Both \(x\) and \(v_1\) miss
\(v_2\), because \(v_2\in R_x\) and \(v_1v_2\in E(J_x)\).  Hence

\[
 vv_2\in E(G).
\tag{5.13}
\]

For \(2\leq i\leq2m\), put

\[
 T_i=\{x,v_{i-1},v_i\}.
\tag{5.14}
\]

Each \(T_i\) is an independent triple of \(G\), hence belongs to every
eternal three-family.  From \(T_2\), the attack at \(v\) admits the
response

\[
 v_2\longrightarrow v,
\]

whose successor is exactly \(D_1\).  Thus

\[
 v_2\in L^{\mathcal F}_{T_2}(v).
\tag{5.15}
\]

Consecutive states \(T_i,T_{i+1}\) share the ridge
\(\{x,v_i\}\), and their ridge transposition exchanges
\(v_{i-1}\) with \(v_{i+1}\).  Response covariance along

\[
 T_2,T_3,\ldots,T_{2m}
\]

fixes the outside attack \(v\) and transports the guard role \(v_2\) to
\(v_{2m}=q\).  It follows that

\[
 q\in L^{\mathcal F}_{T_{2m}}(v).
\tag{5.16}
\]

But response-list membership requires \(qv\in E(G)\), whereas
\(q\in A_v\) says \(qv\notin E(G)\).  This contradiction proves (5.9).

The same argument applies to the other bipartition side.  Theorem 5.2
already makes each individual spoke side-pure.  Since there are only two
sides and no side can contain two distinct spoke types, at most two spoke
types occur in a component, and two occurring types are opposite.
\(\square\)

Theorem 5.3 settles the entire *local* link obstruction.  It still does
not make one of the three global augmented formulas in Corollary 3.2
satisfiable.

## 6. Local anchored-coloring interpretation

Every vertex of \(R_x\) has at most one \(H\)-neighbor in \(S\).  Indeed,
if \(p\in R_x\) had at most one \(G\)-neighbor in \(S\), removing that
neighbor in a full swap \(S-u+x\) would leave \(p\) undominated.

Thus \(R_x\) decomposes as

\[
 R_x=A_a\ \dot\cup\ A_b\ \dot\cup\ A_c\ \dot\cup\ A_\ast,
\tag{6.1}
\]

where vertices of \(A_\ast\) are adjacent in \(G\) to all of \(S\).

Theorem 5.2 puts each nonempty intersection \(A_u\cap C\) on one side of
the component bipartition.  Before using the stronger cross-spoke
separation theorem, the exact abstract three-way obstruction is as follows.
For a component \(C\), define

\[
 \mathcal B_C=
 \bigl\{
 \{u,v\}\subseteq S:
 A_u\cap C,\ A_v\cap C\ne\varnothing
 \text{ and they occupy the same side of }C
 \bigr\}.
\tag{6.2}
\]

The relation “same side” is independent of flipping the component.

### Proposition 6.1 (exact local three-way obstruction) — PROVED

There is an anchored coloring of

\[
 H[S\cup\{x\}\cup R_x]
\]

with \(x\) colored \(w\in S\) if and only if

\[
 S-\{w\}\notin
 \bigcup_C\mathcal B_C.
\tag{6.3}
\]

Consequently, no color works for \(x\) exactly when

\[
 \bigcup_C\mathcal B_C
 =
 \binom S2.
\tag{6.4}
\]

#### Proof

If \(x\) receives anchor color \(w\), every component of \(J_x\) must be
colored with the other two colors \(u,v\).  A vertex in \(A_u\) is forced
to color \(v\), and a vertex in \(A_v\) is forced to color \(u\).
Because each spoke intersection is side-pure, an orientation exists on a
component precisely when the \(A_u\) and \(A_v\) vertices are on opposite
sides whenever both occur.  This is exactly (6.3).  One of the three
choices works exactly when at least one of the three anchor pairs is absent
from the union of bad pairs, proving (6.4). \(\square\)

### Corollary 6.2 (all three colors pass the full-link test) — PROVED

Under the equality and full-family-list hypotheses,

\[
 \bigcup_C\mathcal B_C=\varnothing.
\tag{6.5}
\]

Consequently, for every \(w\in S\), there is an anchored coloring of

\[
 H[S\cup\{x\}\cup R_x]
\]

that gives \(x\) color \(w\).

#### Proof

Theorem 5.3 says that two distinct spoke types never occupy the same side
of a link component.  Thus every \(\mathcal B_C\) is empty.  Proposition
6.1 then applies to each of the three choices of \(w\). \(\square\)

In particular, the marked parity units are consistent on every bipartite
component for every prescribed color of \(x\).

The response-role proof coordinates sides only **within** one connected
component of \(J_x\).  Edge states belonging to distinct link components
share only \(x\), not a two-vertex ridge, so ridge covariance supplies no
canonical comparison between their bipartition labels.  Component flips
remain independent.  Only the same-side/opposite-side relations recorded
in \(\mathcal B_C\) are invariant.

Without Theorem 5.3's eternal-family hypotheses, this local parity
criterion can fail for all three colors.  The smallest abstract example is
a link claw whose three leaves are marked \(a,b,c\), one color per leaf.
The evidence script realizes that local pattern in an eight-vertex graph,
but the realizing graph has \(\gamma=2\) and no eternal three-family.
Thus:

> **REFUTED:** bipartite link geometry and one anchor mark per link vertex
> alone force a local anchored extension.

The cross-spoke separation proof explains exactly why this claw cannot
occur under equality and full closure.  What remains unproved is extension
from the locally colored link through the residual non-full vertices of
\(H\).

## 7. Exact falsification controls

All controls below are recomputed by
`math/working/k3_full_list_slice/probe.py`, which imports no campaign
evaluator.

### 7.1 Genuine full family lists occur under equality

The labeled graph6 record is:

```text
Ksv`f\knJVis
```

It has canonical graph6 identifier:

```text
K{eYptMJynEn
```

At

\[
 S=\{1,2,3\},\qquad x=0,
\]

the independent checker obtains

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3.
\]

All 127 dominating triples survive the greatest fixed point, and

\[
 L_S^{\mathcal K_\ast}(0)=\{1,2,3\}.
\]

Thus a genuine full family list exists under the exact equality hypothesis.
The other response lists are

\[
\begin{array}{c|c}
4&\{1,3\}\\
5&\{1,2\}\\
6&\{2,3\}\\
7,8&\{1,2\}\\
9&\{2,3\}\\
10&\{1,2\}\\
11&\{1,3\}.
\end{array}
\]

Direct list-color enumeration finds exactly one compatible anchored
coloring.  Its clique fibers are

\[
 \{1,5,8,11\}\mid
 \{2,6,7,10\}\mid
 \{0,3,4,9\}.
\tag{7.1}
\]

In particular \(x=0\) receives color \(3\), and the displayed partition
checks \(\theta(G)=3\).

The forced geometry is visible literally:

\[
\begin{array}{c|c|c}
u&A_u&Y_{u,p}\text{ for }p\in A_u\\ \hline
1&\{6\}&Y_{1,6}=\{9\}\\
2&\{11\}&Y_{2,11}=\{4\}\\
3&\{8,10\}&Y_{3,8}=\{7\},\quad Y_{3,10}=\{5\}.
\end{array}
\tag{7.2}
\]

The complement link has two components,

\[
 6-8,\qquad 10-11.
\tag{7.3}
\]

Every spoke is side-pure in each component, as Theorem 5.2 requires.
Both components place their two displayed spoke colors on opposite sides,
so \(\bigcup_C\mathcal B_C=\varnothing\): all three colors pass the **local**
link test.  The global augmented 2-SAT constraints select color \(3\)
uniquely.

Therefore:

> **REFUTED under equality:** every family-response list is proper.

This control also shows that the link criterion alone is not the whole
coloring mechanism; the residual 2-SAT core remains essential.

### 7.2 Equality does not promote static fullness to family fullness

For

\[
 G=\texttt{HCQebjw},\qquad S=\{0,1,2\},\qquad x=8,
\]

the checker obtains

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3.
\]

All three swaps \(S-u+x\) dominate, so

\[
 L_S^{\mathrm{stat}}(8)=S.
\]

The greatest eternal family has 27 states, but

\[
 L_S^{\mathcal K_\ast}(8)=\{1\}.
\]

Its complement link is the path

\[
 5-6-7,
\]

with the three vertices missing anchors \(1,2,0\), respectively.  The
checked clique partition

\[
 \{0,3,6\}\mid\{1,4,8\}\mid\{2,5,7\}
\]

shows the conclusion \(\theta=3\), while the transition kernel itself
selects the unique safe color for \(x\).

Therefore:

> **REFUTED, even under equality:** static full lists automatically survive
> as full family lists.

This graph also shows why Theorem 4.1 needs family fullness: two of the
three spoke states happen to survive, while the spoke state associated
with anchor \(1\) does not.

### 7.3 Proper eternal families can have full lists below equality

The displayed 17-state proper family in

\[
 G=\texttt{FDzro}
\]

passes all 68 state/attack obligations and is a strict subfamily of the
33-state greatest family.  At \(S=\{0,1,2\}\),

\[
 L_S^{\mathcal F}(4)=S.
\]

However,

\[
 (\gamma,\alpha,\gamma^\infty)=(2,3,3).
\]

Only the anchor-\(1\) spoke is nonempty.  This is exactly where the proof of
Theorem 4.1 uses \(\gamma=3\).

Thus:

> **REFUTED outside equality:** arbitrary proper-family closure alone
> eliminates full lists.

### 7.4 A full exchange column is not base-orderability

The probe checks an explicit twelve-state rank-three abstract exchange
system satisfying adversarial target expansion and source restoration.  Its
first target column contains all three sources, but it has no base ordering.

Thus:

> **REFUTED at the abstract exchange level:** a full first-response column
> forces base-orderability.

The displayed system is not claimed to be realized by an equality graph.

## 8. Independent finite scan through order nine

The probe streamed the pinned nauty representative of every connected
unlabeled graph at orders one through nine:

\[
 273{,}193\text{ graphs in total}.
\]

The exact counts were:

\[
\begin{array}{l|r}
\text{predicate}&\text{count}\\ \hline
\gamma=\alpha=3\text{ graphs having a static full incidence}
  &51\\
\text{such static incidences}&61\\
\text{eternal-equality graphs among those 51}&15\\
\text{static full incidences in those 15}&24\\
\text{greatest-family full incidences in those 15}&0.
\end{array}
\]

All 24 equality/static-full incidences had greatest-family response-list
size exactly one.  By Lemma 2.1, the zero greatest-family count also covers
every proper eternal subfamily.

Classification:

- **CERTIFIED-FINITE:** the stated connected-unlabeled universe and exact
  predicate through order nine;
- **OBSERVED PATTERN:** all 24 lists collapse specifically to singletons;
- **NOT CLAIMED:** a universal no-full-list theorem, a new global
  counterexample-order frontier, or any order-ten-and-higher result.

The graph6 stream hashes, pinned generator hash, exact proper-family states,
and all control records are in `probe_result.json`.

## 9. Exact open boundary

The strongest remaining target is:

> Let
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\),
> let \(\mathcal F\) be an arbitrary eternal family of triples, and let
> \(S\) be independent.  If \(F_3(S)=\{x\}\), prove that at least one of
> \[
>  \Psi_{S,x=a},\qquad
>  \Psi_{S,x=b},\qquad
>  \Psi_{S,x=c}
> \]
> is satisfiable, or characterize exactly how all three can be
> unsatisfiable and show that this obstruction is incompatible with the
> eternal-family response system.

Full family lists themselves cannot be eliminated: the order-12 positive
control in Section 7.1 satisfies the equality hypothesis and has one.  In
that graph all three colors pass the local link test, while the residual
2-SAT core selects the unique globally compatible color.  The live issue
is therefore global extension, not existence of the full target.

Any continuation must use at least one feature absent from the controls:

1. rule out the exact global obstruction that all three augmented 2-SAT
   formulas are unsatisfiable;
2. relate the componentwise responder signatures and forced cross-spoke
   separation to implication cycles in the residual 2-SAT core; or
3. combine the three nonempty clique spokes and their external clique
   layers with those implication cycles to force an independent four-set,
   a dominating pair, or a legal recoloring.

A secondary possible route is to prove that some suitably chosen
inclusion-minimal eternal family avoids full lists.  The order-12 control
only refutes this for the greatest family; no pruning theorem is presently
proved.

Merely appealing to static viable swaps is blocked by `HCQebjw`.
Merely appealing to arbitrary-family closure is blocked by the proper
`FDzro` family.  Merely appealing to a full response column is blocked by
the abstract twelve-state exchange system.  Restating the remaining
three-color extension as a coloring problem does not advance the
conjecture; Theorems 3.1, 4.1--4.2, and 5.2 are the exact additional
structure presently available.
