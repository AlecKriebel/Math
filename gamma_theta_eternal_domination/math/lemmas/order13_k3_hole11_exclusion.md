# Near-spanning odd-hole obstruction and the order-13 \(C_{11}\) exclusion

## Status and scope

The theorem below is a direct one-guard proof.  It uses no SAT solver, finite
enumeration, or conjecture assumption.  It proves more than the order-13
`hole11` branch: in every graph with
\(\gamma=\gamma^\infty=3\), every induced odd hole in the complement has at
least three vertices outside it.

The frozen theorem bytes have passed independent adversarial review in
`reviews/order13_k3_math_hostile/`.  Its clean-room checker also reconstructs
the order-13 specialization from the exact two canonical complements; that
computation is not used in the proof.

Throughout, subscripts on rim vertices are read modulo the rim length.
Every attack named below is at an unoccupied vertex, and every considered
response moves exactly one guard along one edge of \(G\).

## 1. Classification with exactly two outside vertices

### Theorem 1 (near-spanning odd-hole obstruction)

Let \(\ell\geq5\) be odd, let \(G\) be a graph on \(\ell+2\) vertices, and
put \(H=\overline G\).  Suppose

\[
 \gamma(G)\geq3
\tag{1.1}
\]

and \(H\) contains a hub-free induced cycle

\[
 R=r_0r_1\cdots r_{\ell-1}r_0.
\tag{1.2}
\]

Then

\[
 \gamma^\infty(G)\geq4.
\tag{1.3}
\]

#### Proof

Suppose instead that \(\gamma^\infty(G)\leq3\).  Equation (1.1) and the
general inequality \(\gamma\leq\gamma^\infty\) give

\[
 \gamma(G)=\gamma^\infty(G)=3.
\tag{1.4}
\]

In particular, an eternal family \(\mathcal D\) of dominating triples
exists.

Let \(x,y\) be the two vertices outside \(R\), and define the sets of rim
vertices missed in \(H\):

\[
 X=\{i:xr_i\notin E(H)\},\qquad
 Y=\{i:yr_i\notin E(H)\}.
\tag{1.5}
\]

Equivalently, \(X\) and \(Y\) are the sets of rim neighbors of \(x\) and
\(y\), respectively, in \(G\).  Hub-freeness makes both sets nonempty.

Because \(\gamma(G)\geq3\), no pair dominates \(G\).  Equivalently, every
pair in \(H\) has an external common \(H\)-neighbor.

We first classify \(X,Y\).

**Claim 1.**

\[
 X\cap Y=\varnothing,
\tag{1.6}
\]

and for every \(i\in X\), \(j\in Y\),

\[
 \operatorname{dist}_{C_\ell}(i,j)=2.
\tag{1.7}
\]

If \(i\in X\cap Y\), consider the adjacent rim pair \(r_i,r_{i+1}\).
Neither \(x\) nor \(y\) is adjacent in \(H\) to \(r_i\), and an adjacent
pair on an induced cycle of length at least five has no common neighbor on
the rim.  The pair would have no common \(H\)-neighbor, a contradiction.
This proves (1.6).

Now take \(i\in X\), \(j\in Y\).  They are distinct by (1.6).  Vertex \(x\)
cannot be their common neighbor because it misses \(r_i\), and \(y\) cannot
be their common neighbor because it misses \(r_j\).  Their required common
neighbor lies on the induced rim.  Two distinct vertices of an induced
cycle of length at least five have a common rim neighbor exactly when their
cyclic distance is two.  This proves (1.7).

Choose an element of \(X\), rotate the rim to call it \(0\), and reflect if
needed.  Equation (1.7) gives

\[
 \varnothing\ne Y\subseteq\{-2,2\}.
\]

If \(Y=\{-2,2\}\), then the only rim vertex at distance two from both
members of \(Y\) is \(0\), so \(X=\{0\}\).  If \(Y=\{2\}\), then
\[
 \{0\}\subseteq X\subseteq\{0,4\}.
\]
The choice \(X=\{0,4\}\), \(Y=\{2\}\) becomes
\(X=\{0\}\), \(Y=\{-2,2\}\) after swapping \(x,y\) and rotating by \(-2\).
Thus, up to a dihedral symmetry of the rim and swapping \(x,y\), exactly
two patterns remain:

