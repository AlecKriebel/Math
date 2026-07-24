# Exact maximal quarter-grid extensions of the 51 selected K11 atoms

## Theorem

Let

\[
V=\{-1,-3/4,-1/2,-1/4,0,1/4,1/2\}.
\]

For \(0\leq i<51\), let \(A_i\) be the eleven-point rank-five
spherical code recorded as atom \(i\) in
`../direct_k11_triangle_extension.json`.  Among all spherical codes in
\(S^4\) which contain an isometric copy of \(A_i\) and whose every inner
product lies in \(V\), the exact maximum cardinalities are as follows.

| Atom | Extra points | Total | Atom | Extra points | Total | Atom | Extra points | Total |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 19 | 30 | 17 | 23 | 34 | 34 | 11 | 22 |
| 1 | 21 | 32 | 18 | 29 | 40 | 35 | 15 | 26 |
| 2 | 17 | 28 | 19 | 26 | 37 | 36 | 15 | 26 |
| 3 | 21 | 32 | 20 | 26 | 37 | 37 | 19 | 30 |
| 4 | 19 | 30 | 21 | 17 | 28 | 38 | 19 | 30 |
| 5 | 19 | 30 | 22 | 15 | 26 | 39 | 11 | 22 |
| 6 | 29 | 40 | 23 | 29 | 40 | 40 | 11 | 22 |
| 7 | 29 | 40 | 24 | 19 | 30 | 41 | 29 | 40 |
| 8 | 19 | 30 | 25 | 8 | 19 | 42 | 15 | 26 |
| 9 | 29 | 40 | 26 | 19 | 30 | 43 | 29 | 40 |
| 10 | 29 | 40 | 27 | 29 | 40 | 44 | 29 | 40 |
| 11 | 15 | 26 | 28 | 19 | 30 | 45 | 15 | 26 |
| 12 | 17 | 28 | 29 | 7 | 18 | 46 | 15 | 26 |
| 13 | 17 | 28 | 30 | 8 | 19 | 47 | 29 | 40 |
| 14 | 17 | 28 | 31 | 8 | 19 | 48 | 26 | 37 |
| 15 | 19 | 30 | 32 | 9 | 20 | 49 | 29 | 40 |
| 16 | 26 | 37 | 33 | 19 | 30 | 50 | 29 | 40 |

In particular, none of these 51 atoms is contained in a 41-point
quarter-grid spherical code.

## Exact reduction to a finite graph

All Gram entries are scaled by four.  Thus the diagonal value is \(4\)
and the allowed off-diagonal values are

\[
W=\{-4,-3,-2,-1,0,1,2\}.
\]

For each atom the first five vertices form a basis.  Let \(B\) be their
scaled \(5\times5\) Gram matrix and let \(D=\det B\).  The verifier
checks Sylvester's criterion exactly and obtains \(D>0\).  It also
checks

\[
B\operatorname{adj}(B)=D I
\]

and, for all eleven source vertices, checks every Gram entry against
the basis representation.  Hence this is not an assumed rank
condition: the complete source Gram matrix is verified to be the Gram
matrix of eleven vectors spanning a five-dimensional Euclidean space.

Any possible additional point \(x\) is uniquely determined by the row

\[
w=(4\langle x,a_0\rangle,\ldots,4\langle x,a_4\rangle)\in W^5.
\]

It is a unit vector exactly when

\[
w^{\mathsf T}\operatorname{adj}(B)w=4D. \tag{1}
\]

If \(r_j\) is the scaled basis-correlation row of source vertex \(a_j\),
then its scaled inner product with \(x\) is exactly

\[
4\langle a_j,x\rangle
 =\frac{r_j^{\mathsf T}\operatorname{adj}(B)w}{D}. \tag{2}
\]

The verifier enumerates all \(7^5=16807\) rows in \(W^5\), keeps exactly
the rows satisfying (1), and requires the six values in (2) for
\(5\leq j<11\) to be integers in \(W\).  This is a complete
enumeration, since the first five source vertices are a basis.  It
produces between 12 and 71 candidates, depending on the atom.

Make two retained rows \(u,w\) adjacent precisely when

\[
\frac{u^{\mathsf T}\operatorname{adj}(B)w}{D}\in W. \tag{3}
\]

A set of additional points is therefore admissible exactly when its
rows form a clique in this graph.

## Exact optimality witnesses

For every one of the 51 graphs, the certificate contains:

1. a clique of size \(m_i\), proving \(\omega\geq m_i\); and
2. a proper vertex coloring with \(m_i\) colors, proving
   \(\omega\leq m_i\).

The independent verifier regenerates the candidates and every graph
edge from the source Gram matrices.  It then checks every pair in the
claimed clique and every edge in the claimed coloring.  Consequently

\[
\omega=m_i
\]

by two elementary, exact witnesses.  The maximum total cardinality is
therefore \(11+m_i\), giving the table above.  The branch-and-bound
clique search and the coloring heuristic used during discovery are not
trusted by the verifier.

The source vertices themselves cannot be counted again.  Each of the
first five has a basis self-correlation \(4\notin W\); each of the
remaining six fails its own source-correlation test for the same
reason.

## Reproduction

From the repository root:

```text
PYTHONPATH=. .venv/bin/python experiments/centered_quarter_k6_rank/k11/maximal_extension/verify_certificate.py
PYTHONPATH=. .venv/bin/python -m unittest -v experiments/centered_quarter_k6_rank/k11/maximal_extension/test_certificate.py
```

The verifier pins:

- source SHA-256
  `f02f52aed4d843434ef6b16c31d03e6176f0566d0a9fa12d02b50b0ec0aee54a`;
- maximal-extension certificate SHA-256
  `c0d75a0d9422a9aef646d90280c0f0d0d984e9981ac77da1bf0063818d7b2465`.

All arithmetic used in the proof is integer arithmetic.  There are no
floating-point comparisons, tolerances, solver statuses, strict/open
boundary substitutions, or PSD approximations.  The value \(2\),
corresponding to the allowed boundary inner product \(1/2\), is
included throughout.

## Scope

This is an exact support-specific theorem, not a resolution of the
five-dimensional kissing-number problem.  It does not prove that every
K11 quarter-grid subcode is one of these atoms, and it says nothing
about configurations having inner products outside \(V\).  In
particular, the result cannot by itself be promoted to
\(\tau(5)\leq40\).
