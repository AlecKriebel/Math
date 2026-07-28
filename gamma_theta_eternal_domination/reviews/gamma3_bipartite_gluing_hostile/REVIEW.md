# Hostile audit: exact \(\gamma=3\) target translation and static gluing control

## Verdict

Date: 2026-07-28 (PDT)

\[
\boxed{\texttt{PASS}}
\]

The exact target-translation theorem, the full-root witness refinement,
and the explicit 12-vertex static countermodel are correct.  A clean-room
bit-mask checker independently reconstructed the graph, all five
parameters of the deletion and target graphs, both greatest-fixed-point
kernels, the marking and coloring data, all 18 one-step obligations, and
the complete rank-three adaptive attack tree.

The hostile draft audit identified one nonfatal wording problem in
Corollary 1.2.  Under only the
displayed hypotheses
\(\alpha(G)=\gamma^\infty(G)=3\), the note has not established its
incidental sentence that every vertex lies in a maximum independent
triple.  That sentence is unnecessary: \(B\subseteq R\) follows directly
from the physical nonedge to the target.  Under the stronger full equality
\(\gamma=\alpha=3\), well-coveredness does establish the sentence.  No
proved conclusion or control computation depended on the overstatement.
The candidate was revised before freezing: the sentence was removed and
the direct proof was inserted.  The reviewed revision therefore passes
without reservation.

The audited candidate manifest has SHA-256

```text
89edc267a7ec289de682b78428a0d20237e9ba9081c2289593547679301bc08b
```

All eleven files listed in that manifest match their recorded hashes.

## 1. Clean proof of the exact target translation