\[
\begin{array}{ll}
\text{I:}&X=\{0\},\quad Y=\{2\};\\[2mm]
\text{II:}&X=\{0\},\quad Y=\{-2,2\}.
\end{array}
\tag{1.8}
\]

This classification is purely graph-theoretic; no computation or
isomorphism program is being used.

**Claim 2.**  Except for one small case handled separately below, we may
assume

\[
 xy\notin E(H),
\quad\text{equivalently}\quad xy\in E(G).
\tag{1.9}
\]

The rim vertices adjacent in \(H\) to both \(x\) and \(y\) are exactly
\[
 R-(X\cup Y).
\]
In Pattern I this set has \(\ell-2\) vertices, and in Pattern II it has
\(\ell-3\) vertices.  For \(\ell\geq7\), either size is larger than
\(\alpha(C_\ell)=(\ell-1)/2\), so the set contains two consecutive rim
vertices.  If \(xy\in E(H)\), those consecutive vertices together with
\(x,y\) form a \(K_4\) in \(H\), hence an independent four-set in \(G\).
This contradicts
\(\alpha(G)\leq\gamma^\infty(G)=3\).  The same argument works when
\(\ell=5\) in Pattern I.

The only exception is \(\ell=5\), Pattern II.  If \(xy\in E(H)\), the
independent triple
\[
 D=\{r_1,r_2,x\}
\]
must belong to every eternal family of triples.  Attack \(r_4\).  The guard
at \(x\) cannot move.  Moving \(r_1\) leaves
\(\{r_2,r_4,x\}\), which does not dominate \(r_3\); moving \(r_2\) leaves
\(\{r_1,r_4,x\}\), which does not dominate \(y\).  Thus \(D\) has no legal
dominating response, contradicting \(D\in\mathcal D\).

We may therefore assume (1.9) in all remaining cases.  It remains to rule
out an eternal family for the two patterns in (1.8).

### The uniform attack for odd \(\ell\geq9\)

Assume first that \(\ell\geq9\).  In both patterns,

\[
 D=\{r_4,r_5,x\}
\tag{1.10}
\]

is independent in \(G\): \(r_4r_5\) is a rim edge of \(H\), and \(x\)
misses in \(H\) only \(r_0\).  Hence \(D\in\mathcal D\).

Attack \(r_0\).  If \(x\) moves, the successor
\(\{r_0,r_4,r_5\}\) leaves \(y\) undominated: the rim neighbors of \(y\) in
\(G\) are \(r_2\), and possibly \(r_{\ell-2}\), while the guard at \(x\)
has left.  The other two possible successors are

\[
 B=\{r_0,r_4,x\}
 \quad\text{and}\quad
 S_5=\{r_0,r_5,x\}.
\tag{1.11}
\]

State \(B\) cannot belong to an eternal family.  Attack \(r_2\).  The guard
at \(x\) cannot move.  Moving \(r_0\) leaves
\(\{r_2,r_4,x\}\), which does not dominate \(r_3\), while moving \(r_4\)
leaves \(\{r_0,r_2,x\}\), which does not dominate \(r_1\).  Therefore
closure from \(D\) forces \(S_5\in\mathcal D\).

For odd \(j\) with

\[
 5\leq j<\ell-4,
\]

suppose

\[
 S_j=\{r_0,r_j,x\}\in\mathcal D.
\]

Attack \(r_{j+2}\).  The guard at \(x\) cannot move.  Moving \(r_0\) leaves
\(\{r_j,r_{j+2},x\}\), which does not dominate \(r_{j+1}\).  Thus the only
possible response moves \(r_j\) and forces

\[
 S_{j+2}=\{r_0,r_{j+2},x\}\in\mathcal D.
\tag{1.12}
\]

