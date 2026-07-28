# Terminal hitting, Kempe ears, and cap locations in the single-full \(k=3\) slice

## Status and exact boundary

Date: 2026-07-27 (PDT)

This note uses the standard one-guard-moves eternal domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained state dominates.

The proved conclusions are conditional reductions:

1. if the no-full-list base formula is satisfiable but a prescribed color
   for the unique full vertex fails, one fixed inclusion-minimal core gives
   a fixed hitting set of at most two link terminals for every compatible
   deletion coloring;
2. three failed colors therefore localize every compatible deletion
   coloring to a rainbow transversal in at most six fixed link vertices;
3. the three corresponding one-coordinate family states form a terminal
   cube whose first same-label failure occurs at level two or three;
4. a rainbow triple of singleton link lists is impossible by a direct
   one-guard attack argument;
5. each pairwise Kempe linkage in a critical deletion coloring yields
   either an edge of the complement link with that color pair or a hub-free
   induced odd hole through the full vertex; and
6. every all-dynamic omitted-color connector edge has one of three exact
   cap locations according to whether zero, one, or two of its endpoints
   lie in the complement link.

These statements do **not** prove that one of the three augmented colorings
succeeds.  The remaining gap is an identification theorem: current results
do not force a terminal-cube cross response, which uses a graph edge, to
lie on either a response-2-SAT connector or an ordinary Kempe path, both of
which are assembled from complement edges.

The new lemmas below are proved from the following accepted prerequisites.

- `math/working/k3_projection_gluing.md`: the exact no-full-list 2-SAT
  formula and its equivalence with family-compatible anchored coloring.
- `math/working/k3_full_list_slice/NOTE.md`: vertex deletion, exact
  augmentation over a full vertex, spoke geometry, and the bipartite
  complement link.
- `math/working/k3_twosat_bicycle/NOTE.md`: the inclusion-minimal
  unsatisfiable 2-CNF terminal trichotomy.
- `math/working/full_list_deletion_dichotomy/NOTE.md`: the deletion
  trichotomy, pairwise Kempe linkage, forced cross-part response, and the
  spoke-terminal dominating-pair/\(Z\)-witness fork.
- `math/working/k3_long_bicycle_connectors/NOTE.md`: the odd fan-path
  exclusion.
- `math/working/dynamic_connector_edge_caps/NOTE.md` and
  `math/working/gamma3_port_identification_proof/NOTE.md`: dynamic edge
  caps and positive completeness of a cap.
- `math/lemmas/k3_structural_day1.md`: the induced odd-wheel exclusion.

No finite calculation is promoted to a theorem here.  No claim in this
note resolves the \(k=3\) slice or the universal
\(\gamma\)--\(\theta\) conjecture.

## 1. Setup

Let

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
 \qquad H=\overline G,
\tag{1.1}
\]

let \(\mathcal F\) be an arbitrary specified eternal family of triples, and
let

\[
 S=\{a,b,c\}
\tag{1.2}
\]

be independent.  Every maximum independent triple lies in every eternal
triple-family, so \(S\in\mathcal F\).

For \(y\notin S\), write

\[
 L(y)=L_S^{\mathcal F}(y)
 =\{u\in S:S-u+y\in\mathcal F\}.
\tag{1.3}
\]

Membership on the right already forces \(uy\in E(G)\): the successor must
dominate the omitted anchor \(u\), while the other two anchors do not.

Fix a full response-list vertex

\[
 x\notin S,\qquad L(x)=S,
\tag{1.4}
\]

and put

\[
 R=N_H(x),\qquad
 Z=V(G)-(S\cup\{x\}\cup R).
\tag{1.5}
\]

Thus \(R\) is the complement link of \(x\), while \(Z=N_G(x)-S\).

Sections 2--4 additionally assume that \(x\) is the unique full-list
vertex at \(S\):

\[
 F_3(S)=\{x\}.
\tag{1.6}
\]

Let \(\Phi\) be the accepted no-full-list projection formula for
\((G-x,\mathcal F^{-x},S)\).  For \(w\in S\), assigning color \(w\) to
\(x\) gives

\[
 \Psi_w=\Phi\wedge U_w.
\tag{1.7}
\]

