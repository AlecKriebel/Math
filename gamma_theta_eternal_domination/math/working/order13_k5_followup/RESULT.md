# Independent follow-up on the order-13, parameter-five slice

## Status and claim boundary

This is a working mathematical note, not an accepted campaign claim and not
an exclusion of the order-13, parameter-five slice.  Every theorem below is
conditional on the accepted lower-order frontier C-050 and on the accepted
projection and simplicial-neighborhood results C-051 and C-048.

The main advances over `math/working/order13_k5_structural.md` are:

1. the complete independent-anchor projection hierarchy is made explicit;
2. the clique-cover condition is converted into an exact attachment
   criterion;
3. domination by four vertices is converted into 707 explicit local tests;
4. no-simplicial and degree restrictions are translated exactly to the
   kernel and masks;
5. cluster-graph kernels are excluded;
6. maximum independent sets forced into every one-guard eternal family give
   two exact response-feasibility filters; and
7. these filters show that two six-vertex attachment masks are possible only
   if they are equal.

The last surviving case in item 7 is real: the present argument does not
exclude \(A=B\) with \(|A|=|B|=6\).  No universal or finite-slice resolution
is claimed.

All eternal-domination statements use attacks only at unoccupied vertices
and exactly one guard moving along one edge.

## 1. Standing notation

Assume that \(G\) is an order-13 counterexample with

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=5<\theta(G).
\tag{1.1}
\]

By C-050, \(G\) is a minimum-order counterexample.  C-048 makes \(G\)
connected, nonsimplicial, and of minimum degree at least two.  Reed's bound,
as used and sourced in the preceding working note, forces a degree-two
vertex \(v\).  Write

\[
 N_G(v)=\{a,b\},\qquad ab\notin E(G),
\tag{1.2}
\]

and put

\[
 Q=G-N_G[v],\qquad
 A=N_G(a)\cap V(Q),\qquad
 B=N_G(b)\cap V(Q),\qquad
 R=Q-(A\cup B).
\tag{1.3}
\]

Thus \(|Q|=10\), and the preceding note proves

\[
 \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=\theta(Q)=4
\tag{1.4}
\]

and

\[
 \gamma(R)=\alpha(R)=\gamma^\infty(R)=\theta(R)=3.
\tag{1.5}
\]

For a vertex set \(X\) in a graph \(F\), write
\(N_F[X]=\bigcup_{x\in X}N_F[x]\).

## 2. The complete projection hierarchy

### Theorem 1 (all independent anchors)

For every independent set \(S\subseteq V(G)\) with
\(1\leq |S|\leq4\), the graph

\[
 P_S=G-N_G[S]
\]

is nonempty and well-covered, and

\[
 \gamma(P_S)=\alpha(P_S)=\gamma^\infty(P_S)
 =\theta(P_S)=5-|S|.
\tag{2.1}
\]

#### Proof

C-051 gives every equality except the clique-cover equality.  Since C-050
makes \(G\) a minimum-order counterexample, the minimum-counterexample
corollary of C-051 supplies that equality as well. \(\square\)

The following instances are useful because they expose all currently hidden
mask dependence.

### Corollary 2 (kernel hierarchy)

If \(T\) is an independent \(s\)-set in \(Q\), where \(0\leq s\leq3\),
then

\[
 Q-N_Q[T]
\quad\hbox{has}\quad
 \gamma=\alpha=\gamma^\infty=\theta=4-s.
\tag{2.2}
\]

For \(s=0\), this means \(Q\) itself.

#### Proof

Apply Theorem 1 to the independent set \(\{v\}\cup T\).  Removing
\(N_G[v]\) first leaves \(Q\), and the further deletion inside \(Q\) is
exactly \(N_Q[T]\). \(\square\)

### Corollary 3 (attachment hierarchy)

Put

\[
 S_a=G-N_G[a]=G[\{b\}\cup(Q-A)]
\tag{2.3}
\]

and symmetrically

\[
 S_b=G-N_G[b]=G[\{a\}\cup(Q-B)].
\tag{2.4}
\]

Both graphs are well-covered and have all four parameters equal to four.
Moreover:

1. if \(T\) is an independent \(s\)-set of \(S_a\), \(0\leq s\leq3\),
   then \(S_a-N_{S_a}[T]\) has all four parameters equal to \(4-s\);
2. the symmetric statement holds in \(S_b\);
3. if \(T\) is an independent \(s\)-set of \(R\), \(0\leq s\leq2\),
   then \(R-N_R[T]\) has all four parameters equal to \(3-s\).

In particular, for \(q\notin A\),

