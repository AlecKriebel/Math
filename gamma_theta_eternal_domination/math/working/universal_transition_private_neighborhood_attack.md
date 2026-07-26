# Universal transition/private-neighborhood attack

## Status and exact claim ledger

Date: 2026-07-26 (PDT)

This is an independent proof lane for the standard one-guard-moves eternal
domination model. Attacks are made only at unoccupied vertices, exactly one
guard moves along one edge to the attacked vertex, and every state retained
in an eternal family dominates.

The universal \(\gamma\)--\(\theta\) conjecture is **not resolved** here.
No categorical literature-novelty claim is made for the Hall formulation
pending a dedicated prior-art audit. The Hall condition is logically
stronger than the pointwise campaign condition; it also adds a constraint
not implied by two-ply survival, with explicit separating graphs.
The results of this lane are:

- **PROVED:** the restoration lemma for an arbitrary state of an eternal
  family containing an independent guard state;
- **PROVED:** the viable-list Hall theorem for every independent outside
  set, and its static private-neighborhood obstruction certificate;
- **PROVED:** an exact equivalence between a \(k\)-clique partition and a
  list-respecting static guard-territory coloring relative to a maximum
  independent state;
- **REFUTED:** the claim that all attacks which one guard can defend directly
  from an independent state form a clique;
- **REFUTED:** the claim that an inclusion-minimal eternal family must itself
  admit globally consistent static guard labels;
- **OBSERVED:** an independent ordinary-set exhaustive probe found no
  violation of the viable-list Hall theorem among all
  \(\gamma=\alpha=\gamma^\infty\) graphs through order \(9\), comprising
  3,585 equal-parameter graphs and 37,358 maximum-independent reference
  states;
- **OBSERVED:** all 78 minimum-cardinality eternal families enumerated for
  the equal-parameter graphs through order \(6\) admitted consistent guard
  labels; no proof of this pattern is known; and
- **CONJECTURED, THEN BLOCKED:** a minimum-cardinality-family labeling theorem
  might imply the desired clique partition, but its conclusion already
  supplies the missing \(k\)-clique partition and no mechanism proving it
  survived the second iteration.

The independent probe and its machine-readable evidence are
`math/working/universal_transition_private_probe.py` and
`results/universal_transition_private_probe.json`; the replay binding is
recorded in `results/universal_transition_private_probe.log`. The probe
invokes the pinned `geng` only. It does not invoke a SAT solver or either
campaign eternal evaluator.

## 1. Definitions rederived from the game

Let \(\mathcal F\) be an eternal family of \(k\)-sets. For a dominating
configuration \(D\) and \(u\in D\), define its closed private region

\[
 P_D(u)=\{z\in V(G):N[z]\cap D=\{u\}\}.
\]

For an independent \(k\)-set \(S\) and a vertex \(x\notin S\), define the
set of viable guards

\[
 L_S(x)=
 \{u\in S:ux\in E(G)\text{ and }S-u+x\text{ dominates }G\}.
\tag{1.1}
\]

Here and below \(S-u+x=(S-\{u\})\cup\{x\}\).

### Lemma 1.1 (independent-state forcing) — PROVED

If \(S\) is an independent \(k\)-set, then \(S\) belongs to every eternal
family of \(k\)-sets.

**Proof.** Start at any \(D\in\mathcal F\). Repeatedly attack an unoccupied
vertex \(s\in S\). A guard already on a different vertex of \(S\) cannot
respond, because \(S\) is independent. Every response therefore increases
\(|D\cap S|\) by one while remaining in \(\mathcal F\). After at most \(k\)
attacks the state is \(S\). All attacked vertices were unoccupied, and one
guard moved at each step. \(\square\)

### Lemma 1.2 (minimum guards have private regions) — PROVED

If \(|D|=\gamma(G)\) and \(D\) dominates, then
\(P_D(u)\ne\varnothing\) for every \(u\in D\).

**Proof.** If \(P_D(u)=\varnothing\), every vertex has a dominator in
\(D-\{u\}\), contradicting the minimal cardinality of \(D\). \(\square\)

### Lemma 1.3 (one-swap criterion) — PROVED

