# Eliminating the odd-antihole branch when \(k=3\)

## Status

The cycle value in Lemma 1 is classical: Goddard--Hedetniemi--Hedetniemi
(2005, Theorem 3, attributing the result to Burger et al.) states
\(\gamma^\infty(C_n)=(n+1)/2\) for odd \(n\).  A self-contained proof of the
only needed case is included here.  The complement-side consequence was
derived on 2026-07-25 and was not located in the audited sources.  This note
is awaiting a separate hostile audit and must not yet be used as an accepted
campaign claim.

## 1. The seven-cycle obstruction

**Lemma 1.**  In the one-guard-moves model,
\[
  \gamma^\infty(C_7)=4.
\]

**Proof.**  Partitioning the cycle into three edges and one singleton gives
\(\theta(C_7)\leq4\), so the standard clique-cover strategy gives
\(\gamma^\infty(C_7)\leq4\).  Also
\(\alpha(C_7)=3\leq\gamma^\infty(C_7)\) by the parameter chain.  It remains
to rule out three guards.

For a dominating triple on a cycle, record the three numbers of unoccupied
vertices in the cyclic gaps between consecutive guards.  On \(C_7\) these
numbers sum to four.  Domination says that no gap has length more than two.
Consequently every dominating triple has one of the two gap multisets
\[
  \{2,1,1\}\quad\text{or}\quad\{2,2,0\}.
\]
Call these types A and B.

Every type-B triple is equivalent under a dihedral symmetry of \(C_7\) to
\(\{0,1,4\}\), with vertices read modulo seven.  Attack vertex \(3\).
Among the occupied vertices, only \(4\) is adjacent to \(3\), so the only
possible move produces \(\{0,1,3\}\).  That triple does not dominate vertex
\(5\), whose two neighbors are \(4\) and \(6\).  Thus a type-B triple cannot
belong to any eternal three-guard family.

Now \(\{0,2,4\}\) is a maximum independent set.  If an eternal three-guard
family existed, the maximum-independent-state lemma would force this triple
to belong to it.  Attack vertex \(1\).  The only possible guards are \(0\)
and \(2\).  Moving \(0\) gives \(\{1,2,4\}\), which fails to dominate vertex
\(6\).  Moving \(2\) gives the type-B triple \(\{0,1,4\}\), which cannot
belong to the family by the preceding paragraph.  Hence the attack has no
allowed response inside an eternal family, a contradiction.

Therefore three guards do not suffice, while four do. \(\square\)

## 2. Consequence for the complement search

**Theorem 2 (odd-antihole elimination at parameter three).**  Let
\(G\) satisfy
\[
  \alpha(G)=\gamma^\infty(G)=3,
\]
and put \(H=\overline G\).  If \(H\) is imperfect, then \(H\) contains an
induced odd hole.  In particular, the odd-antihole alternative in the Strong
Perfect Graph Theorem introduces no additional search branch.

**Proof.**  The Strong Perfect Graph Theorem gives an induced odd hole or an
induced odd antihole in \(H\).  Suppose the latter has length \(2q+1\).
Its clique number is \(q\), so
\[
  q\leq\omega(H)=\alpha(G)=3.
\]
Thus its length is five or seven.  The five-vertex odd antihole is \(C_5\)
itself and is already an odd hole.

The only remaining possibility is an induced
\(\overline{C_7}\) in \(H\).  On the same vertex set, \(G\) induces \(C_7\).
By induced-subgraph monotonicity and Lemma 1,
\[
  \gamma^\infty(G)\geq\gamma^\infty(C_7)=4,
\]
contrary to the hypothesis.  Therefore \(H\) contains an induced odd hole.
\(\square\)

Combining this theorem with the odd-wheel obstruction in
`k3_structural_day1.md` shows that every such odd hole is hub-free.  The
common-neighbor condition from `complement_k3_dictionary.md` then forces at
least two vertices outside the hole.  Hence an order-12 parameter-three
counterexample complement needs only three overlapping synthesis branches:
an induced hub-free \(C_5\), \(C_7\), or \(C_9\).