\[
 G-N_G[\{a,q\}]
 =
 G\!\left[
   \left(Q-(A\cup N_Q[q])\right)
   \cup
   \begin{cases}
     \{b\},&q\notin B,\\
     \varnothing,&q\in B
   \end{cases}
 \right]
\tag{2.5}
\]

has all four parameters equal to three.  There is a symmetric formula with
\(a,A\) and \(b,B\) interchanged.

#### Proof

The displayed identities follow directly from (1.2)--(1.3).  Apply
Theorem 1 to \(\{a\}\cup T\), \(\{b\}\cup T\), or
\(\{a,b\}\cup T\), respectively. \(\square\)

This hierarchy is a necessary filter on \((Q,A,B)\).  Checking only
\(Q-N_Q[q]\) omits genuine mask-dependent consequences such as (2.5).

## 3. Exact clique-cover criterion

### Theorem 4 (insertion criterion)

Assume only the construction (1.2)--(1.3) and \(\theta(Q)=4\).  Then

\[
 \theta(G)\leq5
\tag{3.1}
\]

if and only if there is a partition

\[
 V(Q)=C_1\mathbin{\dot\cup}C_2\mathbin{\dot\cup}
 C_3\mathbin{\dot\cup}C_4
\tag{3.2}
\]

into four nonempty cliques such that \(C_i\subseteq A\) for some \(i\), or
\(C_i\subseteq B\) for some \(i\).

Consequently,

\[
 \theta(G)=6
\tag{3.3}
\]

if and only if, in every four-clique partition of \(Q\), every part contains
a vertex outside \(A\) and a vertex outside \(B\).

#### Proof

If \(C_i\subseteq A\), then \(C_i\cup\{a\}\), the other three parts, and
\(\{v,b\}\) are five cliques partitioning \(G\).  The argument for \(B\)
is symmetric.

Conversely, suppose \(G\) has a clique partition with at most five parts.
The part containing \(v\) is one of
\(\{v\}\), \(\{v,a\}\), or \(\{v,b\}\), because \(v\) has no neighbor in
\(Q\) and \(a,b\) are nonadjacent.

If that part is \(\{v,a\}\), the at most four remaining parts cover
\(\{b\}\cup Q\).  Their nonempty intersections with \(Q\) form a clique
partition of \(Q\).  Since \(\theta(Q)=4\), there are exactly four such
intersections.  The part containing \(b\) therefore also contains a
nonempty clique \(C_i\subseteq Q\), and \(C_i\subseteq B\).  The
\(\{v,b\}\) case is symmetric.

If the part containing \(v\) is \(\{v\}\), the at most four remaining
parts cover \(\{a,b\}\cup Q\).  Again their intersections with \(Q\) are
exactly four nonempty clique parts.  The vertices \(a\) and \(b\) lie in
different parts, and each is complete to the nonempty \(Q\)-intersection
of its part.  Thus both kinds of insertion exist.

Finally, a four-clique partition of \(Q\), together with
\(\{v,a\}\) and \(\{b\}\), always gives \(\theta(G)\leq6\).  This proves
the equivalence with (3.3). \(\square\)

### Corollary 5 (mask sizes and the role of \(R\))

\[
 1\leq |A|,|B|\leq6,\qquad 3\leq |R|\leq9.
\tag{3.4}
\]

In every four-clique partition of \(Q\), \(R\) meets at least three parts.
If one part \(C\) is disjoint from \(R\), then it must contain a vertex of
\(A-B\) and a vertex of \(B-A\).

#### Proof

The lower bounds on \(|A|\) and \(|B|\) follow from
\(\delta(G)\geq2\), since \(a\) and \(b\) each already have the one
neighbor \(v\).  Equation (1.5) gives \(|R|\geq3\), and
\(A\cup B\ne\varnothing\) gives \(|R|\leq9\).

If \(|Q-A|\leq3\), some part of every four-part partition (3.2) is
contained in \(A\), contradicting Theorem 4 and \(\theta(G)=6\).
Therefore \(|Q-A|\geq4\), or \(|A|\leq6\).  The proof for \(B\) is
symmetric.

Restrict any four-clique partition of \(Q\) to \(R\).  Since
\(\theta(R)=3\), at least three restrictions are nonempty.  If a remaining
part \(C\) misses \(R=Q-(A\cup B)\), then a vertex of \(C-A\) must lie in
\(B-A\), and a vertex of \(C-B\) must lie in \(A-B\).  Theorem 4 requires
both vertices. \(\square\)

## 4. Exact domination and local structural tests