The augmentation \(U_w\) is supported on \(R\).  A vertex
\(r\in R\) with \(L(r)=\{w\}\) gives a false constant.  A two-list vertex

\[
 L(r)=S-\{u\},\qquad w\in L(r),
\tag{1.8}
\]

gives the unit forbidding the port event that assigns color \(w\) to
\(r\).

## 2. A fixed two-terminal hitting certificate

### Theorem 2.1 (fixed terminal hitting) — PROVED

Assume that \(\Phi\) is satisfiable and that \(\Psi_w\) is unsatisfiable
for some \(w\in S\).  There is a fixed set

\[
 T_w\subseteq R,\qquad 1\leq |T_w|\leq2,
\tag{2.1}
\]

such that every family-compatible anchored coloring \(\kappa\) of \(H-x\)
arising from a satisfying assignment of \(\Phi\) satisfies

\[
 \kappa(r)=w
 \quad\text{for some }r\in T_w.
\tag{2.2}
\]

The set \(T_w\) can be chosen once and for all from one fixed
inclusion-minimal unsatisfiable subformula of \(\Psi_w\); it is not
reselected for different satisfying assignments of \(\Phi\).

#### Proof

First suppose that \(U_w\) contains a false constant from a vertex
\(r\in R\) with \(L(r)=\{w\}\).  Every family-compatible coloring assigns
the unique list color \(w\) to \(r\), so \(T_w=\{r\}\) works.

Now suppose that there is no false constant.  Fix one
inclusion-minimal unsatisfiable subformula

\[
 M_w\subseteq\Psi_w.
\tag{2.3}
\]

Because \(\Phi\) is satisfiable, \(M_w\) contains at least one unit from
\(U_w\).  Otherwise \(M_w\subseteq\Phi\), contrary to satisfiability of
\(\Phi\).

The accepted terminal trichotomy says that an inclusion-minimal
unsatisfiable 2-CNF has at most two unit clauses.  Hence the set

\[
 A_w=M_w\cap U_w
\tag{2.4}
\]

has one or two members.  Every member of \(A_w\) is a nonconstant
augmentation unit supported at a two-list vertex \(r\in R\) and forbids
the event \(\kappa(r)=w\).  Let \(T_w\) be the set of their physical
support vertices.  Then

\[
 1\leq |T_w|\leq |A_w|\leq2.
\tag{2.5}
\]

Let \(\kappa\) now be any coloring arising from a satisfying assignment of
\(\Phi\).  If \(\kappa(r)\ne w\) for every \(r\in T_w\), then that
assignment satisfies every augmented unit in \(A_w\).  It also satisfies
every other clause of \(M_w\), since those clauses belong to \(\Phi\).
It would therefore satisfy \(M_w\), contradicting (2.3).  This proves
(2.2) for every satisfying assignment of \(\Phi\), using the one fixed
core \(M_w\). \(\square\)

### Corollary 2.2 (a fixed rainbow terminal skeleton) — PROVED

Assume that \(\Phi\) is satisfiable and all three formulas
\(\Psi_a,\Psi_b,\Psi_c\) are unsatisfiable.  There are fixed sets

\[
 T_a,T_b,T_c\subseteq R,\qquad
 1\leq|T_u|\leq2,
\tag{2.6}
\]

whose union has at most six vertices, such that every compatible deletion
coloring \(\kappa\) admits a choice

\[
 r_u\in T_u,\qquad \kappa(r_u)=u
 \quad(u\in S).
\tag{2.7}
\]

The three chosen vertices \(r_a,r_b,r_c\) are distinct.

#### Proof

Apply Theorem 2.1 separately to the three fixed formulas.  For a given
\(\kappa\), choose one vertex satisfying (2.2) from each \(T_u\).  A
single vertex has one color under \(\kappa\), so vertices selected for
distinct colors are distinct. \(\square\)

This is a logical localization only.  It does not assert that the three
vertices chosen from the fixed sets are independent of \(\kappa\).

## 3. The terminal cube

### Lemma 3.1 (terminal-cube localization) — PROVED

Let \(r_a,r_b,r_c\in R\) be distinct and suppose