If \(D\) dominates, \(x\notin D\), and \(u\in D\cap N(x)\), then

\[
 D-u+x\text{ dominates}
 \quad\Longleftrightarrow\quad
 P_D(u)\subseteq N[x].
\tag{1.2}
\]

**Proof.** Removing \(u\) can uncover exactly the vertices whose unique
dominator in \(D\) was \(u\). Adding \(x\) repairs precisely those uncovered
vertices in \(N[x]\). \(\square\)

For independent \(S\), the condition \(P_S(u)\subseteq N[x]\) already
implies \(ux\in E(G)\), because \(u\in P_S(u)\) and \(x\ne u\). Hence

\[
 L_S(x)=\{u\in S:P_S(u)\subseteq N[x]\}.
\tag{1.3}
\]

No all-guards movement, occupied attack, or reachability-only convention is
used in these statements.

## 2. First serious iteration: viable territories

The first attempted route was to use

\[
 R_S(u)=\{x\notin S:u\in L_S(x)\}
\]

as the territory of guard \(u\), and to prove that
\(\{u\}\cup R_S(u)\) is a clique. That would immediately give \(k\) clique
parts after assigning vertices with multiple viable guards.

### The naive territory claim is REFUTED

Take \(G=C_4=K_{2,2}\) with bipartition
\(S=\{0,1\}\) and \(\{2,3\}\), in the graph6 labeling `C]`. Then

\[
 P_S(0)=\{0\},
\]

and both \(2\) and \(3\) can be defended by moving the guard at \(0\).
Thus \(2,3\in R_S(0)\), but \(23\notin E(G)\). This graph satisfies

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=\theta(G)=2.
\]

So even a positive instance of the conjecture can have nonclique direct
response sets. A choice of territories might still work, but the raw
one-step sets do not.

The failed attempt nevertheless exposes a stronger invariant which survives.

## 3. Restoration lemma

### Theorem 3.1 (restoration of an arbitrary family state) — PROVED

Let \(\mathcal F\) be an eternal family of \(k\)-sets and let
\(S\in\mathcal F\) be independent. For an arbitrary \(D\in\mathcal F\), put

\[
 X=D-S,\qquad U=S-D.
\]

Then \(|X|=|U|\), and

\[
 U\subseteq\bigcup_{x\in X}L_S(x).
\tag{3.1}
\]

Equivalently, every guard position missing from \(S\) in a family state is a
viable one-step defender, relative to the original state \(S\), of at least
one outside guard position in that state.

**Proof.** Equality of the two cardinalities follows from
\(|D|=|S|=k\). Fix any \(u\in U\).

Starting from \(D\), attack the vertices of \(U-\{u\}\), one at a time, in
any order. Every such vertex is unoccupied when attacked. At every stage, all
currently occupied vertices of \(S\) are different from the attacked vertex
and hence nonadjacent to it, because \(S\) is independent. Therefore the
responding guard must come from the currently occupied vertices outside
\(S\). The response restores the attacked vertex of \(S\) and removes one
outside guard.

After the \(|U|-1\) restoration attacks, the state has the form

\[
 S-u+x
\]

for one remaining \(x\in X\). It belongs to \(\mathcal F\), so it dominates.
Now attack the still-unoccupied vertex \(u\). No guard in \(S-\{u\}\) is
adjacent to \(u\); closure therefore forces the sole outside guard \(x\) to
be adjacent to \(u\). Consequently \(S-u+x\) is a legal dominating swap from
\(S\), which says \(u\in L_S(x)\).

The vertex \(u\) was arbitrary, proving (3.1). Every attack used above was
unoccupied and every response moved exactly one adjacent guard. \(\square\)

This statement does not require \(X\) to be independent. The independence
needed is exactly that of the reference guard state \(S\).

## 4. Viable-list Hall theorem

### Theorem 4.1 (Hall condition on independent attack sets) — PROVED

Let \(\mathcal F\) be an eternal family of \(k\)-sets and let \(S\) be an
independent \(k\)-set. For every independent set
\(X\subseteq V(G)-S\),

\[
 \left|\bigcup_{x\in X}L_S(x)\right|\ge |X|.
\tag{4.1}
\]