This gives \(S_{\ell-4}\in\mathcal D\).  Attack \(r_{\ell-2}\).  Moving
\(r_0\) leaves \(r_{\ell-3}\) undominated.  Moving \(r_{\ell-4}\) leaves
the state
\(\{r_0,r_{\ell-2},x\}\), which does not dominate \(r_{\ell-1}\).
The guard at \(x\) cannot move.  There is no response, a contradiction.

The case \(\ell=9\) is included: \(S_5=S_{\ell-4}\), so the final attack is
made immediately and the intermediate induction is empty.

### The two small odd rims

It remains to treat \(\ell=5,7\) under (1.9).  The following short attack
trees list every successor that can still dominate.  Each root is an
independent triple and hence is forced into \(\mathcal D\).

For \(\ell=5\), Pattern I, start from
\[
 D=\{r_0,r_1,y\}
\]
and attack \(r_3\).  Moving \(r_1\) leaves \(r_4\) undominated, and \(y\)
cannot move, so the response is forced to
\[
 P=\{r_1,r_3,y\}.
\]
At \(P\), attack \(r_2\).  The rim guards cannot move because each is
consecutive to \(r_2\).  Moving \(y\) leaves
\(\{r_1,r_2,r_3\}\), which does not dominate \(x\).  This is impossible.

For \(\ell=5\), Pattern II, use the same root and first attack.  The only
possibly dominating successors are
\[
 P=\{r_1,r_3,y\},
 \qquad
 Q=\{r_0,r_1,r_3\}.
\]
At \(P\), attack \(r_2\): the only moving guard is \(y\), and its successor
\(\{r_1,r_2,r_3\}\) leaves \(x\) undominated.  At \(Q\), attack \(r_2\):
the only possible move is from \(r_0\), with the same nondominating
successor.  Neither branch can belong to \(\mathcal D\).

For \(\ell=7\), Pattern I, start from
\[
 D=\{r_0,r_1,y\}
\]
and attack \(r_3\).  The only possibly dominating successors are
\[
 P=\{r_1,r_3,y\},
 \qquad
 Q=\{r_0,r_3,y\}.
\]
At \(P\), attack \(r_2\).  The two rim guards cannot move, and moving \(y\)
leaves \(\{r_1,r_2,r_3\}\), which does not dominate \(x\).  At \(Q\),
attack \(r_5\).  Moving \(r_0\) leaves \(r_4\) undominated, moving \(r_3\)
leaves \(r_6\) undominated, and \(y\) cannot move.  Again neither branch can
belong to \(\mathcal D\).

For \(\ell=7\), Pattern II, start from
\[
 D=\{r_1,r_2,x\}
\]
and attack \(r_6\).  The guard at \(x\) cannot move.  The other two moves
give the only possibly dominating successors
\[
 P=\{r_2,r_6,x\},
 \qquad
 Q=\{r_1,r_6,x\}.
\]
At \(P\), attack \(r_4\).  Moving \(r_2\) leaves \(r_5\) undominated,
moving \(r_6\) leaves \(r_3\) undominated, and \(x\) cannot move.  At \(Q\),
attack \(r_0\).  The two rim guards cannot move because they are the two rim
neighbors of \(r_0\); moving \(x\) leaves
\(\{r_0,r_1,r_6\}\), which does not dominate \(y\).

Every possible pattern and response has now produced a contradiction.
Therefore an eternal family of triples cannot exist.  Together with
\(\gamma(G)\geq3\), this proves
\(\gamma^\infty(G)\geq4\). \(\square\)

## 2. Consequences for equality graphs

### Corollary 2 (three outside vertices are necessary)

If

\[
 \gamma(G)=\gamma^\infty(G)=3
\tag{2.1}
\]

and \(H=\overline G\) contains an induced odd hole \(C_\ell\), then at least
three vertices of \(H\) lie outside that hole.

#### Proof

By the accepted odd-wheel obstruction C-014, every induced odd hole in
\(H\) is hub-free.

