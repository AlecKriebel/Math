# Dynamic connector caps in the single-full \(k=3\) branch

## Status and exact boundary

Date: 2026-07-27 (PDT)

All statements use the standard one-guard-moves eternal domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained state dominates.

The accepted prerequisites used below are:

- maximum independent triples belong to every eternal triple-family
  (`math/lemmas/maximum_independent_states.md`);
- the two dead-state lemmas and odd fan-path theorem
  (`math/working/k3_long_bicycle_connectors/NOTE.md`); and
- the full-list link geometry
  (`math/working/k3_full_list_slice/NOTE.md`).

The outcomes are:

1. **PROVED:** every complement edge whose two endpoints dynamically omit
   one response color has a nonempty clique of common complement-neighbors,
   and every such neighbor has that omitted color in its response list.
2. **PROVED:** each such triangle cap is adjacent in \(G\) to every other
   vertex having the recovered response color.  This is a direct
   length-one application of the accepted odd fan-path theorem.
3. **PROVED:** in the exact separated-port geometry of `HFzvvn{`,
   \(\gamma=3\) forces two new vertices: a positive cap in the residual
   \(G\)-neighborhood of the full vertex, followed by an omitted-color
   witness in its complement link.  The second witness cannot see both
   connector endpoints in the complement, by \(K_4\)-freeness.  In
   particular, this exact pattern requires at least eleven vertices.
4. **OBSERVED:** all \(2^{19}=524{,}288\) labeled two-vertex extensions
   preserving the exact old induced complement were scanned.  Six satisfy
   the static conditions \(\gamma=\alpha=3\), but their eternal
   three-kernels are empty.  A clean-room implementation independently
   replayed the complete scope and conclusion.  This bounded diagnostic is
   retained as `OBSERVED`, not promoted to a counterexample-order exclusion
   or general theorem.

The result does **not** prove that a separated-port lollipop is impossible
under \(\gamma=3\), and it does not prove physical terminal-port
recurrence.  It identifies the exact next layer that any proof must handle:
the forced cap-and-escape ladder in Sections 3--4.

## 1. Setup and notation

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

be independent.  Then \(S\in\mathcal F\).

For \(v\notin S\), write

\[
 L(v)=L_S^{\mathcal F}(v).
\tag{1.3}
\]

For one fixed anchor \(a\), put

\[
 P_a=\{v\notin S:a\in L(v)\},
 \qquad
 W_a=\{v\notin S:a\notin L(v)\}.
\tag{1.4}
\]

Thus \(P_a\) records actual retained direct responses, not merely graph
adjacency.  No argument below converts membership in \(W_a\) into a graph
nonedge.

The accepted dead-state lemmas say:

\[
 \{h,y,z\}\notin\mathcal F
 \quad
 (h\in\{b,c\},\ y,z\in W_a\text{ distinct}),
\tag{1.5}
\]

and

\[
 \{y,z,t\}\notin\mathcal F
 \quad
 (y,z,t\in W_a\text{ distinct}).
\tag{1.6}
\]

## 2. Triangle-cap propagation

### Theorem 2.1 (dynamic connector-cap lemma) — PROVED

Let \(y,z\in W_a\) be distinct and suppose

\[
 yz\in E(H),
 \qquad
 ay,az\in E(G).
\tag{2.1}
\]

Define the common complement-neighborhood

\[
 C_a(yz)=N_H(y)\cap N_H(z).
\tag{2.2}
\]

Then:

1. \(C_a(yz)\ne\varnothing\);
2. \(C_a(yz)\cap S=\varnothing\);
3. \(C_a(yz)\subseteq P_a\); and
4. \(G[C_a(yz)]\) is a clique.

#### Proof

Because \(\gamma(G)=3\), the pair \(\{y,z\}\) does not dominate \(G\).
Hence some vertex is missed by both guards, equivalently
\(C_a(yz)\ne\varnothing\).

Take \(t\in C_a(yz)\).  The graph edges in (2.1) exclude \(t=a\).  If
\(t=b\) or \(t=c\), then

\[
 \{t,y,z\}
\]

is an independent triple of \(G\).  Since \(\alpha=\gamma^\infty=3\), the
maximum-independent-state theorem puts it in every eternal triple-family,
including \(\mathcal F\).  This contradicts (1.5).  Therefore
\(t\notin S\).

The three complement edges among \(t,y,z\) make
\(\{t,y,z\}\) an independent triple of \(G\), so it belongs to
\(\mathcal F\).  If \(a\notin L(t)\), then all three vertices lie in
\(W_a\), and (1.6) says that the same state is absent.  Thus
\(a\in L(t)\), proving \(t\in P_a\).