In particular, the bipartite graph joining \(x\in X\) to
\(u\in L_S(x)\) has a matching saturating \(X\).

**Proof.** Lemma 1.1 gives \(S\in\mathcal F\). Attack the vertices of \(X\)
one at a time, in any order. A guard already moved to an earlier attacked
vertex of \(X\) cannot respond to a later attack in \(X\), because \(X\) is
independent. Thus each response removes a previously unmoved guard of \(S\).
After all attacks the family contains a state

\[
 D=(S-U)\cup X
\]

with \(U\subseteq S\) and \(|U|=|X|\). Theorem 3.1 gives

\[
 U\subseteq\bigcup_{x\in X}L_S(x),
\]

which proves (4.1). Hall's marriage theorem gives the final formulation.
Indeed, every subset of \(X\) is independent, so (4.1) supplies Hall's
inequality for every subfamily of the lists.
\(\square\)

The theorem also implies, for every \(Y\subseteq V(G)-S\),

\[
 \left|\bigcup_{y\in Y}L_S(y)\right|
 \ge \alpha(G[Y]),
\tag{4.2}
\]

by applying (4.1) to a maximum independent set of \(G[Y]\).

### Corollary 4.2 (static Hall obstruction certificate) — PROVED

Suppose \(\alpha(G)=k\). If a maximum independent set \(S\) and an
independent \(X\subseteq V(G)-S\) satisfy

\[
 \left|\bigcup_{x\in X}L_S(x)\right|<|X|,
\tag{4.3}
\]

then

\[
 \gamma^\infty(G)\ge k+1.
\]

**Proof.** Theorem 4.1 excludes an eternal \(k\)-family. The general lower
bound \(\alpha(G)\le\gamma^\infty(G)\), together with integrality, gives the
claim. \(\square\)

A certificate needs only:

1. the maximum independent set \(S\);
2. the independent set \(X\);
3. a claimed container \(W\subseteq S\) for the union of the lists;
4. for every \(x\in X\) and \(u\in S-W\), either the nonedge \(ux\), or a
   named witness in \(P_S(u)-N[x]\); and
5. the inequality \(|W|<|X|\).

Item 4 proves \(\bigcup_{x\in X}L_S(x)\subseteq W\); positive list edges do
not have to be certified. Equation (1.2) checks every excluded list edge. No eternal fixed-point
calculation is needed by such a checker.

### Strictness over the pointwise private-region condition — PROVED