The endpoints of each rim edge have an external common \(H\)-neighbor,
because \(\gamma(G)=3\).  Hence the hole cannot be spanning.  If exactly one
vertex lay outside, that vertex would have to be a common neighbor of the
endpoints of every rim edge and would therefore be a hub.  If exactly two
vertices lay outside, Theorem 1 would give
\(\gamma^\infty(G)\geq4\).  All three possibilities contradict (2.1), so
there are at least three outside vertices. \(\square\)

Equivalently, every induced odd hole in the complement of a parameter-three
equality graph has length at most

\[
 |V(G)|-3.
\tag{2.2}
\]

This is a structural theorem for all such equality graphs; it does not use
\(\theta(G)>\gamma(G)\) and is not restricted to counterexamples.

### Corollary 3 (order-13 `hole11` branch is empty)

There is no order-13 graph \(G\) satisfying

\[
 \gamma(G)=\gamma^\infty(G)=3
\tag{2.3}
\]

whose complement contains an induced \(C_{11}\).

#### Proof

Such a hole would have exactly two outside vertices.  It is hub-free by
C-014, so Theorem 1 gives
\(\gamma^\infty(G)\geq4\), contrary to (2.3). \(\square\)

Combining Corollary 3 with the accepted C-052 cover strengthens the
order-13, parameter-three synthesis union from

\[
 C_5,\ C_7,\ C_9,\ C_{11}
\]

to

\[
 C_5,\ C_7,\ C_9.
\tag{2.4}
\]

Thus no SAT proof production is needed for the `hole11` branch once this
direct proof has passed adversarial review.  The three remaining templates
still overlap and still require separate treatment.

## 3. Two exact infinite near-miss families

The classification also gives explicit examples showing that the lower bound
in Theorem 1 is sharp.

For every odd \(\ell\geq5\), define two graphs \(H_\ell^1,H_\ell^2\) on

\[
 \{r_0,\ldots,r_{\ell-1},x,y\}
\]

as follows:

1. the rim induces \(C_\ell\);
2. \(xy\notin E(H_\ell^t)\);
3. in both families, \(x\) is adjacent to every rim vertex except \(r_0\);
4. in \(H_\ell^1\), \(y\) is adjacent to every rim vertex except \(r_2\);
5. in \(H_\ell^2\), \(y\) is adjacent to every rim vertex except
   \(r_{-2},r_2\).

Put

\[
 G_\ell^t=\overline{H_\ell^t}.
\]

### Theorem 4 (exact parameters of the canonical families)

For every odd \(\ell\geq5\) and \(t\in\{1,2\}\),

\[
 \gamma(G_\ell^t)
 =i(G_\ell^t)
 =\alpha(G_\ell^t)
 =3
\tag{3.1}
\]

and

\[
 \gamma^\infty(G_\ell^t)
 =\theta(G_\ell^t)
 =4.
\tag{3.2}
\]

#### Proof

First, every pair of vertices in \(H_\ell^t\) has an external common
neighbor.

- Two rim vertices at cyclic distance two have their intermediate rim
  vertex.  For any other rim pair, \(x\) is a common neighbor unless the
  pair contains \(r_0\), and \(y\) is a common neighbor unless it contains
  one of the one or two vertices missed by \(y\).  The only pairs for which
  both outsiders are unavailable are
  \(\{r_0,r_2\}\) and, in the second family,
  \(\{r_0,r_{-2}\}\); these are distance-two pairs and already have an
  intermediate rim neighbor.
- For the pair \(x,y\), any rim vertex outside their combined miss sets is a
  common neighbor.
- For \(x,r_i\), at least one of the two rim neighbors of \(r_i\) is not
  \(r_0\), and that vertex is a common neighbor.
- For \(y,r_i\), at least one of the two rim neighbors of \(r_i\) lies
  outside the miss set of \(y\).  In the second family the two missed
  indices \(-2,2\) cannot be of the form \(\{i-1,i+1\}\): equivalently,
  \(4\not\equiv\pm2\pmod\ell\) for odd \(\ell\geq5\).

By the pair/common-neighbor dictionary, no pair dominates \(G_\ell^t\), so