Finally, if two distinct members \(t,t'\in C_a(yz)\) were adjacent in
\(H\), then

\[
 H[\{y,z,t,t'\}]=K_4,
\]

contradicting \(\alpha(G)=\omega(H)=3\).  Thus every two cap vertices are
adjacent in \(G\), proving item 4. \(\square\)

The graph-adjacency assumptions \(ay,az\in E(G)\) are essential only to
exclude the anchor \(a\) itself as a common complement-neighbor.  They
hold for the dynamic omissions in the separated-port control.

### Theorem 2.2 (positive completeness of a cap) — PROVED

Under the hypotheses of Theorem 2.1, let

\[
 t\in C_a(yz)
\]

and let \(p\in P_a\) be distinct from \(t,y,z\).  Then

\[
 pt\in E(G).
\tag{2.3}
\]

Equivalently, every cap \(t\) is \(G\)-complete to

\[
 P_a-\{t\}.
\tag{2.4}
\]

#### Proof

Suppose instead that \(pt\in E(H)\).  Apply the accepted odd fan-path
theorem with:

\[
 \text{positive vertex }p,\qquad
 \text{hub }t,\qquad
 \text{path }y-z,
\]

and omitted color \(a\).  The four vertices are distinct by hypothesis.
We have

\[
 a\in L(p),\qquad
 a\notin L(y)\cup L(z),
\]

and all four required complement edges

\[
 pt,\quad ty,\quad tz,\quad yz
\]

are present.  This is the forbidden odd fan with path length one, a
contradiction.  Therefore \(pt\in E(G)\). \(\square\)

This theorem is the useful interaction between the new \(\gamma=3\)
completion and the pre-existing one-guard attack argument.  The cap is not
just a static common neighbor: its recovered response color makes it
incompatible, in the complement, with every other positive-response
vertex.

## 3. The exact separated-port core

Use the labels

\[
 S=\{a,b,c\},\qquad
 x,r,s,q,v_0,v_1\notin S,
\tag{3.1}
\]

where \(s\) is the middle vertex formerly denoted \(t\) in the
`HFzvvn{` control.  Assume:

\[
\begin{aligned}
 &L(x)=S,\\
 &a\in L(r)\cap L(s)\cap L(q),\\
 &a\notin L(v_0)\cup L(v_1),
\end{aligned}
\tag{3.2}
\]

and that the six outside vertices induce in \(H\) exactly the tail-plus-
cycle edges

\[
 xr,\ rs,\ sq,\ qv_1,\ v_1v_0,\ v_0r.
\tag{3.3}
\]

Also assume

\[
 av_0,av_1\in E(G),
\tag{3.4}
\]

as in the exact control.  Equations (3.2)--(3.4) retain the
separated-port one-unit lollipop:

- \(r-s-q\) is the even connector carrying one Boolean orientation;
- \(v_0-v_1\) is the odd connector carrying the other orientation; and
- the terminal cross edges are \(rv_0\) and \(qv_1\), with different
  physical ports \(r,q\).

### Corollary 3.1 (forced residual cap) — PROVED

There is a vertex

\[
 z\notin S\cup\{x,r,s,q,v_0,v_1\}
\tag{3.5}
\]

such that

\[
 zv_0,zv_1\in E(H),
 \qquad
 a\in L(z),
\tag{3.6}
\]

and

\[
 zx,zr,zs,zq\in E(G).
\tag{3.7}
\]

In the notation of the single-full deletion slice,

\[
 z\in N_G(x)-S.
\tag{3.8}
\]

#### Proof

Apply Theorem 2.1 to the dynamic omitted-color edge \(v_0v_1\).
It supplies \(z\in C_a(v_0v_1)\subseteq P_a\).

No anchor can be \(z\), by Theorem 2.1.  The exact induced pattern (3.3)
shows that none of \(x,r,s,q\) sees both \(v_0,v_1\) in \(H\), so \(z\)
is new.  Theorem 2.2 applies to each of the distinct positive vertices
\(x,r,s,q\), proving (3.7). \(\square\)

Thus \(\gamma=3\) does not directly identify the separated terminal
ports.  Its first forced move is to place a new positive cap on the odd
connector, and the odd fan theorem pushes that cap out of the complement
neighborhood of all four old positive vertices.

## 4. The forced escape from the cap

### Theorem 4.1 (cap-and-escape ladder) — PROVED

Under the hypotheses of Section 3, every cap \(z\) from Corollary 3.1 has
a vertex

\[
 w\notin
 S\cup\{x,r,s,q,v_0,v_1,z\}
\tag{4.1}
\]

such that

\[
 wx,wz\in E(H),
 \qquad
 a\notin L(w).
\tag{4.2}
\]

Moreover,

\[
 \{wv_0,wv_1\}\nsubseteq E(H);
\tag{4.3}
\]

that is, \(w\) is adjacent in \(H\) to at most one of the two connector
endpoints.  In full-list notation,

\[
 w\in N_H(x)\cap W_a,
 \qquad
 z\in N_G(x)-S.
\tag{4.4}
\]

#### Proof

Equation (3.7) gives \(xz\in E(G)\).  Since \(\gamma(G)=3\), the pair
\(\{x,z\}\) does not dominate.  Hence it has a common complement-neighbor
\(w\), proving the two edges in (4.2).

Fullness of \(x\) implies that \(x\) is adjacent in \(G\) to all three
anchors, so \(w\notin S\).  The vertex \(w\) cannot be one of
\(r,s,q\), because (3.7) makes each of those adjacent to \(z\) in \(G\).
It cannot be \(v_0\) or \(v_1\), because the exact induced pattern (3.3)
makes each adjacent to \(x\) in \(G\).  It is also distinct from \(x,z\).
This proves (4.1).

If \(a\in L(w)\), then \(w\in P_a-\{z\}\).  The positive-completeness
Theorem 2.2 would give \(wz\in E(G)\), contradicting the defining
complement edge \(wz\).  Hence \(a\notin L(w)\).

Finally, if both \(wv_0,wv_1\) were complement edges, then all six
complement edges on

\[
 \{z,w,v_0,v_1\}
\]

would be present: \(zv_0,zv_1,v_0v_1\) come from the cap, and \(zw\) and
the two assumed edges complete a \(K_4\).  This contradicts
\(\omega(H)=3\), proving (4.3). \(\square\)

### Consequence

The first mandatory \(\gamma=3\) completion is therefore not the hoped-for
common fan hub.  It has the following alternating form:

\[
 \underbrace{v_0v_1}_{W_a\text{ edge}}
 \quad\longrightarrow\quad
 \underbrace{z}_{P_a\text{ residual cap}}
 \quad\longrightarrow\quad
 \underbrace{w}_{W_a\text{ link escape}}.
\tag{4.5}
\]

The escape \(w\) cannot close onto both ends of \(v_0v_1\).  This does not
refute a more global port-recurrence theorem: another vertex or a longer
link walk could still produce the missing physical hub.  It proves that
such recurrence is not the immediate consequence of adding the
common-neighbor required by \(\gamma=3\).

### Corollary 4.2 (exact-pattern order floor) — PROVED

Every equality realization of the exact separated-port core in Section 3
has at least eleven vertices.

#### Proof

The setup contains the nine distinct vertices

\[
 S\cup\{x,r,s,q,v_0,v_1\}.
\]

Corollary 3.1 forces a new vertex \(z\), and Theorem 4.1 forces a further
vertex \(w\) distinct from all nine and from \(z\). \(\square\)

The full-link theorem also says that \(w\), as a vertex of \(N_H(x)\), has
a neighbor in the bipartite graph \(H[N_H(x)]\).  The new unresolved
question is whether iterating that link edge with Theorems 2.1--2.2 must
eventually create:

- an odd fan already excluded by C079;
- a complement \(K_4\);
- a dominating pair; or
- a finite alternating cycle compatible with all response roles.

No answer to that global iteration is claimed here.

## 5. Bounded exact diagnostic

The script

```text
two_vertex_extensions.py
```

enumerates every labeled extension of the exact nine-vertex induced
complement by two new vertices.  There are

\[
 2^{9+9+1}=524{,}288
\tag{5.1}
\]

choices.

For each extension it tests:

1. \(H\) has no \(K_4\), while the anchor triangle gives
   \(\omega(H)=3\);
2. every vertex pair has a common \(H\)-neighbor, which is equivalent to
   \(\gamma(G)\geq3\);
3. the greatest eternal triple-kernel by literal simultaneous deletion;
4. the old six response lists at \(S\).

The deterministic output is
`two_vertex_extensions_result.json`.  Exactly six extensions satisfy the
static equality \(\gamma=\alpha=3\).  In all six, the entire eternal
triple-kernel is empty, and the reference state \(S\) is deleted in round
two.  Thus no exact two-vertex extension realizes eternal equality.

Classification: **OBSERVED bounded falsification.**  The clean-room
addendum in `reviews/separated_port_gamma3_extensions_hostile/`
independently decodes all \(524{,}288\) cases, reproduces the six static
survivors, and confirms that each entire triple kernel is empty with the
reference state deleted in round two.  The conservative label reflects the
deliberately local diagnostic scope.  It does not cover extensions with
three or more vertices, graphs in which one of the old induced nonedges is
changed, or a longer separated-port realization.

The auxiliary `sat_extension_search.py` encodes the same graph/family
conditions directly from the one-guard definition.  It was used only as a
bounded discovery probe.  Its finite negative runs are not mathematical
claims and are deliberately not used in Sections 2--4.

## 6. Exact stopping boundary

The useful new theorem is the cap-completeness mechanism:

> A dynamically omitted connector edge cannot remain untriangulated under
> \(\gamma=3\).  Every triangle cap recovers the omitted response color,
> and the one-guard odd-fan exclusion makes that cap \(G\)-complete to all
> other vertices with that response color.

For the exact separated lollipop, this forces the residual-cap/link-escape
pair \((z,w)\), but \(K_4\)-freeness prevents \(w\) from being the desired
common terminal hub.  The next serious proof target is therefore the
finite iteration of these cap-and-escape steps inside the bipartite link,
not an unsupported contraction of the even connector or an inference from
dynamic list omission to graph nonadjacency.

No result in this note resolves the \(k=3\) slice or the universal
\(\gamma\)--\(\theta\) conjecture.