\[
 u\in L(r_u)\qquad(u\in S).
\tag{3.1}
\]

For \(I\subseteq S\), define

\[
 D_I=(S-I)\cup\{r_u:u\in I\}.
\tag{3.2}
\]

Then:

1. \(D_\varnothing=S\in\mathcal F\);
2. every one-coordinate state \(D_{\{u\}}\) lies in \(\mathcal F\);
3. \(D_S=\{r_a,r_b,r_c\}\notin\mathcal F\); and
4. along every ordering of the three attacks \(r_a,r_b,r_c\), the first
   absent same-label successor occurs at level two or three, and closure
   forces a guard associated with a different label to respond.

#### Proof

Item 1 is the maximum-independent-state theorem.  Equation (3.1) and the
definition of the family-response list give

\[
 D_{\{u\}}=S-u+r_u\in\mathcal F,
\]

proving item 2.

Every \(r_u\) belongs to \(R=N_H(x)\), so no guard in \(D_S\) is adjacent
to \(x\) in \(G\).  Thus \(D_S\) does not dominate \(x\), proving item 3.

Fix an ordering of \(S\).  Start at \(D_\varnothing\), attack the
corresponding \(r_u\)'s in order, and retain the same-label successor as
long as it belongs to \(\mathcal F\).  The first such successor is always
present by item 2, while the third cannot be present by item 3.  Hence the
first failure is at level two or three.

At a failure \(D_I\to D_{I\cup\{u\}}\), the anchor \(u\) is still
occupied and adjacent to \(r_u\), but its same-label successor is absent.
Eternal closure must retain a response by one of the other two occupied
guards.  Relative to the labels inherited from \(S\), this is a
cross-label response. \(\square\)

Applied to Corollary 2.2, this localizes the accepted cross-part escape to
the fixed union \(T_a\cup T_b\cup T_c\).  The conclusion is stronger than
the earlier arbitrary-choice statement because all three one-coordinate
states are known to be present.  It still gives a move edge in \(G\), not
an edge in \(H\).

### Theorem 3.2 (rainbow singleton link lists are impossible) — PROVED

There do not exist distinct vertices \(r_a,r_b,r_c\in R\) such that

\[
 L(r_a)=\{a\},\qquad
 L(r_b)=\{b\},\qquad
 L(r_c)=\{c\}.
\tag{3.3}
\]

#### Proof

The three direct states

\[
 D_a=\{r_a,b,c\},\quad
 D_b=\{a,r_b,c\},\quad
 D_c=\{a,b,r_c\}
\tag{3.4}
\]

belong to \(\mathcal F\).  Consider

\[
 D_{ab}=\{r_a,r_b,c\}.
\tag{3.5}
\]

Suppose first that \(D_{ab}\notin\mathcal F\).  Attack \(r_b\) from
\(D_a\).  Moving \(b\) produces the absent state \(D_{ab}\).  Moving
\(r_a\), if that graph edge exists, produces

\[
 \{r_b,b,c\}=S-a+r_b,
\]

which is absent because \(a\notin L(r_b)\).  Closure must therefore move
\(c\) and retain

\[
 E=\{r_a,b,r_b\}\in\mathcal F.
\tag{3.6}
\]

Attack the unoccupied anchor \(a\) from \(E\).  The guard at \(b\) cannot
move because \(S\) is independent.  Moving \(r_a\), if possible, produces

\[
 \{a,b,r_b\}=S-c+r_b,
\]

which is absent because \(c\notin L(r_b)\).  Moving \(r_b\) produces
\(S-c+r_a\), absent because \(c\notin L(r_a)\).  Thus \(E\) has no
retained response, a contradiction.

It remains to suppose \(D_{ab}\in\mathcal F\).  Attack \(r_c\).  Moving
the guard at \(c\) produces

\[
 \{r_a,r_b,r_c\},
\]

which does not dominate \(x\).  Closure must therefore move \(r_a\) or
\(r_b\).

If \(r_a\) moves, the retained successor is

\[
 E_a=\{r_b,c,r_c\}.
\]