For \(X\subseteq Q\), abbreviate \(N_Q[X]\) by \(D_Q(X)\).  Let
\(\mathcal T=\{a,b,v\}\).

### Theorem 6 (the 707 domination tests)

Assume \(\alpha(Q)=4\) and \(\alpha(R)=3\).  Then \(\alpha(G)=5\) and
\(\gamma(G)\leq5\).  Moreover, \(\gamma(G)=5\) if and only if there is no
pair

\[
 \varnothing\ne C\subseteq\mathcal T,\qquad X\subseteq Q,\qquad
 |C|+|X|\leq4
\tag{4.1}
\]

satisfying all three conditions

\[
 Q\subseteq
 D_Q(X)
 \cup\bigl(A\ \hbox{if }a\in C\bigr)
 \cup\bigl(B\ \hbox{if }b\in C\bigr),
\tag{4.2}
\]

\[
 a\in C\quad\hbox{or}\quad v\in C\quad\hbox{or}\quad X\cap A\ne\varnothing,
\tag{4.3}
\]

and

\[
 b\in C\quad\hbox{or}\quad v\in C\quad\hbox{or}\quad X\cap B\ne\varnothing.
\tag{4.4}
\]

There are exactly

\[
 3\sum_{j=0}^3\binom{10}{j}
 +3\sum_{j=0}^2\binom{10}{j}
 +\sum_{j=0}^1\binom{10}{j}
 =707
\tag{4.5}
\]

such pairs before early rejection.

#### Proof

An independent set containing \(v\) contains neither \(a\) nor \(b\), so it
has size at most \(1+\alpha(Q)=5\).  An independent set containing both
\(a,b\) has its remaining vertices in \(R\), so it has size at most
\(2+\alpha(R)=5\).  If it contains exactly one of \(a,b\), it has at most
four further vertices because it lies otherwise in an induced subgraph of
\(Q\).  If it contains none of \(a,b,v\), it has size at most four.
Conversely, \(\{v\}\cup I\) is an independent five-set for every maximum
independent set \(I\) of \(Q\).  Thus \(\alpha(G)=5\), and such a maximal
independent set dominates \(G\), proving \(\gamma(G)\leq5\).

Every dominating set must meet \(\mathcal T\), because no vertex of \(Q\)
is adjacent to \(v\).  Write it uniquely as \(C\cup X\).  Condition (4.2)
is exactly domination of \(Q\); (4.3) and (4.4) are exactly domination of
\(a\) and \(b\); and \(C\ne\varnothing\) is exactly domination of \(v\).
This proves the characterization.  Counting by \(|C|=1,2,3\) gives
(4.5). \(\square\)

### Proposition 7 (degree and nonsimplicial translation)

Every \(q\in Q\) has

\[
 d_Q(q)\leq6.
\tag{4.6}
\]

The minimum-degree restriction on \(G\) is exactly

\[
 d_Q(q)+{\bf1}_{q\in A}+{\bf1}_{q\in B}\geq2.
\tag{4.7}
\]

The nonsimplicial restriction on \(G\) has the following exact local form.

1. If \(q\in R\), then \(q\) is nonsimplicial in \(Q\).
2. If \(q\in A-B\), then \(q\) is forbidden precisely when
   \(Q[N_Q[q]]\) is a clique and \(N_Q[q]\subseteq A\).
3. If \(q\in B-A\), interchange \(A\) and \(B\) in item 2.
4. If \(q\in A\cap B\), then \(q\) is automatically nonsimplicial in
   \(G\), because its two neighbors \(a,b\) are nonadjacent.

The remaining vertices \(v,a,b\) are automatically nonsimplicial:
\(a,b\) are nonadjacent neighbors of \(v\); since \(A,B\) are nonempty,
\(N_G[a]\) contains the nonadjacent pair consisting of \(v\) and any
vertex of \(A\), and symmetrically for \(b\).

Consequently \(Q\) has at least three nonsimplicial vertices, and \(Q\)
cannot be a cluster graph (a disjoint union of cliques).

#### Proof

Corollary 2 with \(T=\{q\}\) says that \(Q-N_Q[q]\) has independence
number three and hence at least three vertices.  Since \(|Q|=10\), this
gives \(10-(d_Q(q)+1)\geq3\), proving (4.6).

Equation (4.7) is the degree formula in the reconstructed graph.  If
\(q\in R\), it has no neighbor among \(a,b,v\), so
\(N_G[q]=N_Q[q]\).  If \(q\in A-B\), then
\(N_G[q]=N_Q[q]\cup\{a\}\); this is a clique exactly under the two
conditions in item 2.  The other cases follow symmetrically or from
\(ab\notin E(G)\).  Finally, \(|R|\geq3\), while every vertex of a cluster
graph is simplicial. \(\square\)

