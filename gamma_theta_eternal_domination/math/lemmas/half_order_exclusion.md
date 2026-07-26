# The half-order parameter cannot host a connected counterexample

## Status

`PROVED`, conditional only on the classical extremal characterization quoted
as Theorem 1 below.  The deduction from that theorem is self-contained.

This note concerns the standard one-guard eternal domination model fixed in
`math/reductions.md`.  It does not use an all-guards-move parameter.

## Classical input

The corona \(F\circ K_1\) is obtained from a graph \(F\) by adjoining, for
each \(v\in V(F)\), one new leaf \(v'\) adjacent only to \(v\).

**Theorem 1 (Payan--Xuong; independently Fink--Jacobson--Kinch--Roberts).**
Let \(G\) be a graph of even order \(n\) with no isolated vertices.  Then
\[
  \gamma(G)=\frac n2
\]
if and only if every component of \(G\) is either \(C_4\) or
\(F\circ K_1\) for some connected graph \(F\).

Primary bibliographic identifiers:

- C. Payan and N. H. Xuong, *Domination-balanced graphs*,
  Journal of Graph Theory **6** (1982), 23--32,
  <https://doi.org/10.1002/jgt.3190060104>.
- J. F. Fink, M. S. Jacobson, L. F. Kinch, and J. Roberts,
  *On graphs having domination number half their order*,
  Periodica Mathematica Hungarica **16** (1985), 287--293,
  <https://doi.org/10.1007/BF01848079>.

Only the displayed characterization is imported.  The remainder of this
note is proved directly.

## Clique covers of the extremal graphs

**Lemma 2.**  If \(Q=C_4\), then
\[
  \gamma(Q)=\alpha(Q)=\theta(Q)=2.
\]

**Proof.**
Two opposite vertices are independent and dominate, so
\(\gamma(Q)\leq2\) and \(\alpha(Q)\geq2\).  No one vertex dominates \(C_4\),
and no independent set has three vertices, hence
\(\gamma(Q)=\alpha(Q)=2\).  Two disjoint edges partition \(V(Q)\) into
cliques, so \(\theta(Q)\leq2\); the inequality
\(\alpha(Q)\leq\theta(Q)\) gives the reverse bound. \(\square\)

**Lemma 3.**  Let \(F\) have \(m\geq1\) vertices and let
\(Q=F\circ K_1\).  Then
\[
  \gamma(Q)=\alpha(Q)=\theta(Q)=m.
\]

**Proof.**
Write the support--leaf pairs as
\(\{v_1,v'_1\},\ldots,\{v_m,v'_m\}\).  Every dominating set contains
at least one member of each pair: the leaf \(v'_j\) has no neighbor outside
its pair.  Choosing all support vertices dominates \(Q\), so
\(\gamma(Q)=m\).

The \(m\) leaves are independent, hence \(\alpha(Q)\geq m\).  An independent
set contains at most one member of each adjacent support--leaf pair, hence
\(\alpha(Q)\leq m\).  Thus \(\alpha(Q)=m\).

Finally, the \(m\) support--leaf edges partition \(V(Q)\) into cliques, so
\(\theta(Q)\leq m\).  Since every clique partition needs distinct parts for
the members of an independent set, \(\alpha(Q)\leq\theta(Q)\).  Therefore
\(\theta(Q)=m\). \(\square\)

**Proposition 4.**  If \(G\) has no isolated vertices and
\(\gamma(G)=|V(G)|/2\), then
\[
  \gamma(G)=\theta(G).
\]

**Proof.**
Theorem 1 decomposes \(G\) into components of the two types in Lemmas 2 and
3.  On every component the domination and clique-cover numbers agree.
Both parameters are additive over components, by Proposition 5 of
`math/reductions.md`, so they agree on \(G\). \(\square\)

## Consequences for the gamma--theta campaign

**Corollary 5.**  If a connected graph \(G\) of order \(n\geq2\) satisfies
\[
  \gamma(G)=\gamma^\infty(G)<\theta(G),
\]
and \(k=\gamma(G)\), then
\[
  k<\frac n2.
\]

**Proof.**
A connected graph of order at least two has no isolated vertices.  Ore's
bound gives \(k\leq n/2\).  If equality held, Proposition 4 would give
\(\theta(G)=\gamma(G)\), contrary to the displayed strict inequality.
\(\square\)

Together with the independently proved minimum parameter \(k\geq3\), this
gives the useful order constraint
\[
  n\geq 2k+1
\]
for every connected counterexample.

**Corollary 6.**  A connected counterexample of order \(12\) has common
parameter only in
\[
  k\in\{3,4,5\}.
\]
In particular, the half-order case \(k=6\) needs no synthesis search.

The certified result C-035 already excludes \(k=3\) at order \(12\).
Consequently the only remaining connected order-12 parameter slices are
\(k=4\) and \(k=5\).

## Scope

This note does not exclude either remaining slice, does not prove absence of
all order-12 counterexamples, and does not resolve the universal conjecture.
It supplies a general parameter restriction and removes the connected
\((n,k)=(12,6)\) lane.

For disconnected graphs, the campaign continues to use the proved
component-additivity reduction: a counterexample has a connected
counterexample component.  Corollary 5 applies to that component with its
own order and domination parameter.