\[
 \gamma(G_\ell^t)\geq3.
\tag{3.3}
\]

The graph \(H_\ell^t\) has no \(K_4\).  The rim is triangle-free, a clique
containing only one outsider would need three mutually adjacent rim
vertices, and a clique containing both outsiders is impossible because
\(xy\notin E(H_\ell^t)\).  On the other hand, \(x\) together with any rim
edge avoiding \(r_0\) forms a triangle.  Hence

\[
 \alpha(G_\ell^t)=\omega(H_\ell^t)=3.
\tag{3.4}
\]

An independent triple of maximum size is maximal and therefore dominates.
Thus \(\gamma(G_\ell^t)\leq3\).  Equations (3.3)--(3.4), followed by
\(\gamma\leq i\leq\alpha\), prove (3.1).

We next compute the chromatic number of \(H_\ell^t\).  Suppose it had a
proper three-coloring, and call the color of \(x\) color A.  Every rim
vertex except \(r_0\) is adjacent to \(x\), so the path

\[
 r_1,r_2,\ldots,r_{\ell-1}
\]

must alternate the other two colors B and C.  This path has an even number
of vertices, so its endpoints receive different colors.  Since \(r_0\) is
adjacent to both endpoints, \(r_0\) must receive color A.

Vertex \(y\) is adjacent to \(r_0\), so it sees color A.  It also sees both
colors B and C on the alternating path: deleting \(r_2\), or deleting
\(r_2,r_{\ell-2}\), leaves vertices of both parities on that path for every
odd \(\ell\geq5\).  Hence no color remains for \(y\), a contradiction.
Therefore \(\chi(H_\ell^t)\geq4\).

Conversely, properly three-color the odd rim and give the nonadjacent
vertices \(x,y\) one new fourth color.  This proves

\[
 \theta(G_\ell^t)=\chi(H_\ell^t)=4.
\tag{3.5}
\]

The selected rim is hub-free and has exactly two outside vertices, while
(3.3) holds.  Theorem 1 gives
\(\gamma^\infty(G_\ell^t)\geq4\).  The general clique-cover strategy gives
\(\gamma^\infty(G_\ell^t)\leq\theta(G_\ell^t)=4\).  This proves (3.2).
\(\square\)

No novelty claim is made for Theorem 4 until the family has been compared
against the construction literature.

For \(\ell=11\), the two graphs \(G_{11}^1,G_{11}^2\) have the following
Graph6 strings:

```text
LUzvvz}~r~O?G@
LUzvvz}~r~O?GD
```

The clean-room checker in `reviews/order13_k3_math_hostile/` independently
reproduces (3.1)--(3.2) and both displayed Graph6 strings.  This is a
regression check; the parameter proof is Theorem 4.

## 4. Hostile audit checklist

The proof depends on the following points, each exposed above.

1. \(X,Y\) are nonempty because the selected hole is hub-free.
2. The common-neighbor condition follows from
   \(\gamma(G)\geq3\), not from well-coveredness.
3. Cross pairs in \(X\times Y\) are distinct because
   \(X\cap Y=\varnothing\), and their only possible common neighbors lie on
   the rim.
4. The two patterns in (1.8) are exhaustive only up to a dihedral rim
   symmetry and swapping \(x,y\); both operations relabel the whole graph.
5. The \(K_4\) argument forcing \(xy\notin E(H)\) has one genuine exception,
   \(\ell=5\), Pattern II, which is handled separately.
6. Every root state used in an attack tree is an independent triple, so the
   maximum-independent-state lemma forces it into every eternal family of
   triples.
7. Every named attack is unoccupied.
8. Every listed successor removes one guard and inserts the attacked vertex.
9. Each rejected successor has an explicit undominated witness.
10. No inference uses \(\theta\), an UNSAT output, or the
    \(\gamma\)--\(\theta\) conjecture.

The strongest claim proved here is the general near-spanning-hole
obstruction in Theorem 1.  The order-13 \(C_{11}\) exclusion is a strict
corollary, not a finite solver claim.
