# Core reductions for the \(\gamma\)–\(\theta\) conjecture

## Status and scope

This note uses the **one-guard-moves** model in the campaign statement:
an attack is made only at an unoccupied vertex, and exactly one guard moves
along one edge to the attacked vertex.  No assertion below concerns the
all-guards-move parameter.

Except for an explicitly identified use of the Strong Perfect Graph Theorem
(SPGT), the arguments below are from the definitions.  The graph-class
restrictions (planar, subcubic, triangle-free, and so on) are deliberately
quarantined in `class_restrictions_pending.md` until their primary sources and
exact hypotheses have been checked.

Graphs are finite, simple, and undirected.  We assume \(V(G)\ne\varnothing\)
when discussing \(\gamma^\infty(G)\).  This avoids an irrelevant convention for
the empty graph; the full occupied set \(V(G)\) always shows that
\(\gamma^\infty(G)\) exists.

For a fixed \(k\), write

\[
 D \xrightarrow{r} D'
\]

when \(r\notin D\), there is a vertex \(u\in D\cap N(r)\), and
\(D'=(D-\{u\})\cup\{r\}\).  An eternal dominating family is thus a nonempty
family of dominating \(k\)-sets that has at least one outgoing
\(r\)-transition for every allowed attack \(r\).

## 1. Forcing guards onto an independent set

The following elementary lemma is the delicate part of the lower bound
\(\alpha\leq\gamma^\infty\).

**Lemma 1 (independent-set forcing).**  Let \(\mathcal F\) be an eternal
dominating family of \(k\)-sets in \(G\), and let \(I\) be an independent set.
Starting from any \(D\in\mathcal F\), the attacker can, by attacking only
currently unoccupied vertices of \(I\), reach a member \(D'\in\mathcal F\)
such that

\[
 |D'\cap I|=\min\{|I|,k\}.
\]

In particular, if \(|I|=k\), then \(I\in\mathcal F\).

**Proof.**  Suppose that \(r\in I-D\) is attacked.  The response moves a guard
from some \(u\in D\cap N(r)\) to \(r\).  Since \(I\) is independent, \(u\)
cannot be a different vertex of \(I\).  Consequently this move increases
\(|D\cap I|\) by exactly one.  Repeat while there is an unoccupied vertex of
\(I\) and fewer than \(k\) guards in \(I\).  Every attack is allowed, every
resulting configuration remains in \(\mathcal F\), and the process terminates
with the asserted number of guards in \(I\).  If \(|I|=k\), the final
\(k\)-set is exactly \(I\). \(\square\)

Notice that the argument never attacks an occupied vertex.  It also uses the
fact that only one guard moves: a guard already placed in \(I\) cannot be moved
away during this attack sequence.

## 2. The parameter chain

**Theorem 2.**  For every nonempty finite simple graph \(G\),

\[
 \boxed{\gamma(G)\leq i(G)\leq\alpha(G)
        \leq\gamma^\infty(G)\leq\theta(G).}
\]

**Proof.**

1. An independent set is maximal if and only if it is dominating.  Indeed, if
   an independent set \(M\) is not dominating, some vertex outside \(M\) has no
   neighbor in \(M\), and that vertex can be added to \(M\).  Conversely, if
   \(M\) is not maximal, a vertex can be added to it and hence is not dominated
   by \(M\).  Thus every maximal independent set is a dominating set, giving
   \(\gamma(G)\leq i(G)\).

2. A maximum independent set is maximal.  Since \(i(G)\) is the minimum size
   of a maximal independent set, \(i(G)\leq\alpha(G)\).

3. If an eternal family has \(k\) guards, apply Lemma 1 to a maximum
   independent set \(I\).  If \(|I|>k\), Lemma 1 reaches a configuration
   whose \(k\) guards all lie in \(I\).  Choose \(r\in I-D\).  Since \(I\)
   is independent, \(D\cap N(r)=\varnothing\), contradicting the required
   response to the unoccupied attack at \(r\).  Hence
   \(k\geq|I|=\alpha(G)\).  Minimizing over eternal families yields
   \(\alpha(G)\leq\gamma^\infty(G)\).

4. Let \(C_1,\ldots,C_t\) be a partition of \(V(G)\) into cliques.  Put one
   guard in each \(C_j\), and let \(\mathcal T\) be the family of all
   configurations having exactly one guard in each part.  Every member of
   \(\mathcal T\) dominates \(G\): each vertex is either occupied or adjacent
   to the guard in its own clique.  If an unoccupied \(r\in C_j\) is attacked,
   move the unique guard of \(C_j\) to \(r\); this is one move along an edge
   and the result is again in \(\mathcal T\).  Hence
   \(\gamma^\infty(G)\leq t\), and minimizing the clique partition gives
   \(\gamma^\infty(G)\leq\theta(G)\). \(\square\)

The proof of the last inequality uses a **partition** into cliques and keeps
one guard assigned to each part.  No simultaneous guard movement is hidden in
the argument.

## 3. Equality collapse and well-coveredness

**Corollary 3 (equality collapse).**  If
\(\gamma(G)=\gamma^\infty(G)=k\), then

\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=k.
\]

**Proof.**  Every term between the equal endpoints in Theorem 2 must equal
those endpoints. \(\square\)

**Corollary 4.**  If \(\gamma(G)=\gamma^\infty(G)\), then \(G\) is
well-covered.

**Proof.**  Corollary 3 gives \(i(G)=\alpha(G)\).  Every maximal independent
set has size at least \(i(G)\) and at most \(\alpha(G)\), so all maximal
independent sets have the same size. \(\square\)

The converse is false, and well-coveredness must never replace the explicit
condition \(\gamma=\alpha\) in a search target.  For example, \(K_{3,3}\) is
well-covered: its only maximal independent sets are its two partite sets, both
of size \(3\).  Nevertheless

\[
 \gamma(K_{3,3})=2<3=i(K_{3,3})=\alpha(K_{3,3}).
\]

There is a second, stronger warning.  Even “well-covered and
\(\gamma=\alpha\)” does not imply \(\gamma=\gamma^\infty\).  The graph \(C_5\)
is well-covered and has \(\gamma(C_5)=\alpha(C_5)=2\), but Section 6 below
proves \(\gamma^\infty(C_5)=3\).

When the equality collapse does hold, Lemma 1 gives an additional useful
fact: every maximum independent set occurs as a configuration in every eternal
family of size \(\alpha(G)\).

## 4. Additivity over components

Let \(G\) have nonempty components \(G_1,\ldots,G_t\), with vertex sets
\(V_1,\ldots,V_t\).

**Proposition 5.**

\[
\begin{aligned}
 \gamma(G)&=\sum_{j=1}^t\gamma(G_j),\\
 \gamma^\infty(G)&=\sum_{j=1}^t\gamma^\infty(G_j),\\
 \theta(G)&=\sum_{j=1}^t\theta(G_j).
\end{aligned}
\]

**Proof for \(\gamma\).**  A set dominates \(G\) if and only if its
intersection with every \(V_j\) dominates \(G_j\).  Both inequalities, and
hence equality, follow by restriction and union.

**Proof for \(\theta\).**  No clique can contain vertices from two different
components, because such vertices are nonadjacent.  Therefore every clique
partition restricts to a clique partition of each component.  Conversely, the
union of componentwise clique partitions is a clique partition of \(G\).

**Proof for \(\gamma^\infty\), upper bound.**  For each \(j\), choose an
eternal family \(\mathcal F_j\) of
\(k_j=\gamma^\infty(G_j)\)-sets.  The product family

\[
 \mathcal F=\{D_1\cup\cdots\cup D_t:D_j\in\mathcal F_j\}
\]

consists of dominating \(\sum_j k_j\)-sets.  An attack in \(G_j\) is answered
inside \(G_j\) using \(\mathcal F_j\), leaving all other component
configurations unchanged.  This uses exactly one guard move.  Hence
\(\gamma^\infty(G)\leq\sum_j\gamma^\infty(G_j)\).

**Proof for \(\gamma^\infty\), lower bound.**  Let \(\mathcal F\) be any
eternal family of \(k\)-sets in \(G\).  A configuration has a component count
vector

\[
 c(D)=(|D\cap V_1|,\ldots,|D\cap V_t|).
\]

Choose any vector \(c=(c_1,\ldots,c_t)\) realized in \(\mathcal F\), and let

\[
 \mathcal F_c=\{D\in\mathcal F:c(D)=c\}.
\]

This subfamily is nonempty.  Every legal guard move lies inside one component,
so it preserves the entire count vector.  Thus \(\mathcal F_c\) is itself
closed under all required responses.

For a fixed \(j\), project this slice to

\[
 \mathcal P_j=\{D\cap V_j:D\in\mathcal F_c\}.
\]

Every member is a dominating \(c_j\)-set of \(G_j\), since no vertex of
\(G_j\) can be dominated from another component.  Given
\(S=D\cap V_j\in\mathcal P_j\) and an attack \(r\in V_j-S\), the global
response must move a guard \(u\in V_j\), remains in \(\mathcal F_c\), and
projects to the required one-guard response in \(\mathcal P_j\).  Hence
\(\mathcal P_j\) is an eternal family on \(G_j\), so
\(c_j\geq\gamma^\infty(G_j)\).  Summing gives

\[
 k=\sum_jc_j\geq\sum_j\gamma^\infty(G_j).
\]

Together with the upper bound, this proves additivity. \(\square\)

The count-vector slice is essential.  An arbitrary eternal family need not
have one count vector globally: on \(K_2\mathbin{\dot\cup}K_2\), the union of
the closed \(3\)-guard families with count vectors \((2,1)\) and \((1,2)\) is
an eternal family with two different vectors.

**Corollary 6 (connected reduction).**  If any counterexample to the
\(\gamma\)–\(\theta\) conjecture exists, then a connected counterexample
exists.

**Proof.**  Suppose

\[
 \gamma(G)=\gamma^\infty(G)<\theta(G).
\]

For each component set
\(a_j=\gamma(G_j)\), \(b_j=\gamma^\infty(G_j)\), and
\(c_j=\theta(G_j)\).  Theorem 2 gives \(a_j\leq b_j\leq c_j\).  Additivity and
\(\sum_j a_j=\sum_j b_j\) imply \(a_j=b_j\) for every \(j\), because all
differences \(b_j-a_j\) are nonnegative and sum to zero.  The strict inequality
\(\sum_j b_j<\sum_jc_j\) implies \(b_j<c_j\) for at least one \(j\).  That
connected component satisfies

\[
 \gamma(G_j)=\gamma^\infty(G_j)<\theta(G_j).
\]

\(\square\)

This proves only that **at least one** component is a counterexample; it does
not say that every component is one.

## 5. Imperfection obstruction

**Proposition 7.**  Every counterexample \(G\) contains an induced odd hole or
an induced odd antihole, of odd length at least \(5\).

**Proof.**  Let
\(\gamma(G)=\gamma^\infty(G)=k<\theta(G)\).  By Corollary 3,
\(\alpha(G)=k\).  Put \(H=\overline G\).  Then

\[
 \omega(H)=\alpha(G)=k<\theta(G)=\chi(H),
\]

so \(H\) is not perfect (the graph \(H\) itself violates
\(\chi=\omega\)).  By the Strong Perfect Graph Theorem, \(H\) contains an
induced odd hole or an induced odd antihole.  Taking complements on the same
vertex set interchanges holes and antiholes, so \(G\) also contains an induced
odd hole or odd antihole. \(\square\)

This is a necessary condition only.  It does not by itself explain the
order-\(10\) threshold for graphs with \(\gamma^\infty<\theta\), and it is far
from sufficient for the target equalities.  For example, \(C_5\) has the
required obstruction but has \(\gamma=2<3=\gamma^\infty\).

## 6. The case \(\alpha=2\) and the minimum parameter

This section gives a self-contained reduction to the SPGT and an explicit
attack argument; it does not assume the \(\gamma\)–\(\theta\) conjecture.

### 6.1 Induced-subgraph monotonicity

**Lemma 8.**  If \(H=G[W]\) is a nonempty induced subgraph of \(G\), then

\[
 \gamma^\infty(H)\leq\gamma^\infty(G).
\]

**Proof.**  Let \(\mathcal F\) be an eternal family of \(k\)-sets in \(G\).
Set

\[
 m=\max_{D\in\mathcal F}|D\cap W|
\]

and let \(\mathcal F^\star\) consist of the configurations attaining this
maximum.  It is nonempty.  Project it to

\[
 \mathcal P=\{D\cap W:D\in\mathcal F^\star\}.
\]

Fix \(S=D\cap W\in\mathcal P\) and \(r\in W-S\).  The global closure property
gives a response

\[
 D'=(D-\{u\})\cup\{r\}\in\mathcal F
\quad\text{for some }u\in D\cap N_G(r).
\]

If \(u\notin W\), then \(|D'\cap W|=m+1\), contradicting maximality of \(m\).
Thus \(u\in W\).  Since \(H\) is induced, \(ur\in E(H)\), and

\[
 D'\cap W=(S-\{u\})\cup\{r\}\in\mathcal P.
\]

Here \(|D'\cap W|=m\), so \(D'\in\mathcal F^\star\), which justifies the
displayed membership in \(\mathcal P\).  The argument also shows that every
\(S\in\mathcal P\) dominates \(H\):
every unoccupied \(r\in W-S\) has the neighbor \(u\in S\) just exhibited.
If \(m=0\), the same response would necessarily increase the number of guards
in \(W\), so \(m\geq1\).  Therefore \(\mathcal P\) is an eternal family of
\(m\)-sets in \(H\), and
\(\gamma^\infty(H)\leq m\leq k\).  Minimize over \(k\). \(\square\)

A naive projection of an arbitrary configuration need not dominate an induced
subgraph; choosing configurations with the **maximum** number of guards in
\(W\) is what makes the proof work.

### 6.2 Odd antiholes need three guards

**Lemma 9.**  For every odd \(n\geq5\),

\[
 \gamma^\infty(\overline{C_n})=3.
\]

**Proof.**  Label the vertices of \(C_n\) by
\(0,1,\ldots,n-1\) cyclically, and put \(A_n=\overline{C_n}\).
A pair \(\{x,y\}\) fails to dominate \(A_n\) exactly when \(x\) and \(y\)
are at cyclic distance \(2\) in \(C_n\).  Indeed, a vertex \(z\) is
undominated by the pair in \(A_n\) exactly when \(z\) is adjacent in \(C_n\)
to both \(x\) and \(y\), which happens exactly when \(x,y\) are the two cycle
neighbors of \(z\).

Suppose, for a contradiction, that \(A_n\) has an eternal family
\(\mathcal F\) of \(2\)-sets.  The set \(\{0,1\}\) is independent in \(A_n\),
so Lemma 1 forces \(\{0,1\}\in\mathcal F\).

We claim successively that

\[
 \{0,1\},\{0,3\},\{0,5\},\ldots,\{0,n-4\}
 \quad\text{all belong to }\mathcal F.
\]

Suppose \(\{0,d\}\in\mathcal F\), where \(d\) is odd and
\(1\leq d\leq n-6\), and attack \(r=d+2\).  Moving the guard at \(0\) (if
that move is an edge at all) leaves the pair \(\{d,d+2\}\), which has cycle
distance \(2\) and does not dominate \(A_n\).  Hence the only possible valid
response moves the guard at \(d\) to \(d+2\).  This is a legal edge of
\(A_n\), and closure forces \(\{0,d+2\}\in\mathcal F\).  The claim follows by
induction.

Now attack \(n-2\) from the configuration \(\{0,n-4\}\).  Moving the guard at
\(n-4\) leaves \(\{0,n-2\}\), while moving the guard at \(0\) leaves
\(\{n-4,n-2\}\).  Both resulting pairs have cyclic distance \(2\), so neither
dominates \(A_n\).  Both candidate moves traverse edges of \(A_n\), since
both possible guards are at cyclic distance \(2\) from \(n-2\); nevertheless
there is no response into a dominating member of \(\mathcal F\), a
contradiction.  (For \(n=5\), the initial configuration is already
\(\{0,n-4\}\), and this final attack is the whole argument.)

Thus \(\gamma^\infty(A_n)\geq3\).  On the other hand,
\(\theta(A_n)=\chi(C_n)=3\), so Theorem 2 gives
\(\gamma^\infty(A_n)\leq3\). \(\square\)

Every attack in this proof is at an unoccupied vertex and every proposed
response moves exactly one guard.

### 6.3 Excluding \(k=1,2\)

**Theorem 10 (the \(\alpha=2\) case).**  If

\[
 \alpha(G)=\gamma^\infty(G)=2,
\]

then \(\theta(G)=2\).

**Proof.**  Suppose instead that \(\theta(G)>2\), and let
\(H=\overline G\).  Then

\[
 \omega(H)=\alpha(G)=2<\theta(G)=\chi(H),
\]

so \(H\) is imperfect.  By the SPGT, \(H\) contains an induced odd hole or
odd antihole.

If \(H\) contains an induced odd hole \(C_n\), then \(G\) contains the induced
odd antihole \(\overline{C_n}\).  Lemmas 8 and 9 give
\(\gamma^\infty(G)\geq3\), a contradiction.

If \(H\) contains an induced odd antihole \(\overline{C_n}\), then \(G\)
contains an induced odd hole \(C_n\).  For \(n\geq7\),
\(\alpha(C_n)=\lfloor n/2\rfloor\geq3\), contradicting
\(\alpha(G)=2\).  For \(n=5\), the graph \(C_5\) is also its own odd
antihole, and Lemmas 8 and 9 again give
\(\gamma^\infty(G)\geq3\).

Both SPGT outcomes are impossible.  Hence \(\theta(G)\leq2\); Theorem 2 and
\(\alpha(G)=2\) force \(\theta(G)=2\). \(\square\)

**Corollary 11 (minimum parameter).**  Every counterexample has

\[
 k=\gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)\geq3.
\]

**Proof.**  The equality is Corollary 3.  If \(k=1\), then
\(\alpha(G)=1\), so \(G\) is complete and \(\theta(G)=1\), not a
counterexample.  If \(k=2\), Theorem 10 gives \(\theta(G)=2\), again not a
counterexample. \(\square\)

## 7. Sound search target established by these reductions

Without using any citation-pending graph-class theorem, a counterexample may
be sought among connected graphs satisfying

\[
\begin{gathered}
 k=\gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)\geq3,\\
 \theta(G)\geq k+1,
\end{gathered}
\]

that contain an induced odd hole or odd antihole of odd length at least \(5\).

Well-coveredness may be used as a necessary filter only together with the
explicit test \(\gamma=\alpha\).  The odd-hole/antihole condition is likewise
only a necessary filter.  The additional proposed filters “nonplanar,”
“\(\Delta\geq4\),” “contains a triangle,” and “contains a \(4\)-cycle” become
sound only after the exact one-guard graph-class theorems listed in
`class_restrictions_pending.md` have passed their source audit.