Let \(H=\overline G\), fix \(x\), put \(H'=H-x\), and let
\(B=N_H(x)\).  For distinct vertices \(u,v\), the pair \(\{u,v\}\)
fails to dominate \(G\) if and only if some vertex is adjacent in \(H\)
to both \(u\) and \(v\).  Such a common neighbor is automatically outside
\(\{u,v\}\), since \(H\) has no loops.

Assume every pair in \(H'\) has a common neighbor in \(H'\).  Hence all
pairs contained in \(V(H')\) already fail to dominate \(G\).  For
\(v\in V(H')\), the remaining pair \(\{x,v\}\) fails to dominate exactly
when

\[
N_H(x)\cap N_H(v)
=B\cap N_{H'}(v)\ne\varnothing .
\]

Therefore no pair dominates \(G\) if and only if every vertex of \(H'\)
has an open \(H'\)-neighbor in \(B\), which is exactly total domination
of \(H'\) by \(B\).  On a graph of order at least three, the absence of a
dominating pair also excludes a dominating singleton: a dominating
singleton could be enlarged to a dominating pair.  Thus

\[
\gamma(G)\ge3
\quad\Longleftrightarrow\quad
B\text{ totally dominates }H'.
\]

The theorem's common-neighbor hypothesis is equivalently
\(\gamma(G-x)\ge3\), by applying the same pair criterion to \(G-x\).
The use of **total** rather than ordinary domination is essential:
members of \(B\) themselves need another \(B\)-neighbor.

## 2. Audit of \(B\subseteq R\)

In the C-108 definition, a vertex belongs to the family-relative active
set \(A_x\) only if its guard can answer the attack at \(x\).  In
particular, activity requires an edge to \(x\) in \(G\).  If
\(b\in B=N_{\overline G}(x)\), then \(bx\notin E(G)\), so \(b\notin A_x\).
Since \(R=V(G-x)-A_x\),

\[
\boxed{B\subseteq R}.
\]

This proof needs neither well-coveredness nor the assertion that every
vertex lies in a maximum independent triple.  Combining it with the exact
translation gives, whenever both \(\gamma(G-x)\ge3\) and
\(\gamma(G)\ge3\) hold,

\[
N_{H'}(v)\cap B\ne\varnothing
\quad\text{for every }v\in V(H').
\]

Consequently every deletion vertex, active or inactive, has an
\(H'\)-neighbor in \(B\subseteq R\), and \(R\) totally dominates \(H'\).
The inclusion can be strict: a physical \(G\)-neighbor of \(x\) can still
be family-inactive if its proposed successor is absent.

## 3. Audit of the full-root witness refinement

Let \(S=\{s_0,s_1,s_2\}\) be an independent triple of \(G\) avoiding
\(x\), and suppose each swap \(S-s_i+x\) dominates \(G\).

First, domination of the \(i\)-th swap forces \(s_ix\in E(G)\): after
removing \(s_i\), the two remaining anchors cannot dominate it because
\(S\) is independent.  Thus \(S\cap B=\varnothing\).

Now suppose \(b\in B\) sees two anchors \(s_j,s_k\) in \(H'\).  The
successor obtained by replacing the third anchor \(s_i\) is
\(\{x,s_j,s_k\}\).  The vertex \(b\), which is outside this successor,
is adjacent in \(H\) to all three of its vertices, so the successor misses
\(b\) in \(G\), contradicting domination.  Hence every \(b\in B\) sees
at most one anchor.

Total domination of \(H'\) by \(B\) gives a member of
\(B\cap N_{H'}(s_i)\) for each anchor.  The at-most-one conclusion makes
these three spokes nonempty and pairwise disjoint.  It also follows
immediately that \(H'[B]\) has no isolated vertex and remains bipartite
whenever \(H'[R]\) is bipartite.

The note's more general opposite-ridge statement is also correctly
scoped: for a marked response
\(\{a,p,q\}\mapsto\{x,p,q\}\), any member of
\(B\cap N_{H'}(p)\cap N_{H'}(q)\) would be missed by the successor.

## 4. Independent reconstruction of the control

The deletion complement \(H'\) has order 11 and labeled graph6

```text
JEhbtjKk@o_
```

with edges

```text
03 04 07 08 09
13 15 16 18
24 25 26 27 29 (2,10)
36 37 39 (3,10)
46 48 (4,10)
57 58
(9,10)
```

Adjoining \(x=11\) with \(N_H(x)=R=\{1,2,3,5\}\) gives

```text
H = KEhbtjKk@om_
G = KxU[ISrR}NP^
```

Independent graph6 decoding reproduced the edge masks.  The pinned nauty
2.9.3 `labelg` binary, SHA-256
`ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0`,
gave the canonical records

```text
H' = J``E@SV^Tx?
H  = K_?@h]SRNr^Q
G  = Kq]p`SVJw~W^
```

### Static geometry

The independent checker found a common neighbor for all 55 pairs of
\(H'\) and all 66 pairs of \(H\).  The maximal cliques of \(H'\) are
exactly the following ten triangles:

\[
\begin{aligned}
&037,\ 039,\ 048,\ 136,\ 158,\\
&246,\ \{2,4,10\},\ 257,\ \{2,9,10\},\
\{3,9,10\}.
\end{aligned}
\]

For

\[
A=\{0,4,6,7,8,9,10\},\qquad R=\{1,2,3,5\},
\]

the nontrivial opposite-ridge exchanges are

\[
7\leftrightarrow9,\quad
6\leftrightarrow10,\quad
4\leftrightarrow9,\quad
0\leftrightarrow10,\quad
2\leftrightarrow3.
\]

Their transitive classes are

\[
\{0,6,10\},\ \{1\},\ \{2,3\},\
\{4,7,9\},\ \{5\},\ \{8\}.
\]

Each class lies wholly in \(A\) or wholly in \(R\), and the exchanges are
genuinely nonvacuous.  Every facet meets \(A\), while
\(\{0,4,8\}\subseteq A\) is a full root.

The induced graph \(H'[R]\) has edges

\[
13,\ 15,\ 25,
\]

so it is the path \(3-1-5-2\).  It is bipartite and isolate-free.
Moreover, \(B=N_H(x)=R\) totally dominates every vertex of \(H'\).
At the full root, its three anchor spokes are

\[
B\cap N_{H'}(0)=\{3\},\qquad
B\cap N_{H'}(4)=\{2\},\qquad
B\cap N_{H'}(8)=\{1,5\}.
\]

All 18 marked active swaps from the ten deletion facets move one guard
along a \(G\)-edge to the unoccupied target \(x\), and every resulting
triple dominates \(G\).

### Coloring and parameters

Modulo color permutation, \(H'\) has the unique proper three-coloring

\[
\{0,5,6,10\}\mid
\{1,4,7,9\}\mid
\{2,3,8\}.
\]

The inactive set \(R\) meets all three color classes, so no color is
available for \(x\) in \(H\).  Exact coloring search gives
\(\chi(H')=3\) and \(\chi(H)=4\).

Direct subset and greatest-fixed-point computations give

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)(G-x)
=(3,3,3,3,3).
\]

There are 87 dominating deletion triples initially.  Parallel kernel
deletion removes 19 and then 20, leaving a 48-state eternal family whose
384 unoccupied-attack obligations all pass.

For the target graph,

\[
\boxed{
(\gamma,i,\alpha,\gamma^\infty,\theta)(G)
=(3,3,3,4,4).
}
\]

There are 106 dominating triples.  The three-guard kernel removes
\(47,56,3\) states and becomes empty.  All 404 dominating four-sets
already form a fixed family, satisfying 3,232 unoccupied-attack
obligations.

### Complete rank-three adaptive defeat

The full root \(048\) is removed in the third kernel round.  The exact
attack tree is:

```text
048 --attack 1-->
  move 0: 148 --attack 9-->
    move 4: 189 --attack 7--> no legal dominating successor
    move 8: 149 --attack 2--> no legal dominating successor
  move 4: 018 --attack 11--> no legal dominating successor
```

At every node the displayed branches are **all** one-guard moves along a
\(G\)-edge whose successor still dominates.  Attacks are unoccupied.  No
all-guards move, occupied attack, or nondominating state is admitted.

## 5. Exact claim boundary

The control proves only that the strengthened static implication is
false:

> deletion equality, pure triangle geometry, every-pair common-neighbor
> structure, nonvacuous ridge covariance, a full active root, bipartite
> and totally dominating \(R=B\), and all prescribed one-step successors
> do not force a deletion coloring omitting one color on \(R\).

It does **not** refute the equality-specific dynamic gluing theorem,
because the target graph has \(\gamma^\infty(G)=4\), not 3.  It neither
proves nor refutes the complete \(k=3\) case, and it is not a
counterexample to or a resolution of the universal
\(\gamma\)--\(\theta\) conjecture.

The discovery scans and any minimal-order impression remain `OBSERVED`;
this review checked their manifest hashes but did not promote their
bounded negative outcomes to coverage theorems.  No literature-priority
claim was audited or made.

## 6. Reproduction

From the campaign root:

```text
python3 -I -B -W error \
  reviews/gamma3_bipartite_gluing_hostile/independent_checker.py
```

The frozen output is `independent_result.json`.