Attack the unoccupied anchor \(b\).  The guard at \(c\) cannot move.
Moving \(r_b\) produces \(S-a+r_c\), absent because
\(a\notin L(r_c)\), while moving \(r_c\) produces \(S-a+r_b\), absent
because \(a\notin L(r_b)\).  Hence \(E_a\) is impossible.

If \(r_b\) moves, the successor is

\[
 E_b=\{r_a,c,r_c\}.
\]

Attack \(a\).  The two possible nonanchor moves produce \(S-b+r_c\) and
\(S-b+r_a\), both absent.  Thus \(E_b\) is also impossible.  All responses
to the attack at \(r_c\) have been excluded, a contradiction. \(\square\)

### Corollary 3.3 (some failed color has a genuine Boolean core) — PROVED

Assume that \(\Phi\) is satisfiable and all three augmentations fail.
Then at least one \(U_w\) has no false constant.  For that color, every
fixed terminal set obtained in Theorem 2.1 comes from a genuine marked
one-unit lollipop or two-unit chain.

#### Proof

If every \(U_w\) had a false constant, choose
\(r_w\in R\) with \(L(r_w)=\{w\}\).  These vertices are distinct and
contradict Theorem 3.2.  The remaining assertion is the accepted terminal
trichotomy applied exactly as in Theorem 2.1. \(\square\)

## 4. Spoke terminals and a residual witness

For \(u\in S\), recall the spoke

\[
 A_u=N_H(x)\cap N_H(u)
\tag{4.1}
\]

and the dynamically omitted link class

\[
 A_\ast=\{r\in R:r\text{ is adjacent in }G\text{ to all of }S\}.
\tag{4.2}
\]

The accepted terminal geometry says that a two-list terminal

\[
 L(r)=S-\{u\}
\tag{4.3}
\]

lies either in \(A_u\) or in \(A_\ast\).

### Corollary 4.1 (rainbow spoke terminals force two spoke types) — PROVED

In the setting of Corollary 2.2, fix a compatible coloring and a rainbow
transversal \(r_a,r_b,r_c\).  Suppose all three selected vertices have
two-element lists and none lies in \(A_\ast\).  Write

\[
 r_w\in A_{\tau(w)}.
\tag{4.4}
\]

Then:

1. \(\tau(w)\ne w\) for every \(w\);
2. at least two values occur among
   \(\tau(a),\tau(b),\tau(c)\); and
3. some selected pair \(r_i,r_j\) lies on distinct spokes.  That pair
   either dominates \(G-x\) or has a common complement neighbor in \(Z\).
   If \(\gamma(G-x)=3\), the \(Z\)-witness alternative is forced.

#### Proof

Since \(r_w\) is colored \(w\) by a family-compatible coloring,
\(w\in L(r_w)\).  Equation (4.3) therefore gives
\(\tau(w)\ne w\), proving item 1.

If all three values of \(\tau\) were one anchor \(u\), then the equality
\(\tau(u)=u\) would contradict item 1.  This proves item 2 and supplies a
pair on distinct spokes.

The last assertion is precisely the accepted distinct-spoke terminal fork:
such a pair has no common complement neighbor in \(R\), so it either
dominates \(G-x\) or has a common complement neighbor in \(Z\).  A
dominating pair is impossible when \(\gamma(G-x)=3\). \(\square\)

This conclusion does not cover a selected singleton terminal or an
\(A_\ast\) terminal.  It also does not determine the response list of the
new \(Z\)-witness.

## 5. Kempe linkages produce link edges or odd ears

This section uses the minimum-counterexample critical deletion branch.
Assume that

\[
 \theta(G-x)=3,\qquad \theta(G)=4.
\tag{5.1}
\]

Let

\[
 \kappa:V(H-x)\longrightarrow S
\tag{5.2}
\]

be a proper three-coloring, relabeled so that each anchor receives its own
name.  Put

\[
 R_u=R\cap\kappa^{-1}(u).
\tag{5.3}
\]

The accepted criticality theorem says that every \(R_u\) is nonempty and,
for each distinct \(i,j\in S\), some \(\{i,j\}\)-Kempe component meets
both \(R_i\) and \(R_j\).

### Theorem 5.1 (Kempe-ear dichotomy) — PROVED

Fix distinct colors \(i,j\in S\).  At least one of the following occurs.

