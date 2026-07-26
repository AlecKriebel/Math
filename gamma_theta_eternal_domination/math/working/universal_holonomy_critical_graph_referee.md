# Universal-proof referee: local coloring, line graphs, and holonomy

## Status and claim boundary

This note uses the standard **one-guard-moves** eternal domination model:
attacks occur only at unoccupied vertices, exactly one adjacent guard moves
to the attacked vertex, and every successor configuration dominates.

The status of each result is explicit:

| Item | Status |
|---|---|
| The line-graph local-link theorem (Theorem 1) | **PROVED** |
| The cubic one-guard theorem (Theorem 2) | **PROVED** |
| The diameter-two classification (Theorem 3) | **PROVED** |
| Exclusion of every triangle-free cubic class-II line-graph host (Corollary 4) | **PROVED** |
| Noncanonical-holonomy warning (Proposition 5) | **PROVED** |
| Petersen and odd-cycle parameter records | **EXACT TWO-EVALUATOR OBSERVATION**, pending hostile acceptance |
| Petersen critical-core subset scan | **OBSERVED EXHAUSTIVE FINITE SCAN**, pending hostile acceptance |

No novelty claim is made pending a literature audit.  The proved family
exclusion does not resolve the gamma--theta conjecture: it excludes one
natural obstruction mechanism and shows exactly why a tempting local-to-
global coloring lemma is false.

## 1. The line-graph stress-test family

Let \(F\) be a finite simple triangle-free \(r\)-regular graph, let

\[
 H=L(F),
 \qquad
 G=\overline{H},
\tag{1.1}
\]

and identify vertices of \(H\) and \(G\) with edges of \(F\).  Thus two
vertices are adjacent in \(H\) when their \(F\)-edges intersect, and they are
adjacent in \(G\) when their \(F\)-edges are disjoint.

For \(v\in V(F)\), write \(\delta_F(v)\) for the \(r\) edges incident with
\(v\).  It is a clique of \(H\), hence an independent set of \(G\).

### Theorem 1 (the full local coloring hierarchy survives)

For \(F,H,G\) as in (1.1):

