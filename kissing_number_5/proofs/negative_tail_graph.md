# A Forced Negative Tail in Every Hypothetical 41-Code

This note combines the exact antipodal bound with an elementary graph lemma.
It proves a universal restriction on a hypothetical 41-point code, but it
does not by itself rule one out.

## Geometric reduction

Let \(X=\{x_1,\ldots,x_{41}\}\subset S^4\) satisfy
\(\langle x_i,x_j\rangle\leq1/2\) for \(i\ne j\).  Define a graph \(H\) on
\(\{1,\ldots,41\}\) by

\[
ij\in E(H)\quad\Longleftrightarrow\quad
\langle x_i,x_j\rangle<-\frac12.                         \tag{1}
\]

If \(I\) is an independent set in \(H\), then for distinct \(i,j\in I\)

\[
-\frac12\leq\langle x_i,x_j\rangle\leq\frac12.
\]

Consequently \(\{\mathord\pm x_i:i\in I\}\) is an antipodal kissing
configuration of \(2|I|\) distinct points.  Distinctness is worth checking:
if \(x_i=-x_j\), then their inner product is \(-1<-1/2\), so \(ij\) would be
an edge of \(H\).  The exact antipodal bound proved in
[`antipodal_bound.md`](antipodal_bound.md) now gives

\[
\alpha(H)\leq20.                                         \tag{2}
\]

The graph \(H\) is triangle-free.  Indeed, if \(x,y,z\) represented a
triangle, then

\[
\|x+y+z\|^2
=3+2\bigl(\langle x,y\rangle+\langle x,z\rangle
                    +\langle y,z\rangle\bigr)<0,
\]

which is impossible.  The strict inequality in (1) is essential here; pairs
at exactly \(-1/2\) are correctly retained as nonedges.

## Graph lemma

**Lemma.** If a triangle-free graph \(G\) has 41 vertices and
\(\alpha(G)\leq20\), then \(|E(G)|\geq23\).

**Proof.** Let \(I\) be a maximum independent set and put
\(C=V(G)\setminus I\).  Then \(C\) is a minimum vertex cover of size

\[
\tau(G)=41-\alpha(G)\geq21.                               \tag{3}
\]

Because a minimum vertex cover is inclusion-minimal, every vertex of \(C\)
has a neighbor in \(I\).  Thus the number \(b\) of edges between \(C\) and
\(I\) satisfies \(b\geq|C|=\tau(G)\).

Suppose for contradiction that \(|E(G)|\leq22\).  If \(\tau(G)\geq23\),
then already \(b\geq23\), impossible.  If \(\tau(G)=22\), all 22 available
edges must run between \(C\) and \(I\).  The graph is then bipartite, so
Kőnig's theorem gives

\[
\tau(G)=\nu(G)\leq |I|=19,
\]

a contradiction.

It remains to consider \(\tau(G)=21\), so \(|I|=20\).  If \(C\) contains no
edge, the graph is again bipartite and Kőnig's theorem gives
\(\tau(G)\leq20\).  Hence \(C\) contains an edge.  Since \(b\geq21\) and
there are at most 22 edges total, there is exactly one edge \(ab\) inside
\(C\), exactly 21 cross edges, and no other edges.  Every one of the 21
vertices of \(C\) therefore has exactly one neighbor in \(I\).  Let the
unique neighbors of \(a,b\) be \(p,q\), respectively.  Triangle-freeness
implies \(p\ne q\).

Let \(J\subseteq I\) be the set of vertices incident with a cross edge.
It covers every cross edge.  If \(|J|\leq19\), then
\(J\cup\{a\}\) is a vertex cover of all of \(G\) of size at most 20,
contrary to (3).  If \(|J|=20\), the 21 degree-one vertices on the \(C\)
side are distributed among 20 nonempty stars centered at \(J\).  Exactly one
of these stars has two leaves and every other star has one.  Since \(p\ne q\),
at least one of their stars has one leaf; suppose it is the star centered at
\(p\).  Then

\[
(J\setminus\{p\})\cup\{a\}
\]

is a 20-vertex cover: \(a\) covers both \(ap\) and \(ab\), and the remaining
centers cover every other cross edge.  This final contradiction proves the
lemma. \(\square\)

The numerical constant 23 is sharp as a graph-theoretic statement:
\(C_5\sqcup18K_2\) is triangle-free, has 41 vertices and 23 edges, and has
independence number \(2+18=20\).  No claim is made that this graph is
realizable as (1).

## Consequence

Every hypothetical 41-point kissing configuration in \(S^4\) has at least
23 unordered pairs, or 46 ordered pairs, with inner product strictly below
\(-1/2\).

This conclusion is classification-free and uses neither symmetry nor
rigidity.  It is only a necessary condition: a graph satisfying the lemma
need not have a rank-five spherical realization.

## Reproduction

The accompanying standard-library checker verifies the sharp extremal graph,
the relevant integer identities, and the antipodal polynomial certificate:

```sh
python3 verifiers/verify_negative_tail_graph.py
python3 -m unittest tests.test_negative_tail_graph -v
```
