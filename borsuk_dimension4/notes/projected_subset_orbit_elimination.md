# Exact elimination of the projected-subset orbit family

## Family

Let \(U=\mathbb Z/5\mathbb Z\). For every nonempty proper subset
\(A\subset U\), put

\[
 v_A={\bf1}_A-\frac{|A|}{5}{\bf1}\in
 H:=\left\{x\in\mathbb R^5:\sum_i x_i=0\right\}\cong\mathbb R^4.
\]

Consider any finite union of full permutation orbits of the form

\[
 \{r_{k,s}v_A:|A|=k\},\qquad r_{k,s}>0,quad 1\le k\le4.
\]

There may be any finite number of positive radial shells for each subset size.
Negative radii add no cases, because \(-v_A=v_{U\setminus A}\).

## Theorem

Every configuration in this family has a five-colorable diameter graph.
Consequently no union of full projected-subset shells in the standard
four-dimensional representation of \(S_5\) can refute the five-part Borsuk
assertion.

## Distance order

For \(|A|=k\), \(|B|=\ell\), and positive radii \(r,s\),

\[
 \begin{aligned}
 \lVert rv_A-sv_B\rVert^2
 ={}&r^2\frac{k(5-k)}5+s^2\frac{\ell(5-\ell)}5\\
 &-2rs\left(|A\cap B|-\frac{k\ell}{5}\right). \tag{1}
 \end{aligned}
\]

For fixed shells, (1) is strictly decreasing in \(|A\cap B|\). Full
permutation orbits contain pairs at every feasible intersection size.
Therefore, if a pair between two given shells is a global diameter pair, its
intersection has the minimum feasible size

\[
 |A\cap B|=\max(0,k+\ell-5). \tag{2}
\]

Condition (2) says exactly one of the following:

1. \(A\cap B=\varnothing\); or
2. \(A\cup B=U\).

The same conclusion applies to two points in one shell. Different shell pairs
may tie for the global diameter, but every resulting edge still has one of
these two forms.

## A five-coloring

For every nonempty proper \(A\subset U\), its cyclic boundary

\[
 \partial A=\{a\in A:a+1\notin A\}
\]

is nonempty. Choose any deterministic element \(c(A)\in\partial A\); for
example, represent \(U\) by \(\{0,1,2,3,4\}\) and take the least boundary
element in the ordinary integer order. Give every radial copy of \(v_A\) color
\(c(A)\).

If \(A\cap B=\varnothing\), then \(c(A)\in A\) and \(c(B)\in B\), so the
colors differ. If \(A\cup B=U\) and the two colors were the same element
\(a\), then \(a+1\) would lie in neither \(A\) nor \(B\), contradicting
\(A\cup B=U\). Thus every possible diameter edge is bichromatic.

This is a human-readable coloring of a relation graph containing every
diameter graph in the family, so it remains valid at all algebraic parameter
ties and needs no genericity assumption.

## Scope

The full-orbit hypothesis matters. If individual orbit points are deleted, a
pair with nonminimal intersection can become a diameter pair after all farther
orbit mates are removed. The argument does cover arbitrary finite numbers of
full shells and arbitrary positive algebraic or transcendental radii.