## 5. Necessary one-guard response filters

The accepted independent-set forcing lemma says that every independent
five-set belongs to every eternal five-family of \(G\).  Merely asking
whether its first successor dominates already gives useful necessary
conditions.

### Theorem 8 (forced-state feasibility)

For every maximum independent set \(I\) of \(Q\), both

\[
 I\cap B\ne\varnothing
 \quad\hbox{or}\quad
 \exists x\in I\cap A:
 A\cup N_Q[I-\{x\}]=Q,
\tag{5.1}
\]

and

\[
 I\cap A\ne\varnothing
 \quad\hbox{or}\quad
 \exists x\in I\cap B:
 B\cup N_Q[I-\{x\}]=Q
\tag{5.2}
\]

must hold.

For every maximum independent set \(J\) of \(R\), at least one of

\[
 B\cup N_Q[J]=Q
\qquad\hbox{and}\qquad
 A\cup N_Q[J]=Q
\tag{5.3}
\]

must hold.

These are necessary domination-feasibility tests, not sufficient
eternality tests.

#### Proof

The independent state \(D=\{v\}\cup I\) belongs to every eternal
five-family.  Under an attack at \(a\), the only possible responding guards
are \(v\) and the vertices of \(I\cap A\).

If \(v\) moves to \(a\), the new state is \(\{a\}\cup I\).  The set \(I\)
already dominates \(Q\), and \(a\) dominates \(v\); this state dominates
\(b\) exactly when \(I\cap B\ne\varnothing\).  If
\(x\in I\cap A\) moves to \(a\), the new state is
\(\{v,a\}\cup(I-\{x\})\).  The vertex \(v\) handles \(a,b\), while
domination of \(Q\) is exactly the second alternative of (5.1).  Some
legal response must have a dominating successor, proving (5.1).
Attacking \(b\) gives (5.2).

Likewise, \(\{a,b\}\cup J\) is an independent five-state forced into every
eternal family.  On an attack at \(v\), only \(a\) or \(b\) can respond.
The move \(a\to v\) leaves \(\{v,b\}\cup J\), which dominates \(Q\)
exactly when the first equality in (5.3) holds.  The move \(b\to v\)
gives the second equality. \(\square\)

## 6. Six-vertex attachment masks

### Lemma 9 (exact residual at a six-mask)

If \(|A|=6\), put \(X=Q-A\), so \(|X|=4\).  Exactly one of the following
holds.

1. \(B-A=\varnothing\), \(R=X\), and \(Q[X]\) consists of one edge and
   two isolated vertices.
2. \(B-A=\{x\}\), \(R=X-\{x\}\), and \(Q[X]\) is edgeless.

The symmetric statement holds when \(|B|=6\).

#### Proof

By Corollary 3, \(S_a=G[\{b\}\cup X]\) has order five and
\(\gamma(S_a)=\alpha(S_a)=\theta(S_a)=4\).  The equality
\(\theta(S_a)=4\) shows that \(S_a\) has at least one edge.  If it had two
distinct edges, then either they meet, say \(xy,xz\), in which case
\(\{x\}\) together with the two vertices outside \(\{x,y,z\}\) dominates
with three vertices, or they are disjoint, in which case one endpoint of
each edge together with the fifth vertex dominates with three vertices.
Both contradict \(\gamma(S_a)=4\).  Hence \(S_a\) has exactly one edge.

Its edges are precisely the edges of \(Q[X]\) together with the edges
\(bq\) for \(q\in B-A\).  Thus \(|B-A|\leq1\).  If it is zero, then
\(R=X\), and the unique edge lies in \(Q[X]\).  If it is one, its
mandatory edge to \(b\) is the unique edge, so \(Q[X]\) is edgeless and
\(|R|=3\). \(\square\)

### Theorem 10 (two six-masks must coincide)

If

\[
 |A|=|B|=6,
\tag{6.1}
\]

then necessarily

\[
 A=B.
\tag{6.2}
\]

In that surviving case, \(|R|=4\) and \(Q[R]\) consists of one edge and
two isolated vertices.

#### Proof

Because \(|R|\geq3\),

\[
 |A\cap B|
 =|A|+|B|-|A\cup B|
 =12-(10-|R|)
 =|R|+2
\]

is at least five.  Hence either \(A=B\), or
\(|A\cap B|=5\) and both differences are singletons.  The first case has
the stated residual structure by Lemma 9.

Suppose the second case occurs.  Write

