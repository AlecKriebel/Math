# Leaf--support reduction and a \(5k/2\) minimum-order bound

## Status and claim boundary

This note proves a reduction for the standard one-guard-moves eternal
domination model.  In particular, attacks are made only at unoccupied
vertices and exactly one guard moves along one graph edge.

The reduction shows that deleting a leaf together with its unique neighbor
from a \(\gamma=\gamma^\infty\) graph preserves that equality while lowering
the common value by one.  Clique cover number also falls by exactly one.
Consequently the deletion preserves a strict \(\gamma\)--\(\theta\) gap.

The later \(5k/2\) corollary uses the classical McCuaig--Shepherd domination
bound and the published absence of a counterexample through order \(11\).
No novelty claim is made here until the dedicated literature audit is
complete.  Nothing in this note resolves the universal
\(\gamma\)--\(\theta\) conjecture.

## 1. The exact deletion theorem

### Theorem 1 (leaf--support deletion)

Let \(G\) be a finite simple graph with

\[
 \gamma(G)=\gamma^\infty(G)=k,
\]

let \(x\) be a leaf of \(G\), let \(y\) be its unique neighbor, and suppose
that

\[
 Q=G-\{x,y\}
\]

is nonempty.  Then

\[
 \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=k-1,
 \tag{1.1}
\]

\(Q\) is well-covered, and

\[
 \theta(G)=\theta(Q)+1.
 \tag{1.2}
\]

The nonempty-\(Q\) hypothesis only removes the degenerate graph
\(G=K_2\), for which \(k=1\).  Extending (1.1) to that case would require
choosing conventions for domination and eternal domination on the empty
graph.  No counterexample is affected, because every counterexample has
common parameter at least three.

#### Proof

The accepted parameter chain

\[
 \gamma\leq i\leq\alpha\leq\gamma^\infty
\]

first gives

\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=k.
 \tag{1.3}
\]

Thus every maximal independent set of \(G\) has size \(k\).

Let \(I\) be any maximal independent set of \(Q\).  The set
\(I\cup\{x\}\) is independent in \(G\).  It is maximal there: the vertex
\(y\) is adjacent to \(x\), and every vertex of \(Q-I\) has a neighbor in
\(I\) by maximality inside \(Q\).  Equation (1.3) therefore gives

\[
 |I|+1=k.
\]

This holds for every maximal independent set \(I\) of \(Q\).  Hence \(Q\)
is well-covered and

\[
 i(Q)=\alpha(Q)=k-1.
 \tag{1.4}
\]

In particular, \(\gamma(Q)\leq k-1\).  Conversely, if \(Q\) had a
dominating set \(A\) of size at most \(k-2\), then

\[
 A\cup\{x\}
\]

would dominate \(G\): \(A\) dominates \(Q\), while \(x\) dominates both
\(x\) and \(y\).  This would contradict \(\gamma(G)=k\).  Thus

\[
 \gamma(Q)=k-1.
\tag{1.5}
\]

It remains to prove the eternal equality without silently changing the
game model.  Fix an eternal dominating family \(\mathcal D\) of \(k\)-sets
in \(G\).  We use the following elementary forcing fact.

> If \(\alpha(G)=k\), then every independent \(k\)-set \(S\) belongs to
> every eternal \(k\)-family.

Indeed, begin at any state in the family and attack the unoccupied vertices
of \(S\) one at a time.  Because \(S\) is independent, a response to an
attack in \(S\) cannot move a guard that is already on \(S\).  Each legal
one-guard response therefore increases the number of guards on \(S\) by
one.  After finitely many unoccupied attacks, the state is exactly \(S\).

Choose a maximum independent set \(I\) of \(Q\).  By (1.4),
\(I\cup\{x\}\) is an independent \(k\)-set of \(G\), so the forcing fact
puts it in \(\mathcal D\).  Consequently the projected family

\[
 \mathcal E=
 \{D-\{x\}:D\in\mathcal D,\ x\in D\}
 \tag{1.6}
\]