1. The complement link \(H[R]\) contains an edge whose endpoint colors
   under \(\kappa\) are \(i\) and \(j\).
2. The graph \(H\) contains a hub-free induced odd hole through \(x\),
   and the two neighbors of \(x\) on that hole have colors \(i\) and
   \(j\).

#### Proof

Choose, among all paths in

\[
 (H-x)[\kappa^{-1}(\{i,j\})]
\]

with one endpoint in \(R_i\) and the other in \(R_j\), a path

\[
 P=v_0v_1\ldots v_m
\tag{5.4}
\]

of minimum length.  Such a path exists by the accepted pairwise Kempe
linkage.

The path \(P\) is induced.  Indeed, a chord \(v_pv_q\) with
\(q\geq p+2\) would replace the intervening subpath by one edge and give a
shorter path between the same two endpoint sets.  A proper bichromatic
coloring also rules out a chord between equal-colored vertices.

List in order the vertices of \(R\) that occur on \(P\).  The first has
color \(i\), and the last has color \(j\).  Therefore two consecutive
members \(r,s\) of this list have different colors.  Let \(Q\) be the
\(r\)--\(s\) subpath of \(P\).  By consecutiveness, every internal vertex
of \(Q\) lies outside \(R\).

If \(Q\) has one edge, then \(rs\in E(H[R])\) and alternative 1 holds.
Otherwise, bichromatic alternation and the different endpoint colors make
the length of \(Q\) odd.  It is therefore at least three.

Add \(x\) to \(Q\).  The vertex \(x\) is adjacent in \(H\) to \(r,s\)
and to no internal vertex of \(Q\), by the definition of \(R\).  The path
\(Q\) is induced as a subpath of \(P\), and a possible edge \(rs\) would
also shorten \(P\).  Hence

\[
 H[V(Q)\cup\{x\}]
\tag{5.5}
\]

is an induced cycle.  Its length is the odd length of \(Q\) plus two, so
it is odd and at least five.  The accepted odd-wheel obstruction says
that an induced odd hole in \(H\) has no external vertex complete to its
rim.  Thus the cycle in (5.5) is hub-free, proving alternative 2.
\(\square\)

The theorem applies independently to all three color pairs.  It does not
say that the three witnesses are distinct, that the odd ears stay in one
response projection, or that their endpoints belong to the fixed terminal
sets of Theorem 2.1.

## 6. Where a dynamic connector cap can lie

Fix \(a\in S\), and put

\[
 P_a=\{v\notin S:a\in L(v)\},\qquad
 W_a=\{v\notin S:a\notin L(v)\}.
\tag{6.1}
\]

### Theorem 6.1 (cap-location trichotomy) — PROVED

Let \(y,z\in W_a\) be distinct and suppose

\[
 yz\in E(H),\qquad ay,az\in E(G).
\tag{6.2}
\]

Thus the two omissions of \(a\) are dynamic.  Put

\[
 C_a(yz)=N_H(y)\cap N_H(z).
\tag{6.3}
\]

Then:

1. \(C_a(yz)\ne\varnothing\), every member lies outside \(S\), every
   member belongs to \(P_a\), and \(G[C_a(yz)]\) is a clique.
2. If \(t\in C_a(yz)-\{x\}\), then
   \[
   tx\in E(G).
   \tag{6.4}
   \]
3. If \(y,z\) are not both in \(R\), then \(x\notin C_a(yz)\).  For every
   \(t\in C_a(yz)\), the pair \(\{x,t\}\) has a common complement neighbor
   \(w\), and every such \(w\) satisfies
   \[
   w\in R\cap W_a.
   \tag{6.5}
   \]
4. The location of \(y,z\) gives the following exact split.
   - If \(y,z\in R\), then \(x\in C_a(yz)\); the full vertex itself is
     already a positive cap, and no additional cap or escape is forced.
   - If exactly one endpoint, say \(y\), lies in \(R\), then
     \(y\in N_H(x)\cap N_H(t)\cap W_a\) for every cap \(t\).  The link
     endpoint itself is already an escape.
   - If \(y,z\in Z\), every \(w\) in item 3 is distinct from \(y,z\) and
     is adjacent in \(H\) to at most one of them.