\[
 B-A=\{x\},\qquad A-B=\{y\}.
\]

Lemma 9 applied in both directions says that both
\(R\cup\{x\}\) and \(R\cup\{y\}\) are independent in \(Q\).  In
particular,

\[
 I=R\cup\{x\}
\]

is a maximum independent four-set of \(Q\), so
\(D=\{v\}\cup I\) is forced into every eternal five-family.

Attack the unoccupied vertex \(b\).  Its only occupied neighbors are
\(v\) and \(x\).  The response \(v\to b\) leaves \(a\) undominated:
\(I\cap A=\varnothing\).  The only remaining response is \(x\to b\),
leaving the state

\[
 \{v,b\}\cup R.
\]

But this state does not dominate \(y\): \(y\notin B\), and
\(R\cup\{y\}\) is independent.  Thus the attacked state has no legal
one-guard response with a dominating successor, contradicting eternality.
The unequal-mask case is impossible. \(\square\)

Theorem 10 is a strict reduction, not an exclusion: the equal-mask branch
\(A=B\), \(|A|=6\), remains open.

## 7. Complete finite enumeration design and coverage proof

The following finite search is materially smaller and safer than a
monolithic order-13, parameter-five adjacency/family formula.

### Kernel stage

Generate one representative of every unlabeled ten-vertex graph \(Q\)
satisfying:

1. the four equalities (1.4);
2. the full kernel hierarchy (2.2);
3. \(\Delta(Q)\leq6\); and
4. at least three nonsimplicial vertices.

A constructive generator may fix an independent four-set
\(\{0,1,2,3\}\), justified by \(\alpha(Q)=4\), impose no independent
five-set, no maximal independent set of size at most three, and no
dominating three-set, and canonicalize completed graphs.  Eternal
domination and every
clique-cover equality must then be checked exactly; fixing the independent
set is only a relabeling device, not a claim that its orbit is unique.

### Attachment stage

For each retained \(Q\), enumerate unordered mask pairs
\(\{A,B\}\) under the diagonal action of

\[
 \operatorname{Aut}(Q)\times\langle A\leftrightarrow B\rangle.
\]

Before quotienting by \(\operatorname{Aut}(Q)\), Corollary 5 leaves exactly

\[
 \frac{465157+847}{2}=233002
\tag{7.1}
\]

unordered pairs with \(1\leq|A|,|B|\leq6\) and
\(|Q-(A\cup B)|\geq3\).  This is only a raw ceiling; the following filters
are much stronger:

1. the exact \(R,S_a,S_b\), and mask-dependent projection hierarchy of
   Corollary 3;
2. the exact clique insertion criterion of Theorem 4;
3. the 707 domination tests of Theorem 6;
4. connectedness, (4.7), and the nonsimplicial tests of Proposition 7;
5. the forced-state tests (5.1)--(5.3);
6. Lemma 9 and Theorem 10; and
7. finally, two independent exact one-guard fixed-point evaluators at
   \(k=5\).

Every survivor must be reconstructed as a 13-vertex graph and checked
without trusting the generator.  Canonical Graph6 deduplication at this
last stage removes duplicates caused by different choices of a degree-two
root.

### Coverage proof

Given any graph satisfying (1.1), Reed plus C-048 supplies a degree-two
vertex \(v\), and its two unordered neighbors give a triple
\((Q,\{A,B\})\) exactly as in (1.2)--(1.3).  Theorems 1--10 prove that this
triple survives every listed necessary filter.  Relabeling \(Q\) maps it to
one generated kernel, and an automorphism of \(Q\), possibly followed by
swapping \(a,b\), maps its masks to the retained orbit representative.
Thus no counterexample orbit is omitted.

Conversely, if a reconstructed survivor is independently verified to have
\(\gamma=\gamma^\infty=5<\theta\), it is a counterexample by definition.
If every orbit is discharged, a manifest of all kernel and mask orbits plus
independently checked coverage and proof artifacts is required before
claiming the order-13, parameter-five slice excluded.

## 8. Exact remaining blocker

No analytic contradiction is known after Theorem 10.  In particular, the
following cases remain live:

1. the false-twin branch \(A=B\) with \(|A|=|B|=6\);
2. one six-mask and one smaller mask satisfying Lemma 9 and Theorem 8; and
3. both masks of size at most five.

The projection hierarchy controls every antineighborhood but does not
provide a converse lift of eternal families or a general extension theorem
for clique partitions.  Closing the slice therefore requires either a new
transition lemma that eliminates these attachment patterns or the complete
canonical enumeration in Section 7.