is nonempty.  No state \(D\in\mathcal D\) can contain both \(x\) and
\(y\).  If it did, then \(D-\{x\}\) would still dominate \(G\): the guard
on \(y\) dominates \(x\), while \(x\) has no neighbor other than \(y\) and
therefore cannot be the sole guard dominating any other vertex.  This
would be a dominating \((k-1)\)-set, contrary to \(\gamma(G)=k\).
It follows that every member \(D-\{x\}\) in (1.6) lies wholly in \(Q\), so
\(\mathcal E\) is a family of \((k-1)\)-sets of \(Q\).

Every \(B\in\mathcal E\) dominates \(Q\).  To see this, write
\(D=B\cup\{x\}\in\mathcal D\).  The state \(D\) dominates \(G\), and the
leaf \(x\) has no neighbor in \(Q\), so the guards in \(B\) alone dominate
every vertex of \(Q\).

Now let \(r\in V(Q)-B\) be attacked.  It is also unoccupied in
\(D=B\cup\{x\}\).  Eternal closure in \(G\) supplies a guard

\[
 u\in D\cap N_G(r)
\]

such that

\[
 D'=(D-\{u\})\cup\{r\}\in\mathcal D.
\]

Since \(x\) has no neighbor in \(Q\), \(u\neq x\).  Therefore \(u\in B\),
\(x\in D'\), and

\[
 D'-\{x\}=(B-\{u\})\cup\{r\}\in\mathcal E.
\]

Thus every unoccupied attack in \(Q\) has a response in \(\mathcal E\) by
exactly one guard moving along exactly one edge.  The family \(\mathcal E\)
is an eternal dominating family of size \(k-1\) in \(Q\).  Hence

\[
 \gamma^\infty(Q)\leq k-1.
\]

Together with
\(\alpha(Q)=k-1\leq\gamma^\infty(Q)\), this proves the remaining equality
in (1.1).

Finally, \(\{x,y\}\) is a clique, so a clique partition of \(Q\), together
with this two-vertex clique, gives

\[
 \theta(G)\leq\theta(Q)+1.
\tag{1.7}
\]

For the reverse inequality, take a minimum clique partition of \(G\).
The part containing \(x\) is either \(\{x,y\}\) or \(\{x\}\), because
\(x\) has no other neighbor.  In the first case, deleting that part leaves
a clique partition of \(Q\) with \(\theta(G)-1\) parts.  In the second
case, let \(C\) be the part containing \(y\).  We cannot have
\(C=\{y\}\), since then the two singleton parts could be replaced by the
single clique \(\{x,y\}\), contradicting minimality.  Replace the parts
\(\{x\}\) and \(C\) by \(\{x,y\}\) and \(C-\{y\}\).  This preserves the
number of parts; deleting \(\{x,y\}\) again leaves a partition of \(Q\)
with \(\theta(G)-1\) parts.  Thus

\[
 \theta(Q)\leq\theta(G)-1.
\tag{1.8}
\]

Equations (1.7)--(1.8) prove (1.2). \(\square\)

## 2. Counterexample preservation

### Corollary 2

Under the hypotheses of Theorem 1, if

\[
 \gamma(G)=\gamma^\infty(G)=k<\theta(G),
\]

then \(Q=G-\{x,y\}\) is a smaller counterexample:

\[
 \gamma(Q)=\gamma^\infty(Q)=k-1<\theta(Q).
\]

#### Proof

Theorem 1 gives the two equalities and
\(\theta(Q)=\theta(G)-1\).  Since the parameters are integral,
\(\theta(G)\geq k+1\), and hence

\[
 \theta(Q)\geq k>k-1.
\]

\(\square\)

### Corollary 3 (minimum counterexamples have minimum degree two)

If the \(\gamma\)--\(\theta\) conjecture has a counterexample, then every
minimum-order counterexample is connected and has minimum degree at least
two.

#### Proof

The accepted component-additivity reduction says that a disconnected
counterexample has a counterexample component.  Minimum order therefore
forces connectedness.  A counterexample has common parameter at least
three, so it is not \(K_1\) or \(K_2\).  A connected minimum-order
counterexample cannot have a leaf by Corollary 2.  It has no isolated
vertex by connectedness.  Thus its minimum degree is at least two.
\(\square\)

## 3. A classical minimum-order consequence

McCuaig and Shepherd proved that if a connected graph \(R\) of order \(n\)
has \(\delta(R)\geq2\) and is not one of seven exceptional graphs, then

\[
 \gamma(R)\leq\frac{2n}{5}.
\tag{3.1}
\]

The original source is:

> W. McCuaig and B. Shepherd, *Domination in graphs with minimum degree
> two*, Journal of Graph Theory **13** (1989), 749--762,
> DOI `10.1002/jgt.3190130610`.

The journal abstract states the bound and the seven-exception scope.  The
exception inventory is restated explicitly as
\(\mathcal F_4\cup\mathcal F_7\), hence consists only of graphs of orders
four and seven, in Theorem 1 of:

> M. A. Henning, I. Schiermeyer, and A. Yeo, *A new bound on the domination
> number of graphs with minimum degree two*, Electronic Journal of
> Combinatorics **18** (2011), Paper P12, DOI `10.37236/499`.

The official EJC PDF is retained locally as
`literature/sources/henning_schiermeyer_yeo_2011_p12.pdf`, with SHA-256
`418199b3a9f9c92974046a6c92b0b11b24cdec51e034f5aa23168c4bdfbb4285`.

The lower-order premise used below is the published exhaustive computation
of:

> G. MacGillivray, C. M. Mynhardt, and V. Virgile, *Eternal Domination and
> Clique Covering*, Electronic Journal of Graph Theory and Applications
> **10**(2) (2022), 603--624,
> DOI `10.5614/ejgta.2022.10.2.19`.

That paper reports no counterexample through order \(11\).  This is a
paper-level premise, not a new campaign-grade coverage certificate for all
graphs of orders ten and eleven.  The official PDF is retained as
`literature/sources/mmv2022.pdf`, with SHA-256
`e1a5c6bb4fb4767c3d91a5e848872d26d97d3f0df284142a1b885ad720a20edf`.

### Theorem 4 (the \(5k/2\) bound)

Assume the published, independently audited fact that no counterexample
has order at most \(11\).  If \(G\) is a minimum-order counterexample of
order \(n\) and common parameter

\[
 k=\gamma(G)=\gamma^\infty(G),
\]

then

\[
 n\geq\left\lceil\frac{5k}{2}\right\rceil.
\tag{3.2}
\]

#### Proof

The published lower-order result gives \(n\geq12\), so \(G\) is not one of
the seven McCuaig--Shepherd exceptions of orders four and seven.
Corollary 3 gives connectedness and \(\delta(G)\geq2\).  Apply (3.1):

\[
 k=\gamma(G)\leq\frac{2n}{5}.
\]

Rearranging and using integrality gives (3.2). \(\square\)

### Corollary 5 (the order-12 parameter-five slice)

Assume the published absence of counterexamples through order \(11\).
There is no graph \(G\) of order \(12\) satisfying

\[
 \gamma(G)=\gamma^\infty(G)=5<\theta(G).
\]

#### Proof

If such a graph existed, then, because no smaller counterexample exists, a
counterexample of order \(12\) would itself have minimum possible order.
Theorem 4 would therefore apply to that same graph with common parameter
\(k=5\), giving

\[
 12\geq\left\lceil\frac{5\cdot5}{2}\right\rceil=13,
\]

a contradiction. \(\square\)

## 4. Exact scope

Theorem 1 and Corollaries 2--3 are self-contained consequences of the
one-guard definition and the accepted parameter/component reductions.
Theorem 4 and Corollary 5 additionally depend on the cited classical
domination theorem and the published order-\(11\) frontier.

Corollary 5 removes the remaining \(k=5\) lane at order \(12\).  It does
not remove the order-12 \(k=4\) lane, does not by itself increase the full
minimum counterexample order beyond \(11\), and does not resolve the
universal conjecture.