#### Proof

Item 1 is the accepted dynamic connector-cap theorem.  In particular, the
graph-adjacency assumptions in (6.2) exclude the anchor \(a\) itself from
the cap set, so all caps are outside and \(a\)-positive.

Take \(t\in C_a(yz)-\{x\}\).  Both \(t\) and the full vertex \(x\) belong
to \(P_a\).  Positive completeness of a cap says that \(t\) is adjacent in
\(G\) to every other \(a\)-positive vertex.  Applying it to \(x\) proves
(6.4).

The full vertex belongs to \(C_a(yz)\) exactly when both endpoints lie in
\(R=N_H(x)\).  Thus if they are not both in \(R\), every cap differs from
\(x\), and (6.4) holds.  Since \(\gamma(G)=3\), the pair \(\{x,t\}\)
does not dominate.  Equivalently, it has a common complement neighbor

\[
 w\in N_H(x)\cap N_H(t).
\tag{6.6}
\]

The first edge puts \(w\) in \(R\).  If \(a\in L(w)\), then \(w\in P_a\).
It cannot equal \(y\) or \(z\), since both are in \(W_a\), and positive
completeness of the cap \(t\) would give \(tw\in E(G)\), contrary to
(6.6).  Hence \(a\notin L(w)\), proving (6.5).

If \(y,z\in R\), both are complement neighbors of \(x\), so \(x\) is a
cap.  This proves the first location alternative.

If exactly \(y\) lies in \(R\), then \(xy,ty\in E(H)\), because \(t\) is
a cap of \(yz\).  Thus \(y\) itself is a common complement neighbor of
\(x,t\), and \(y\in W_a\) by hypothesis.  This proves the second
alternative.

Finally suppose \(y,z\in Z\).  A common complement neighbor \(w\) of
\(x,t\) cannot equal \(y\) or \(z\), since \(x\) is adjacent to both of
them in \(G\).  If both \(wy,wz\in E(H)\), then all six complement edges
on

\[
 \{t,w,y,z\}
\]

would be present: \(ty,tz,yz\) come from the cap and connector,
\(tw\) comes from (6.6), and \(wy,wz\) are the two assumed edges.  This
would be a \(K_4\) in \(H\), contrary to
\(\omega(H)=\alpha(G)=3\).  Therefore \(w\) sees at most one endpoint,
proving the final alternative. \(\square\)

The \(Z\)--\(Z\) case is the general cap-and-escape step previously proved
for the exact separated-port core.  The other two cases explain why that
step does not automatically iterate along a general connector.

## 7. Combined reduction and exact remaining branches

Suppose now that \(G\) is a minimum-order \(k=3\) counterexample,
\(F_3(S)=\{x\}\), and none of the three augmentations succeeds.

The accepted deletion trichotomy gives three branches.

1. If
   \[
   \gamma(G-x)=2,\qquad\theta(G-x)>3,
   \]
   then \(\Phi\) is necessarily unsatisfiable, because a satisfying
   assignment would give a three-coloring of \(H-x\).  There is no
   deletion three-coloring to which Theorem 5.1 can be applied.
2. If
   \[
   \theta(G-x)=3,\qquad \Phi\text{ is unsatisfiable},
   \]
   then the response obstruction already exists before coloring \(x\).
   In the subbranch \(\gamma(G-x)=3\), the deletion graph has a
   three-clique partition even though the inherited specified family has
   no compatible anchored coloring.
3. If
   \[
   \theta(G-x)=3,\qquad \Phi\text{ is satisfiable},
   \]
   then:
   - Theorem 2.1 supplies at most six fixed terminals;
   - every compatible coloring has a rainbow terminal transversal;
   - Lemma 3.1 forces a cross-label terminal-cube escape at level two or
     three;
   - Theorem 3.2 ensures that at least one failed color has a genuine
     marked lollipop or chain, rather than a false constant;
   - if the selected terminals are two-list spoke vertices and
     \(\gamma(G-x)=3\), Corollary 4.1 supplies a \(Z\)-witness;
   - for each color pair, Theorem 5.1 supplies either a link edge or a
     hub-free odd Kempe ear; and
   - every all-dynamic connector edge obeys Theorem 6.1.