The graph6 record `FCp`_` is \(C_7\), with cycle

\[
 0,3,6,2,5,1,4,0.
\]

For

\[
 S=\{0,1,2\},\qquad X=\{4,5\},
\]

one has

\[
 P_S(0)=\{0,3\},\quad P_S(1)=\{1\},\quad
 P_S(2)=\{2,6\},
\]

and therefore

\[
 L_S(4)=L_S(5)=\{1\}.
\]

Both singleton attack lists are nonempty, but their union has size one.
Thus the Hall obstruction rejects this state while the pointwise
private-neighborhood test does not. By cyclic symmetry, every maximum
independent state of \(C_7\) passes the pointwise test.

There is also a separation from two-ply survival. On \(C_{15}\), let

\[
 S=\{0,2,4,6,8,10,12\},\quad
 X=\{1,3,5,7,9,11\}.
\]

Then

\[
\begin{aligned}
L_S(1)&=\{2\},\\
L_S(3)&=\{2,4\},\\
L_S(5)&=\{4,6\},\\
L_S(7)&=\{6,8\},\\
L_S(9)&=\{8,10\},\\
L_S(11)&=\{10\}.
\end{aligned}
\]

The union has size five while \(|X|=6\). Nevertheless every maximum
independent state of \(C_{15}\) survives through the two-ply kernel
\(\mathcal K_2\). The exact kernel sizes are

\[
 |\mathcal K_0|=765,\quad |\mathcal K_1|=120,\quad
 |\mathcal K_2|=15,\quad |\mathcal K_3|=0.
\]

The positive two-ply survival certificate already stored at
`certificates/c15_k2_not_k3.json` and the independent probe both check this
finite separation. Hence Theorem 4.1 is not merely a restatement of the
one- or two-ply conditions.

## 5. Exact connection to clique partitions

The Hall theorem suggests assigning every outside vertex \(x\) to one of its
viable guards in \(L_S(x)\). The missing condition is global compatibility.

### Proposition 5.1 (viable-list coloring equivalence) — PROVED

Suppose \(\alpha(G)=k\), and fix a maximum independent set \(S\). Then
\(\theta(G)=k\) if and only if there is a map

\[
 c:V(G)\longrightarrow S
\]

such that:

1. \(c(s)=s\) for every \(s\in S\);
2. \(c(x)\in L_S(x)\) for every \(x\notin S\); and
3. every fiber \(c^{-1}(s)\) is a clique of \(G\).

**Proof.** Such a map immediately partitions \(V(G)\) into \(k\) cliques,
so \(\theta(G)\le k\). The general bound \(\alpha(G)\le\theta(G)\) gives
equality.

Conversely, suppose \(\theta(G)=k\) and take a partition into \(k\) cliques.
Each clique contains at most one vertex of the independent \(k\)-set \(S\).
Since there are exactly \(k\) cliques, each contains exactly one member of
\(S\). Assign every vertex to that member.

It remains to check the viable-list condition. If \(y\in P_S(s)\), then
\(y\) is adjacent to no member of \(S-\{s\}\). It therefore cannot lie in a
clique whose representative is in \(S-\{s\}\); hence \(y\) lies in the
\(s\)-clique. Every other vertex \(x\) assigned to \(s\) is adjacent to all
of \(P_S(s)\). Equation (1.3) gives \(s\in L_S(x)\). \(\square\)

Thus Theorem 4.1 proves Hall's necessary condition for the exact list-coloring
instance whose solution would settle the conjecture. It does not prove that
the instance is colorable.

### Odd-cycle parity is the first explicit obstruction — REFUTED implication

The complement of \(C_7\), graph6 `FUzro`, has

\[
 \gamma(G)=\alpha(G)=2,\qquad \theta(G)=3,\qquad
 \gamma^\infty(G)>2.
\]

For the maximum independent set \(S=\{0,1\}\), the five outside lists are

\[
 L_S(2)=\{0\},\quad L_S(3)=\{1\},\quad
 L_S(4)=\{0,1\},\quad L_S(5)=\{0\},\quad L_S(6)=\{1\}.
\]

Every independent outside set satisfies Hall, and cyclic symmetry gives the
same conclusion for every maximum independent reference. But a compatible
two-coloring would have to alternate around the complementary \(7\)-cycle,
which is impossible. Therefore the Hall condition does not imply the
clique partition even under \(\gamma=\alpha\).

The order-11 graph `J@l|bfNuVK_` gives the campaign-relevant \(k=3\)
version:

\[
 \gamma=\alpha=3,\qquad \theta=4,\qquad \gamma^\infty=4,
\]

and all of its maximum-independent references pass the viable-list Hall
condition. The independent probe recomputes these facts with ordinary sets.

This identifies the precise obstruction left by the first iteration:
Hall controls all simultaneous pairwise-conflicting attack sets, but it
does not control parity or more general global coloring obstructions.

## 6. Second serious iteration: static labels from a minimal family

The second route tried to eliminate the global coloring obstruction by
labeling guards in a small eternal family.

Call an eternal \(k\)-family \(\mathcal F\) **statically rainbow** if there
is a map \(c:V(G)\to\{1,\ldots,k\}\) such that every \(D\in\mathcal F\)
contains exactly one vertex of each color.

### Lemma 6.1 (static rainbow family gives a clique partition) — PROVED

If an eternal \(k\)-family is statically rainbow, its color classes are
cliques. Consequently \(\theta(G)\le k\).

**Proof.** First, every vertex occurs in some family state: if it is
unoccupied, attack it and use closure.

Let \(x\) and \(y\) have the same color. Choose \(D\in\mathcal F\) with
\(x\in D\). Then \(y\notin D\), because \(D\) is rainbow. Attack \(y\).
Any successor in \(\mathcal F\) must remain rainbow, so the moved guard must
be the unique guard of \(D\) having color \(c(y)\), namely the guard at
\(x\). The move is legal only if \(xy\in E(G)\). Thus every color class is
a clique. \(\square\)

This is the desired static-territory mechanism. Inclusion-minimality,
however, does not force it.

### Inclusion-minimal-family labeling claim — REFUTED

Let \(G\) be \(K_6\) with the perfect matching

\[
 01,\ 23,\ 45
\]

deleted. Its graph6 record is `E]~o`, and

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=\theta(G)=2.
\]

The following twelve dominating pairs form an eternal family:

\[
\begin{split}
\mathcal F=\{&
01,02,03,04,\;
12,14,15,\;
23,25,\;
34,35,\;
45\}.
\end{split}
\tag{6.1}
\]

The evidence JSON contains one legal response for all \(48\) state/attack
pairs. It also contains the following cycle of attacks, each of which has
the displayed next state as its **unique** successor inside \(\mathcal F\):

\[
\begin{array}{c|c|c}
\text{state}&\text{attack}&\text{unique successor}\\ \hline
01&3&03\\
03&5&35\\
35&1&15\\
15&4&45\\
45&0&04\\
04&2&02\\
02&5&25\\
25&3&23\\
23&4&34\\
34&1&14\\
14&2&12\\
12&0&01
\end{array}
\]

Any nonempty eternal subfamily of \(\mathcal F\) containing one state is
forced around this cycle to contain all twelve states. Hence \(\mathcal F\)
is inclusion-minimal.

But \(\mathcal F\) is not statically rainbow with two colors: it contains
the three pairs \(02,03,23\), so vertices \(0,2,3\) would have to be
pairwise differently colored. This is impossible with two colors.

Thus even an inclusion-minimal eternal family can have nontrivial token-label
holonomy and need not encode any clique partition, despite the underlying
graph itself satisfying the conjecture.

## 7. Refined minimum-cardinality hypothesis and stop diagnosis

The counterexample (6.1) is inclusion-minimal but not minimum-cardinality.
The independent probe exhaustively enumerated all inclusion-minimal eternal
families for every \(\gamma=\alpha=\gamma^\infty\) graph through order \(6\).
Among 78 families of minimum cardinality, it found no static-label
obstruction. This is **OBSERVED**, not proved.

A refined statement would be:

> **CONJECTURED.** If \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=k\), then some
> minimum-cardinality eternal \(k\)-family is statically rainbow.

By Lemma 6.1 this statement immediately implies
\(\theta(G)=k\). Conversely, Proposition 5.1 shows that a \(k\)-clique
partition supplies a statically rainbow eternal family (the full family of
clique transversals). Thus proving the refined statement would require the
same missing global compatibility mechanism as the original conjecture.

After two serious iterations, this lane is therefore **BLOCKED as a
universal-resolution route** at a precisely identified obstruction:

1. local viable territories need not be cliques;
2. their lists satisfy a new Hall condition, but odd-cycle/global coloring
   obstructions survive it;
3. arbitrary inclusion-minimal families can have label holonomy; and
4. restricting to minimum-cardinality families removes the known small
   holonomy witness but leaves a statement whose next step is essentially
   the original conjecture.

The viable-list Hall theorem remains a genuine stronger lemma and a compact
new rejection certificate. It is suitable for the proof and search lanes,
especially as a static filter before deeper transition-kernel evaluation.

## 8. Evidence boundary

The mathematical proofs in Sections 1, 3, 4, 5, and Lemma 6.1 are
definition-level arguments and do not depend on the computation.

The deterministic probe independently:

- decodes graph6 into ordinary adjacency sets;
- enumerates subsets for \(\gamma\) and \(\alpha\);
- computes the one-guard greatest fixed point from the exact online
  quantifiers;
- computes \(\theta\) by a separate canonical clique-partition backtracker;
- enumerates inclusion-minimal families through the declared small-order
  boundary;
- checks all response tables and unique-response arcs; and
- records exact graph, family, list, kernel, and resource data.

The exhaustive through-order-\(9\) counts and the through-order-\(6\)
minimum-family pattern are **OBSERVED finite evidence** only. They are not
used as a universal proof and do not raise the certified order frontier.
