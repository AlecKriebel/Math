# Day-1 structural restrictions for the \(k=3\) complement target

## Status

The statements below were proved directly on 2026-07-25 and accepted by the
separate hostile audit in `reviews/k3_structural_hostile_review.md`.  The
finite counts at the end are computational observations, not theorem claims.

Let \(G\) be a finite simple graph and put \(H=\overline G\).  An **induced
odd wheel** in \(H\) consists of an induced odd cycle
\[
  v_0v_1\cdots v_{2q}v_0,\qquad q\geq2,
\]
together with a vertex \(h\) outside the cycle that is adjacent in \(H\) to
every \(v_j\).  Thus the induced graph is
\(K_1\mathbin{\vee}C_{2q+1}\).

## 1. Two static constraints are automatic

**Lemma 1.**  Suppose that \(\omega(H)=3\) and every pair of distinct
vertices of \(H\) has a common neighbor.  Then:

1. every maximal clique of \(H\) is a triangle;
2. \(H\) has diameter at most two; and
3. \(\delta(H)\geq2\).

**Proof.**  Every edge \(uv\) has a common neighbor, so it is contained in a
triangle.  No vertex is isolated: an isolated vertex could have no common
neighbor with any other vertex.  Consequently, no clique of size one or two
is maximal.  Since \(\omega(H)=3\), every maximal clique has size three.

Adjacent vertices are at distance one, and nonadjacent vertices have a common
neighbor and hence are at distance two.  This proves the diameter assertion.
Finally, a vertex of degree zero is impossible.  If \(v\) had unique neighbor
\(u\), then a common neighbor of the pair \(u,v\) would be a second neighbor
of \(v\), also impossible.  Hence every degree is at least two. \(\square\)

In particular, condition (3) in the exact target of
`complement_k3_dictionary.md` is logically redundant once conditions
\(\omega(H)=3\) and “every pair has a common neighbor” are enforced.  It
remains useful as a consistency check, but it need not be a separate
generation constraint.

## 2. Odd wheels are forbidden

**Theorem 2 (odd-wheel obstruction).**  If
\(\gamma^\infty(G)=3\), then \(\overline G\) contains no induced odd wheel.

**Proof.**  Suppose that \(H=\overline G\) contains an induced
\[
  W=K_1\mathbin{\vee}C_{2q+1}
  \quad(q\geq2).
\]
Taking complements on this vertex set gives
\[
  G[V(W)]=K_1\mathbin{\dot\cup}\overline{C_{2q+1}}.
\]
Eternal domination is additive over components,
\(\gamma^\infty(K_1)=1\), and
\(\gamma^\infty(\overline{C_{2q+1}})=3\).  Therefore
\[
  \gamma^\infty(G[V(W)])=4.
\]
Eternal domination is monotone under taking induced subgraphs, so
\[
  \gamma^\infty(G)\geq
  \gamma^\infty(G[V(W)])=4,
\]
contrary to the hypothesis. \(\square\)

All three ingredients used in this proof have self-contained proofs in
`math/reductions.md`: component additivity is Proposition 5,
induced-subgraph monotonicity is Lemma 8, and the odd-antihole calculation is
Lemma 9.

For the smallest wheel there is also a one-attack certificate that uses the
forced maximum-independent states directly.

**Lemma 3 (local \(W_5\) certificate).**  Suppose
\(\alpha(G)=\gamma^\infty(G)=3\).  If \(H=\overline G\) contains an induced
\(W_5\), then no eternal three-guard family exists.

**Proof.**  Let \(c\) be the wheel center and let
\(v_0v_1v_2v_3v_4v_0\) be its induced rim.  The triangle
\[
  S=\{c,v_0,v_1\}
\]
in \(H\) is a maximum independent set in \(G\), so every eternal
three-guard family would have to contain \(S\).  Attack \(v_3\).
The guard at \(c\) cannot move because \(cv_3\in E(H)\), while the only two
other possible moves fail domination:

* after moving \(v_0\), the configuration
  \(\{c,v_1,v_3\}\) leaves \(v_2\) undominated in \(G\), because \(v_2\) is
  adjacent in \(H\) to all three occupied vertices;
* after moving \(v_1\), the configuration
  \(\{c,v_0,v_3\}\) leaves \(v_4\) undominated for the same reason.

Thus the allowed unoccupied attack at \(v_3\) has no legal dominating
successor, a contradiction. \(\square\)

This six-vertex certificate can be emitted immediately when a synthesis
candidate contains an induced \(W_5\); no configuration fixed-point
calculation is needed.

## 3. A finite template split for \(n=12,k=3\)

**Theorem 4 (SPGT template split).**  Suppose that \(G\) is a
parameter-three counterexample and \(H=\overline G\).  Then \(H\) contains at
least one of the following:

1. a hub-free induced odd hole; or
2. an induced \(\overline{C_7}\).

Here “hub-free” means that no vertex outside the hole is adjacent to every
vertex of the hole.

Moreover, an induced odd hole in \(H\) has at least two vertices outside it.
Consequently, when \(|V(H)|=12\), the odd-hole branch needs only the lengths
\[
  5,\ 7,\ 9.
\]

**Proof.**  The complement dictionary gives
\[
  \omega(H)=3<\chi(H).
\]
Hence \(H\) is imperfect.  By the Strong Perfect Graph Theorem, \(H\)
contains an induced odd hole or an induced odd antihole.

Every induced odd hole is hub-free by Theorem 2: a hub together with the
hole would be an induced odd wheel.  If \(H\) contains an odd antihole
\(\overline{C_{2q+1}}\), then
\[
  q=\omega(\overline{C_{2q+1}})\leq\omega(H)=3.
\]
Thus its length is five or seven.  The five-vertex odd antihole is again
\(C_5\), so it belongs to the odd-hole branch; the only additional
antihole template is \(\overline{C_7}\).

It remains to bound the hole length.  Let \(C\) be an induced odd hole in
\(H\).  The endpoints of any rim edge have no common neighbor on \(C\).
Because every pair in \(H\) has a common neighbor, every rim edge therefore
has a common neighbor outside \(C\).  There cannot be zero outside vertices.
If there were exactly one, that one vertex would have to be adjacent to both
endpoints of every rim edge, hence to every vertex of \(C\); it would be a
hub, contrary to Theorem 2.  Thus at least two vertices lie outside \(C\),
so \(|C|\leq |V(H)|-2\).  At order twelve the possible odd lengths at least
five are exactly \(5,7,9\). \(\square\)

This gives a sound direct-synthesis split at \((n,k)=(12,3)\):

* force an induced \(\overline{C_7}\); or
* force an induced \(C_5,C_7\), or \(C_9\), and forbid every external vertex
  from being complete to its rim.

The branches may overlap.  They are exhaustive, not disjoint.

## 4. Small-order pruning measurement

The reproducible probe `src/search/k3_wheel_probe.py` streamed connected
unlabeled graphs from nauty `geng` and used both exact evaluators
independently.  Among graphs \(G\) satisfying the static prefilter
\[
  \gamma(G)=\alpha(G)=3<\theta(G),
\]
it obtained:

| order | static prefilter | rejected by an odd wheel in \(\overline G\) |
|---:|---:|---:|
| 6 | 0 | 0 |
| 7 | 5 | 2 |
| 8 | 78 | 47 |

The two implementations agreed on every parameter value, eternal value, and
wheel decision in this table.  These counts are evidence that the obstruction
is a useful early filter (it removes \(47/78\) of the order-eight static
targets), but they are not used in any proof above.