The following bridges remain open.

- A cross-label terminal-cube response is a move along an edge of \(G\).
  Neither the 2-SAT implication walk nor a Kempe path is forced to contain
  that move, since those objects use edges of \(H\).
- An ordinary Kempe swap need not preserve family-response lists, so the
  Kempe-ear endpoints need not belong to a fixed hitting set \(T_w\).
- A \(Z\)-witness from distinct spoke terminals has no currently forced
  response list.
- An all-dynamic connector touching \(R\) already has an escape, and an
  \(R\)--\(R\) connector may use \(x\) as its cap.  Therefore cap
  propagation need not create a new \(Z\)--\(Z\) edge.
- C079 excludes a hub-recurrent odd connector, but Boolean recurrence can
  use separated physical ports.  Longer two-unit chains, multi-clause
  lollipops, repeated or intersecting connectors, and the base-unsatisfiable
  regime remain open.

## 8. Exact \(\gamma=2\) controls

The hypothesis \(\gamma(G)=3\) cannot be weakened to
\(\alpha(G)=\gamma^\infty(G)=3\).

1. **MMV-021.**  The graph `JEhbtj{rv~?` has
   \[
   (\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,4).
   \]
   It has a full greatest-family incidence and no compatible anchored
   coloring.  One color-restricted safe kernel survives, but that kernel
   still has no compatible coloring.  Thus safe-kernel survival alone
   does not prove an augmented coloring.
2. **MMV-001.**  The graph `IEhbtj{ro}` has the same parameter pattern,
   but all three tested restricted kernels at the named full incidence are
   empty.
3. **`GFznc{`.**  Its checked proper eternal family has an unsatisfiable
   no-full-list formula at both ends of a nontrivial independent ridge,
   despite exact response covariance.  It has \(\gamma=2\), so it is a
   boundary control for the base-unsatisfiable branch, not a refutation of
   an equality-specific theorem.
4. **`FDzro`.**  Its proper eternal family has a genuine full target and
   immediate singleton conflicts in \(R\) for one target color, while the
   other two colors extend.  This is consistent with Theorem 3.2: the
   graph does not have singleton blockers of all three colors.
5. **`HFzvvn{`.**  Its 65-state family realizes an
   augmentation-sensitive one-unit lollipop with separated physical
   ports.  The graph has \(\gamma=2\).  A dynamic connector edge has no
   common complement neighbor, so the first cap conclusion in
   Theorem 6.1 fails exactly at the missing domination equality.

There is also an important deletion-\(\gamma=2\) equality control.  The
order-12 graph with canonical record `K{eYptMJynEn` has

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=\theta(G)=3
\]

and a genuine full greatest-family list, but

\[
 \gamma(G-x)=2,\qquad\theta(G-x)=3.
\]

Two augmentations fail through two-unit chains whose terminal pairs
dominate \(G-x\), while the third augmentation succeeds.  Thus the
\(\gamma(G-x)=2\) side of the accepted terminal fork is sharp and cannot
simply be discarded.

## 9. Claim boundary

The genuinely new proved deductions in this note are:

- Theorem 2.1 and Corollary 2.2: fixed two-terminal hitting and the fixed
  six-vertex rainbow skeleton;
- Lemma 3.1: terminal-cube localization at levels two and three;
- Theorem 3.2 and Corollary 3.3: rainbow singleton exclusion and the
  existence of at least one genuine Boolean failed-color core;
- Corollary 4.1: the rainbow-spoke consequence;
- Theorem 5.1: the Kempe-ear dichotomy; and
- Theorem 6.1: the cap-location trichotomy.

The deletion trichotomy, pairwise Kempe linkage, arbitrary cross-part
escape, terminal trichotomy, distinct-spoke witness fork, odd fan-path
exclusion, dynamic cap theorem, and positive cap completeness are imported
accepted prerequisites, not new claims here.

No statement proves that one of the three augmented colorings succeeds.
The exact unresolved task is to identify one of the fixed terminal-cube
objects with a forbidden physical 2-SAT/Kempe/cap configuration, or to
rule out finite recurrence of the remaining separated-port and
base-unsatisfiable branches.