1. \(\omega(H)=r\), and every maximal clique of \(H\) has size \(r\);
2. \(\chi(H)=\chi'(F)\);
3. for every \(t\)-clique \(A\) of \(H\), \(1\leq t<r\),
   \[
   \chi(H[N_H(A)])=\omega(H[N_H(A)])=r-t;
   \tag{1.2}
   \]
4. more precisely, if \(A=\{e\}\) and \(e=uv\), then
   \[
   H[N_H(e)]\cong K_{r-1}\mathbin{\dot\cup}K_{r-1},
   \tag{1.3}
   \]
   while for \(2\leq t<r\),
   \[
   H[N_H(A)]\cong K_{r-t};
   \tag{1.4}
   \]
5. \(G\) is well-covered and
   \[
   i(G)=\alpha(G)=r;
   \tag{1.5}
   \]
6. if \(r\geq3\), then \(F\) has a matching of size at least \(r\), and
   \[
   \gamma(G)\leq3.
   \tag{1.6}
   \]

#### Proof

A pairwise intersecting family of edges in a triangle-free simple graph
shares a common endpoint.  Indeed, if three pairwise intersecting edges do
not share one endpoint, they are the three edges of a triangle.  Every
clique of \(H\) is therefore contained in some star \(\delta_F(v)\).
Regularity makes each such star an \(r\)-clique.  Every smaller star subset
extends inside that star, so the maximal cliques are exactly the
\(\delta_F(v)\), proving item 1.

A proper coloring of \(L(F)\) is exactly a proper edge coloring of \(F\);
this proves item 2.

Fix an edge \(e=uv\).  Its neighbors in \(L(F)\) are the other \(r-1\)
edges at \(u\) and the other \(r-1\) edges at \(v\).  Each group is a
clique.  There is no edge between the groups: such an adjacency would mean
that an edge \(ux\) from the first group and an edge \(vx\) from the second
group share a common third vertex \(x\), giving the triangle \(uvx\) in
\(F\).  This proves (1.3).

Now let \(A\) be a clique of size \(t\geq2\).  Its edges share a center
\(v\).  The \(r-t\) unused edges at \(v\) are common neighbors.  A common
neighbor not incident with \(v\) would have to join the two non-\(v\)
endpoints of two members of \(A\), again creating a triangle.  Thus the
common neighborhood is exactly the remaining \(K_{r-t}\), proving
(1.4), and (1.2) follows.

Independent sets in \(G\) are cliques in \(H\).  Item 1 says that every
maximal such set has size \(r\), proving (1.5).

It remains to prove the matching assertion without importing a matching
theorem.  Let \(M\) be a maximum matching of size \(m\).  If it is perfect,
then for any edge \(uv\), triangle-freeness makes
\[
 \{u,v\},\quad N_F(u)-\{v\},\quad N_F(v)-\{u\}
\]
pairwise disjoint, so \(|V(F)|\geq2r\) and \(m\geq r\).

If \(M\) is not perfect, let \(x\) be unmatched.  Every neighbor of \(x\)
is matched, or its incident edge with \(x\) would augment \(M\).  Moreover,
\(x\) is adjacent to at most one endpoint of each matching edge, since
adjacency to both would form a triangle.  Hence
\[
 r=d_F(x)\leq |M|=m.
\]
Thus \(F\) has three pairwise disjoint edges when \(r\geq3\).  The
corresponding three vertices of \(G\) dominate: no single edge of \(F\)
can intersect all three matching edges.  This proves (1.6). \(\square\)

### Consequence for \(r\geq4\)

If \(F\) is class II, then
\[
 \omega(H)=r<\chi(H)=r+1,
\]
and \(H\) satisfies the entire pure-clique and local-link hierarchy required
of a minimum counterexample complement.  Nevertheless Theorem 1 gives
\[
 \gamma(G)\leq3<r=\alpha(G).
\tag{1.7}
\]

Thus every such host is excluded by the required equality
\(\gamma=\alpha\), before the one-guard game is considered.

## 2. Cubic hosts satisfy the one-guard condition

The cubic case is substantially sharper.  The one-guard condition does not
exclude the class-II hosts.

### Theorem 2 (all dominating triples form an eternal family)

Let \(F\) be finite, simple, triangle-free, and cubic, and let
\(G=\overline{L(F)}\).  Then
\[
 \alpha(G)=\gamma^\infty(G)=3.
\tag{2.1}
\]

More strongly, the family of **all** dominating triples of \(G\) is a
one-guard eternal dominating family.

#### Proof

Theorem 1 gives \(\alpha(G)=3\).  Let \(\mathcal D\) be the set of all
dominating triples.  It is nonempty because each star \(\delta_F(v)\) is a
maximal independent set of \(G\), hence dominates.

Take \(D\in\mathcal D\), and let the unoccupied attacked vertex of \(G\)
correspond to an edge
\[
 s=xy\in E(F)-D.
\]
Because \(D\) dominates \(s\) in \(G\), some edge of \(D\) is disjoint from
\(s\); its guard can move along a \(G\)-edge to \(s\).  We must choose such
a guard so that the successor still dominates.

Let \(q\) be the number of edges of \(D\) incident with \(x\) or \(y\).
Since at least one member of \(D\) is disjoint from \(s\), \(q\leq2\).
Triangle-freeness ensures that no member of \(D\) is incident with both
\(x\) and \(y\).

**Case \(q=2\).**  Move the unique disjoint guard.  If the two retained
edges meet the same endpoint, the successor is the full star at that
endpoint and dominates.  Otherwise they have the form \(xa\) and \(yb\).
An edge meeting \(s=xy\), \(xa\), and \(yb\) would have to be \(xb\) or
\(ya\), producing a triangle with \(s\).  No such edge exists, so the
successor dominates.

**Case \(q=1\).**  Write the unique incident edge as \(xa\), after exchanging
\(x,y\) if necessary, and let \(xb\) be the third edge at \(x\), besides
\(xy\) and \(xa\).  Let the two disjoint guards be \(d_1,d_2\).

If moving \(d_1\) gives a nondominating successor, an outside edge must meet
\(xy,xa,d_2\).  It cannot meet \(xy\) at \(y\), since meeting \(xa\) would
then form a triangle.  It is therefore \(xb\), and \(d_2\) is incident with
\(b\).  Symmetrically, failure after moving \(d_2\) implies that \(d_1\) is
incident with \(b\).  If both moves failed, the outside edge \(xb\) would
meet all three original members \(xa,d_1,d_2\), contradicting that \(D\)
dominates.  At least one move succeeds.

**Case \(q=0\).**  Suppose every one of the three moves failed.  For each
removed edge \(d\in D\), a witness to failure must meet \(xy\) and the other
two edges of \(D\).  Since those other edges are disjoint from \(xy\), they
must share the witness's other endpoint.  Hence every pair of edges in
\(D\) intersects.  In a triangle-free graph the three edges share a common
vertex \(v\), and cubicity gives \(D=\delta_F(v)\).

For two retained edges at \(v\), the only outside edge meeting both is the
removed third star edge: an edge joining their remote endpoints would make
a triangle.  But the removed edge is disjoint from \(xy\) because \(q=0\),
so it cannot witness failure.  This contradiction completes the last case.

Thus every state in \(\mathcal D\) has a legal one-edge, one-guard response
to every unoccupied attack, and every successor remains in \(\mathcal D\).
Therefore \(\gamma^\infty(G)\leq3\).  The general inequality
\(\alpha(G)\leq\gamma^\infty(G)\) proves (2.1). \(\square\)

This proof uses exactly one moving guard and never attacks an occupied
vertex.  It is not an all-guards-move argument.

## 3. The static equality kills every cubic class-II host

### Lemma 3.1 (exact domination dictionary for cubic line graphs)

For triangle-free cubic \(F\) and \(G=\overline{L(F)}\),
\[
 \gamma(G)=3
\quad\Longleftrightarrow\quad
 \operatorname{diam}(L(F))\leq2.
\tag{3.1}
\]
If the diameter exceeds two, then \(\gamma(G)=2\).

#### Proof

Two adjacent edges of \(F\) have the third edge at their common cubic
endpoint as a common neighbor in \(L(F)\).  Two disjoint edges have a common
neighbor in \(L(F)\) exactly when some edge of \(F\) intersects both.
Hence every pair of vertices of \(L(F)\) has a common neighbor exactly when
\(\operatorname{diam}(L(F))\leq2\).

Since \(\omega(L(F))=3\), the accepted pair/common-neighbor dictionary gives
\(\gamma(G)=3\) exactly in this case.  Otherwise a pair with no common
neighbor dominates \(G\).  No singleton dominates because every edge of a
cubic graph intersects another edge, so \(\gamma(G)=2\). \(\square\)

### Theorem 3 (diameter two forces \(K_{3,3}\))

If \(F\) is a finite simple triangle-free cubic graph and
\[
 \operatorname{diam}(L(F))\leq2,
\tag{3.2}
\]
then
\[
 F\cong K_{3,3}.
\tag{3.3}
\]

#### Proof

Fix \(uv\in E(F)\), and write
\[
 A=N_F(u)-\{v\}=\{a_1,a_2\},
 \qquad
 B=N_F(v)-\{u\}=\{b_1,b_2\}.
\]
Triangle-freeness makes the six vertices \(u,v,a_1,a_2,b_1,b_2\)
distinct.  Put \(C=A\cup B\).

Every edge other than \(uv\) has an endpoint in \(C\).  Indeed, an edge
adjacent to \(uv\) has this form directly.  An edge at line-graph distance
two from \(uv\) intersects an edge \(ua_i\) or \(vb_j\), and therefore has
endpoint \(a_i\) or \(b_j\).

Let
\[
 X=V(F)-(\{u,v\}\cup C).
\]
There are no edges inside \(X\), and every vertex of \(X\) has all three
neighbors in \(C\).  Each vertex of \(C\) has one edge to \(u\) or \(v\)
and two remaining degree slots.  Consequently
\[
 3|X|+2|E(F[C])|=8.
\tag{3.4}
\]
It follows that \(|X|=0\) or \(2\).

If \(X=\varnothing\), then \(|E(F[C])|=4\).  There are no edges inside
\(A\) or inside \(B\), as those would make triangles with \(u\) or \(v\).
All four \(A\)--\(B\) edges are therefore present, and the bipartition
\[
 \{u,b_1,b_2\},\qquad \{v,a_1,a_2\}
\]
exhibits \(F\cong K_{3,3}\).

Suppose instead \(X=\{x,y\}\).  Equation (3.4) gives one edge \(pq\)
inside \(C\).  It joins \(A\) to \(B\); write
\[
 p\in A,\quad q\in B,\quad
 r=A-\{p\},\quad s=B-\{q\}.
\]
The endpoints \(p,q\) each have one neighbor in \(X\), while \(r,s\) are
adjacent to both \(x\) and \(y\).  The endpoints \(p,q\) cannot have the
same neighbor in \(X\), since that would form a triangle with \(pq\).
Relabel so that \(px,qy\in E(F)\).

Now the edges \(up\) and \(ys\) are disjoint.  No edge intersects both:
\[
 uy,\ us,\ py,\ ps\notin E(F).
\]
The first is excluded by the definition of \(X\), the second by
triangle \(uvs\), the third by the degree pattern above, and the fourth
because \(pq\) is the unique edge inside \(C\).  Thus these two line-graph
vertices have distance greater than two, contradicting (3.2).  The case
\(|X|=2\) is impossible. \(\square\)

### Corollary 4 (all triangle-free cubic class-II hosts are near-misses)

Let \(F\) be finite, simple, triangle-free, cubic, and class II.  For
\[
 H=L(F),\qquad G=\overline H,
\]
one has
\[
 \boxed{
 \gamma(G)=2
 <
 i(G)=\alpha(G)=\gamma^\infty(G)=3
 <
 \theta(G)=4.
 }
\tag{3.5}
\]

#### Proof

Theorem 1 gives \(i=\alpha=3\), and
\[
 \theta(G)=\chi(H)=\chi'(F)=4.
\]
Theorem 2 gives \(\gamma^\infty=3\).  If \(\gamma=3\), Lemma 3.1 and
Theorem 3 would force \(F\cong K_{3,3}\), which is 3-edge-colorable,
contrary to class II.  Thus \(\gamma=2\). \(\square\)

In particular, this applies to every triangle-free cubic class-II graph,
including every snark under the usual simple triangle-free convention.
The one-guard condition does **not** eliminate this family: it holds with
equality.  The exact obstruction is the static condition
\(\gamma=\alpha\), equivalently the missing common neighbor for some pair
of vertices of \(H\).

## 4. Critical hosts show the opposite failure

Let \(F=C_{2q+1}\), \(q\geq2\).  Then
\[
 H=L(F)\cong C_{2q+1}
\]
is vertex-critical with
\[
 \omega(H)=2<\chi(H)=3.
\]
Its clique complex is pure, and the link of every vertex is a nonempty
independent graph, so the complete \(k=2\) local-link condition holds.
For \(G=\overline H\),
\[
 \gamma(G)=i(G)=\alpha(G)=2
 <\gamma^\infty(G)=\theta(G)=3.
\tag{4.1}
\]

The static equality now holds, but the exact one-guard requirement fails.
This is the complementary failure to (3.5).

Thus neither chromatic criticality nor exact local link colorability
selects the missing target equality:

| host \(H\) | local hierarchy | \(\gamma=\alpha\) | \(\alpha=\gamma^\infty\) | gap |
|---|---:|---:|---:|---:|
| odd cycle \(C_{2q+1}\) | yes | yes | no | \(\omega=2<\chi=3\) |
| \(L(F)\), cubic triangle-free class II | yes | no | yes | \(\omega=3<\chi=4\) |
| \(L(K_{3,3})\) | yes | yes | yes | no gap: \(\omega=\chi=3\) |

The first line is already covered by the accepted \(\alpha=2\) theorem; it
is included here to stress-test the critical-graph mechanism.

## 5. What “holonomy” can rigorously mean here

At a vertex \(v\in V(F)\), a local \(r\)-coloring of the maximal clique
\(\delta_F(v)\) is a bijection
\[
 c_v:\delta_F(v)\longrightarrow [r].
\tag{5.1}
\]
For an edge \(e=uv\), the two maximal cliques
\(\delta_F(u)\) and \(\delta_F(v)\) overlap in the single line-graph vertex
\(e\).  A global \(r\)-coloring exists exactly when the local frames can be
chosen so that
\[
 c_u(e)=c_v(e)
\qquad\text{for every }e=uv.
\tag{5.2}
\]
This is simply the edge-coloring constraint satisfaction problem for \(F\).

### Proposition 5 (there is no canonical permutation holonomy)

For \(r\geq3\), the local clique colorings and their singleton overlaps do
not determine a canonical \(S_r\)-valued transition map, and hence do not
determine a canonical product of color permutations around a cycle.

#### Proof

On the singleton overlap \(\{e\}\), compatibility identifies only the color
assigned to \(e\).  After that color is fixed, there remain
\[
 (r-1)!
\]
permutations of the other colors extending the same overlap identification.
Changing one such extension changes a proposed cycle product while leaving
every local coloring and every restriction to a clique overlap unchanged.
Therefore the product depends on auxiliary transition choices, not only on
the locally colored clique complex. \(\square\)

The sharp invariant is feasibility of the gluing system (5.2), not an
unqualified permutation product.  A future holonomy argument must specify
extra transition data, prove independence from the \((r-1)!\) stabilizer
choices, and then connect the resulting invariant to the one-guard
transition family.  Without those steps, “nontrivial holonomy” is only an
analogy.

## 6. Exact light computation

The independent script
`reviews/universal_holonomy_critical_graph_referee/audit.py` uses both exact
evaluator stacks on named graphs of order at most 15.  It records:

- for the Petersen host,
  \[
  (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,4);
  \]
- all 395 dominating triples survive in both independent greatest closed
  families;
- the explicit host edges \(03\) and \(14\) have no line-graph common
  neighbor and form a dominating pair in \(G\);
- all ten maximal cliques of \(L(F)\) are triangles, every vertex link is
  \(2K_2\), and every edge link is \(K_1\);
- for the \(K_{3,3}\) control,
  \[
  (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3);
  \]
- for the \(C_5,C_7\) critical controls,
  \[
  (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,2,3,3).
  \]

These named-graph values are labeled **EXACT TWO-EVALUATOR OBSERVATION**
until their artifact receives hostile review.

The same script exhausts all induced subsets of \(L(\mathrm{Petersen})\)
through the first order supporting a 4-chromatic vertex-critical core.  It
finds ten such cores, all of order 12, and none preserves either purity or
the full local-link profile.  This is labeled
**OBSERVED EXHAUSTIVE FINITE SCAN**, not a theorem about all critical graphs.

The rigorous warning does not depend on that scan: purity and the exact link
hierarchy are not hereditary under arbitrary vertex deletion, so replacing
\(H\) by an induced chromatic-critical core is unsound unless those
properties are re-established on the core.

## 7. Referee conclusion

The tempting implication
\[
\begin{split}
 &\omega(H)=k<\chi(H),\quad
 \text{pure \(k\)-clique complex},\\
 &\chi(H[N_H(A)])=\omega(H[N_H(A)])=k-|A|
 \text{ for every nonempty clique }A
\end{split}
\]
\[
 \Longrightarrow\quad \chi(H)=k
\]
is false in the strongest possible way: every triangle-free regular
class-II line graph violates its conclusion while satisfying its local
hypotheses.

For cubic hosts, even adding
\[
 \gamma^\infty(\overline H)=\omega(H)=3
\]
does not repair the implication.  The Petersen line graph and Corollary 4
show that the missing condition is \(\gamma(\overline H)=3\), equivalently
the all-pairs common-neighbor condition in \(H\).

The useful universal-proof target is therefore not “local coloring implies
global coloring.”  It must exploit the interaction between:

1. the all-\((k-1)\)-set domination obstruction, which is stronger than
   clique-link colorability;
2. the exact one-guard transition family; and
3. a genuinely defined, gauge-invariant gluing obstruction, if one exists.

The line-graph family is now rigorously closed as a counterexample source,
but the general locally colorable, globally non-\(k\)-colorable mechanism
remains open.
